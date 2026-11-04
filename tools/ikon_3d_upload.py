"""Unggah wordpress/ikon-3d/*.webp ke Media WordPress elharamainwisata.com (nama file ikon-eh-<slug>.webp).
Lewati yang sudah ada (cek slug media). Simpan peta slug -> URL di wordpress/ikon-3d/media.json.
Kredensial dari env WP_USER / WP_APP_PASSWORD."""
import glob, json, os, time, urllib.request
import wp_rest as w

DIR = os.path.join(os.path.dirname(__file__), '..', 'wordpress', 'ikon-3d')
ALT = {
    'izin-resmi': 'Ikon izin resmi Kemenag', 'rincian-harga': 'Ikon rincian harga', 'booking-dp': 'Ikon booking seat dengan DP',
    'pembimbing': 'Ikon pembimbing ibadah', 'akreditasi': 'Ikon akreditasi A', 'hotel-bintang': 'Ikon hotel bintang 5',
    'satu-rekening': 'Ikon rekening resmi perusahaan', 'cicilan-ringan': 'Ikon tahapan pembayaran', 'reschedule': 'Ikon reschedule jadwal',
    'konsultasi-gratis': 'Ikon konsultasi gratis', 'konsultasi': 'Ikon konsultasi', 'booking-seat': 'Ikon tiket booking seat',
    'manasik': 'Ikon manasik umroh', 'berangkat': 'Ikon pesawat berangkat', 'beribadah': 'Ikon Ka\'bah, beribadah di Tanah Suci',
    'pulang': 'Ikon kembali ke tanah air', 'umroh-januari': 'Ikon kalender Januari', 'umroh-ramadhan': 'Ikon bulan sabit Ramadhan',
    'itikaf': 'Ikon lentera i\'tikaf', 'umroh-syawal': 'Ikon ketupat Syawal',
    'jamaah-umroh': 'Ikon jamaah umroh', 'pendaftar-haji': 'Ikon pendaftar haji', 'kantor-cabang': 'Ikon kantor cabang',
    'berpengalaman': 'Ikon piala pengalaman', 'reputasi': 'Ikon reputasi dan kepuasan jamaah', 'sajadah': 'Ikon sajadah, kenyamanan ibadah',
    'rating': 'Ikon rating bintang lima', 'tim-solid': 'Ikon tim berpengalaman', 'asatidz': 'Ikon asatidz berilmu',
    'kajian': 'Ikon kajian dan ilmu', 'medali-silver': 'Medali paket Silver', 'medali-gold': 'Medali paket Gold',
    'medali-arbain': 'Medali paket Gold Arbain', 'medali-platinum': 'Medali paket Platinum',
    'tenda-vip': 'Ikon tenda VIP Arafah Mina', 'bus-vip': 'Ikon bus VIP jamaah', 'medis': 'Ikon pendamping kesehatan',
}
peta_f = os.path.join(DIR, 'media.json')
peta = json.load(open(peta_f)) if os.path.exists(peta_f) else {}
for p in sorted(glob.glob(os.path.join(DIR, '*.webp'))):
    slug = os.path.basename(p)[:-5]
    if slug in peta:
        continue
    nama = f'ikon-eh-{slug}.webp'
    s, ada = w.req('GET', f'/wp/v2/media?search=ikon-eh-{slug}&_fields=id,source_url,slug')
    hit = [m for m in (ada if s == 200 else []) if m['slug'] == f'ikon-eh-{slug}']
    if hit:
        peta[slug] = {'id': hit[0]['id'], 'url': hit[0]['source_url']}; continue
    r = urllib.request.Request(w.BASE + '/wp/v2/media', data=open(p, 'rb').read(), method='POST', headers={
        'Authorization': w.AUTH, 'Content-Type': 'image/webp', 'Content-Disposition': f'attachment; filename="{nama}"',
        'User-Agent': 'Mozilla/5.0 eh-admin'})
    m = json.load(urllib.request.urlopen(r, timeout=120))
    w.req('POST', f'/wp/v2/media/{m["id"]}', {'alt_text': ALT[slug], 'title': ALT[slug]})
    peta[slug] = {'id': m['id'], 'url': m['source_url']}
    print(slug, m['id'], m['source_url'])
    json.dump(peta, open(peta_f, 'w'), indent=1)
    time.sleep(2)
json.dump(peta, open(peta_f, 'w'), indent=1)
print(len(peta), 'ikon di media')
