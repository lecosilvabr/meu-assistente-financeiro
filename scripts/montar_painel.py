#!/usr/bin/env python3
"""
Gera um painel em ARQUIVO ÚNICO (HTML com os dados embutidos).

Serve para:
- publicar o painel como página no Claude (versão com Claude);
- abrir no celular ou mandar para outro computador, sem precisar da pasta do projeto.

Atenção: o arquivo gerado contém TODOS os seus lançamentos. Não publique nem compartilhe sem querer.

Uso:
    python scripts/montar_painel.py                         # dados/dados.js -> dados/painel-completo.html
    python scripts/montar_painel.py --dados X.js --saida Y.html
"""
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def arg(nome, padrao):
    return os.path.abspath(sys.argv[sys.argv.index(nome) + 1]) if nome in sys.argv else padrao


def main():
    dados = arg('--dados', os.path.join(RAIZ, 'dados', 'dados.js'))
    saida = arg('--saida', os.path.join(os.path.dirname(dados), 'painel-completo.html'))
    if not os.path.exists(dados):
        sys.exit('Não achei ' + dados + '. Rode antes: python scripts/processar.py')
    html = open(os.path.join(RAIZ, 'painel', 'index.html'), encoding='utf-8').read()
    js = open(dados, encoding='utf-8').read().replace('</', '<\\/')   # não fecha o <script> sem querer
    bloco = re.compile(r'// <carregador>.*?// </carregador>\n', re.S)
    if not bloco.search(html):
        sys.exit('painel/index.html sem o bloco <carregador>.')
    html = bloco.sub(lambda m: js + '\ndocument.addEventListener("DOMContentLoaded", () => iniciar());\n', html)
    with open(saida, 'w', encoding='utf-8') as f:
        f.write(html)
    print('Painel único gerado:', saida)


if __name__ == '__main__':
    main()
