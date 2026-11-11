#!/usr/bin/env python3
"""
Atualiza cotacoes.csv com o preço de fechamento das ações e ETFs da carteira.csv.

Usa a API gratuita da Alpha Vantage (25 consultas por dia). Pegue uma chave grátis em
https://www.alphavantage.co/support/#api-key e coloque em "alpha_vantage_chave" no config.json.

Uso:
    python scripts/cotacoes.py

Renda fixa (CDB, Tesouro) não tem cotação aqui: atualize o valor à mão em cotacoes.csv.
"""
import csv
import datetime as dt
import io
import json
import os
import sys
import time
import urllib.parse
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    cfg = json.load(open(os.path.join(RAIZ, 'config.json'), encoding='utf-8'))
    chave = cfg.get('alpha_vantage_chave')
    if not chave:
        sys.exit('Coloque sua chave gratuita da Alpha Vantage em "alpha_vantage_chave" no config.json.')
    carteira = list(csv.DictReader(open(os.path.join(RAIZ, 'carteira.csv'), encoding='utf-8-sig'), delimiter=';'))
    caminho = os.path.join(RAIZ, 'cotacoes.csv')
    linhas = list(csv.DictReader(open(caminho, encoding='utf-8-sig'), delimiter=';')) if os.path.exists(caminho) else []

    for c in carteira:
        if 'renda fixa' in c.get('classe', '').lower():
            continue
        simbolo = c.get('simbolo_alpha') or (c['ticker'] + '.SAO' if c.get('moeda', 'BRL') == 'BRL' else c['ticker'])
        url = 'https://www.alphavantage.co/query?' + urllib.parse.urlencode({'function': 'GLOBAL_QUOTE', 'symbol': simbolo, 'apikey': chave})
        try:
            dados = json.load(urllib.request.urlopen(url, timeout=30)).get('Global Quote') or {}
        except Exception as e:  # sem internet, limite do dia etc.
            print('  falhou', simbolo, '-', e)
            continue
        if not dados.get('05. price'):
            print('  sem cotação para', simbolo, '(limite diário atingido ou símbolo errado)')
            continue
        data = dados.get('07. latest trading day') or dt.date.today().isoformat()
        linhas = [l for l in linhas if not (l['ticker'] == c['ticker'] and l['data'] == data)]
        linhas.append({'ticker': c['ticker'], 'data': data, 'preco': dados['05. price']})
        print('  ', c['ticker'], data, dados['05. price'])
        time.sleep(1.5)  # o plano gratuito aceita 1 consulta por segundo

    with open(caminho, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['ticker', 'data', 'preco'], delimiter=';')
        w.writeheader()
        w.writerows(sorted(linhas, key=lambda l: (l['data'], l['ticker'])))
    print('Cotações salvas. Rode python scripts/processar.py para atualizar o painel.')


if __name__ == '__main__':
    main()
