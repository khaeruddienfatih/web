"""Desain ulang halaman-halaman haji.biz (selain beranda 197) dengan gaya baru (.ehc/.ehb/.ehj, ikon 3D, font Martel/Mulish).
Permintaan pemilik 2026-11-04 ("semua page"). Isi diambil dari halaman asli (cadangan: backup/2026-11-04_hajibiz_pages/).
Tiap halaman dibuat sebagai DRAFT halaman baru; halaman asli belum disentuh sampai pemilik setuju.

  python3 tools/build_hajibiz_pages.py [slug ...]            -> tulis landing-pages/situs/haji-biz/<slug>.html
  python3 tools/build_hajibiz_pages.py --draft [slug ...]    -> + buat/perbarui Draft (ID di <slug>.draft-id)
slug: paket-haji-plus, haji-plus-2027, haji-plus-2028, tentang-kami, lokasi-kantor, galeri-haji
Kredensial: env WP_USER/WP_APP_PASSWORD (ambil CSS dasar dari elharamainwisata.com) & WP_HAJIBIZ_USER/WP_HAJIBIZ_PASS."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import build_hajibiz_home as H

ROOT = H.ROOT
DIR = os.path.join(ROOT, 'landing-pages', 'situs', 'haji-biz')
U, CTA, WA, DETAIL = H.U, H.CTA, H.WA, H.DETAIL
ik, card, btn = H.ik, H.card, H.btn

KANTOR = [  # dari halaman Lokasi Kantor (793)
    ('Kantor Pusat Bekasi', 'Ruko Emerald No.5 Blok EB 1, Jl. Harapan Indah Raya, Kec. Medan Satria, Kota Bekasi, Jawa Barat 17132', '0812-8729-2422', '6281287292422', 'Bekasi'),
    ('Kantor Jakarta', 'Jl. Tebet Raya No.39 B, Tebet Timur, Kec. Tebet, Kota Jakarta Selatan, DKI Jakarta 12820', '0812-1417-8056', '6281214178056', 'Jakarta'),
    ('Kantor Depok', 'Jl. Margonda No.252 D, Kemiri Muka, Kec. Beji, Kota Depok, Jawa Barat', '0851-7998-8198', '6285179988198', 'Depok'),
    ('Kantor Tangerang', 'Ruko Ps. Modern No.18 BSD, Rw. Mekar Jaya, Kec. Serpong, Kota Tangerang Selatan, Banten 15318', '0856-9388-3208', '6285693883208', 'Tangerang'),
    ('Kantor Bandung', 'Jl. Bulevar Utama Blok RC No.18, Ruby Commercial – Summarecon Bandung, Kota Bandung, Jawa Barat', '0813-2212-344', '628132212344', 'Bandung'),
    ('Kantor Bogor', 'Ruko Graha Boulevard, Jl. Summarecon Bogor GBVD No.10, Sukatani, Kec. Sukaraja, Kab. Bogor, Jawa Barat 16144', '0822-6012-6394', '6282260126394', 'Bogor'),
]


def kantor_html():
    import urllib.parse as up
    out = []
    for nama, alamat, telp, wa, kota in KANTOR:
        peta = 'https://www.google.com/maps/search/?api=1&query=' + up.quote(f'Elharamain Wisata {alamat}')
        pesan = up.quote(f"Assalamu'alaikum Elharamain Wisata {kota}")
        out.append(f'<div class="ehb-card hb-ktr">{ik("kantor-cabang")}<h3>{nama}</h3><p>{alamat}</p>'
                   f'<p class="tel">Telp/WA <b>{telp}</b></p><div class="hb-ktr-b">'
                   f'<a class="ehb-btn wa" href="https://wa.me/{wa}?text={pesan}" target="_blank" rel="noopener"><i class="ehb-wa"></i> WhatsApp</a>'
                   f'<a class="ehb-btn ghost2" href="{peta}" target="_blank" rel="noopener">Lihat peta</a></div></div>')
    return '<div class="ehb-g3">' + ''.join(out) + '</div>'


def hero(pill, h1, p, kanan='', ctas=None):
    ctas = ctas or btn('<i class="ehb-wa"></i> Konsultasi Gratis', 'wa')
    return (f'<section class="ehb-hero hb-hero hb-hero-s"><div class="ehc-wrap ehb-hero-in"><div class="ehb-hero-tx">'
            f'<span class="ehb-pill">{pill}</span><h1>{h1}</h1><p>{p}</p><div class="ehc-ctas">{ctas}</div></div>{kanan}</div></section>')


def promo3(kelas='ehb-up ehb-pt0'):
    return (f'<section class="ehb-sec {kelas}"><div class="ehc-wrap"><div class="ehb-g3">'
            + card('satu-rekening', 'Setoran awal 4.000 USD', 'Untuk pengambilan nomor porsi resmi; dana masuk langsung ke Kementerian, bukan ke travel.')
            + card('pendaftar-haji', 'Jaminan berangkat', 'Setiap jamaah mendapatkan nomor porsi resmi di sistem SISKOHAT.')
            + card('booking-seat', 'Promo voucher umroh Rp 5 juta', 'Bonus voucher umroh untuk dipakai selama masa tunggu keberangkatan haji.')
            + '</div></div></section>')


def paket_sec(judul, lead, label='Haji Plus 1448 H', catatan=''):
    pk = []
    for p in H.PAKET:
        html = H.paket_html(p).replace('Haji Plus 1448 H', label)
        html = html.replace(f'href="{DETAIL}"', f'href="{CTA}" target="_blank" rel="noopener"').replace('>Lihat detail paket<', '>Konsultasi paket ini<')
        pk.append(html)
    cat = f'<div class="hb-cat">{catatan}</div>' if catatan else ''
    return (f'<section class="ehb-sec ehb-soft" id="paket"><div class="ehc-wrap"><span class="ehb-kick">Pilihan paket</span>'
            f'<h2>{judul}</h2><p class="ehb-lead">{lead}</p>{cat}<div class="ehj-pks">{"".join(pk)}</div></div></section>')


def ajakan():
    return ('<section class="ehb-sec ehb-dark" id="ajakan"><div class="ehc-wrap hb-ajak"><span class="ehb-kick">Paket Haji Plus</span>'
            '<h2>Lebih cepat, lebih nyaman, dan lebih khusyuk beribadah</h2>'
            '<p>Jangan menunda panggilan Allah. Setiap tahun antrean semakin panjang dan biaya terus meningkat. Semakin cepat mendaftar, '
            'semakin cepat peluang berangkat ke Baitullah.</p><div class="ehc-ctas ehj-c">'
            + btn('<i class="ehb-wa"></i> Konsultasi Gratis', 'wa') + '</div></div></section>')


def apa_itu(kelas=''):
    return (f'<section class="ehb-sec {kelas}" id="apa-itu"><div class="ehc-wrap ehj-2c rev"><figure class="hb-sq"><img loading="lazy" '
            f'src="{U}2026/01/4-16.webp" alt="Ka\'bah, tujuan ibadah haji"></figure><div><span class="ehb-kick">Mengenal Haji Plus</span>'
            '<h2>Apa itu Haji Khusus atau Haji Plus?</h2><p>Program haji resmi yang menggunakan kuota haji nasional / Pemerintah RI, sesuai '
            'UU No. 8 Tahun 2019 tentang Penyelenggaraan Ibadah Haji dan Umrah.</p><p>Penyelenggara Haji Khusus/Plus adalah pihak swasta '
            'yang telah diberi izin sebagai Penyelenggara Ibadah Haji Khusus (PIHK) oleh Kementerian Haji dan Umrah. Elharamain Wisata '
            'terdaftar sebagai PIHK dengan SK No. 846/2020.</p></div></div></section>')


def ulasan(kelas='ehb-soft'):
    return (f'<section class="ehb-sec {kelas}" id="ulasan-jamaah"><div class="ehc-wrap"><span class="ehb-kick">Testimoni jamaah</span>'
            '<h2>Bintang 5 dari 7.000+ ulasan Google</h2><div class="hb-ti">[trustindex no-registration=google]</div></div></section>')


# ------------------------------------------------------------------ halaman
def pg_paket_haji_plus():
    s = H.SEKSI.replace('<h1>Berangkat haji lebih pasti bersama <em>Elharamain Wisata</em></h1>',
                        '<h1>Paket Haji Plus resmi, <em>masa tunggu 8–10 tahun</em></h1>')
    return s


def pg_haji_plus(tahun):
    is28 = tahun == 2028
    catatan = ('<b>Catatan:</b> harga di bawah adalah harga acuan untuk estimasi keberangkatan 2027. Untuk estimasi keberangkatan 2028, '
               'harga diperkirakan naik sekitar 4–5% dari harga tahun sebelumnya (sesuai kebijakan resmi Elharamain Wisata) dan detailnya '
               'diinformasikan 6–12 bulan sebelum keberangkatan. Estimasi waiting list jamaah untuk keberangkatan 2028: sekitar 120 jamaah.') if is28 else ''
    h = hero(f'Haji Plus · estimasi keberangkatan {tahun}',
             f'Pilihan Paket Haji Plus <em>{tahun}</em> Elharamain Wisata',
             'Setiap jamaah memiliki kebutuhan dan kondisi yang berbeda. Seluruh paket memakai porsi resmi, fasilitas terbaik sesuai kelasnya, '
             'serta pendampingan ibadah intensif dari awal hingga akhir perjalanan.',
             ctas=btn('<i class="ehb-wa"></i> Konsultasi Gratis', 'wa') + '<a class="ehb-btn glass" href="#paket">Lihat 4 paket</a>')
    pk = paket_sec(f'4 paket Haji Plus {"(estimasi 2028)" if is28 else "1448 H"}',
                   'Harga per jamaah dalam USD menurut jumlah orang per kamar. Semua paket dengan tenda VIP di Arafah–Mina, bus, dan kereta cepat Haramain.',
                   label='Estimasi 2028' if is28 else 'Haji Plus 1448 H', catatan=catatan)
    lain = ('<p class="ehb-note ehj-c">' + ('Lihat juga <a href="https://haji.biz/paket-haji-plus-2027-elharamain-wisata/">Paket Haji Plus 2027</a>.'
            if is28 else 'Lihat juga <a href="https://haji.biz/paket-haji-plus-2028-elharamain-wisata/">Paket Haji Plus 2028</a>.') + '</p>')
    return h + promo3() + pk.replace('</div></section>', lain + '</div></section>', 1) + ajakan() + apa_itu() + ulasan()


def pg_tentang_kami():
    h = hero('PT Dhiyaa El Haramain El Mubarakah', 'Tentang <em>Elharamain Wisata</em>',
             'Penyelenggara Ibadah Haji Khusus (PIHK) resmi yang berkomitmen mendampingi umat Muslim menunaikan rukun Islam kelima '
             'dengan proses yang aman, nyaman, dan sesuai tuntunan syariat.')
    tentang = (f'<section class="ehb-sec" id="tentang"><div class="ehc-wrap ehj-2c"><div><span class="ehb-kick">Tentang kami</span>'
               '<h2>Mitra ibadah, bukan sekadar penyelenggara perjalanan</h2><p>Di bawah naungan PT Dhiyaa El Haramain El Mubarakah, kami hadir '
               'bukan hanya sebagai penyelenggara perjalanan, tetapi sebagai mitra ibadah yang menjaga niat suci jamaah sejak pendaftaran '
               'hingga kembali ke Tanah Air.</p></div>'
               f'<figure class="ehj-foto"><img loading="lazy" src="{U}2026/01/1-5.webp" '
               'alt="Jamaah dan tim Elharamain Wisata"></figure></div></section>')
    legal = ('<section class="ehb-sec ehb-soft" id="legalitas"><div class="ehc-wrap"><span class="ehb-kick">Legalitas &amp; kepercayaan</span>'
             '<h2>Terdaftar dan berizin resmi</h2><p class="ehb-lead">Elharamain Wisata terdaftar dan berizin resmi sebagai Penyelenggara Ibadah '
             'Haji Khusus (PIHK) dengan SK Kemenag RI No. 846 Tahun 2020.</p><div class="ehb-g3">'
             + card('izin-resmi', 'SK Kemenag RI No. 846/2020', 'Izin resmi sebagai Penyelenggara Ibadah Haji Khusus (PIHK).')
             + card('pendaftar-haji', 'Nomor porsi di SISKOHAT', 'Setiap jamaah mendapatkan nomor porsi resmi di sistem SISKOHAT.')
             + card('satu-rekening', 'Aman &amp; transparan', 'Wujud komitmen kami terhadap keamanan, transparansi, dan kepastian keberangkatan.')
             + '</div></div></section>')
    visi = ('<section class="ehb-sec ehb-dark" id="visi-misi"><div class="ehc-wrap"><span class="ehb-kick">Visi &amp; misi</span>'
            '<h2>Amanah, profesional, dan terpercaya</h2><div class="hb-visi"><b>Visi</b><p>Menjadi penyelenggara Haji Plus yang amanah, '
            'profesional, dan terpercaya dalam melayani tamu Allah SWT.</p></div><div class="ehb-g4">'
            + card('beribadah', 'Sesuai syariat', 'Menyelenggarakan ibadah haji sesuai syariat dan regulasi resmi pemerintah.')
            + card('reputasi', 'Jujur &amp; transparan', 'Memberikan pelayanan yang jujur, transparan, dan bertanggung jawab.')
            + card('asatidz', 'Bimbingan berkesinambungan', 'Mendampingi jamaah dengan bimbingan ibadah yang intensif dan berkesinambungan.')
            + card('hotel-bintang', 'Fasilitas terbaik', 'Menghadirkan fasilitas terbaik demi kenyamanan dan kekhusyukan ibadah.')
            + '</div></div></section>')
    makna = (f'<section class="ehb-sec" id="makna"><div class="ehc-wrap ehj-2c rev"><figure class="hb-sq"><img loading="lazy" src="{U}2026/01/5-12.webp" '
             'alt="Menara jam Makkah"></figure><div><span class="ehb-kick">Lebih dari sekadar perjalanan</span><h2>Perjalanan ruhani menuju ridha Allah</h2>'
             '<p>Bagi kami, haji bukan sekadar perjalanan fisik menuju Baitullah, tetapi perjalanan ruhani menuju ridha Allah SWT.</p>'
             '<div class="ehc-ctas">' + btn('Lihat paket Haji Plus', 'pri', 'https://haji.biz/paket-haji-plus/', baru=False) + '</div></div></div></section>')
    ktr = ('<section class="ehb-sec ehb-soft" id="kantor"><div class="ehc-wrap"><span class="ehb-kick">Alamat kantor</span>'
           '<h2>6 kantor pelayanan Elharamain Wisata</h2>' + kantor_html() + '</div></section>')
    return h + tentang + legal + visi + makna + ktr + ulasan('')


def pg_lokasi_kantor():
    h = hero('Jabodetabek &amp; Bandung', 'Lokasi <em>kantor kami</em>',
             'Kunjungi kantor Elharamain Wisata terdekat untuk konsultasi langsung. Semua kantor melayani pendaftaran Haji Plus.')
    ktr = ('<section class="ehb-sec" id="kantor"><div class="ehc-wrap"><span class="ehb-kick">6 kantor pelayanan</span>'
           '<h2>Pilih kantor terdekat dari Anda</h2>' + kantor_html()
           + '<p class="ehb-note">PT Dhiyaa El Haramain El Mubarakah · Izin Haji Plus (PIHK) SK Kemenag No. 846 Tahun 2020.</p></div></section>')
    return h + ktr + ulasan()


GALERI = [f'{U}2026/01/{n}.webp' for n in (  # 14 foto yang tampil di galeri asli (238), urutan sama
    '31', '17', '9-3', '7-3', '8-3', '22', '30-1', '32', '10-2', '21', '5-1', '11-2', '27-1', '24-1')]
GALERI += [U + x for x in (  # tambahan dari Media haji.biz (foto jamaah Elharamain), dipilih 2026-11-04
    '2026/09/jamaah-haji-mekkah-2-scaled.webp',
    '2026/09/jamaah-haji-mekkah-1-scaled.webp',
    '2026/09/jamaah-haji-doa-bersama-scaled.webp',
    '2026/09/jamaah-haji-tenda-mina-scaled.webp',
    '2026/09/jamaah-haji-kabah-malam-scaled.webp',
    '2026/01/WhatsApp-Image-2025-06-06-at-14.39.47_5481698c-scaled-1.jpg',
    '2026/01/WhatsApp-Image-2025-06-10-at-22.28.40_399f5fd8-scaled-1.jpg',
    '2026/01/23.webp',
    '2026/01/19.webp',
    '2026/01/27-2.webp',
    '2026/01/4-5.webp',
    '2026/01/3-5.webp',
    '2026/01/2-5.webp',
    '2026/01/1-5.webp',
    '2026/01/29.webp',
    '2026/01/28.webp',
    '2026/01/27.webp',
    '2026/01/26.webp',
    '2026/01/25.webp',
    '2026/01/24.webp',
    '2026/01/30.webp',
    '2026/01/9-3-1.webp',
    '2026/01/11-4-1.webp',
    '2026/01/7-8-1.webp',
    '2026/01/5-8-1.webp',
    '2026/01/3-5-1.webp',
    '2026/01/8-2-2.webp',
    '2026/01/4-5-1.webp')]


def pg_galeri_haji():
    h = hero('Galeri jamaah', 'Jejak langkah <em>tamu Allah</em> di Tanah Suci',
             'Setiap foto adalah saksi perjalanan iman: momen kebersamaan jamaah Elharamain Wisata saat menunaikan ibadah haji, '
             'pengingat bahwa Allah telah memanggil dan memuliakan hamba-Nya.')
    foto = ''.join(f'<a href="{u}" target="_blank" rel="noopener"><img loading="lazy" src="{u}" alt="Galeri jamaah haji Elharamain Wisata"></a>' for u in GALERI)
    gal = ('<section class="ehb-sec" id="galeri"><div class="ehc-wrap"><span class="ehb-kick">Dokumentasi</span><h2>Momen jamaah Elharamain Wisata</h2>'
           f'<p class="ehb-lead">Klik foto untuk melihat ukuran penuh.</p><div class="hb-gal">{foto}</div></div></section>')
    return h + gal + ajakan() + ulasan()


HALAMAN = {
    'paket-haji-plus': ('Paket Haji Plus (desain baru)', pg_paket_haji_plus),
    'haji-plus-2027': ('Paket Haji Plus 2027 (desain baru)', lambda: pg_haji_plus(2027)),
    'haji-plus-2028': ('Paket Haji Plus 2028 (desain baru)', lambda: pg_haji_plus(2028)),
    'tentang-kami': ('Tentang Kami (desain baru)', pg_tentang_kami),
    'lokasi-kantor': ('Lokasi Kantor (desain baru)', pg_lokasi_kantor),
    'galeri-haji': ('Galeri Haji (desain baru)', pg_galeri_haji),
}

CSS_PAGES = '''<style id="hb-pages">
.hb-hero-s{padding-bottom:64px}
.hb-hero-s .ehb-hero-tx{max-width:760px}
.ehb .ehb-up.ehb-pt0 .ehb-g3{margin-top:-28px;position:relative}
.ehb-btn.ghost2{background:#fff;color:var(--bl)!important;border-color:var(--ln)}
.hb-ktr{gap:2px}
.hb-ktr p{margin:4px 0;color:var(--mu);font-size:14.5px}
.hb-ktr p.tel b{color:var(--nv)}
.hb-ktr-b{display:flex;gap:8px;margin-top:auto;padding-top:14px;flex-wrap:wrap}
.hb-ktr-b .ehb-btn{padding:10px 14px;font-size:14px}
.hb-cat{background:#fff8e1;border:1px solid #f1d57a;border-radius:14px;padding:14px 18px;margin:0 0 22px;color:#5c4400;font-size:14.5px;line-height:1.65}
.hb-ajak{text-align:center;max-width:820px}
.hb-ajak h2,.hb-ajak .ehb-kick{text-align:center}
.hb-sq{margin:0}.hb-sq img{width:100%;max-width:420px;display:block;margin:auto;border-radius:24px;background:radial-gradient(circle at 50% 40%,#fff,#e6efff);padding:18px}
.hb-visi{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.25);border-left:4px solid var(--gd);border-radius:14px;padding:16px 20px;margin:10px 0 22px;max-width:820px}
.hb-visi b{font:700 13px Montserrat,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--gd)}
.hb-visi p{margin:4px 0 0;font:700 19px/1.5 Martel,Georgia,serif;color:#fff}
.hb-gal{columns:4 220px;column-gap:12px}
.hb-gal a{display:block;margin:0 0 12px;break-inside:avoid}
.hb-gal img{width:100%;display:block;border-radius:14px;box-shadow:0 8px 20px rgba(16,33,61,.1)}
</style>'''


def bangun(slug):
    isi = HALAMAN[slug][1]()
    return (f'<!-- wp:html -->\n{H.FONTS}\n<div class="ehc ehb ehj">{isi}\n</div>\n'
            f'{H.gaya_dasar()}\n{H.CSS_HAJI}\n{H.CSS_HB}\n{CSS_PAGES}\n<!-- /wp:html -->\n')


if __name__ == '__main__':
    pilih = [a for a in sys.argv[1:] if not a.startswith('--')] or list(HALAMAN)
    os.makedirs(DIR, exist_ok=True)
    for slug in pilih:
        konten = bangun(slug)
        f = os.path.join(DIR, f'{slug}.html')
        open(f, 'w', encoding='utf-8').write(konten)
        print('tulis', os.path.relpath(f, ROOT), len(konten))
        if '--draft' in sys.argv:
            idf = os.path.join(DIR, f'{slug}.draft-id')
            pid = open(idf).read().strip() if os.path.exists(idf) else ''
            data = {'title': HALAMAN[slug][0], 'content': konten, 'status': 'draft', 'template': 'elementor_header_footer'}
            s, r = H.hb('POST', f'/wp/v2/pages/{pid}' if pid else '/wp/v2/pages', data)
            if s not in (200, 201):
                sys.exit(f'{slug}: gagal simpan draft {s} {str(r)[:200]}')
            open(idf, 'w').write(str(r['id']))
            print('  draft', r['id'], s)
