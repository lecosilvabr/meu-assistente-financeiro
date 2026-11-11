@echo off
REM Rotina mensal do Meu Assistente Financeiro (Windows).
REM Agende este arquivo no "Agendador de Tarefas" para todo dia 11 (veja docs/MANUAL.md).
cd /d "%~dp0.."
python scripts\processar.py
if exist config.json python scripts\cotacoes.py
start "" "painel\index.html"
