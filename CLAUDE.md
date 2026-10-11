# CLAUDE.md — konteks proyek Elharamain Wisata

Baca file ini di awal sesi. Bahasa kerja: Indonesia. Jangan minta pemilik mengulang info yang sudah tertulis di sini.

## 4 domain (WordPress + Elementor + Rank Math)
| Domain | Peran |
|---|---|
| elharamainwisata.com | Web utama, hub brand (umroh + haji). **Sudah bagus — JANGAN diubah.** |
| elharamainhaji.com | Web haji utama (jualan/transaksional). 1.530 post spam sudah di-Trash (30 Sep); lihat README |
| elharamain.id | Info/edukasi umroh |
| haji.biz | Info/edukasi haji. Theme **GeneratePress** (sejak Okt 2026). Auth REST jalan lagi per 10 Okt 2026 |
| elharamainwisata.com | Web utama, hub brand (umroh + haji). **Sudah bagus — JANGAN diubah.** Sejak 5 Okt 2026 di WordPress.com (blog ID 257762850); REST pakai apex tanpa www (www 301 → POST jadi GET). |
| elharamainhaji.com | Web haji utama (jualan/transaksional). Ada 1.376 post spam di-noindex; lihat README |
| elharamain.id | Info/edukasi umroh |
| haji.biz | Info/edukasi haji. **Sudah pindah ke WordPress.com (4 Okt 2026)**; kelola via konektor `WordPress_com` |

**Sumber kebenaran: `README.md` (branch `main`).** Baca itu dulu; berisi peran domain, tools, widget live, tracking GTM,
pelajaran teknis LiteSpeed, dan daftar "Pekerjaan berikutnya". Branch kerja utama = `main`; jangan mulai dari branch `claude/*` lama.
Kredensial: env var per domain (nama ada di README), jangan tulis di repo.

## Akses
- MCP WordPress tersambung: `elharamainwisata_com`, `haji_biz` (tool: elementor/*, rank-math/*, marketplace/*).
- `Elharamainhaji` & `Elharamain_id` **sudah tersambung** (30 Sep, kemampuan sama).
- `Elharamainhaji` & `Elharamain_id` **sudah tersambung** (30 Sep 2026), tool sama (elementor/*, rank-math/*, marketplace/*).
- Sejak 3 Okt 2026 juga tersambung: `Elharamainhaji`, `Elharamain_id` (MCP adapter: discover/execute ability).
- Cloudinary: upload langsung dari container diblokir proxy → upload file ke Media WP via REST, lalu `upload-asset` Cloudinary dari URL WP.
- Tersambung juga: `Elharamainhaji`, `Elharamain_id` (sejak 3 Okt 2026).
- Konektor WordPress.com (`WordPress_com`, tool `wpcom-*`), per 4 Okt 2026:
  **haji.biz sekarang di WordPress.com** (blog ID 257739192, atomic, domain custom aktif; Elementor, Rank Math Pro, UAE, Click to Chat Pro, WPCode sudah terpasang);
  `news.elharamainwisata.com` (blog ID 257737206, atomic, portal berita); `sublime-collector.wordpress.com` (blog ID 257742537, kosong, tujuan belum dijelaskan).
  Konektor MCP `haji_biz` (hosting lama) sudah tidak relevan; auth REST lama haji.biz yang rusak = tidak berlaku lagi (uji ulang jika perlu REST di hosting baru).
- REST API elharamainwisata.com: lihat `README.md` (snippet WPCode `wordpress/wpcode-bantu-login-api.php`, kredensial dari env `WP_USER` / `WP_APP_PASSWORD`, jangan pernah tulis kredensial di repo).
- Tool marketplace hanya memasang plugin dari URL download; plugin berbayar butuh file zip/lisensi dari pemilik.

## Aturan kerja
- **JANGAN ubah elharamainwisata.com** (situs utama sudah bagus, kata pemilik). Hanya boleh baca/audit. Perubahan hanya jika pemilik minta eksplisit.
- **haji.biz = khusus haji**: jangan tautkan/buat halaman umroh di menu, header, footer, atau halaman haji.biz. **Artikel/blog boleh campur** haji & umroh (keputusan pemilik 30 Sep 2026).
- Istilah pemilik: "UAE" = plugin Ultimate Addons for Elementor. Kalau istilah ambigu, cek dulu di sini sebelum bertanya.
- Konfirmasi dulu sebelum aksi di situs live yang sulit dibatalkan (pasang/hapus plugin, publish halaman). Halaman baru dibuat sebagai Draft.
- Jangan buat PR kecuali diminta. Commit ke branch sesi, push di akhir.
- Simpan ringkasan tiap sesi di `catatan/AAAA-BB-HH-sesi.md` (keputusan, pekerjaan, temuan; tanpa kredensial). Lakukan otomatis di akhir sesi tanpa diminta, lalu commit & push. Transkrip mentah tidak bisa disimpan; hanya ringkasan.
- Di akhir sesi, perbarui bagian "Status & tugas" di bawah supaya sesi berikutnya tidak mengulang.

## Status & tugas
Lihat "Pekerjaan berikutnya" di `README.md`. Tambahan sesi 2026-09-30:
- Plugin UAE (= Ultimate Addons for Elementor gratis, slug `header-footer-elementor`) aktif di haji.biz, elharamain.id, elharamainhaji.com.
- Draf header/footer haji.biz: `wordpress/uae/haji-biz-*.html` (brand dari `tools/build_header.py`/`build_footer.py`). Belum dipasang: MCP haji.biz tak bisa membuat post type `elementor-hf`, REST haji.biz rusak → tempel manual di UAE.
- Konektor `Elharamainhaji` & `Elharamain_id` sudah tersambung; audit kedua situs ada di `catatan/2026-09-30-sesi.md`.
- Spam elharamainhaji.com: 1.530 post sudah di-Trash (30 Sep). Sisa: pemilik buat 1 redirect regex Rank Math (isian di README;
  per 3 Okt belum ada), lalu cek `rank-math/get-redirections`. Helper REST: `tools/wp_rest_elharamainhaji.py`. Jangan cari "generator" lagi (itu drip post terjadwal, sudah dibuang).
- elharamain.id (3 Okt): timezone Asia/Jakarta ✅, LiteSpeed Cache aktif ✅. Menunggu pemilik di wp-admin: Site Language →
  Bahasa Indonesia (paket bahasa belum ada, REST tak bisa) dan update Elementor Pro 3.28.3 → 4.3.0 (berlisensi). Lihat `catatan/2026-10-03-sesi.md`.
- Akses otomatis: snippet `wordpress/wpcode-uae-rest.php` aktif di haji.biz, elharamainhaji.com, elharamain.id. Login REST semua situs OK (helper `tools/deploy_uae.py` → fungsi `rest()`, pakai curl).
- Header/footer UAE **LIVE** di 3 situs (menu: Home, Paket, Tentang Kami, Lokasi Kantor, Blog). Ubah lewat `tools/build_uae_sites.py` lalu `tools/deploy_uae.py`; halaman Lokasi Kantor/Tentang Kami lewat `tools/build_info_pages.py --publish`. Detail: catatan/2026-09-30-sesi.md.
- Paket di beranda elharamain.id & elharamainhaji.com sudah sesuai brosur PDF (`tools/update_home_paket.py`).
- Menunggu keputusan pemilik: di haji.biz masih terbit 2 **halaman** umroh (ID 778, 135) → draft/redirect? (Artikel umroh ID 293, 263 & kategori "Haji & Umroh" dibiarkan: artikel boleh campur.)
- Artikel TERBIT 30 Sep: elharamain.id 832 & 801, elharamainhaji.com 3509. Draft halaman elharamain.id 809/811/814/815 & elharamainhaji 3516 + draft elharamainwisata.com 9733/9735 belum diterbitkan. Sumber berita luar (HIMPUH, news.elharamainwisata.com, Kemenag) diblok egress environment.
- **70 artikel terjadwal 1–7 Okt 2026** (35 elharamain.id, 35 haji.biz) — lihat `data/jadwal-artikel-2026-10.json` & `tools/artikel_mingguan/`. Hosting membatasi laju request: beri jeda 20–30 dtk.
- **Indexing haji.biz seret**: anti-bot hosting (openresty) membalas halaman reload ke Googlebot; haji.biz tidak lewat Cloudflare. Detail & rekomendasi: catatan/2026-09-30-sesi.md (bagian audit indexing).
- SEO Rank Math per post bisa diisi via REST `POST /rankmath/v1/updateMeta` {objectID, objectType:'post', meta}.
- Audit Rank Math 30 Sep: elharamainhaji.com skor 78 (59 post + 12 halaman tanpa focus keyword, GSC belum ditautkan); elharamain.id skor 80 (meta deskripsi beranda 170 kar., 42 gambar tanpa alt, og:image kosong, GSC belum ditautkan).
- (3 Okt) Konektor `Elharamainhaji` & `Elharamain_id` sudah tersambung.
- (3 Okt) Brosur Riyadh Air November (update 29/09) & Ramadhan 1448 H sudah live di 12 halaman paket elharamainwisata.com
  (atas permintaan pemilik). Skrip: `tools/update_paket_2026_10.py`, backup `backup/2026-10-03/`. Sisa: SEO 9581, tab "Semua", sinkron builder.
- (3 Okt) Carousel "Fasilitas Elharamain Wisata" lama diganti slider semua hotel + bus (`tools/fasilitas_hotel.py`) di 13 halaman
  elharamainwisata.com, 12 halaman elharamain.id, 4 halaman umroh elharamainhaji.com. Halaman haji & haji.biz tidak diubah.
- (3 Okt) Judul "Apa Kata Jamaah…" dikecilkan (36/30/22 px) di 15 halaman; ruang kosong di bawah carousel 8289 diperbaiki.
- Hosting elharamainwisata.com kadang membalas halaman anti-bot "One moment, please..." (juga ke REST) → tunggu ±20 dtk lalu ulangi.
- Konektor MCP `Elharamainhaji` & `Elharamain_id` belum diotorisasi di claude.ai.

Tambahan sesi 2026-10-10: haji.biz ganti theme ke GeneratePress; template halaman LandingPress diganti ke Elementor Full Width,
CSS perbaikan di footer UAE (post 419, `<style id="hb-gp-fix">`), sidebar dirapikan. Detail: `catatan/2026-10-10-sesi.md`.
- Konektor MCP `Elharamainhaji` & `Elharamain_id` sudah tersambung (3 Okt 2026); audit SEO keduanya skor 80, detail di `catatan/2026-10-03-sesi.md`.

Tambahan sesi 2026-10-05: halaman /haji/ elharamainwisata.com disalin sebagai Draft di haji.biz (page ID 894, `brosur-haji-plus-2027`); lihat `catatan/2026-10-05-sesi.md`. Belum publish; cek risiko konten duplikat dulu.
