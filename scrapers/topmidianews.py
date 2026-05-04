"""Scraper Top Midia News - DESATIVADO. Precisa Selenium (site renderiza via JS)."""
from typing import List
from scrapers.base import BaseScraper, Noticia


class TopMidiaNewsScraper(BaseScraper):
    nome_portal = "Top Midia News"
    url_base = "https://www.topmidianews.com.br"

    def listar_noticias_recentes(self, limite: int = 5) -> List[Noticia]:
        return []

    def extrair_conteudo(self, noticia: Noticia) -> Noticia:
        return noticia
