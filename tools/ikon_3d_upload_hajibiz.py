"""Unggah wordpress/ikon-3d/*.webp ke Media WordPress haji.biz (nama ikon-eh-<slug>.webp), simpan peta di
wordpress/ikon-3d/media-hajibiz.json. Kredensial dari env WP_HAJIBIZ_USER / WP_HAJIBIZ_PASS (curl; hosting menolak urllib)."""
import base64, glob, json, os, subprocess, time

DIR = os.path.join(os.path.dirname(__file__), '..', 'wordpress', 'ikon-3d')
AUTH = 'Basic ' + base64.b64encode(f"{os.environ['WP_HAJIBIZ_USER']}:{os.environ['WP_HAJIBIZ_PASS']}".encode()).decode()
BASE = 'https://haji.biz/wp-json/wp/v2'
peta_f = os.path.join(DIR, 'media-hajibiz.json')
peta = json.load(open(peta_f)) if os.path.exists(peta_f) else {}
from ikon_3d_upload import ALT  # alt text sama dengan elharamainwisata.com


def curl(*args):
    out = subprocess.run(['curl', '-sS', '-H', 'Authorization: ' + AUTH, '-H', 'User-Agent: Mozilla/5.0 eh-admin', *args],
                         capture_output=True).stdout.decode()
    return json.loads(out)


for p in sorted(glob.glob(os.path.join(DIR, '*.webp'))):
    slug = os.path.basename(p)[:-5]
    if slug in peta:
        continue
    ada = [m for m in curl(f'{BASE}/media?search=ikon-eh-{slug}&_fields=id,slug,source_url') if m.get('slug') == f'ikon-eh-{slug}']
    if ada:
        peta[slug] = {'id': ada[0]['id'], 'url': ada[0]['source_url']}
    else:
        m = curl('-X', 'POST', '-H', 'Content-Type: image/webp', '-H', f'Content-Disposition: attachment; filename="ikon-eh-{slug}.webp"',
                 '--data-binary', '@' + p, f'{BASE}/media')
        curl('-X', 'POST', '-H', 'Content-Type: application/json', '--data', json.dumps({'alt_text': ALT.get(slug, ''), 'title': ALT.get(slug, slug)}),
             f'{BASE}/media/{m["id"]}')
        peta[slug] = {'id': m['id'], 'url': m['source_url']}
        print(slug, m['id'], m['source_url'])
        time.sleep(2)
    json.dump(peta, open(peta_f, 'w'), indent=1)
print(len(peta), 'ikon di media haji.biz')
