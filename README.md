<div align="center">

# 🔒 NewsSecScan — Auditoria de Segurança em Portais de Notícias

### Ferramenta de Pesquisa em Segurança Web e Análise de Vulnerabilidades em Portais Jornalísticos do Mato Grosso do Sul

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Security](https://img.shields.io/badge/Research-Security-FF0000?style=for-the-badge&logo=hackthebox&logoColor=white)]()
[![OWASP](https://img.shields.io/badge/OWASP-Top_10-000000?style=for-the-badge&logo=owasp&logoColor=white)](https://owasp.org)
[![License](https://img.shields.io/badge/Licença-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Pesquisa_Ativa-yellow?style=for-the-badge)]()

<br>

**Pesquisa em Segurança Web — Laboratório Inovisão / UCDB**

*Campo Grande, MS — Brasil*

</div>

---

## 📋 Sobre o Projeto

O **NewsSecScan** é um projeto de pesquisa acadêmica em **segurança da informação aplicada à web jornalística**, conduzido como parte das atividades do Laboratório Inovisão da Universidade Católica Dom Bosco (UCDB).

O projeto avalia a **postura de segurança** de portais de notícias do Mato Grosso do Sul, identificando vulnerabilidades comuns relacionadas a **scraping não autorizado**, **proteção de conteúdo**, **anti-bot bypass**, **content fingerprinting** e **ausência de rate limiting**, propondo recomendações práticas de hardening para equipes de tecnologia desses veículos.

A pesquisa também explora como **modelos de linguagem (LLMs)** podem ser utilizados em ataques de **content laundering** (rebranding automatizado de conteúdo), tema crítico e pouco estudado no contexto brasileiro de mídia digital.

---

## 🎯 Objetivos da Pesquisa

- **Mapear** os mecanismos de proteção existentes nos principais portais de MS
- **Avaliar** a eficácia de cada camada de defesa (RSS público, Cloudflare, JS-rendering, anti-scraping)
- **Documentar** vetores de extração não autorizada de conteúdo jornalístico
- **Demonstrar** o risco do content laundering automatizado por IA generativa
- **Propor** contramedidas técnicas e arquiteturais para hardening de portais
- **Contribuir** com a literatura nacional sobre segurança em mídia digital

> ⚠️ **Disclaimer Acadêmico:** Esta pesquisa segue princípios de **responsible disclosure**. Nenhum conteúdo coletado é publicado, redistribuído ou comercializado. Todos os portais analisados serão notificados das vulnerabilidades identificadas antes de qualquer publicação científica.

---

## 🏗️ Arquitetura da Ferramenta

```
newssec_scanner/
│
├── 🔍 reconhecimento/             # Phase 1 — Recon passivo
│   ├── settings.py                # Configurações do scanner
│   └── targets.py                 # Lista de alvos do escopo
│
├── 🕷️ probes/                     # Phase 2 — Probes de extração
│   ├── base_probe.py              # Probe base abstrato
│   ├── rss_probe.py               # Auditoria de feeds RSS expostos
│   ├── js_render_probe.py         # Detecção de SPA / JS-rendering
│   └── waf_probe.py               # Identificação de Cloudflare/WAF
│
├── 🧠 analyzers/                  # Phase 3 — Análise de risco
│   ├── content_db.py              # Catálogo de evidências (SQLite)
│   ├── llm_analyzer.py            # Análise de fingerprint via LLM
│   └── risk_assessment.py         # Pontuação OWASP-like
│
├── 📊 reporters/                  # Phase 4 — Geração de relatórios
│   └── html_report.py             # Relatório técnico para disclosure
│
├── 🧪 testes/
│   ├── test_recon.py              # Testes de reconhecimento
│   └── test_analyzer.py           # Testes do analisador
│
├── main.py                        # Entry point do scanner
├── requirements.txt
├── Dockerfile
├── .env.example
└── LICENSE
```

---

## 🌐 Escopo da Pesquisa — Portais Analisados

| Portal | Postura Atual | Vetor Identificado | Severidade |
|--------|---------------|---------------------|------------|
| **Portal A** | RSS público, sem rate limiting | Extração massiva via feed `/rss` | 🟡 Média |
| **Portal B** | SPA com JavaScript rendering | Bypass via headless browser | 🟠 Alta |
| **Portal C** | Cloudflare WAF (modo padrão) | Bypass via TLS fingerprint customizado | 🔴 Crítica |

> Os nomes dos portais foram anonimizados neste documento conforme política de **responsible disclosure**. A versão completa do relatório será compartilhada apenas com as equipes técnicas dos veículos após validação acadêmica.

---

## 🔄 Metodologia de Auditoria

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   RECON      │───▶│  PROBING     │───▶│   ANÁLISE    │───▶│   RELATÓRIO  │
│ (passivo)    │    │ (não invas.) │    │ (catalogação)│    │ (disclosure) │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
       │                  │                    │                    │
       ▼                  ▼                    ▼                    ▼
  DNS / Whois         RSS / Headers        SQLite + Hash         HTML / PDF
  Tech stack          JS rendering         LLM fingerprint       Recomendações
  Robots.txt          WAF detection        Risk scoring          OWASP mapping
```

---

## 🔬 Módulo 1 — Reconhecimento Passivo (Phase 1)

Coleta de informações **sem interação ativa** com a infraestrutura dos alvos. Reduz pegada e respeita os princípios de pesquisa ética.

### Técnicas Aplicadas

| Técnica | Objetivo | Status |
|---------|----------|--------|
| Análise de `robots.txt` | Identificar áreas excluídas pelos portais | ✅ |
| Verificação de `sitemap.xml` | Mapear conteúdo público estruturado | ✅ |
| Detecção de RSS feeds | Avaliar exposição de conteúdo | ✅ |
| Identificação de tech stack | WordPress, frameworks, CDN | ✅ |
| Análise de headers HTTP | Server, X-Powered-By, Cookies | ✅ |

---

## 🕷️ Módulo 2 — Probes de Extração (Phase 2)

Probes **não invasivos** que avaliam até onde um agente automatizado consegue ir antes de ser detectado e bloqueado.

### Vetores Testados

| Vetor | Descrição | OWASP / CWE |
|-------|-----------|-------------|
| **Feed RSS público** | Verifica exposição irrestrita de conteúdo full-text | CWE-200 |
| **Renderização JavaScript** | Avalia se o portal cai sem JS (defesa anti-bot básica) | OWASP API4 |
| **Detecção de WAF** | Identifica Cloudflare, Akamai, AWS WAF | CWE-693 |
| **Rate limiting** | Mede se há limite de requisições por IP | OWASP API4 |
| **User-Agent filtering** | Testa filtros baseados em UA strings | CWE-693 |

> 🔒 **Princípio aplicado:** todos os probes respeitam um intervalo mínimo de 5s entre requisições para evitar carga sobre os servidores dos alvos.

---

## 🧠 Módulo 3 — Análise via LLM (Phase 3)

Investigação da capacidade de **modelos de linguagem** em realizar **content fingerprinting** e **content laundering** — temas centrais para a discussão de proteção de propriedade intelectual em mídia digital.

### Hipóteses Investigadas

| Hipótese | Status |
|----------|--------|
| H1: LLMs podem reescrever artigos jornalísticos preservando 100% dos fatos | ✅ Confirmada |
| H2: Reescritas via LLM evadem detectores de plágio textual tradicionais | ✅ Confirmada |
| H3: Watermarking estatístico em texto poderia mitigar laundering | 🔬 Em pesquisa |
| H4: Fingerprinting estrutural (lide, ângulo) sobrevive à reescrita | 🔬 Em pesquisa |

### Catálogo de Evidências (SQLite)

| Campo | Descrição |
|-------|-----------|
| `hash_id` | Hash SHA-256 da URL original |
| `portal` | Veículo de origem (anonimizado em publicações) |
| `original_text` | Texto coletado para análise |
| `rewritten_sample` | Amostra reescrita para fingerprinting |
| `fingerprint_score` | Pontuação de similaridade estrutural |
| `owasp_category` | Categorização OWASP do vetor identificado |

> Todas as amostras são armazenadas localmente em ambiente controlado e **nunca são publicadas, redistribuídas ou comercializadas**.

---

## 📊 Módulo 4 — Recomendações de Hardening

Com base nas evidências coletadas, o projeto produz um conjunto de recomendações técnicas para portais jornalísticos:

### Recomendações Defensivas

| # | Recomendação | Camada |
|---|--------------|--------|
| 1 | Implementar rate limiting por IP/UA (nginx, Cloudflare) | Edge |
| 2 | Reduzir conteúdo full-text no RSS (apenas resumos) | Aplicação |
| 3 | Adotar Cloudflare Bot Management ou similar | Edge |
| 4 | Adicionar JavaScript challenges em rotas críticas | Edge |
| 5 | Implementar fingerprinting passivo (TLS, JA3) | Edge |
| 6 | Watermarking estatístico no texto publicado | Aplicação |
| 7 | Monitoramento de republicação via reverse image search | Operacional |
| 8 | Termos de uso explícitos sobre scraping (LGPD/Lei 9.279) | Jurídico |

---

## ⚙️ Requisitos

```
Python >= 3.11
requests >= 2.31.0
beautifulsoup4 >= 4.12.0
lxml >= 4.9.0
python-dotenv >= 1.0.0
APScheduler >= 3.10.0
```

---

## 🚀 Como Rodar

### 1. Preparar o ambiente

```bash
cd ~/Documents/newssec_scanner

python3 -m venv venv
source venv/bin/activate            # macOS/Linux
.\venv\Scripts\Activate.ps1         # Windows

pip install -r requirements.txt
```

### 2. Configurar variáveis

```bash
cp .env.example .env
```

Edite o `.env` com as configurações de coleta e análise.

### 3. Executar testes

```bash
# Testar reconhecimento passivo
python test_recon.py

# Testar análise de fingerprint
python test_analyzer.py
```

### 4. Rodar auditoria completa

```bash
# Modo único (1 ciclo)
python main.py --once

# Modo contínuo (monitoramento longitudinal)
python main.py
```

---

## 📑 Princípios Éticos da Pesquisa

Esta pesquisa segue rigorosamente os seguintes princípios:

1. ✅ **Responsible Disclosure** — todos os portais identificados serão notificados antes de qualquer publicação
2. ✅ **Não-Invasividade** — probes respeitam intervalos mínimos e não causam impacto nos servidores
3. ✅ **Não-Redistribuição** — nenhum conteúdo coletado é publicado, vendido ou compartilhado
4. ✅ **Anonimização** — nomes dos portais são anonimizados em publicações até autorização explícita
5. ✅ **Conformidade LGPD** — nenhum dado pessoal é coletado ou processado
6. ✅ **Aprovação Institucional** — projeto vinculado ao Laboratório Inovisão / UCDB

---

## 📚 Fundamentação Teórica

### Referências Centrais

- **OWASP API Security Top 10** — particularmente API4:2023 (Unrestricted Resource Consumption)
- **OWASP Web Security Testing Guide v4.2** — métodos de teste para coleta automatizada
- **MITRE ATT&CK** — tática TA0001 (Initial Access) e técnicas relacionadas a web scraping
- **NIST SP 800-115** — Technical Guide to Information Security Testing
- **Lei nº 9.279/96** — Concorrência desleal aplicada a aproveitamento de conteúdo
- **Lei nº 9.610/98** — Direitos autorais sobre apuração jornalística
- **LGPD (Lei nº 13.709/18)** — Para tratamento de dados durante a pesquisa

### Trabalhos Relacionados

- Imperva Bad Bot Report (2024) — distribuição de tráfego automatizado em mídia
- Cloudflare Radar — análise de bot traffic em sites jornalísticos
- ACM CCS / USENIX Security — papers sobre scraping detection e watermarking de texto

---

## 🎯 Potencial de Publicação

| Tema | Veículo Alvo |
|------|--------------|
| Content laundering via LLMs em mídia brasileira | SBSeg / SBSI |
| Fingerprinting estrutural de notícias | WCAMA / SIBGRAPI |
| Mapeamento de postura de segurança em portais regionais | Revista Brasileira de Computação Aplicada |
| Recomendações de hardening pra mídia digital | RBSeg / Qualis B+ |

---

## 🛠️ Troubleshooting

| Problema | Solução |
|----------|---------|
| `ModuleNotFoundError` | Ative o venv e reinstale dependências |
| Probe retorna 403 | WAF detectado — comportamento esperado, registre no relatório |
| Probe retorna lista vazia | Site usa JS rendering — registre como defesa ativa |
| Erro de tabela SQLite | Apague `evidencias.db` para recriar schema |

---

## 🔬 Tecnologias Utilizadas

| Tecnologia | Função |
|------------|--------|
| **Python 3.11+** | Linguagem principal |
| **requests** | Probes HTTP |
| **BeautifulSoup4** | Parser HTML |
| **lxml** | Parser XML para RSS |
| **APScheduler** | Agendamento de auditorias longitudinais |
| **SQLite3** | Catálogo de evidências |
| **DeepSeek API** | Análise de fingerprint via LLM |
| **Docker** | Ambiente isolado de pesquisa |

---

## ⚠️ Aviso Importante

Esta ferramenta é **estritamente para fins de pesquisa acadêmica em segurança da informação**.

- ❌ **Não use para republicar conteúdo de terceiros** — isso configura violação de direitos autorais (Lei 9.610/98) e concorrência desleal (Lei 9.279/96)
- ❌ **Não use contra alvos sem autorização explícita** ou fora do escopo de pesquisa documentado
- ✅ **Use para auditar seus próprios portais** ou em pesquisa com responsible disclosure
- ✅ **Use para estudar mecanismos de defesa** e implementar contramedidas

> O autor não se responsabiliza por uso indevido. A ferramenta é distribuída sob licença MIT para fins educacionais.

---

## 👨‍🔬 Equipe de Pesquisa

| Nome | Função | Contato |
|------|--------|---------|
| **George Emannuel Guedes de Carvalho** | Pesquisador principal | ra196379@ucdb.br |

**Estudante de Ciência da Computação — UCDB**
**Pesquisador no Laboratório Inovisão**

Campo Grande — MS, Brasil

---

## 📄 Licença

Este projeto está sob a licença **MIT** para fins de pesquisa acadêmica e educacional. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<div align="center">

**🔒 NewsSecScan** — Pesquisa em Segurança Web Jornalística

Laboratório Inovisão · UCDB · Campo Grande, MS

*Pesquisa conduzida sob princípios de responsible disclosure*

</div>
