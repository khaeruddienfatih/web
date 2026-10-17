"""Hapus bagian "Kenapa Memilih Elharamain Wisata?" (daftar ikon + foto Ka'bah) dari halaman elharamainwisata.com,
kecuali beranda (7840). Permintaan pemilik 2026-10-17. Cadangan: backup/2026-10-17_hapus_kenapa_memilih/.
Ditambah: bagian "Pembimbing Ibadah Umroh & Haji Elharamain Wisata" (carousel .ehpb), juga kecuali beranda.
Halaman haji 8080/8061 punya bagian berjudul sama tapi desain lain (6 kotak) -> tidak disentuh."""
import json, sys, time
import wp_rest as w

IDS = [9589, 9588, 9587, 9586, 9585, 9584, 9581, 8910, 8909, 8908, 8896, 8869]

def is_kenapa(js):
    return 'Kenapa Memilih Elharamain Wisata' in js and '"icon-list"' in js and 'Assets-LP-Elharamain-Wisata-3' in js

def is_pembimbing(js):
    return 'Pembimbing Ibadah Umroh & Haji Elharamain Wisata' in js and '.ehpb{' in js

def is_target(sec):
    js = json.dumps(sec)
    return is_kenapa(js) or is_pembimbing(js)

for pid in IDS:
    s, d = w.req('GET', f'/wp/v2/pages/{pid}?context=edit&_fields=id,slug,meta')
    data = json.loads(d['meta']['_elementor_data'])
    keep = [e for e in data if not is_target(e)]
    if len(data) == len(keep):
        print(pid, 'LEWATI: ditemukan', len(data) - len(keep)); continue
    s, r = w.req('POST', f'/wp/v2/pages/{pid}', {'meta': {'_elementor_data': json.dumps(keep, ensure_ascii=False)}})
    print(pid, d['slug'], s)
    time.sleep(3)

# hapus cache Elementor (respon kosong -> urllib langsung), lalu isi ulang dengan tools/warm.py
import urllib.request
r = urllib.request.Request(w.BASE + '/elementor/v1/cache', method='DELETE', headers={'Authorization': w.AUTH, 'User-Agent': 'Mozilla/5.0 eh-admin'})
print('hapus cache', urllib.request.urlopen(r, timeout=120).status)
