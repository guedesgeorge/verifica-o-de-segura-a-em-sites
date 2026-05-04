<div align="center">

# ⛪ ArqCGR Scraper — Coletor de Paróquias e Horários de Missa

### Ferramenta de Web Scraping para Mapeamento Pastoral da Arquidiocese de Campo Grande

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4.12+-FFB91A?style=for-the-badge&logo=python&logoColor=white)]()
[![Requests](https://img.shields.io/badge/Requests-HTTP-2CA02C?style=for-the-badge&logo=python&logoColor=white)]()
[![License](https://img.shields.io/badge/Licença-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Funcional-brightgreen?style=for-the-badge)]()

<br>

**Projeto Pessoal — Mapeamento Pastoral**

*Campo Grande, MS — Brasil*

</div>

---

## 📋 Sobre o Projeto

O **ArqCGR Scraper** é uma ferramenta automatizada de coleta e estruturação de dados pastorais a partir do site oficial da [Arquidiocese de Campo Grande](https://arquidiocesedecampogrande.org.br).

A ferramenta navega pela seção **Nossas Paróquias**, percorre cada uma das 54 páginas paroquiais individuais e extrai informações estruturadas — incluindo **forania**, **endereço completo**, **contatos** e a **tabela de horários de celebrações**, com tipo, dia da semana, horário e observações pastorais.

O resultado final são dois arquivos prontos para uso: **JSON estruturado** para integração com aplicações e **CSV** para análise em planilhas.

---

## 🎯 Objetivos da Ferramenta

- **Mapear** todas as paróquias da Arquidiocese de Campo Grande e suas foranias
- **Extrair** os horários de missas de forma estruturada e padronizada
- **Consolidar** informações de contato (endereço, telefone, e-mail) em base única
- **Disponibilizar** os dados em formatos abertos (JSON, CSV) para reuso pastoral
- **Automatizar** atualizações periódicas conforme mudanças no site oficial
- **Servir de base** para futuras aplicações: bots, apps mobile, sites informativos

---

## 🏗️ Estrutura do Projeto

```
lista igreja/
│
├── 🕷️ scraper_arqcgr.py          # Script principal de scraping
│
├── 📂 saida/                      # Arquivos gerados após execução
│   ├── paroquias_arqcgr.json     # Dados estruturados (JSON)
│   └── paroquias_arqcgr.csv      # Planilha (CSV - delimitador `;`)
│
├── 📄 README.md                   # Este arquivo
└── 📄 requirements.txt            # Dependências do projeto
```

---

## ⛪ Escopo da Coleta — Paróquias Mapeadas

| Forania | Quantidade | Cobertura |
|---------|------------|-----------|
| **Centro** | ~8 paróquias | Catedral e centro de Campo Grande |
| **Norte / Sul / Leste / Oeste** | ~30 paróquias | Bairros de Campo Grande |
| **Sudoeste** | ~5 paróquias | Região sudoeste de CG |
| **Rural** | ~10 paróquias | Sidrolândia, Terenos, Jaraguari, Bandeirantes, Anhanduí, Rochedo, Corguinho, Ribas do Rio Pardo |

> **Total:** 54 paróquias mapeadas — incluindo Catedral, Santuários (Nossa Senhora da Abadia, São Judas Tadeu, Nossa Senhora do Perpétuo Socorro, Santo Antônio de Pádua/Terenos), Capelania Hospitalar e Paróquia Universitária.

---

## 🔄 Fluxo de Execução

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   LISTAGEM   │───▶│   PARSING    │───▶│  EXTRAÇÃO    │───▶│    SAÍDA     │
│  (54 URLs)   │    │ (HTML→Soup)  │    │ (regex+CSS)  │    │ (JSON+CSV)   │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
       │                  │                    │                    │
       ▼                  ▼                    ▼                    ▼
 /nossas-paroquias    BeautifulSoup       Tabela horários      paroquias.json
 Lista de links       lxml parser         Info de contato      paroquias.csv
 Deduplicação         Limpeza HTML        Forania              UTF-8 + BOM
```

---

## 🔍 Módulo 1 — Listagem de Paróquias

Acessa a página `arquidiocesedecampogrande.org.br/nossas-paroquias/` e extrai os links de todas as 54 paróquias da Arquidiocese.

### Técnicas Aplicadas

| Técnica | Objetivo | Status |
|---------|----------|--------|
| Filtro por padrão de URL `/paroquias/<slug>/` | Identificar links de páginas individuais | ✅ |
| Deduplicação por URL canônica | Evitar processamento duplicado | ✅ |
| Filtro de texto mínimo | Descartar links de ícones e botões | ✅ |
| Normalização de URLs | Garantir formato consistente com `urljoin` | ✅ |

---

## 🕷️ Módulo 2 — Extração de Dados Paroquiais

Visita cada página individual e extrai dados estruturados usando uma combinação de **parsing de tabela HTML** e **regex** sobre o texto limpo da página.

### Campos Extraídos

| Campo | Origem | Método |
|-------|--------|--------|
| **Nome da paróquia** | Título da página | Texto do link |
| **Forania** | Bloco "Forania" | Regex contextual |
| **Ano de criação** | Bloco "Ano da criação" | Regex contextual |
| **Endereço** | Bloco "Endereço" | Regex multi-linha |
| **Telefone** | Texto da página | Regex `(XX) XXXXX-XXXX` |
| **E-mail** | Texto da página | Regex de e-mail |
| **Horários de celebrações** | Tabela "Horário das celebrações" | Parser de `<table>` |

> 🔒 **Princípio aplicado:** o scraper respeita um intervalo mínimo de **1,5 segundo** entre requisições para não sobrecarregar o servidor da Arquidiocese.

---

## 📊 Módulo 3 — Estruturação dos Horários

A tabela de celebrações é extraída e normalizada, preservando todas as informações pastorais.

### Estrutura de Cada Celebração

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| `tipo` | Tipo de celebração | Missa, Adoração, Confissão |
| `dia` | Dia da semana | Domingo, Sábado, Quarta-feira |
| `horario` | Horário | 19:00, 08:00 |
| `observacoes` | Observações adicionais | "19h00", "Capela X", "1º domingo" |

### Exemplo Real — Catedral

| Tipo | Dia | Horário | Observações |
|------|-----|---------|-------------|
| Missa | Domingo | 08:00 | — |
| Missa | Domingo | 09:30 | — |
| Missa | Domingo | 18:00 | — |
| Missa | Domingo | 19:30 | — |
| Missa | Sábado | 18:00 | — |
| Missa | Segunda-feira | 19:00 | — |
| Missa | Terça a Quinta | 12:00 | 19h00 (adicional) |
| Missa | Sexta-feira | 12:00 | — |

---

## 📑 Saídas Geradas

### `paroquias_arqcgr.json` — Dados Estruturados

```json
[
  {
    "nome": "CATEDRAL NOSSA SENHORA DA ABADIA E SANTO ANTÔNIO DE PÁDUA",
    "url": "https://arquidiocesedecampogrande.org.br/paroquias/catedral-.../",
    "forania": "Centro",
    "ano_criacao": "07 de abril de 1912",
    "endereco": "Travessa Lídia Baís, 29 - Centro - CEP 79003-120 - Campo Grande/MS",
    "telefone": "(67) 3321-9886",
    "email": "catedral.santoantonio@hotmail.com",
    "celebracoes": [
      { "tipo": "Missa", "dia": "Domingo", "horario": "08:00", "observacoes": "" },
      { "tipo": "Missa", "dia": "Sábado", "horario": "18:00", "observacoes": "" }
    ]
  }
]
```

### `paroquias_arqcgr.csv` — Planilha

| Paróquia | Forania | Endereço | Telefone | E-mail | Tipo | Dia | Horário | Obs. | URL |
|----------|---------|----------|----------|--------|------|-----|---------|------|-----|

> Encoding **UTF-8 com BOM** e delimitador **ponto-e-vírgula** — abre direto no Excel e no Numbers sem perder acentuação.

---

## ⚙️ Requisitos

```
Python >= 3.9
requests >= 2.31.0
beautifulsoup4 >= 4.12.0
lxml >= 4.9.0
```

---

## 🚀 Como Rodar

### 1. Preparar o ambiente

```bash
cd ~/Documents/lista\ igreja

# Opção A — ambiente virtual (recomendado)
python3 -m venv .venv
source .venv/bin/activate            # macOS/Linux
.\.venv\Scripts\Activate.ps1         # Windows

pip install -r requirements.txt

# Opção B — instalar global (macOS)
pip3 install requests beautifulsoup4 lxml --break-system-packages
```

### 2. Executar o scraper

```bash
python3 scraper_arqcgr.py
```

### 3. Acompanhar o progresso

```
==> Lendo lista de paroquias: https://arquidiocesedecampogrande.org.br/nossas-paroquias/
    54 paroquias encontradas.
[1/54] CATEDRAL NOSSA SENHORA DA ABADIA E SANTO ANTÔNIO DE PÁDUA
    10 celebracoes extraidas
[2/54] PARÓQUIA NOSSA SENHORA DA ABADIA (SANTUÁRIO)
    8 celebracoes extraidas
...
==> JSON salvo em: paroquias_arqcgr.json
==> CSV salvo em: paroquias_arqcgr.csv
==> Concluido! 54 paroquias, ~400 celebracoes no total.
```

> ⏱️ **Tempo estimado:** ~1 minuto e 30 segundos (54 paróquias × 1,5s de delay + tempo de rede).

---

## 🛡️ Boas Práticas Aplicadas

Esta ferramenta segue rigorosamente os seguintes princípios:

1. ✅ **Rate Limiting Próprio** — delay de 1,5s entre requisições para não sobrecarregar o servidor
2. ✅ **Retry com Backoff Exponencial** — 3 tentativas com intervalos crescentes (2s, 4s, 6s)
3. ✅ **Tolerância a Falhas** — uma paróquia que falhe não interrompe o processamento das demais
4. ✅ **User-Agent Identificável** — não tenta mascarar o tipo de cliente
5. ✅ **Uso Não-Comercial** — projeto pessoal para fins informativos e pastorais
6. ✅ **Dados Públicos** — apenas informações já abertas no site oficial da Arquidiocese

---

## 🎯 Casos de Uso

| Aplicação | Descrição |
|-----------|-----------|
| **App de Missas** | Base de dados para aplicativo mobile com horários por bairro |
| **Bot WhatsApp/Telegram** | Chatbot que responde "qual missa mais próxima?" |
| **Site Pastoral** | Página estática consolidada com todas as paróquias |
| **Análise Pastoral** | Distribuição geográfica de celebrações por região |
| **Mapa Interativo** | Visualização das paróquias por forania |
| **Integração com Google Maps** | Geolocalização e rotas para fiéis |

---

## 🛠️ Troubleshooting

| Problema | Solução |
|----------|---------|
| `ModuleNotFoundError` | Ative o venv e rode `pip install -r requirements.txt` |
| `externally-managed-environment` (macOS) | Use `--break-system-packages` ou crie um venv |
| Timeout em alguma paróquia | O retry automático tenta 3 vezes; se falhar, é registrado no JSON |
| CSV com acentos errados no Excel | Importe via "Dados → De Texto/CSV" escolhendo UTF-8 e `;` |
| Site mudou de estrutura | Ajuste os seletores em `extrair_celebracoes` e `extrair_info_paroquia` |
| Script aparenta estar parado | Normal — está respeitando o delay de 1,5s entre requisições |

---

## 🔬 Tecnologias Utilizadas

| Tecnologia | Função |
|------------|--------|
| **Python 3.9+** | Linguagem principal |
| **requests** | Cliente HTTP com retry |
| **BeautifulSoup4** | Parser de HTML |
| **lxml** | Backend de parsing de alta performance |
| **csv (stdlib)** | Geração de planilha CSV |
| **json (stdlib)** | Serialização estruturada |
| **re (stdlib)** | Extração via regex |

---

## 🗺️ Roadmap

- [x] Listagem completa das 54 paróquias
- [x] Extração de horários de celebrações em formato estruturado
- [x] Exportação JSON + CSV
- [x] Tratamento de erros e retentativas
- [ ] Geocodificação automática de endereços (lat/lng)
- [ ] Detecção automática de mudanças no site (diff entre execuções)
- [ ] Integração com Google Calendar (gerar `.ics`)
- [ ] API REST consultável (FastAPI)
- [ ] Dashboard web com mapa interativo
- [ ] Bot Telegram para consulta de missas próximas

---

## ⚠️ Aviso

Esta ferramenta é destinada ao **uso pessoal e pastoral**.

- ✅ **Use para fins informativos** — apoio à vida pastoral, divulgação de horários
- ✅ **Use para projetos pessoais** — apps, bots, sites estáticos
- ❌ **Não redistribua os dados como produto comercial** sem autorização da Arquidiocese
- ❌ **Não sobrecarregue o servidor** — respeite o delay configurado (1,5s)
- 📞 **Em caso de dúvida sobre uso institucional**, consulte a Arquidiocese de Campo Grande

> Os dados pertencem à Arquidiocese de Campo Grande e podem mudar a qualquer momento. Sempre confirme horários diretamente com a paróquia antes de divulgar publicamente.

---

## 👨‍💻 Autor

| Nome | Função | Contato |
|------|--------|---------|
| **George Emannuel Guedes de Carvalho** | Desenvolvedor | ra196379@ucdb.br |

**Estudante de Ciência da Computação — UCDB**
**Pesquisador no Laboratório Inovisão**

Campo Grande — MS, Brasil

---

## 📄 Licença

Este projeto está sob a licença **MIT** para uso pessoal e pastoral. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

Os dados coletados pertencem à Arquidiocese de Campo Grande e devem ser usados com respeito à fonte original.

---

<div align="center">

**⛪ ArqCGR Scraper** — Mapeamento Pastoral Automatizado

Campo Grande · MS · Brasil

*"Ide e fazei discípulos de todas as nações"* — Mt 28,19

</div>
