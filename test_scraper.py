"""Testa apenas a coleta de noticias."""
import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

from scrapers.campograndenews import CampoGrandeNewsScraper

scrapers = [CampoGrandeNewsScraper()]

for scraper in scrapers:
    print("\n" + "=" * 70)
    print(f"PORTAL: {scraper.nome_portal}")
    print("=" * 70)

    try:
        noticias = scraper.coletar(limite=2)
    except Exception as e:
        print(f"ERRO: {e}")
        continue

    if not noticias:
        print("Nenhuma noticia coletada")
        continue

    print(f"OK - {len(noticias)} noticia(s) coletada(s)\n")

    for i, n in enumerate(noticias, 1):
        print(f"--- Noticia {i} ---")
        print(f"TITULO:  {n.titulo}")
        print(f"URL:     {n.url}")
        print(f"AUTOR:   {n.autor or '(nao encontrado)'}")
        print(f"IMAGEM:  {n.imagem_destaque[:80] if n.imagem_destaque else '(nao encontrada)'}")
        print(f"CONTEUDO ({len(n.conteudo)} caracteres):")
        if n.conteudo:
            print(n.conteudo[:400] + "..." if len(n.conteudo) > 400 else n.conteudo)
        else:
            print("(vazio)")
        print()
