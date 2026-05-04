"""Reescritor com DeepSeek API."""
import json
import logging
import re
from typing import Tuple

import requests

from config.settings import DEEPSEEK_API_KEY, DEEPSEEK_API_URL, DEEPSEEK_MODEL, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """Voce e um jornalista profissional brasileiro experiente.

Sua tarefa e REESCREVER uma noticia mantendo 100% dos fatos, numeros, nomes, datas, lugares
e declaracoes originais, mas mudando completamente a redacao para evitar plagio.

REGRAS:
1. PRESERVE todos os fatos: nomes, cargos, numeros, datas, locais, valores.
2. PRESERVE o sentido das declaracoes entre aspas.
3. MUDE a estrutura das frases: ordem, conectivos, sinonimos, voz ativa/passiva.
4. MUDE o lide reorganizando a ordem das informacoes.
5. NAO invente informacoes que nao estao no original.
6. NAO emita opinioes pessoais.
7. Tom jornalistico neutro e objetivo.
8. Crie um TITULO NOVO mantendo o mesmo fato mas com palavras diferentes.
9. Tamanho similar ao original (+/- 20%).

FORMATO (JSON estrito, sem markdown):
{
  "titulo": "Novo titulo",
  "subtitulo": "Linha de apoio (ou string vazia)",
  "conteudo": "Texto reescrito com paragrafos separados por \\n\\n"
}
"""


class DeepSeekRewriter:
    def __init__(self, api_key=DEEPSEEK_API_KEY):
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY nao configurada no .env")
        self.api_key = api_key

    def reescrever(self, titulo_original, conteudo_original, subtitulo_original="") -> Tuple[str, str, str]:
        partes = [f"TITULO ORIGINAL:\n{titulo_original}\n"]
        if subtitulo_original:
            partes.append(f"SUBTITULO ORIGINAL:\n{subtitulo_original}\n")
        partes.append(f"CONTEUDO ORIGINAL:\n{conteudo_original}\n")
        partes.append("Reescreva conforme as regras e retorne em JSON.")
        user_prompt = "\n".join(partes)

        payload = {
            "model": DEEPSEEK_MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.7,
            "max_tokens": 4000,
            "response_format": {"type": "json_object"},
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        response = requests.post(DEEPSEEK_API_URL, headers=headers,
                                 json=payload, timeout=REQUEST_TIMEOUT * 3)
        response.raise_for_status()
        data = response.json()

        content = data["choices"][0]["message"]["content"]
        content = re.sub(r"^```(?:json)?\s*", "", content.strip())
        content = re.sub(r"\s*```$", "", content)
        resultado = json.loads(content)

        titulo = resultado.get("titulo", "").strip()
        sub = resultado.get("subtitulo", "").strip()
        conteudo = resultado.get("conteudo", "").strip()

        if not titulo or not conteudo:
            raise ValueError("DeepSeek retornou resposta vazia")

        logger.info(f"Reescrita ok - tokens: {data.get('usage', {})}")
        return titulo, sub, conteudo
