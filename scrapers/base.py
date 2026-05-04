"""Classe base para todos os scrapers."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import hashlib
import logging

import requests
from bs4 import BeautifulSoup

from config.settings import USER_AGENT, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


@dataclass
class Noticia:
    titulo: str
    url: str
    portal: str
    conteudo: str = ""
    subtitulo: str = ""
    autor: str = ""
    data_publicacao: Optional[datetime] = None
    imagem_destaque: str = ""
    categoria: str = ""
    tags: List[str] = field(default_factory=list)
    coletada_em: datetime = field(default_factory=datetime.now)

    @property
    def hash_id(self) -> str:
        return hashlib.sha256(self.url.encode()).hexdigest()[:16]


class BaseScraper(ABC):
    nome_portal: str = ""
    url_base: str = ""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
            "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
        })

    def _fetch(self, url: str) -> Optional[BeautifulSoup]:
        try:
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            logger.error(f"Erro ao acessar {url}: {e}")
            return None

    @abstractmethod
    def listar_noticias_recentes(self, limite: int = 5) -> List[Noticia]:
        pass

    @abstractmethod
    def extrair_conteudo(self, noticia: Noticia) -> Noticia:
        pass

    def coletar(self, limite: int = 5) -> List[Noticia]:
        noticias = self.listar_noticias_recentes(limite=limite)
        completas = []
        for n in noticias:
            try:
                completa = self.extrair_conteudo(n)
                if completa.conteudo:
                    completas.append(completa)
            except Exception as e:
                logger.error(f"Erro ao extrair {n.url}: {e}")
        return completas
