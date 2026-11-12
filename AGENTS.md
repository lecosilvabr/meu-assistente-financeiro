# AGENTS.md

Instruções para agentes de IA (Claude Code, Codex, Copilot, Cursor etc.) que forem ler ou alterar este repositório. Pessoas devem começar pelo [README](README.md) e pelo [Manual](docs/MANUAL.md); a seção 15 do manual explica este arquivo para quem não programa.

## O que é o projeto

**Meu Assistente Financeiro** é um painel de finanças pessoais que roda no computador do usuário: scripts em Python leem o extrato da conta e a fatura do cartão (CSV), categorizam por regras e geram um arquivo de dados que um painel HTML abre direto no navegador.

- Público: pessoas leigas em programação, no Brasil. Textos, nomes de variáveis, comentários e mensagens são em **português do Brasil**.
- Duas versões com o **mesmo código**: sem IA (roda local, grátis) e com Claude (skill em `claude/`).
- Princípios: sem servidor, sem cadastro, sem dependências para instalar, dados do usuário nunca saem do computador.

## Regra número 1: privacidade

Este repositório é público e só pode conter **dados fictícios**.

- Nunca crie, versione ou cite dados reais de ninguém (nomes, valores, extratos, chaves de API, links de painel).
- Dados do usuário ficam em `config.json`, `entrada/`, `dados/`, `ajustes.csv`, `carteira.csv`, `cotacoes.csv` e `regras-pessoais.csv`, todos no `.gitignore`. Não remova essas entradas nem use `git add -f` nelas.
- Exemplos novos vão em `exemplo/`, com nomes claramente fictícios ("Ana Exemplo", "JOAO EXEMPLO DA SILVA") e valores inventados.
- Antes de qualquer commit, confira o `git status` e o diff em busca de dados pessoais.

## Mapa do repositório

| Caminho | O que é |
|---|---|
| `scripts/processar.py` | Núcleo. Lê `entrada/<AAAA-MM>/*.csv`, categoriza, soma ajustes e gera `dados/dados.js` |
| `scripts/montar_painel.py` | Gera o painel em arquivo único (HTML com os dados embutidos) |
| `scripts/cotacoes.py` | Opcional. Atualiza `cotacoes.csv` pela Alpha Vantage (plano gratuito) |
| `painel/index.html` | O painel inteiro (HTML, CSS e JS em um arquivo) |
| `painel/dados-exemplo.js` | **Gerado**. Dados fictícios que o painel usa quando não há `dados/dados.js` |
| `regras/categorias.csv` | Regras gerais de categorização |
| `config.exemplo.json` | Modelo de configuração (o usuário copia para `config.json`) |
| `exemplo/` | Conjunto fictício completo: config, entradas, regras pessoais, carteira, ajustes |
| `automacao/` | Rotina mensal (cron e Agendador do Windows) |
| `claude/` | Versão com Claude: `skill/assistente-financeiro/SKILL.md`, manual, tarefas agendadas e o zip da skill |
| `claude/assistente-financeiro.zip` | **Gerado** por `claude/empacotar_skill.py` |
| `docs/MANUAL.md`, `docs/img/` | Manual do usuário e capturas de tela (com dados fictícios) |

## O que ler antes de mexer

1. `README.md` (visão geral e promessas feitas ao usuário).
2. O docstring e o `main()` de `scripts/processar.py` (fluxo completo dos dados).
3. O cabeçalho de `regras/categorias.csv` (como as regras funcionam).
4. Para a versão com Claude: `claude/skill/assistente-financeiro/SKILL.md` e `claude/MANUAL-CLAUDE.md`.
5. Para mudanças visíveis ao usuário: a seção correspondente de `docs/MANUAL.md`.

## Como rodar e validar

Não há build, instalador nem suíte de testes. A validação é rodar com os dados de exemplo:

```bash
python scripts/processar.py --exemplo     # regenera painel/dados-exemplo.js
python scripts/montar_painel.py --dados painel/dados-exemplo.js --saida /tmp/painel.html
python claude/empacotar_skill.py          # regenera claude/assistente-financeiro.zip
```

Checklist antes de concluir uma alteração:

- `processar.py --exemplo` termina com "Pronto: N lançamentos, M faturas", sem erro e sem arquivo "ignorado".
- `painel/index.html` abre no navegador sem erro no console, nas abas afetadas, em tema claro e escuro e em largura de celular.
- Se mudou `scripts/`, `painel/index.html`, `regras/categorias.csv`, `config.exemplo.json` ou o `SKILL.md`: rode `empacotar_skill.py` e inclua o zip no commit.
- Se mudou `processar.py`, as regras ou algo em `exemplo/`: inclua o `painel/dados-exemplo.js` regenerado. Se nada disso mudou, não o inclua (só a data de geração muda).
- Se mudou comportamento, opção de configuração ou tela: atualize `README.md`, `docs/MANUAL.md` e `claude/MANUAL-CLAUDE.md`.

## Padrões de código

**Python**

- Só a biblioteca padrão, compatível com Python 3.8+. Não adicione `requirements.txt`, pandas ou qualquer pacote externo.
- Scripts autossuficientes, executados da raiz (`python scripts/x.py`), com caminhos a partir de `RAIZ` e argumentos lidos de `sys.argv`.
- Docstring no topo com o que faz e o "Uso:". Mensagens de erro em português, dizendo ao usuário o que fazer (`sys.exit('Falta o config.json. Copie ...')`).
- CSV de entrada pode vir em UTF-8 ou Latin-1 e com números no formato brasileiro: use `ler_texto()`, `num()` e `data_iso()` em vez de reescrever a leitura.

**Painel**

- Um único `index.html`, sem framework, sem CDN e sem chamadas de rede. Tem que funcionar offline, aberto por duplo clique (`file://`).
- Os dados chegam em `window.DADOS`. Mantenha o bloco `// <carregador> ... // </carregador>` intacto: `montar_painel.py` depende dele.
- Toda tela nova precisa funcionar em tema claro/escuro, no celular e com o botão de ocultar valores.
- Espaçamentos, alturas e raios seguem a seção "UI/UX Design System" abaixo.

**Dados e regras**

- CSV com separador `;`. Linhas iniciadas por `#` são comentários.
- Colunas das regras: `padrao;onde;tipo;categoria;subcategoria;pontual`. `padrao` é regex sem diferenciar maiúsculas; `onde` é `conta`, `cartao` ou `ambos`; `tipo` é `Despesa`, `Receita` ou `Interno`.
- **A primeira regra que bate vence.** A ordem importa: regra específica antes da genérica (ex.: `MERCADOLIVRE` antes de `MERCADO`). `regras-pessoais.csv` é lido antes de `regras/categorias.csv`.
- `regras/categorias.csv` só recebe regras úteis para qualquer pessoa (lojas e serviços conhecidos). Nome de pessoa ou comércio local vai em `regras-pessoais.csv`.
- Opção nova de configuração entra em `config.exemplo.json` e em `exemplo/config.json`, sempre lida com `cfg.get(chave, padrao)` para não quebrar o `config.json` de quem já usa.

## UI/UX Design System

O painel segue uma escala de espaçamento de 8 pontos. Os tokens ficam no início do `<style>` de `painel/index.html` (`--space-*`, `--radius-*`, `--altura-controle` e os semânticos `--spacing-*`).

- Use a escala de 8pt: 8, 16, 24, 32, 48 px. Passos de 4px só para ajuste fino (12px é aceito como meio passo).
- Não introduza valores arbitrários sem justificativa. Use os tokens existentes; não crie token novo se um existente serve.
- Padronize alturas de componentes equivalentes: 48px para botões, itens de menu, abas e linhas tocáveis; 40px para controles secundários (chips, segmentos); 8px para barras.
- Preserve a hierarquia por proximidade: espaço menor dentro de um grupo (8px entre título e número), maior entre grupos (16 a 24px dentro do cartão, 24px entre cartões, uma seção a mais de distância entre blocos).
- Cartões: compacto 16px, padrão 24px, destaque 32px (um por tela, borda de 2px na cor de destaque). No celular a densidade cai um passo (página e cartões 16px, destaque 24px), pelos tokens dentro do `@media`.
- Raios: 6px (pequeno), 10px (botões e avisos), 16px (cartões). Tipografia: 12, 14, 16, 18, 24, 30 e 36px.
- Fora da escala, de propósito: bordas de 1 ou 2px, ícones, traços de gráfico e ajustes ópticos de 1 a 2px. Larguras de coluna seguem fluidas (flex/grid).
- Mantenha a consistência entre telas e respeite acessibilidade (área de toque de 48px, contraste de texto de pelo menos 4,5:1).
- Não altere o design system sem necessidade. A escala não substitui conferir a tela no desktop e no celular.

## Regras de negócio que não podem quebrar

- **Competência:** lançamento da conta pertence ao mês da data; compra no cartão pertence ao mês anterior ao vencimento da fatura.
- **Interno** (investimentos, transferência entre contas do titular, pagamento de fatura, estornos) fica fora de gastos e receitas. O pagamento da fatura na conta é Interno porque as compras já entram detalhadas pela fatura.
- **Pontual:** despesa única acima de `valor_gasto_pontual` sai das médias, exceto parcelas, contas fixas e as categorias Moradia, Seguros, Assinaturas e Impostos e taxas.
- **Sem duplicar:** extratos que se sobrepõem são deduplicados por data + entrada + saída + texto.
- Lançamento sem regra vira "A identificar" (nunca é descartado nem adivinhado).
- Cotações usam só o plano gratuito da Alpha Vantage (25 consultas por dia). Não use parâmetros pagos.
- Formatos lidos: extrato e fatura do C6 e o CSV genérico `data;descricao;valor`. Banco novo entra como um leitor `ler_<tipo>_<banco>()` mais a detecção pelo cabeçalho em `main()`, com um arquivo fictício em `exemplo/entrada/`.

## Commits e pull requests

- Mensagens em português, curtas, dizendo o que mudou para o usuário (ex.: "Suporte ao extrato do Nubank").
- Uma mudança por commit ou PR. Não misture refatoração com funcionalidade.
- Não reescreva o histórico da `main` nem troque a licença (MIT).

## O que não fazer

- Adicionar dependência, etapa de build, servidor, banco de dados, telemetria ou login.
- Editar à mão arquivos gerados (`painel/dados-exemplo.js`, `claude/assistente-financeiro.zip`, `dados/`).
- Duplicar na pasta `claude/` a lógica que já existe em `scripts/` e `painel/`: a skill empacota os mesmos arquivos.
- Apresentar projeções (financiamento, reserva) como recomendação financeira: são estimativas, e os textos devem dizer isso.
