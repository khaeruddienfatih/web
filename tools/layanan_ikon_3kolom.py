"""Ganti grid foto "Layanan Eksklusif" (12 kartu foto) dengan model 3 kolom ikon gradasi yang sudah live di
/umroh-premium/ (8909, section 824723a). Permintaan pemilik 2026-10-17 ("dari gambar 1 ke no 2").
Beranda (7840) tidak diubah. Cadangan: backup/2026-10-17_layanan_ikon/."""
import copy, json, os, random, time, urllib.request
import wp_rest as w

IDS = [9589, 9588, 9587, 9586, 9585, 9584, 9581, 8910, 8908, 8896, 8869]
BK = os.path.join(os.path.dirname(__file__), '..', 'backup', '2026-10-17_layanan_ikon')
os.makedirs(BK, exist_ok=True)

def page(pid):
    s, d = w.req('GET', f'/wp/v2/pages/{pid}?context=edit&_fields=id,slug,meta')
    return d['slug'], d['meta']['_elementor_data']

def new_ids(e):
    e['id'] = '%07x' % random.randrange(16 ** 7)
    for k in e.get('elements', []):
        new_ids(k)

_, src_raw = page(8909)
src = next(e for e in json.loads(src_raw) if e['id'] == '824723a')

for pid in IDS:
    slug, raw = page(pid)
    open(os.path.join(BK, f'{pid}-{slug}.json'), 'w').write(raw)
    data = json.loads(raw)
    idx = [i for i, e in enumerate(data) if 'Program Ziarah Thaif' in json.dumps(e) and 'class=\\"ehl' not in json.dumps(e)
           and len(json.dumps(e)) > 30000]
    if len(idx) != 1:
        print(pid, slug, 'LEWATI', idx); continue
    sec = copy.deepcopy(src); new_ids(sec)
    data[idx[0]] = sec
    s, r = w.req('POST', f'/wp/v2/pages/{pid}', {'meta': {'_elementor_data': json.dumps(data, ensure_ascii=False)}})
    print(pid, slug, s)
    time.sleep(3)

r = urllib.request.Request(w.BASE + '/elementor/v1/cache', method='DELETE', headers={'Authorization': w.AUTH, 'User-Agent': 'Mozilla/5.0 eh-admin'})
print('hapus cache', urllib.request.urlopen(r, timeout=120).status)
