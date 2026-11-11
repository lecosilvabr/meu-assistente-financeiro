# Manual da versão com Claude

Esta é a versão para quem assina um **plano pago do Claude**. O código e as regras são os mesmos da versão sem IA. A diferença é que o próprio Claude roda tudo, pergunta o que não reconhece, lê PDFs e prints, publica o painel num link que abre no celular e faz a rotina do dia 11 sozinho, na nuvem.

> Testado em novembro de 2026. Os recursos do Claude (skills, Projetos, conectores, tarefas agendadas e páginas publicadas) dependem do plano e mudam com frequência. Se algum nome de menu estiver diferente, procure na [central de ajuda](https://support.claude.com).

**Sumário**

1. [O que você ganha em relação à versão sem IA](#1-o-que-você-ganha)
2. [Instalar a skill](#2-instalar-a-skill)
3. [Criar o Projeto](#3-criar-o-projeto)
4. [Conectar o Google Drive](#4-conectar-o-google-drive)
5. [Primeira conversa: configurar e dar nome ao assistente](#5-primeira-conversa)
6. [A rotina do dia 11 (tarefa agendada)](#6-a-rotina-do-dia-11)
7. [O dia a dia](#7-o-dia-a-dia)
8. [Limitações e custos](#8-limitações-e-custos)
9. [Privacidade](#9-privacidade)

---

## 1. O que você ganha

| | Sem IA | Com Claude |
|---|---|---|
| Rodar o processamento | Você roda o script ou agenda no computador | O Claude roda, mesmo com o computador desligado |
| Lançamento desconhecido | Vai para "A identificar" e você cria a regra | O Claude pergunta "quem é?" e grava a regra sozinho |
| Holerite, print do financiamento | Você digita os números | Você manda o PDF ou o print |
| Painel | Arquivo no computador | Página privada com link, que abre no celular |
| Resumo do mês | Você lê o painel | O Claude manda o resumo: resultado, metas estouradas, alertas |
| Personalizar o painel | Editar HTML | Pedir: "cria uma aba de viagens" |

## 2. Instalar a skill

A skill é o "manual de instruções" que ensina o Claude a ser o seu assistente financeiro.

1. Baixe o arquivo [`assistente-financeiro.zip`](assistente-financeiro.zip): abra o link e clique em **Download raw file** (ícone de download).
2. No Claude, vá em **Configurações → Capacidades → Skills** (o nome pode variar) e envie o .zip, sem descompactar.
3. Confira se a skill **assistente-financeiro** aparece ativada.

Se o seu plano não mostrar a opção de skills, use o [plano B](#plano-b-sem-skills) no fim desta página.

## 3. Criar o Projeto

O Projeto guarda a memória do assistente: sua configuração e suas regras.

1. Crie um Projeto chamado, por exemplo, **Finanças pessoais**.
2. Nas **instruções do Projeto**, cole o texto de [`projeto/instrucoes-do-projeto.md`](projeto/instrucoes-do-projeto.md).
3. Não precisa criar os outros documentos: o assistente cria `financas/config.json` e `financas/regras-pessoais.csv` na primeira conversa.

## 4. Conectar o Google Drive

É o que permite a rotina do dia 11 rodar sem você anexar nada.

1. Em **Configurações → Conectores**, conecte o **Google Drive**.
2. No seu Drive, crie uma pasta (por exemplo, `Finanças`) com **uma subpasta por mês**. O nome da subpasta é livre: `2026-11`, `nov26`…
3. Todo mês, coloque na subpasta do mês:
   - o extrato da conta em CSV;
   - a fatura do cartão em CSV (no C6, o nome `Fatura_AAAA-MM-DD.csv` já traz a data de vencimento);
   - o holerite, se quiser que a renda seja atualizada.

Como baixar os arquivos do banco: veja a [seção 5 do manual principal](../docs/MANUAL.md#5-baixando-os-arquivos-do-banco).

## 5. Primeira conversa

Abra uma conversa **dentro do Projeto**, anexe os extratos e as faturas dos últimos 2 ou 3 meses e escreva:

> Configura meu assistente financeiro.

O assistente vai perguntar, de uma vez:
- **seu nome** e **o nome que você quer dar a ele**. O modelo vem como "Meu Assistente Financeiro", mas você pode criar o seu ("Finn da Ana", "Contador Zé"…). Dá para trocar depois: "muda o nome do assistente para X";
- seu nome como aparece no extrato;
- renda líquida, vencimento e limite do cartão;
- quais contas fixas acompanhar;
- se tem financiamento (mande o print da tela de detalhes do contrato no app do banco);
- se quer acompanhar investimentos;
- o nome da pasta do Drive.

Depois ele processa os arquivos, pergunta sobre os lançamentos que não reconheceu ("Pix para JOÃO EXEMPLO, 2 vezes, R$ 160: o que é?"), publica o painel e manda o link. Guarde o link nos favoritos do celular.

Veja um exemplo de configuração fictícia em [`projeto/config-exemplo-para-o-projeto.json`](projeto/config-exemplo-para-o-projeto.json).

## 6. A rotina do dia 11

**Por que dia 11:** o cartão do modelo vence no dia 10. No dia 11, a fatura do mês anterior já fechou e o extrato tem as contas pagas no começo do mês. Se o seu cartão vence em outro dia, use o dia seguinte.

1. Numa conversa do Projeto, peça:
   > Cria uma tarefa agendada para todo dia 11 às 9h com este texto: (cole o texto de [`tarefas/rotina-dia-11.md`](tarefas/rotina-dia-11.md))
2. Confira a tarefa na lista de tarefas agendadas.
3. **Aprovação:** dependendo da conta, a tarefa pode parar para pedir aprovação de algumas ações (como publicar o painel). Se você quer que ela rode sozinha, veja nas configurações da tarefa se sua conta permite aprovação automática.

**O que continua manual:** colocar o extrato e a fatura na pasta do Drive até o dia 11. Crie um lembrete no celular para o dia 10 ou 11. Se a pasta estiver vazia, a tarefa avisa e para; você sobe os arquivos e pede "roda a rotina do mês".

**Opcional: cotações diárias.** Se você tem ações e um conector de cotações, use [`tarefas/cotacoes-diarias.md`](tarefas/cotacoes-diarias.md).

## 7. O dia a dia

Exemplos do que pedir numa conversa do Projeto:

- "Processa outubro" (com os arquivos anexados ou já no Drive)
- "O Pix para MARIA DA SILVA é a diarista"
- "Esse holerite é o novo, atualiza a renda" (com o PDF)
- "Atualiza o financiamento" (com o print do app do banco)
- "Comprei 10 cotas de BOVA11 a R$ 150" ou "atualiza minha carteira" (com a nota de corretagem)
- "Põe uma meta de R$ 400 para delivery"
- "Cria uma aba com os gastos de viagem"
- "Quanto eu economizo de juros se amortizar R$ 5 mil?"

Toda mudança fica salva no Projeto, e o painel é publicado de novo no **mesmo link**.

## 8. Limitações e custos

- **Precisa de plano pago** para skills, conectores, tarefas agendadas e páginas publicadas. Confira os recursos do seu plano.
- **Baixar os arquivos do banco continua manual.** O Claude não acessa a sua conta bancária.
- **Limites de uso:** processar muitos meses de uma vez gasta mais do limite do plano. Depois da primeira carga, é um mês por vez.
- **A IA pode errar uma categoria.** Corrija dizendo o certo; a correção vira regra e não se repete.
- **As tarefas agendadas rodam numa conversa nova.** Tudo o que o assistente precisa saber tem que estar nos documentos do Projeto, e a skill cuida disso.
- **Projeções são estimativas** (financiamento em SAC sem TR). Não é recomendação financeira.

## 9. Privacidade

- Seus extratos são enviados à Anthropic para processamento, conforme os termos e a política de privacidade do Claude. Se isso não serve para você, use a versão sem IA, que não envia nada para fora do computador.
- O painel é publicado como página **privada**: só você vê, a não ser que você mesmo compartilhe.
- Para mostrar a alguém, use o botão do **olho**, que borra os valores.
- Nada dos seus dados vai para o GitHub: este repositório só tem código e exemplos fictícios.

---

### Plano B: sem skills

Se o seu plano não tem skills, dá para usar quase tudo mesmo assim:

1. Crie o Projeto e suba nele os arquivos `scripts/processar.py`, `scripts/montar_painel.py`, `painel/index.html`, `regras/categorias.csv` e `config.exemplo.json` deste repositório, junto com o `SKILL.md` da pasta [`skill/assistente-financeiro`](skill/assistente-financeiro/SKILL.md).
2. Nas instruções do Projeto, troque "Use sempre a skill assistente-financeiro" por "Siga o SKILL.md deste Projeto, usando os arquivos dele no lugar da pasta da skill".
3. Se o Claude não conseguir rodar os arquivos direto do Projeto, anexe-os na conversa junto com os extratos.
4. O resto do manual vale igual.
