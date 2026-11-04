"""Beranda elharamainwisata.com (7840): perbarui jumlah ulasan Google di statistik hero (6.800+ -> 7.000+).
Info pemilik 2026-11-04: "sekarang sudah 7000+ google review". Cadangan: backup/2026-11-04_beranda_fasilitas/7840-content-sebelum-ulasan.html."""
import os, sys
import wp_rest as w
LAMA, BARU = '<b>6.800+</b><span>ulasan Google bintang 5</span>', '<b>7.000+</b><span>ulasan Google bintang 5</span>'
s, d = w.req('GET', '/wp/v2/pages/7840?context=edit&_fields=content')
c = d['content']['raw']
if c.count(LAMA) != 1:
    sys.exit(f'teks lama ditemukan {c.count(LAMA)}x, berhenti')
bk = os.path.join(os.path.dirname(__file__), '..', 'backup', '2026-11-04_beranda_fasilitas', '7840-content-sebelum-ulasan.html')
open(bk, 'w', encoding='utf-8').write(c)
s, r = w.req('POST', '/wp/v2/pages/7840', {'content': c.replace(LAMA, BARU)})
print('POST beranda', s)
