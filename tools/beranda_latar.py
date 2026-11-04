"""Beranda elharamainwisata.com (7840): rapikan selang-seling latar section setelah urutan disusun ulang.
Jadwal, Kenapa memilih, Langkah umroh sempat bertiga biru tua (ehb-dark); Program, Kelas, Fasilitas bertiga biru muda.
Ubah: "Kenapa memilih" ehb-dark -> putih; "Kelas paket" ehb-soft -> putih.
(#fasilitas dan testimoni #ulasan dipaksa biru muda oleh CSS blok 9991/9994, jadi tidak diubah di sini.)
Permintaan pemilik 2026-11-04. Cadangan: backup/2026-11-04_beranda_fasilitas/7840-content-sebelum-latar.html.
Kredensial dari env WP_USER / WP_APP_PASSWORD. Uji kering tanpa --deploy."""
import os, sys
import wp_rest as w

HOME = 7840
BACKUP = os.path.join(os.path.dirname(__file__), '..', 'backup', '2026-11-04_beranda_fasilitas')
GANTI = [
    ('<section class="ehb-sec ehb-dark">\n  <div class="ehc-wrap">\n    <span class="ehb-kick">Kenapa Elharamain Wisata</span>',
     '<section class="ehb-sec" id="kenapa">\n  <div class="ehc-wrap">\n    <span class="ehb-kick">Kenapa Elharamain Wisata</span>'),
    ('<section class="ehb-sec ehb-soft" id="kelas">', '<section class="ehb-sec" id="kelas">'),
]

s, d = w.req('GET', f'/wp/v2/pages/{HOME}?context=edit&_fields=content')
if s != 200:
    sys.exit(f'GET {HOME} gagal: {s} {d}')
c = d['content']['raw']
hasil = c
for lama, baru in GANTI:
    if hasil.count(lama) != 1:
        sys.exit(f'pola tidak ditemukan tepat 1x: {lama[:60]!r}')
    hasil = hasil.replace(lama, baru)

os.makedirs(BACKUP, exist_ok=True)
with open(os.path.join(BACKUP, '7840-content-sebelum-latar.html'), 'w', encoding='utf-8') as f:
    f.write(c)
if '--deploy' not in sys.argv:
    print('uji kering OK; jalankan dengan --deploy')
    sys.exit()
s, r = w.req('POST', f'/wp/v2/pages/{HOME}', {'content': hasil})
print('POST beranda', s, '' if s == 200 else r)
