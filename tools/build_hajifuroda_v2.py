"""hajifuroda.co.id v2: landing page kualitas desainer profesional (permintaan pemilik 2026-11-04: "gambar dan icon tidak pas,
tulisan acak-acakan ... buat lp yang bagus enak dilihat seperti hasil web desainer profesional, seo-nya juga").
Perbaikan dari v1: section dikunci lebar penuh (tema Astra membatasi <section> 1200px), grid min-width:0 (tabel tidak lagi
mendorong teks keluar layar di HP), judul section rata tengah dengan ruang lega, kartu radius 16 + bayangan halus, ikon seragam
di atas judul (tidak menimpa foto), stepper bernomor, perjalanan 12 titik dalam grid (tanpa geser), strip logo legalitas,
foto seragam 4:3 fokus atas (wajah tidak terpotong), CTA penutup bergambar.
SEO: satu H1 berkata kunci "daftar haji khusus", H2 per bagian, alt text, JSON-LD TravelAgency (6 kantor) + FAQPage + BreadcrumbList,
dan judul/deskripsi meta All in One SEO per halaman (sebelumnya deskripsi = #post_content -> potongan teks berantakan).
Aturan pemilik untuk situs ini tetap: biru + putih saja (tanpa kuning/emas), Poppins, ikon solid putih di lingkaran biru,
tanpa kata sumber/brosur, tanpa label kecil di atas judul, judul tanpa titik dua. Data dari build_hajifuroda.py (Brosur 1448 H).

  python3 tools/build_hajifuroda_v2.py [halaman ...]            -> landing-pages/situs/hajifuroda/<halaman>.html
  python3 tools/build_hajifuroda_v2.py --draft [halaman ...]    -> + simpan Draft (ID <halaman>.draft-id)
Pasang ke live: tools/pasang_hajifuroda.py (memakai HALAMAN dari modul ini)."""
import html, json, os, sys, urllib.parse as up
sys.path.insert(0, os.path.dirname(__file__))
import build_hajifuroda as B

U, H, P, wa, hf, META = B.U, B.H, B.P, B.wa, B.hf, B.META
DIR = B.DIR
LOGO = json.load(open(os.path.join(DIR, 'logo-media.json')))
WA_DAFTAR = B.WA_DAFTAR


def ik(n, cls=''):
    return f'<span class="hx-ic {cls}" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="{P[n]}"/></svg></span>'


def img(f, alt, cls='', eager=False, w=800, h=600):
    ld = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ''
    return f'<img{c} {ld} decoding="async" width="{w}" height="{h}" src="{U}{f}" alt="{html.escape(alt)}">'


def btn(t, href=WA_DAFTAR, k='wa', baru=True):
    tgt = ' target="_blank" rel="noopener"' if baru else ''
    ico = f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="{P["chat"]}"/></svg>' if k == 'wa' else ''
    return f'<a class="hx-btn {k}" href="{href}"{tgt}>{ico}<span>{t}</span></a>'


def head(h2, p='', kiri=False):
    return f'<header class="hx-head{" l" if kiri else ""}"><h2>{h2}</h2>' + (f'<p>{p}</p>' if p else '') + '</header>'


def sec(isi, kelas='', id_=''):
    return f'<section class="hx-sec {kelas}"' + (f' id="{id_}"' if id_ else '') + f'><div class="hx-w">{isi}</div></section>'


def faq(items):
    body = ''.join(f'<details class="hx-q"><summary><h3>{q}</h3></summary><p>{a}</p></details>' for q, a in items)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": html.unescape(q), "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a.replace('&amp;', '&'))}} for q, a in items]}
    return f'<div class="hx-faq">{body}</div><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'


def schema_org(crumb=None):
    org = {"@context": "https://schema.org", "@type": "TravelAgency", "@id": H + "/#organisasi", "name": "Elharamain Wisata",
           "legalName": "PT Dhiyaa El Haramain El Mubarakah", "url": H + "/", "telephone": "+62-812-8729-2422",
           "logo": U + "2025/06/haji-furoda-logo-1.webp",
           "description": "Penyelenggara Ibadah Haji Khusus (PIHK) resmi SK Kemenag RI No. 846/2020 dan penyelenggara umroh resmi SK No. 63/2020.",
           "areaServed": "Indonesia", "sameAs": ["https://www.elharamainwisata.com/", "https://www.instagram.com/elharamainwisata/"],
           "department": [{"@type": "TravelAgency", "name": f"Elharamain Wisata {n.replace('Kantor ', '')}", "telephone": "+" + no,
                           "address": {"@type": "PostalAddress", "streetAddress": a, "addressCountry": "ID"}} for n, a, t, no, k in B.KANTOR]}
    out = f'<script type="application/ld+json">{json.dumps(org, ensure_ascii=False)}</script>'
    if crumb:
        bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Beranda", "item": H + "/"},
            {"@type": "ListItem", "position": 2, "name": crumb[0], "item": H + crumb[1]}]}
        out += f'<script type="application/ld+json">{json.dumps(bc, ensure_ascii=False)}</script>'
    return out


# ---------------- komponen ----------------
def trust():
    st = [('4.000 USD', 'setoran awal nomor porsi'), ('6–10 tahun', 'estimasi masa tunggu'), ('7.000+', 'ulasan Google bintang 5'), ('6 kantor', 'Jabodetabek &amp; Bandung')]
    s = ''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in st)
    return f'<div class="hx-trust"><div class="hx-w"><div class="hx-stat">{s}</div></div></div>'


def logos():
    items = [('kemenag', 'Kemenag RI', 'PIHK 846/2020 · PPIU 63/2020'), ('himpuh', 'HIMPUH', 'Anggota resmi'), ('iata', 'IATA', 'Anggota resmi')]
    s = ''.join(f'<div class="hx-logo"><img loading="lazy" width="120" height="120" src="{LOGO[k]}" alt="Logo {n}"><div><b>{n}</b><span>{t}</span></div></div>' for k, n, t in items)
    s += f'<div class="hx-logo">{ik("perisai")}<div><b>Akreditasi A</b><span>Komite Akreditasi Nasional</span></div></div>'
    return f'<div class="hx-logos">{s}</div>'


def hero(h1, p, foto, kanan='', ctas=None, kecil=False, crumb=''):
    ctas = ctas or (btn('Konsultasi gratis') + '<a class="hx-btn ghost" href="#paket"><span>Lihat paket &amp; harga</span></a>')
    cr = f'<nav class="hx-crumb" aria-label="breadcrumb"><a href="{H}/">Beranda</a><span>/</span>{crumb}</nav>' if crumb else ''
    return (f'<section class="hx-hero{" sm" if kecil else ""}" style="--img:url({U}{foto})"><div class="hx-w hx-hero-g">'
            f'<div class="hx-hero-t">{cr}<h1>{h1}</h1><p>{p}</p><div class="hx-ctas">{ctas}</div></div>{kanan}</div></section>')


def ringkasan():
    rows = [('Setoran awal nomor porsi', '4.000 USD'), ('Estimasi masa tunggu', '6–10 tahun'), ('Dana manfaat setoran', '± 120 USD/tahun'), ('Paket mulai', '12.000 USD')]
    r = ''.join(f'<li><span>{a}</span><b>{b}</b></li>' for a, b in rows)
    return (f'<aside class="hx-sum" aria-label="Ringkasan biaya"><h2>Ringkasan setoran</h2><ul>{r}</ul>'
            '<p>Pelunasan dikurangi DP dan dana manfaat. Estimasi keberangkatan 2027, naik ±4–5% per tahun.</p>'
            + btn('Minta simulasi biaya', B.WA_SIMULASI) + '</aside>')


def kartu_ikon(items, kolom=3, rata='c'):
    s = ''.join(f'<article class="hx-card {rata}">{ik(i)}<h3>{t}</h3><p>{d}</p></article>' for i, t, d in items)
    return f'<div class="hx-grid g{kolom}">{s}</div>'


def tabel_banding():
    rows = [('Penyelenggara', 'PIHK berizin (swasta resmi)', 'Pemerintah'), ('Kuota', 'Kuota haji nasional resmi', 'Kuota haji nasional resmi'),
            ('Nomor antrean', 'Antrean Haji Khusus di SISKOHAT', 'Antrean Haji Reguler, terpisah'), ('Setoran awal', '4.000 USD', 'Sesuai ketentuan pemerintah'),
            ('Estimasi masa tunggu', '6–10 tahun', 'Jauh lebih lama, tergantung provinsi'), ('Pindah porsi', 'Porsi reguler tidak bisa dipindah ke Haji Khusus', '—'),
            ('Pendampingan', 'Pembimbing, 3 petugas per bus, dokter, tenda VIP', 'Sesuai layanan pemerintah')]
    tr = ''.join(f'<tr><th scope="row">{a}</th><td class="k" data-l="Haji Khusus">{b}</td><td data-l="Haji Reguler">{c}</td></tr>' for a, b, c in rows)
    return (f'<div class="hx-tbl"><table><caption class="sr">Perbandingan Haji Khusus dan Haji Reguler</caption><thead><tr><th scope="col">Aspek</th>'
            f'<th scope="col" class="k">Haji Khusus</th><th scope="col">Haji Reguler</th></tr></thead><tbody>{tr}</tbody></table></div>')


def stepper():
    st = [('Konsultasi', 'Ceritakan rencana Bapak/Ibu lewat WhatsApp atau di salah satu dari 6 kantor.'),
          ('Siapkan dokumen', 'KTP, KK, akta kelahiran atau buku nikah, dan pas foto.'),
          ('Setor 4.000 USD', 'Ke rekening resmi a.n. PT Dhiyaa El Haramain El Mubarakah.'),
          ('Nomor porsi terbit', 'Tercatat di SISKOHAT atas nama Bapak/Ibu sendiri.'),
          ('Masa tunggu', 'Diisi kajian bulanan dan voucher umroh Rp 5 juta.'),
          ('Pelunasan &amp; manasik', 'Biaya akhir diumumkan setahun sebelum berangkat, lalu manasik camp 5 hari.')]
    return '<ol class="hx-steps">' + ''.join(f'<li><span class="n">{i}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(st, 1)) + '</ol>'


def kartu_paket(p, unggul=False):
    h4, h3, h2 = p['h']
    fit = [p['hari'], f"Makkah · {p['mk']}", f"Madinah · {p['md']}", f"Transit · {p['tr']}", f"Maskapai {p['fl']}", 'Kereta cepat Haramain',
           'Tenda VIP Arafah–Mina'] + (['Program Arbain 40 waktu'] if p['arb'] else [])
    li = ''.join(f'<li>{ik("cek", "xs")}<span>{x}</span></li>' for x in fit)
    lbl = '<span class="hx-pop">Paling banyak dipilih</span>' if unggul else ''
    return (f'<article class="hx-pk{" pop" if unggul else ""}">{lbl}<h3>Paket {p["n"]}</h3><p class="hx-pk-s">Haji Khusus 1448 H · estimasi 2027</p>'
            f'<div class="hx-pk-m"><small>mulai</small><b>{h4}</b><small>USD / jamaah</small></div>'
            f'<div class="hx-pk-r"><span>sekamar 3 <b>{h3}</b></span><span>sekamar 2 <b>{h2}</b></span></div><ul>{li}</ul>'
            + btn(f'Tanya Paket {p["n"]}', wa(f"Assalamu'alaikum, saya ingin tanya Paket Haji Khusus {p['n']} 1448 H."), 'wa') + '</article>')


def paket_grid():
    return '<div class="hx-pks">' + ''.join(kartu_paket(p, i == 1) for i, p in enumerate(B.PAKET)) + '</div>'


def perjalanan():
    return '<ol class="hx-trip">' + ''.join(f'<li>{ik(i, "sm")}<b>{d} Dzulhijjah</b><h3>{t}</h3><p>{x}</p></li>' for d, t, x, i in B.PERJALANAN) + '</ol>'


def layanan_kartu():
    return '<div class="hx-grid g4">' + ''.join(
        f'<article class="hx-fc"><figure>{img(f, t)}</figure><div class="hx-fc-b"><h3>{ik(i, "sm")}{t}</h3><p>{d}</p></div></article>'
        for t, d, i, f in B.LAYANAN) + '</div>'


def pembimbing(n=8):
    # file pembimbing = kartu bingkai 577x576; panel foto di x142-463, y48-475 -> hanya panel itu yang ditampilkan
    return '<div class="hx-ust">' + ''.join(f'<figure><div class="ph">{img(f"2026/10/pembimbing-ust-{s}.webp", nm + ", pembimbing ibadah Elharamain Wisata", w=577, h=576)}</div>'
                                           f'<figcaption>{nm}</figcaption></figure>' for s, nm in B.PEMBIMBING[:n]) + '</div>'


def galeri(fs):
    return '<div class="hx-gal">' + ''.join(f'<figure>{img(f, a)}</figure>' for f, a in fs) + '</div>'


def kantor():
    out = []
    for nama, alamat, telp, no, kota in B.KANTOR:
        peta = 'https://www.google.com/maps/search/?api=1&amp;query=' + up.quote(f'Elharamain Wisata {alamat}')
        pesan = up.quote("Assalamu'alaikum Elharamain Wisata " + kota)
        out.append(f'<article class="hx-card l ktr">{ik("pin")}<h3>{nama}</h3><p>{alamat}</p><p class="tel">{telp}</p><div class="hx-ctas sm">'
                   + btn('WhatsApp', f'https://wa.me/{no}?text={pesan}') + f'<a class="hx-btn line" href="{peta}" target="_blank" rel="noopener"><span>Petunjuk arah</span></a></div></article>')
    return '<div class="hx-grid g3">' + ''.join(out) + '</div>'


def penutup(h2='Amankan nomor porsi Haji Khusus keluarga Bapak/Ibu', p='Antrean bertambah setiap tahun. Konsultasi gratis dan tanpa kewajiban, tim kami menjawab dengan sabar dan terbuka.'):
    return (f'<section class="hx-end"><div class="hx-w hx-end-g"><figure>{img("2026/10/rombongan-haji-elharamain-di-depan-kabah.webp", "Rombongan haji Elharamain di depan Ka\'bah")}</figure>'
            f'<div><h2>{h2}</h2><p>{p}</p><div class="hx-ctas">{btn("Konsultasi via WhatsApp")}<a class="hx-btn ghost" href="{H}/kontak/"><span>Lihat 6 kantor</span></a></div>'
            '<p class="hx-end-n">Pembayaran hanya sah ke rekening atas nama PT Dhiyaa El Haramain El Mubarakah.</p></div></div></section>')


ULASAN = sec(head('Bintang 5 dari lebih 7.000 ulasan Google', 'Pengalaman jamaah Elharamain Wisata yang menulis ulasan di Google.') + '<div class="hx-ti">[trustindex no-registration=google]</div>', 'soft', 'ulasan')
FAQ_UMUM = [
    ('Apa itu Haji Khusus atau Haji Plus?', 'Program haji resmi yang memakai kuota haji nasional sesuai UU No. 8 Tahun 2019. Penyelenggaranya pihak swasta berizin PIHK, seperti Elharamain Wisata dengan SK Kemenag RI No. 846/2020.'),
    ('Berapa setoran awal untuk nomor porsi Haji Khusus?', 'Setoran awal 4.000 USD per jamaah untuk pengambilan nomor porsi. Pembayaran hanya sah ke rekening atas nama PT Dhiyaa El Haramain El Mubarakah.'),
    ('Berapa lama masa tunggu Haji Khusus?', 'Di sistem Kementerian Haji masa tunggu berkisar 10 tahun, tetapi di lapangan bisa lebih cepat, sekitar 6–10 tahun. Tambahan kuota dari Arab Saudi bisa mempercepat antrean.'),
    ('Apakah porsi Haji Reguler bisa dipindah ke Haji Khusus?', 'Tidak bisa, karena alur pendaftaran dan antrean Haji Reguler dan Haji Khusus berbeda.'),
    ('Apa itu dana manfaat setoran haji?', 'Setoran 4.000 USD dikelola BPKH dengan instrumen syariah dan bertumbuh sekitar 120 USD per tahun. Di Elharamain Wisata dana manfaat dikembalikan sebagai pengurangan harga paket.'),
    ('Berapa kenaikan biaya haji per tahun?', 'Estimasi kenaikan sekitar 4–5% per tahun dari harga tahun sebelumnya. Biaya akhir diinformasikan setahun sebelum keberangkatan.')]


# ---------------- halaman ----------------
def pg_beranda():
    h = hero('Daftar Haji Khusus resmi Kemenag, porsi atas nama Bapak/Ibu sendiri',
             'Elharamain Wisata, PIHK berizin SK Kemenag RI No. 846/2020. Setoran awal 4.000 USD, estimasi masa tunggu 6–10 tahun, dan dana manfaat setoran dikembalikan untuk jamaah.',
             '2026/10/daftar-haji-khusus-rombongan-masjidil-haram.webp', ringkasan())
    legal = sec(logos(), 'thin', 'legalitas')
    beda = sec(head('Beda Haji Khusus dan Haji Reguler', 'Sama-sama memakai kuota haji nasional resmi, tetapi antrean, masa tunggu, dan pendampingannya berbeda.') + tabel_banding(), '', 'beda')
    hak = sec(head('Hak jamaah selama masa tunggu', 'Menunggu giliran berangkat tidak berarti menunggu tanpa kepastian.') + kartu_ikon([
        ('koin', 'Dana manfaat transparan', 'Setoran dikelola BPKH secara syariah, bertumbuh ±120 USD per tahun, dan mengurangi harga paket. Bisa dicek di aplikasi BPKH.'),
        ('hadiah', 'Voucher umroh Rp 5 juta', 'Bonus voucher umroh Elharamain Wisata selama masa tunggu. Syarat dan ketentuan berlaku.'),
        ('hati', 'Free Badal Haji', 'Bila calon jamaah wafat sebelum berangkat, InsyaAllah dibadalkan tanpa biaya. Untuk pendaftar 1448 H, S&amp;K berlaku.'),
        ('buku', 'Kajian bulanan', 'Kajian online rutin sebulan sekali agar bekal ilmu dan semangat terjaga.')], 4), 'soft', 'masa-tunggu')
    langkah = sec(head('Enam langkah daftar Haji Khusus', 'Dari konsultasi pertama sampai berangkat ke Tanah Suci, semua dibantu tim kami.') + stepper()
                  + f'<div class="hx-ctas c">{btn("Mulai konsultasi")}</div>', '', 'langkah')
    pk = sec(head('Paket Haji Khusus 1448 H', 'Estimasi keberangkatan 2027. Harga per jamaah dalam USD; sekamar berempat, bertiga, atau berdua.') + paket_grid()
             + f'<p class="hx-note">Biaya keseluruhan diinformasikan setahun sebelum keberangkatan, estimasi naik 4–5% per tahun. Rincian di halaman <a href="{H}/layanan/">Layanan</a>.</p>', 'navy', 'paket')
    trip = sec(head('Rangkaian perjalanan 2–26 Dzulhijjah', 'Gambaran paket 22–23 hari. Gold Arbain menambah waktu di Madinah untuk 40 kali sholat berjamaah.') + perjalanan(), 'soft', 'perjalanan')
    ly = sec(head('Layanan di Tanah Suci', 'Disiapkan agar jamaah tenang, nyaman, dan fokus beribadah.') + layanan_kartu(), '', 'layanan')
    ust = sec(head('Dibimbing asatidz lulusan Timur Tengah', 'Pembimbing mendampingi jamaah dari manasik sampai pulang ke Tanah Air.') + pembimbing(), 'soft', 'pembimbing')
    gal = sec(head('Jamaah Elharamain di Tanah Suci') + galeri([
        ('2026/10/haji-khusus-jamaah-tawaf-malam-kabah.webp', 'Jamaah haji khusus tawaf malam di Ka\'bah'),
        ('2026/10/rombongan-haji-elharamain-ihram-dalam-tenda.webp', 'Rombongan haji Elharamain berihram di dalam tenda'),
        ('2026/10/haji-khusus-jamaah-elharamain-hotel-makkah.webp', 'Jamaah haji khusus di hotel Makkah'),
        ('2026/10/jamaah-haji-stasiun-haramain-jawa-barat.webp', 'Jamaah haji di stasiun kereta Haramain'),
        ('2026/10/haji-khusus-jamaah-ihram-masjid-nabawi-senja.webp', 'Jamaah haji khusus di Masjid Nabawi saat senja'),
        ('2026/10/haji-khusus-rombongan-elharamain-spanduk-tanah-suci.webp', 'Rombongan haji khusus Elharamain di Tanah Suci')]), '', 'galeri')
    tanya = sec(head('Pertanyaan seputar daftar Haji Khusus') + faq(FAQ_UMUM), 'soft', 'faq')
    return h + trust() + legal + beda + hak + langkah + pk + trip + ly + ust + gal + ULASAN.replace(' soft"', '"', 1) + tanya + penutup() + schema_org()


def pg_profil():
    h = hero('Profil Elharamain Wisata, penyelenggara Haji Khusus resmi', 'PT Dhiyaa El Haramain El Mubarakah mendampingi jamaah Haji Khusus dan umroh dari 6 kantor di Jabodetabek dan Bandung.',
             '2026/10/profil-elharamain-keluarga-besar-jamaah-haji-1447h.webp', kecil=True, crumb='Profil',
             ctas=btn('Konsultasi gratis') + f'<a class="hx-btn ghost" href="{H}/layanan/"><span>Lihat layanan</span></a>')
    tentang = sec('<div class="hx-split"><div>' + head('Melayani tamu Allah dengan amanah', kiri=True)
                  + '<p class="hx-p">Elharamain Wisata adalah nama dagang PT Dhiyaa El Haramain El Mubarakah, Penyelenggara Ibadah Haji Khusus (PIHK) berizin SK Kemenag RI '
                  'No. 846/2020 dan penyelenggara perjalanan ibadah umrah berizin SK No. 63/2020.</p><p class="hx-p">Kami percaya perjalanan haji adalah momen istimewa yang layak '
                  'dipersiapkan secara istimewa. Jamaah didampingi sejak pendaftaran, selama masa tunggu, di Tanah Suci, sampai kembali ke rumah.</p></div>'
                  f'<figure class="hx-ph">{img("2026/10/kantor-pusat-elharamain-wisata-bekasi.webp", "Kantor pusat Elharamain Wisata di Bekasi")}</figure></div>', '', 'tentang')
    legal = sec(logos(), 'thin', 'legalitas')
    kel = sec(head('Kelebihan Elharamain Wisata') + kartu_ikon([
        ('perisai', 'PIHK resmi', 'Terdaftar di Kementerian sehingga keberangkatan jamaah sesuai regulasi.'),
        ('koin', 'DP 4.000 USD', 'Pendaftaran Haji Khusus paling ringan, prosesnya mudah dan cepat.'),
        ('gedung', 'Variasi paket', 'Empat kelas paket sesuai kebutuhan dan kenyamanan.'),
        ('buku', 'Bimbingan intensif', 'Kurikulum bimbingan terarah dan berkelanjutan menuju haji mabrur.'),
        ('hati', 'Free Badal Haji', 'Badal haji tanpa biaya bila calon jamaah wafat sebelum berangkat (S&amp;K berlaku).'),
        ('dokumen', 'Dana manfaat transparan', 'Seluruh manfaat setoran dikembalikan sebagai pengurangan biaya paket.')]), 'soft', 'kelebihan')
    bim = sec(head('Program bimbingan ibadah', 'Haji adalah perjalanan perubahan hidup; bimbingan disusun agar jamaah pulang membawa bekal menjadi pribadi yang lebih baik.')
              + kartu_ikon([(i, t, d) for t, d, i in B.BIMBINGAN], 3, 'l'), '', 'bimbingan')
    ust = sec(head('Pembimbing ibadah kami', 'Asatidz lulusan Timur Tengah yang mendampingi jamaah dari manasik sampai pulang.') + pembimbing(), 'soft', 'pembimbing')
    gal = sec(head('Keluarga besar jamaah Elharamain') + galeri([
        ('2026/10/profil-elharamain-jamaah-haji-zamzam-tower.webp', 'Jamaah haji Elharamain di depan Zamzam Tower'),
        ('2026/10/jamaah-haji-elharamain-pelataran-kabah-malam.webp', 'Jamaah haji Elharamain di pelataran Ka\'bah malam hari'),
        ('2026/10/jamaah-haji-elharamain-berangkat-di-bandara.webp', 'Jamaah haji Elharamain berangkat di bandara'),
        ('2026/10/jamaah-haji-1447h-elharamain-di-tenda.webp', 'Jamaah haji 1447 H Elharamain di tenda'),
        ('2026/10/jamaah-haji-masjid-quba-jakarta-utara.webp', 'Jamaah haji di Masjid Quba'),
        ('2026/10/haji-plus-keluarga-besar-jamaah-elharamain.webp', 'Keluarga besar jamaah haji plus Elharamain')]), '', 'galeri')
    return h + tentang + legal + kel + bim + ust + gal + ULASAN + penutup() + schema_org(('Profil', '/profil/'))


def pg_layanan():
    h = hero('Layanan Haji Khusus 1448 H, dari nomor porsi sampai kembali ke Tanah Air',
             'Empat kelas paket, tenda VIP Arafah–Mina, kereta cepat Haramain, dan pendampingan ibadah intensif. Estimasi keberangkatan 2027.',
             '2026/10/layanan-haji-khusus-jamaah-tawaf-kabah-malam.webp', ringkasan(), kecil=True, crumb='Layanan')
    pk = sec(head('Harga Paket Haji Khusus 1448 H', 'Harga per jamaah dalam USD. Setoran awal semua paket 4.000 USD.') + paket_grid()
             + '<p class="hx-note">Pelunasan dikurangi DP 4.000 USD dan dana manfaat (±120 USD per tahun). Biaya keseluruhan diinformasikan setahun sebelum keberangkatan; estimasi naik 4–5% per tahun.</p>', 'navy', 'paket')
    trip = sec(head('Rangkaian perjalanan haji', 'Paket 22–23 hari; Gold Arbain 27–28 hari dengan tambahan waktu di Madinah.') + perjalanan(), 'soft', 'perjalanan')
    ly = sec(head('Fasilitas dan pendampingan') + layanan_kartu() + '<div class="hx-gap"></div>' + kartu_ikon([
        ('pesawat', 'Penerbangan', 'Saudia, Qatar, atau Emirates; Platinum dengan Saudia atau Garuda Indonesia.'),
        ('kereta', 'Kereta cepat Haramain', 'Perjalanan Makkah–Madinah dengan Haramain High Speed Railway.'),
        ('gedung', 'Hotel transit', 'Jamaah dipersiapkan di hotel transit Makkah sebelum menuju Armuzna.'),
        ('koper', 'Perlengkapan eksklusif', 'Koper bagasi dan kabin, kain ihram, mukena, batik, rompi, dan lainnya.'),
        ('ulang', 'Umroh hingga 3 kali', 'Difasilitasi selama di Makkah, bisa untuk membadalkan keluarga.'),
        ('bintang', 'Pelayanan berkualitas', 'Perhatian pada detail layanan, dinilai bintang 5 oleh jamaah.')], 3, 'l'), '', 'fasilitas')
    istilah = sec(head('Istilah yang perlu Bapak/Ibu ketahui') + faq([
        ('Apa itu Tarwiyah?', 'Amalan sunnah pada 8 Dzulhijjah ketika jamaah mulai berihram dan menuju Mina untuk bermalam, pembuka rangkaian menuju wukuf di Arafah.'),
        ('Apa itu Nafar Tsani?', 'Program tetap bermalam di Mina hingga 13 Dzulhijjah, lalu melontar jumrah pada hari itu sebelum meninggalkan Mina.'),
        ('Apa itu hotel transit?', 'Hotel di Makkah tempat jamaah transit sebelum berangkat ke Armuzna, agar lebih fokus menghadapi ibadah inti haji.'),
        ('Apa itu Program Arbain?', 'Ibadah 40 kali sholat fardhu berjamaah berturut-turut di Masjid Nabawi, tersedia di Paket Gold Arbain.'),
        ('Apa itu Murur?', 'Metode mabit di Muzdalifah dengan melintas setelah wukuf tanpa turun dari kendaraan, lalu langsung ke Mina atau Masjidil Haram.'),
        ('Apa itu Tanazul?', 'Skema layanan di mana jamaah menginap di hotel sekitar Mina, bukan di tenda, lalu kembali ke Mina untuk melontar jumrah.')]), 'soft', 'istilah')
    return h + pk + trip + ly + istilah + ULASAN.replace(' soft"', '"', 1) + penutup() + schema_org(('Layanan', '/layanan/'))


def pg_kontak():
    h = hero('Kontak Elharamain Wisata untuk konsultasi Haji Khusus', 'Tanyakan paket, nomor porsi, atau dokumen haji lewat WhatsApp, atau datang langsung ke salah satu dari enam kantor kami.',
             '2026/10/kontak-elharamain-jamaah-depan-kabah-malam.webp', kecil=True, crumb='Kontak',
             ctas=btn('Chat WhatsApp kantor pusat') + '<a class="hx-btn ghost" href="#kantor"><span>Alamat kantor</span></a>')
    ktr = sec(head('Enam kantor pelayanan', 'Semua kantor melayani konsultasi dan pendaftaran Haji Khusus maupun umroh.') + kantor(), '', 'kantor')
    siap = sec('<div class="hx-split"><div>' + head('Siapkan ini agar konsultasi lebih cepat', kiri=True) + '<ul class="hx-chk">' + ''.join(
        f'<li>{ik("cek", "xs")}<span>{t}</span></li>' for t in ['Scan atau fotokopi KTP dan Kartu Keluarga', 'Akta kelahiran atau buku nikah suami-istri',
                                                               'Pas foto 4x6, cetak atau digital', 'Rencana paket dan tipe kamar bila sudah ada', 'Setoran awal nomor porsi 4.000 USD per jamaah'])
        + '</ul><p class="hx-warn">Pembayaran hanya sah ke rekening atas nama <b>PT Dhiyaa El Haramain El Mubarakah</b>. Jangan transfer ke rekening pribadi siapa pun.</p></div>'
        f'<figure class="hx-ph">{img("2026/10/kantor-pusat-elharamain-wisata-bekasi.webp", "Kantor pusat Elharamain Wisata Bekasi")}</figure></div>', 'soft', 'dokumen')
    tanya = sec(head('Pertanyaan seputar konsultasi') + faq([
        ('Apakah konsultasi dikenakan biaya?', 'Tidak. Konsultasi lewat WhatsApp maupun di kantor gratis dan tanpa kewajiban mendaftar.'),
        ('Bisakah mendaftar tanpa datang ke kantor?', 'Bisa. Dokumen dapat dikirim lewat WhatsApp; tim kami memandu proses sampai nomor porsi terbit.'),
        ('Bagaimana memastikan menghubungi kontak resmi?', 'Gunakan nomor di halaman ini dan pastikan pembayaran hanya ke rekening atas nama PT Dhiyaa El Haramain El Mubarakah.'),
        ('Di mana rincian paket dan harga?', f'Rincian empat paket Haji Khusus 1448 H ada di halaman <a href="{H}/layanan/">Layanan</a>.')]), '', 'faq')
    return h + ktr + siap + tanya + ULASAN + penutup('Konsultasi Haji Khusus sekarang', 'Ceritakan rencana Bapak/Ibu, tim kami menjawab dengan sabar dan terbuka.') + schema_org(('Kontak', '/kontak/'))


HALAMAN = {  # judul halaman WP, fungsi, ringkasan (excerpt), judul SEO, deskripsi SEO
    'beranda': ('Daftar Haji Khusus Resmi Kemenag', pg_beranda, 'Daftar Haji Khusus resmi Kemenag di Elharamain Wisata. Setoran porsi 4.000 USD, tunggu 6–10 tahun, dana manfaat, Free Badal Haji.',
                'Daftar Haji Khusus Resmi Kemenag, Setoran Porsi 4.000 USD | Elharamain Wisata',
                'Daftar Haji Khusus resmi PIHK Kemenag 846/2020 di Elharamain Wisata. Setoran porsi 4.000 USD, estimasi tunggu 6–10 tahun, dana manfaat, dan Free Badal Haji.'),
    'profil': ('Profil', pg_profil, 'Profil Elharamain Wisata, PIHK resmi SK Kemenag RI No. 846/2020 dengan 6 kantor dan pembimbing lulusan Timur Tengah.',
               'Profil Elharamain Wisata, PIHK Resmi Kemenag 846/2020',
               'Profil Elharamain Wisata (PT Dhiyaa El Haramain El Mubarakah), PIHK resmi Kemenag 846/2020, 6 kantor, bimbingan ibadah intensif, dan asatidz Timur Tengah.'),
    'layanan': ('Layanan', pg_layanan, 'Layanan dan harga Paket Haji Khusus 1448 H Elharamain Wisata: Silver, Gold, Gold Arbain, Platinum.',
                'Harga Paket Haji Khusus 1448 H, Silver hingga Platinum | Elharamain Wisata',
                'Harga Paket Haji Khusus 1448 H mulai 12.000 USD. Silver, Gold, Gold Arbain, Platinum dengan tenda VIP Arafah–Mina, kereta Haramain, dan bimbingan intensif.'),
    'kontak': ('Kontak', pg_kontak, 'Kontak dan alamat 6 kantor Elharamain Wisata untuk konsultasi Haji Khusus.',
               'Kontak dan Alamat 6 Kantor Elharamain Wisata',
               'Hubungi Elharamain Wisata untuk konsultasi Haji Khusus gratis. Alamat dan WhatsApp kantor Bekasi, Jakarta, Depok, Tangerang, Bandung, dan Bogor.'),
}

CSS = '''<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style id="hx">
.hx{--b:#004AAD;--n:#0A2E6B;--l:#1684CF;--s:#9FC9F5;--soft:#F3F7FC;--ink:#0f1d36;--mu:#56657d;--ln:#e2e9f3;--r:16px;--sh:0 12px 32px rgba(10,46,107,.07);
width:100vw;margin-left:calc(50% - 50vw);overflow-x:clip;font-family:Poppins,sans-serif;color:var(--ink);font-size:16px;line-height:1.7;-webkit-font-smoothing:antialiased}
.hx *,.hx *::before,.hx *::after{box-sizing:border-box}
.hx section{max-width:none!important;width:auto!important;margin:0!important}
.hx img{display:block;max-width:100%;height:auto}
.hx h1,.hx h2,.hx h3{font-family:Poppins,sans-serif!important;color:var(--ink);margin:0;letter-spacing:-.015em}
.hx p{margin:0}.hx a{color:var(--b)}.hx ul,.hx ol{margin:0;padding:0;list-style:none}
.hx .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.hx-w{max-width:1200px;margin:0 auto;padding:0 24px}
.hx-sec{padding:96px 0;background:#fff}.hx-sec.soft{background:var(--soft)}.hx-sec.thin{padding:40px 0;border-bottom:1px solid var(--ln)}
.hx-sec.navy{background:var(--n)}.hx-sec.navy .hx-head h2{color:#fff}.hx-sec.navy .hx-head p,.hx-sec.navy .hx-note{color:rgba(255,255,255,.78)}.hx-sec.navy .hx-note a{color:var(--s)}
.hx-head{max-width:720px;margin:0 auto 48px;text-align:center}.hx-head.l{margin:0 0 20px;text-align:left}
.hx-head h2{font-size:clamp(28px,3.4vw,40px);font-weight:700;line-height:1.2}
.hx-head p{margin-top:14px;font-size:17px;color:var(--mu)}
.hx-p{color:var(--mu);margin-top:14px}
.hx-ic{flex:none;display:inline-grid;place-items:center;width:56px;height:56px;border-radius:50%;background:var(--b);box-shadow:0 8px 18px rgba(0,74,173,.25)}
.hx-ic svg{width:26px;height:26px;fill:#fff}
.hx-ic.sm{width:38px;height:38px;box-shadow:0 6px 12px rgba(0,74,173,.22)}.hx-ic.sm svg{width:18px;height:18px}
.hx-ic.xs{width:22px;height:22px;box-shadow:none}.hx-ic.xs svg{width:13px;height:13px}
.hx-btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:52px;padding:0 26px;border-radius:999px;font:600 15.5px/1 Poppins,sans-serif;text-decoration:none!important;border:2px solid transparent;transition:transform .2s,box-shadow .2s,background .2s;white-space:nowrap}
.hx-btn svg{width:19px;height:19px;fill:currentColor}.hx-btn:hover{transform:translateY(-2px)}
.hx-btn.wa{background:#1fa855;color:#fff!important;box-shadow:0 10px 24px rgba(31,168,85,.28)}.hx-btn.wa:hover{background:#188f47}
.hx-btn.ghost{border-color:rgba(255,255,255,.75);color:#fff!important}.hx-btn.ghost:hover{background:rgba(255,255,255,.12)}
.hx-btn.line{border-color:var(--ln);color:var(--b)!important;background:#fff}.hx-btn.line:hover{border-color:var(--b)}
.hx-ctas{display:flex;flex-wrap:wrap;gap:12px;margin-top:32px}.hx-ctas.c{justify-content:center;margin-top:44px}
.hx-ctas.sm{margin-top:18px}.hx-ctas.sm .hx-btn{min-height:42px;padding:0 18px;font-size:14px}
.hx-hero{position:relative;color:#fff;padding:180px 0 120px;background:linear-gradient(100deg,rgba(7,28,68,.96) 0%,rgba(10,46,107,.86) 45%,rgba(0,74,173,.45) 100%),var(--img) center 30%/cover no-repeat}
.hx-hero.sm{padding:170px 0 96px}
.hx-hero-g{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,.85fr);gap:56px;align-items:center}
.hx-hero h1{color:#fff!important;font-size:clamp(34px,4.4vw,54px);font-weight:700;line-height:1.14}
.hx-hero-t>p{margin-top:20px;font-size:18px;color:rgba(255,255,255,.86);max-width:620px}
.hx-crumb{font-size:14px;margin-bottom:16px;color:rgba(255,255,255,.7)}.hx-crumb a{color:#fff!important;text-decoration:none}.hx-crumb span{margin:0 8px}
.hx-sum{background:#fff;color:var(--ink);border-radius:var(--r);padding:30px;box-shadow:0 30px 70px rgba(0,0,0,.28)}
.hx-sum h2{font-size:20px;font-weight:700}.hx-sum ul{margin:14px 0 16px}
.hx-sum li{display:flex;justify-content:space-between;gap:14px;padding:12px 0;border-bottom:1px solid var(--ln);font-size:15px}
.hx-sum li span{color:var(--mu)}.hx-sum li b{color:var(--b);white-space:nowrap}
.hx-sum>p{font-size:13.5px;color:var(--mu);margin-bottom:18px}.hx-sum .hx-btn{width:100%}
.hx-trust{background:#fff;position:relative;z-index:2}
.hx-stat{display:grid;grid-template-columns:repeat(4,1fr);background:#fff;border-radius:var(--r);box-shadow:var(--sh);margin-top:-56px;border:1px solid var(--ln)}
.hx-stat div{padding:26px 22px;text-align:center;border-right:1px solid var(--ln)}.hx-stat div:last-child{border-right:0}
.hx-stat b{display:block;font-size:28px;font-weight:700;color:var(--b);line-height:1.2}.hx-stat span{font-size:14px;color:var(--mu)}
.hx-logos{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;align-items:center}
.hx-logo{display:flex;align-items:center;gap:14px}.hx-logo img{width:60px;height:60px;object-fit:contain}
.hx-logo b{display:block;font-size:15.5px}.hx-logo span{font-size:13px;color:var(--mu)}
.hx-tbl{max-width:960px;margin:0 auto;border-radius:var(--r);overflow:auto;box-shadow:var(--sh);border:1px solid var(--ln)}
.hx-tbl table{width:100%;border-collapse:collapse;min-width:620px;font-size:15px;background:#fff}
.hx-tbl th,.hx-tbl td{padding:16px 22px;text-align:left;border-bottom:1px solid var(--ln);vertical-align:top}
.hx-tbl tr:last-child th,.hx-tbl tr:last-child td{border-bottom:0}
.hx-tbl thead th{background:var(--n);color:#fff;font-weight:600;font-size:15px}.hx-tbl thead th.k{background:var(--b)}
.hx-tbl tbody th{font-weight:500;color:var(--mu);width:26%}.hx-tbl td.k{background:#eef5ff;color:var(--n);font-weight:600}
.hx-grid{display:grid;gap:24px}.hx-grid.g2{grid-template-columns:repeat(2,minmax(0,1fr))}.hx-grid.g3{grid-template-columns:repeat(3,minmax(0,1fr))}.hx-grid.g4{grid-template-columns:repeat(4,minmax(0,1fr))}
.hx-card{background:#fff;border:1px solid var(--ln);border-radius:var(--r);padding:32px 26px;box-shadow:var(--sh);transition:transform .25s,box-shadow .25s}
.hx-card:hover{transform:translateY(-4px);box-shadow:0 20px 44px rgba(10,46,107,.12)}
.hx-card.c{text-align:center}.hx-card.c .hx-ic{margin:0 auto}
.hx-card h3{font-size:18.5px;font-weight:700;margin:20px 0 8px;line-height:1.35}.hx-card p{font-size:15px;color:var(--mu)}
.hx-card.l{padding:28px 24px}.hx-card.ktr .tel{color:var(--ink);font-weight:600;margin-top:8px}
.hx-steps{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:18px;counter-reset:s;position:relative}
.hx-steps::before{content:"";position:absolute;left:8%;right:8%;top:27px;height:2px;background:var(--s)}
.hx-steps li{position:relative;text-align:center}
.hx-steps .n{position:relative;display:inline-grid;place-items:center;width:56px;height:56px;border-radius:50%;background:var(--b);color:#fff;font-size:20px;font-weight:700;box-shadow:0 0 0 8px #fff,0 10px 20px rgba(0,74,173,.25)}
.hx-steps h3{font-size:16.5px;font-weight:700;margin:20px 0 6px}.hx-steps p{font-size:14px;color:var(--mu)}
.hx-pks{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px;align-items:stretch}
.hx-pk{position:relative;background:#fff;border-radius:20px;padding:30px 24px 26px;display:flex;flex-direction:column}
.hx-pk.pop{outline:3px solid var(--s);outline-offset:-3px}
.hx-pop{position:absolute;top:-14px;left:50%;transform:translateX(-50%);background:var(--l);color:#fff;font-size:12.5px;font-weight:600;padding:5px 14px;border-radius:999px;white-space:nowrap}
.hx-pk h3{font-size:22px;font-weight:700}.hx-pk-s{font-size:13px;color:var(--mu);margin-top:2px}
.hx-pk-m{margin:20px 0 6px;display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
.hx-pk-m small{font-size:13px;color:var(--mu)}.hx-pk-m b{font-size:36px;font-weight:800;color:var(--b);line-height:1}
.hx-pk-r{display:flex;gap:10px;flex-wrap:wrap;font-size:13px;color:var(--mu);padding-bottom:18px;border-bottom:1px solid var(--ln)}
.hx-pk-r span{background:var(--soft);border-radius:999px;padding:4px 12px}.hx-pk-r b{color:var(--ink)}
.hx-pk ul{margin:18px 0 24px;display:grid;gap:11px;flex:1}
.hx-pk li{display:flex;gap:10px;align-items:flex-start;font-size:14px;line-height:1.5}.hx-pk li .hx-ic{margin-top:1px}
.hx-pk .hx-btn{width:100%}
.hx-note{text-align:center;margin-top:30px;font-size:14px;color:var(--mu)}
.hx-trip{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:30px 20px}
.hx-trip li{background:#fff;border-radius:var(--r);padding:22px 18px;border:1px solid var(--ln);box-shadow:var(--sh)}
.hx-trip b{display:block;margin-top:14px;font-size:13px;color:var(--l);font-weight:600}
.hx-trip h3{font-size:16.5px;font-weight:700;margin-top:2px}.hx-trip p{font-size:13.5px;color:var(--mu);margin-top:4px;line-height:1.55}
.hx-fc{background:#fff;border-radius:var(--r);overflow:hidden;border:1px solid var(--ln);box-shadow:var(--sh);display:flex;flex-direction:column}
.hx-fc figure{margin:0}.hx-fc img{width:100%;aspect-ratio:4/3;object-fit:cover;object-position:center 25%}
.hx-fc-b{padding:22px 22px 26px}.hx-fc h3{display:flex;align-items:center;gap:12px;font-size:17px;font-weight:700;line-height:1.3}
.hx-fc p{font-size:14.5px;color:var(--mu);margin-top:10px}
.hx-gap{height:28px}
.hx-ust{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:22px}
.hx-ust figure{margin:0;background:#fff;border-radius:var(--r);overflow:hidden;box-shadow:var(--sh)}
.hx-ust .ph{position:relative;aspect-ratio:322/428;overflow:hidden;background:#fff}
.hx-ust .ph img{position:absolute;max-width:none;width:179.2%;height:auto;left:-44.1%;top:-11.2%}
.hx-ust figcaption{padding:14px 12px;text-align:center;font-size:14.5px;font-weight:600}
.hx-gal{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.hx-gal figure{margin:0;border-radius:var(--r);overflow:hidden}.hx-gal img{width:100%;aspect-ratio:4/3;object-fit:cover;object-position:center 30%;transition:transform .4s}
.hx-gal figure:hover img{transform:scale(1.04)}
.hx-faq{max-width:860px;margin:0 auto;display:grid;gap:12px}
.hx-q{background:#fff;border:1px solid var(--ln);border-radius:14px;padding:0 24px;box-shadow:0 6px 16px rgba(10,46,107,.04)}
.hx-q summary{list-style:none;cursor:pointer;padding:20px 36px 20px 0;position:relative}
.hx-q summary::-webkit-details-marker{display:none}
.hx-q summary h3{font-size:16.5px;font-weight:600;line-height:1.45}
.hx-q summary::after{content:"";position:absolute;right:2px;top:50%;width:12px;height:12px;border-right:2.5px solid var(--b);border-bottom:2.5px solid var(--b);transform:translateY(-70%) rotate(45deg);transition:transform .2s}
.hx-q[open] summary::after{transform:translateY(-30%) rotate(-135deg)}
.hx-q p{padding:0 0 20px;color:var(--mu);font-size:15.5px}
.hx-split{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:56px;align-items:center}
.hx-ph{margin:0}.hx-ph img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:20px;box-shadow:var(--sh)}
.hx-chk{display:grid;gap:12px;margin:8px 0 22px}.hx-chk li{display:flex;gap:12px;align-items:center}
.hx-warn{background:#eef5ff;border-radius:12px;padding:16px 20px;font-size:14.5px;color:var(--n)}
.hx-ti{max-width:1100px;margin:0 auto}
.hx-end{background:var(--n);padding:96px 0;color:#fff}
.hx-end-g{display:grid;grid-template-columns:minmax(0,.95fr) minmax(0,1.05fr);gap:56px;align-items:center}
.hx-end figure{margin:0}.hx-end img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:20px}
.hx-end h2{color:#fff!important;font-size:clamp(28px,3.2vw,40px);font-weight:700;line-height:1.2}
.hx-end p{color:rgba(255,255,255,.82);margin-top:14px;font-size:17px}.hx-end .hx-end-n{font-size:13.5px;margin-top:22px;color:rgba(255,255,255,.62)}
@media(max-width:1100px){.hx-pks,.hx-grid.g4,.hx-ust{grid-template-columns:repeat(2,minmax(0,1fr))}.hx-trip,.hx-steps{grid-template-columns:repeat(3,minmax(0,1fr))}
.hx-steps::before{display:none}.hx-logos{grid-template-columns:repeat(2,1fr)}}
@media(max-width:860px){.hx-hero-g,.hx-split,.hx-end-g{grid-template-columns:minmax(0,1fr)}.hx-hero{padding:140px 0 96px}.hx-grid.g3{grid-template-columns:repeat(2,minmax(0,1fr))}
.hx-stat{grid-template-columns:repeat(2,1fr)}.hx-stat div:nth-child(2){border-right:0}.hx-stat div:nth-child(-n+2){border-bottom:1px solid var(--ln)}}
@media(max-width:600px){.hx{font-size:15.5px}.hx-sec{padding:64px 0}.hx-w{padding:0 18px}.hx-head{margin-bottom:32px}.hx-head p{font-size:16px}
.hx-hero h1{font-size:30px}.hx-hero-t>p{font-size:16px}.hx-hero.sm{padding:130px 0 72px}
.hx-pks,.hx-grid.g2,.hx-grid.g3,.hx-grid.g4{grid-template-columns:minmax(0,1fr)}.hx-ust,.hx-gal,.hx-trip{grid-template-columns:repeat(2,minmax(0,1fr))}
.hx-steps{grid-template-columns:minmax(0,1fr);text-align:left}.hx-steps li{display:grid;grid-template-columns:56px 1fr;gap:4px 16px;text-align:left}
.hx-steps .n{grid-row:span 2}.hx-steps h3{margin:6px 0 0}
.hx-stat b{font-size:22px}.hx-stat div{padding:18px 10px}.hx-logos{grid-template-columns:minmax(0,1fr)}
.hx-tbl{overflow:visible;box-shadow:none;border:0}.hx-tbl table{min-width:0;background:none}.hx-tbl thead{display:none}.hx-tbl tr{display:block;background:#fff;border:1px solid var(--ln);border-radius:14px;margin-bottom:12px;overflow:hidden;box-shadow:var(--sh)}.hx-tbl tbody th{display:block;width:auto;background:var(--n);color:#fff;font-weight:600;padding:12px 16px}.hx-tbl td{display:grid;grid-template-columns:42% 1fr;gap:10px;padding:12px 16px}.hx-tbl td::before{content:attr(data-l);font-weight:500;color:var(--mu)}.hx-tbl tr:last-child th{border-bottom:1px solid var(--ln)}.hx-ctas .hx-btn{width:100%}.hx-sum{padding:24px}.hx-trip li{padding:18px 14px}.hx-end{padding:64px 0}}
</style>'''


def bangun(slug):
    return f'<!-- wp:html -->\n{CSS}\n<div class="hx">{HALAMAN[slug][1]()}</div>\n<!-- /wp:html -->\n'


def set_seo(pid, slug):
    _, _, _, judul_seo, desk = HALAMAN[slug]
    return hf('POST', '/aioseo/v1/post', {'id': pid, 'title': judul_seo, 'description': desk})


if __name__ == '__main__':
    pilih = [a for a in sys.argv[1:] if not a.startswith('--')] or list(HALAMAN)
    for slug in pilih:
        konten = bangun(slug)
        open(os.path.join(DIR, f'{slug}.html'), 'w', encoding='utf-8').write(konten)
        print('tulis', slug, len(konten))
        if '--draft' in sys.argv:
            idf = os.path.join(DIR, f'{slug}.draft-id')
            pid = open(idf).read().strip()
            s, r = hf('POST', f'/wp/v2/pages/{pid}', {'content': konten, 'excerpt': HALAMAN[slug][2], 'status': 'draft', 'template': '', 'meta': META})
            print('  draft', pid, s)
