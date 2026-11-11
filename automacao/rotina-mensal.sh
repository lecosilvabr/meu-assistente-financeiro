#!/bin/sh
# Rotina mensal do Meu Assistente Financeiro (Mac e Linux).
# Agende com o cron para todo dia 11 às 9h:   0 9 11 * * /caminho/para/meu-assistente-financeiro/automacao/rotina-mensal.sh
cd "$(dirname "$0")/.." || exit 1
python3 scripts/processar.py
[ -f config.json ] && python3 scripts/cotacoes.py
