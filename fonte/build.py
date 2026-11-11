#!/usr/bin/env python3
"""Gera o site do Vitality Pilates e Fisioterapia na raiz do repositório.
Uso: python3 fonte/build.py
Todos os arquivos ficam soltos na raiz (sem subpastas), para que o envio pelo
navegador ao GitHub não quebre os caminhos."""
import json
import re
from pathlib import Path
from urllib.parse import quote

OUT = Path(__file__).parent.parent

# ───────────────────────────── DADOS ─────────────────────────────
DOMINIO = "https://SEU-DOMINIO.com.br"   # trocar pelo endereço final
NOME = "Vitality Pilates e Fisioterapia"
FONE_EXIBE = "(85) 99651-5199"
FONE_TEL = "+5585996515199"
WHATS = "5585996515199"                  # confirmar se este número é o WhatsApp
RUA = "R. Carlos Studart, 640, sala 108"
BAIRRO = "Maraponga, Fortaleza - CE"
CEP = "60711-180"
NOTA, N_AVAL = "5,0", 22
MAPS_Q = "Vitality Pilates e Fisioterapia, R. Carlos Studart, 640 - Sl 108 - Maraponga, Fortaleza - CE, 60711-180"
MAPS_ROTA = "https://www.google.com/maps/dir/?api=1&destination=" + quote(MAPS_Q)
MAPS_VER = "https://www.google.com/maps/search/?api=1&query=" + quote(MAPS_Q)
MAPS_EMBED = "https://www.google.com/maps?q=" + quote(MAPS_Q) + "&z=16&output=embed"
AVALIACOES = [
    "Ambiente aconchegante, agradável e excelente profissional. Atendimento vip.",
    "Relação custo-benefício em relação ao preço excelente!",
    "Muito dedicada no que faz, atenciosa e prestativa com os alunos.",
]
# ─────────────────────────────────────────────────────────────────

WA_ICON = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2a9.9 9.9 0 0 0-8.46 15.03L2 22l5.1-1.54A9.9 9.9 0 1 0 12.04 2Zm0 1.8a8.1 8.1 0 1 1-4.3 14.96l-.3-.19-3.03.92.94-2.94-.2-.31A8.1 8.1 0 0 1 12.04 3.8Zm-3.4 3.9c-.2 0-.5.07-.76.36-.26.28-1 .98-1 2.38 0 1.4 1.02 2.76 1.17 2.95.14.19 2 3.06 4.86 4.29 2.38 1.02 2.87.82 3.39.77.51-.05 1.66-.68 1.9-1.33.23-.66.23-1.22.16-1.34-.07-.12-.26-.19-.54-.33-.29-.14-1.67-.82-1.93-.92-.26-.09-.45-.14-.64.14-.19.29-.73.92-.9 1.11-.16.19-.33.21-.61.07-.29-.14-1.2-.44-2.29-1.41a8.6 8.6 0 0 1-1.58-1.97c-.17-.28-.02-.44.12-.58.13-.12.29-.33.43-.49.14-.17.19-.29.28-.48.1-.19.05-.35-.02-.5-.07-.13-.63-1.55-.88-2.12-.22-.52-.45-.53-.64-.54l-.52-.06Z"/></svg>')


def wa(msg):
    return f"https://wa.me/{WHATS}?text={quote(msg)}"


def photo(name, alt, shape, caption="", eager=False):
    w, h = (480, 600) if shape == "p" else (480, 320)
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    dec = "" if eager else ' decoding="async"'
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return (f'<figure class="photo photo--{shape}"><picture><source srcset="{name}.webp" type="image/webp">'
            f'<img src="{name}.jpg" alt="{alt}" width="{w}" height="{h}" {load}{dec}></picture>{cap}</figure>')


ALT = {
    "vt-reformer": "Aparelhos de Pilates em madeira com estofado roxo, sobre piso claro",
    "vt-cadillac": "Cadillac e Reformers de Pilates em madeira, com alças e molas",
    "vt-estudio": "Vista do estúdio com aparelhos de Pilates, espelho e iluminação quente no teto",
    "vt-bolas": "Área de solo com tatame, estante de acessórios e bolas de Pilates",
    "vt-sala": "Sala do estúdio com aparelhos de madeira, tatame e estante com bolas",
    "vt-entrada": "Entrada da sala com o letreiro Vitality Pilates e Fisioterapia",
    "vt-predio": "Fachada do prédio comercial onde fica o estúdio, com vagas na frente",
}

NAV = [("index.html", "Início"), ("pilates.html", "Pilates"), ("fisioterapia.html", "Fisioterapia"), ("contato.html", "Contato")]


def nav_items(current, skip_home=False):
    return "".join(
        f'<li><a href="{h}"{" aria-current=" + chr(34) + "page" + chr(34) if h == current else ""}>{l}</a></li>'
        for h, l in NAV if not (skip_home and h == "index.html"))


VIZINHOS = ["Mondubim", "Jardim Cearense", "Parangaba"]   # bairros vizinhos à Maraponga

FAQ = [
    ("Onde fica o Vitality?", f"Na {RUA}, na Maraponga, em Fortaleza. Procure o letreiro roxo na entrada da sala 108."),
    ("Nunca fiz Pilates. Posso começar?", "Pode. Os exercícios são adaptados ao seu nível, e as molas dos aparelhos ajudam ou desafiam o movimento conforme a necessidade."),
    ("Qual a diferença entre Pilates e fisioterapia?", "A fisioterapia avalia e trata dores, lesões e limitações de movimento. O Pilates é um método de exercícios que trabalha força, postura e flexibilidade. Os dois podem andar juntos."),
    ("O que devo vestir?", "Roupa confortável, que permita se movimentar com liberdade."),
    ("Como eu agendo?", f"Pelo WhatsApp ou por telefone, no {FONE_EXIBE}. Diga se procura Pilates ou fisioterapia e combinamos o horário."),
]


def json_ld(page, crumb=None):
    negocio = {
        "@context": "https://schema.org", "@type": ["HealthAndBeautyBusiness", "Physiotherapy"],
        "@id": DOMINIO + "/#negocio",
        "name": NOME,
        "description": "Estúdio de Pilates e fisioterapia na Maraponga, em Fortaleza, com aulas nos aparelhos e atendimento individual.",
        "image": [f"{DOMINIO}/vt-estudio.jpg", f"{DOMINIO}/vt-entrada.jpg"],
        "url": DOMINIO + "/", "telephone": FONE_TEL,
        "address": {"@type": "PostalAddress", "streetAddress": RUA, "addressLocality": "Fortaleza",
                    "addressRegion": "CE", "postalCode": CEP, "addressCountry": "BR"},
        "areaServed": [{"@type": "Place", "name": n + ", Fortaleza"} for n in ["Maraponga"] + VIZINHOS],
        "knowsAbout": ["Pilates", "Pilates nos aparelhos", "Fisioterapia"],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Serviços", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Pilates", "url": f"{DOMINIO}/pilates.html"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Fisioterapia", "url": f"{DOMINIO}/fisioterapia.html"}}]},
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "bestRating": "5", "reviewCount": N_AVAL},
        "contactPoint": {"@type": "ContactPoint", "telephone": FONE_TEL, "contactType": "agendamento", "availableLanguage": "Portuguese"},
        "hasMap": MAPS_VER,
        # Completar quando confirmado: "openingHoursSpecification" (horários) e "geo" (latitude e longitude).
    }
    blocos = [negocio]
    if page == "index.html":
        blocos.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in FAQ]})
    if crumb:
        blocos.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": DOMINIO + "/"},
            {"@type": "ListItem", "position": 2, "name": crumb, "item": f"{DOMINIO}/{page}"}]})
    return json.dumps(blocos, ensure_ascii=False, indent=2)


def layout(page, title, desc, body, wa_msg, crumb=None):
    w = wa(wa_msg)
    url = f"{DOMINIO}/{'' if page == 'index.html' else page}"
    html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#2e1541">
<meta name="geo.region" content="BR-CE">
<meta name="geo.placename" content="Maraponga, Fortaleza">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="{NOME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMINIO}/vt-estudio.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preload" href="bricolage.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="hanken.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="style.css">
<script>document.documentElement.classList.add("js")</script>
<script type="application/ld+json">
{json_ld(page, crumb)}
</script>
</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>

<header class="site-header" data-header>
  <div class="wrap header-in">
    <a class="brand" href="index.html" aria-label="Vitality Pilates e Fisioterapia, página inicial">
      <span class="brand-mark">Vitality</span><span class="brand-sub">Pilates e Fisioterapia</span>
    </a>
    <nav class="nav" aria-label="Principal"><ul>{nav_items(page, skip_home=True)}</ul></nav>
    <a class="btn btn--plum btn--sm header-cta" href="{w}" target="_blank" rel="noopener">Agendar pelo WhatsApp</a>
    <button class="menu-btn" type="button" data-menu-btn aria-expanded="false" aria-controls="menu"><span data-menu-label>Menu</span><i aria-hidden="true"></i></button>
  </div>
</header>

<div class="menu" id="menu">
  <nav aria-label="Menu"><ul class="menu-links">{nav_items(page)}</ul></nav>
  <div class="menu-foot">
    <a class="btn btn--plum" href="{w}" target="_blank" rel="noopener">{WA_ICON}Agendar pelo WhatsApp</a>
    <p>{RUA}<br>{BAIRRO}<br><a href="tel:{FONE_TEL}">{FONE_EXIBE}</a></p>
  </div>
</div>

<main id="conteudo">
{body}
</main>

<footer class="site-footer">
  <div class="wrap grid">
    <div class="footer-brand">
      <span class="brand-mark">Vitality</span>
      <p>Estúdio de Pilates e fisioterapia na Maraponga, em Fortaleza.</p>
    </div>
    <div class="footer-col">
      <h2>Onde estamos</h2>
      <address>{RUA}<br>{BAIRRO}<br>CEP {CEP}</address>
      <p style="margin-top:.75rem"><a href="{MAPS_ROTA}" target="_blank" rel="noopener">Abrir rota no mapa</a></p>
    </div>
    <div class="footer-col">
      <h2>Contato</h2>
      <ul>
        <li><a href="tel:{FONE_TEL}">{FONE_EXIBE}</a></li>
        <li><a href="{w}" target="_blank" rel="noopener">WhatsApp</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h2>Páginas</h2>
      <ul>{nav_items(page)}</ul>
    </div>
  </div>
  <div class="wrap"><p class="footer-legal">© 2026 {NOME}. Todos os direitos reservados.</p></div>
</footer>

<div class="dock" data-dock>
  <a class="btn btn--wood" href="{w}" target="_blank" rel="noopener">{WA_ICON}WhatsApp</a>
  <a class="btn btn--ghost" href="tel:{FONE_TEL}">Ligar</a>
</div>

<script src="main.js" defer></script>
</body>
</html>
"""
    head, rest = html.split("</head>", 1)

    def tidy(m):  # sem quebras ruins no endereço; só em texto visível, nunca em atributos
        t = m.group(0)
        return t.replace("sala 108", "sala&nbsp;108").replace("Fortaleza - CE", "Fortaleza&nbsp;-&nbsp;CE").replace(CEP, f'<span class="nw">{CEP}</span>')
    return head + "</head>" + re.sub(r">[^<]+<", tidy, rest)


def cta(titulo, texto, msg=None):
    wp = wa("Olá! Vi o site do Vitality e quero saber mais sobre as aulas de Pilates.")
    wf = wa("Olá! Vi o site do Vitality e quero agendar uma avaliação de fisioterapia.")
    return f"""
<section class="cta" id="agendar" aria-labelledby="cta-t">
  <div class="wrap">
    <div class="cta-box reveal">
      <div class="cta-main">
        <span class="eyebrow">Agendamento</span>
        <h2 id="cta-t">{titulo}</h2>
        <p>{texto}</p>
        <div class="cta-actions">
          <a class="btn btn--wood" href="{wp}" target="_blank" rel="noopener">{WA_ICON}Quero fazer Pilates</a>
          <a class="btn btn--wood" href="{wf}" target="_blank" rel="noopener">{WA_ICON}Quero fisioterapia</a>
        </div>
        <p class="cta-alt">Prefere falar? Ligue para <a href="tel:{FONE_TEL}">{FONE_EXIBE}</a>.</p>
      </div>
      <div class="cta-side">
        <ul class="cta-points">
          <li><b>Sem formulário</b>A conversa é direto pelo WhatsApp.</li>
          <li><b>Sem compromisso</b>Tire as dúvidas antes de decidir.</li>
          <li><b>{NOTA} no Google</b>{N_AVAL} avaliações de alunos.</li>
        </ul>
        <blockquote class="cta-quote"><p class="quote">{AVALIACOES[2]}</p><span class="quote-src">Avaliação no Google</span></blockquote>
      </div>
    </div>
  </div>
</section>"""


def crumbs(label):
    return f'<nav class="crumbs" aria-label="Você está em"><a href="index.html">Início</a><span aria-hidden="true">/</span><span aria-current="page">{label}</span></nav>'


def onde(alt=False):
    return f"""
<section class="section{' section--alt' if alt else ''}" id="como-chegar" aria-labelledby="onde-t">
  <div class="wrap">
    <div class="grid">
      <div class="where-photos reveal">
        {photo("vt-entrada", ALT["vt-entrada"], "p", "<b>A entrada</b>Procure o letreiro roxo na sala 108.")}
        {photo("vt-predio", ALT["vt-predio"], "l", "<b>O prédio</b>Visto da R. Carlos Studart.")}
      </div>
      <div class="where-body reveal">
        <span class="eyebrow">Como chegar</span>
        <h2 id="onde-t">Na Maraponga, sala 108 da Carlos Studart.</h2>
        <p class="muted" style="margin-top:1rem">Fica perto para quem mora na Maraponga e em bairros vizinhos de Fortaleza, como {", ".join(VIZINHOS[:-1])} e {VIZINHOS[-1]}.</p>
        <dl class="info">
          <div><dt>Endereço</dt><dd><address>{RUA}<br>{BAIRRO}, {CEP}</address></dd></div>
          <div><dt>Telefone</dt><dd><a href="tel:{FONE_TEL}">{FONE_EXIBE}</a></dd></div>
        </dl>
        <div class="actions">
          <a class="btn btn--plum" href="{MAPS_ROTA}" target="_blank" rel="noopener">Abrir rota</a>
          <a class="btn btn--ghost" href="tel:{FONE_TEL}">Ligar</a>
        </div>
      </div>
    </div>
    <div class="map reveal">
      <a class="map-alt" href="{MAPS_VER}" target="_blank" rel="noopener">Ver a localização no Google Maps</a>
      <iframe src="{MAPS_EMBED}" title="Mapa com a localização do Vitality Pilates e Fisioterapia na R. Carlos Studart, Maraponga" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
    </div>
  </div>
</section>"""


def rows(items):
    return '<div class="rows">' + "".join(f'<div class="row grid reveal"><h3>{t}</h3><p>{d}</p></div>' for t, d in items) + "</div>"


# ───────────────────────────── INÍCIO ─────────────────────────────
def page_index():
    msg = "Olá! Vi o site do Vitality e gostaria de agendar um horário."
    faq_html = "".join(f'<details><summary>{q}</summary><div class="answer"><p>{r}</p></div></details>' for q, r in FAQ)
    quotes = "".join(f'<li><blockquote><p class="quote">{q}</p></blockquote><span class="quote-src">Avaliação no Google</span></li>' for q in AVALIACOES)
    body = f"""
<section class="hero on-plum" aria-labelledby="hero-t">
  <div class="wrap grid">
    <div class="hero-text">
      <span class="eyebrow">Estúdio de Pilates e Fisioterapia · Maraponga</span>
      <h1 id="hero-t">Pilates e fisioterapia na Maraponga, em um estúdio <span>aconchegante.</span></h1>
      <p class="lead">Aulas nos aparelhos e atendimento de fisioterapia em Fortaleza, com atenção a cada aluno.</p>
      <div class="hero-actions">
        <a class="btn btn--wood" href="{wa(msg)}" target="_blank" rel="noopener">{WA_ICON}Agendar minha primeira visita</a>
        <a class="link" href="#como-chegar">Como chegar</a>
      </div>
      <p class="hero-rating"><b>{NOTA}</b><span>no Google, com<br>{N_AVAL} avaliações</span></p>
    </div>
    <div class="hero-strip">
      {photo("vt-estudio", ALT["vt-estudio"], "p", eager=True)}
      {photo("vt-cadillac", ALT["vt-cadillac"], "p", eager=True)}
      {photo("vt-bolas", ALT["vt-bolas"], "p", eager=True)}
      {photo("vt-reformer", ALT["vt-reformer"], "p", eager=True)}
    </div>
  </div>
  <div class="wrap">
    <dl class="hero-foot">
      <div><dt>Endereço</dt><dd>{RUA}</dd></div>
      <div><dt>Bairro</dt><dd>Maraponga, Fortaleza</dd></div>
      <div><dt>Telefone</dt><dd>{FONE_EXIBE}</dd></div>
    </dl>
  </div>
</section>

<section class="section" aria-labelledby="caminhos-t">
  <div class="wrap">
    <div class="head grid reveal">
      <div class="head-a">
        <span class="eyebrow">O que fazemos</span>
        <h2 id="caminhos-t">Dois caminhos para cuidar do corpo, na Maraponga.</h2>
      </div>
      <p class="head-b lead">Você pode vir pelo Pilates, pela fisioterapia ou combinar os dois.</p>
    </div>
    <div class="paths">
      <article class="path path--plum reveal">
        <span class="path-k">01 · Pilates</span>
        <h3>Movimento nos aparelhos e no solo.</h3>
        <p>Exercícios para trabalhar força, postura, flexibilidade e respiração, no seu ritmo.</p>
        <ul><li>Cadillac, Reformer, Chair e Barrel</li><li>Bolas, tatame e acessórios</li><li>Exercícios adaptados ao seu nível</li></ul>
        <a class="link" href="pilates.html">Conhecer o Pilates</a>
      </article>
      <article class="path reveal">
        <span class="path-k">02 · Fisioterapia</span>
        <h3>Avaliação e tratamento para o seu caso.</h3>
        <p>Atendimento para dores e limitações de movimento, com um plano explicado em linguagem simples.</p>
        <ul><li>Avaliação individual</li><li>Plano de tratamento</li><li>Exercícios orientados</li></ul>
        <a class="link" href="fisioterapia.html">Conhecer a fisioterapia</a>
      </article>
    </div>
  </div>
</section>

<section class="section section--alt" id="estudio" aria-labelledby="estudio-t">
  <div class="wrap grid band">
    <div class="band-media reveal">{photo("vt-bolas", ALT["vt-bolas"], "p")}{photo("vt-reformer", ALT["vt-reformer"], "p")}</div>
    <div class="band-body reveal">
      <span class="eyebrow">O estúdio</span>
      <h2 id="estudio-t">Aparelhos de madeira, luz quente e espaço para respirar.</h2>
      <ul>
        <li><b>Cadillac</b><span>Maca com barras, alças e molas.</span></li>
        <li><b>Reformer</b><span>Plataforma deslizante com molas.</span></li>
        <li><b>Chair e Barrel</b><span>Para força, equilíbrio e alongamento.</span></li>
        <li><b>Solo</b><span>Tatame, bolas e acessórios.</span></li>
      </ul>
      <a class="link" href="pilates.html#aparelhos">Ver os aparelhos</a>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="comecar-t">
  <div class="wrap">
    <div class="head grid reveal">
      <div class="head-a">
        <span class="eyebrow">Como começar</span>
        <h2 id="comecar-t">Em três passos você já está em movimento.</h2>
      </div>
    </div>
    <ol class="steps">
      <li class="step reveal"><h3>Chame no WhatsApp</h3><p>Diga o que você procura, Pilates ou fisioterapia, e combinamos um horário.</p></li>
      <li class="step reveal"><h3>Primeira visita</h3><p>Conversamos sobre seus objetivos, seu histórico e qualquer dor ou limitação.</p></li>
      <li class="step reveal"><h3>Sua rotina</h3><p>As aulas e sessões são ajustadas conforme você evolui.</p></li>
    </ol>
    <p class="steps-cta reveal"><a class="btn btn--plum" href="{wa(msg)}" target="_blank" rel="noopener">{WA_ICON}Dar o primeiro passo</a><span>Leva um minuto: é só mandar uma mensagem.</span></p>
  </div>
</section>

<section class="section section--alt" aria-labelledby="aval-t">
  <div class="wrap">
    <div class="head grid reveal" style="margin-bottom:0">
      <div class="head-a">
        <span class="eyebrow">Avaliações</span>
        <h2 id="aval-t" class="vh">Avaliações no Google</h2>
        <p class="score"><b>{NOTA}</b><span>Nota no Google, com {N_AVAL} avaliações de alunos.</span></p>
      </div>
      <p class="head-b"><a class="link" href="{MAPS_VER}" target="_blank" rel="noopener">Ver todas no Google</a></p>
    </div>
    <ul class="quotes reveal">{quotes}</ul>
  </div>
</section>

{onde()}

<section class="section" style="padding-top:0" aria-labelledby="faq-t">
  <div class="wrap grid">
    <div class="faq-head reveal">
      <span class="eyebrow">Dúvidas</span>
      <h2 id="faq-t">Perguntas frequentes.</h2>
    </div>
    <div class="faq-list reveal">
      {faq_html}
    </div>
  </div>
</section>

{cta("Sua primeira visita começa com uma mensagem.", "Diga se você procura Pilates ou fisioterapia e conte o que precisa. A gente tira as suas dúvidas e combina o melhor horário.")}
"""
    return layout("index.html", "Pilates e Fisioterapia na Maraponga, Fortaleza | Vitality",
                  "Estúdio de Pilates e fisioterapia na Maraponga, em Fortaleza. Aulas nos aparelhos, atendimento atencioso e nota 5,0 no Google. Agende pelo WhatsApp.", body, msg)


# ───────────────────────────── PILATES ─────────────────────────────
def page_pilates():
    msg = "Olá! Vi o site do Vitality e gostaria de agendar uma aula de Pilates."
    body = f"""
<section class="page-hero">
  <div class="wrap">
    {crumbs("Pilates")}
    <div class="grid">
      <div class="page-hero-text">
        <h1>Pilates na Maraponga, nos aparelhos e no seu ritmo.</h1>
        <p class="lead">Um método de exercícios que trabalha o corpo inteiro com controle, respiração e atenção à postura.</p>
        <a class="btn btn--plum" href="{wa(msg)}" target="_blank" rel="noopener">{WA_ICON}Agendar uma aula</a>
      </div>
      <div class="page-hero-media">
        {photo("vt-cadillac", ALT["vt-cadillac"], "p", eager=True)}
        {photo("vt-estudio", ALT["vt-estudio"], "p", eager=True)}
      </div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0" aria-label="Sobre o Pilates">
  <div class="wrap">
    {rows([
      ("O que é", "O Pilates é um método de exercícios feito nos aparelhos e no solo. As molas oferecem resistência ou apoio, e cada movimento é feito com controle e respiração."),
      ("Para quem", "Para quem quer ganhar força, melhorar a postura e a flexibilidade ou sair do sedentarismo. Se você tem alguma dor ou lesão, conte antes da aula para que os exercícios sejam adaptados."),
      ("Como é a aula", "Você passa por diferentes aparelhos e pelo solo. A carga e a dificuldade mudam conforme você evolui, e a execução é acompanhada de perto."),
      ("O que vestir", "Roupa confortável, que permita se movimentar com liberdade."),
    ])}
  </div>
</section>

<section class="section section--alt" id="aparelhos" aria-labelledby="ap-t">
  <div class="wrap">
    <div class="head grid reveal">
      <div class="head-a">
        <span class="eyebrow">O estúdio</span>
        <h2 id="ap-t">Os aparelhos que você vai usar.</h2>
      </div>
    </div>
    <div class="tiles">
      <div class="reveal">{photo("vt-cadillac", ALT["vt-cadillac"], "p", "<b>Cadillac</b>Maca com barras, alças e molas.")}</div>
      <div class="reveal">{photo("vt-reformer", ALT["vt-reformer"], "p", "<b>Reformer</b>Plataforma deslizante com molas.")}</div>
      <div class="reveal">{photo("vt-estudio", ALT["vt-estudio"], "p", "<b>Chair e Barrel</b>Para força, equilíbrio e alongamento.")}</div>
      <div class="reveal">{photo("vt-bolas", ALT["vt-bolas"], "p", "<b>Solo</b>Tatame, bolas e acessórios.")}</div>
    </div>
  </div>
</section>

{cta("Venha conhecer o estúdio e fazer a sua primeira aula.", "Mande uma mensagem dizendo os dias e horários que funcionam para você. A gente combina o resto.")}
"""
    return layout("pilates.html", "Pilates nos aparelhos na Maraponga, Fortaleza | Vitality",
                  "Aulas de Pilates nos aparelhos e no solo na Maraponga, em Fortaleza: Cadillac, Reformer, Chair e Barrel. Agende a sua primeira aula pelo WhatsApp.", body, msg, crumb="Pilates")


# ─────────────────────────── FISIOTERAPIA ───────────────────────────
def page_fisio():
    msg = "Olá! Vi o site do Vitality e gostaria de agendar uma avaliação de fisioterapia."
    body = f"""
<section class="page-hero">
  <div class="wrap">
    {crumbs("Fisioterapia")}
    <div class="grid page-hero--text">
      <div class="page-hero-text">
        <h1>Fisioterapia na Maraponga, com avaliação e plano para o seu caso.</h1>
        <p class="lead">O atendimento começa por entender o que você sente, como é a sua rotina e o que você quer voltar a fazer.</p>
        <a class="btn btn--plum" href="{wa(msg)}" target="_blank" rel="noopener">{WA_ICON}Agendar avaliação</a>
      </div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0" aria-label="Como funciona a fisioterapia">
  <div class="wrap">
    {rows([
      ("Avaliação", "Uma conversa sobre a sua história e a sua rotina, seguida de testes de movimento, força e postura. Se tiver exames ou pedido médico, traga."),
      ("Plano de tratamento", "Você fica sabendo o que foi encontrado, o que será feito e por quê, em linguagem simples."),
      ("Sessões", "O tratamento combina exercícios orientados e técnicas de fisioterapia, e é ajustado conforme o corpo responde."),
      ("Fisioterapia e Pilates", "No mesmo espaço há um estúdio de Pilates completo. Quando faz sentido, os exercícios nos aparelhos entram como parte ou como continuidade do tratamento."),
    ])}
  </div>
</section>

<section class="section section--alt" aria-labelledby="fx-t">
  <div class="wrap grid band">
    <div class="band-media reveal">{photo("vt-estudio", ALT["vt-estudio"], "p")}{photo("vt-bolas", ALT["vt-bolas"], "p")}</div>
    <div class="band-body reveal">
      <span class="eyebrow">O espaço</span>
      <h2 id="fx-t">Um ambiente calmo para se cuidar.</h2>
      <p>O atendimento acontece no estúdio da sala 108, com aparelhos, tatame e acessórios à disposição.</p>
      <a class="link" href="pilates.html#aparelhos">Ver os aparelhos</a>
    </div>
  </div>
</section>

{cta("Conte o que você está sentindo. A gente começa por aí.", "Mande uma mensagem explicando a sua queixa. A gente tira as dúvidas e agenda a sua avaliação.")}
"""
    return layout("fisioterapia.html", "Fisioterapia na Maraponga, Fortaleza | Vitality",
                  "Fisioterapia na Maraponga, em Fortaleza, com avaliação individual e plano de tratamento explicado. Agende a sua avaliação pelo WhatsApp.", body, msg, crumb="Fisioterapia")


# ───────────────────────────── CONTATO ─────────────────────────────
def page_contato():
    msg = "Olá! Vi o site do Vitality e gostaria de agendar um horário."
    body = f"""
<section class="page-hero" style="padding-bottom:clamp(2rem,4vw,3.5rem)">
  <div class="wrap">
    {crumbs("Contato")}
    <div class="grid page-hero--text">
      <div class="page-hero-text">
        <h1>Fale com a gente.</h1>
        <p class="lead">O caminho mais rápido para agendar é o WhatsApp. Se preferir, ligue ou passe no estúdio.</p>
      </div>
    </div>
  </div>
</section>

<section aria-label="Canais de contato">
  <div class="wrap">
    <ul class="channels reveal">
      <li class="channel"><a href="{wa(msg)}" target="_blank" rel="noopener"><span class="k">WhatsApp</span><span class="big">Agendar um horário</span><span class="note">{FONE_EXIBE}</span></a></li>
      <li class="channel"><a href="tel:{FONE_TEL}"><span class="k">Telefone</span><span class="big">{FONE_EXIBE}</span><span class="note">Toque para ligar</span></a></li>
      <li class="channel"><a href="{MAPS_ROTA}" target="_blank" rel="noopener"><span class="k">Endereço</span><span class="big">{RUA}</span><span class="note">{BAIRRO}</span></a></li>
    </ul>
  </div>
</section>

{onde()}

{cta("Um recado no WhatsApp já resolve.", "Diga o que você procura e a gente combina o melhor horário.")}
"""
    return layout("contato.html", "Contato e endereço na Maraponga | Vitality Pilates",
                  "Agende pelo WhatsApp (85) 99651-5199. R. Carlos Studart, 640, sala 108, Maraponga, Fortaleza - CE. Veja como chegar.", body, msg, crumb="Contato")


PAGES = {"index.html": page_index, "pilates.html": page_pilates, "fisioterapia.html": page_fisio, "contato.html": page_contato}
FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#4b2468"/>'
           '<text x="32" y="46" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" font-size="40" fill="#fbf8f4">V</text></svg>')

if __name__ == "__main__":
    for name, fn in PAGES.items():
        (OUT / name).write_text(fn(), encoding="utf-8")
    (OUT / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    urls = "".join(f"  <url><loc>{DOMINIO}/{'' if n == 'index.html' else n}</loc></url>\n" for n in PAGES)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOMINIO}/sitemap.xml\n", encoding="utf-8")
    print("ok:", ", ".join(PAGES))
