"""Testa apenas a reescrita com DeepSeek."""
import os
from dotenv import load_dotenv
load_dotenv()

from core.rewriter import DeepSeekRewriter


TITULO = "Policia prende suspeito de furto em supermercado de Campo Grande"
CONTEUDO = """
Um homem de 32 anos foi preso na manha desta segunda-feira (28) suspeito de furtar
mercadorias em um supermercado no Bairro Tiradentes, em Campo Grande. Segundo a Policia
Militar, o suspeito teria escondido produtos de higiene pessoal dentro de uma mochila e
tentado deixar o estabelecimento sem passar pelo caixa.

Funcionarios do mercado acionaram a PM, que chegou ao local em poucos minutos.
Os produtos furtados, avaliados em R$ 480, foram recuperados.

"O homem confessou o furto e disse que estava desempregado", afirmou o tenente
responsavel pela ocorrencia.

O suspeito foi conduzido a Delegacia de Pronto Atendimento Comunitario (Depac)
da regiao e deve responder por furto.
"""


def main():
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("Configure DEEPSEEK_API_KEY no .env primeiro")
        return

    print("=" * 60)
    print("ORIGINAL:")
    print("=" * 60)
    print(f"Titulo: {TITULO}\n")
    print(CONTEUDO)

    rewriter = DeepSeekRewriter()
    titulo, sub, conteudo = rewriter.reescrever(TITULO, CONTEUDO)

    print("\n" + "=" * 60)
    print("REESCRITO:")
    print("=" * 60)
    print(f"Titulo: {titulo}")
    if sub:
        print(f"Subtitulo: {sub}")
    print()
    print(conteudo)


if __name__ == "__main__":
    main()
