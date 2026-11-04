"""haji.biz khusus haji: 2 halaman umroh dialihkan ke elharamainwisata.com (keputusan pemilik 2026-11-04 "paket umroh redirect saja").
Endpoint Rank Math updateRedirection menjawab "dibuat" tapi tidak menyimpan apa pun (sama seperti di elharamainhaji.com), dan
tidak ada ability untuk membuat redirect, jadi dipakai pengalihan instan di halaman (meta refresh 0 + JS) + Rank Math noindex
& canonical ke tujuan. Redirect 301 sejati bisa ditambah manual di wp-admin > Rank Math > Redirections.
Cadangan isi asli: backup/2026-11-04_hajibiz_pages/778-*.json, 135-*.json. Kredensial env WP_HAJIBIZ_USER / WP_HAJIBIZ_PASS."""
import base64, json, os, subprocess

AUTH = 'Basic ' + base64.b64encode(f"{os.environ['WP_HAJIBIZ_USER']}:{os.environ['WP_HAJIBIZ_PASS']}".encode()).decode()
TUJUAN = {778: 'https://elharamainwisata.com/paket-umroh-musim-dingin/',  # Paket Umroh Desember 2026
          135: 'https://elharamainwisata.com/'}                          # Paket Umroh Saudia Landing Jeddah


def curl(method, path, data=None):
    cmd = ['curl', '-sS', '-X', method, '-H', 'Authorization: ' + AUTH, '-H', 'User-Agent: Mozilla/5.0 eh-admin',
           '-H', 'Content-Type: application/json', '-w', '\n%{http_code}', 'https://haji.biz/wp-json' + path]
    if data is not None:
        cmd[1:1] = ['--data-binary', '@-']
    out = subprocess.run(cmd, input=json.dumps(data).encode() if data is not None else None, capture_output=True).stdout.decode()
    body, code = out.rsplit('\n', 1)
    return int(code), body[:200]


for pid, url in TUJUAN.items():
    isi = (f'<!-- wp:html -->\n<meta http-equiv="refresh" content="0;url={url}">'
           f'<script>location.replace({json.dumps(url)});</script>'
           f'<p style="text-align:center;padding:60px 20px;font-family:sans-serif">Halaman ini sudah pindah ke '
           f'<a href="{url}">{url}</a>.</p>\n<!-- /wp:html -->')
    print(pid, 'isi', curl('POST', f'/wp/v2/pages/{pid}', {'content': isi, 'meta': {'_elementor_edit_mode': ''}})[0])
    print(pid, 'seo', curl('POST', '/rankmath/v1/updateMeta', {'objectID': pid, 'objectType': 'post',
                                                               'meta': {'rank_math_robots': ['noindex', 'follow'], 'rank_math_canonical_url': url}}))
print('hapus cache Elementor', curl('DELETE', '/elementor/v1/cache')[0])
