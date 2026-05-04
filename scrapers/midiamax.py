"""Scraper Midia Max - DESATIVADO. Precisa Selenium + cloudscraper (Cloudflare)."""
from typing import List
from scrapers.base import BaseScraper, Noticia


class MidiaMaxScraper(BaseScraper):
    nome_portal = "Midia Max"
    url_base = "https://www.midiamax.com.br"

    def listar_noticias_recentes(self, limite: int = 5) -> List[Noticia]:
        return []

    def extrair_conteudo(self, noticia: Noticia) -> Noticia:
        return noticia
