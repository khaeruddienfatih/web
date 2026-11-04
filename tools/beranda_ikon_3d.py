"""Beranda elharamainwisata.com (7840): ganti 20 ikon garis (.ehb-ic <svg>) dengan ikon 3D orisinal (Media WP, lihat
wordpress/ikon-3d/media.json, dibuat tools/ikon_3d.py), rapikan kartu "Kenapa memilih" (rata tengah + garis emas),
dan tambah kartu logo Kemenag/HIMPUH/IATA di Legalitas (logo sudah ada di Media WP 2024/05).
CSS ditaruh di <style id="eh-ikon3d"> pada blok wp:html terakhir. Permintaan pemilik 2026-11-04.
Cadangan: backup/2026-11-04_beranda_fasilitas/7840-content-sebelum-ikon.html. Uji kering tanpa --deploy."""
import json, os, re, sys
import wp_rest as w
from ikon_3d import KARTU, IKON

HOME = 7840
ROOT = os.path.join(os.path.dirname(__file__), '..')
BACKUP = os.path.join(ROOT, 'backup', '2026-11-04_beranda_fasilitas')
MEDIA = json.load(open(os.path.join(ROOT, 'wordpress', 'ikon-3d', 'media.json')))
UP = 'https://elharamainwisata.com/wp-content/uploads/2024/05/'

CSS = '''<style id="eh-ikon3d">
.ehb .ehb-ic.ehb-ic3d{width:76px;height:76px;border-radius:22px;background:#eef4ff;margin-bottom:16px}
.ehb .ehb-dark .ehb-ic.ehb-ic3d{background:rgba(255,255,255,.14)}
.ehb .ehb-ic3d img{width:64px;height:64px;display:block}
.ehb #kenapa .ehb-card{align-items:center;text-align:center;padding:30px 24px 26px;box-shadow:0 12px 30px rgba(16,33,61,.07);transition:transform .2s,box-shadow .2s}
.ehb #kenapa .ehb-card:hover{transform:translateY(-4px);box-shadow:0 18px 36px rgba(0,74,173,.14)}
.ehb #kenapa .ehc-wrap>.ehb-kick,.ehb #kenapa .ehc-wrap>h2{text-align:center}
.ehb #kenapa .ehc-wrap>h2::after{content:"";display:block;width:64px;height:4px;border-radius:4px;background:#DBC033;margin:14px auto 30px}
.ehb .ehb-logos{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:26px 0 22px}
.ehb .ehb-logos figure{margin:0;display:flex;align-items:center;gap:16px;background:#fff;border:1px solid var(--ln);border-radius:16px;padding:16px 20px;box-shadow:0 10px 26px rgba(16,33,61,.06)}
.ehb .ehb-logos img{height:64px;width:auto;flex:none}
.ehb .ehb-logos b{display:block;font:700 16px Poppins,sans-serif;color:var(--nv)}
.ehb .ehb-logos small{display:block;font-size:13px;color:var(--mu);margin-top:2px}
@media(max-width:760px){.ehb .ehb-logos{grid-template-columns:1fr;gap:10px}.ehb .ehb-logos img{height:52px}.ehb .ehb-ic.ehb-ic3d{width:68px;height:68px}.ehb .ehb-ic3d img{width:56px;height:56px}}
</style>'''

LOGOS = f'''<div class="ehb-logos">
      <figure><img loading="lazy" src="{UP}logo-kemenag.png" alt="Logo Kementerian Agama RI" width="150" height="165"><figcaption><b>Kemenag RI</b><small>PPIU 63/2020 · PIHK 846/2020</small></figcaption></figure>
      <figure><img loading="lazy" src="{UP}logo-himpuh.png" alt="Logo HIMPUH" width="154" height="165"><figcaption><b>HIMPUH</b><small>Anggota No. 131/2017</small></figcaption></figure>
      <figure><img loading="lazy" src="{UP}logo-iata.png" alt="Logo IATA" width="200" height="165"><figcaption><b>IATA</b><small>Kode 15333220</small></figcaption></figure>
    </div>
'''

s, d = w.req('GET', f'/wp/v2/pages/{HOME}?context=edit&_fields=content')
if s != 200:
    sys.exit(f'GET {HOME} gagal: {s} {d}')
c = d['content']['raw']
if 'eh-ikon3d' in c:
    sys.exit('ikon 3D sudah terpasang, berhenti')

dipakai = []


def ganti(m):
    judul = m.group(3)
    slug = KARTU.get(judul)
    if not slug:
        sys.exit(f'judul kartu tak dikenal: {judul!r}')
    dipakai.append(slug)
    img = (f'<span class="ehb-ic ehb-ic3d"><img src="{MEDIA[slug]["url"]}" alt="" width="64" height="64" '
           f'loading="lazy" decoding="async"></span>')
    return img + m.group(2) + f'<h3>{judul}</h3>'


hasil = re.sub(r'<span class="ehb-ic">(<svg.*?</svg>)</span>(\s*(?:<[^>]*>\s*)*?)<h3>([^<]*)</h3>', ganti, c, flags=re.S)
if len(dipakai) != len(KARTU) or 'class="ehb-ic"><svg' in hasil:
    sys.exit(f'ikon terganti {len(dipakai)} dari {len(KARTU)}, berhenti')

lead = 'yang terdaftar di Kementerian Agama RI.</p>\n'
if hasil.count(lead) != 1:
    sys.exit('kalimat pembuka Legalitas tidak ditemukan tepat 1x, berhenti')
hasil = hasil.replace(lead, lead + '    ' + LOGOS, 1)

akhir = hasil.rindex('<!-- /wp:html -->')
hasil = hasil[:akhir] + CSS + '\n' + hasil[akhir:]

os.makedirs(BACKUP, exist_ok=True)
with open(os.path.join(BACKUP, '7840-content-sebelum-ikon.html'), 'w', encoding='utf-8') as f:
    f.write(c)
print(f'{len(dipakai)} ikon diganti, logo + CSS ditambah | {len(c)} -> {len(hasil)} karakter')
if '--deploy' not in sys.argv:
    print('uji kering; jalankan dengan --deploy')
    sys.exit()
s, r = w.req('POST', f'/wp/v2/pages/{HOME}', {'content': hasil})
print('POST beranda', s, '' if s == 200 else r)
