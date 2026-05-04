"""Orquestrador principal do pipeline."""
import logging
from typing import List

from scrapers.base import BaseScraper, Noticia
from scrapers.campograndenews import CampoGrandeNewsScraper
from scrapers.topmidianews import TopMidiaNewsScraper
from scrapers.midiamax import MidiaMaxScraper

from core.database import Database
from core.rewriter import DeepSeekRewriter
from publishers.wordpress import WordPressPublisher

from config.settings import PORTAIS, MAX_NOTICIAS_POR_PORTAL

logger = logging.getLogger(__name__)


class Orquestrador:
    def __init__(self):
        self.db = Database()
        self.rewriter = DeepSeekRewriter()
        self.publisher = WordPressPublisher()
        self.scrapers: List[BaseScraper] = []
        if PORTAIS["campograndenews"]["ativo"]:
            self.scrapers.append(CampoGrandeNewsScraper())
        if PORTAIS["topmidianews"]["ativo"]:
            self.scrapers.append(TopMidiaNewsScraper())
        if PORTAIS["midiamax"]["ativo"]:
            self.scrapers.append(MidiaMaxScraper())

    def executar_ciclo(self):
        logger.info("=" * 60)
        logger.info("Iniciando ciclo")
        logger.info("=" * 60)
        total = 0
        for scraper in self.scrapers:
            logger.info(f"\n>>> {scraper.nome_portal}")
            try:
                noticias = scraper.coletar(limite=MAX_NOTICIAS_POR_PORTAL)
            except Exception as e:
                logger.error(f"Erro coletar {scraper.nome_portal}: {e}")
                continue
            for noticia in noticias:
                try:
                    if self._processar(noticia):
                        total += 1
                except Exception as e:
                    logger.error(f"Erro processar: {e}")
                    self.db.marcar_erro(noticia.hash_id, str(e))
        logger.info(f"\nCiclo ok. Publicadas: {total}")

    def _processar(self, noticia: Noticia) -> bool:
        if self.db.ja_processada(noticia.hash_id):
            return False
        if not self.db.registrar_coleta(noticia):
            return False
        if not noticia.conteudo or len(noticia.conteudo) < 200:
            self.db.marcar_erro(noticia.hash_id, "Conteudo curto")
            return False

        logger.info(f"Reescrevendo: {noticia.titulo[:60]}")
        titulo_n, sub_n, conteudo_n = self.rewriter.reescrever(
            noticia.titulo, noticia.conteudo, noticia.subtitulo)
        self.db.atualizar_reescrita(noticia.hash_id, titulo_n, conteudo_n)

        logger.info(f"Publicando: {titulo_n[:60]}")
        post_id = self.publisher.publicar(
            titulo=titulo_n, conteudo=conteudo_n, subtitulo=sub_n,
            portal_origem=noticia.portal, url_origem=noticia.url,
            imagem_url=noticia.imagem_destaque)
        if post_id:
            self.db.marcar_publicada(noticia.hash_id, post_id)
            logger.info(f"OK WP id={post_id}")
            return True
        return False
