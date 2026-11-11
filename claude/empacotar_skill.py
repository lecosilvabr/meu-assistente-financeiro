#!/usr/bin/env python3
"""Gera claude/assistente-financeiro.zip: a skill pronta para instalar no Claude.

Junta o SKILL.md com os scripts, o painel, as regras gerais e o modelo de configuração
do projeto, para que a versão com Claude use exatamente o mesmo código da versão sem IA.
Uso: python claude/empacotar_skill.py
"""
import os
import zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ITENS = {
    'claude/skill/assistente-financeiro/SKILL.md': 'SKILL.md',
    'scripts/processar.py': 'scripts/processar.py',
    'scripts/montar_painel.py': 'scripts/montar_painel.py',
    'painel/index.html': 'painel/index.html',
    'regras/categorias.csv': 'regras/categorias.csv',
    'config.exemplo.json': 'config.exemplo.json',
}
destino = os.path.join(RAIZ, 'claude', 'assistente-financeiro.zip')
with zipfile.ZipFile(destino, 'w', zipfile.ZIP_DEFLATED) as z:
    for origem, nome in ITENS.items():
        info = zipfile.ZipInfo('assistente-financeiro/' + nome, date_time=(2026, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        z.writestr(info, open(os.path.join(RAIZ, origem), 'rb').read())
print('Skill gerada:', os.path.relpath(destino, RAIZ))
