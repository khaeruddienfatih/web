"""Desain ulang halaman Paket Haji Plus elharamainwisata.com (live: page 8289, Elementor) dengan gaya beranda
(blok wp:html .ehc.ehb, ikon 3D orisinal, latar selang-seling). Font khusus halaman ini: judul Martel, teks Mulish,
tombol/label Montserrat (Google Fonts). Isi, harga, foto, dan link CTA diambil dari halaman lama (8289, 4 Nov 2026).
Permintaan pemilik 2026-11-04: "desain ulang penuh", dibuat dulu sebagai DRAFT.

  python3 tools/build_haji_plus.py            -> tulis landing-pages/situs/elharamainwisata-com/haji-plus.html
  python3 tools/build_haji_plus.py --draft    -> + buat/perbarui page Draft (ID disimpan di file .draft-id)
Kredensial dari env WP_USER / WP_APP_PASSWORD."""
import html, json, os, re, sys

ROOT = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(ROOT, 'landing-pages', 'situs', 'elharamainwisata-com', 'haji-plus.html')
DRAFT_ID = os.path.join(ROOT, 'landing-pages', 'situs', 'elharamainwisata-com', 'haji-plus.draft-id')
MEDIA = json.load(open(os.path.join(ROOT, 'wordpress', 'ikon-3d', 'media.json')))
U = 'https://elharamainwisata.com/wp-content/uploads/'
CTA = 'https://umroh.elharamainwisata.com/hajiplus/'  # link CTA halaman lama (semua tombol)


def ik(slug):
    return (f'<span class="ehb-ic ehb-ic3d"><img src="{MEDIA[slug]["url"]}" alt="" width="64" height="64" '
            f'loading="lazy" decoding="async"></span>')


def card(slug, judul, teks):
    return f'<div class="ehb-card">{ik(slug)}<h3>{judul}</h3><p>{teks}</p></div>'


def btn(teks, kelas='pri', href=CTA):
    return f'<a class="ehb-btn {kelas}" href="{href}" target="_blank" rel="noopener">{teks}</a>'


# ---------------- data paket (dari 8289) ----------------
UMUM = [('Maskapai', 'Saudia / Qatar / Emirates'), ('Transportasi', 'Bus VIP terbaru'),
        ('Bimbingan', 'Asatidz berilmu &amp; berpengalaman')]
PAKET = [
    dict(nama='Silver', medali='medali-silver', kelas='p1', harga='USD 12.000', catatan='', baris=[
        ('Durasi', '23–24 hari'), ('Maktab VIP', '116'), ('Jarak Jamarat', '900 m'),
        ('Hotel Makkah', 'Anjum / setaraf (★5)'), ('Hotel Madinah', 'Concorde Dar Al Khair / setaraf (★4)'),
        *UMUM, ('Program Arbain', '–'), ('Layanan', 'Pendaftaran mudah &amp; ringan')]),
    dict(nama='Gold', medali='medali-gold', kelas='p2', harga='USD 15.500', catatan='', baris=[
        ('Durasi', '23–24 hari'), ('Maktab VIP', '113'), ('Jarak Jamarat', '500 m'),
        ('Hotel Makkah', 'Anjum / setaraf (★5) atau Marwa Rotana / setaraf (★5)'), ('Hotel Madinah', 'Al-Aqeeq / setaraf (★5)'),
        *UMUM, ('Program Arbain', '–'), ('Layanan', 'Pendaftaran mudah &amp; ringan')]),
    dict(nama='Gold Arbain', medali='medali-arbain', kelas='p3', harga='USD 17.000', catatan='', baris=[
        ('Durasi', '28–29 hari'), ('Maktab VIP', '113'), ('Jarak Jamarat', '500 m'),
        ('Hotel Makkah', 'Marwa Rotana / setaraf (★5)'), ('Hotel Madinah', 'Al-Aqeeq / setaraf (★5)'),
        *UMUM, ('Program Arbain', '<b class="ok">Termasuk</b>'), ('Layanan', 'Pendaftaran mudah &amp; ringan')]),
    dict(nama='Platinum', medali='medali-platinum', kelas='p4', harga='USD 20.000', catatan='±Rp 321 juta', baris=[
        ('Durasi', '23–24 hari'), ('Maktab VIP', '111/112'), ('Jarak Jamarat', '200 m'),
        ('Hotel Makkah', 'Fairmont / setaraf (★5)'), ('Hotel Madinah', 'Movenpick / setaraf (★5)'),
        *UMUM, ('Program Arbain', '–'), ('Layanan', 'Layanan premium prioritas')]),
]


def paket_html(p):
    rows = ''.join(f'<li><span>{k}</span><b>{v}</b></li>' for k, v in p['baris'])
    cat = f'<small class="cat">{p["catatan"]}</small>' if p['catatan'] else ''
    return (f'<div class="ehj-pk {p["kelas"]}"><div class="ehj-pkh"><img src="{MEDIA[p["medali"]]["url"]}" alt="Medali paket {p["nama"]}" '
            f'width="72" height="72" loading="lazy"><h3>{p["nama"]}</h3></div>'
            f'<div class="ehj-pkb"><small>opsi kamar 4 / 3 / 2 · mulai</small><b class="hrg">{p["harga"]}</b>{cat}'
            f'<small>DP porsi 4.000 USD</small><ul>{rows}</ul>{btn("Tanya detail paket")}</div></div>')


SLIDE = [f'{U}2025/08/Slide{n}Elharamain-Haji-2025.jpeg' for n in (10, 9, 8, 7, 6, 5, 4, 11, 13)]
ULASAN = [f'{U}2026/02/{n}.jpg' for n in ('22', '21', '20', '19', '18', '14-1', '17', '16-1', '15-1')]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Martel:wght@400;700;800&family=Montserrat:wght@600;700&'
         'family=Mulish:wght@400;600;700&display=swap" rel="stylesheet">')

SEKSI = f'''
<section class="ehb-hero">
  <div class="ehc-wrap ehb-hero-in">
    <div class="ehb-hero-tx">
      <span class="ehb-pill">PT Dhiyaa El Haramain El Mubarakah · PIHK resmi No. 846/2020</span>
      <h1>Semakin menunda, <em>masa tunggu Haji Plus</em> semakin panjang</h1>
      <p>Masa tunggu Haji Plus lebih singkat, pelayanan terbaik, dan fasilitas eksklusif untuk ibadah Haji Plus Anda bersama Elharamain Wisata.</p>
      <div class="ehc-ctas">{btn('<i class="ehb-wa"></i> Konsultasi Sekarang', 'wa')}<a class="ehb-btn glass" href="#paket">Lihat 4 paket Haji Plus</a></div>
    </div>
    <div class="ehb-next">
      <small>Program Haji Plus</small>
      <b>Masa tunggu 8–10 tahun</b>
      <span>DP porsi 4.000 USD</span>
      <p>mulai <strong>USD 12.000</strong></p>
      <span>Paket Silver · opsi kamar 4 / 3 / 2</span>
      {btn('Tanya detail paket →', 'wa')}
    </div>
  </div>
  <div class="ehc-wrap"><div class="ehb-stat">
    <div><b>7.000+</b><span>ulasan Google bintang 5</span></div>
    <div><b>1.400+</b><span>pendaftar haji dalam 1 tahun</span></div>
    <div><b>6 kantor</b><span>Jabodetabek &amp; Bandung</span></div>
    <div><b>Akreditasi A</b><span>Komite Akreditasi Nasional</span></div>
  </div></div>
</section>
<section class="ehb-sec ehb-pt0 ehb-up">
  <div class="ehc-wrap"><div class="ehb-g4">
    {card('cicilan-ringan', 'Masa tunggu 8–10 tahun', 'Program Haji Plus dengan masa tunggu lebih singkat dibanding haji reguler.')}
    {card('izin-resmi', 'Resmi Kemenag RI', 'Penyelenggara Ibadah Haji Khusus (PIHK) dengan SK No. 846/2020.')}
    {card('akreditasi', 'Terakreditasi A', 'Diakreditasi oleh Komite Akreditasi Nasional (KAN).')}
    {card('beribadah', 'Maktab VIP', 'Jarak ke Jamarat 200–900 m sesuai paket, akses lebih mudah saat puncak haji.')}
  </div></div>
</section>
<section class="ehb-sec" id="profil">
  <div class="ehc-wrap">
    <div class="ehj-2c">
      <div>
        <span class="ehb-kick">Profil</span>
        <h2>Profil Elharamain Wisata</h2>
        <p>PT Dhiyaa El Haramain El Mubarakah (Elharamain Wisata) merupakan Penyelenggara Resmi Ibadah Haji Khusus (PIHK) dengan izin No. 846 Tahun 2020.</p>
        <p>Elharamain Wisata menghadirkan layanan Haji Plus Premium dengan fasilitas unggulan, hotel berkualitas, maskapai terbaik, pembimbing berpengalaman, pelayanan personal, serta sistem perjalanan terencana demi ibadah yang aman, nyaman, khusyuk, dan penuh makna. Elharamain Wisata memiliki 6 kantor di Jakarta, Bekasi, Tangerang, Depok, Bogor, dan Bandung.</p>
      </div>
      <figure class="ehj-foto"><img loading="lazy" src="{U}2026/02/Assets-LP-Elharamain-Wisata-18-1.webp" alt="Kantor Elharamain Wisata"></figure>
    </div>
    <div class="ehb-logos">
      <figure><img loading="lazy" src="{U}2024/05/logo-kemenag.png" alt="Logo Kementerian Agama RI" width="150" height="165"><figcaption><b>Kemenag RI</b><small>PIHK 846/2020 · PPIU 63/2020</small></figcaption></figure>
      <figure><img loading="lazy" src="{U}2024/05/logo-himpuh.png" alt="Logo HIMPUH" width="154" height="165"><figcaption><b>HIMPUH</b><small>Anggota No. 131/2017</small></figcaption></figure>
      <figure><img loading="lazy" src="{U}2024/05/logo-iata.png" alt="Logo IATA" width="200" height="165"><figcaption><b>IATA</b><small>Kode 15333220</small></figcaption></figure>
    </div>
    <div class="ehj-g5">
      {card('jamaah-umroh', '8.500+', 'Jamaah umroh dalam 1 tahun')}
      {card('pendaftar-haji', '1.400+', 'Pendaftar haji dalam 1 tahun')}
      {card('kantor-cabang', '6 kantor', 'Pelayanan di Jabodetabek &amp; Bandung')}
      {card('berpengalaman', 'Berpengalaman', 'Membimbing ribuan jamaah umroh &amp; haji')}
      {card('reputasi', 'Reputasi tinggi', 'Layanan &amp; kepuasan jamaah yang tinggi')}
    </div>
  </div>
</section>
<section class="ehb-sec ehb-dark" id="kenapa-haji">
  <div class="ehc-wrap ehj-2c">
    <div>
      <span class="ehb-kick">Kenapa Elharamain Wisata</span>
      <h2>Kenapa berhaji dengan Elharamain Wisata?</h2>
      <p class="ehb-lead">Kami hadir dengan proses pendaftaran paling ringan &amp; mudah se-Indonesia. Masa tunggu saat ini 8–10 tahun: semakin menunda, masa tunggu semakin panjang.</p>
      <div class="ehj-why">
        {card('booking-dp', 'Pendaftaran paling ringan se-Indonesia', 'DP hanya 4.000 USD, jauh lebih terjangkau dibanding travel lain yang bisa 5.000–6.000 USD.')}
        {card('booking-seat', 'Free voucher umroh Rp 5.000.000', 'Bisa digunakan untuk perjalanan umroh berikutnya.')}
      </div>
      <p class="ehb-note">*Syarat &amp; ketentuan berlaku.</p>
    </div>
    <figure class="ehj-promo"><img loading="lazy" src="{U}2026/02/Assets-LP-Elharamain-Wisata-12-1.webp" alt="Free voucher umroh Rp 5 juta untuk jamaah Haji Plus Elharamain Wisata"></figure>
  </div>
</section>
<section class="ehb-sec ehb-soft" id="paket">
  <div class="ehc-wrap">
    <span class="ehb-kick">Harga paket kompetitif</span>
    <h2>4 paket Haji Plus Elharamain Wisata</h2>
    <p class="ehb-lead">Semua paket dengan DP porsi 4.000 USD, maskapai Saudia / Qatar / Emirates, Bus VIP terbaru, dan bimbingan asatidz berilmu &amp; berpengalaman.</p>
    <div class="ehj-pks">{''.join(paket_html(p) for p in PAKET)}</div>
  </div>
</section>
<section class="ehb-sec" id="fasilitas-haji">
  <div class="ehc-wrap">
    <span class="ehb-kick">Fasilitas</span>
    <h2>Fasilitas terbaik di kelasnya</h2>
    <div class="ehj-ph">
      <figure><img loading="lazy" src="{U}2026/02/14.jpg" alt="Fasilitas Maktab VIP Haji Plus Elharamain Wisata"><figcaption><h3>Fasilitas Maktab VIP</h3><p>Jarak dekat dengan Jamarat, akses lebih mudah saat puncak haji.</p></figcaption></figure>
      <figure><img loading="lazy" src="{U}2026/02/15.jpg" alt="Fasilitas hotel bintang 5 Haji Plus Elharamain Wisata"><figcaption><h3>Fasilitas hotel ★★★★★</h3><p>Hotel bintang 5 terbaik di kelasnya, lebih nyaman untuk istirahat jamaah.</p></figcaption></figure>
      <figure><img loading="lazy" src="{U}2026/02/16.jpg" alt="Maskapai terbaik dan Bus VIP Haji Plus Elharamain Wisata"><figcaption><h3>Airlines terbaik &amp; Bus VIP terbaru</h3><p>Perjalanan lebih aman, nyaman, dan terjamin.</p></figcaption></figure>
    </div>
  </div>
</section>
<section class="ehb-sec ehb-dark" id="layanan-haji">
  <div class="ehc-wrap">
    <span class="ehb-kick">Pelayanan</span>
    <h2>Menghadirkan layanan terbaik</h2>
    <div class="ehb-g3">
      {card('sajadah', 'Kenyamanan beribadah', 'Program dirancang memberikan kenyamanan &amp; ketenangan beribadah.')}
      {card('rating', 'Rating kepuasan tertinggi', 'Elharamain Wisata memiliki rating tertinggi dalam kepuasan jamaahnya.')}
      {card('tim-solid', 'Tim solid &amp; berpengalaman', 'Tim berpengalaman menangani puluhan ribu jamaah.')}
    </div>
  </div>
</section>
<section class="ehb-sec" id="bimbingan">
  <div class="ehc-wrap">
    <span class="ehb-kick">Bimbingan ibadah intensif</span>
    <h2>Membuat ibadah Anda lebih bermakna</h2>
    <div class="ehb-g3">
      {card('asatidz', 'Dibimbing asatidz', 'Dibimbing oleh asatidz berpengalaman &amp; berilmu.')}
      {card('beribadah', 'Program ibadah terarah', 'Program ibadah yang dirancang menjadikan ibadah haji Anda penuh nilai &amp; bermakna.')}
      {card('kajian', 'Kajian selama perjalanan', 'Banyak kajian dan ilmu selama perjalanan ibadah haji.')}
    </div>
  </div>
</section>
<section class="ehb-sec ehb-dark" id="pembiayaan">
  <div class="ehc-wrap ehj-2c rev">
    <figure class="ehj-poster"><img loading="lazy" src="{U}2026/02/Elhamain-Wisata-Haji-1.jpg" alt="Program pembiayaan nomor porsi Haji Plus Elharamain Wisata bersama Bank Muamalat"></figure>
    <div>
      <span class="ehb-kick">Solusi syariah · Bank Muamalat</span>
      <h2>Program pembiayaan nomor porsi Haji Plus</h2>
      <p>Program Pembiayaan Nomor Porsi Haji bekerja sama dengan Bank Muamalat hadir sebagai solusi syariah bagi Anda yang ingin segera mendaftar haji. Menggunakan prinsip syariah dan telah mendapatkan persetujuan DSN MUI, program ini aman dan terpercaya.</p>
      <p>Dengan DP hanya <b class="gd">Rp2,5 juta</b> dan cicilan mulai satu jutaan per bulan, Anda sudah dapat memperoleh nomor porsi haji resmi. Wujudkan niat suci ke Baitullah lebih cepat, terencana, dan sesuai syariat bersama Elharamain Wisata.</p>
      <div class="ehc-ctas">{btn('Program pembiayaan nomor porsi', 'wa')}</div>
    </div>
  </div>
</section>
<section class="ehb-sec ehb-soft" id="itinerary">
  <div class="ehc-wrap">
    <span class="ehb-kick">Perjalanan</span>
    <h2>Rencana &amp; itinerary perjalanan haji</h2>
    <p class="ehb-lead">Gambaran rute dan jadwal perjalanan tiap paket. Klik gambar untuk melihat ukuran penuh.</p>
    <div class="ehj-itin">
      <a href="{U}2026/02/haji-plus-819x1024-1.jpg" target="_blank" rel="noopener"><img loading="lazy" src="{U}2026/02/haji-plus-819x1024-1.jpg" alt="Rencana program perjalanan Haji Plus Elharamain Wisata"></a>
      <a href="{U}2026/02/Paket-Haji-Plus-819x1024-1.jpg" target="_blank" rel="noopener"><img loading="lazy" src="{U}2026/02/Paket-Haji-Plus-819x1024-1.jpg" alt="Itinerary perjalanan Haji Plus Elharamain Wisata per paket"></a>
    </div>
  </div>
</section>
<section class="ehb-sec" id="dokumentasi-haji">
  <div class="ehc-wrap">
    <span class="ehb-kick">Dokumentasi</span>
    <h2>Jamaah Haji Plus Elharamain Wisata</h2>
    <p class="ehb-lead">Momen jamaah Haji Plus Elharamain Wisata musim haji 2025.</p>
    <div class="ehb-mos ehj-mos">{''.join(f'<figure class="{"big" if i == 0 else ""}"><img loading="lazy" src="{u}" alt="Jamaah Haji Plus Elharamain Wisata 2025"></figure>' for i, u in enumerate(SLIDE[:8]))}</div>
  </div>
</section>'''

ULASAN_HTML = f'''<div class="ehc ehb ehj"><section class="ehb-sec ehb-soft ehb-pt0" id="ulasan-jamaah">
  <div class="ehc-wrap">
    <p class="ehb-lead ehj-c">Elharamain Wisata memiliki <b>bintang 5 dari 7.000+ ulasan Google</b>. Berikut sebagian ulasan jamaah:</p>
    <div class="ehj-rv">{''.join(f'<a href="{u}" target="_blank" rel="noopener"><img loading="lazy" src="{u}" alt="Ulasan Google jamaah Elharamain Wisata"></a>' for u in ULASAN)}</div>
    <div class="ehc-ctas ehj-c">{btn('<i class="ehb-wa"></i> Konsultasi Haji Plus sekarang', 'wa')}</div>
  </div>
</section></div>'''

CSS_HAJI = '''<style id="ehj">
.ehj,.ehj p,.ehj li,.ehj small,.ehj span,.ehj figcaption{font-family:Mulish,sans-serif}
.ehj h1,.ehj h2,.ehj h3,.ehj .ehb-next b,.ehj .ehb-stat b,.ehj .ehj-pkb .hrg{font-family:Martel,Georgia,serif!important;letter-spacing:0}
.ehj .ehb-hero h1{font-weight:800;line-height:1.14;font-size:clamp(34px,5vw,56px)}
.ehj h2{font-weight:800;line-height:1.25}
.ehj h3{font-weight:700;line-height:1.35}
.ehj .ehb-kick,.ehj .ehb-btn,.ehj .ehb-pill,.ehj .ehb-next small{font-family:Montserrat,sans-serif!important}
.ehj .ehb-hero{background:linear-gradient(100deg,rgba(16,33,61,.95) 0%,rgba(16,33,61,.82) 48%,rgba(0,74,173,.42) 100%),url(https://elharamainwisata.com/wp-content/uploads/2025/08/Slide10Elharamain-Haji-2025.jpeg) center/cover no-repeat}
.ehj p{line-height:1.7}
.ehj-2c{display:grid;grid-template-columns:1.25fr .75fr;gap:40px;align-items:center}
.ehj-2c.rev{grid-template-columns:.8fr 1.2fr}
.ehj-foto,.ehj-promo,.ehj-poster{margin:0}
.ehj-foto img{width:100%;border-radius:18px;box-shadow:0 14px 34px rgba(16,33,61,.14)}
.ehj-promo img{width:100%;max-width:420px;display:block;margin:auto}
.ehj-poster img{width:100%;border-radius:18px;box-shadow:0 18px 40px rgba(0,0,0,.25)}
#profil p{color:var(--mu)}
.ehj-g5{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}
.ehj-g5 .ehb-card{align-items:center;text-align:center;padding:24px 16px}
.ehj-g5 h3{font-size:22px;color:var(--bl)}
.ehj-why{display:grid;gap:14px}
.ehj-why .ehb-card{flex-direction:row;gap:18px;align-items:center}
.ehj-why .ehb-ic{margin:0;flex:none}
.ehj .ehb-dark p.ehb-note{color:rgba(255,255,255,.7)}
.ehj .ehb-g3 .ehb-card,.ehj .ehb-up .ehb-card{text-align:left}
.ehj-pks{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;align-items:stretch}
.ehj-pk{background:#fff;border:1px solid var(--ln);border-radius:20px;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 12px 30px rgba(16,33,61,.07);transition:transform .2s,box-shadow .2s}
.ehj-pk:hover{transform:translateY(-4px);box-shadow:0 20px 40px rgba(0,74,173,.16)}
.ehj-pkh{padding:22px 16px 18px;text-align:center;color:#fff}
.ehj-pkh img{width:72px;height:72px;display:block;margin:0 auto 6px}
.ehj-pkh h3{color:#fff;margin:0;font-size:24px}
.p1 .ehj-pkh{background:linear-gradient(135deg,#4f5d70,#95a3b5)}
.p2 .ehj-pkh{background:linear-gradient(135deg,#8c6812,#d0a534)}
.p3 .ehj-pkh{background:linear-gradient(135deg,#6b3f00,#c07f10)}
.p4 .ehj-pkh{background:linear-gradient(135deg,#004AAD,#1684CF)}
.ehj-pkb{padding:18px;display:flex;flex-direction:column;flex:1}
.ehj-pkb small{font-size:12.5px;color:var(--mu)}
.ehj-pkb .hrg{font-size:28px;font-weight:800;color:var(--nv);margin:2px 0}
.ehj-pkb .cat{font-weight:700;color:var(--bl)}
.ehj-pkb ul{list-style:none;margin:14px 0 18px;padding:0;border-top:1px solid var(--ln)}
.ehj-pkb li{display:grid;grid-template-columns:44% 56%;gap:8px;padding:8px 0;border-bottom:1px dashed var(--ln);font-size:13.5px}
.ehj-pkb li span{color:var(--mu)}
.ehj-pkb li b{font-weight:700;color:var(--nv)}
.ehj-pkb li b.ok{color:#0f9157}
.ehj-pkb .ehb-btn{margin-top:auto}
.ehj-ph{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:28px}
.ehj-ph figure{margin:0;background:#fff;border:1px solid var(--ln);border-radius:18px;overflow:hidden;box-shadow:0 12px 30px rgba(16,33,61,.07)}
.ehj-ph img{width:100%;aspect-ratio:16/10;object-fit:cover;display:block}
.ehj-ph figcaption{padding:18px 20px 22px}
.ehj-ph h3{margin:0 0 6px;font-size:19px;color:var(--nv)}
.ehj-ph p{margin:0;color:var(--mu);font-size:14.5px}
.ehj .gd{color:var(--gd)}
.ehj-itin{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.ehj-itin img{width:100%;border-radius:16px;display:block;box-shadow:0 12px 30px rgba(16,33,61,.12)}
.ehj-mos{grid-template-columns:2fr 1fr 1fr}
.ehj .ehj-c{text-align:center;margin-left:auto;margin-right:auto;justify-content:center}
.ehj-rv{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;padding:6px 2px 16px;margin-bottom:22px}
.ehj-rv a{flex:0 0 260px;scroll-snap-align:start}
.ehj-rv img{width:100%;border-radius:14px;display:block;box-shadow:0 8px 22px rgba(16,33,61,.12)}
@media(max-width:1024px){.ehj-pks{grid-template-columns:repeat(2,1fr)}.ehj-g5{grid-template-columns:repeat(3,1fr)}}
@media(max-width:760px){.ehj-2c,.ehj-2c.rev{grid-template-columns:1fr;gap:24px}.ehj-pks,.ehj-ph,.ehj-itin{grid-template-columns:1fr}
.ehj-g5{grid-template-columns:1fr 1fr}.ehj-why .ehb-card{flex-direction:column;align-items:flex-start}.ehj-rv a{flex-basis:220px}
.ehj .ehb-stat b{font-size:21px}.ehj .ehb-next b{font-size:23px}}
</style>'''


def gaya_beranda():
    """CSS komponen .ehb + ikon 3D disalin dari beranda (7840) supaya halaman ini mandiri."""
    import wp_rest as w
    s, d = w.req('GET', '/wp/v2/pages/7840?context=edit&_fields=content')
    c = d['content']['raw']
    st = re.findall(r'<style>\n\.ehb\{--nv.*?</style>|<style id="eh-ikon3d">.*?</style>', c, re.S)
    if len(st) != 2:
        sys.exit(f'CSS beranda tidak ditemukan lengkap ({len(st)}), berhenti')
    return '\n'.join(st)


def bangun():
    return ('<!-- wp:block {"ref":9991} /-->\n\n<!-- wp:block {"ref":9999} /-->\n\n<!-- wp:block {"ref":10076} /-->\n\n'
            f'<!-- wp:html -->\n{FONTS}\n<div class="ehc ehb ehj">{SEKSI}\n</div>\n<!-- /wp:html -->\n\n'
            '<!-- wp:block {"ref":9994} /-->\n\n'
            f'<!-- wp:html -->\n{ULASAN_HTML}\n{gaya_beranda()}\n{CSS_HAJI}\n<!-- /wp:html -->\n')


if __name__ == '__main__':
    konten = bangun()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(konten)
    print('tulis', os.path.relpath(OUT, ROOT), len(konten), 'karakter')
    if '--draft' in sys.argv:
        import wp_rest as w
        data = {'title': 'Paket Haji Plus Elharamain Wisata (desain baru)', 'content': konten, 'status': 'draft',
                'template': 'elementor_header_footer'}
        pid = open(DRAFT_ID).read().strip() if os.path.exists(DRAFT_ID) else ''
        s, r = w.req('POST', f'/wp/v2/pages/{pid}' if pid else '/wp/v2/pages', data)
        if s not in (200, 201):
            sys.exit(f'gagal simpan draft: {s} {r}')
        open(DRAFT_ID, 'w').write(str(r['id']))
        print('draft', r['id'], s, r['link'])
