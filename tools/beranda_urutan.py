"""Susun ulang urutan section beranda elharamainwisata.com (7840). Semua section ada di dua blok `wp:html`
yang sama-sama dibungkus <div class="ehc ehb">, sebelum testimoni (blok sinkron 9994). Skrip ini mengambil
semua section dari kedua blok, lalu menaruhnya kembali sesuai URUTAN (blok 1 berisi BLOK1 section pertama).
Blok <style> tab di akhir blok kedua dan blok lain tidak diubah.
Urutan per permintaan pemilik 2026-11-04. Cadangan: backup/2026-11-04_beranda_fasilitas/7840-content-sebelum-urutan.html.
Kredensial dari env WP_USER / WP_APP_PASSWORD. Uji kering tanpa --deploy."""
import os, re, sys
import wp_rest as w

HOME = 7840
BACKUP = os.path.join(os.path.dirname(__file__), '..', 'backup', '2026-11-04_beranda_fasilitas')
# kunci = id section, atau kelas penanda bila section tak punya id
URUTAN = ['ehb-hero', 'ehb-up', 'legalitas', 'jadwal', 'kenapa', 'alur', 'layanan', 'kelas', 'fasilitas', 'dokumentasi']
BLOK1 = 6
WRAP = '<div class="ehc ehb">'

s, d = w.req('GET', f'/wp/v2/pages/{HOME}?context=edit&_fields=content')
if s != 200:
    sys.exit(f'GET {HOME} gagal: {s} {d}')
c = d['content']['raw']


def kunci(sec):
    head = sec[:300]
    m = re.search(r'id="([^"]+)"', head)
    if m:
        return m.group(1)
    if 'ehb-hero' in head:
        return 'ehb-hero'
    if 'ehb-up' in head:
        return 'ehb-up'
    if 'Kenapa memilih Elharamain Wisata?' in sec:
        return 'kenapa'
    sys.exit('section tak dikenal: ' + head[:120])


class Blok:
    """Satu blok wp:html berbungkus: isi = section-section, ekor = sesudah </div> penutup pembungkus."""
    def __init__(self, m):
        body = m.group(1)
        tutup = body.index('</div>', body.rindex('</section>'))
        self.isi, self.ekor = body[:tutup], body[tutup + len('</div>'):]
        self.start, self.end = m.start(), m.end()

    def group(self, i):
        return self.isi if i == 1 else self.ekor


blok = [Blok(m) for m in re.finditer(r'<!-- wp:html -->\n' + re.escape(WRAP) + r'(.*?)<!-- /wp:html -->', c, re.S)]
if len(blok) != 2:
    sys.exit(f'blok html berbungkus ditemukan {len(blok)}, harus 2; berhenti')
secs = {}
for b in blok:
    isi = b.group(1)
    found = re.findall(r'<section\b.*?</section>', isi, re.S)
    if re.sub(r'<section\b.*?</section>', '', isi, flags=re.S).strip():
        sys.exit('ada isi lain di luar section dalam pembungkus; berhenti')
    for sct in found:
        secs[kunci(sct)] = sct
if sorted(secs) != sorted(URUTAN):
    sys.exit(f'section tidak cocok: ada {sorted(secs)}')


def susun(keys):
    return '\n'.join(secs[k] for k in keys)


baru = [f'<!-- wp:html -->\n{WRAP}{susun(URUTAN[:BLOK1])}</div>{blok[0].group(2)}<!-- /wp:html -->',
        f'<!-- wp:html -->\n{WRAP}{susun(URUTAN[BLOK1:])}</div>{blok[1].group(2)}<!-- /wp:html -->']
hasil = c[:blok[0].start] + baru[0] + c[blok[0].end:blok[1].start] + baru[1] + c[blok[1].end:]

os.makedirs(BACKUP, exist_ok=True)
with open(os.path.join(BACKUP, '7840-content-sebelum-urutan.html'), 'w', encoding='utf-8') as f:
    f.write(c)
print('urutan baru:', ', '.join(URUTAN), f'| {len(c)} -> {len(hasil)} karakter')
if '--deploy' not in sys.argv:
    print('uji kering; jalankan dengan --deploy')
    sys.exit()
s, r = w.req('POST', f'/wp/v2/pages/{HOME}', {'content': hasil})
print('POST beranda', s, '' if s == 200 else r)
