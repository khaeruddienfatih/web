"""Pasang desain baru Haji Plus (landing-pages/situs/elharamainwisata-com/haji-plus.html, dibangun build_haji_plus.py)
ke halaman live 8289 /paket-haji-plus-elharamain-wisata/. Elementor dimatikan untuk halaman ini (_elementor_edit_mode='')
agar `content` yang dirender; `_elementor_data` lama dibiarkan (tidak dipakai). URL, judul, dan SEO Rank Math tetap.
Disetujui pemilik 2026-11-04 ("ok sudah bagus"). Cadangan: backup/2026-11-04_haji_plus/8289-sebelum.json.
Kembalikan: POST content lama + meta {"_elementor_edit_mode": "builder"} dari file cadangan, lalu DELETE /elementor/v1/cache."""
import os, sys, urllib.request
import wp_rest as w

ROOT = os.path.join(os.path.dirname(__file__), '..')
PAGE = 8289
if not os.path.exists(os.path.join(ROOT, 'backup', '2026-11-04_haji_plus', '8289-sebelum.json')):
    sys.exit('cadangan belum ada, berhenti')
konten = open(os.path.join(ROOT, 'landing-pages', 'situs', 'elharamainwisata-com', 'haji-plus.html'), encoding='utf-8').read()
s, r = w.req('POST', f'/wp/v2/pages/{PAGE}', {'content': konten, 'template': 'elementor_header_footer',
                                              'meta': {'_elementor_edit_mode': ''}})
print('POST', PAGE, s, '' if s == 200 else r)
if s != 200:
    sys.exit(1)
s, d = w.req('GET', f'/wp/v2/pages/{PAGE}?context=edit&_fields=meta._elementor_edit_mode,status,link')
print('cek:', d)
rq = urllib.request.Request(w.BASE + '/elementor/v1/cache', method='DELETE',
                            headers={'Authorization': w.AUTH, 'User-Agent': 'Mozilla/5.0 eh-admin'})
print('hapus cache Elementor', urllib.request.urlopen(rq, timeout=120).status)
