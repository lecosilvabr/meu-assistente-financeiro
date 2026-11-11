#!/usr/bin/env python3
"""
Meu Assistente Financeiro — processamento mensal (não precisa de IA).

Lê os extratos da conta e as faturas do cartão em entrada/<AAAA-MM>/,
categoriza com regras/categorias.csv, soma os ajustes manuais e gera
dados/dados.js, que o painel (painel/index.html) abre direto no navegador.

Uso:
    python scripts/processar.py            # usa seus dados (config.json, entrada/)
    python scripts/processar.py --exemplo  # usa os dados fictícios de exemplo/

Só usa a biblioteca padrão do Python 3.8+. Nada sai do seu computador.
"""
import csv
import datetime as dt
import glob
import io
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------- utilidades
def ler_texto(caminho):
    for enc in ('utf-8-sig', 'latin-1'):
        try:
            with open(caminho, encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    raise RuntimeError('Não consegui ler ' + caminho)


def num(v):
    """Converte '1.234,56', '1234.56' ou '-12,3' em float."""
    v = str(v or '').strip().replace('R$', '').replace(' ', '')
    if not v:
        return 0.0
    if ',' in v and '.' in v:
        v = v.replace('.', '').replace(',', '.') if v.rfind(',') > v.rfind('.') else v.replace(',', '')
    elif ',' in v:
        v = v.replace(',', '.')
    return float(v)


def data_iso(v):
    v = v.strip()
    for fmt in ('%d/%m/%Y', '%Y-%m-%d', '%d/%m/%y'):
        try:
            return dt.datetime.strptime(v, fmt).date()
        except ValueError:
            pass
    raise ValueError('Data inválida: ' + v)


def mes_anterior(d):
    return (d.replace(day=1) - dt.timedelta(days=1)).strftime('%Y-%m')


def limpa(s):
    return re.sub(r'\s+', ' ', str(s or '')).replace('\\', '').strip()


# ---------------------------------------------------------------- regras
def carregar_regras(caminho):
    regras = []
    for linha in ler_texto(caminho).splitlines()[1:]:
        if not linha.strip() or linha.startswith('#'):
            continue
        p = linha.split(';')
        if len(p) < 5:
            continue
        regras.append({'re': re.compile(p[0], re.I), 'onde': p[1].strip().lower(), 'tipo': p[2].strip(),
                       'categoria': p[3].strip(), 'subcategoria': p[4].strip(),
                       'pontual': (p[5].strip() if len(p) > 5 else '0') == '1'})
    return regras


def categorizar(texto, origem, entrada, saida, regras, titular):
    onde = 'conta' if origem == 'Conta' else 'cartao'
    for r in regras:
        if r['onde'] not in (onde, 'ambos'):
            continue
        if r['re'].search(texto):
            tipo, cat, sub = r['tipo'], r['categoria'], r['subcategoria']
            if tipo == 'Despesa' and entrada > 0 and saida == 0:
                return 'Receita', 'Outras entradas', 'Estornos e devoluções', False
            return tipo, cat, sub, r['pontual']
    if titular and titular.upper() in texto.upper() and 'PIX' in texto.upper():
        return 'Interno', 'Transferência própria', 'Entre contas suas', False
    if re.search(r'Pix recebido', texto, re.I) or entrada > 0:
        return 'Receita', 'Outras entradas', 'Pix e créditos recebidos', False
    if re.search(r'Pix enviado', texto, re.I):
        return 'Despesa', 'Pix para pessoas', 'A identificar', False
    return 'Despesa', 'Outros', 'A identificar', False


# ---------------------------------------------------------------- leitores
def ler_extrato_c6(texto):
    """Extrato CSV do C6 Bank (conta corrente). Pula o cabeçalho até 'Data Lançamento'."""
    linhas = texto.splitlines()
    ini = next(i for i, l in enumerate(linhas) if l.strip().startswith('Data Lan'))
    out = []
    for r in csv.DictReader(io.StringIO('\n'.join(l.strip() for l in linhas[ini:]))):
        r = {k.strip(): v for k, v in r.items() if k}
        if not r.get('Data Lançamento'):
            continue
        titulo, desc = limpa(r.get('Título')), limpa(r.get('Descrição'))
        if titulo.upper().startswith('DEBITO DE CARTAO'):
            descricao = re.sub(r'\s+(RIO DE JANEIR|SAO PAULO|BRA)\b.*$', '', desc, flags=re.I).strip() or desc
        elif titulo.startswith('Pix '):
            descricao = titulo
        else:
            descricao = titulo if titulo == desc or not desc else titulo + ' · ' + desc
        out.append({'data': data_iso(r['Data Lançamento']), 'descricao': descricao, 'texto': titulo + ' | ' + desc,
                    'entrada': num(r.get('Entrada(R$)')), 'saida': num(r.get('Saída(R$)'))})
    return out


def ler_extrato_generico(texto):
    """CSV simples: data;descricao;valor (valor negativo = saída). Aceita ',' ou ';'."""
    sep = ';' if texto.count(';') > texto.count(',') else ','
    out = []
    for r in csv.DictReader(io.StringIO(texto), delimiter=sep):
        r = {k.strip().lower(): v for k, v in r.items() if k}
        v = num(r.get('valor'))
        out.append({'data': data_iso(r['data']), 'descricao': limpa(r.get('descricao')), 'texto': limpa(r.get('descricao')),
                    'entrada': max(v, 0), 'saida': max(-v, 0)})
    return out


def ler_fatura_c6(texto, vencimento):
    """Fatura CSV do cartão C6 (separada por ';')."""
    out = []
    for r in csv.DictReader(io.StringIO(texto), delimiter=';'):
        r = {k.strip(): v for k, v in r.items() if k}
        desc = limpa(r.get('Descrição'))
        if not desc or 'Inclusao de Pagamento' in desc or desc.startswith('Pagamento'):
            continue
        v = num(r.get('Valor (em R$)'))
        parcela = limpa(r.get('Parcela'))
        out.append({'data': data_iso(r['Data de Compra']), 'descricao': desc, 'texto': desc + ' | ' + limpa(r.get('Categoria')),
                    'entrada': max(-v, 0), 'saida': max(v, 0), 'parcela': '' if parcela in ('', 'Única') else parcela,
                    'vencimento': vencimento})
    return out


def vencimento_da_fatura(nome, compras, dia):
    m = re.search(r'(\d{4}-\d{2}-\d{2})', nome)
    if m:
        return dt.date.fromisoformat(m.group(1))
    ult = max(c['data'] for c in compras)
    ano, mes = (ult.year + (ult.month // 12), ult.month % 12 + 1)
    return dt.date(ano, mes, min(dia, 28))


# ---------------------------------------------------------------- principal
def main():
    exemplo = '--exemplo' in sys.argv
    base = os.path.join(RAIZ, 'exemplo') if exemplo else RAIZ
    cfg_path = os.path.join(base, 'config.json')
    if not os.path.exists(cfg_path):
        sys.exit('Falta o config.json. Copie config.exemplo.json para config.json e preencha com os seus dados.')
    cfg = json.loads(ler_texto(cfg_path))
    regras = carregar_regras(os.path.join(RAIZ, 'regras', 'categorias.csv'))
    titular = cfg.get('titular_no_banco', '')
    dia_venc = int(cfg.get('dia_vencimento_fatura', 10))
    lim_pontual = float(cfg.get('valor_gasto_pontual', 1000))
    subs_fixas = {c.get('subcategoria') for c in cfg.get('contas_fixas', [])}
    NUNCA_PONTUAL = ('Moradia', 'Seguros', 'Assinaturas', 'Impostos e taxas')  # contas da rotina, mesmo se caras

    lanc, faturas, parcelas_futuras = [], [], []
    pastas = sorted(glob.glob(os.path.join(base, 'entrada', '*')))
    if not pastas:
        sys.exit('Nenhuma pasta em entrada/. Crie entrada/AAAA-MM/ e coloque o extrato e a fatura do mês.')

    vistos_conta = set()
    ultima_fatura = None
    for pasta in pastas:
        for arq in sorted(glob.glob(os.path.join(pasta, '*.csv'))):
            texto = ler_texto(arq)
            nome = os.path.basename(arq)
            if 'Data Lan' in texto and 'Saldo do Dia' in texto:
                itens, origem = ler_extrato_c6(texto), 'Conta'
            elif 'Data de Compra' in texto:
                bruto = ler_fatura_c6(texto, None)
                if not bruto:
                    continue
                venc = vencimento_da_fatura(nome, bruto, dia_venc)
                for b in bruto:
                    b['vencimento'] = venc
                itens, origem = bruto, 'Cartão'
            elif re.search(r'^\s*data\s*[;,]', texto, re.I | re.M):
                itens, origem = ler_extrato_generico(texto), 'Conta'
            else:
                print('  ignorado (formato desconhecido):', nome)
                continue
            print('  lido:', os.path.relpath(arq, base), '-', len(itens), 'linhas', '(' + origem + ')')
            for it in itens:
                if origem == 'Conta':
                    chave = (it['data'], it['entrada'], it['saida'], it['texto'])
                    if chave in vistos_conta:   # extratos que se sobrepõem
                        continue
                    vistos_conta.add(chave)
                    mes = it['data'].strftime('%Y-%m')
                else:
                    mes = mes_anterior(it['vencimento'])
                tipo, cat, sub, pont = categorizar(it['texto'], origem, it['entrada'], it['saida'], regras, titular)
                if (tipo == 'Despesa' and it['saida'] >= lim_pontual and not it.get('parcela')
                        and sub not in subs_fixas and cat not in NUNCA_PONTUAL):
                    pont = True
                lanc.append({'data': it['data'].isoformat(), 'mes': mes, 'origem': origem, 'tipo': tipo,
                             'categoria': cat, 'subcategoria': sub, 'descricao': it['descricao'],
                             'parcela': it.get('parcela', ''), 'entrada': round(it['entrada'], 2),
                             'saida': round(it['saida'], 2), 'pontual': 1 if pont and tipo == 'Despesa' else 0,
                             'vencimento': it['vencimento'].isoformat() if origem == 'Cartão' else ''})
            if origem == 'Cartão':
                if ultima_fatura is None or itens[0]['vencimento'] > ultima_fatura:
                    ultima_fatura = itens[0]['vencimento']

    # ajustes manuais (lançamentos que não estão nos arquivos, ou correções)
    aj = os.path.join(base, 'ajustes.csv')
    if os.path.exists(aj):
        for r in csv.DictReader(io.StringIO(ler_texto(aj)), delimiter=';'):
            if not r.get('data') or r['data'].startswith('#'):
                continue
            d = data_iso(r['data'])
            lanc.append({'data': d.isoformat(), 'mes': r.get('mes') or d.strftime('%Y-%m'), 'origem': r.get('origem') or 'Conta',
                         'tipo': r['tipo'], 'categoria': r['categoria'], 'subcategoria': r['subcategoria'],
                         'descricao': r['descricao'] + ' (ajuste)', 'parcela': '', 'entrada': num(r.get('entrada')),
                         'saida': num(r.get('saida')), 'pontual': int(r.get('pontual') or 0), 'vencimento': ''})

    lanc.sort(key=lambda l: (l['mes'], l['data']))
    for i, l in enumerate(lanc, 1):
        l['id'] = i

    # resumo por fatura
    for venc in sorted({l['vencimento'] for l in lanc if l['origem'] == 'Cartão'}):
        g = [l for l in lanc if l['vencimento'] == venc]
        desp = [l for l in g if l['tipo'] == 'Despesa']
        fixo = sum(l['saida'] for l in desp if l['parcela'] or l['categoria'] in ('Assinaturas', 'Seguros') and not l['pontual'])
        pont = sum(l['saida'] for l in desp if l['pontual'])
        cred = sum(l['entrada'] for l in g if l['tipo'] == 'Receita')
        total = sum(l['saida'] for l in desp) - cred
        faturas.append({'vencimento': venc, 'competencia': mes_anterior(dt.date.fromisoformat(venc)), 'total': round(total, 2),
                        'fixo': round(fixo, 2), 'pontual': round(pont, 2), 'variavel': round(total - fixo - pont, 2)})

    # parcelas que ainda vão vencer (da fatura mais recente)
    if ultima_fatura:
        for l in lanc:
            m = re.match(r'(\d+)/(\d+)', l['parcela'] or '')
            if l['vencimento'] == ultima_fatura.isoformat() and m and int(m.group(1)) < int(m.group(2)):
                falta = int(m.group(2)) - int(m.group(1))
                parcelas_futuras.append({'descricao': l['descricao'], 'parcela': l['parcela'], 'valor': l['saida'],
                                         'restantes': falta, 'total': round(falta * l['saida'], 2)})

    # carteira de investimentos e cotações (opcionais)
    def ler_csv_opcional(nome):
        p = os.path.join(base, nome)
        if not os.path.exists(p):
            return []
        return list(csv.DictReader(io.StringIO(ler_texto(p)), delimiter=';'))

    publico = {k: v for k, v in cfg.items() if not k.startswith('_') and k not in ('alpha_vantage_chave', 'titular_no_banco')}
    dados = {'gerado_em': dt.datetime.now().strftime('%Y-%m-%d %H:%M'), 'exemplo': exemplo, 'config': publico,
             'lancamentos': lanc, 'faturas': faturas, 'parcelas': parcelas_futuras,
             'carteira': ler_csv_opcional('carteira.csv'), 'cotacoes': ler_csv_opcional('cotacoes.csv')}

    destino = os.path.join(RAIZ, 'painel', 'dados-exemplo.js') if exemplo else os.path.join(RAIZ, 'dados', 'dados.js')
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, 'w', encoding='utf-8') as f:
        f.write('// Gerado por scripts/processar.py em ' + dados['gerado_em'] + '. Não edite à mão.\n')
        f.write('window.DADOS = ' + json.dumps(dados, ensure_ascii=False) + ';\n')
    if not exemplo:
        with open(os.path.join(RAIZ, 'dados', 'lancamentos.csv'), 'w', encoding='utf-8-sig', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(lanc[0].keys()) if lanc else ['id'], delimiter=';')
            w.writeheader()
            w.writerows(lanc)

    # resumo no terminal
    print('\nPronto:', len(lanc), 'lançamentos,', len(faturas), 'faturas →', os.path.relpath(destino, RAIZ))
    pend = [l for l in lanc if l['subcategoria'] == 'A identificar']
    if pend:
        print('\n', len(pend), 'lançamentos sem categoria (veja a aba "A identificar" do painel e crie regras para eles):')
        for l in pend[-10:]:
            print('   ', l['data'], l['descricao'][:50], l['saida'] or l['entrada'])
    print('\nAbra painel/index.html no navegador.')


if __name__ == '__main__':
    main()
