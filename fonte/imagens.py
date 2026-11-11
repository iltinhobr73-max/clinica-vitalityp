"""Padroniza as fotos do Vitality. Retrato 4:5 (480x600) | Paisagem 3:2 (480x320). Saída na raiz, em WebP + JPG."""
import sys
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
SRC, OUT = sys.argv[1], sys.argv[2]
P, L = (480, 600), (480, 320)
def box(w, h, ratio, cx=0.5, cy=0.5):
    if w / h > ratio: nw, nh = h * ratio, h
    else: nw, nh = w, w / ratio
    x = (w - nw) * cx; y = (h - nh) * cy
    return tuple(round(v) for v in (x, y, x + nw, y + nh))
JOBS = {  # nome: (arquivo, formato, centro x, centro y)
 "vt-bolas":     ("10.png", P, 0.5, 0.55),
 "vt-cadillac":  ("11.png", P, 0.6, 0.5),
 "vt-sala":      ("12.png", L, 0.5, 0.5),
 "vt-reformer":  ("13.png", P, 0.5, 0.45),
 "vt-estudio":   ("14.png", P, 0.5, 0.35),
 "vt-entrada":   ("15.png", P, 0.5, 0.25),
 "vt-predio":    ("16.png", L, 0.5, 0.5),
}
for name, (f, size, cx, cy) in JOBS.items():
    im = Image.open(f"{SRC}/{f}").convert("RGB")
    im = im.crop(box(*im.size, size[0] / size[1], cx, cy)).resize(size, Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=40, threshold=2))
    im.save(f"{OUT}/{name}.webp", "WEBP", quality=84, method=6)
    im.save(f"{OUT}/{name}.jpg", "JPEG", quality=86, optimize=True, progressive=True)
# fundo do hero: sala ampla, desfocada (o CSS cobre com a cor da marca)
bg = Image.open(f"{SRC}/12.png").convert("RGB").resize((1600, 1146), Image.LANCZOS).crop((0, 123, 1600, 1023))
bg = ImageEnhance.Contrast(ImageOps.grayscale(bg).filter(ImageFilter.GaussianBlur(5))).enhance(1.1).convert("RGB")
bg.save(f"{OUT}/vt-fundo.webp", "WEBP", quality=60, method=6)
print("ok", len(JOBS) + 1)
