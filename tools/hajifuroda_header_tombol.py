"""hajifuroda.co.id: gaya tombol header "Konsultasi Gratis!" (Astra Header Builder, ast-header-button-1) dibuat senada dengan CTA
halaman (pil hijau WhatsApp + ikon). Permintaan pemilik 2026-11-04 ("untuk tombol header juga kurang cocok, perbaiki").
Dipasang sebagai Astra Pro Advanced Hook (wp_head, seluruh situs) bernama "EH: gaya tombol header", tanpa mengubah Customizer.
Nonaktifkan: ubah status hook itu ke draft (ID disimpan di landing-pages/situs/hajifuroda/header-hook.id).
Kredensial env WP_HAJIFURODA_USER / WP_HAJIFURODA_PASS."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_hajifuroda import hf, P

IDF = os.path.join(os.path.dirname(__file__), '..', 'landing-pages', 'situs', 'hajifuroda', 'header-hook.id')
WA = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path fill='white' d='" + P['chat'] + "'/></svg>")
CSS = f'''<style id="eh-header-tombol">
.ast-header-button-1 .ast-custom-button-link{{text-decoration:none!important}}
.ast-header-button-1 .ast-custom-button{{display:inline-flex!important;align-items:center;gap:8px;background:#1fa855!important;color:#fff!important;
border:0!important;border-radius:999px!important;padding:11px 20px 11px 16px!important;font-family:Poppins,sans-serif!important;font-weight:600!important;
font-size:14.5px!important;line-height:1!important;letter-spacing:0!important;box-shadow:0 8px 20px rgba(31,168,85,.32)!important;transition:transform .2s,background .2s}}
.ast-header-button-1 .ast-custom-button::before{{content:"";width:17px;height:17px;flex:none;background:url("{WA}") center/contain no-repeat}}
.ast-header-button-1 .ast-custom-button:hover{{background:#178a45!important;transform:translateY(-1px)}}
@media(max-width:921px){{.ast-header-button-1 .ast-custom-button{{padding:9px 14px 9px 12px!important;font-size:13.5px!important}}}}
</style>'''

data = {'title': 'EH: gaya tombol header', 'status': 'publish', 'content': CSS,
        'meta': {'ast-advanced-hook-layout': 'hooks', 'ast-advanced-hook-action': 'wp_head', 'ast-advanced-hook-priority': '99',
                 'ast-advanced-hook-location': {'rule': ['basic-global'], 'specific': []}}}
pid = open(IDF).read().strip() if os.path.exists(IDF) else ''
s, r = hf('POST', f'/wp/v2/astra-advanced-hook/{pid}' if pid else '/wp/v2/astra-advanced-hook', data)
print('hook', s, r.get('id') if isinstance(r, dict) else str(r)[:300])
if isinstance(r, dict) and r.get('id'):
    open(IDF, 'w').write(str(r['id']))
    print('meta tersimpan:', {k: v for k, v in r.get('meta', {}).items() if k.startswith('ast-advanced-hook')})
