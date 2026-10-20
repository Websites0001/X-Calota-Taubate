"""Gera js/dados.js do X Calota Taubaté a partir do cardápio do Brendi (produtos.json + nuxt.json).
Rode dentro desta pasta: python gerar_dados.py"""
import json, os, re, unicodedata

os.chdir(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open('produtos.json', encoding='utf-8'))
N = json.load(open('nuxt.json', encoding='utf-8'))
M = json.load(open('manifest.json', encoding='utf-8'))
STORE = N['data']['menu-x-calota-taubate']['store']
OUT = os.path.join('..', 'js', 'dados.js')


def slug(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def nome_limpo(n):
    n = re.sub(r'\s+', ' ', n).strip()
    fix = {'cotra filé': 'Contra Filé', 'Entreveiro': 'Entrevero', 'entrevero': 'Entrevero', 'COCA 2L': 'Coca-Cola 2 L',
           'Coca 2L': 'Coca-Cola 2 L', 'Coca-Cola 2L': 'Coca-Cola 2 L', '350Ml': '350 ml', 'Coca-Cola Original 2l': 'Coca-Cola Original 2 L',
           'Calotinha bacon': 'Calotinha Bacon', 'acebolado': 'Acebolado', 'Ao Alho': 'ao Alho', 'c/ ': 'com ',
           '( ': '(', 'com frango': 'com Frango', 'Combo Calota': 'Calota'}
    for a, b in fix.items():
        n = n.replace(a, b)
    return n


CATS = [
    ('UFHHaxWnP9jAeP3ujUd6', 'calotas', 'Calotas', 'Calotas', '28 cm, cortada em 4 pedaços. Serve até 4 pessoas.'),
    ('i5fLPeFEUX5VIb6pNodA', 'calotinhas', 'Calotinhas', 'Calotinhas', 'O mesmo recheio, no tamanho de uma pessoa.'),
    ('LzxDGxoeeEbNVD4dzlbv', 'combos', 'Combos', 'Combos', 'Calota ou Calotinha com Coca-Cola.'),
    ('fritas', 'fritas', 'Fritas', 'Fritas', 'Tradicional ou Xcb, com molho especial e bacon.'),
    ('VxaYjjwXOXzce5PQoEcB', 'molhos', 'Molhos', 'Molhos', 'Para acompanhar o lanche ou as fritas.'),
    ('oXBQ4PXIDmfwG84GKRHn', 'bebidas', 'Bebidas', 'Bebidas', 'Coca-Cola em lata ou 2 litros.'),
]
SUBFRITAS = {'evOpDZwhC68N2FdfbhAW': 'Tradicional', 'KzSkNfDJFOpKDiCtQxcv': 'Xcb'}
# "Mais pedidos" que o próprio Brendi mostra no topo do cardápio (na ordem dele)
MAIS_PEDIDOS = ['Calotinha Especial', 'Calotinha Frango com Catupiry', 'Calotinha Frango', 'Calotinha Bacon',
                'Calotinha Frango Defumado com Cream Cheese']

grupos, gkey = {}, {}


def reg(g):
    t = re.sub(r'\s+\d+$', '', g['titulo']).strip()
    ops = [[o['nome'].strip(), round(o['preco'], 2), o.get('max') or 3] for o in g['opcoes'] if o.get('ativo', True)]
    d = {'titulo': t, 'tipo': 'qtd', 'max': g['max'] or 3, 'opcoes': ops}
    k = json.dumps(d, ensure_ascii=False, sort_keys=True)
    if k not in gkey:
        base = slug(t)[:14] or 'g'
        n, i = base, 2
        while n in grupos:
            n = f'{base}{i}'
            i += 1
        gkey[k] = n
        grupos[n] = d
    return gkey[k]


por_cat = {c[1]: [] for c in CATS}
ids, faltando = set(), []
for p in D['produtos']:
    cid = p['cat']
    if cid in SUBFRITAS:
        destino, sub = 'fritas', SUBFRITAS[cid]
    else:
        destino = next((c[1] for c in CATS if c[0] == cid), None)
        sub = None
    if not destino:
        continue
    nome = nome_limpo(p['nome'])
    i = slug(nome)
    if i in ids:
        continue  # o Brendi repete alguns itens em "Mais pedidos"
    ids.add(i)
    it = {'id': i, 'nome': nome, 'desc': (p['desc'] or '').strip(), 'preco': round(p['preco'], 2)}
    if p['slug'] in M:
        it['img'] = M[p['slug']]
    gs = [reg(g) for g in p['grupos'] if g['opcoes']]
    if gs:
        it['grupos'] = gs
    if sub:
        it['sub'] = sub
    if nome in MAIS_PEDIDOS:
        it['maisPedido'] = MAIS_PEDIDOS.index(nome) + 1
    if p['falta']:
        faltando.append(nome)
    por_cat[destino].append(it)

por_cat['fritas'].sort(key=lambda x: (x.get('sub') != 'Tradicional', x['preco']))
for k in ('calotas', 'calotinhas', 'combos'):
    por_cat[k].sort(key=lambda x: x['preco'])

saida = [{'id': c[1], 'nome': c[2], 'curto': c[3], 'desc': c[4], 'itens': por_cat[c[1]]} for c in CATS if por_cat[c[1]]]

wh = STORE['workingHours']
dias = {'sun': 0, 'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5, 'sat': 6}
hm = lambda m: f'{m // 60:02d}:{m % 60:02d}'
horarios_app = {str(dias[k]): [[hm(t['start']), hm(t['end'])] for t in v] for k, v in wh.items()}

LOJA = {
    'nome': 'X Calota', 'nomeCompleto': 'X Calota Taubaté', 'unidade': 'Taubaté',
    'endereco': 'Praça Santa Terezinha, 159 · Centro', 'cidade': 'Taubaté · SP', 'cep': '12010-140',
    'whatsapp': '5512997337077', 'whatsappTexto': '(12) 99733-7077',
    'instagram': 'xcalotataubate', 'instagramSeguidores': '15 mil',
    'facebook': 'X Calota Taubaté',
    'mapa': 'https://www.google.com/maps/dir//X+Calota+Taubat%C3%A9,+Pra%C3%A7a+Santa+Terezinha,+159+-+Centro,+Taubat%C3%A9+-+SP,+12010-140',
    'mapaEmbed': 'https://www.google.com/maps?q=X+Calota+Taubat%C3%A9,+Pra%C3%A7a+Santa+Terezinha,+159,+Taubat%C3%A9+-+SP&output=embed',
    'nota': '3,5', 'avaliacoes': '58',
    # Horário do Google Maps (o do cardápio online, diferente, fica só no REVISAR.md)
    'horarios': {'0': [['17:30', '00:00']], '1': [['17:30', '00:00']], '2': [], '3': [['17:30', '00:00']],
                 '4': [['17:30', '00:00']], '5': [['17:30', '00:00']], '6': [['17:30', '00:00']]},
    'entrega': {'tempo': '1h a 1h10', 'retirada': '20 a 40 min', 'raioKm': 12,
                'faixas': [[r['minDistance'] / 1000, r['maxDistance'] / 1000, r['price'] / 100] for r in STORE['delivery']]},
    'pagamentos': ['Pix', 'Dinheiro', 'Cartão de crédito', 'Cartão de débito'],
    'pagamentoNota': 'Cartões Visa, Mastercard e Elo.',
    'frases': {
        'facebook': 'X Calota 28 cm para compartilhar, Calotinha somente para você. Sabor e união definem a gente!',
        'instagram': 'Muito mais que alimentar, queremos unir as pessoas, para criar memórias e momentos felizes!',
    },
    'fotos': {'logo': 'fotos/local/logo-x-calota.webp', 'anuncio': 'fotos/local/anuncio-adeus-fome.jpg',
              'caixa': 'fotos/local/calota-na-caixa.jpg'},
    'creditos': [['fotos/local/calota-na-caixa.jpg', 'Calota na caixa', 'Chris Gemini no Google Maps'],
                 ['fotos/local/anuncio-adeus-fome.jpg', 'Anúncio "Adeus fome"', 'X Calota Taubaté no Google Maps']],
}

js = ('/* ==========================================================================\n'
      '   DADOS DO SITE · X Calota Taubaté\n'
      '   Gerado em 19/10/2026 a partir do cardápio da loja e do Google.\n'
      '   Para editar preços e adicionais, troque aqui ou rode\n'
      '   _coleta/gerar_dados.py de novo (isso sobrescreve este arquivo).\n'
      '   ========================================================================== */\n')
js += 'window.LOJA = ' + json.dumps(LOJA, ensure_ascii=False, indent=1) + ';\n\n'
js += 'window.GRUPOS = ' + json.dumps(grupos, ensure_ascii=False) + ';\n\n'
js += 'window.CATEGORIAS = ' + json.dumps(saida, ensure_ascii=False, indent=1) + ';\n'
open(OUT, 'w', encoding='utf-8').write(js)

print({c['id']: len(c['itens']) for c in saida}, 'grupos:', {k: (v['titulo'], len(v['opcoes'])) for k, v in grupos.items()})
print('mais pedidos:', [i['nome'] for c in saida for i in c['itens'] if i.get('maisPedido')])
print('em falta no app:', len(faltando))
print('nomes:', [i['nome'] for i in por_cat['calotas']][:30])
print('horario app:', horarios_app)
