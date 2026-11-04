"""Beranda elharamainwisata.com (7840): bagian "Pembimbing ibadah umroh & haji" (<section id="pembimbing">) diganti
"Fasilitas Elharamain Wisata" (slider hotel & bus, label "Hotel & transportasi") yang diambil dari blok sinkron 9995
(dipakai di /paket-umroh-silver/ 8896). Permintaan eksplisit pemilik 2026-11-04.

Catatan: beranda dan halaman paket sekarang memakai blok Gutenberg `wp:html` (content), BUKAN `_elementor_data`
(_elementor_edit_mode kosong). Mengubah `_elementor_data` tidak berpengaruh ke tampilan.
Cadangan: backup/2026-11-04_beranda_fasilitas/7840-content-sebelum.html (kembalikan: POST {"content": isi file}).
Kredensial dari env WP_USER / WP_APP_PASSWORD."""
import os, re, sys
import wp_rest as w

HOME, BLOK_FASILITAS = 7840, 9995
BACKUP = os.path.join(os.path.dirname(__file__), '..', 'backup', '2026-11-04_beranda_fasilitas')

s, d = w.req('GET', f'/wp/v2/pages/{HOME}?context=edit&_fields=content')
if s != 200:
    sys.exit(f'GET {HOME} gagal: {s} {d}')
home = d['content']['raw']
s, b = w.req('GET', f'/wp/v2/blocks/{BLOK_FASILITAS}?context=edit&_fields=content')
if s != 200:
    sys.exit(f'GET blok {BLOK_FASILITAS} gagal: {s} {b}')
blok = b['content']['raw']

pola = re.compile(r'<section class="ehb-sec" id="pembimbing">.*?</section>', re.S)
if len(pola.findall(home)) != 1:
    sys.exit('bagian Pembimbing tidak ditemukan tepat 1x, berhenti')

# Bagian slider dari blok: <style> sesudah judul "Fasilitas" sampai </script> sesudah catatan .ehfs-note
m = re.search(r'<h2>Fasilitas Elharamain Wisata</h2></div>(<style>.*?</script>)', blok, re.S)
if not m or 'id="ehfs"' not in m.group(1):
    sys.exit('slider fasilitas tidak ditemukan di blok, berhenti')
if 'id="ehfs"' in home:
    sys.exit('beranda sudah punya slider ehfs, berhenti')

baru = ('<section class="ehb-sec" id="fasilitas">\n  <div class="ehc-wrap">\n'
        '    <span class="ehb-kick">Hotel &amp; transportasi</span>\n'
        '    <h2>Fasilitas Elharamain Wisata</h2>\n'
        f'    {m.group(1)}\n  </div>\n</section>')

os.makedirs(BACKUP, exist_ok=True)
with open(os.path.join(BACKUP, '7840-content-sebelum.html'), 'w', encoding='utf-8') as f:
    f.write(home)

hasil = pola.sub(lambda _: baru, home)
if '--deploy' not in sys.argv:
    print(f'uji kering: {len(home)} -> {len(hasil)} karakter; jalankan dengan --deploy')
    sys.exit()
s, r = w.req('POST', f'/wp/v2/pages/{HOME}', {'content': hasil})
print('POST beranda', s, '' if s == 200 else r)
