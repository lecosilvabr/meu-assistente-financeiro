# Novidades

Todas as mudanças do **Meu Assistente Financeiro** que você percebe ao usar. A versão atual está no arquivo [`VERSION`](VERSION) e no rodapé do menu do painel.

Para atualizar sem perder nada, veja a [seção 16 do manual](docs/MANUAL.md#16-atualizar-para-uma-versão-nova).

## 1.1.0 · 12/11/2026

Nova **Visão geral** e um padrão visual único para todo o painel.

### Visão geral redesenhada

- **Dia a dia e cartão:** o card de destaque mostra quanto você já gastou fora das contas fixas, comparado com o **teto** do mês (o que entrou menos contas fixas, parcelas, assinaturas e seguros). O gráfico compara o gasto acumulado com o ritmo que fecha o mês no zero.
  - No mês em andamento, mostra **quanto ainda dá para gastar por dia**.
  - Nos meses fechados, mostra se o mês fechou acima ou abaixo do teto.
- **Metas do mês:** as metas do `config.json` viraram barras na própria Visão geral (azul dentro da meta, âmbar acima de 90%, vermelho quando passa).
- **Resultado do mês:** o que entrou, o fixo e o dia a dia, com os gastos pontuais à parte.
- **Meu cartão:** fatura do mês, uso do limite (com as parcelas futuras), vencimento e melhor dia de compra no mesmo card.
- **Linha do tempo:** salário, contas fixas pagas, melhor dia de compra e vencimento da fatura, em ordem de data.
- **Longo prazo:** reserva de emergência, investimentos e financiamento ficam numa seção própria, abaixo do mês.
- Saíram da Visão geral o checklist de contas (continua na aba **Contas fixas**) e o card de Moradia.

### Visual e usabilidade

- **Escala de espaçamento de 8 pontos** em todas as abas: espaços de 8, 16, 24, 32 e 48 px, com 4 px só para ajuste fino. Os valores ficam em variáveis (tokens) no início do CSS do painel.
- **Cards padronizados:** compacto (16 px), padrão (24 px) e destaque (32 px, um por tela, com borda azul). Cantos de 16 px nos cards e 10 px nos botões.
- **Botões e itens de menu com 48 px de altura**, o tamanho confortável para o dedo no celular.
- **Tipografia em escala:** 12, 14, 16, 18, 24, 30 e 36 px, com números alinhados (tabulares).
- **Barras mais finas (8 px)** em metas, limite, reserva e financiamento.
- **Menu em dois grupos:** "Hoje" (Visão geral, Gastos, Cartão, Contas fixas, A identificar) e "Longo prazo" (Investimentos, Financiamento e o tema).
- **No celular:** o menu virou uma **barra de abas embaixo** (Visão geral, Gastos, Cartão e Mais), a página usa 16 px de margem e a linha do tempo fica na vertical.
- Tema escuro com as novas cores de alerta e de sucesso; o botão de ocultar valores cobre todos os números novos.

### Documentação e projeto

- `AGENTS.md`: nova seção **UI/UX Design System**, com as regras de espaçamento, alturas, raios e tipografia que qualquer mudança no painel deve seguir.
- Novos arquivos `CHANGELOG.md` (esta página) e `VERSION`.
- Manual: a seção 7 explica a nova Visão geral e o menu, e a nova seção 16 mostra como atualizar para uma versão nova.
- Capturas de tela novas no README e no manual, com dados fictícios.
- A skill da versão com Claude (`claude/assistente-financeiro.zip`) foi gerada de novo com o painel novo.

Nada mudou nos scripts, nas regras de categorização nem no formato do `config.json`: seus dados e suas regras continuam funcionando.

## 1.0.0 · 11/11/2026

Primeira versão aberta.

- Painel em arquivo único, offline, com Visão geral, Gastos, Cartão, Contas fixas, Financiamento (com simulador de amortização), Investimentos e A identificar.
- `scripts/processar.py`: lê o extrato e a fatura do C6 ou um CSV genérico (`data;descricao;valor`), categoriza por regras e separa gastos pontuais.
- `scripts/cotacoes.py`: cotações pela API gratuita da Alpha Vantage (opcional).
- `scripts/montar_painel.py`: gera o painel com os dados embutidos, para abrir no celular.
- Rotina do dia 11 para Windows, Mac e Linux.
- Versão com Claude: skill, manual, tarefas agendadas e painel publicado em link privado.
- Tema claro e escuro, botão de ocultar valores e dados de exemplo fictícios.
