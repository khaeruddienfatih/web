"""Beranda elharamainwisata.com (7840): pindahkan <section id="dokumentasi"> ("Dokumentasi jamaah Elharamain Wisata")
ke tepat di atas testimoni (blok sinkron 9994), yaitu sesudah <section id="alur"> ("Langkah umroh").
Permintaan eksplisit pemilik 2026-11-04. Cadangan: backup/2026-11-04_beranda_fasilitas/7840-content-sebelum-dokumentasi.html.
Kredensial dari env WP_USER / WP_APP_PASSWORD. Uji kering tanpa --deploy."""
import os, re, sys
import wp_rest as w

HOME = 7840
BACKUP = os.path.join(os.path.dirname(__file__), '..', 'backup', '2026-11-04_beranda_fasilitas')

s, d = w.req('GET', f'/wp/v2/pages/{HOME}?context=edit&_fields=content')
if s != 200:
    sys.exit(f'GET {HOME} gagal: {s} {d}')
c = d['content']['raw']

dok = re.compile(r'<section class="ehb-sec" id="dokumentasi">.*?</section>\n?', re.S)
alur = re.compile(r'<section class="ehb-sec ehb-dark" id="alur">.*?</section>\n?', re.S)
if len(dok.findall(c)) != 1 or len(alur.findall(c)) != 1:
    sys.exit('section dokumentasi/alur tidak ditemukan tepat 1x, berhenti')
blok_dok = dok.search(c).group(0)
tanpa = dok.sub('', c, count=1)
m = alur.search(tanpa)
hasil = tanpa[:m.end()] + blok_dok + tanpa[m.end():]

# pastikan sesudah dokumentasi yang ada hanya penutup wp:html lalu testimoni 9994
sisa = hasil[hasil.find(blok_dok) + len(blok_dok):]
antara = sisa[:sisa.find('<!-- wp:block {"ref":9994} /-->')]
if '<!-- wp:block {"ref":9994} /-->' not in sisa or '<section' in antara or '<h2' in antara:
    sys.exit('posisi hasil bukan tepat di atas testimoni 9994, berhenti:\n' + sisa[:200])

os.makedirs(BACKUP, exist_ok=True)
with open(os.path.join(BACKUP, '7840-content-sebelum-dokumentasi.html'), 'w', encoding='utf-8') as f:
    f.write(c)
if '--deploy' not in sys.argv:
    print(f'uji kering OK: {len(c)} -> {len(hasil)} karakter; jalankan dengan --deploy')
    sys.exit()
s, r = w.req('POST', f'/wp/v2/pages/{HOME}', {'content': hasil})
print('POST beranda', s, '' if s == 200 else r)
