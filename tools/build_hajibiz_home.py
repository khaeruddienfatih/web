"""Desain ulang beranda haji.biz (live: page 197 "Haji Plus", Elementor) dengan gaya baru (.ehc/.ehb, ikon 3D orisinal,
font Martel/Mulish/Montserrat seperti halaman Haji Plus elharamainwisata.com). Teks ditulis ulang khusus haji.biz
(hindari konten ganda), data paket dari Brosur 1448 H haji.biz (page 226), foto dari Media haji.biz.
Permintaan pemilik 2026-11-04. Dibuat sebagai DRAFT halaman baru; page 197 tidak disentuh (ada yang sedang mengeditnya).
Cadangan asli 197: backup/2026-11-04_hajibiz_home/.

  python3 tools/build_hajibiz_home.py           -> tulis landing-pages/situs/haji-biz/beranda.html
  python3 tools/build_hajibiz_home.py --draft   -> + buat/perbarui Draft di haji.biz (ID di beranda.draft-id)
Kredensial: env WP_HAJIBIZ_USER / WP_HAJIBIZ_PASS."""
import base64, json, os, re, subprocess, sys

ROOT = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(ROOT, 'landing-pages', 'situs', 'haji-biz', 'beranda.html')
DRAFT_ID = os.path.join(ROOT, 'landing-pages', 'situs', 'haji-biz', 'beranda.draft-id')
MEDIA = json.load(open(os.path.join(ROOT, 'wordpress', 'ikon-3d', 'media-hajibiz.json')))
sys.path.insert(0, os.path.dirname(__file__))
from build_haji_plus import CSS_HAJI, FONTS  # gaya .ehj (font Martel dll.) dipakai ulang

U = 'https://haji.biz/wp-content/uploads/'
CTA = 'https://umroh.elharamainwisata.com/hajiplus/'          # tombol Konsultasi/Download Brosur di 197
DETAIL = 'https://haji.biz/paket-haji-plus-2027-elharamain-wisata/'
WA = ('https://api.whatsapp.com/send?phone=6281287292422&text=Assalamu%27alaikum%20Elharamain%20Wisata%2C%20'
      'saya%20ingin%20konsultasi%20haji%20plus.')


def ik(slug):
    return (f'<span class="ehb-ic ehb-ic3d"><img src="{MEDIA[slug]["url"]}" alt="" width="64" height="64" '
            f'loading="lazy" decoding="async"></span>')


def card(slug, judul, teks):
    return f'<div class="ehb-card">{ik(slug)}<h3>{judul}</h3><p>{teks}</p></div>'


def btn(teks, kelas='pri', href=CTA, baru=True):
    t = ' target="_blank" rel="noopener"' if baru else ''
    return f'<a class="ehb-btn {kelas}" href="{href}"{t}>{teks}</a>'


# ---------- paket 1448 H (Brosur haji.biz page 226) ----------
PAKET = [
    dict(nama='Silver', medali='medali-silver', kelas='p1', foto='2026/01/7-5.webp', hari='22–23 hari',
         makkah='Anjum / setaraf ★5 · ±350 m', madinah='Concorde / setaraf ★4 · ±200 m', jamarat='±1.000 m', maktab='Tenda VIP · Maktab 116',
         transit='Hotel Orvana', harga=('12.000', '13.500', '15.000')),
    dict(nama='Gold', medali='medali-gold', kelas='p2', foto='2026/01/5-12.webp', hari='22–23 hari',
         makkah='Marwa Rotana / setaraf ★5 · depan Masjidil Haram', madinah='Al-Aqeeq / setaraf ★5 · ±50 m', jamarat='±500 m',
         maktab='Tenda VIP · Maktab 113', transit='Hotel Orvana', harga=('15.500', '17.000', '18.500')),
    dict(nama='Gold Arbain', medali='medali-arbain', kelas='p3', foto='2026/01/6-5.webp', hari='27–28 hari',
         makkah='Marwa Rotana / setaraf ★5 · depan Masjidil Haram', madinah='Al-Aqeeq / setaraf ★5 · ±50 m', jamarat='±500 m',
         maktab='Tenda VIP · Maktab 113', transit='Hotel Orvana', harga=('17.000', '18.500', '20.000')),
    dict(nama='Platinum', medali='medali-platinum', kelas='p4', foto='2026/01/4-16.webp', hari='22–23 hari',
         makkah='Fairmont Royal Clock ★5 · depan Masjidil Haram', madinah='Movenpick / setaraf ★5 · ±50 m', jamarat='±300 m',
         maktab='Tenda VIP · Maktab 111/112', transit='Roots Hotel', harga=('20.000', '22.000', '24.000')),
]


def paket_html(p):
    baris = [('Lama perjalanan', p['hari']), ('Hotel Makkah', p['makkah']), ('Hotel Madinah', p['madinah']),
             ('Maskapai', 'Saudia / Qatar / Emirates'), ('Armina', p['maktab']), ('Jarak ke Jamarat', p['jamarat']),
             ('Transportasi', 'Bus &amp; kereta cepat Haramain'), ('Hotel transit', p['transit'])]
    rows = ''.join(f'<li><span>{k}</span><b>{v}</b></li>' for k, v in baris)
    h4, h3, h2 = p['harga']
    return (f'<div class="ehj-pk {p["kelas"]}"><div class="ehj-pkh hb-pkh"><img class="foto" src="{U}{p["foto"]}" alt="" loading="lazy">'
            f'<img src="{MEDIA[p["medali"]]["url"]}" alt="Medali paket {p["nama"]}" width="72" height="72" loading="lazy">'
            f'<h3>Paket {p["nama"]}</h3><span class="th">Haji Plus 1448 H</span></div>'
            f'<div class="ehj-pkb"><div class="hb-hrg"><div><small>sekamar 4</small><b>{h4}</b></div>'
            f'<div><small>sekamar 3</small><b>{h3}</b></div><div><small>sekamar 2</small><b>{h2}</b></div></div>'
            f'<small class="hb-usd">harga dalam USD per jamaah</small><ul>{rows}</ul>'
            f'{btn("Lihat detail paket", "pri", DETAIL, baru=False)}</div></div>')


ULASAN = [f'{U}2026/01/{n}.jpg' for n in ('22', '14-1', '21', '20', '19', '18', '17', '16-1', '15-1')]

SEKSI = f'''
<section class="ehb-hero hb-hero">
  <div class="ehc-wrap ehb-hero-in">
    <div class="ehb-hero-tx">
      <span class="ehb-pill">PIHK resmi · SK Kemenag No. 846/2020 · Akreditasi A</span>
      <h1>Berangkat haji lebih pasti bersama <em>Elharamain Wisata</em></h1>
      <p>Elharamain Wisata adalah Penyelenggara Ibadah Haji Khusus (PIHK) yang terdaftar dan diawasi langsung oleh Kementerian Haji dan Umrah RI. Daftar sekarang, karena semakin menunda, masa tunggu semakin panjang.</p>
      <div class="ehc-ctas">{btn('<i class="ehb-wa"></i> Konsultasi Gratis', 'wa')}<a class="ehb-btn glass" href="#paket">Lihat paket &amp; harga</a></div>
    </div>
    <div class="ehb-next">
      <small>Haji Plus 1448 H</small>
      <b>Setoran awal 4.000 USD</b>
      <span>Langsung ke Kementerian, porsi atas nama Anda</span>
      <p>paket mulai <strong>12.000 USD</strong></p>
      <span>Paket Silver · sekamar 4 orang</span>
      {btn('Tanya paket haji plus →', 'wa', WA)}
    </div>
  </div>
  <div class="ehc-wrap"><div class="ehb-stat">
    <div><b>8–10 tahun</b><span>estimasi masa tunggu Haji Plus</span></div>
    <div><b>1.400+</b><span>pendaftar haji dalam 1 tahun</span></div>
    <div><b>7.000+</b><span>ulasan Google bintang 5</span></div>
    <div><b>6 kantor</b><span>Jabodetabek &amp; Bandung</span></div>
  </div></div>
</section>
<section class="ehb-sec ehb-pt0 ehb-up">
  <div class="ehc-wrap"><div class="ehb-g4">
    {card('booking-dp', 'DP paling ringan', 'Cukup 4.000 USD untuk nomor porsi, saat travel lain bisa 5.000 USD ke atas.')}
    {card('pendaftar-haji', 'Porsi resmi SISKOHAT', 'Setiap jamaah tercatat dengan nomor porsi resmi di sistem SISKOHAT.')}
    {card('booking-seat', 'Bonus voucher umroh', 'Voucher umroh senilai Rp 5 juta untuk dipakai selama masa tunggu.')}
    {card('cicilan-ringan', 'Bisa dicicil', 'Program cicilan untuk mendapatkan nomor antrean haji khusus lebih cepat.')}
  </div></div>
</section>
<section class="ehb-sec" id="kenapa">
  <div class="ehc-wrap">
    <span class="ehb-kick">Alasan memilih kami</span>
    <h2>Kenapa berhaji dengan Elharamain Wisata?</h2>
    <div class="ehb-g3">
      {card('izin-resmi', 'PIHK resmi berizin', 'Terdaftar dan berizin resmi, sehingga seluruh proses haji sesuai regulasi dan masuk sistem SISKOHAT.')}
      {card('satu-rekening', 'Porsi resmi &amp; aman', 'Setoran awal 4.000 USD masuk langsung ke Kementerian, bukan ke travel. Porsi atas nama jamaah sendiri.')}
      {card('konsultasi', 'Daftar mudah &amp; cepat', 'Administrasi dibantu penuh oleh tim Elharamain. Nomor porsi terbit sekitar 8 hari kerja.')}
      {card('asatidz', 'Bimbingan terstruktur', 'Manasik lengkap di hotel, online, dan camp, ditambah pembekalan sebelum dan selama di Tanah Suci.')}
      {card('hotel-bintang', 'Fasilitas berkualitas', 'Hotel strategis, maktab VIP, dan transportasi nyaman agar jamaah fokus beribadah dengan khusyuk.')}
      {card('rating', 'Dipercaya ribuan jamaah', '8.500+ jamaah umroh setahun dan 7.000+ ulasan Google bintang 5.')}
    </div>
  </div>
</section>
<section class="ehb-sec ehb-soft" id="paket">
  <div class="ehc-wrap">
    <span class="ehb-kick">Paket Haji Plus 1448 H</span>
    <h2>Pilih paket Haji Plus sesuai kebutuhan Anda</h2>
    <p class="ehb-lead">Empat kelas paket dengan porsi resmi, tenda VIP di Armina, dan pendampingan ibadah dari manasik hingga pulang. Harga per jamaah dalam USD menurut jumlah orang per kamar.</p>
    <div class="ehj-pks">{''.join(paket_html(p) for p in PAKET)}</div>
    <p class="ehb-note">Untuk keberangkatan 2028, lihat <a href="https://haji.biz/paket-haji-plus-2028-elharamain-wisata/">Paket Haji Plus 2028</a>.</p>
  </div>
</section>
<section class="ehb-sec" id="fasilitas-haji">
  <div class="ehc-wrap">
    <span class="ehb-kick">Fasilitas</span>
    <h2>Nyaman dari Tanah Air sampai Armina</h2>
    <div class="ehj-ph">
      <figure><img loading="lazy" src="{U}2026/01/AAssets-haji-biz-2-2.webp" alt="Tenda maktab VIP jamaah Haji Plus di Mina"><figcaption><h3>Maktab VIP di Armina</h3><p>Tenda VIP dengan jarak dekat ke Jamarat, sehingga puncak haji lebih ringan dijalani.</p></figcaption></figure>
      <figure><img loading="lazy" src="{U}2026/01/AAssets-haji-biz-1-2.webp" alt="Hotel bintang 5 dekat Masjidil Haram untuk jamaah Haji Plus"><figcaption><h3>Hotel bintang 5</h3><p>Menginap dekat Masjidil Haram dan Masjid Nabawi, nyaman untuk beristirahat di sela ibadah.</p></figcaption></figure>
      <figure class="plane"><img loading="lazy" src="{U}2026/01/Untitled-design-1.png" alt="Pesawat Saudia Airlines untuk keberangkatan jamaah Haji Plus"><figcaption><h3>Maskapai &amp; bus VIP</h3><p>Terbang bersama Saudia, Qatar, atau Emirates, dilanjutkan bus VIP dan kereta cepat Haramain.</p></figcaption></figure>
    </div>
  </div>
</section>
<section class="ehb-sec ehb-dark" id="pelayanan">
  <div class="ehc-wrap">
    <span class="ehb-kick">Pelayanan &amp; bimbingan</span>
    <h2>Ibadah tenang, dibimbing dengan ilmu</h2>
    <div class="ehb-g3">
      {card('sajadah', 'Program yang menenangkan', 'Rangkaian perjalanan disusun agar jamaah nyaman dan tenang beribadah.')}
      {card('tim-solid', 'Tim berpengalaman', 'Tim solid yang terbiasa melayani puluhan ribu jamaah umroh dan haji.')}
      {card('reputasi', 'Kepuasan jamaah tinggi', 'Rating kepuasan jamaah yang tinggi menjadi ukuran kerja kami.')}
      {card('asatidz', 'Dibimbing asatidz', 'Pembimbing berpengalaman dan berilmu menemani dari manasik sampai pulang.')}
      {card('beribadah', 'Ibadah penuh makna', 'Program ibadah dirancang agar haji Anda bernilai dan bermakna.')}
      {card('kajian', 'Kajian sepanjang perjalanan', 'Banyak kajian dan ilmu yang didapat selama perjalanan ibadah haji.')}
    </div>
  </div>
</section>
<section class="ehb-sec ehb-soft" id="voucher">
  <div class="ehc-wrap ehj-2c rev">
    <figure class="ehj-promo"><img loading="lazy" src="{U}2026/08/promo-haji-plus.webp" alt="Free voucher umroh Rp 5 juta untuk jamaah Haji Plus Elharamain Wisata"></figure>
    <div>
      <span class="ehb-kick">Promo selama masa tunggu</span>
      <h2>Gratis voucher umroh senilai Rp 5 juta</h2>
      <p>Masa tunggu Haji Plus 8–10 tahun bisa diisi dengan ibadah umroh. Setiap jamaah Haji Plus Elharamain Wisata mendapatkan voucher umroh senilai Rp 5 juta yang bisa dipakai selama menunggu keberangkatan haji.</p>
      <p class="ehb-note">*Syarat &amp; ketentuan berlaku.</p>
      <div class="ehc-ctas">{btn('<i class="ehb-wa"></i> Tanyakan promo ini', 'wa', WA)}</div>
    </div>
  </div>
</section>
<section class="ehb-sec ehb-dark" id="cicilan">
  <div class="ehc-wrap ehj-2c">
    <div>
      <span class="ehb-kick">Program cicilan</span>
      <h2>Program Cicilan Haji Plus Elharamain Wisata</h2>
      <p>Layanan pembiayaan untuk mempermudah Anda mendapatkan nomor antrean haji khusus, dengan estimasi keberangkatan 5 hingga 9 tahun. Anda tidak perlu menunggu dana awal terkumpul penuh: dengan skema cicilan yang fleksibel, porsi haji bisa segera didapat.</p>
      <div class="ehc-ctas">{btn('Download brosur cicilan', 'wa')}</div>
    </div>
    <figure class="ehj-poster"><img loading="lazy" src="{U}2026/08/cicilan-haji-plus.webp" alt="Brosur program cicilan Haji Plus Elharamain Wisata"></figure>
  </div>
</section>
<section class="ehb-sec ehb-soft" id="tanya-jawab">
  <div class="ehc-wrap">
    <span class="ehb-kick">Seputar Haji Plus</span>
    <h2>Yang sering ditanyakan calon jamaah</h2>
    <div class="hb-faq">
      <details open><summary>Apa itu Haji Khusus atau Haji Plus?</summary><p>Program haji resmi yang memakai kuota haji nasional sesuai UU No. 8 Tahun 2019 tentang Penyelenggaraan Ibadah Haji dan Umrah. Penyelenggaranya pihak swasta yang sudah berizin sebagai Penyelenggara Ibadah Haji Khusus (PIHK), seperti Elharamain Wisata (SK No. 846/2020).</p></details>
      <details><summary>Berapa setoran awal untuk mendapatkan nomor porsi?</summary><p>Setoran awal 4.000 USD. Dana masuk langsung ke Kementerian, bukan ke rekening travel, dan nomor porsi tercatat atas nama jamaah di sistem SISKOHAT.</p></details>
      <details><summary>Berapa lama masa tunggu Haji Plus?</summary><p>Estimasi masa tunggu saat ini 8–10 tahun. Antrean terus bertambah setiap tahun, jadi semakin cepat mendaftar, semakin cepat peluang berangkat.</p></details>
      <details><summary>Berapa lama nomor porsi terbit setelah mendaftar?</summary><p>Sekitar 8 hari kerja. Seluruh administrasi pendaftaran dibantu oleh tim Elharamain Wisata.</p></details>
      <details><summary>Apakah pendaftaran bisa dicicil?</summary><p>Bisa, melalui Program Cicilan Haji Plus Elharamain Wisata. Hubungi tim kami untuk simulasi cicilan sesuai kemampuan Anda.</p></details>
    </div>
  </div>
</section>
<section class="ehb-sec" id="dokumentasi-haji">
  <div class="ehc-wrap">
    <span class="ehb-kick">Dokumentasi</span>
    <h2>Bersama jamaah Elharamain Wisata</h2>
    <div class="hb-doc">
      <img loading="lazy" src="{U}2026/01/2-5.webp" alt="Jamaah Elharamain Wisata di pelataran Masjidil Haram">
      <img loading="lazy" src="{U}2026/01/3-5.webp" alt="Rombongan jamaah Elharamain Wisata di Makkah">
      <img loading="lazy" src="{U}2026/01/1-5.webp" alt="Manasik jamaah Elharamain Wisata">
    </div>
  </div>
</section>
<section class="ehb-sec ehb-soft" id="ulasan-jamaah">
  <div class="ehc-wrap">
    <span class="ehb-kick">Testimoni jamaah</span>
    <h2>Bintang 5 dari 7.000+ ulasan Google</h2>
    <div class="hb-ti">[trustindex no-registration=google]</div>
    <div class="ehj-rv">{''.join(f'<a href="{u}" target="_blank" rel="noopener"><img loading="lazy" src="{u}" alt="Ulasan Google jamaah Elharamain Wisata"></a>' for u in ULASAN)}</div>
    <div class="ehc-ctas ehj-c">{btn('<i class="ehb-wa"></i> Konsultasi Haji Plus sekarang', 'wa', WA)}</div>
  </div>
</section>'''

CSS_HB = '''<style id="hb-home">
.hb-hero{background:linear-gradient(100deg,rgba(16,33,61,.95) 0%,rgba(16,33,61,.8) 48%,rgba(0,74,173,.4) 100%),url(https://haji.biz/wp-content/uploads/2026/01/2-5.webp) center/cover no-repeat!important}
.hb-pkh{position:relative;overflow:hidden;padding-top:26px}
.hb-pkh>*{position:relative}
.hb-pkh .foto{position:absolute;right:-18px;bottom:-14px;width:130px;height:auto;opacity:.28;margin:0}
.hb-pkh .th{display:inline-block;margin-top:6px;background:rgba(255,255,255,.2);border-radius:999px;padding:3px 10px;font:700 10.5px Montserrat,sans-serif;letter-spacing:.05em;text-transform:uppercase}
.hb-hrg{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;text-align:center}
.hb-hrg div{background:var(--soft);border-radius:10px;padding:8px 4px}
.hb-hrg small{display:block;font-size:11px}
.hb-hrg b{display:block;font:800 17px Martel,Georgia,serif;color:var(--nv)}
.hb-hrg div:first-child{background:#e6efff;outline:2px solid var(--bl)}
.hb-usd{display:block;text-align:center;margin-top:6px}
#kenapa .ehb-g3 .ehb-card{align-items:center;text-align:center}
.ehj-ph figure.plane img{object-fit:contain;background:linear-gradient(180deg,#e8f1ff,#fff);padding:18px}
.hb-faq{max-width:860px;display:grid;gap:12px}
.hb-faq details{background:#fff;border:1px solid var(--ln);border-radius:14px;padding:4px 20px;box-shadow:0 8px 22px rgba(16,33,61,.05)}
.hb-faq summary{cursor:pointer;list-style:none;padding:14px 28px 14px 0;font:700 17px Martel,Georgia,serif;color:var(--nv);position:relative}
.hb-faq summary::-webkit-details-marker{display:none}
.hb-faq summary::after{content:"+";position:absolute;right:0;top:10px;font:700 24px Montserrat,sans-serif;color:var(--bl)}
.hb-faq details[open] summary::after{content:"–"}
.hb-faq p{margin:0 0 16px;color:var(--mu)}
.hb-doc{display:grid;grid-template-columns:2fr 1fr 1fr;gap:12px;margin-top:24px}
.hb-doc img{width:100%;height:280px;object-fit:cover;border-radius:16px;display:block}
.hb-ti{margin:20px 0 24px}
@media(max-width:760px){.hb-doc{grid-template-columns:1fr}.hb-doc img{height:200px}.hb-hrg b{font-size:15px}}
</style>'''


def gaya_dasar():
    """CSS .ehc (blok 9991 & 9999) + .ehb + ikon 3D dari elharamainwisata.com, disalin agar halaman haji.biz mandiri."""
    import wp_rest as w
    css = []
    for ref in (9991, 9999):
        s, b = w.req('GET', f'/wp/v2/blocks/{ref}?context=edit&_fields=content')
        css += re.findall(r'<style[^>]*>.*?</style>', b['content']['raw'], re.S)
    s, d = w.req('GET', '/wp/v2/pages/7840?context=edit&_fields=content')
    st = re.findall(r'<style>\n\.ehb\{--nv.*?</style>|<style id="eh-ikon3d">.*?</style>', d['content']['raw'], re.S)
    if len(st) != 2 or len(css) < 2:
        sys.exit('CSS dasar tidak lengkap, berhenti')
    return '\n'.join(css + st)


def bangun():
    return (f'<!-- wp:html -->\n{FONTS}\n<div class="ehc ehb ehj">{SEKSI}\n</div>\n'
            f'{gaya_dasar()}\n{CSS_HAJI}\n{CSS_HB}\n<!-- /wp:html -->\n')


def hb(method, path, data=None):
    auth = 'Basic ' + base64.b64encode(f"{os.environ['WP_HAJIBIZ_USER']}:{os.environ['WP_HAJIBIZ_PASS']}".encode()).decode()
    cmd = ['curl', '-sS', '-X', method, '-H', 'Authorization: ' + auth, '-H', 'User-Agent: Mozilla/5.0 eh-admin',
           '-H', 'Content-Type: application/json', '-w', '\n%{http_code}', 'https://haji.biz/wp-json' + path]
    if data is not None:
        cmd[1:1] = ['--data-binary', '@-']
    out = subprocess.run(cmd, input=json.dumps(data).encode() if data is not None else None, capture_output=True).stdout.decode()
    body, code = out.rsplit('\n', 1)
    try:
        return int(code), json.loads(body)
    except ValueError:  # respons kosong/terpotong: kembalikan teks mentah, status tetap dipakai
        return int(code), body[:300]


if __name__ == '__main__':
    konten = bangun()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(konten)
    print('tulis', os.path.relpath(OUT, ROOT), len(konten), 'karakter')
    if '--draft' in sys.argv:
        data = {'title': 'Haji Plus (desain baru beranda)', 'content': konten, 'status': 'draft', 'template': 'elementor_header_footer'}
        pid = open(DRAFT_ID).read().strip() if os.path.exists(DRAFT_ID) else ''
        s, r = hb('POST', f'/wp/v2/pages/{pid}' if pid else '/wp/v2/pages', data)
        if s not in (200, 201):
            sys.exit(f'gagal simpan draft: {s} {str(r)[:300]}')
        open(DRAFT_ID, 'w').write(str(r['id']))
        print('draft haji.biz', r['id'], s, r['link'])
