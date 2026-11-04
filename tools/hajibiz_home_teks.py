"""Beranda haji.biz (page 197): perbaiki salah tulis & data tanpa mengubah desain (disetujui pemilik 2026-11-04).
- SK No.848/2020 -> 846/2020 (izin PIHK yang benar); EXCELENT -> EXCELLENT; Profile -> Profil; Trusted -> Terpercaya;
  "berpengalaman 7 berilmu" -> "& berilmu"; 6100 ulasan -> 7.000+; "hotel Nyaman" -> "Hotel Nyaman";
  "Menunda , Masa Tunggu semakin" -> "Menunda, Masa Tunggu Semakin"; "menghandel" -> "menangani".
- Kotak statistik ke-6 (hanya ikon panah) diisi "Akreditasi A" dengan gaya kolom & icon-box yang sama seperti kotak "Trusted".
Cadangan sebelum langkah ini: backup/2026-11-04_hajibiz_home/197-sebelum-teks.json. Berhenti bila ada pengedit lain sejak itu.
Kredensial env WP_HAJIBIZ_USER / WP_HAJIBIZ_PASS. Uji kering tanpa --deploy."""
import base64, copy, json, os, secrets, subprocess, sys

PAGE = 197
M = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'wordpress', 'ikon-3d', 'media-hajibiz.json')))
AUTH = 'Basic ' + base64.b64encode(f"{os.environ['WP_HAJIBIZ_USER']}:{os.environ['WP_HAJIBIZ_PASS']}".encode()).decode()


def curl(method, path, data=None):
    cmd = ['curl', '-sS', '-X', method, '-H', 'Authorization: ' + AUTH, '-H', 'User-Agent: Mozilla/5.0 eh-admin',
           '-H', 'Content-Type: application/json', '-w', '\n%{http_code}', 'https://haji.biz/wp-json' + path]
    if data is not None:
        cmd[1:1] = ['--data-binary', '@-']
    out = subprocess.run(cmd, input=json.dumps(data).encode() if data is not None else None, capture_output=True).stdout.decode()
    body, code = out.rsplit('\n', 1)
    return int(code), (json.loads(body) if body.strip().startswith(('{', '[')) else body)


def gambar_widget(slug, size, align):
    return {'id': secrets.token_hex(4)[:7], 'elType': 'widget', 'isInner': False, 'widgetType': 'image', 'elements': [],
            'settings': {'image': {'url': M[slug]['url'], 'id': M[slug]['id'], 'alt': '', 'source': 'library'},
                         'image_size': 'full', 'width': {'unit': 'px', 'size': size, 'sizes': []}, 'align': align,
                         '_css_classes': 'hb-ikon3d'}}

ROOT = os.path.join(os.path.dirname(__file__), '..')
CADANGAN = os.path.join(ROOT, 'backup', '2026-11-04_hajibiz_home', '197-sebelum-teks.json')

GANTI = [  # (id widget, kunci setting | 'icon_list', teks lama, teks baru)
    ('2b05f3f4', 'icon_list', 'No.848/2020', 'No. 846/2020'),
    ('4778c306', 'title', 'EXCELENT SERVICE', 'EXCELLENT SERVICE'),
    ('657703cf', 'title', 'Profile Elharamain Wisata', 'Profil Elharamain Wisata'),
    ('76457abb', 'title_text', 'Trusted', 'Terpercaya'),
    ('5d308226', 'description_text', 'berpengalaman 7 berilmu', 'berpengalaman &amp; berilmu'),
    ('504ddf5', 'title', 'DARI 6100 ULASAN', 'DARI 7.000+ ULASAN'),
    ('191c3dd', 'title', 'hotel Nyaman', 'Hotel Nyaman'),
    ('40a1ffe8', 'title', 'Semakin Menunda , Masa Tunggu semakin Panjang', 'Semakin Menunda, Masa Tunggu Semakin Panjang'),
    ('5d1de363', 'description_text', 'menghandel', 'menangani'),
]
CHEVRON, KOLOM_KOSONG, CONTOH_IBOX = '45d5716', '3891de59', '76457abb'

s, d = curl('GET', f'/wp/v2/pages/{PAGE}?context=edit&_fields=modified,meta')
raw = d['meta']['_elementor_data']
if not os.path.exists(CADANGAN):
    open(CADANGAN, 'w', encoding='utf-8').write(raw)
elif open(CADANGAN, encoding='utf-8').read() != raw:
    sys.exit('halaman berubah sejak cadangan sebelum-teks; ada pengedit lain, berhenti')
data = json.loads(raw)

idx, induk = {}, {}


def index(e, par=None):
    idx[e['id']] = e
    induk[e['id']] = par
    for c in e.get('elements', []):
        index(c, e)


for x in data:
    index(x)

for wid, key, lama, baru in GANTI:
    st = idx[wid]['settings']
    if key == 'icon_list':
        item = next(i for i in st['icon_list'] if lama in i.get('text', ''))
        item['text'] = item['text'].replace(lama, baru)
    else:
        if lama not in st.get(key, ''):
            sys.exit(f'{wid}.{key}: "{lama}" tidak ditemukan, berhenti')
        st[key] = st[key].replace(lama, baru)

# kotak ke-6: salin gaya kolom & icon-box "Trusted" (beserta ikon 3D di atasnya)
kol_contoh = induk[CONTOH_IBOX]
kol = idx[KOLOM_KOSONG]
if [c['id'] for c in kol['elements']] != [CHEVRON]:
    sys.exit('isi kolom ke-6 tidak sesuai dugaan, berhenti')
ukuran = {k: v for k, v in kol['settings'].items() if k.startswith('_column_size') or k.startswith('_inline_size')}
kol['settings'] = {**copy.deepcopy(kol_contoh['settings']), **ukuran}
ibox = copy.deepcopy(idx[CONTOH_IBOX])
ibox['id'] = secrets.token_hex(4)[:7]
ibox['settings']['title_text'] = 'Akreditasi A'
ibox['settings']['description_text'] = 'TERAKREDITASI A OLEH KOMITE AKREDITASI NASIONAL (KAN)'
ikon = [c for c in kol_contoh['elements'] if c.get('widgetType') == 'image' and 'hb-ikon3d' in c['settings'].get('_css_classes', '')]
gambar = copy.deepcopy(ikon[0]) if ikon else gambar_widget('akreditasi', 56, 'left')
gambar['id'] = secrets.token_hex(4)[:7]
gambar['settings']['image'] = gambar_widget('akreditasi', 56, 'left')['settings']['image']
kol['elements'] = [gambar, ibox]

print('9 teks diperbaiki + kotak "Akreditasi A"')
if '--deploy' not in sys.argv:
    print('uji kering; jalankan dengan --deploy')
    sys.exit()
s, r = curl('POST', f'/wp/v2/pages/{PAGE}', {'meta': {'_elementor_data': json.dumps(data, ensure_ascii=False)}})
print('POST', PAGE, s, '' if s == 200 else str(r)[:300])
print('hapus cache Elementor', curl('DELETE', '/elementor/v1/cache')[0])
