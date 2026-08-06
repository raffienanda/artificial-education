import math
import os
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "lawang-bandung-promo-90s.mp4"
THUMB = ROOT / "output" / "lawang-bandung-promo-90s-cover.png"
FFMPEG = ROOT / "tmp" / "video-tools" / "node_modules" / "ffmpeg-static" / "ffmpeg.exe"

W, H = 1080, 1920
FPS = 12
DURATION = 90
TOTAL = FPS * DURATION

BLUE = "#0247AB"
SKY = "#459ED6"
GREEN = "#0E9455"
YELLOW = "#F8BF16"
WHITE = "#FFFFFF"
OFF = "#F5F9FF"
DARK = "#08214A"
MUTED = "#D9E8F7"


def font(size, bold=False):
    names = [
        r"C:\Windows\Fonts\seguisb.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for name in names:
        if os.path.exists(name):
            return ImageFont.truetype(name, size)
    return ImageFont.load_default()


F = {
    "hero": font(88, True),
    "h1": font(74, True),
    "h2": font(56, True),
    "body": font(37),
    "body_b": font(38, True),
    "small": font(28),
    "tiny": font(23),
    "badge": font(34, True),
}


def ease(x):
    x = max(0, min(1, x))
    return 1 - pow(1 - x, 3)


def lerp(a, b, t):
    return a + (b - a) * t


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def blend(c1, c2, t):
    a, b = hex_to_rgb(c1), hex_to_rgb(c2)
    return tuple(int(lerp(a[i], b[i], t)) for i in range(3))


def make_gradient_bg():
    img = Image.new("RGB", (W, H), BLUE)
    px = img.load()
    for y in range(H):
        t = y / H
        base = blend(BLUE, SKY, min(1, t * 1.15))
        for x in range(W):
            r = math.hypot((x - W * 0.78) / W, (y - H * 0.18) / H)
            glow = max(0, 1 - r * 2.4) * 0.36
            px[x, y] = blend("#0247AB", "#459ED6", min(1, t * 0.42 + glow))
    return img.convert("RGBA")


BG_CACHE = make_gradient_bg()


def gradient_bg():
    return BG_CACHE.copy()


def text_center(draw, xy, text, font_obj, fill=WHITE, spacing=8):
    lines = text.split("\n")
    y = xy[1]
    for line in lines:
        box = draw.textbbox((0, 0), line, font=font_obj)
        draw.text((xy[0] - (box[2] - box[0]) / 2, y), line, font=font_obj, fill=fill)
        y += box[3] - box[1] + spacing


def wrap(draw, text, font_obj, max_width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        test = (line + " " + word).strip()
        if draw.textlength(test, font=font_obj) <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return "\n".join(lines)


def shadowed_round(draw, xy, radius, fill, shadow=True, outline=None, width=2):
    if shadow:
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(layer)
        sx = (xy[0] + 0, xy[1] + 18, xy[2] + 0, xy[3] + 18)
        sd.rounded_rectangle(sx, radius=radius, fill=(2, 20, 58, 55))
        layer = layer.filter(ImageFilter.GaussianBlur(18))
        draw._image.alpha_composite(layer)
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_pin(draw, x, y, color, scale=1.0):
    r = 18 * scale
    draw.ellipse((x - r, y - r, x + r, y + r), fill=color)
    draw.polygon([(x, y + 34 * scale), (x - 12 * scale, y + 10 * scale), (x + 12 * scale, y + 10 * scale)], fill=color)
    draw.ellipse((x - 6 * scale, y - 6 * scale, x + 6 * scale, y + 6 * scale), fill=WHITE)


def draw_phone(base, x, y, scale=1.0, progress=1.0):
    draw = ImageDraw.Draw(base)
    w, h = int(410 * scale), int(780 * scale)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((x + 16, y + 24, x + w + 16, y + h + 24), radius=int(58 * scale), fill=(0, 0, 0, 80))
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    base.alpha_composite(shadow)
    draw.rounded_rectangle((x, y, x + w, y + h), radius=int(58 * scale), fill=DARK)
    pad = int(24 * scale)
    sx, sy = x + pad, y + pad
    sw, sh = w - pad * 2, h - pad * 2
    draw.rounded_rectangle((sx, sy, sx + sw, sy + sh), radius=int(38 * scale), fill=OFF)
    draw.rounded_rectangle((sx + 34 * scale, sy + 18 * scale, sx + sw - 34 * scale, sy + 60 * scale), radius=int(20 * scale), fill=BLUE)
    draw.text((sx + 56 * scale, sy + 24 * scale), "Lawang Bandung", font=font(int(22 * scale), True), fill=WHITE)

    # Map area
    mx, my = sx + 26 * scale, sy + 86 * scale
    mw, mh = sw - 52 * scale, 310 * scale
    draw.rounded_rectangle((mx, my, mx + mw, my + mh), radius=int(28 * scale), fill="#DFF1FF")
    for i in range(5):
        yy = my + 40 * scale + i * 54 * scale
        draw.line((mx + 20 * scale, yy, mx + mw - 20 * scale, yy + 26 * scale), fill="#B7DDF7", width=int(5 * scale))
    pts = [
        (mx + 70 * scale, my + 230 * scale),
        (mx + 140 * scale, my + 145 * scale),
        (mx + 220 * scale, my + 190 * scale),
        (mx + 295 * scale, my + 80 * scale),
    ]
    shown = max(1, int(1 + progress * (len(pts) - 1)))
    for a, b in zip(pts[:shown], pts[1:shown]):
        draw.line((*a, *b), fill=YELLOW, width=int(7 * scale))
    for idx, (px, py) in enumerate(pts):
        if progress > idx / len(pts):
            draw_pin(draw, px, py, [GREEN, BLUE, YELLOW, SKY][idx], scale=0.58 * scale)

    cards = [
        ("Sekolah", "Zonasi 1.2 km", GREEN),
        ("Museum", "Trip hari ini", BLUE),
        ("AI Planner", "Rute otomatis", YELLOW),
    ]
    cy = my + mh + 28 * scale
    for i, (a, b, c) in enumerate(cards):
        yy = cy + i * 92 * scale
        draw.rounded_rectangle((mx, yy, mx + mw, yy + 70 * scale), radius=int(22 * scale), fill=WHITE)
        draw.ellipse((mx + 18 * scale, yy + 17 * scale, mx + 52 * scale, yy + 51 * scale), fill=c)
        draw.text((mx + 70 * scale, yy + 12 * scale), a, font=font(int(22 * scale), True), fill=DARK)
        draw.text((mx + 70 * scale, yy + 40 * scale), b, font=font(int(18 * scale)), fill="#536B8B")


def draw_feature(draw, x, y, title, sub, color, icon):
    shadowed_round(draw, (x, y, x + 430, y + 145), 28, WHITE, True)
    draw.ellipse((x + 28, y + 32, x + 86, y + 90), fill=color)
    if icon == "pin":
        draw_pin(draw, x + 57, y + 57, WHITE, 0.55)
    elif icon == "book":
        draw.rectangle((x + 43, y + 47, x + 72, y + 78), outline=WHITE, width=4)
        draw.line((x + 57, y + 47, x + 57, y + 78), fill=WHITE, width=3)
    elif icon == "ticket":
        draw.rounded_rectangle((x + 40, y + 50, x + 76, y + 74), radius=6, outline=WHITE, width=4)
    elif icon == "ai":
        draw.ellipse((x + 42, y + 42, x + 75, y + 75), outline=WHITE, width=4)
        draw.line((x + 58, y + 34, x + 58, y + 84), fill=WHITE, width=3)
        draw.line((x + 34, y + 58, x + 84, y + 58), fill=WHITE, width=3)
    draw.text((x + 108, y + 28), title, font=F["body_b"], fill=DARK)
    draw.text((x + 108, y + 78), sub, font=F["small"], fill="#536B8B")


def draw_problem_card(draw, x, y, title, sub, color):
    shadowed_round(draw, (x, y, x + 900, y + 148), 34, WHITE, True)
    draw.rounded_rectangle((x + 30, y + 34, x + 98, y + 102), radius=22, fill=color)
    draw.text((x + 126, y + 28), title, font=F["body_b"], fill=DARK)
    draw.text((x + 126, y + 79), sub, font=F["small"], fill="#536B8B")


def draw_metric(draw, x, y, number, label, color):
    shadowed_round(draw, (x, y, x + 420, y + 220), 36, WHITE, True)
    draw.text((x + 36, y + 32), number, font=F["h2"], fill=color)
    draw.text((x + 36, y + 116), label, font=F["small"], fill="#536B8B")


def draw_logo(draw, x=70, y=64):
    draw.rounded_rectangle((x, y, x + 64, y + 64), radius=18, fill=YELLOW)
    draw.text((x + 82, y + 7), "Lawang Bandung", font=F["body_b"], fill=WHITE)


def scene(t):
    img = gradient_bg()
    draw = ImageDraw.Draw(img)

    # Common motion lines
    for i in range(7):
        x = int((i * 170 + t * 42) % (W + 240)) - 120
        y = 280 + i * 185
        draw.line((x, y, x + 120, y + 58), fill=(255, 255, 255, 32), width=3)

    if t < 10:
        p = ease(t / 10)
        draw_logo(draw)
        text_center(draw, (W / 2, 260 - 30 * (1 - p)), "Lawang\nBandung", F["hero"], WHITE, 2)
        text_center(draw, (W / 2, 520), "Jelajahi Pendidikan &\nEdu-Wisata Bandung", F["h2"], WHITE)
        draw.rounded_rectangle((145, 700, 935, 780), radius=40, fill=YELLOW)
        text_center(draw, (W / 2, 717), "Cari sekolah. Rancang trip. Belajar dari kota.", F["body_b"], DARK)
        draw_phone(img, int(335 + 80 * (1 - p)), 900, 1.0, p)

    elif t < 22:
        lt = t - 10
        p = ease(lt / 12)
        draw_logo(draw)
        draw.text((72, 165), "Masalahnya?", font=F["h1"], fill=WHITE)
        draw.text((72, 270), "Informasi penting masih tersebar,\npadahal keputusan harus cepat.", font=F["body"], fill=OFF, spacing=10)
        cards = [
            ("Cari sekolah", "Zonasi, jalur masuk, dan jarak belum mudah dibandingkan.", GREEN),
            ("Rencana wisata", "Destinasi, tiket, jam buka, dan rute sering terpisah.", BLUE),
            ("Belajar dari kota", "Museum dan sejarah Bandung belum terhubung ke pengalaman belajar.", YELLOW),
        ]
        for i, item in enumerate(cards):
            appear = ease((lt - i * 1.0) / 2.8)
            draw_problem_card(draw, 90, int(525 + i * 195 + 42 * (1 - appear)), *item)
        draw.rounded_rectangle((125, 1245, 955, 1385), radius=44, fill=YELLOW)
        text_center(draw, (W / 2, 1272), "95,2% pengguna butuh\nplatform wisata terintegrasi", F["badge"], DARK)

    elif t < 36:
        lt = t - 22
        p = ease(lt / 14)
        draw_logo(draw)
        draw.text((72, 205), "Semua kebutuhan\nada di satu aplikasi", font=F["h1"], fill=WHITE, spacing=8)
        draw.text((72, 400), "Sekolah, PKBM, kursus, wisata edukatif,\ntiket, dan itinerary otomatis.", font=F["body"], fill=OFF, spacing=10)
        draw_phone(img, int(600 - 60 * (1 - p)), 525, 1.03, p)
        draw.rounded_rectangle((70, 810, 540, 940), radius=32, fill=WHITE)
        draw.text((110, 842), "Berbasis lokasi", font=F["body_b"], fill=BLUE)
        draw.text((110, 895), "Temukan pilihan terdekat\ndan paling relevan.", font=F["small"], fill="#536B8B")
        draw.rounded_rectangle((70, 980, 540, 1110), radius=32, fill=WHITE)
        draw.text((110, 1012), "Rekomendasi AI", font=F["body_b"], fill=GREEN)
        draw.text((110, 1065), "Disesuaikan dengan minat,\nwaktu, dan budget.", font=F["small"], fill="#536B8B")

    elif t < 52:
        lt = t - 36
        draw.text((72, 125), "Fitur yang bikin\nrencana lebih cepat", font=F["h1"], fill=WHITE, spacing=8)
        features = [
            ("Cek Zonasi", "Sekolah terdekat", GREEN, "pin"),
            ("PKBM & Kursus", "Akses pendidikan", SKY, "book"),
            ("Booking Tiket", "Wisata edukatif", BLUE, "ticket"),
            ("AI Trip Planner", "Itinerary otomatis", YELLOW, "ai"),
        ]
        for i, item in enumerate(features):
            row = i // 2
            col = i % 2
            appear = ease((lt - i * 1.3) / 3.2)
            y = int(430 + row * 190 + 40 * (1 - appear))
            x = 70 + col * 510
            draw_feature(draw, x, y, *item)
        draw_phone(img, 335, 1010, 1.0, ease((lt - 5) / 8))

    elif t < 66:
        lt = t - 52
        p = ease(lt / 14)
        draw.text((72, 150), "AI Trip Planner", font=F["h1"], fill=WHITE)
        draw.text((72, 250), "Tentukan minat, budget, tanggal,\nlalu dapatkan rute belajar-wisata.", font=F["body"], fill=OFF, spacing=10)
        # Route card
        shadowed_round(draw, (86, 500, 994, 1115), 48, WHITE, True)
        draw.text((135, 555), "Itinerary hari ini", font=F["h2"], fill=DARK)
        stops = [("Museum Geologi", GREEN), ("Gedung Sate", BLUE), ("Kursus Coding", SKY), ("Tiket Edu-Wisata", YELLOW)]
        for i, (name, color) in enumerate(stops):
            y = 680 + i * 92
            draw.ellipse((145, y, 190, y + 45), fill=color)
            if i < 3:
                draw.line((168, y + 45, 168, y + 90), fill=MUTED, width=6)
            draw.text((220, y - 2), name, font=F["body_b"], fill=DARK)
            draw.text((220, y + 42), "Direkomendasikan berdasarkan lokasi", font=F["tiny"], fill="#536B8B")
        draw_phone(img, int(355), int(1135 - 50 * p), 0.9, p)

    elif t < 78:
        lt = t - 66
        p = ease(lt / 12)
        draw.text((72, 140), "Dibangun untuk\nBandung yang lebih pintar", font=F["h1"], fill=WHITE, spacing=8)
        draw.text((72, 340), "Menggabungkan teknologi, akses pendidikan,\ndan pengalaman wisata edukatif.", font=F["body"], fill=OFF, spacing=10)
        draw_metric(draw, 90, int(570 + 35 * (1 - p)), "SDG 4", "Pendidikan berkualitas\nlebih mudah diakses.", GREEN)
        draw_metric(draw, 570, int(570 + 35 * (1 - p)), "SDG 11", "Kota berkelanjutan\nsebagai ruang belajar.", SKY)
        tech = ["Machine Learning", "Geospatial / LBS", "Flutter", "PostGIS", "Payment Gateway"]
        for i, label in enumerate(tech):
            x = 100 + (i % 2) * 450
            y = 920 + (i // 2) * 112
            draw.rounded_rectangle((x, y, x + 395, y + 76), radius=38, fill=YELLOW if i == 0 else WHITE)
            draw.text((x + 34, y + 20), label, font=F["small"], fill=DARK if i == 0 else BLUE)
        draw_phone(img, 362, 1295, 0.84, p)

    else:
        lt = t - 78
        p = ease(lt / 12)
        draw_logo(draw)
        text_center(draw, (W / 2, 270), "Mulai dari\nLawang Bandung", F["hero"], WHITE, 4)
        text_center(draw, (W / 2, 560), "Satu pintu untuk pendidikan,\nwisata edukatif, dan rencana perjalanan.", F["body"], OFF, 10)
        draw.rounded_rectangle((190, 760, 890, 850), radius=45, fill=YELLOW)
        text_center(draw, (W / 2, 780), "Jelajahi sekarang", F["body_b"], DARK)
        draw_phone(img, int(335), int(980 + 40 * (1 - p)), 1.0, p)
        draw.text((238, 1770), "Machine Learning  •  Geospatial  •  SDG 4 & SDG 11", font=F["small"], fill=WHITE)

    return img.convert("RGB")


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if not FFMPEG.exists():
        raise FileNotFoundError(f"ffmpeg not found: {FFMPEG}")

    cmd = [
        str(FFMPEG),
        "-y",
        "-f",
        "rawvideo",
        "-vcodec",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        f"{W}x{H}",
        "-r",
        str(FPS),
        "-i",
        "-",
        "-an",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        "-crf",
        "20",
        str(OUT),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(TOTAL):
        frame = scene(i / FPS)
        if i == 0:
            frame.save(THUMB)
        proc.stdin.write(frame.tobytes())
    proc.stdin.close()
    code = proc.wait()
    if code != 0:
        raise RuntimeError(f"ffmpeg failed with exit code {code}")
    print(OUT)
    print(THUMB)


if __name__ == "__main__":
    main()
