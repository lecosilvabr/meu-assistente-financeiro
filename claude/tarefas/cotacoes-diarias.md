# Tarefa agendada: cotações (opcional, dias úteis)

Só se você acompanha ações e tem um conector de cotações ligado ao Claude (por exemplo, Alpha Vantage, que tem plano gratuito de 25 consultas por dia).

**Quando:** de segunda a sexta, depois do fechamento da bolsa (por exemplo, 19h).

**Texto da tarefa:**

> Use a skill assistente-financeiro para atualizar as cotações. Para cada ativo de financas/carteira.csv que não seja renda fixa, busque o preço de fechamento do dia (B3: TICKER.SAO), uma consulta por vez, e grave em financas/cotacoes.csv (ticker;data;preco). Use no máximo 15 consultas. Depois gere e publique o painel de novo no mesmo link. Não mande resumo, a não ser que algum ativo tenha variado mais de 5% no dia.
