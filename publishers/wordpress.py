"""Publicador no WordPress via REST API."""
import logging
from base64 import b64encode

import requests

from config.settings import (
    WP_URL, WP_USER, WP_APP_PASSWORD,
    WP_DEFAULT_CATEGORY_ID, WP_DEFAULT_AUTHOR_ID, WP_POST_STATUS,
    REQUEST_TIMEOUT,
)

logger = logging.getLogger(__name__)


class WordPressPublisher:
    def __init__(self):
        if not all([WP_URL, WP_USER, WP_APP_PASSWORD]):
            raise ValueError("Configuracoes do WordPress incompletas no .env")
        self.api_base = f"{WP_URL.rstrip('/')}/wp-json/wp/v2"
        creds = f"{WP_USER}:{WP_APP_PASSWORD}".encode()
        self.auth_header = {"Authorization": f"Basic {b64encode(creds).decode()}"}

    def upload_imagem(self, url_imagem, titulo=""):
        if not url_imagem:
            return None
        try:
            img_response = requests.get(url_imagem, timeout=REQUEST_TIMEOUT, stream=True)
            img_response.raise_for_status()
            content_type = img_response.headers.get("content-type", "image/jpeg")
            ext = content_type.split("/")[-1].split(";")[0] or "jpg"
            filename = f"noticia-{titulo[:30].replace(' ', '-')}.{ext}"
            headers = {**self.auth_header,
                       "Content-Disposition": f'attachment; filename="{filename}"',
                       "Content-Type": content_type}
            upload = requests.post(f"{self.api_base}/media",
                                   headers=headers, data=img_response.content,
                                   timeout=REQUEST_TIMEOUT * 2)
            upload.raise_for_status()
            return upload.json().get("id")
        except Exception as e:
            logger.warning(f"Falha imagem: {e}")
            return None

    def publicar(self, titulo, conteudo, portal_origem, url_origem,
                 subtitulo="", imagem_url="",
                 categoria_id=WP_DEFAULT_CATEGORY_ID,
                 autor_id=WP_DEFAULT_AUTHOR_ID,
                 status=WP_POST_STATUS):
        media_id = self.upload_imagem(imagem_url, titulo) if imagem_url else None

        partes = []
        if subtitulo:
            partes.append(f"<h2>{subtitulo}</h2>")
        for paragrafo in conteudo.split("\n\n"):
            paragrafo = paragrafo.strip()
            if paragrafo:
                partes.append(f"<p>{paragrafo}</p>")
        partes.append(
            f'<p><em>Com informacoes de <a href="{url_origem}" '
            f'target="_blank" rel="noopener">{portal_origem}</a>.</em></p>'
        )
        conteudo_html = "\n".join(partes)

        payload = {
            "title": titulo,
            "content": conteudo_html,
            "status": status,
            "categories": [categoria_id],
            "author": autor_id,
        }
        if media_id:
            payload["featured_media"] = media_id

        response = requests.post(f"{self.api_base}/posts",
                                 headers={**self.auth_header,
                                          "Content-Type": "application/json"},
                                 json=payload, timeout=REQUEST_TIMEOUT * 2)
        response.raise_for_status()
        post_id = response.json().get("id")
        logger.info(f"Post WP id={post_id} status={status}")
        return post_id
