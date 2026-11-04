"""hajifuroda.co.id: desain ulang beranda + Profil/Layanan/Kontak dengan identitas sendiri (prefix kelas hfx-), permintaan
pemilik 2026-11-04 ("perbaiki semua page dan homepagenya buat unik dari lainnya").
Mengikuti aturan pemilik untuk situs ini (brief Agen Paket 29-30 Okt): warna hanya biru #004AAD/#0A2E6B/#1684CF/#9FC9F5 + putih
(TANPA kuning/emas), font Poppins, ikon solid putih di lingkaran biru (SVG sendiri), tanpa kata "sumber/brosur", tanpa label kecil
di atas judul, judul tanpa titik dua, sudut pandang "daftar haji khusus & nomor porsi". Angka dari Brosur Haji 1448 H
(workspace-paket/materi/BROSUR_HAJI_1448_H.txt); jarak Jamarat/tenda & nomor maktab TIDAK ditulis (angka di brosur bertentangan).
Foto dari Media hajifuroda.co.id. Cadangan semua halaman: backup/2026-11-04_hajifuroda/.

  python3 tools/build_hajifuroda.py [halaman ...]          -> landing-pages/situs/hajifuroda/<halaman>.html
  python3 tools/build_hajifuroda.py --draft [halaman ...]  -> + simpan ke Draft (ID di <halaman>.draft-id)
halaman: beranda, profil, layanan, kontak.  Kredensial env WP_HAJIFURODA_USER / WP_HAJIFURODA_PASS."""
import base64, html, json, os, subprocess, sys, urllib.parse as up

ROOT = os.path.join(os.path.dirname(__file__), '..')
DIR = os.path.join(ROOT, 'landing-pages', 'situs', 'hajifuroda')
U = 'https://www.hajifuroda.co.id/wp-content/uploads/'
H = 'https://www.hajifuroda.co.id'
WA_NO = '6281287292422'


def wa(teks):
    return f'https://api.whatsapp.com/send?phone={WA_NO}&amp;text=' + up.quote(teks)


WA_DAFTAR = wa("Assalamu'alaikum Elharamain Wisata, saya ingin daftar haji khusus.")
WA_SIMULASI = wa("Assalamu'alaikum Elharamain Wisata, saya ingin simulasi biaya haji khusus.")

# ---------- ikon solid (24x24), putih di lingkaran biru ----------
P = {
    'perisai': 'M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5zm-1.2 14.2-3.5-3.5 1.4-1.4 2.1 2.1 4.6-4.6 1.4 1.4z',
    'dokumen': 'M6 2h8l5 5v13a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2zm7 1.5V8h4.5zM8 12v2h8v-2zm0 4v2h6v-2z',
    'koin': 'M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm1 15.9V19h-2v-1.1c-1.7-.3-3-1.4-3.1-3h2c.1.8.9 1.4 2.1 1.4 1.3 0 2-.6 2-1.4 0-.9-.8-1.2-2.4-1.6-2-.5-3.4-1.2-3.4-3 0-1.4 1.1-2.5 2.8-2.8V6.4h2v1.1c1.6.3 2.7 1.4 2.8 2.9h-2c-.1-.8-.8-1.3-1.9-1.3-1 0-1.7.5-1.7 1.2 0 .8.8 1.1 2.3 1.5 2.1.5 3.5 1.3 3.5 3.1 0 1.5-1.2 2.6-3 3z',
    'kalender': 'M7 2h2v2h6V2h2v2h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2zM5 9v11h14V9zm2 2h3v3H7z',
    'pesawat': 'M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z',
    'gedung': 'M4 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v4h2a2 2 0 0 1 2 2v12h-6v-4h-4v4zm4-16v2h2V6zm4 0v2h2V6zM8 10v2h2v-2zm4 0v2h2v-2zm-4 4v2h2v-2zm4 0v2h2v-2zm4-2v2h2v-2zm0 4v2h2v-2z',
    'bus': 'M5 3h14a2 2 0 0 1 2 2v11a2 2 0 0 1-1 1.7V20a1 1 0 0 1-1 1h-1a1 1 0 0 1-1-1v-1H7v1a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-2.3A2 2 0 0 1 3 16V5a2 2 0 0 1 2-2zm0 3v5h14V6zm2 8.5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3zm10 0a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3z',
    'tenda': 'M12 2 1 21h8l3-6 3 6h8zm0 4.6L5.3 18H8l4-8 4 8h2.7z',
    'kabah': 'M3 7 12 3l9 4v11l-9 4-9-4zm0 4.5 9 4 9-4V9.3l-9 4-9-4z',
    'buku': 'M12 6c-2-1.5-5-2-9-2v15c4 0 7 .5 9 2 2-1.5 5-2 9-2V4c-4 0-7 .5-9 2zm-1 12.6c-1.8-.9-4.1-1.4-6-1.5V6c2.4.1 4.5.6 6 1.6zm2 0V7.6c1.5-1 3.6-1.5 6-1.6v11.1c-1.9.1-4.2.6-6 1.5z',
    'chat': 'M4 3h16a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H9l-5 4v-4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2zm3 7a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3zm5 0a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3zm5 0a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3z',
    'pin': 'M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z',
    'orang': 'M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zm8 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM1 20c0-3.3 3.6-6 8-6s8 2.7 8 6v1H1zm16.5-5.9c2.9.4 5.5 2.4 5.5 4.9v1h-4.2v-1c0-1.9-.5-3.5-1.3-4.9z',
    'hati': 'M12 21s-9-5.6-9-12a5 5 0 0 1 9-3 5 5 0 0 1 9 3c0 6.4-9 12-9 12z',
    'medis': 'M10 3h4v7h7v4h-7v7h-4v-7H3v-4h7z',
    'hadiah': 'M20 7h-2.2A3 3 0 0 0 12 4.4 3 3 0 0 0 6.2 7H4a1 1 0 0 0-1 1v3h8V7h2v4h8V8a1 1 0 0 0-1-1zM9 7a1 1 0 1 1 1-1v1zm5 0V6a1 1 0 1 1 1 1zM4 13h7v8H5a1 1 0 0 1-1-1zm9 0h7v7a1 1 0 0 1-1 1h-6z',
    'bulan': 'M14.5 2A10 10 0 1 0 22 15.5 8 8 0 0 1 14.5 2z',
    'kereta': 'M7 2h10a3 3 0 0 1 3 3v10a3 3 0 0 1-2.2 2.9L20 21h-2.5l-2-3h-7l-2 3H4l2.2-3.1A3 3 0 0 1 4 15V5a3 3 0 0 1 3-3zm-1 4v5h12V6zm2 7.5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3zm8 0a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3z',
    'ulang': 'M12 4V1L7 5l5 4V6a6 6 0 1 1-6 6H4a8 8 0 1 0 8-8z',
    'telepon': 'M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.6 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.2.2 2.4.6 3.6a1 1 0 0 1-.25 1z',
    'bintang': 'M12 2l3 6.3 7 1-5 4.8 1.2 6.9L12 17.7 5.8 21 7 14.1 2 9.3l7-1z',
    'cek': 'M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z',
    'koper': 'M9 2h6a1 1 0 0 1 1 1v3h3a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h3V3a1 1 0 0 1 1-1zm1 2v2h4V4z',
}


def ik(nama, kecil=False):
    return (f'<span class="hfx-ic{" s" if kecil else ""}" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="{P[nama]}"/></svg></span>')


def foto(f, alt, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<img{c} loading="lazy" decoding="async" src="{U}{f}" alt="{html.escape(alt)}">'


def btn(teks, href=WA_DAFTAR, kelas='wa', baru=True):
    t = ' target="_blank" rel="noopener"' if baru else ''
    pre = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="' + P['chat'] + '"/></svg>' if kelas == 'wa' else ''
    return f'<a class="hfx-btn {kelas}" href="{href}"{t}>{pre}{teks}</a>'


def judul(h2, lead=''):
    return f'<div class="hfx-hd"><h2>{h2}</h2>' + (f'<p>{lead}</p>' if lead else '') + '</div>'


def faq(items):
    body = ''.join(f'<details class="hfx-faq-i"><summary>{q}</summary><p>{a}</p></details>' for q, a in items)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": html.unescape(q), "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}} for q, a in items]}
    return f'<div class="hfx-faq">{body}</div><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'


# ---------- data (Brosur Haji 1448 H, estimasi keberangkatan 2027) ----------
PAKET = [
    dict(n='Silver', hari='22–23 hari', mk='Anjum Hotel / setaraf ★5', md='Concorde Dar Al Khair / setaraf ★4', fl='Saudia / Qatar / Emirates',
         tr='Hotel Orvana', arb=False, h=('12.000', '13.500', '15.000')),
    dict(n='Gold', hari='22–23 hari', mk='Marwa Rotana / setaraf ★5', md='Al-Aqeeq Hotel / setaraf ★5', fl='Saudia / Qatar / Emirates',
         tr='Hotel Orvana', arb=False, h=('15.500', '17.000', '18.500')),
    dict(n='Gold Arbain', hari='27–28 hari', mk='Marwa Rotana / setaraf ★5', md='Al-Aqeeq Hotel / setaraf ★5', fl='Saudia / Qatar / Emirates',
         tr='Hotel Orvana', arb=True, h=('17.000', '18.500', '20.000')),
    dict(n='Platinum', hari='22–23 hari', mk='Fairmont Makkah Clock Royal Tower / setaraf ★5', md='Movenpick Hotel / setaraf ★5',
         fl='Saudia / Garuda Indonesia', tr='Roots Hotel', arb=False, h=('20.000', '22.000', '24.000')),
]

KANTOR = [
    ('Kantor Pusat Bekasi', 'Ruko Emerald No.5 Blok EB 1, Jl. Harapan Indah Raya, Kec. Medan Satria, Kota Bekasi, Jawa Barat 17132', '0812-8729-2422', '6281287292422', 'Bekasi'),
    ('Kantor Jakarta', 'Jl. Tebet Raya No.39 B, Tebet Timur, Kec. Tebet, Kota Jakarta Selatan, DKI Jakarta 12820', '0812-1417-8056', '6281214178056', 'Jakarta'),
    ('Kantor Depok', 'Jl. Margonda No.252 D, Kemiri Muka, Kec. Beji, Kota Depok, Jawa Barat', '0851-7998-8198', '6285179988198', 'Depok'),
    ('Kantor Tangerang', 'Ruko Ps. Modern No.18 BSD, Rw. Mekar Jaya, Kec. Serpong, Kota Tangerang Selatan, Banten 15318', '0856-9388-3208', '6285693883208', 'Tangerang'),
    ('Kantor Bandung', 'Jl. Bulevar Utama Blok RC No.18, Ruby Commercial – Summarecon Bandung, Kota Bandung, Jawa Barat', '0813-2212-344', '628132212344', 'Bandung'),
    ('Kantor Bogor', 'Ruko Graha Boulevard, Jl. Summarecon Bogor GBVD No.10, Sukatani, Kec. Sukaraja, Kab. Bogor, Jawa Barat 16144', '0822-6012-6394', '6282260126394', 'Bogor'),
]

PERJALANAN = [('2', 'Berangkat', 'Tanah Air ke Jeddah, lanjut Makkah', 'pesawat'), ('3–7', 'Makkah', 'Umroh dan pemantapan manasik di hotel transit', 'kabah'),
              ('8', 'Tarwiyah', 'Menghidupkan sunnah di Mina', 'tenda'), ('9', 'Wukuf', 'Puncak haji di Arafah', 'bulan'),
              ('10', 'Muzdalifah, Mina', 'Mabit, lontar jumrah pertama', 'tenda'), ('11–12', 'Mina', 'Lontar jumrah hari tasyrik', 'tenda'),
              ('13', 'Nafar Tsani', 'Lontar terakhir, kembali ke hotel transit', 'ulang'), ('15', 'Hotel Makkah', 'Ibadah di Masjidil Haram sesuai paket', 'gedung'),
              ('20', 'Tawaf Wada', 'Pamitan ke Baitullah', 'kabah'), ('21–25', 'Madinah', 'Ziarah, Raudhah, dan city tour', 'bulan'),
              ('25', 'Pulang', 'Madinah atau Jeddah ke Jakarta', 'pesawat'), ('26', 'Tiba', 'Kembali di Tanah Air', 'hati')]

BIMBINGAN = [('Manasik camp 5 hari', 'Pesantren singkat manasik, fiqih haji, dan pembinaan akhlak.', 'buku'),
             ('Kajian 5 waktu sholat', 'Pembekalan manasik dan hati selama di Tanah Suci.', 'chat'),
             ('Program Tarwiyah', 'Menghidupkan sunnah di Mina pada 8 Dzulhijjah.', 'tenda'),
             ('Nafar Tsani', 'Bermalam di Mina hingga 13 Dzulhijjah, diisi kajian Hadis Arbain Nawawi.', 'kalender'),
             ('Umroh hingga 3 kali', 'Difasilitasi selama di Makkah, bisa untuk membadalkan keluarga.', 'ulang'),
             ('Tahajjud bersama', 'Pembiasaan sholat malam berjamaah selama di Arab Saudi.', 'bulan'),
             ('Siroh Nabawiyah', 'Pendalaman sejarah Nabi dan sahabat di Madinah.', 'buku'),
             ('Ziarah Raudhah', 'Ziarah Raudhah dan makam Nabi Muhammad ﷺ.', 'hati'),
             ('Kajian bulanan online', 'Pembinaan rutin sebulan sekali selama masa tunggu.', 'kalender')]

LAYANAN = [('Tenda VIP Arafah & Mina', 'Tenda VIP dengan pelayanan maksimal; tenda Mina di Zona 1 dekat pelontaran jumrah.', 'tenda', '2026/10/haji-plus-jamaah-perempuan-tenda-mina.webp'),
           ('1 bus, 3 petugas', 'Setiap bus didampingi tiga petugas profesional yang mengurus kebutuhan jamaah.', 'bus', '2026/10/haji-plus-bus-vip-rombongan.webp'),
           ('Pendamping kesehatan', 'Dokter profesional memantau kesehatan jamaah secara berkala.', 'medis', '2026/10/jamaah-haji-makan-bersama-tenda-jakarta.webp'),
           ('Ramah lansia', 'Layanan asistensi khusus (add-on) untuk jamaah berkebutuhan khusus.', 'hati', '2026/10/jamaah-haji-wanita-penyambutan-bogor.webp')]

PEMBIMBING = [('ahmad-shobirin', 'Ust. Ahmad Shobirin, Lc., MA'), ('muhammad-tahir', 'Ust. Dr. Muhammad Tahir, Lc., MA'),
              ('didi-wibawa', 'Ust. Didi Wibawa, Lc., MA'), ('furqon-abdurrohman', 'Ust. Furqon Abdurrohman, Lc., MA'),
              ('ahmad-husain', 'Ust. Ahmad Husain, Lc., M.Pd'), ('idrus-abidin', 'Ust. Idrus Abidin, Lc., MA'),
              ('zulfahmi-yusuf', 'Ust. Zulfahmi Yusuf, S.Pd.I'), ('ade-abu-yusuf', 'Ust. Ade Abu Yusuf, Lc.')]

LEGAL = ['PIHK SK Kemenag RI No. 846/2020', 'PPIU SK Kemenag No. 63/2020', 'Anggota HIMPUH', 'Anggota IATA', 'Akreditasi A oleh KAN']


# ---------- komponen ----------
def hero(h1, p, kanan, foto_bg, ctas=None):
    ctas = ctas or (btn('Daftar nomor porsi') + f'<a class="hfx-btn line" href="#paket">Lihat 4 paket</a>')
    return (f'<section class="hfx-hero" style="--bg:url({U}{foto_bg})"><div class="hfx-w hfx-hero-in"><div class="hfx-hero-tx">'
            f'<h1>{h1}</h1><p>{p}</p><div class="hfx-ctas">{ctas}</div></div>{kanan}</div></section>')


def ringkasan():
    rows = [('Setoran awal nomor porsi', '4.000 USD'), ('Estimasi masa tunggu', '6–10 tahun'),
            ('Dana manfaat setoran', '± 120 USD / tahun'), ('Harga paket mulai', '12.000 USD')]
    r = ''.join(f'<div><span>{a}</span><b>{b}</b></div>' for a, b in rows)
    return (f'<aside class="hfx-sum"><h2>Ringkasan setoran Haji Khusus</h2><div class="hfx-sum-r">{r}</div>'
            '<p>Pelunasan paket dikurangi DP 4.000 USD dan dana manfaat yang terkumpul selama menunggu. Harga estimasi keberangkatan 2027, naik ±4–5% per tahun.</p>'
            + btn('Tanya simulasi biaya', WA_SIMULASI) + '</aside>')


def legal_strip():
    return '<div class="hfx-legal">' + ''.join(f'<span>{ik("perisai", True)}{t}</span>' for t in LEGAL) + '</div>'


def tabel_banding():
    rows = [('Penyelenggara', 'PIHK berizin (swasta resmi)', 'Pemerintah'), ('Kuota', 'Kuota haji nasional resmi', 'Kuota haji nasional resmi'),
            ('Nomor antrean', 'Antrean Haji Khusus di SISKOHAT', 'Antrean Haji Reguler, terpisah'),
            ('Setoran awal', '4.000 USD', 'Ketentuan pemerintah'), ('Estimasi masa tunggu', '6–10 tahun', 'Jauh lebih lama, tergantung provinsi'),
            ('Pindah porsi', 'Porsi reguler tidak bisa dipindah ke Haji Khusus', '—'),
            ('Pendampingan', 'Pembimbing, petugas bus, dokter, tenda VIP', 'Sesuai layanan pemerintah')]
    tr = ''.join(f'<tr><th>{a}</th><td class="k">{b}</td><td>{c}</td></tr>' for a, b, c in rows)
    return f'<div class="hfx-tbl"><table><thead><tr><th></th><th class="k">Haji Khusus</th><th>Haji Reguler</th></tr></thead><tbody>{tr}</tbody></table></div>'


def hak_jamaah():
    items = [('koin', 'Dana manfaat transparan', 'Setoran 4.000 USD dikelola BPKH dengan instrumen syariah dan bertumbuh ±120 USD per tahun. Di Elharamain, dana ini menjadi hak jamaah dan mengurangi harga paket. Nilainya bisa dicek di aplikasi BPKH.'),
             ('hadiah', 'Voucher umroh Rp 5 juta', 'Selama masa tunggu, jamaah mendapatkan voucher umroh Elharamain Wisata senilai Rp 5 juta. Syarat dan ketentuan berlaku.'),
             ('hati', 'Free Badal Haji', 'Bila calon jamaah wafat sebelum berangkat, InsyaAllah Elharamain memberikan badal haji tanpa biaya, agar niat berhaji tetap terlaksana. Berlaku untuk pendaftar 1448 H, S&amp;K berlaku.'),
             ('buku', 'Kajian bulanan', 'Kajian online rutin sebulan sekali supaya bekal ilmu dan semangat terjaga selama menunggu giliran berangkat.')]
    return '<div class="hfx-g2">' + ''.join(f'<div class="hfx-card">{ik(i)}<div><h3>{t}</h3><p>{d}</p></div></div>' for i, t, d in items) + '</div>'


def langkah():
    st = [('Konsultasi', 'Ceritakan rencana Bapak/Ibu lewat WhatsApp atau datang ke salah satu dari 6 kantor kami.', 'chat'),
          ('Siapkan dokumen', 'KTP, KK, akta kelahiran atau buku nikah, dan pas foto. Paspor bisa menyusul.', 'dokumen'),
          ('Setor 4.000 USD', 'Setoran awal ke rekening resmi atas nama PT Dhiyaa El Haramain El Mubarakah untuk pengambilan nomor porsi.', 'koin'),
          ('Nomor porsi terbit', 'Nomor porsi Haji Khusus tercatat di SISKOHAT atas nama Bapak/Ibu sendiri.', 'perisai'),
          ('Masa tunggu', 'Estimasi 6–10 tahun, diisi kajian bulanan dan voucher umroh Rp 5 juta.', 'kalender'),
          ('Pelunasan &amp; manasik', 'Biaya akhir diinformasikan setahun sebelum berangkat, lalu manasik camp 5 hari.', 'buku')]
    return '<ol class="hfx-tl">' + ''.join(f'<li>{ik(i)}<div><b>Langkah {n}</b><h3>{t}</h3><p>{d}</p></div></li>' for n, (t, d, i) in enumerate(st, 1)) + '</ol>'


def kartu_paket(p, href=None):
    h4, h3, h2 = p['h']
    rows = [('Durasi', p['hari']), ('Hotel Makkah', p['mk']), ('Hotel Madinah', p['md']), ('Hotel transit', p['tr']),
            ('Maskapai', p['fl']), ('Makkah–Madinah', 'Kereta cepat Haramain'), ('Program Arbain', 'Termasuk' if p['arb'] else 'Tidak')]
    li = ''.join(f'<li><span>{a}</span><b{" class=ok" if v == "Termasuk" else ""}>{v}</b></li>' for a, v in rows)
    href = href or wa(f"Assalamu'alaikum, saya ingin tanya Paket Haji Khusus {p['n']} 1448 H.")
    return (f'<div class="hfx-pk"><div class="hfx-pk-h"><h3>Paket {p["n"]}</h3><span>Haji Khusus 1448 H · estimasi berangkat 2027</span></div>'
            f'<div class="hfx-pk-p"><div><small>sekamar 4</small><b>{h4}</b></div><div><small>sekamar 3</small><b>{h3}</b></div>'
            f'<div><small>sekamar 2</small><b>{h2}</b></div></div><small class="usd">USD per jamaah</small><ul>{li}</ul>'
            f'{btn("Tanya paket " + p["n"], href)}</div>')


def paket_grid():
    return '<div class="hfx-pks">' + ''.join(kartu_paket(p) for p in PAKET) + '</div>'


def peta_perjalanan():
    return ('<div class="hfx-trip">' + ''.join(f'<div class="hfx-trip-i">{ik(i, True)}<b>{d} Dzulhijjah</b><h3>{t}</h3><p>{x}</p></div>'
                                              for d, t, x, i in PERJALANAN) + '</div>')


def galeri(fs):
    return '<div class="hfx-gal">' + ''.join(f'<figure>{foto(f, a)}</figure>' for f, a in fs) + '</div>'


def pembimbing():
    return ('<div class="hfx-ust">' + ''.join(f'<figure>{foto(f"2026/10/pembimbing-ust-{s}.webp", n + ", pembimbing ibadah Elharamain Wisata")}'
                                             f'<figcaption>{n}</figcaption></figure>' for s, n in PEMBIMBING) + '</div>')


def kantor():
    out = []
    for nama, alamat, telp, no, kota in KANTOR:
        peta = 'https://www.google.com/maps/search/?api=1&amp;query=' + up.quote(f'Elharamain Wisata {alamat}')
        out.append(f'<div class="hfx-card ktr">{ik("pin")}<div><h3>{nama}</h3><p>{alamat}</p><p class="tel">{ik("telepon", True)}{telp}</p>'
                   f'<div class="hfx-ctas sm">{btn("WhatsApp", f"https://wa.me/{no}?text=" + up.quote(chr(39).join(["Assalamu", f"alaikum Elharamain Wisata {kota}"])))}'
                   f'<a class="hfx-btn line2" href="{peta}" target="_blank" rel="noopener">Petunjuk arah</a></div></div></div>')
    return '<div class="hfx-g3">' + ''.join(out) + '</div>'


def cta(h2='Amankan nomor porsi Haji Khusus Bapak/Ibu', p='Antrean bertambah setiap tahun. Konsultasikan rencana haji keluarga dengan tim kami, gratis dan tanpa kewajiban.'):
    return (f'<section class="hfx-cta"><div class="hfx-w"><h2>{h2}</h2><p>{p}</p><div class="hfx-ctas c">{btn("Konsultasi gratis via WhatsApp")}'
            f'<a class="hfx-btn line" href="{H}/kontak/">Kunjungi kantor</a></div>{legal_strip()}</div></section>')


def sec(isi, kelas='', id_=''):
    i = f' id="{id_}"' if id_ else ''
    return f'<section class="hfx-sec {kelas}"{i}><div class="hfx-w">{isi}</div></section>'


ULASAN = sec(judul('Dipercaya jamaah, dinilai bintang 5 di Google', 'Lebih dari 7.000 ulasan jamaah Elharamain Wisata di Google.')
             + '<div class="hfx-ti">[trustindex no-registration=google]</div>', 'soft', 'ulasan')


# ---------- halaman ----------
def pg_beranda():
    h = hero('Daftar Haji Khusus resmi, nomor porsi atas nama Bapak/Ibu sendiri',
             'Elharamain Wisata adalah Penyelenggara Ibadah Haji Khusus (PIHK) berizin Kemenag RI No. 846/2020. Setoran awal 4.000 USD, '
             'estimasi masa tunggu 6–10 tahun, dan dana manfaat setoran dikembalikan untuk jamaah.', ringkasan(), '2026/10/daftar-haji-khusus-rombongan-masjidil-haram.webp')
    banding = sec('<div class="hfx-2c"><div>' + judul('Beda Haji Khusus dan Haji Reguler',
                  'Haji Khusus memakai kuota haji nasional resmi dengan antrean terpisah dan masa tunggu lebih singkat. Penyelenggaranya swasta yang berizin PIHK.')
                  + tabel_banding() + f'</div><figure class="hfx-ph">{foto("2026/10/haji-khusus-jamaah-ihram-mina.webp", "Jamaah haji khusus Elharamain berihram di Mina")}</figure></div>', '', 'beda')
    hak = sec(judul('Hak jamaah selama masa tunggu', 'Menunggu giliran berangkat tidak berarti menunggu tanpa kepastian.') + hak_jamaah(), 'soft', 'masa-tunggu')
    lk = sec('<div class="hfx-2c rev"><figure class="hfx-ph tall">' + foto('2026/10/daftar-haji-khusus-jamaah-elharamain-manasik.webp', 'Manasik jamaah haji khusus Elharamain')
             + '</figure><div>' + judul('Langkah daftar Haji Khusus', 'Enam langkah dari konsultasi pertama sampai berangkat ke Tanah Suci.') + langkah()
             + f'<div class="hfx-ctas">{btn("Mulai konsultasi")}</div></div></div>', '', 'langkah')
    pk = sec(judul('Empat pilihan Paket Haji Khusus 1448 H', 'Estimasi keberangkatan 2027. Harga per jamaah dalam USD menurut jumlah orang per kamar; seluruh paket memakai tenda VIP Arafah–Mina dan bus VIP.')
             + paket_grid() + '<p class="hfx-note">Biaya paket keseluruhan diinformasikan setahun sebelum keberangkatan. Estimasi kenaikan 4–5% per tahun. '
             f'Rincian lengkap ada di halaman <a href="{H}/layanan/">Layanan</a>.</p>', 'navy', 'paket')
    trip = sec(judul('Perjalanan haji dari 2 sampai 26 Dzulhijjah', 'Gambaran rangkaian perjalanan paket 22–23 hari. Paket Gold Arbain menambah waktu di Madinah.') + peta_perjalanan(), '', 'perjalanan')
    ly = sec(judul('Layanan di Tanah Suci') + '<div class="hfx-g4">' + ''.join(
        f'<div class="hfx-fc">{foto(f, t)}<div>{ik(i)}<h3>{t}</h3><p>{d}</p></div></div>' for t, d, i, f in LAYANAN) + '</div>', 'soft', 'layanan')
    gal = sec(judul('Jamaah Elharamain di Tanah Suci') + galeri([
        ('2026/10/haji-khusus-jamaah-tawaf-malam-kabah.webp', 'Jamaah haji khusus tawaf malam di Ka\'bah'),
        ('2026/10/rombongan-haji-elharamain-ihram-dalam-tenda.webp', 'Rombongan haji Elharamain berihram di dalam tenda'),
        ('2026/10/haji-khusus-jamaah-elharamain-hotel-makkah.webp', 'Jamaah haji khusus di hotel Makkah'),
        ('2026/10/jamaah-haji-stasiun-haramain-jawa-barat.webp', 'Jamaah haji di stasiun kereta Haramain'),
        ('2026/10/haji-khusus-jamaah-ihram-masjid-nabawi-senja.webp', 'Jamaah haji khusus di Masjid Nabawi saat senja'),
        ('2026/10/haji-khusus-rombongan-elharamain-spanduk-tanah-suci.webp', 'Rombongan haji khusus Elharamain di Tanah Suci')]), '', 'galeri')
    tanya = sec(judul('Pertanyaan seputar daftar Haji Khusus') + faq([
        ('Apa itu Haji Khusus atau Haji Plus?', 'Program haji resmi yang memakai kuota haji nasional sesuai UU No. 8 Tahun 2019. Penyelenggaranya pihak swasta berizin PIHK, seperti Elharamain Wisata (SK Kemenag RI No. 846/2020).'),
        ('Berapa setoran awal untuk nomor porsi?', 'Setoran awal 4.000 USD untuk pengambilan nomor porsi. Pembayaran hanya sah ke rekening atas nama PT Dhiyaa El Haramain El Mubarakah.'),
        ('Berapa lama masa tunggu Haji Khusus?', 'Di sistem Kementerian Haji masa tunggu berkisar 10 tahun, namun di lapangan bisa lebih cepat, sekitar 6–10 tahun. Masa tunggu bisa lebih singkat bila ada tambahan kuota dari Arab Saudi.'),
        ('Apakah porsi Haji Reguler bisa dipindah ke Haji Khusus?', 'Tidak bisa, karena alur pendaftaran dan antrean Haji Reguler dan Haji Khusus berbeda.'),
        ('Apa itu dana manfaat setoran haji?', 'Setoran 4.000 USD dikelola BPKH dengan instrumen syariah dan bertumbuh sekitar 120 USD per tahun. Di Elharamain Wisata dana manfaat dikembalikan kepada jamaah sebagai pengurangan harga paket.'),
        ('Berapa kenaikan biaya haji per tahun?', 'Estimasi kenaikan sekitar 4–5% per tahun dari harga tahun sebelumnya. Biaya akhir diinformasikan setahun sebelum keberangkatan.')]), 'soft', 'faq')
    return h + banding + hak + lk + pk + trip + ly + gal + ULASAN + tanya + cta()


def hero_halaman(h1, p, foto_bg, kanan=''):
    return hero(h1, p, kanan, foto_bg, ctas=btn('Konsultasi gratis') + f'<a class="hfx-btn line" href="{H}/kontak/">Alamat kantor</a>').replace('hfx-hero"', 'hfx-hero sm"', 1)


def pg_profil():
    h = hero_halaman('Profil Elharamain Wisata, penyelenggara Haji Khusus resmi Kemenag',
                     'PT Dhiyaa El Haramain El Mubarakah mendampingi jamaah Haji Khusus dan umroh dari 6 kantor di Jabodetabek dan Bandung.',
                     '2026/10/profil-elharamain-keluarga-besar-jamaah-haji-1447h.webp')
    siapa = sec('<div class="hfx-2c"><div>' + judul('Melayani tamu Allah dengan amanah')
                + '<p class="hfx-p">Elharamain Wisata adalah nama dagang PT Dhiyaa El Haramain El Mubarakah, Penyelenggara Ibadah Haji Khusus (PIHK) '
                'berizin SK Kemenag RI No. 846/2020 dan Penyelenggara Perjalanan Ibadah Umrah berizin SK No. 63/2020.</p>'
                '<p class="hfx-p">Kami percaya perjalanan haji adalah momen istimewa yang layak dipersiapkan secara istimewa. Karena itu jamaah didampingi '
                'sejak pendaftaran, selama masa tunggu, di Tanah Suci, sampai kembali ke rumah.</p>' + legal_strip()
                + f'</div><figure class="hfx-ph">{foto("2026/10/kantor-pusat-elharamain-wisata-bekasi.webp", "Kantor pusat Elharamain Wisata di Bekasi")}</figure></div>', '', 'tentang')
    kel = sec(judul('Kelebihan Elharamain Wisata') + '<div class="hfx-g3">' + ''.join(f'<div class="hfx-card">{ik(i)}<div><h3>{t}</h3><p>{d}</p></div></div>' for i, t, d in [
        ('perisai', 'PIHK resmi', 'Terdaftar di Kementerian sehingga keberangkatan jamaah sesuai regulasi.'),
        ('koin', 'DP 4.000 USD', 'Pendaftaran Haji Khusus paling ringan, prosesnya mudah dan cepat.'),
        ('gedung', 'Variasi paket', 'Empat kelas paket yang bisa disesuaikan dengan kebutuhan dan kenyamanan.'),
        ('buku', 'Bimbingan intensif', 'Kurikulum bimbingan yang terarah dan berkelanjutan menuju haji mabrur.'),
        ('hati', 'Free Badal Haji', 'Badal haji tanpa biaya bila calon jamaah wafat sebelum berangkat (S&amp;K berlaku).'),
        ('dokumen', 'Dana manfaat transparan', 'Seluruh manfaat setoran dikembalikan sebagai pengurangan biaya paket.')]) + '</div>', 'soft', 'kelebihan')
    bim = sec(judul('Program bimbingan ibadah', 'Haji adalah perjalanan perubahan hidup. Bimbingan disusun agar jamaah pulang membawa bekal menjadi pribadi yang lebih baik.')
              + '<div class="hfx-g3 list">' + ''.join(f'<div class="hfx-li">{ik(i, True)}<div><h3>{t}</h3><p>{d}</p></div></div>' for t, d, i in BIMBINGAN) + '</div>', '', 'bimbingan')
    ust = sec(judul('Pembimbing ibadah kami', 'Asatidz lulusan Timur Tengah yang mendampingi jamaah dari manasik sampai pulang.') + pembimbing(), 'navy', 'pembimbing')
    gal = sec(judul('Keluarga besar jamaah Elharamain') + galeri([
        ('2026/10/profil-elharamain-jamaah-haji-zamzam-tower.webp', 'Jamaah haji Elharamain di depan Zamzam Tower'),
        ('2026/10/rombongan-haji-elharamain-di-depan-kabah.webp', 'Rombongan haji Elharamain di depan Ka\'bah'),
        ('2026/10/jamaah-haji-elharamain-berangkat-di-bandara.webp', 'Jamaah haji Elharamain berangkat di bandara'),
        ('2026/10/jamaah-haji-1447h-elharamain-di-tenda.webp', 'Jamaah haji 1447 H Elharamain di tenda'),
        ('2026/10/jamaah-haji-masjid-quba-jakarta-utara.webp', 'Jamaah haji di Masjid Quba'),
        ('2026/10/haji-plus-keluarga-besar-jamaah-elharamain.webp', 'Keluarga besar jamaah haji plus Elharamain')]), 'soft', 'galeri')
    return h + siapa + kel + bim + ust + gal + ULASAN.replace(' soft"', '"', 1) + cta()


def pg_layanan():
    h = hero_halaman('Layanan Haji Khusus 1448 H dari nomor porsi sampai kembali ke Tanah Air',
                     'Empat kelas paket, tenda VIP Arafah–Mina, kereta cepat Haramain, dan pendampingan ibadah intensif. Estimasi keberangkatan 2027.',
                     '2026/10/layanan-haji-khusus-jamaah-tawaf-kabah-malam.webp', ringkasan())
    pk = sec(judul('Harga Paket Haji Khusus 1448 H', 'Harga per jamaah dalam USD menurut jumlah orang per kamar. Setoran awal semua paket 4.000 USD.') + paket_grid()
             + '<p class="hfx-note">Biaya pelunasan dikurangi DP 4.000 USD dan dana manfaat (±120 USD per tahun). Biaya keseluruhan diinformasikan setahun '
             'sebelum keberangkatan; estimasi kenaikan 4–5% per tahun.</p>', 'soft', 'paket')
    trip = sec(judul('Rangkaian perjalanan haji', 'Paket 22–23 hari. Gold Arbain 27–28 hari dengan tambahan waktu di Madinah untuk 40 kali sholat berjamaah di Masjid Nabawi.')
               + peta_perjalanan(), '', 'perjalanan')
    ly = sec(judul('Fasilitas dan pendampingan') + '<div class="hfx-g4">' + ''.join(
        f'<div class="hfx-fc">{foto(f, t)}<div>{ik(i)}<h3>{t}</h3><p>{d}</p></div></div>' for t, d, i, f in LAYANAN) + '</div>'
        + '<div class="hfx-g3 list mt">' + ''.join(f'<div class="hfx-li">{ik(i, True)}<div><h3>{t}</h3><p>{d}</p></div></div>' for i, t, d in [
            ('pesawat', 'Penerbangan', 'Saudia, Qatar, atau Emirates; Platinum dengan Saudia atau Garuda Indonesia.'),
            ('kereta', 'Kereta cepat Haramain', 'Perjalanan Makkah–Madinah dengan Haramain High Speed Railway.'),
            ('gedung', 'Hotel transit', 'Jamaah dipersiapkan di hotel transit Makkah sebelum menuju Armuzna.'),
            ('koper', 'Perlengkapan eksklusif', 'Koper bagasi dan kabin, kain ihram, mukena, batik, rompi, dan perlengkapan lain.'),
            ('ulang', 'Umroh hingga 3 kali', 'Difasilitasi selama di Makkah, bisa untuk membadalkan keluarga.'),
            ('bintang', 'Kualitas pelayanan', 'Pelayanan dengan perhatian pada detail, dinilai bintang 5 oleh jamaah.')]) + '</div>', 'navy', 'fasilitas')
    istilah = sec(judul('Istilah yang perlu Bapak/Ibu ketahui') + faq([
        ('Apa itu Tarwiyah?', 'Amalan sunnah pada 8 Dzulhijjah ketika jamaah mulai berihram dan menuju Mina untuk bermalam, pembuka rangkaian menuju wukuf di Arafah.'),
        ('Apa itu Nafar Tsani?', 'Program tetap bermalam di Mina hingga 13 Dzulhijjah, lalu melontar jumrah pada hari itu sebelum meninggalkan Mina.'),
        ('Apa itu hotel transit?', 'Hotel di Makkah tempat jamaah transit sebelum berangkat ke Armuzna, agar lebih fokus menghadapi ibadah inti haji.'),
        ('Apa itu Program Arbain?', 'Ibadah 40 kali sholat fardhu berjamaah berturut-turut di Masjid Nabawi selama di Madinah, tersedia di Paket Gold Arbain.'),
        ('Apa itu Murur?', 'Metode mabit di Muzdalifah dengan melintas setelah wukuf tanpa turun dari kendaraan, lalu langsung menuju Mina atau Masjidil Haram.'),
        ('Apa itu Tanazul?', 'Skema layanan di mana jamaah menginap di hotel sekitar Mina, bukan di tenda, lalu kembali ke Mina untuk melontar jumrah.')]), 'soft', 'istilah')
    return h + pk + trip + ly + istilah + ULASAN.replace(' soft"', '"', 1) + cta()


def pg_kontak():
    h = hero_halaman('Kontak Elharamain Wisata untuk konsultasi Haji Khusus',
                     'Tanyakan paket, nomor porsi, atau dokumen haji lewat WhatsApp, atau datang langsung ke salah satu dari enam kantor kami.',
                     '2026/10/kontak-elharamain-jamaah-depan-kabah-malam.webp')
    ktr = sec(judul('Enam kantor pelayanan', 'Semua kantor melayani konsultasi dan pendaftaran Haji Khusus maupun umroh.') + kantor(), '', 'kantor')
    siap = sec('<div class="hfx-2c"><div>' + judul('Siapkan ini agar konsultasi lebih cepat') + '<ul class="hfx-chk">' + ''.join(
        f'<li>{ik("cek", True)}{t}</li>' for t in ['Scan atau fotokopi KTP dan Kartu Keluarga', 'Akta kelahiran atau buku nikah suami-istri',
                                                     'Pas foto 4x6, cetak atau digital', 'Rencana paket dan tipe kamar bila sudah ada',
                                                     'Setoran awal nomor porsi 4.000 USD per jamaah'])
        + '</ul><p class="hfx-warn">Pembayaran hanya sah ke rekening atas nama <b>PT Dhiyaa El Haramain El Mubarakah</b>. Jangan transfer ke rekening pribadi siapa pun.</p>'
        f'</div><figure class="hfx-ph">{foto("2026/10/kantor-pusat-elharamain-wisata-bekasi.webp", "Kantor pusat Elharamain Wisata Bekasi")}</figure></div>', 'soft', 'dokumen')
    tanya = sec(judul('Pertanyaan seputar konsultasi') + faq([
        ('Apakah konsultasi dikenakan biaya?', 'Tidak. Konsultasi lewat WhatsApp maupun di kantor gratis dan tanpa kewajiban mendaftar.'),
        ('Bisakah mendaftar tanpa datang ke kantor?', 'Bisa. Dokumen dapat dikirim lewat WhatsApp; tim kami memandu proses sampai nomor porsi terbit.'),
        ('Bagaimana memastikan menghubungi kontak resmi?', 'Gunakan nomor yang tercantum di halaman ini dan pastikan pembayaran hanya ke rekening atas nama PT Dhiyaa El Haramain El Mubarakah.'),
        ('Di mana rincian paket dan harga?', f'Rincian empat paket Haji Khusus 1448 H ada di halaman <a href="{H}/layanan/">Layanan</a>.')]), '', 'faq')
    return h + ktr + siap + tanya + ULASAN + cta('Konsultasi Haji Khusus sekarang', 'Ceritakan rencana Bapak/Ibu, tim kami menjawab dengan sabar dan terbuka.')


HALAMAN = {
    'beranda': ('Daftar Haji Khusus Resmi Kemenag', pg_beranda,
                'Daftar haji khusus resmi Kemenag di Elharamain Wisata. Setoran nomor porsi 4.000 USD, estimasi tunggu 6–10 tahun, dana manfaat, dan free badal haji.'),
    'profil': ('Profil', pg_profil, 'Profil Elharamain Wisata, PIHK resmi SK Kemenag RI No. 846/2020 dengan 6 kantor, bimbingan ibadah intensif, dan pembimbing lulusan Timur Tengah.'),
    'layanan': ('Layanan', pg_layanan, 'Layanan dan harga Paket Haji Khusus 1448 H Elharamain Wisata: Silver, Gold, Gold Arbain, Platinum, tenda VIP, kereta cepat Haramain.'),
    'kontak': ('Kontak', pg_kontak, 'Kontak dan alamat 6 kantor Elharamain Wisata di Bekasi, Jakarta, Depok, Tangerang, Bandung, dan Bogor untuk konsultasi Haji Khusus.'),
}

CSS = '''<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style id="hfx">
.hfx{width:100vw;margin-left:calc(50% - 50vw);overflow-x:hidden;--b:#004AAD;--n:#0A2E6B;--l:#1684CF;--s:#9FC9F5;--bg:#F1F6FD;--ink:#0d1f3c;--mu:#4f607b;--ln:#d9e4f3;font-family:Poppins,sans-serif;color:var(--ink);line-height:1.65;font-size:16px}
.hfx *{box-sizing:border-box}.hfx img{max-width:100%;height:auto;display:block}
.hfx h1,.hfx h2,.hfx h3{font-family:Poppins,sans-serif!important;color:var(--ink);margin:0;letter-spacing:-.01em}
.hfx p{margin:0}.hfx a{color:var(--b)}
.hfx-w{max-width:1180px;margin:0 auto;padding:0 20px}
.hfx-sec{padding:76px 0;background:#fff}.hfx-sec.soft{background:var(--bg)}
.hfx-sec.navy{background:var(--n)}.hfx-sec.navy h2,.hfx-sec.navy .hfx-hd p,.hfx-sec.navy .hfx-note{color:#fff}.hfx-sec.navy .hfx-hd h2::before{background:var(--s)}
.hfx-hd{max-width:760px;margin-bottom:34px}
.hfx-hd h2{font-size:clamp(26px,3.2vw,36px);font-weight:700;line-height:1.22;position:relative;padding-top:18px}
.hfx-hd h2::before{content:"";position:absolute;left:0;top:0;width:56px;height:5px;background:var(--b)}
.hfx-hd p{margin-top:12px;color:var(--mu);font-size:16.5px}
.hfx-p{color:var(--mu);margin-bottom:14px}
.hfx-ic{flex:none;width:54px;height:54px;border-radius:50%;background:var(--b);display:grid;place-items:center;box-shadow:0 0 0 6px rgba(0,74,173,.1)}
.hfx-ic svg{width:26px;height:26px;fill:#fff}
.hfx-ic.s{width:34px;height:34px;box-shadow:0 0 0 4px rgba(0,74,173,.1)}.hfx-ic.s svg{width:17px;height:17px}
.hfx-btn{display:inline-flex;align-items:center;gap:8px;justify-content:center;padding:13px 22px;border-radius:4px;font:600 15px Poppins,sans-serif;text-decoration:none!important;border:2px solid transparent;transition:background .2s,transform .2s}
.hfx-btn:hover{transform:translateY(-1px)}.hfx-btn svg{width:18px;height:18px;fill:currentColor}
.hfx-btn.wa{background:#1fa855;color:#fff!important}.hfx-btn.wa:hover{background:#178a45}
.hfx-btn.line{border-color:#fff;color:#fff!important}.hfx-btn.line:hover{background:rgba(255,255,255,.12)}
.hfx-btn.line2{border-color:var(--b);color:var(--b)!important;background:#fff}
.hfx-ctas{display:flex;gap:12px;flex-wrap:wrap;margin-top:26px}.hfx-ctas.c{justify-content:center}.hfx-ctas.sm{margin-top:14px}.hfx-ctas.sm .hfx-btn{padding:9px 14px;font-size:14px}
.hfx-hero{position:relative;color:#fff;padding:170px 0 90px;background:linear-gradient(90deg,rgba(10,46,107,.97) 0%,rgba(10,46,107,.88) 46%,rgba(0,74,173,.55) 100%),var(--bg) center/cover no-repeat}
.hfx-hero.sm{padding:160px 0 70px}
.hfx-hero-in{display:grid;grid-template-columns:1.25fr .9fr;gap:48px;align-items:center}
.hfx-hero h1{color:#fff!important;font-size:clamp(32px,4.6vw,52px);font-weight:800;line-height:1.12}
.hfx-hero p{color:rgba(255,255,255,.88);font-size:17px;margin-top:18px;max-width:620px}
.hfx-sum{background:#fff;color:var(--ink);border-radius:4px;padding:26px;border-top:6px solid var(--l);box-shadow:0 24px 60px rgba(0,0,0,.3)}
.hfx-sum h2{font-size:19px;font-weight:700;margin-bottom:12px}
.hfx-sum-r div{display:flex;justify-content:space-between;gap:12px;padding:11px 0;border-bottom:1px solid var(--ln);font-size:14.5px}
.hfx-sum-r span{color:var(--mu)}.hfx-sum-r b{color:var(--b);font-weight:700;text-align:right}
.hfx-sum p{font-size:13px;color:var(--mu);margin:14px 0 16px}.hfx-sum .hfx-btn{width:100%}
.hfx-2c{display:grid;grid-template-columns:1.2fr .8fr;gap:44px;align-items:center}.hfx-2c.rev{grid-template-columns:.8fr 1.2fr}
.hfx-ph{margin:0}.hfx-ph img{width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:4px;box-shadow:16px 16px 0 var(--s)}
.hfx-ph.tall img{aspect-ratio:3/4}
.hfx-tbl{overflow-x:auto;border:1px solid var(--ln)}
.hfx-tbl table{width:100%;border-collapse:collapse;font-size:14.5px;min-width:560px}
.hfx-tbl th,.hfx-tbl td{padding:13px 16px;border-bottom:1px solid var(--ln);text-align:left;vertical-align:top}
.hfx-tbl thead th{background:var(--n);color:#fff;font-weight:600}.hfx-tbl thead th.k{background:var(--b)}
.hfx-tbl tbody th{color:var(--mu);font-weight:500;width:28%}.hfx-tbl td.k{background:#eaf2ff;color:var(--n);font-weight:600}
.hfx-g2{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}.hfx-g3{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.hfx-g4{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.hfx-g3.mt{margin-top:22px}
.hfx-card{display:flex;gap:18px;background:#fff;border:1px solid var(--ln);border-left:5px solid var(--b);border-radius:4px;padding:24px}
.hfx-card h3{font-size:18px;font-weight:700;margin-bottom:6px}.hfx-card p{color:var(--mu);font-size:14.5px}
.hfx-card.ktr p{margin-bottom:6px}.hfx-card .tel{display:flex;align-items:center;gap:10px;color:var(--ink)!important;font-weight:600}
.hfx-tl{list-style:none;margin:0;padding:0;position:relative}
.hfx-tl::before{content:"";position:absolute;left:26px;top:10px;bottom:10px;width:3px;background:var(--s)}
.hfx-tl li{position:relative;display:flex;gap:20px;padding:0 0 22px}
.hfx-tl b{display:block;font-size:12.5px;color:var(--l);font-weight:600}.hfx-tl h3{font-size:18px;font-weight:700}.hfx-tl p{color:var(--mu);font-size:14.5px}
.hfx-pks{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.hfx-pk{background:#fff;border-radius:4px;display:flex;flex-direction:column;overflow:hidden}
.hfx-pk-h{background:var(--b);color:#fff;padding:20px}.hfx-pk:nth-child(2) .hfx-pk-h{background:var(--l)}.hfx-pk:nth-child(3) .hfx-pk-h{background:#0b5cc4}.hfx-pk:nth-child(4) .hfx-pk-h{background:#071f4d}
.hfx-pk-h h3{color:#fff!important;font-size:21px;font-weight:700}.hfx-pk-h span{font-size:12.5px;color:rgba(255,255,255,.82)}
.hfx-pk-p{display:grid;grid-template-columns:repeat(3,1fr);border-bottom:1px solid var(--ln)}
.hfx-pk-p div{padding:12px 6px;text-align:center;border-right:1px solid var(--ln)}.hfx-pk-p div:last-child{border-right:0}
.hfx-pk-p div:first-child{background:#eaf2ff}
.hfx-pk-p small{display:block;font-size:11px;color:var(--mu)}.hfx-pk-p b{font-size:18px;font-weight:800;color:var(--n)}
.hfx-pk .usd{display:block;text-align:center;font-size:12px;color:var(--mu);padding:6px 0 0}
.hfx-pk ul{list-style:none;margin:8px 18px 18px;padding:0;flex:1}
.hfx-pk li{display:grid;grid-template-columns:42% 58%;gap:8px;padding:8px 0;border-bottom:1px dashed var(--ln);font-size:13.5px}
.hfx-pk li span{color:var(--mu)}.hfx-pk li b{font-weight:600}.hfx-pk li b.ok{color:#178a45}
.hfx-pk .hfx-btn{margin:0 18px 18px}
.hfx-note{margin-top:18px;font-size:13.5px;color:var(--mu)}.hfx-sec.navy .hfx-note a{color:var(--s)}
.hfx-trip{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(190px,1fr);gap:0;overflow-x:auto;padding:8px 2px 14px;scroll-snap-type:x mandatory;margin-top:10px;background:linear-gradient(var(--s),var(--s)) 0 24px/100% 3px no-repeat}
.hfx-trip-i{scroll-snap-align:start;padding:0 16px 0 0;position:relative}
.hfx-trip-i .hfx-ic{background:var(--b);position:relative}
.hfx-trip-i b{display:block;margin-top:12px;font-size:12.5px;color:var(--l);font-weight:700}.hfx-trip-i h3{font-size:16.5px;font-weight:700}.hfx-trip-i p{font-size:13.5px;color:var(--mu)}
.hfx-fc{background:#fff;border-radius:4px;overflow:hidden;border:1px solid var(--ln)}
.hfx-fc img{width:100%;aspect-ratio:4/3;object-fit:cover}.hfx-fc>div{padding:0 20px 22px}
.hfx-fc .hfx-ic{margin-top:-27px;border:4px solid #fff;box-shadow:none}.hfx-fc h3{font-size:17px;font-weight:700;margin:10px 0 6px}.hfx-fc p{color:var(--mu);font-size:14px}
.hfx-sec.navy .hfx-li h3{color:#fff}.hfx-sec.navy .hfx-li p{color:rgba(255,255,255,.78)}.hfx-sec.navy .hfx-li .hfx-ic{background:var(--l)}
.hfx-li{display:flex;gap:14px;align-items:flex-start}.hfx-li h3{font-size:16px;font-weight:700}.hfx-li p{font-size:14px;color:var(--mu)}
.hfx-gal{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.hfx-gal figure{margin:0}.hfx-gal img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:4px}

.hfx-ust{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.hfx-ust figure{margin:0;background:#fff;border-radius:4px;overflow:hidden}.hfx-ust img{width:100%;aspect-ratio:4/5;object-fit:cover;object-position:top}
.hfx-ust figcaption{padding:12px;font-size:14px;font-weight:600;text-align:center;color:var(--ink)}
.hfx-faq{max-width:860px;display:grid;gap:10px}
.hfx-faq-i{background:#fff;border:1px solid var(--ln);border-left:5px solid var(--b);border-radius:4px;padding:2px 20px}
.hfx-faq-i summary{cursor:pointer;list-style:none;padding:15px 30px 15px 0;font-weight:600;position:relative}
.hfx-faq-i summary::-webkit-details-marker{display:none}
.hfx-faq-i summary::after{content:"+";position:absolute;right:0;top:9px;font-size:26px;color:var(--b);font-weight:500}
.hfx-faq-i[open] summary::after{content:"–"}.hfx-faq-i p{color:var(--mu);padding:0 0 16px;font-size:15px}
.hfx-chk{list-style:none;margin:0 0 18px;padding:0;display:grid;gap:10px}.hfx-chk li{display:flex;gap:12px;align-items:center}
.hfx-warn{background:#eaf2ff;border-left:5px solid var(--b);padding:14px 18px;font-size:14.5px}
.hfx-legal{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}
.hfx-legal span{display:inline-flex;align-items:center;gap:10px;background:#fff;border:1px solid var(--ln);border-radius:4px;padding:6px 14px 6px 6px;font-size:13.5px;font-weight:600;color:var(--n)}
.hfx-legal .hfx-ic.s{width:28px;height:28px;box-shadow:none}.hfx-legal .hfx-ic.s svg{width:15px;height:15px}
.hfx-cta{background:linear-gradient(120deg,var(--b),var(--n));padding:70px 0;text-align:center;color:#fff}
.hfx-cta h2{color:#fff!important;font-size:clamp(26px,3.2vw,36px);font-weight:700}.hfx-cta p{color:rgba(255,255,255,.88);margin:12px auto 0;max-width:640px}
.hfx-cta .hfx-legal{justify-content:center;margin-top:30px}.hfx-cta .hfx-legal span{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.25);color:#fff}
.hfx-ti{margin-top:10px}
@media(max-width:1024px){.hfx-pks,.hfx-g4,.hfx-ust{grid-template-columns:repeat(2,1fr)}.hfx-g3{grid-template-columns:repeat(2,1fr)}}
@media(max-width:820px){.hfx-hero-in,.hfx-2c,.hfx-2c.rev{grid-template-columns:1fr}.hfx-hero{padding:130px 0 60px}.hfx-ph img{box-shadow:10px 10px 0 var(--s)}}
@media(max-width:620px){.hfx-sec{padding:54px 0}.hfx-pks,.hfx-g2,.hfx-g3,.hfx-g4{grid-template-columns:1fr}.hfx-ust{grid-template-columns:repeat(2,1fr)}
.hfx-gal{grid-template-columns:1fr 1fr}.hfx-card{padding:20px}.hfx-ctas .hfx-btn{width:100%}}
</style>'''

META = {'site-sidebar-layout': 'no-sidebar', 'site-content-layout': 'page-builder', 'ast-site-content-layout': 'full-width-container',
        'site-post-title': 'disabled', 'ast-featured-img': 'disabled', 'theme-transparent-header-meta': 'enabled'}


def bangun(slug):
    return f'<!-- wp:html -->\n{CSS}\n<div class="hfx">{HALAMAN[slug][1]()}</div>\n<!-- /wp:html -->\n'


def hf(method, path, data=None):
    auth = 'Basic ' + base64.b64encode(f"{os.environ['WP_HAJIFURODA_USER']}:{os.environ['WP_HAJIFURODA_PASS']}".encode()).decode()
    cmd = ['curl', '-sS', '-L', '-X', method, '-H', 'Authorization: ' + auth, '-H', 'User-Agent: Mozilla/5.0 eh-admin',
           '-H', 'Content-Type: application/json', '-w', '\n%{http_code}', H + '/wp-json' + path]
    if data is not None:
        cmd[1:1] = ['--data-binary', '@-']
    out = subprocess.run(cmd, input=json.dumps(data).encode() if data is not None else None, capture_output=True).stdout.decode('utf-8', 'replace')
    body, code = out.rsplit('\n', 1)
    k = body.find('{"')
    try:
        return int(code), json.loads(body[k:] if k > 0 else body)
    except ValueError:
        return int(code), body[:300]


DRAFT_AWAL = {'profil': 28381, 'layanan': 28380, 'kontak': 28382}  # draft -baru buatan Agen Paket, diisi ulang

if __name__ == '__main__':
    pilih = [a for a in sys.argv[1:] if not a.startswith('--')] or list(HALAMAN)
    os.makedirs(DIR, exist_ok=True)
    for slug in pilih:
        konten = bangun(slug)
        open(os.path.join(DIR, f'{slug}.html'), 'w', encoding='utf-8').write(konten)
        print('tulis', slug, len(konten))
        if '--draft' in sys.argv:
            idf = os.path.join(DIR, f'{slug}.draft-id')
            pid = open(idf).read().strip() if os.path.exists(idf) else str(DRAFT_AWAL.get(slug, ''))
            data = {'title': HALAMAN[slug][0], 'content': konten, 'excerpt': HALAMAN[slug][2], 'status': 'draft', 'template': '', 'meta': META}
            if not pid:
                data['slug'] = f'{slug}-unik'
            s, r = hf('POST', f'/wp/v2/pages/{pid}' if pid else '/wp/v2/pages', data)
            if s not in (200, 201) or not isinstance(r, dict):
                sys.exit(f'{slug}: gagal simpan draft {s} {str(r)[:200]}')
            open(idf, 'w').write(str(r['id']))
            print('  draft', r['id'], s)
