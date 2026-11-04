"""hajifuroda.co.id: gaya header (bar kaca navy, menu pil + penanda halaman aktif, logo, ikon sosial, tombol menu HP) dan tombol header "Konsultasi Gratis!" (Astra Header Builder, ast-header-button-1) dibuat senada dengan CTA
halaman (pil hijau WhatsApp + ikon). Permintaan pemilik 2026-11-04 ("untuk tombol header juga kurang cocok, perbaiki").
Dipasang sebagai Astra Pro Advanced Hook (wp_head, seluruh situs) bernama "EH: gaya tombol header", tanpa mengubah Customizer.
Nonaktifkan: ubah status hook itu ke draft (ID disimpan di landing-pages/situs/hajifuroda/header-hook.id).
Kredensial env WP_HAJIFURODA_USER / WP_HAJIFURODA_PASS."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_hajifuroda import hf, P

IDF = os.path.join(os.path.dirname(__file__), '..', 'landing-pages', 'situs', 'hajifuroda', 'header-hook.id')
WA = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path fill='white' d='" + P['chat'] + "'/></svg>")
CSS = f'''<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
<style id="eh-header-tombol">
.ast-header-button-1 .ast-custom-button-link{{text-decoration:none!important}}
.ast-header-button-1 .ast-custom-button{{display:inline-flex!important;align-items:center;gap:8px;background:#1fa855!important;color:#fff!important;
border:0!important;border-radius:999px!important;padding:11px 20px 11px 16px!important;font-family:Poppins,sans-serif!important;font-weight:600!important;
font-size:14.5px!important;line-height:1!important;letter-spacing:0!important;box-shadow:0 8px 20px rgba(31,168,85,.32)!important;transition:transform .2s,background .2s}}
.ast-header-button-1 .ast-custom-button::before{{content:"";width:17px;height:17px;flex:none;background:url("{WA}") center/contain no-repeat}}
.ast-header-button-1 .ast-custom-button:hover{{background:#178a45!important;transform:translateY(-1px)}}
@media(max-width:921px){{.ast-header-button-1 .ast-custom-button{{padding:9px 14px 9px 12px!important;font-size:13.5px!important}}}}
/* --- bar header & menu (pemilik 2026-11-04: "header page kurang enak dilihat") --- */
#masthead .ast-primary-header-bar,#masthead .main-header-bar{{background:linear-gradient(180deg,rgba(5,22,56,.82),rgba(5,22,56,.55))!important;
-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);border-bottom:1px solid rgba(255,255,255,.12)!important;box-shadow:0 10px 30px rgba(0,0,0,.12)}}
#masthead .site-primary-header-wrap{{min-height:84px}}
#masthead .custom-logo-link img,#masthead .site-logo-img img{{max-height:62px!important;width:auto!important;filter:drop-shadow(0 4px 10px rgba(0,0,0,.25))}}
#masthead .main-header-menu>.menu-item>.menu-link{{font-family:Poppins,sans-serif!important;font-size:15px!important;font-weight:500!important;color:#fff!important;
padding:10px 18px!important;margin:0 2px;line-height:1!important;border-radius:999px;transition:background .2s,color .2s}}
#masthead .main-header-menu>.menu-item>.menu-link:hover{{background:rgba(255,255,255,.14)!important;color:#fff!important}}
#masthead .main-header-menu>.menu-item>.menu-link .icon-arrow{{display:none!important}}
.home #masthead .menu-item-25681>.menu-link,.page-id-25978 #masthead .menu-item-25682>.menu-link,.page-id-25981 #masthead .menu-item-25683>.menu-link,
.page-id-25794 #masthead .menu-item-25684>.menu-link,.single-post #masthead .menu-item-25684>.menu-link,.archive #masthead .menu-item-25684>.menu-link,
.page-id-25844 #masthead .menu-item-25685>.menu-link{{background:#fff!important;color:#004AAD!important;font-weight:600!important}}
#masthead .ast-header-social-wrap .ast-builder-social-element{{width:36px;height:36px;display:inline-grid!important;place-items:center;border-radius:50%!important;
background:rgba(255,255,255,.12)!important;border:1px solid rgba(255,255,255,.28)!important;margin:0 3px!important;padding:0!important;transition:background .2s}}
#masthead .ast-header-social-wrap .ast-builder-social-element:hover{{background:rgba(255,255,255,.24)!important}}
#masthead .ast-header-social-wrap .ast-builder-social-element svg{{width:15px!important;height:15px!important;fill:#fff!important}}
#masthead .menu-toggle.main-header-menu-toggle{{width:44px!important;height:44px!important;padding:0!important;display:inline-grid!important;place-items:center;
border-radius:12px!important;background:rgba(255,255,255,.14)!important;border:1px solid rgba(255,255,255,.3)!important;box-shadow:none!important}}
#masthead .menu-toggle .mobile-menu-toggle-icon svg,#masthead .menu-toggle svg{{fill:#fff!important;width:20px!important;height:20px!important}}
@media(max-width:921px){{#masthead .site-primary-header-wrap{{min-height:70px}}#masthead .custom-logo-link img,#masthead .site-logo-img img{{max-height:50px!important}}
#masthead .ast-header-social-wrap .ast-builder-social-element{{width:32px;height:32px}}}}
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
