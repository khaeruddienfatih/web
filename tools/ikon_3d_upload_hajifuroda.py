"""Unggah ikon 3D (wordpress/ikon-3d/*.webp) ke Media hajifuroda.co.id; peta di wordpress/ikon-3d/media-hajifuroda.json.
Pemilik 2026-11-04: "untuk homepage tambahkan icon seperti elharamainwisata". Kredensial env WP_HAJIFURODA_USER / WP_HAJIFURODA_PASS."""
import base64, glob, json, os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(__file__))
from ikon_3d_upload import ALT
from build_hajifuroda import hf

DIR = os.path.join(os.path.dirname(__file__), '..', 'wordpress', 'ikon-3d')
PERLU = sys.argv[1:] or [os.path.basename(p)[:-5] for p in glob.glob(os.path.join(DIR, '*.webp'))]
peta_f = os.path.join(DIR, 'media-hajifuroda.json')
peta = json.load(open(peta_f)) if os.path.exists(peta_f) else {}
auth = 'Basic ' + base64.b64encode(f"{os.environ['WP_HAJIFURODA_USER']}:{os.environ['WP_HAJIFURODA_PASS']}".encode()).decode()
for slug in sorted(PERLU):
    if slug in peta:
        continue
    s, ada = hf('GET', f'/wp/v2/media?search=ikon-eh-{slug}&_fields=id,source_url,slug')
    hit = [m for m in (ada if isinstance(ada, list) else []) if m.get('slug') == f'ikon-eh-{slug}']
    if hit:
        peta[slug] = {'id': hit[0]['id'], 'url': hit[0]['source_url']}
    else:
        out = subprocess.run(['curl', '-sS', '-L', '-X', 'POST', '-H', 'Authorization: ' + auth, '-H', 'User-Agent: Mozilla/5.0 eh-admin',
                              '-H', 'Content-Type: image/webp', '-H', f'Content-Disposition: attachment; filename="ikon-eh-{slug}.webp"',
                              '--data-binary', '@' + os.path.join(DIR, f'{slug}.webp'), 'https://www.hajifuroda.co.id/wp-json/wp/v2/media'],
                             capture_output=True).stdout.decode()
        m = json.loads(out[out.find('{"'):])
        hf('POST', f'/wp/v2/media/{m["id"]}', {'alt_text': ALT.get(slug, ''), 'title': ALT.get(slug, slug)})
        peta[slug] = {'id': m['id'], 'url': m['source_url']}
        print(slug, m['id'])
        time.sleep(1)
    json.dump(peta, open(peta_f, 'w'), indent=1)
print(len(peta), 'ikon di media hajifuroda')
