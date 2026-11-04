"""hajifuroda.co.id halaman Blog (25794, Elementor): tombol "Selengkapnya" kuning #FFBC28 -> biru #004AAD, teks putih
(aturan pemilik: tanpa kuning/emas di situs ini). Desain lain tidak diubah. Cadangan: backup/2026-11-04_hajifuroda/25794-blog.json."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_hajifuroda import hf

ROOT = os.path.join(os.path.dirname(__file__), '..')
asli = json.load(open(os.path.join(ROOT, 'backup', '2026-11-04_hajifuroda', '25794-blog.json')))
s, d = hf('GET', '/wp/v2/pages/25794?context=edit&_fields=modified,meta')
if d['modified'] != asli['modified']:
    sys.exit('halaman Blog berubah sejak cadangan, berhenti')
data = json.loads(d['meta']['_elementor_data'])
n = 0


def jalan(e):
    global n
    st = e.get('settings', {})
    if st.get('classic_cta_background_color', '').upper() == '#FFBC28':
        st['classic_cta_background_color'] = '#004AAD'
        st['classic_cta_color'] = '#FFFFFF'
        n += 1
    for c in e.get('elements', []):
        jalan(c)


for x in data:
    jalan(x)
if n != 1:
    sys.exit(f'ditemukan {n} pengaturan, berhenti')
print('POST', hf('POST', '/wp/v2/pages/25794', {'meta': {'_elementor_data': json.dumps(data, ensure_ascii=False)}})[0])
print('hapus cache Elementor', hf('DELETE', '/elementor/v1/cache')[0])
