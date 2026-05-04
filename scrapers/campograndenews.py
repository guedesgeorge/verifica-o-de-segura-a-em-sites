"""Scraper do Campo Grande News usando RSS feed."""
import logging
import re
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from typing import List

from scrapers.base import BaseScraper, Noticia

logger = logging.getLogger(__name__)


class CampoGrandeNewsScraper(BaseScraper):
    nome_portal = "Campo Grande News"
    url_base = "https://www.campograndenews.com.br"
    url_rss = "https://www.campograndenews.com.br/rss"

    def listar_noticias_recentes(self, limite: int = 5) -> List[Noticia]:
        try:
            response = self.session.get(self.url_rss, timeout=20)
            response.raise_for_status()
            response.encoding = response.apparent_encoding or "utf-8"
        except Exception as e:
            logger.error(f"[{self.nome_portal}] Erro ao acessar RSS: {e}")
            return []

        try:
            root = ET.fromstring(response.text)
        except ET.ParseError as e:
            logger.error(f"[{self.nome_portal}] RSS invalido: {e}")
            return []

        noticias = []
        items = root.findall(".//item")

        for item in items[:limite]:
            titulo_el = item.find("title")
            link_el = item.find("link")
            desc_el = item.find("description")
            pubdate_el = item.find("pubDate")
            categoria_el = item.find("category")

            titulo = titulo_el.text.strip() if titulo_el is not None and titulo_el.text else ""
            url = link_el.text.strip() if link_el is not None and link_el.text else ""

            if not titulo or not url:
                continue

            noticia = Noticia(titulo=titulo, url=url, portal=self.nome_portal)

            if desc_el is not None and desc_el.text:
                desc_texto = re.sub(r"<[^>]+>", "", desc_el.text).strip()
                noticia.subtitulo = desc_texto[:300]

            if pubdate_el is not None and pubdate_el.text:
                try:
                    noticia.data_publicacao = parsedate_to_datetime(pubdate_el.text)
                except Exception:
                    pass

            if categoria_el is not None and categoria_el.text:
                noticia.categoria = categoria_el.text.strip()

            noticias.append(noticia)

        logger.info(f"[{self.nome_portal}] {len(noticias)} noticias listadas via RSS")
        return noticias

    def extrair_conteudo(self, noticia: Noticia) -> Noticia:
        soup = self._fetch(noticia.url)
        if not soup:
            return noticia

        h1 = soup.select_one("h1")
        if h1:
            t = h1.get_text(strip=True)
            if t:
                noticia.titulo = t

        for sel in ["meta[property='og:image']", "article img",
                    ".materia-foto img", ".foto-principal img", "figure img"]:
            img = soup.select_one(sel)
            if img:
                src = img.get("content") or img.get("src") or img.get("data-src")
                if src and src.startswith("http"):
                    noticia.imagem_destaque = src
                    break

        for sel in [".autor", ".author", "[rel='author']",
                    ".materia-autor", "meta[name='author']"]:
            el = soup.select_one(sel)
            if el:
                texto = el.get("content") if el.name == "meta" else el.get_text(strip=True)
                if texto:
                    noticia.autor = texto[:100]
                    break

        conteudo_container = None
        for sel in [".materia-conteudo", ".conteudo-materia", ".texto-materia",
                    "article .conteudo", ".entry-content", ".post-content",
                    "[itemprop='articleBody']", "article", "main"]:
            el = soup.select_one(sel)
            if el:
                ps_test = el.find_all("p")
                texto_total = sum(len(p.get_text(strip=True)) for p in ps_test)
                if texto_total > 200:
                    conteudo_container = el
                    break

        if conteudo_container:
            for tag in conteudo_container.select(
                "script, style, .publicidade, .ads, .ad, .banner, "
                "aside, .related, .compartilhar, .social, .newsletter, iframe"
            ):
                tag.decompose()

            paragrafos = conteudo_container.find_all("p")
            textos = []
            for p in paragrafos:
                texto = p.get_text(strip=True)
                if texto and len(texto) > 30:
                    textos.append(texto)
            noticia.conteudo = "\n\n".join(textos)

        if not noticia.conteudo:
            logger.warning(f"[{self.nome_portal}] Conteudo vazio: {noticia.url}")

        return noticia
