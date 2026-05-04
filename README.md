<div align="center">

# 📰 Metropolitano MS Bot

### Sistema de Republicação Inteligente de Notícias com IA para o Portal O Metropolitano MS

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-AI-5E5CE6?style=for-the-badge&logo=openai&logoColor=white)](https://deepseek.com)
[![WordPress](https://img.shields.io/badge/WordPress-REST_API-21759B?style=for-the-badge&logo=wordpress&logoColor=white)](https://wordpress.org)
[![Railway](https://img.shields.io/badge/Deploy-Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)](https://railway.app)
[![License](https://img.shields.io/badge/Licença-Privada-red?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow?style=for-the-badge)]()

<br>

**Desenvolvido por George Emannuel**

*Campo Grande, MS — Brasil*

</div>

---

## 📋 Sobre o Projeto

O **Metropolitano MS Bot** é um sistema automatizado de monitoramento, reescrita e publicação de notícias que integra **scraping**, **Inteligência Artificial Generativa** e a **API REST do WordPress** para alimentar continuamente o portal **O Metropolitano MS** com matérias dos principais veículos de imprensa de Mato Grosso do Sul.

A cada ciclo configurado, o bot coleta as notícias mais recentes dos portais ativos, descarta as que já foram processadas (controle por hash em SQLite), reescreve cada matéria via DeepSeek preservando 100% dos fatos, números, nomes e citações originais — mas com redação completamente diferente para evitar plágio — e publica automaticamente no WordPress, com crédito à fonte original.

> ⚠️ **Atenção:** A republicação de conteúdo de terceiros, mesmo reescrito por IA, envolve riscos jurídicos. Veja a seção [Aviso Legal](#-aviso-legal-importante) ao final.

---

## 🎯 Objetivos

- **Monitorar** automaticamente os principais portais de notícias de MS
- **Coletar** matérias recentes via RSS feed ou web scraping
- **Reescrever** notícias com IA preservando fatos e citações originais
- **Publicar** automaticamente no WordPress como rascunho ou direto
- **Controlar** duplicatas via banco SQLite com hash da URL
- **Agendar** ciclos contínuos de coleta e publicação
- **Creditar** sempre o veículo original com link da matéria

---

## 🏗️ Arquitetura do Projeto

```
metropolitano_bot/
│
├── ⚙️ config/
│   └── settings.py              # Configurações e variáveis de ambiente
│
├── 🕷️ scrapers/                  # Coleta de notícias
│   ├── base.py                  # Classe base abstrata
│   ├── campograndenews.py       # Scraper Campo Grande News (RSS)
│   ├── topmidianews.py          # Scraper Top Mídia News (placeholder)
│   └── midiamax.py              # Scraper Mídia Max (placeholder)
│
├── 🧠 core/                      # Lógica de negócio
│   ├── database.py              # Controle de notícias (SQLite)
│   ├── rewriter.py              # Reescrita via DeepSeek API
│   └── orchestrator.py          # Orquestrador do pipeline
│
├── 📤 publishers/                # Publicação
│   └── wordpress.py             # WordPress REST API
│
├── 🧪 testes/
│   ├── test_scraper.py          # Testa apenas a coleta
│   └── test_rewriter.py         # Testa apenas a reescrita
│
├── 📄 docs/
│   └── README.md
│
├── main.py                      # Entry point
├── requirements.txt
├── Dockerfile                   # Deploy Railway
├── .env.example                 # Modelo de configuração
└── LICENSE
```

---

## 🌐 Status dos Portais

| Portal | Status | Estratégia | Observação |
|--------|--------|------------|------------|
| **Campo Grande News** | ✅ Ativo | RSS Feed | 20 notícias atualizadas via feed oficial |
| **Top Mídia News** | ⏸️ Desativado | Selenium | Site renderizado em JavaScript |
| **Mídia Max** | ⏸️ Desativado | Selenium + Cloudscraper | Proteção Cloudflare (HTTP 403) |

---

## 🔄 Pipeline de Funcionamento

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   PORTAIS    │───▶│   SCRAPER    │───▶│   SQLITE     │───▶│   DEEPSEEK   │
│  (RSS/HTML)  │    │  (RSS/BS4)   │    │ (Duplicatas) │    │ (Reescrita)  │
└──────────────┘    └──────────────┘    └──────────────┘    └──────┬───────┘
                                                                    │
                    ┌──────────────┐    ┌──────────────┐            │
                    │  WORDPRESS   │◀───│  PUBLISHER   │◀───────────┘
                    │  (Site Live) │    │  (REST API)  │
                    └──────────────┘    └──────────────┘
```

---

## 🤖 Módulo 1 — Reescrita Inteligente com DeepSeek

A reescrita é o coração do sistema. O modelo `deepseek-chat` é instruído por um prompt jornalístico estruturado que segue padrões editoriais brasileiros.

### Regras Aplicadas pelo Modelo

| # | Regra | Status |
|---|-------|--------|
| 1 | Preservar 100% dos fatos (nomes, datas, números, locais) | ✅ |
| 2 | Manter citações entre aspas inalteradas | ✅ |
| 3 | Reescrever estrutura de frases (ordem, conectivos, voz) | ✅ |
| 4 | Reorganizar lide (primeiro parágrafo) | ✅ |
| 5 | Criar novo título mantendo o mesmo fato | ✅ |
| 6 | Manter tom jornalístico neutro e impessoal | ✅ |
| 7 | Não inventar informações | ✅ |
| 8 | Tamanho similar ao original (±20%) | ✅ |

### Saída Esperada (JSON)

```json
{
  "titulo": "Novo título reescrito",
  "subtitulo": "Linha de apoio reescrita",
  "conteudo": "Texto completo com parágrafos separados por \n\n"
}
```

---

## 📊 Módulo 2 — Controle de Duplicatas (SQLite)

Cada notícia é identificada por um hash SHA-256 da URL e armazenada em SQLite para evitar reprocessamento.

### Estrutura da Tabela `noticias`

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `hash_id` | TEXT (PK) | Hash único derivado da URL |
| `url` | TEXT | URL original da matéria |
| `portal` | TEXT | Nome do portal de origem |
| `titulo_original` | TEXT | Título original |
| `titulo_reescrito` | TEXT | Título gerado pela IA |
| `conteudo_original` | TEXT | Texto original completo |
| `conteudo_reescrito` | TEXT | Texto reescrito pela IA |
| `status` | TEXT | `coletada` / `reescrita` / `publicada` / `erro` |
| `wp_post_id` | INTEGER | ID do post no WordPress |
| `coletada_em` | TIMESTAMP | Data/hora da coleta |
| `processada_em` | TIMESTAMP | Data/hora da reescrita |
| `publicada_em` | TIMESTAMP | Data/hora da publicação |

---

## 📤 Módulo 3 — Publicação Automatizada no WordPress

A publicação utiliza a **REST API nativa do WordPress** com autenticação via Application Password (sem necessidade de plugins).

### Funcionalidades

- ✅ Upload automático de imagem destaque
- ✅ Crédito automático à fonte original com link
- ✅ Categorização configurável
- ✅ Definição de autor configurável
- ✅ Modo rascunho (`draft`) para revisão humana
- ✅ Modo publicação direta (`publish`) para automação total
- ✅ Conversão de texto em HTML estruturado (`<h2>`, `<p>`)

---

## ⚙️ Requisitos

```
Python >= 3.10
requests >= 2.31.0
beautifulsoup4 >= 4.12.0
lxml >= 4.9.0
python-dotenv >= 1.0.0
APScheduler >= 3.10.0
```

### Serviços Externos

- **DeepSeek API** — chave em https://platform.deepseek.com/
- **WordPress 5.6+** — REST API + Application Passwords habilitados
- **Railway** (opcional) — para deploy contínuo em nuvem

---

## 🚀 Como Rodar

### 1. Preparar o ambiente

```bash
# Entrar na pasta do projeto
cd ~/Documents/metropolitano_bot

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate            # macOS/Linux
.\venv\Scripts\Activate.ps1         # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

Edite o `.env`:

```env
DEEPSEEK_API_KEY=sk-sua_chave_aqui
WP_URL=https://ometropolitanoms.com.br
WP_USER=seu_usuario_wp
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
WP_DEFAULT_CATEGORY_ID=1
WP_DEFAULT_AUTHOR_ID=1
WP_POST_STATUS=draft
SCRAPE_INTERVAL_MINUTES=30
MAX_NOTICIAS_POR_PORTAL=8
```

### 3. Testar componentes isoladamente

```bash
# Testar apenas a coleta de notícias
python test_scraper.py

# Testar apenas a reescrita com DeepSeek
python test_rewriter.py
```

### 4. Executar o bot

```bash
# Modo único (1 ciclo e para) — útil para debug
python main.py --once

# Modo contínuo (produção)
python main.py
```

### 5. Acompanhar logs

```bash
tail -f bot.log
```

---

## 🔐 Configuração do WordPress

### Application Password

1. Painel WP → **Usuários** → seu usuário
2. Role até **Application Passwords**
3. Nome: `metropolitano-bot` → **Add New Application Password**
4. Copie a senha gerada (formato: `xxxx xxxx xxxx xxxx xxxx xxxx`)

### Descobrir IDs

Acesse no navegador:

| Recurso | URL |
|---------|-----|
| Lista de categorias | `https://ometropolitanoms.com.br/wp-json/wp/v2/categories` |
| Lista de usuários | `https://ometropolitanoms.com.br/wp-json/wp/v2/users` |

---

## ☁️ Deploy no Railway

```bash
# 1. Subir código pro GitHub
git init && git add . && git commit -m "Initial commit"
git push origin main

# 2. No Railway:
# - New Project → Deploy from GitHub
# - Selecionar o repositório
# - Adicionar variáveis de ambiente (mesmas do .env)
# - Configurar volume em /app/data (para persistir SQLite)
```

O `Dockerfile` já está pronto. Railway detecta automaticamente.

---

## 💰 Custos Estimados

| Serviço | Custo Mensal Estimado |
|---------|----------------------|
| DeepSeek API (8 notícias × 48 ciclos/dia) | ~R$ 50 |
| Railway Hobby (worker contínuo) | US$ 5 (com US$ 5 free) |
| **Total estimado** | **~R$ 75/mês** |

> Na prática o consumo de API é muito menor pois o controle de duplicatas evita reprocessamento.

---

## 🧪 Adicionando Novos Portais

```python
# 1. Criar arquivo scrapers/novo_portal.py
from scrapers.base import BaseScraper, Noticia

class NovoPortalScraper(BaseScraper):
    nome_portal = "Novo Portal"
    url_base = "https://www.novoportal.com.br"

    def listar_noticias_recentes(self, limite=5):
        # implementar...
        pass

    def extrair_conteudo(self, noticia):
        # implementar...
        pass

# 2. Ativar em config/settings.py
PORTAIS["novoportal"] = {
    "nome": "Novo Portal",
    "url_base": "https://www.novoportal.com.br",
    "ativo": True,
}

# 3. Importar em core/orchestrator.py
```

Para portais com Cloudflare ou JavaScript, use `cloudscraper` ou `selenium + undetected-chromedriver`.

---

## 🛠️ Troubleshooting

| Problema | Solução |
|----------|---------|
| `ModuleNotFoundError` | Ative o venv e reinstale dependências |
| `DEEPSEEK_API_KEY não configurada` | Verifique o `.env` na raiz do projeto |
| `401 Unauthorized` no WP | Use Application Password, não senha normal |
| Scraper retorna lista vazia | RSS pode ter mudado; precisa Selenium |
| Erro `403 Forbidden` | Cloudflare bloqueando — use cloudscraper |
| Conteúdo vazio na coleta | Seletores CSS desatualizados |
| Erro de tabela SQLite | Apague `noticias.db` para recriar schema |

---

## 🔬 Tecnologias Utilizadas

| Tecnologia | Função |
|------------|--------|
| **Python 3.11+** | Linguagem principal |
| **requests** | Requisições HTTP |
| **BeautifulSoup4** | Parser HTML |
| **lxml** | Parser XML para RSS |
| **APScheduler** | Agendamento de ciclos |
| **python-dotenv** | Gestão de variáveis |
| **SQLite3** | Persistência local |
| **DeepSeek API** | Reescrita por LLM |
| **WordPress REST API** | Publicação automatizada |
| **Docker** | Containerização |
| **Railway** | Deploy em nuvem |

---

## ⚠️ Aviso Legal Importante

A republicação automatizada de conteúdo de terceiros, **mesmo reescrito por IA**, pode caracterizar:

- ❌ **Violação de direitos autorais** (Lei 9.610/98)
- ❌ **Concorrência desleal** (Lei 9.279/96, art. 195)
- ❌ **Aproveitamento parasitário de apuração jornalística**

### Recomendações Obrigatórias

1. ✅ **Sempre citar a fonte original** com link no rodapé (já implementado)
2. ✅ **Buscar autorização formal** dos veículos de origem (parceria de conteúdo)
3. ✅ **Documentar por escrito** com o cliente que ele assume a responsabilidade
4. ✅ **Manter `WP_POST_STATUS=draft`** inicialmente para revisão humana
5. ⚠️ **A paráfrase automática NÃO elimina o risco jurídico** — a estrutura, ângulo e fontes da apuração também são protegidas

> O desenvolvedor não se responsabiliza pelo uso indevido deste software.

---

## 👨‍💻 Autor

| Nome | Função | Contato |
|------|--------|---------|
| **George Emannuel Guedes de Carvalho** | Desenvolvedor | ra196379@ucdb.br |

**Estudante de Ciência da Computação — UCDB**
**Pesquisador no Laboratório Inovisão**
**Agente Administrativo na Prefeitura Municipal de Terenos**

Campo Grande — MS, Brasil

---

## 📄 Licença

Projeto privado/comercial desenvolvido sob contrato. Todos os direitos reservados ao cliente contratante.

---

<div align="center">

**📰 Metropolitano MS Bot** — Sistema de Republicação Inteligente

Desenvolvido por **George Emannuel** · Campo Grande, MS

*Powered by DeepSeek AI · WordPress REST API · Python*

</div>
