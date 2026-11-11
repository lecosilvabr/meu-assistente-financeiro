# Usar com o Claude (opcional, plano pago)

A versão original deste projeto roda com o **Claude**, assistente de IA da Anthropic. Nela, o próprio Claude faz o papel do `processar.py`: lê os arquivos, categoriza, pergunta o que não reconhece e mantém um painel publicado que abre no celular.

Isto é **opcional**. Tudo funciona sem IA (veja o [Manual](../docs/MANUAL.md)). Esta página é para quem já assina um plano pago do Claude (Pro ou superior) e quer a versão mais automática.

> Os recursos do Claude mudam com frequência. Os nomes abaixo eram os disponíveis quando o projeto foi publicado; confira a [central de ajuda](https://support.claude.com).

## O que muda

| | Sem IA | Com Claude |
|---|---|---|
| Categorizar | Regras fixas em CSV | O Claude categoriza pelo contexto, pergunta os casos novos e guarda a resposta nas regras do projeto |
| Pix para pessoas | Você cria a regra | O Claude lista os Pix novos e pergunta "quem é?" |
| Holerite, prints do app do banco | Você digita os números | Você manda o PDF ou o print e o Claude extrai os números |
| Rotina do dia 11 | Script no seu computador | **Tarefa agendada** no Claude, que roda na nuvem mesmo com o computador desligado |
| Painel | Arquivo no seu computador | Dashboard publicado, privado, abre no celular |
| Resumo do mês | Você lê os números | O Claude manda um resumo: resultado, metas, alertas e contas sem pagamento |

## Montagem (uma vez)

1. **Crie um Projeto** no Claude chamado, por exemplo, "Finanças pessoais".
2. **Suba as regras:** copie [`regras-modelo.md`](regras-modelo.md) para o projeto e troque os campos entre `<>` pelos seus (nome, banco, dia de vencimento, renda, contas fixas). Esse documento é a "memória" do assistente: toda conversa e toda tarefa agendada leem ele.
3. **Conecte o Google Drive** (em Configurações → Conectores) e crie uma pasta, por exemplo `Finanças Pessoais`, com uma subpasta por mês (`nov26`, `dez26`…, ou `2026-11`, `2026-12`…: escolha um formato e anote nas regras).
4. **Primeira carga:** numa conversa do projeto, anexe os extratos e as faturas dos últimos meses e peça:
   > Monte um dashboard das minhas finanças a partir destes arquivos, seguindo o documento de regras do projeto. Me pergunte o que não souber categorizar.
5. **Personalize:** dê um nome ao seu assistente, peça abas novas (financiamento, investimentos, "a receber"), metas etc. Cada decisão importante vale ser anotada no documento de regras ("anote isso nas regras").

## A tarefa agendada do dia 11

Peça ao Claude, numa conversa do projeto:

> Crie uma tarefa agendada que rode todo dia 11 às 9h com o prompt do arquivo prompt-tarefa-agendada.md.

O texto do prompt está em [`prompt-tarefa-agendada.md`](prompt-tarefa-agendada.md). Troque os campos entre `<>` antes.

Pontos de atenção:
- A tarefa roda numa **sessão nova**, sem lembrar das conversas. Por isso tudo o que ela precisa saber tem de estar no documento de regras.
- Ela pode precisar de **aprovação** para algumas ações. Se você quer que ela rode sozinha, veja nas configurações da tarefa se sua conta permite aprovação automática.
- Se a pasta do mês estiver vazia, a tarefa só avisa e para. Você sobe os arquivos e roda de novo.

## Limites do plano gratuito do Claude

No plano gratuito você pode usar o Claude para **categorizar um mês** colando o extrato numa conversa e para **gerar regras** para o `categorias.csv` ("leia este extrato e me devolva linhas no formato padrao;onde;tipo;categoria;subcategoria;pontual"). Recursos como tarefas agendadas, conectores e painéis publicados dependem do plano e podem mudar; confira a página de planos.

## Privacidade

Ao usar o Claude, seus extratos são enviados para a Anthropic para processamento, conforme os termos e a política de privacidade do serviço. Se isso for um problema para você, use a versão sem IA, que não envia nada para fora do seu computador.
