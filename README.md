# Metropolitano MS - Bot de Republicação Automatizada

Bot que monitora portais de notícias de MS, reescreve as matérias usando IA (DeepSeek)
mantendo os fatos, e publica automaticamente no site O Metropolitano MS (WordPress).

## Setup local

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Preencher .env com as credenciais
```

## Testes em ordem

```bash
# 1. Testa apenas a coleta dos portais
python test_scraper.py

# 2. Testa apenas a reescrita (precisa DEEPSEEK_API_KEY no .env)
python test_rewriter.py

# 3. Roda um ciclo completo
python main.py --once

# 4. Roda em loop contínuo
python main.py
```

## Status dos portais

- ✅ **Campo Grande News**: ativo (via RSS)
- ⏸️ **Top Mídia News**: desativado (precisa Selenium - JS-rendered)
- ⏸️ **Mídia Max**: desativado (precisa Selenium - Cloudflare)

## ⚠️ AVISO LEGAL

Republicação automatizada de conteúdo de terceiros pode caracterizar violação
de direitos autorais (Lei 9.610/98). Sempre cite a fonte e idealmente busque
autorização formal dos veículos.
