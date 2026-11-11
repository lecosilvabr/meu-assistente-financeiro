# Manual do Meu Assistente Financeiro

Este manual é para quem nunca programou. Se você sabe abrir uma pasta e copiar um arquivo, consegue usar.

**Sumário**

1. [O que é e como funciona](#1-o-que-é-e-como-funciona)
2. [O que você precisa](#2-o-que-você-precisa)
3. [Instalação](#3-instalação)
4. [Configuração: seu nome e seus números](#4-configuração-seu-nome-e-seus-números)
5. [Baixando os arquivos do banco](#5-baixando-os-arquivos-do-banco)
6. [Processando o mês](#6-processando-o-mês)
7. [Lendo o painel](#7-lendo-o-painel)
8. [Ensinando as categorias](#8-ensinando-as-categorias)
9. [A rotina do dia 11 (tarefa agendada)](#9-a-rotina-do-dia-11-tarefa-agendada)
10. [Financiamento imobiliário](#10-financiamento-imobiliário)
11. [Investimentos e cotações](#11-investimentos-e-cotações)
12. [Limitações](#limitações)
13. [Privacidade](#13-privacidade)
14. [Problemas comuns](#14-problemas-comuns)

---

## 1. O que é e como funciona

São três peças:

```
Arquivos do banco (CSV)  →  scripts/processar.py  →  painel/index.html
  extrato da conta            categoriza tudo          abre no navegador
  fatura do cartão            com as suas regras
```

- Você **baixa** os arquivos do banco uma vez por mês e coloca numa pasta.
- O **script** lê esses arquivos, separa cada lançamento em categorias (Mercado, Moradia, Restaurantes…) e grava o resultado em `dados/dados.js`.
- O **painel** lê esse arquivo e desenha tudo. Não precisa de internet.

Nada depende de inteligência artificial. A "inteligência" está em `regras/categorias.csv`, uma lista de palavras-chave que você mesmo ajusta.

## 2. O que você precisa

- Um computador com Windows, Mac ou Linux
- **Python 3.8 ou mais novo** (gratuito)
- Um navegador (Chrome, Edge, Firefox ou Safari)
- O extrato da conta e a fatura do cartão em **CSV**

Não precisa instalar nenhuma biblioteca extra: o script usa só o que já vem no Python.

## 3. Instalação

1. **Instale o Python:** baixe em [python.org/downloads](https://www.python.org/downloads/).
   - No **Windows**, na primeira tela do instalador, marque **"Add Python to PATH"**. Se esquecer, rode o instalador de novo e escolha *Modify*.
   - No **Mac**, o instalador do site já resolve. Use `python3` no lugar de `python` nos comandos.
2. **Baixe o projeto:** na página do GitHub, clique no botão verde **Code → Download ZIP** e descompacte numa pasta fácil de achar, por exemplo `Documentos/meu-assistente-financeiro`.
3. **Teste:** abra `painel/index.html` com dois cliques. Você deve ver o painel com uma faixa amarela dizendo que são **dados de exemplo**. Se viu, está tudo certo.

### Como abrir o terminal na pasta do projeto

Todos os comandos do manual são digitados no terminal, **dentro da pasta do projeto**.

- **Windows:** abra a pasta no Explorador de Arquivos, clique na barra de endereço, digite `cmd` e aperte Enter.
- **Mac:** clique com o botão direito na pasta no Finder → **Novo Terminal na Pasta**. (Se não aparecer, ative em Ajustes do Sistema → Teclado → Atalhos → Serviços.)
- **Linux:** botão direito na pasta → **Abrir no terminal**.

## 4. Configuração: seu nome e seus números

O projeto vem com um **modelo genérico** (`config.exemplo.json`), com o nome "Seu Nome". Para personalizar:

1. Copie `config.exemplo.json` e renomeie a cópia para **`config.json`**.
   - Pelo terminal: `copy config.exemplo.json config.json` (Windows) ou `cp config.exemplo.json config.json` (Mac/Linux).
2. Abra o `config.json` no Bloco de Notas (Windows) ou TextEdit (Mac) e troque os valores.

| Campo | O que é | Exemplo |
|---|---|---|
| `nome` | Seu nome, aparece no topo do painel | `"Maria Souza"` |
| `nome_assistente` | O nome que você quer dar ao seu assistente. Pode deixar o padrão ou criar um seu | `"Finn da Maria"` |
| `titular_no_banco` | Seu nome **como aparece no extrato**. Serve para reconhecer Pix entre contas suas e não contar como gasto | `"MARIA SOUZA DA SILVA"` |
| `renda_liquida_mensal` | Quanto cai na conta por mês (líquido). Usado quando o salário ainda não caiu e para calcular percentuais | `6500.00` |
| `dia_vencimento_fatura` | Dia do vencimento do cartão | `10` |
| `limite_cartao` | Limite total do cartão | `15000` |
| `valor_gasto_pontual` | Compras acima deste valor saem das médias (iPhone, viagem…) | `1000` |
| `metas_mensais` | Teto por categoria ou subcategoria. O painel avisa quando estoura | `{"Delivery": 300}` |
| `contas_fixas` | As contas que você quer acompanhar mês a mês. `subcategoria` precisa ser igual à das regras | veja o modelo |
| `financiamento` | Dados do financiamento imobiliário. Use `"ativo": false` se não tiver | veja a seção 10 |
| `alpha_vantage_chave` | Chave gratuita para cotações (opcional) | veja a seção 11 |

**Regras do formato** (o JSON é chato com isso):
- Use **ponto** como separador decimal: `6500.50`, nunca `6.500,50`.
- Textos ficam entre aspas duplas `"assim"`.
- Não deixe vírgula depois do último item de uma lista.
- Se o script reclamar do `config.json`, cole o conteúdo em [jsonlint.com](https://jsonlint.com) para achar o erro.

## 5. Baixando os arquivos do banco

### C6 Bank (lido direto)

- **Extrato da conta:** app C6 → Conta → Extrato → escolha o período → **Exportar** → **CSV**.
- **Fatura do cartão:** app C6 → Cartão → Faturas → escolha a fatura **fechada** → **Exportar** → **CSV**. O arquivo vem com o nome `Fatura_AAAA-MM-DD.csv`. Mantenha esse nome: a data é o vencimento.

### Outros bancos

O script entende um CSV simples com estas três colunas:

```
data;descricao;valor
05/11/2026;SUPERMERCADO EXEMPLO;-152,30
06/11/2026;SALARIO EMPRESA X;6500,00
```

Valor **negativo** é saída e **positivo** é entrada. Quase todo banco exporta para Excel ou CSV. Abra o arquivo no Excel ou no Google Planilhas, deixe só essas três colunas, renomeie os títulos e salve como CSV.

> Se o seu banco é muito usado, peça suporte nativo abrindo uma *issue* no GitHub com um exemplo do arquivo (apague nomes e valores).

### Onde colocar os arquivos

Crie a pasta `entrada/` na raiz do projeto, com **uma subpasta por mês**. O nome é livre, mas `AAAA-MM` deixa tudo em ordem:

```
entrada/
  2026-10/
    extrato-outubro.csv
    Fatura_2026-11-10.csv      ← fatura das compras de outubro, que vence em novembro
  2026-11/
    extrato-novembro.csv
    Fatura_2026-12-10.csv
```

**Como o mês é contado (competência):**
- **Conta:** cada lançamento conta no mês da data dele.
- **Cartão:** a fatura conta no **mês anterior ao vencimento**. A fatura que vence em 10/12 tem as compras de novembro, então entra em novembro.

Pode colocar extratos que se sobrepõem (por exemplo, um de 26/10 a 10/11 e outro do mês inteiro): o script ignora as linhas repetidas.

## 6. Processando o mês

No terminal, dentro da pasta do projeto:

```bash
python scripts/processar.py
```

(No Mac/Linux, `python3`.) A saída mostra os arquivos lidos, o total de lançamentos e uma lista dos que ficaram **sem categoria**. Depois, abra (ou atualize com F5) o `painel/index.html`.

O script **refaz tudo do zero** a cada vez, a partir de todas as pastas de `entrada/`. Por isso:
- pode rodar quantas vezes quiser, nada é duplicado;
- se você mudar uma regra, basta rodar de novo que os meses antigos também são recategorizados.

Para ver de novo os dados de exemplo: `python scripts/processar.py --exemplo`.

**Quer ver no celular?** Rode também `python scripts/montar_painel.py`. Ele gera `dados/painel-completo.html`, um arquivo único que abre em qualquer navegador. Ele tem todos os seus dados: guarde só para você.

## 7. Lendo o painel

No topo: o **mês** (setas ‹ › ou a lista), o **olho** que borra os valores (bom para prints) e, no menu, o **tema** claro/escuro.

| Aba | O que mostra |
|---|---|
| **Visão geral** | Resultado do mês (entrou − gasto recorrente), contas fixas pagas, fatura do mês, peso da moradia na renda e patrimônio |
| **Gastos** | Barras por mês (recorrente × pontual), categorias do mês comparadas com a média e as metas, lista de lançamentos |
| **Cartão** | Faturas por vencimento, divisão fixo/variável/pontual, compras da fatura, parcelas futuras, limite livre e melhor data de compra |
| **Contas fixas** | Tabela mês a mês: verde = paga |
| **Financiamento** | Saldo, composição da parcela, juros que faltam e simulador de amortização (seção 10) |
| **Investimentos** | Patrimônio, resultado, alocação e reserva de emergência em meses (seção 11) |
| **A identificar** | Lançamentos que nenhuma regra reconheceu |

**Recorrente × pontual:** o gasto "pontual" (compras grandes e fora da rotina) fica fora das médias, para não distorcer o seu mês normal. Contas da casa, seguros e assinaturas nunca viram pontuais, mesmo se forem caras.

**Lançamentos internos** (aplicação e resgate de investimentos, pagamento da fatura, Pix entre contas suas) não contam como gasto. O pagamento da fatura fica de fora porque as compras já entram uma por uma pela própria fatura.

## 8. Ensinando as categorias

Abra `regras/categorias.csv` no Excel, no Google Planilhas ou no Bloco de Notas. Cada linha é uma regra:

```
padrao;onde;tipo;categoria;subcategoria;pontual
UBER|99 ?APP;ambos;Despesa;Transporte;App e transporte público;0
```

- **padrao:** palavras que aparecem na descrição do lançamento. Use `|` para "ou". Maiúsculas não importam.
- **onde:** `conta`, `cartao` ou `ambos`.
- **tipo:** `Despesa`, `Receita` ou `Interno` (fora dos gastos).
- **categoria / subcategoria:** os nomes que você quiser.
- **pontual:** `1` para sempre tirar das médias.

A **primeira regra que bater vence**, de cima para baixo. Coloque as mais específicas antes. Por exemplo, "MERCADOLIVRE" vem antes de "MERCADO" para não cair em Mercado.

**Suas regras ficam num arquivo separado.** Pessoas que recebem Pix com frequência (diarista, professor, pet shop) e lojas que só você usa vão em **`regras-pessoais.csv`**, na raiz do projeto, no mesmo formato. Esse arquivo é lido antes das regras gerais, não vai para o GitHub e não é apagado quando você baixa uma versão nova do projeto. Veja o exemplo em `exemplo/regras-pessoais.csv`:

```
padrao;onde;tipo;categoria;subcategoria;pontual
MARIA DA SILVA;conta;Despesa;Moradia;Diarista;0
```

**Lançamentos que não estão em nenhum arquivo** (algo pago em dinheiro ou por outra conta): copie `exemplo/ajustes.csv` para a raiz do projeto, como `ajustes.csv`, e acrescente uma linha por lançamento.

Fluxo recomendado no primeiro mês: rode o script, veja a aba **A identificar**, crie as regras que faltam e rode de novo. Em dois ou três meses, quase nada fica sem categoria.

## 9. A rotina do dia 11 (tarefa agendada)

**Por que dia 11?** O cartão do modelo vence no dia 10 e o salário cai no começo do mês. No dia 11, a fatura do mês anterior já fechou e foi paga, e o extrato tem todas as contas. Se o seu vencimento for outro, use o dia seguinte ao vencimento.

A rotina tem uma parte **manual** e uma **automática**:

1. **Manual (5 minutos):** baixar o extrato e a fatura e salvar na pasta `entrada/AAAA-MM/`. Nenhum banco brasileiro oferece um jeito gratuito e oficial de baixar isso sozinho para pessoa física.
2. **Automática:** processar, atualizar as cotações e abrir o painel. O projeto traz os scripts prontos em `automacao/`.

### Windows: Agendador de Tarefas

1. Menu Iniciar → digite **Agendador de Tarefas** → abra.
2. À direita, **Criar Tarefa Básica…**
3. Nome: `Meu Assistente Financeiro`. Avançar.
4. Disparador: **Mensalmente**. Avançar. Meses: **todos**. Dias: **11**. Hora: por exemplo **09:00**.
5. Ação: **Iniciar um programa**. Em *Programa/script*, clique em Procurar e escolha `automacao\rotina-mensal-windows.bat` dentro da pasta do projeto.
6. Concluir.

No dia 11, se o computador estiver ligado, o script roda e abre o painel. Se estiver desligado, a tarefa roda na próxima vez que você ligar, desde que você marque, nas propriedades da tarefa, **"Executar a tarefa assim que possível após uma inicialização agendada ter sido perdida"**.

### Mac e Linux: cron

No terminal, digite `crontab -e` e acrescente a linha (troque o caminho):

```
0 9 11 * * /Users/seu-usuario/Documentos/meu-assistente-financeiro/automacao/rotina-mensal.sh
```

Isso roda todo dia 11 às 9h. No Mac, o Terminal pode precisar de permissão em Ajustes do Sistema → Privacidade → Acesso Total ao Disco.

### Lembrete no celular

Crie um lembrete recorrente, todo dia 11, para "baixar extrato e fatura". É a única parte que depende de você.

## 10. Financiamento imobiliário

Preencha o bloco `financiamento` do `config.json` com os números do **app do seu banco** (na Caixa: Habitação → seu contrato → Detalhes do contrato):

```json
"financiamento": {
  "ativo": true,
  "banco": "Caixa",
  "data_ref": "2026-11-10",
  "saldo_devedor": 128000.00,
  "meses_restantes": 235,
  "prazo_total": 360,
  "valor_financiado": 170000.00,
  "juros_aa": 7.5
}
```

E garanta que a parcela do extrato caia na subcategoria **Financiamento habitacional** (a regra `CAIXA - HABITA` já faz isso para a Caixa; para outro banco, crie a sua).

O painel calcula:
- **Composição da parcela:** amortização (saldo ÷ meses restantes), juros (saldo × taxa ÷ 12) e seguros e taxas (o que sobra da última parcela paga).
- **Juros que ainda faltam** e **quando a amortização passa a ser maior que os juros**.
- **Simulador:** um valor único agora e/ou um extra todo mês, reduzindo **prazo** ou **parcela**. Mostra a nova data de quitação, os juros economizados e quanto cada R$ 1 extra poupa.

**Atualize a cada poucos meses** com um novo print do app, já que a TR muda o saldo. As contas supõem **tabela SAC e TR zero**: são estimativas, não o valor oficial do banco. Antes de amortizar, simule também no app do banco e lembre que, enquanto você não tiver reserva de emergência, guardar costuma ser melhor que amortizar.

## 11. Investimentos e cotações

Copie `exemplo/carteira.csv` para a raiz do projeto e edite:

```
ticker;nome;classe;moeda;quantidade;preco_medio
CDB;CDB banco (reserva);Renda fixa;BRL;1;15000
BOVA11;ETF Ibovespa;Ações BR;BRL;20;150.00
```

- **classe:** use `Renda fixa` para a reserva de emergência (CDB, Tesouro Selic). A aba Investimentos calcula quantos meses de gasto ela cobre.
- Para renda fixa, use `quantidade` 1 e o valor aplicado em `preco_medio`.

As cotações ficam em `cotacoes.csv` (`ticker;data;preco`). Duas formas de atualizar:

- **À mão:** acrescente uma linha com o preço do dia. Para renda fixa, use o valor atual do app do banco.
- **Automático (grátis):** pegue uma chave em [alphavantage.co](https://www.alphavantage.co/support/#api-key) (só pede um e-mail), coloque em `alpha_vantage_chave` no `config.json` e rode `python scripts/cotacoes.py`. O plano gratuito permite 25 consultas por dia, suficiente para uma carteira de até uns 20 ativos. Ações da B3 são buscadas como `TICKER.SAO`; ações dos EUA, pelo próprio ticker (preencha a coluna `moeda` com `USD`).

## Limitações

O que a versão **sem IA** não faz, e o que você precisa fazer à mão:

| Limitação | Como contornar |
|---|---|
| **Baixar os arquivos do banco é manual.** Não há conexão automática com o banco (Open Finance para pessoa física não tem acesso gratuito para scripts caseiros) | Lembrete no dia 11; leva uns 5 minutos |
| **Categorizar exige criar regras.** O script só reconhece o que está em `regras/categorias.csv`. Nomes novos ficam em "A identificar" | Use a aba A identificar e crie a regra uma vez. Com o tempo, quase nada fica pendente |
| **Não entende contexto.** Não sabe que um Pix para uma pessoa é a diarista, ou que um Pix recebido é a parcela de algo que você vendeu | Crie a regra com o nome da pessoa |
| **Só lê CSV do C6 de forma nativa.** Outros bancos precisam virar o CSV simples (`data;descricao;valor`) | Ajuste no Excel. Contribuições com leitores de outros bancos são bem-vindas |
| **Não lê PDF nem print.** Holerite, print do app do financiamento e posição de investimentos são digitados no `config.json` ou nos CSVs | São poucos números e mudam pouco |
| **O painel fica no computador.** Não há link para abrir no celular de qualquer lugar | Rode `python scripts/montar_painel.py`: ele gera `dados/painel-completo.html`, um arquivo único com tudo dentro, que abre no celular (mande para você pelo Drive ou iCloud). Ele contém todos os seus lançamentos: nunca publique nem compartilhe |
| **Agendamento depende do computador ligado** | Use a opção de rodar após inicialização perdida (Windows) ou rode à mão |
| **Não dá conselho nem resume o mês em texto** | O painel mostra os números; a análise é sua. Quem usa uma IA pode colar o resumo e pedir opinião |
| **Projeções são simplificadas** (financiamento em SAC sem TR, "melhor data de compra" pela regra da última sexta-feira antes do vencimento) | Confira sempre com o app do banco |

O que você **ganha** usando com o Claude (plano pago) está no [manual da versão com Claude](../claude/MANUAL-CLAUDE.md).

## 13. Privacidade

- O processamento e o painel funcionam **sem internet**. Seus extratos nunca saem do computador.
- O `.gitignore` impede que `config.json`, `entrada/`, `dados/`, `ajustes.csv`, `carteira.csv` e `cotacoes.csv` vão para o GitHub se você fizer um fork. Mesmo assim, **confira antes de qualquer `git push`**.
- O botão do olho borra os valores para você tirar print sem expor números.
- A chave da Alpha Vantage fica só no seu `config.json`.

## 14. Problemas comuns

**"python não é reconhecido como um comando"**: o Python não foi adicionado ao PATH. Reinstale marcando "Add Python to PATH", ou use `py` no lugar de `python` no Windows.

**O painel continua mostrando dados de exemplo**: o script não gerou `dados/dados.js`. Rode `python scripts/processar.py` e veja a mensagem de erro.

**"Falta o config.json"**: você não criou a cópia do `config.exemplo.json` com o nome `config.json`.

**Acentos estranhos (Ã§ no lugar de ç)**: salve os CSVs como **UTF-8** (no Excel: Salvar como → CSV UTF-8).

**Um gasto caiu na categoria errada**: alguma regra mais acima bateu primeiro. Mova a regra certa para cima ou deixe o padrão mais específico.

**A fatura caiu no mês errado**: confira se o nome do arquivo tem a data de vencimento (`Fatura_2026-12-10.csv`). Sem a data, o script estima pelo `dia_vencimento_fatura`.

**Ficou com dúvida ou achou um erro?** Abra uma *issue* no GitHub do projeto.
