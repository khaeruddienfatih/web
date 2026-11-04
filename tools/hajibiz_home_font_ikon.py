"""Beranda haji.biz (page 197, Elementor): desain asli DIPERTAHANKAN (keputusan pemilik 2026-11-04), hanya:
1) font: judul Martel, teks Mulish, tombol Montserrat (widget HTML <style> di awal halaman, scope .elementor-197);
2) ikon 3D orisinal (Media haji.biz, wordpress/ikon-3d/media-hajibiz.json):
   - ganti gambar ikon datar (Kenapa berhaji, Pelayanan Premium) -> ikon 3D;
   - ganti ikon FontAwesome (strip DP/Voucher, Bimbingan) -> ikon 3D lewat CSS per elemen;
   - tambah ikon di kotak statistik Profil dan medali di kartu paket (widget image baru).
Cadangan asli: backup/2026-11-04_hajibiz_home/197-asli.json (kembalikan: POST meta._elementor_data dari file itu,
lalu DELETE /elementor/v1/cache). Berhenti bila halaman berubah sejak cadangan (ada pengedit lain).
Kredensial env WP_HAJIBIZ_USER / WP_HAJIBIZ_PASS. Uji kering tanpa --deploy."""
import base64, json, os, secrets, subprocess, sys

ROOT = os.path.join(os.path.dirname(__file__), '..')
PAGE = 197
CADANGAN = os.path.join(ROOT, 'backup', '2026-11-04_hajibiz_home', '197-asli.json')
M = json.load(open(os.path.join(ROOT, 'wordpress', 'ikon-3d', 'media-hajibiz.json')))
AUTH = 'Basic ' + base64.b64encode(f"{os.environ['WP_HAJIBIZ_USER']}:{os.environ['WP_HAJIBIZ_PASS']}".encode()).decode()

GANTI_GAMBAR = {  # id widget image / image-box -> slug ikon
    '5bd90196': 'izin-resmi', '255f454b': 'satu-rekening', '2d3348a3': 'pendaftar-haji', '2f8871ca': 'asatidz',
    '5ab1a3eb': 'hotel-bintang', '41191fd5': 'sajadah', '5704d60c': 'rating', '5d1de363': 'tim-solid'}
GANTI_FA = {'179ac932': 'booking-dp', '2d533569': 'booking-seat', '5d308226': 'asatidz', '2c76672b': 'beribadah',
            '33e09e81': 'kajian'}
TAMBAH_SEBELUM = {  # sisipkan widget image ikon tepat sebelum widget ini
    '25ad9934': ('jamaah-umroh', 56), '124a66d0': ('pendaftar-haji', 56), '6f0c07f1': ('kantor-cabang', 56),
    '2c898942': ('berpengalaman', 56), '76457abb': ('reputasi', 56),
    '5e76701b': ('medali-silver', 60), '375444e': ('medali-gold', 60), '8f69929': ('medali-arbain', 60), '15ee4ab1': ('medali-platinum', 60)}

FONT = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Martel:wght@400;700;800&family=Montserrat:wght@500;600;700&'
        'family=Mulish:wght@400;600;700&display=swap" rel="stylesheet">')
P = '.elementor-197'
CSS = ['<style id="hb-font-ikon">',
       f'{P} h1,{P} h2,{P} h3,{P} h4,{P} .elementor-heading-title,{P} .elementor-icon-box-title,{P} .elementor-image-box-title'
       '{font-family:Martel,Georgia,serif!important;letter-spacing:0!important}',
       f'{P} .elementor-heading-title{{line-height:1.3!important}}',
       f'{P} p,{P} li,{P} .elementor-widget-text-editor,{P} .elementor-icon-box-description,{P} .elementor-image-box-description,'
       f'{P} .elementor-icon-list-text{{font-family:Mulish,sans-serif!important}}',
       f'{P} .elementor-button,{P} .elementor-button-text{{font-family:Montserrat,sans-serif!important}}',
       f'{P} .hb-ikon3d img{{filter:drop-shadow(0 6px 10px rgba(6,42,102,.18))}}',
       # widget 'judul' yang isinya paragraf panjang (hero, Program Cicilan) tetap Mulish agar mudah dibaca
       f'{P} .elementor-element-1792a9cc .elementor-heading-title,{P} .elementor-element-9659917 .elementor-heading-title'
       '{font-family:Mulish,sans-serif!important;line-height:1.6!important}']
for wid, slug in GANTI_FA.items():
    e = f'{P} .elementor-element-{wid} .elementor-icon'
    CSS.append(f'{e}{{width:60px!important;height:60px!important;padding:0!important;border-radius:16px!important;'
               f'background:url({M[slug]["url"]}) center/82% no-repeat,#eef4ff!important;box-shadow:0 6px 14px rgba(6,42,102,.15)}}')
    CSS.append(f'{e} i,{e} svg{{opacity:0!important}}')
CSS.append('</style>')
HTML_WIDGET = {'id': secrets.token_hex(4)[:7], 'elType': 'widget', 'isInner': False, 'widgetType': 'html',
               'settings': {'html': FONT + '\n' + '\n'.join(CSS)}, 'elements': []}


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
                         '_margin': {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '6', 'left': '0', 'isLinked': False},
                         '_css_classes': 'hb-ikon3d'}}


def perbarui_css():
    """Tulis ulang isi widget HTML hb-font-ikon (setelah terpasang) dengan CSS terbaru di skrip ini."""
    s, d = curl('GET', f'/wp/v2/pages/{PAGE}?context=edit&_fields=modified,meta')
    data = json.loads(d['meta']['_elementor_data'])
    n = [0]
    def jalan(e):
        if e.get('widgetType') == 'html' and 'hb-font-ikon' in e.get('settings', {}).get('html', ''):
            e['settings']['html'] = FONT + '\n' + '\n'.join(CSS); n[0] += 1
        for c in e.get('elements', []): jalan(c)
    for x in data: jalan(x)
    if n[0] != 1:
        sys.exit(f'widget hb-font-ikon ditemukan {n[0]}x, berhenti')
    s, r = curl('POST', f'/wp/v2/pages/{PAGE}', {'meta': {'_elementor_data': json.dumps(data, ensure_ascii=False)}})
    print('perbarui CSS', s); print('hapus cache', curl('DELETE', '/elementor/v1/cache')[0])


if '--css' in sys.argv:  # sesudah terpasang: hanya perbarui isi widget CSS/font
    perbarui_css()
    sys.exit()
s, d = curl('GET', f'/wp/v2/pages/{PAGE}?context=edit&_fields=modified,meta')
asli = json.load(open(CADANGAN))
if s != 200 or d['modified'] != asli['modified'] or d['meta']['_elementor_data'] != asli['meta']['_elementor_data']:
    sys.exit(f'halaman berubah sejak cadangan ({d.get("modified") if isinstance(d, dict) else s}); ada pengedit lain, berhenti')
data = json.loads(d['meta']['_elementor_data'])
if 'hb-font-ikon' in d['meta']['_elementor_data']:
    sys.exit('sudah terpasang, berhenti')

hit = {'gambar': 0, 'tambah': 0}


def proses(e):
    st = e.get('settings', {})
    if e.get('id') in GANTI_GAMBAR:
        slug = GANTI_GAMBAR[e['id']]
        st['image'] = {'url': M[slug]['url'], 'id': M[slug]['id'], 'alt': '', 'source': 'library'}
        st['_css_classes'] = (st.get('_css_classes', '') + ' hb-ikon3d').strip()
        hit['gambar'] += 1
    anak = []
    for c in e.get('elements', []):
        if c.get('id') in TAMBAH_SEBELUM:
            slug, size = TAMBAH_SEBELUM[c['id']]
            align = c.get('settings', {}).get('text_align') or 'left'
            anak.append(gambar_widget(slug, size, align if align in ('left', 'center', 'right') else 'left'))
            hit['tambah'] += 1
        anak.append(c)
        proses(c)
    if 'elements' in e:
        e['elements'] = anak


for sec in data:
    proses(sec)
fa_ada = sum(json.dumps(data).count(f'"id": "{w}"') for w in GANTI_FA)
if hit['gambar'] != len(GANTI_GAMBAR) or hit['tambah'] != len(TAMBAH_SEBELUM) or fa_ada != len(GANTI_FA):
    sys.exit(f'jumlah tidak cocok: {hit}, fa={fa_ada}; berhenti')

# widget HTML font/CSS di kolom pertama section pertama
kol = data[0]['elements'][0]
kol['elements'].insert(0, HTML_WIDGET)
print(f'ganti gambar {hit["gambar"]}, tambah ikon {hit["tambah"]}, ganti FA {fa_ada}, + widget font')
if '--deploy' not in sys.argv:
    print('uji kering; jalankan dengan --deploy')
    sys.exit()
s, r = curl('POST', f'/wp/v2/pages/{PAGE}', {'meta': {'_elementor_data': json.dumps(data, ensure_ascii=False)}})
print('POST', PAGE, s, '' if s == 200 else str(r)[:300])
s, r = curl('DELETE', '/elementor/v1/cache')
print('hapus cache Elementor', s)

