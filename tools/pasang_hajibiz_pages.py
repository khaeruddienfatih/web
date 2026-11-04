"""Pasang desain baru (landing-pages/situs/haji-biz/<slug>.html, dari build_hajibiz_pages.py) ke halaman live haji.biz.
Disetujui pemilik 2026-11-04 ("nanti publish sudah oke"). Elementor dimatikan per halaman (_elementor_edit_mode=''),
template elementor_header_footer (header/footer UAE). URL, judul, SEO Rank Math tetap.
Pengaman: halaman dilewati bila `modified` berbeda dari cadangan backup/2026-11-04_hajibiz_pages/<id>-*.json (ada pengedit lain).
Kembalikan: POST content + meta (_elementor_edit_mode, _elementor_data) + template dari file cadangan, lalu DELETE /elementor/v1/cache.
Kredensial env WP_HAJIBIZ_USER / WP_HAJIBIZ_PASS. Pakai: python3 tools/pasang_hajibiz_pages.py [slug ...] --deploy"""
import glob, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_hajibiz_home import hb

ROOT = os.path.join(os.path.dirname(__file__), '..')
TARGET = {'paket-haji-plus': 113, 'haji-plus-2027': 226, 'haji-plus-2028': 742,
          'tentang-kami': 248, 'lokasi-kantor': 793, 'galeri-haji': 238}

pilih = [a for a in sys.argv[1:] if not a.startswith('--')] or list(TARGET)
for slug in pilih:
    pid = TARGET[slug]
    cad = glob.glob(os.path.join(ROOT, 'backup', '2026-11-04_hajibiz_pages', f'{pid}-*.json'))
    cad = [c for c in cad if not c.endswith('-publik.json')]
    asli = json.load(open(cad[0]))
    s, d = hb('GET', f'/wp/v2/pages/{pid}?context=edit&_fields=modified,link')
    if d['modified'] != asli['modified']:
        print(f'{slug} ({pid}): LEWATI, berubah sejak cadangan ({asli["modified"]} -> {d["modified"]})')
        continue
    konten = open(os.path.join(ROOT, 'landing-pages', 'situs', 'haji-biz', f'{slug}.html'), encoding='utf-8').read()
    if '--deploy' not in sys.argv:
        print(f'{slug} ({pid}): siap dipasang ({len(konten)} karakter) -> {d["link"]}')
        continue
    s, r = hb('POST', f'/wp/v2/pages/{pid}', {'content': konten, 'template': 'elementor_header_footer',
                                              'meta': {'_elementor_edit_mode': ''}})
    print(f'{slug} ({pid}): POST {s}', '' if s == 200 else str(r)[:200])
if '--deploy' in sys.argv:
    try:
        print('hapus cache Elementor', hb('DELETE', '/elementor/v1/cache')[0])
    except ValueError:  # respons kosong = sukses
        print('hapus cache Elementor: selesai')
