"""Pasang desain baru hajifuroda.co.id (landing-pages/situs/hajifuroda/<halaman>.html dari build_hajifuroda.py) ke halaman live.
Disetujui pemilik 2026-11-04 ("langsung publish saja"). URL/slug, judul, dan SEO Rank Math halaman lama tetap; Elementor dimatikan
per halaman (_elementor_edit_mode='') dan layout Astra lebar penuh + header transparan.
Pengaman: dilewati bila `modified` berbeda dari cadangan DAN isinya bukan desain kita (hfx/hx) backup/2026-11-04_hajifuroda/<id>-*.json.
Kembalikan: POST content/excerpt/template/meta dari file cadangan. Kredensial env WP_HAJIFURODA_USER / WP_HAJIFURODA_PASS.
Pakai: python3 tools/pasang_hajifuroda.py [halaman ...] --deploy"""
import glob, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_hajifuroda import hf, META
from build_hajifuroda_v2 import HALAMAN, set_seo  # v2 = desain profesional

ROOT = os.path.join(os.path.dirname(__file__), '..')
TARGET = {'beranda': 27820, 'profil': 25978, 'layanan': 25981, 'kontak': 25844}

pilih = [a for a in sys.argv[1:] if not a.startswith('--')] or list(TARGET)
for slug in pilih:
    pid = TARGET[slug]
    cad = [c for c in glob.glob(os.path.join(ROOT, 'backup', '2026-11-04_hajifuroda', f'{pid}-*.json'))]
    asli = json.load(open(cad[0]))
    s, d = hf('GET', f'/wp/v2/pages/{pid}?context=edit&_fields=modified,link,content')
    milik_kita = isinstance(d, dict) and ('class="hfx"' in d['content']['raw'] or 'class="hx"' in d['content']['raw'])
    if not isinstance(d, dict) or (d.get('modified') != asli['modified'] and not milik_kita):
        print(f'{slug} ({pid}): LEWATI, berubah sejak cadangan ({asli["modified"]} -> {d.get("modified") if isinstance(d, dict) else s})')
        continue
    konten = open(os.path.join(ROOT, 'landing-pages', 'situs', 'hajifuroda', f'{slug}.html'), encoding='utf-8').read()
    if '--deploy' not in sys.argv:
        print(f'{slug} ({pid}): siap -> {d["link"]}')
        continue
    s, r = hf('POST', f'/wp/v2/pages/{pid}', {'content': konten, 'excerpt': HALAMAN[slug][2], 'template': '',
                                              'meta': {**META, '_elementor_edit_mode': ''}})
    print(f'{slug} ({pid}): POST {s}', '' if s == 200 else str(r)[:200])
    s2, r2 = set_seo(pid, slug)
    print(f'   SEO judul/deskripsi AIOSEO: {s2}', '' if s2 == 200 else str(r2)[:200])
if '--deploy' in sys.argv:
    print('hapus cache Elementor', hf('DELETE', '/elementor/v1/cache')[0])
