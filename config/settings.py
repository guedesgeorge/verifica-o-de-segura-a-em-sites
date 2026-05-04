"""Configuracoes centralizadas do bot."""
import os
from dotenv import load_dotenv

load_dotenv()

# DeepSeek API
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"

# WordPress
WP_URL = os.getenv("WP_URL")
WP_USER = os.getenv("WP_USER")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")
WP_DEFAULT_CATEGORY_ID = int(os.getenv("WP_DEFAULT_CATEGORY_ID", "1"))
WP_DEFAULT_AUTHOR_ID = int(os.getenv("WP_DEFAULT_AUTHOR_ID", "1"))
WP_POST_STATUS = os.getenv("WP_POST_STATUS", "draft")

# Banco
DB_PATH = os.getenv("DB_PATH", "noticias.db")

# Scraping
SCRAPE_INTERVAL_MINUTES = int(os.getenv("SCRAPE_INTERVAL_MINUTES", "30"))
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)
REQUEST_TIMEOUT = 20
MAX_NOTICIAS_POR_PORTAL = int(os.getenv("MAX_NOTICIAS_POR_PORTAL", "5"))

# Portais ativos
PORTAIS = {
    "campograndenews": {
        "nome": "Campo Grande News",
        "url_base": "https://www.campograndenews.com.br",
        "ativo": True,
    },
    "topmidianews": {
        "nome": "Top Midia News",
        "url_base": "https://www.topmidianews.com.br",
        "ativo": False,
    },
    "midiamax": {
        "nome": "Midia Max",
        "url_base": "https://www.midiamax.com.br",
        "ativo": False,
    },
}
