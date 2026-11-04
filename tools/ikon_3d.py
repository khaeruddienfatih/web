"""Ikon 3D orisinal Elharamain Wisata (SVG, viewBox 96x96) untuk kartu beranda elharamainwisata.com.
Desain sendiri (gradasi biru/emas/hijau/koral + kilap + bayangan), BUKAN salinan ikon situs lain.
Keluaran: wordpress/ikon-3d/<slug>.svg ; render ke WebP 192px lewat tools/ikon_3d_render.mjs.
Jalankan: python3 tools/ikon_3d.py"""
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'wordpress', 'ikon-3d')

PAL = {  # id: (terang, gelap)
    'b': ('#4FB3FF', '#0B4FB3'), 'g': ('#FFE68A', '#E0A112'), 'gr': ('#6BE8A6', '#0F9157'),
    'r': ('#FFA184', '#E1453B'), 'w': ('#FFFFFF', '#D9E4F5'), 'k': ('#4A4F5A', '#121418'),
    'n': ('#2C6FD6', '#06306F'), 's': ('#F7F9FC', '#98A2B3'), 'p': ('#D6ECFF', '#3B7DD8'),
}


def defs():
    g = ''.join(f'<linearGradient id="{k}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/>'
                f'<stop offset="1" stop-color="{b}"/></linearGradient>' for k, (a, b) in PAL.items())
    return (f'<defs>{g}<filter id="bl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>'
            '<filter id="ds" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="3" stdDeviation="2.5" '
            'flood-color="#062a66" flood-opacity=".28"/></filter></defs>')


SHADOW = '<ellipse cx="48" cy="87" rx="25" ry="4.5" fill="#062a66" opacity=".22" filter="url(#bl)"/>'
CHECK = '<polyline points="{x1},{y1} {x2},{y2} {x3},{y3}" fill="none" stroke="#fff" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'


def chk(cx, cy, r, fill='url(#g)'):
    s = r / 12
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="#fff" stroke-width="2.5"/>' +
            CHECK.format(x1=cx - 5 * s, y1=cy, x2=cx - 1 * s, y2=cy + 4 * s, x3=cx + 5.5 * s, y3=cy - 4 * s, w=3.2 * s))


SHINE = '<path d="{d}" fill="#fff" opacity=".28"/>'

IKON = {
    # --- keunggulan (atas) ---
    'izin-resmi': (
        '<path d="M48 9 79 20v23c0 21-13 35-31 43C30 78 17 64 17 43V20z" fill="url(#b)"/>'
        '<path d="M48 16 72 25v18c0 16-10 28-24 35-14-7-24-19-24-35V25z" fill="url(#n)" opacity=".45"/>'
        + SHINE.format(d='M48 13 21 23v19c0 9 3 17 8 23 1-22 8-38 19-52z') +
        CHECK.format(x1=34, y1=46, x2=44, y2=56, x3=63, y3=36, w=8).replace('#fff', '#FFD54A')),
    'rincian-harga': (
        '<rect x="20" y="10" width="46" height="64" rx="7" fill="url(#w)"/>'
        '<rect x="28" y="22" width="30" height="5" rx="2.5" fill="#0B4FB3" opacity=".75"/>'
        '<rect x="28" y="33" width="24" height="4" rx="2" fill="#0B4FB3" opacity=".35"/>'
        '<rect x="28" y="42" width="27" height="4" rx="2" fill="#0B4FB3" opacity=".35"/>'
        '<rect x="28" y="51" width="18" height="4" rx="2" fill="#0B4FB3" opacity=".35"/>'
        '<circle cx="66" cy="64" r="17" fill="url(#g)"/><circle cx="66" cy="64" r="12" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="2"/>'
        '<text x="66" y="69" text-anchor="middle" font-family="Poppins,Arial,sans-serif" font-weight="800" font-size="13" fill="#8A5600">Rp</text>'
        + SHINE.format(d='M56 52a14 14 0 0 1 16-3 17 17 0 0 0-19 9z')),
    'booking-dp': (
        '<rect x="26" y="14" width="42" height="24" rx="4" fill="url(#gr)" transform="rotate(-9 47 26)"/>'
        '<circle cx="47" cy="25" r="5" fill="#fff" opacity=".55" transform="rotate(-9 47 26)"/>'
        '<rect x="14" y="30" width="62" height="46" rx="11" fill="url(#r)"/>'
        '<rect x="56" y="44" width="26" height="18" rx="7" fill="url(#g)"/><circle cx="65" cy="53" r="3.8" fill="#fff"/>'
        + SHINE.format(d='M25 30h40a11 11 0 0 1 9 5H18a11 11 0 0 1 7-5z')),
    'pembimbing': (
        '<circle cx="63" cy="28" r="11" fill="url(#g)"/><path d="M43 74c0-15 8-24 20-24s20 9 20 24z" fill="url(#g)"/>'
        '<circle cx="39" cy="33" r="13" fill="url(#b)"/><path d="M14 82c0-18 11-27 25-27s25 9 25 27z" fill="url(#b)"/>'
        + SHINE.format(d='M31 24a12 12 0 0 1 14-2 13 13 0 0 0-16 9z') + SHINE.format(d='M20 72c2-9 8-14 16-15-7 3-12 8-13 15z')),
    # --- kenapa memilih ---
    'akreditasi': (
        '<path d="M33 50 25 84l11-6 8 9 6-31z" fill="url(#b)"/><path d="M63 50l8 34-11-6-8 9-6-31z" fill="url(#n)"/>'
        '<circle cx="48" cy="38" r="26" fill="url(#g)"/><circle cx="48" cy="38" r="19" fill="#FFF3C4" opacity=".55"/>'
        '<text x="48" y="48" text-anchor="middle" font-family="Poppins,Arial,sans-serif" font-weight="800" font-size="28" fill="#0B4FB3">A</text>'
        + SHINE.format(d='M30 30a20 20 0 0 1 22-14 24 24 0 0 0-24 22z')),
    'hotel-bintang': (
        '<rect x="22" y="30" width="52" height="52" rx="6" fill="url(#b)"/>'
        + ''.join(f'<rect x="{30 + c * 13}" y="{39 + r * 10}" width="8" height="6" rx="1.5" fill="#fff" opacity="{.95 if (r + c) % 2 else .7}"/>'
                  for r in range(3) for c in range(3)) +
        '<rect x="42" y="68" width="12" height="14" rx="2" fill="url(#g)"/>'
        '<path d="M48 4l4.9 9.9 10.9 1.6-7.9 7.7 1.9 10.8L48 28.9l-9.7 5.1 1.9-10.8-7.9-7.7 10.9-1.6z" fill="url(#g)" stroke="#fff" stroke-width="2"/>'
        + SHINE.format(d='M22 36a6 6 0 0 1 6-6h10L22 50z')),
    'satu-rekening': (
        '<rect x="12" y="22" width="58" height="38" rx="7" fill="url(#gr)" transform="rotate(-10 41 41)"/>'
        '<rect x="22" y="34" width="62" height="40" rx="7" fill="url(#b)"/>'
        '<rect x="22" y="43" width="62" height="7" fill="#06306F" opacity=".55"/>'
        '<rect x="30" y="57" width="13" height="10" rx="2" fill="url(#g)"/>'
        '<rect x="48" y="60" width="20" height="4" rx="2" fill="#fff" opacity=".7"/>'
        + SHINE.format(d='M29 34h48a7 7 0 0 1 6 4H23a7 7 0 0 1 6-4z') + chk(76, 72, 11)),
    'cicilan-ringan': (
        '<rect x="16" y="18" width="62" height="60" rx="10" fill="url(#w)"/>'
        '<path d="M26 18h42a10 10 0 0 1 10 10v8H16v-8a10 10 0 0 1 10-10z" fill="url(#r)"/>'
        '<rect x="30" y="11" width="7" height="16" rx="3.5" fill="#55627a"/><rect x="57" y="11" width="7" height="16" rx="3.5" fill="#55627a"/>'
        + ''.join(f'<rect x="{25 + c * 12}" y="{44 + r * 10}" width="7" height="6" rx="1.5" fill="#0B4FB3" opacity=".3"/>'
                  for r in range(3) for c in range(4) if not (r == 2 and c >= 2)) + chk(68, 68, 13)),
    'reschedule': (
        '<path d="M22 46a26 26 0 0 1 44-18" fill="none" stroke="url(#b)" stroke-width="10" stroke-linecap="round"/>'
        '<path d="M58 16l16 10-15 9z" fill="#0B4FB3"/>'
        '<path d="M74 50a26 26 0 0 1-44 18" fill="none" stroke="url(#g)" stroke-width="10" stroke-linecap="round"/>'
        '<path d="M38 80l-16-10 15-9z" fill="#E0A112"/>'
        '<circle cx="48" cy="48" r="10" fill="url(#r)"/><path d="M48 43v5l3.5 2.5" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round"/>'),
    'konsultasi-gratis': (
        '<rect x="14" y="14" width="66" height="48" rx="15" fill="url(#gr)"/><path d="M26 58l-3 22 20-18z" fill="#0F9157"/>'
        '<circle cx="33" cy="38" r="5" fill="#fff"/><circle cx="47" cy="38" r="5" fill="#fff"/><circle cx="61" cy="38" r="5" fill="#fff"/>'
        + SHINE.format(d='M29 14h36a15 15 0 0 1 13 8H17a15 15 0 0 1 12-8z')),
    # --- langkah umroh ---
    'konsultasi': (
        '<rect x="40" y="12" width="44" height="32" rx="12" fill="url(#g)"/><path d="M72 40l6 14-16-10z" fill="#E0A112"/>'
        '<rect x="12" y="30" width="54" height="40" rx="13" fill="url(#b)"/><path d="M24 66l-4 18 18-15z" fill="#0B4FB3"/>'
        '<circle cx="28" cy="50" r="4.2" fill="#fff"/><circle cx="39" cy="50" r="4.2" fill="#fff"/><circle cx="50" cy="50" r="4.2" fill="#fff"/>'
        + SHINE.format(d='M25 30h28a13 13 0 0 1 11 7H15a13 13 0 0 1 10-7z')),
    'booking-seat': (
        '<g transform="rotate(-12 48 48)"><path d="M14 30h68v12a6 6 0 0 0 0 12v12H14V54a6 6 0 0 0 0-12z" fill="url(#g)"/>'
        '<line x1="62" y1="32" x2="62" y2="64" stroke="#fff" stroke-width="2.5" stroke-dasharray="4 4"/>'
        '<path d="M28 52l10-3 9-11 4 1-5 9 9-2 3-4h3l-2 6 2 6h-3l-3-4-9-2 5 9-4 1-9-11z" fill="#0B4FB3" transform="translate(-6 -2)"/>'
        '<rect x="66" y="40" width="10" height="4" rx="2" fill="#fff" opacity=".8"/><rect x="66" y="48" width="8" height="4" rx="2" fill="#fff" opacity=".6"/></g>'),
    'manasik': (
        '<path d="M10 32v48c14-5 26-5 38 0 12-5 24-5 38 0V32z" fill="url(#gr)"/>'
        '<path d="M48 28c-10-6-22-6-33-2v46c11-4 23-4 33 2z" fill="url(#w)"/>'
        '<path d="M48 28c10-6 22-6 33-2v46c-11-4-23-4-33 2z" fill="#EEF3FB"/>'
        + ''.join(f'<path d="M22 {38 + i * 8}c7-2 13-2 20 0" stroke="#0B4FB3" stroke-opacity=".3" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
                  f'<path d="M54 {38 + i * 8}c7-2 13-2 20 0" stroke="#0B4FB3" stroke-opacity=".3" stroke-width="2.5" fill="none" stroke-linecap="round"/>' for i in range(4)) +
        '<path d="M66 24v20l5-4 5 4V26c-3-1-7-2-10-2z" fill="url(#r)"/>'),
    'berangkat': (
        '<ellipse cx="26" cy="72" rx="16" ry="8" fill="#fff" opacity=".85"/><ellipse cx="38" cy="68" rx="11" ry="9" fill="#fff" opacity=".9"/>'
        '<g transform="rotate(40 50 44)"><ellipse cx="50" cy="44" rx="8" ry="34" fill="url(#w)"/>'
        '<path d="M50 36 16 54v7l34-9 34 9v-7z" fill="url(#b)"/><path d="M50 68 37 77v5l13-4 13 4v-5z" fill="url(#n)"/>'
        '<ellipse cx="50" cy="18" rx="4" ry="6" fill="#0B4FB3"/><rect x="47" y="28" width="6" height="30" rx="3" fill="#0B4FB3" opacity=".15"/></g>'),
    'beribadah': (
        '<path d="M20 34 48 24l28 10-28 10z" fill="#5A606C"/>'
        '<path d="M20 34l28 10v40L20 74z" fill="url(#k)"/><path d="M76 34 48 44v40l28-10z" fill="#1E2127"/>'
        '<path d="M20 42l28 10v6L20 48z" fill="url(#g)"/><path d="M76 42 48 52v6l28-10z" fill="#C98F0C"/>'
        '<path d="M60 60l8-3v14l-8 3z" fill="url(#g)" opacity=".9"/>'
        '<path d="M22 37l26 9" stroke="#fff" stroke-opacity=".25" stroke-width="1.5"/>'),
    'pulang': (
        '<path d="M12 48 48 18l36 30-5 5-31-26-31 26z" fill="url(#r)"/>'
        '<path d="M20 47 48 24l28 23v31a4 4 0 0 1-4 4H24a4 4 0 0 1-4-4z" fill="url(#w)"/>'
        '<rect x="41" y="56" width="14" height="26" rx="3" fill="url(#b)"/>'
        '<rect x="62" y="16" width="8" height="16" rx="2" fill="#E1453B"/>'
        '<path d="M30 52c0-4 6-5 6 0 0-5 6-4 6 0 0 4-6 8-6 8s-6-4-6-8z" fill="url(#r)"/>'
        '<rect x="61" y="54" width="9" height="9" rx="2" fill="url(#g)"/>'),
    # --- program umroh ---
    'umroh-januari': (
        '<rect x="18" y="16" width="60" height="64" rx="10" fill="url(#w)"/>'
        '<path d="M28 16h40a10 10 0 0 1 10 10v8H18v-8a10 10 0 0 1 10-10z" fill="url(#b)"/>'
        '<text x="48" y="31" text-anchor="middle" font-family="Poppins,Arial,sans-serif" font-weight="800" font-size="11" fill="#fff" letter-spacing="1">JAN</text>'
        '<text x="48" y="68" text-anchor="middle" font-family="Poppins,Arial,sans-serif" font-weight="800" font-size="30" fill="#0B4FB3">01</text>'
        '<rect x="30" y="10" width="7" height="14" rx="3.5" fill="#55627a"/><rect x="59" y="10" width="7" height="14" rx="3.5" fill="#55627a"/>'
        '<path d="M76 62v20M66 72h20M69 65l14 14M83 65 69 79" stroke="#7FC8FF" stroke-width="3" stroke-linecap="round"/>'),
    'umroh-ramadhan': (
        '<path d="M56 10a34 34 0 1 0 28 54A27 27 0 1 1 56 10z" fill="url(#g)"/>'
        '<path d="M72 20l2.6 5.4 5.9.8-4.3 4.1 1 5.8-5.2-2.8-5.2 2.8 1-5.8-4.3-4.1 5.9-.8z" fill="url(#b)"/>'
        + SHINE.format(d='M40 18a32 32 0 0 0-18 22 34 34 0 0 1 26-27z')),
    'itikaf': (
        '<circle cx="48" cy="11" r="5" fill="none" stroke="#0B4FB3" stroke-width="3"/>'
        '<path d="M32 30 48 15l16 15z" fill="url(#b)"/><rect x="30" y="29" width="36" height="6" rx="3" fill="#0B4FB3"/>'
        '<path d="M33 35h30l-2 30H35z" fill="url(#g)"/><path d="M39 39h18l-1.5 22h-15z" fill="#FFF6C9"/>'
        '<path d="M48 41c4 5 4 9 0 13-4-4-4-8 0-13z" fill="#FFB020"/>'
        '<path d="M43 35v30M53 35v30" stroke="#C98F0C" stroke-width="2"/>'
        '<path d="M30 65h36l-5 10H35z" fill="url(#b)"/><rect x="40" y="75" width="16" height="5" rx="2.5" fill="#0B4FB3"/>'),
    'umroh-syawal': (
        '<path d="M48 6c-4 6-10 7-12 4M48 6c4 6 10 6 13 2" stroke="#0F9157" stroke-width="3" fill="none" stroke-linecap="round"/>'
        '<clipPath id="kt"><path d="M48 18 78 48 48 80 18 48z"/></clipPath>'
        '<path d="M48 18 78 48 48 80 18 48z" fill="url(#gr)"/>'
        '<g clip-path="url(#kt)" stroke="#C9F5DA" stroke-width="5" opacity=".75">'
        + ''.join(f'<line x1="{x}" y1="10" x2="{x + 70}" y2="80"/><line x1="{x + 70}" y1="10" x2="{x}" y2="80"/>' for x in (-22, -6, 10, 26)) +
        '</g><path d="M48 18 78 48 48 80 18 48z" fill="none" stroke="#0F9157" stroke-width="2.5"/>'
        '<path d="M48 18 58 28" stroke="#FFE68A" stroke-width="3" stroke-linecap="round"/>'),

    # --- halaman haji (8289) ---
    'jamaah-umroh': (
        '<circle cx="24" cy="36" r="9" fill="url(#g)"/><path d="M8 74c0-13 7-20 16-20s16 7 16 20z" fill="url(#g)"/>'
        '<circle cx="72" cy="36" r="9" fill="url(#gr)"/><path d="M56 74c0-13 7-20 16-20s16 7 16 20z" fill="url(#gr)"/>'
        '<circle cx="48" cy="30" r="12" fill="url(#b)"/><path d="M26 82c0-17 10-26 22-26s22 9 22 26z" fill="url(#b)"/>'
        + SHINE.format(d='M41 22a11 11 0 0 1 12-2 12 12 0 0 0-14 8z')),
    'pendaftar-haji': (
        '<rect x="18" y="16" width="56" height="66" rx="9" fill="url(#w)"/>'
        '<rect x="34" y="10" width="24" height="12" rx="5" fill="url(#b)"/>'
        '<path d="M32 40 46 35l14 5-14 5z" fill="#5A606C"/><path d="M32 40l14 5v18l-14-5z" fill="url(#k)"/><path d="M60 40 46 45v18l14-5z" fill="#1E2127"/>'
        '<path d="M32 44l14 5v3l-14-5z" fill="url(#g)"/><path d="M60 44 46 49v3l14-5z" fill="#C98F0C"/>'
        '<rect x="28" y="68" width="30" height="4" rx="2" fill="#0B4FB3" opacity=".3"/>' + chk(70, 70, 13)),
    'kantor-cabang': (
        '<path d="M10 70l22-8 32 8 22-8v18l-22 8-32-8-22 8z" fill="url(#gr)" opacity=".9"/>'
        '<path d="M48 8c-15 0-26 11-26 25 0 19 26 43 26 43s26-24 26-43C74 19 63 8 48 8z" fill="url(#r)"/>'
        '<rect x="37" y="20" width="22" height="24" rx="3" fill="#fff"/>'
        + ''.join(f'<rect x="{41 + c * 8}" y="{25 + r * 7}" width="5" height="4" rx="1" fill="#0B4FB3" opacity=".8"/>' for r in range(2) for c in range(2)) +
        '<rect x="45" y="38" width="6" height="6" fill="url(#g)"/>' + SHINE.format(d='M30 22a24 24 0 0 1 16-11 25 25 0 0 0-20 20z')),
    'berpengalaman': (
        '<path d="M28 14h40v18a20 20 0 0 1-40 0z" fill="url(#g)"/>'
        '<path d="M28 20H16v6a14 14 0 0 0 14 14M68 20h12v6a14 14 0 0 1-14 14" fill="none" stroke="#E0A112" stroke-width="5" stroke-linecap="round"/>'
        '<rect x="43" y="50" width="10" height="14" fill="#E0A112"/><rect x="30" y="64" width="36" height="14" rx="4" fill="url(#b)"/>'
        '<path d="M48 20l3 6.2 6.8 1-4.9 4.8 1.2 6.7L48 35.6l-6.1 3.1 1.2-6.7-4.9-4.8 6.8-1z" fill="#fff"/>'
        + SHINE.format(d='M32 14h10c-4 8-5 16-3 26a20 20 0 0 1-7-8z')),
    'reputasi': (
        '<path d="M48 82S14 62 14 38c0-12 9-20 19-20 7 0 12 4 15 9 3-5 8-9 15-9 10 0 19 8 19 20 0 24-34 44-34 44z" fill="url(#r)"/>'
        + SHINE.format(d='M22 30c2-6 7-9 12-9-5 3-8 8-8 15z') +
        ''.join(f'<path d="M{x} {y}l2.4 4.8 5.3.8-3.8 3.7.9 5.3-4.8-2.5-4.8 2.5.9-5.3-3.8-3.7 5.3-.8z" fill="url(#g)" stroke="#fff" stroke-width="1.5"/>'
                for x, y in ((36, 40), (48, 34), (60, 40)))),
    'sajadah': (
        '<rect x="22" y="8" width="52" height="76" rx="6" fill="url(#gr)"/>'
        '<rect x="28" y="14" width="40" height="64" rx="4" fill="none" stroke="#FFE68A" stroke-width="2.5"/>'
        '<path d="M34 72V40c0-9 6-16 14-20 8 4 14 11 14 20v32z" fill="#0F7A4A"/>'
        '<path d="M38 72V42c0-7 4-12 10-15 6 3 10 8 10 15v30z" fill="none" stroke="#FFE68A" stroke-width="2"/>'
        '<circle cx="48" cy="48" r="4" fill="url(#g)"/>'
        + ''.join(f'<line x1="{x}" y1="84" x2="{x}" y2="90" stroke="#0F9157" stroke-width="2.2" stroke-linecap="round"/>' for x in range(26, 74, 6)) +
        SHINE.format(d='M22 14a6 6 0 0 1 6-6h12L22 40z')),
    'rating': (
        '<rect x="10" y="22" width="76" height="44" rx="14" fill="url(#w)"/><path d="M26 62l-4 16 18-14z" fill="#D9E4F5"/>'
        + ''.join(f'<path d="M{x} 35.5l2.9 5.9 6.5.9-4.7 4.6 1.1 6.5-5.8-3.1-5.8 3.1 1.1-6.5-4.7-4.6 6.5-.9z" fill="url(#g)"/>'
                  for x in (20, 34, 48, 62, 76))),
    'tim-solid': (
        '<circle cx="28" cy="34" r="10" fill="url(#gr)"/><path d="M10 74c0-14 8-22 18-22s18 8 18 22z" fill="url(#gr)"/>'
        '<circle cx="68" cy="34" r="10" fill="url(#g)"/><path d="M50 74c0-14 8-22 18-22s18 8 18 22z" fill="url(#g)"/>'
        '<circle cx="48" cy="28" r="12" fill="url(#b)"/><path d="M26 80c0-17 10-26 22-26s22 9 22 26z" fill="url(#b)"/>' + chk(70, 70, 12)),
    'asatidz': (
        '<path d="M12 62v14c12-4 24-4 36 0 12-4 24-4 36 0V62z" fill="url(#gr)"/>'
        '<path d="M48 60c-9-5-20-5-30-2v14c10-3 21-3 30 2z" fill="url(#w)"/><path d="M48 60c9-5 20-5 30-2v14c-10-3-21-3-30 2z" fill="#EEF3FB"/>'
        '<path d="M48 14 86 30 48 46 10 30z" fill="url(#n)"/><path d="M26 37v12c0 5 10 9 22 9s22-4 22-9V37L48 46z" fill="url(#b)"/>'
        '<path d="M80 32v18" stroke="#E0A112" stroke-width="3"/><circle cx="80" cy="52" r="4" fill="url(#g)"/>'
        + SHINE.format(d='M48 17 18 30l8 3z')),
    'kajian': (
        '<path d="M22 84 60 44M74 84 36 44" stroke="url(#r)" stroke-width="7" stroke-linecap="round"/>'
        '<path d="M48 54c-10-8-24-9-36-5V24c12-4 26-3 36 5z" fill="url(#w)"/>'
        '<path d="M48 54c10-8 24-9 36-5V24c-12-4-26-3-36 5z" fill="#EEF3FB"/>'
        '<path d="M8 22v30c14-4 28-3 40 6 12-9 26-10 40-6V22c-2-1-3-1-4-1v28c-12-3-25-2-36 5-11-7-24-8-36-5V21c-1 0-3 0-4 1z" fill="url(#gr)"/>'
        + ''.join(f'<path d="M18 {32 + i * 6}c8-2 15-1 22 3M56 {35 + i * 6}c7-4 14-5 22-3" stroke="#0F9157" stroke-opacity=".45" stroke-width="2" fill="none" stroke-linecap="round"/>' for i in range(3))),
}

for _slug, _pal, _isi in (
        ('medali-silver', 's', '<path d="M48 26l4.4 9 9.9 1.4-7.2 7 1.7 9.8L48 48.6l-8.8 4.6 1.7-9.8-7.2-7 9.9-1.4z" fill="#fff"/>'),
        ('medali-gold', 'g', '<path d="M48 26l4.4 9 9.9 1.4-7.2 7 1.7 9.8L48 48.6l-8.8 4.6 1.7-9.8-7.2-7 9.9-1.4z" fill="#fff"/>'),
        ('medali-arbain', 'g', '<text x="48" y="49" text-anchor="middle" font-family="Poppins,Arial,sans-serif" font-weight="800" font-size="20" fill="#8A5600">40</text>'),
        ('medali-platinum', 'p', '<path d="M48 26l12 12-12 16-12-16z" fill="#fff"/><path d="M36 38h24M48 26l-4 12 4 16 4-16z" stroke="#3B7DD8" stroke-width="1.5" fill="none" opacity=".6"/>')):
    IKON[_slug] = (
        '<path d="M34 54 26 86l11-6 8 9 5-32z" fill="url(#b)"/><path d="M62 54l8 32-11-6-8 9-5-32z" fill="url(#r)"/>'
        f'<circle cx="48" cy="40" r="27" fill="url(#{_pal})" stroke="#fff" stroke-width="2.5"/>'
        f'<circle cx="48" cy="40" r="20" fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="2"/>' + _isi
        + SHINE.format(d='M28 32a22 22 0 0 1 24-16 27 27 0 0 0-27 25z'))

# judul kartu di beranda -> slug ikon
KARTU = {
    'Berizin resmi Kemenag': 'izin-resmi', 'Rincian harga lengkap': 'rincian-harga',
    'Booking seat Rp 6 juta': 'booking-dp', 'Pembimbing sepanjang perjalanan': 'pembimbing',
    'Terdaftar dan terakreditasi': 'akreditasi', 'Fasilitas eksklusif': 'hotel-bintang',
    'Satu nama rekening': 'satu-rekening', 'Tahapan pembayaran ringan': 'cicilan-ringan',
    'Bisa reschedule': 'reschedule', 'Konsultasi gratis': 'konsultasi-gratis',
    'Konsultasi': 'konsultasi', 'Booking seat': 'booking-seat', 'Manasik': 'manasik',
    'Berangkat': 'berangkat', 'Beribadah': 'beribadah', 'Kembali ke tanah air': 'pulang',
    'Umroh Januari 2027': 'umroh-januari', 'Umroh Ramadhan 2027': 'umroh-ramadhan',
    "I'tikaf Ramadhan 17 Hari": 'itikaf', 'Umroh Syawal 2027': 'umroh-syawal',
}


def svg(slug):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" width="96" height="96">{defs()}{SHADOW}'
            f'<g filter="url(#ds)">{IKON[slug]}</g></svg>')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for slug in IKON:
        with open(os.path.join(OUT, f'{slug}.svg'), 'w', encoding='utf-8') as f:
            f.write(svg(slug))
    print(len(IKON), 'ikon ->', os.path.abspath(OUT))
