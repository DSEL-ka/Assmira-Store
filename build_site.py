
#!/usr/bin/env python3
import base64, os, sys

PHOTOS = {
    "green1":"img/IMG_8721.jpeg",
    "green2":"img/IMG_8719.JPG",
    "green3":"img/IMG_8720.JPG",

    "blue1":"img/IMG_8766.jpeg",
    "blue2":"img/IMG_8765.jpeg",
    "blue3":"img/IMG_8767.jpeg",

    "tulip1":"img/IMG_8734.jpeg",
    "tulip2":"img/IMG_8735.JPG",
    "tulip3":"img/IMG_8736.jpeg",

    "dot1":"img/IMG_8722.jpeg",

    "pink1":"img/IMG_8728.jpeg",
    "pink2":"img/IMG_8730.jpeg",
    "pink3":"img/IMG_8729.jpeg",

    "palm1":"img/IMG_8726.jpeg",
    "palm2":"img/IMG_8725.jpeg",
    "palm3":"img/IMG_8727.jpeg",

    "tile1":"img/IMG_8732.JPG",
    "tile2":"img/IMG_8731.JPG",
    "tile3":"img/IMG_8733.JPG",
}

missing=[f for f in PHOTOS.values() if not os.path.exists(f)]
if missing:
    print("Не найдены файлы:")
    for f in missing: print(f"  {f}")
    sys.exit(1)
imgs_js = "const IMGS={" + ",".join(f'"{k}":"{v}"' for k,v in PHOTOS.items()) + "};"

html = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Assmira Collection — AS</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
:root{
  --r50:#fdf2f5;--r100:#fce4ec;--r200:#f8c8d9;--r300:#f3a8c0;
  --r400:#e8839f;--r500:#d4607e;--r600:#b84567;
  --dark:#1a0d12;--tmain:#2c1520;--tmuted:#7a5060;--tlight:#b09098;
}
body{font-family:'DM Sans',sans-serif;color:var(--tmain);overflow-x:hidden;background:#fff}

/* NAV */
.nav{position:fixed;top:0;left:0;right:0;z-index:1000;display:flex;align-items:center;justify-content:space-between;padding:1.1rem 4rem;background:rgba(255,255,255,0.95);backdrop-filter:blur(16px);border-bottom:1px solid var(--r100);transition:padding .3s}
.nav.scrolled{padding:.75rem 4rem;box-shadow:0 1px 20px rgba(212,96,126,.07)}
.logo{font-family:'Cormorant Garamond',serif;font-size:1.45rem;font-weight:500;color:var(--tmain);text-decoration:none;letter-spacing:.06em;line-height:1}
.logo-sub{font-size:.58rem;font-family:'DM Sans',sans-serif;font-weight:300;letter-spacing:.35em;color:var(--tmuted);text-transform:uppercase;display:block;margin-top:2px}
.nav-links{display:flex;gap:2.5rem;list-style:none}
.nav-links a{font-size:.75rem;font-weight:300;letter-spacing:.18em;text-transform:uppercase;color:var(--tmuted);text-decoration:none;transition:color .2s;padding-bottom:2px;border-bottom:1px solid transparent}
.nav-links a:hover,.nav-links a.active{color:var(--r500);border-bottom-color:var(--r400)}
.nav-right{display:flex;align-items:center;gap:1.5rem}
.cart-btn{background:none;border:none;cursor:pointer;display:flex;align-items:center;gap:.5rem;font-family:'DM Sans',sans-serif;font-size:.75rem;font-weight:300;letter-spacing:.18em;text-transform:uppercase;color:var(--tmuted);transition:color .2s}
.cart-btn:hover{color:var(--r500)}
.cart-count{background:var(--r400);color:#fff;border-radius:50%;width:19px;height:19px;font-size:.62rem;display:flex;align-items:center;justify-content:center}
.burger{display:none;flex-direction:column;gap:5px;background:none;border:none;cursor:pointer;padding:4px}
.burger span{display:block;width:22px;height:1.5px;background:var(--tmain);transition:all .3s;border-radius:2px}

/* HERO */
.hero{min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;overflow:hidden;background:linear-gradient(160deg,var(--r50) 0%,#fff 45%,var(--r100) 100%);padding-top:6rem}
.hero-bg-text{position:absolute;font-family:'Cormorant Garamond',serif;font-size:38vw;font-weight:300;color:var(--r100);opacity:.55;top:50%;left:50%;transform:translate(-50%,-52%);pointer-events:none;user-select:none;line-height:1;letter-spacing:-.02em}
.hero-inner{position:relative;z-index:2;text-align:center;padding:2rem 1rem}
.hero-badge{display:inline-flex;align-items:center;gap:.6rem;font-size:.68rem;letter-spacing:.35em;text-transform:uppercase;color:var(--r500);margin-bottom:1.8rem}
.hero-badge::before,.hero-badge::after{content:'';display:block;width:30px;height:1px;background:var(--r300)}
.hero-h1{font-family:'Cormorant Garamond',serif;font-size:clamp(3.2rem,9vw,7rem);font-weight:400;line-height:.92;color:var(--tmain);letter-spacing:-.01em;margin-bottom:.5rem}
.hero-h1 em{font-style:italic;color:var(--r500)}
.hero-tagline{font-family:'Cormorant Garamond',serif;font-size:clamp(1.1rem,2.5vw,1.6rem);font-weight:300;font-style:italic;color:var(--tmuted);margin-bottom:3rem;letter-spacing:.02em}
.hero-btns{display:flex;gap:1rem;justify-content:center;flex-wrap:wrap}
.btn-primary{display:inline-flex;align-items:center;gap:.7rem;background:var(--tmain);color:#fff;padding:.9rem 2.4rem;font-size:.73rem;font-weight:300;letter-spacing:.2em;text-transform:uppercase;text-decoration:none;border:1px solid var(--tmain);transition:all .3s;cursor:pointer;font-family:'DM Sans',sans-serif}
.btn-primary:hover{background:transparent;color:var(--tmain)}
.btn-outline{display:inline-flex;align-items:center;gap:.7rem;background:transparent;color:var(--tmain);padding:.9rem 2.4rem;font-size:.73rem;font-weight:300;letter-spacing:.2em;text-transform:uppercase;text-decoration:none;border:1px solid var(--r300);transition:all .3s;cursor:pointer;font-family:'DM Sans',sans-serif}
.btn-outline:hover{border-color:var(--r500);color:var(--r500)}
.hero-scroll{position:absolute;bottom:2.5rem;left:50%;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;gap:.5rem;opacity:.5;animation:pulse 2.5s infinite}
.hero-scroll span{font-size:.62rem;letter-spacing:.25em;text-transform:uppercase;color:var(--tmuted)}
.hero-scroll-line{width:1px;height:40px;background:var(--r300);animation:scrollAnim 2.5s infinite}
@keyframes scrollAnim{0%,100%{transform:scaleY(0);transform-origin:top}50%{transform:scaleY(1);transform-origin:top}51%{transform-origin:bottom}100%{transform:scaleY(0);transform-origin:bottom}}
@keyframes pulse{0%,100%{opacity:.3}50%{opacity:.7}}

/* MARQUEE */
.marquee-bar{background:var(--r100);padding:.85rem 0;overflow:hidden;white-space:nowrap}
.marquee-track{display:inline-flex;animation:marquee 28s linear infinite}
.mi{font-size:.68rem;letter-spacing:.28em;text-transform:uppercase;color:var(--tmuted);padding:0 2rem}
.mi-dot{color:var(--r400);padding:0 .8rem}
@keyframes marquee{from{transform:translateX(0)}to{transform:translateX(-50%)}}

/* SECTION */
.section{padding:7rem 4rem}
.sec-header{text-align:center;margin-bottom:5rem}
.sec-eye{font-size:.68rem;font-weight:300;letter-spacing:.4em;text-transform:uppercase;color:var(--r400);margin-bottom:1rem;display:block}
.sec-title{font-family:'Cormorant Garamond',serif;font-size:clamp(2.2rem,4vw,3.5rem);font-weight:400;color:var(--tmain)}
.sec-title em{font-style:italic;color:var(--r500)}
.sec-line{width:50px;height:1px;background:var(--r300);margin:1.5rem auto 0}

/* GRID */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:2.5rem;max-width:1500px;margin:0 auto}

/* CARD */
.card{cursor:pointer;transition:transform .35s ease}
.card:hover{transform:translateY(-5px)}
.card-gal{position:relative;overflow:hidden;aspect-ratio:3/4;background:var(--r50)}
.card-gal img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .5s ease}
.card-gal img.active{opacity:1}
.card-tag{position:absolute;top:1rem;left:1rem;z-index:3;background:var(--r400);color:#fff;font-size:.6rem;letter-spacing:.18em;text-transform:uppercase;padding:.28rem .75rem}
.gal-nav{position:absolute;top:50%;transform:translateY(-50%);z-index:3;background:rgba(255,255,255,.85);border:none;cursor:pointer;width:36px;height:36px;display:flex;align-items:center;justify-content:center;font-size:1.3rem;color:var(--tmain);opacity:0;transition:opacity .2s}
.gal-nav.pr{left:.75rem}.gal-nav.nx{right:.75rem}
.card-gal:hover .gal-nav{opacity:1}
.gal-dots{position:absolute;bottom:.85rem;left:50%;transform:translateX(-50%);display:flex;gap:5px;z-index:3}
.gal-dot{width:5px;height:5px;border-radius:50%;background:rgba(255,255,255,.45);border:none;cursor:pointer;transition:all .3s;padding:0}
.gal-dot.active{background:#fff;width:18px;border-radius:3px}
.card-info{padding:1.1rem 0 0}
.card-name{font-family:'Cormorant Garamond',serif;font-size:1.3rem;font-weight:400;color:var(--tmain);margin-bottom:.25rem}
.card-desc{font-size:.78rem;font-weight:300;color:var(--tmuted);line-height:1.65;margin-bottom:.8rem}
.sizes{display:flex;gap:.35rem;flex-wrap:wrap;margin-bottom:.65rem}
.sz{padding:.22rem .6rem;border:.5px solid var(--r200);background:none;cursor:pointer;font-size:.7rem;color:var(--tmuted);transition:all .2s;font-family:'DM Sans',sans-serif}
.sz.on,.sz:hover{background:var(--tmain);border-color:var(--tmain);color:#fff}
.card-foot{display:flex;align-items:center;justify-content:space-between;margin-top:.7rem;gap:.5rem}
.card-price{font-family:'Cormorant Garamond',serif;font-size:1.35rem;font-weight:500;color:var(--tmain)}
.add-btn{background:none;border:.5px solid var(--r300);cursor:pointer;padding:.48rem 1rem;font-size:.68rem;font-weight:300;letter-spacing:.15em;text-transform:uppercase;color:var(--tmuted);transition:all .25s;font-family:'DM Sans',sans-serif;white-space:nowrap}
.add-btn:hover{background:var(--r400);border-color:var(--r400);color:#fff}
.qty-row{display:flex;align-items:center;gap:.6rem;margin:.55rem 0}
.ql{font-size:.67rem;letter-spacing:.1em;text-transform:uppercase;color:var(--tlight)}
.qc{display:flex;align-items:center;gap:.4rem}
.qb{width:24px;height:24px;border:.5px solid var(--r200);background:none;cursor:pointer;font-size:1rem;display:flex;align-items:center;justify-content:center;color:var(--tmuted);transition:all .2s}
.qb:hover{background:var(--r100)}
.qn{font-size:.82rem;min-width:1.3rem;text-align:center}

/* FEATURES */
.features{background:var(--r50);padding:6rem 4rem}
.feat-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:2rem;max-width:1200px;margin:0 auto}
.feat{text-align:center;padding:2rem 1.5rem}
.feat-icon{font-size:2rem;margin-bottom:1rem;display:block}
.feat-title{font-family:'Cormorant Garamond',serif;font-size:1.2rem;font-weight:400;margin-bottom:.6rem}
.feat-text{font-size:.8rem;font-weight:300;color:var(--tmuted);line-height:1.7}

/* ABOUT */
.about{padding:7rem 4rem;max-width:1400px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:6rem;align-items:center}
.about-mono{aspect-ratio:1;background:var(--r100);display:flex;align-items:center;justify-content:center;font-family:'Cormorant Garamond',serif;font-size:clamp(5rem,12vw,10rem);font-weight:300;font-style:italic;color:var(--r300)}
.about-eye{font-size:.68rem;letter-spacing:.4em;text-transform:uppercase;color:var(--r400);margin-bottom:1.2rem;display:block}
.about-h{font-family:'Cormorant Garamond',serif;font-size:clamp(2rem,3.5vw,3rem);font-weight:400;line-height:1.1;margin-bottom:1.5rem}
.about-h em{font-style:italic;color:var(--r500)}
.about-p{font-size:.88rem;font-weight:300;line-height:1.9;color:var(--tmuted);margin-bottom:1rem}

/* INSTAGRAM */
.insta{padding:6rem 4rem;background:var(--r50);text-align:center}
.insta-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;max-width:900px;margin:3rem auto 2rem;overflow:hidden}
.insta-cell{aspect-ratio:1;overflow:hidden;cursor:pointer;position:relative}
.insta-cell img{width:100%;height:100%;object-fit:cover;transition:transform .4s ease}
.insta-cell:hover img{transform:scale(1.05)}
.insta-handle{font-family:'Cormorant Garamond',serif;font-size:1.1rem;font-style:italic;color:var(--tmuted)}

/* CART */
.cart-ov{position:fixed;inset:0;background:rgba(0,0,0,.4);z-index:2000;opacity:0;pointer-events:none;transition:opacity .3s}
.cart-ov.on{opacity:1;pointer-events:all}
.cart-dr{position:fixed;top:0;right:0;bottom:0;width:420px;max-width:100vw;background:#fff;z-index:2001;transform:translateX(100%);transition:transform .4s cubic-bezier(.4,0,.2,1);display:flex;flex-direction:column}
.cart-dr.on{transform:translateX(0)}
.cart-hd{padding:1.5rem;border-bottom:1px solid var(--r100);display:flex;align-items:center;justify-content:space-between}
.cart-hd h2{font-family:'Cormorant Garamond',serif;font-size:1.5rem;font-weight:400}
.cart-x{background:none;border:none;cursor:pointer;font-size:1.6rem;color:var(--tmuted);line-height:1}
.cart-body{flex:1;overflow-y:auto;padding:1rem 1.5rem}
.ci{display:flex;gap:1rem;padding:1rem 0;border-bottom:1px solid var(--r50)}
.ci-img{width:80px;height:100px;object-fit:cover;flex-shrink:0;background:var(--r50)}
.ci-info{flex:1}
.ci-name{font-family:'Cormorant Garamond',serif;font-size:1rem;margin-bottom:.25rem}
.ci-meta{font-size:.73rem;color:var(--tlight);margin-bottom:.25rem}
.ci-price{font-size:.85rem;color:var(--r500)}
.ci-rm{background:none;border:none;cursor:pointer;font-size:1.1rem;color:var(--tlight);align-self:flex-start;transition:color .2s}
.ci-rm:hover{color:var(--r500)}
.cart-empty-msg{text-align:center;padding:3rem 1rem;font-family:'Cormorant Garamond',serif;font-size:1.1rem;color:var(--tlight);font-style:italic}
.cart-ft{padding:1.2rem 1.5rem;border-top:1px solid var(--r100)}
.cart-tot{display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem}
.cart-tot-lbl{font-size:.73rem;letter-spacing:.18em;text-transform:uppercase;color:var(--tmuted)}
.cart-tot-val{font-family:'Cormorant Garamond',serif;font-size:1.5rem;font-weight:500}

/* MODAL */
.modal-ov{position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:3000;display:flex;align-items:center;justify-content:center;padding:1rem;opacity:0;pointer-events:none;transition:opacity .3s}
.modal-ov.on{opacity:1;pointer-events:all}
.modal{background:#fff;padding:2.5rem;max-width:540px;width:100%;max-height:90vh;overflow-y:auto;position:relative;transform:scale(.96);transition:transform .3s}
.modal-ov.on .modal{transform:scale(1)}
.modal-x{position:absolute;top:1rem;right:1rem;background:none;border:none;cursor:pointer;font-size:1.6rem;color:var(--tmuted)}
.modal-title{font-family:'Cormorant Garamond',serif;font-size:1.9rem;font-weight:400;margin-bottom:.3rem}
.modal-sub{font-size:.8rem;color:var(--tmuted);margin-bottom:2rem}
.fg{margin-bottom:1.1rem}
.fl{display:block;font-size:.67rem;letter-spacing:.15em;text-transform:uppercase;color:var(--tmuted);margin-bottom:.4rem}
.fi{width:100%;padding:.72rem .9rem;border:1px solid var(--r200);background:var(--r50);font-family:'DM Sans',sans-serif;font-size:.88rem;color:var(--tmain);outline:none;transition:border-color .2s}
.fi:focus{border-color:var(--r400);background:#fff}
.fr{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
.success-wrap{text-align:center;padding:2.5rem 1rem}
.success-ico{font-size:2.8rem;margin-bottom:1rem}
.success-title{font-family:'Cormorant Garamond',serif;font-size:2rem;margin-bottom:.5rem}
.success-txt{font-size:.88rem;color:var(--tmuted);line-height:1.7}

/* TOAST */
.toast{position:fixed;bottom:2rem;left:50%;transform:translateX(-50%) translateY(90px);background:var(--tmain);color:#fff;padding:.8rem 2rem;font-size:.8rem;letter-spacing:.05em;z-index:5000;transition:transform .4s cubic-bezier(.4,0,.2,1);white-space:nowrap;border-radius:2px}
.toast.on{transform:translateX(-50%) translateY(0)}

/* MOBILE */
.mob-menu{position:fixed;inset:0;background:#fff;z-index:1500;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2rem;transform:translateX(-100%);transition:transform .4s cubic-bezier(.4,0,.2,1)}
.mob-menu.on{transform:translateX(0)}
.mob-menu a{font-family:'Cormorant Garamond',serif;font-size:2.2rem;font-weight:400;color:var(--tmain);text-decoration:none;transition:color .2s}
.mob-menu a:hover{color:var(--r500)}
.mob-x{position:absolute;top:1.5rem;right:1.5rem;background:none;border:none;font-size:2rem;cursor:pointer;color:var(--tmain)}

/* FOOTER */
footer{background:var(--tmain);color:var(--r200);padding:5rem 4rem 2.5rem}
.ft-grid{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:3rem;margin-bottom:3.5rem;padding-bottom:3.5rem;border-bottom:1px solid rgba(255,255,255,.07)}
.ft-logo{font-family:'Cormorant Garamond',serif;font-size:1.8rem;font-weight:400;font-style:italic;margin-bottom:.8rem}
.ft-about{font-size:.8rem;font-weight:300;color:var(--tlight);line-height:1.8;margin-bottom:1.2rem}
.ft-socials{display:flex;gap:.7rem}
.ft-soc{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);color:var(--r300);padding:.4rem .8rem;font-size:.7rem;letter-spacing:.1em;text-decoration:none;transition:all .2s}
.ft-soc:hover{background:var(--r600);border-color:var(--r600);color:#fff}
.ft-h{font-size:.65rem;letter-spacing:.28em;text-transform:uppercase;color:var(--r400);margin-bottom:1.2rem}
.ft-ul{list-style:none}
.ft-ul li{margin-bottom:.55rem}
.ft-ul a{font-size:.82rem;font-weight:300;color:var(--tlight);text-decoration:none;transition:color .2s}
.ft-ul a:hover{color:var(--r300)}
.ft-bottom{display:flex;justify-content:space-between;align-items:center;font-size:.7rem;font-weight:300;color:var(--tlight);flex-wrap:wrap;gap:.5rem}

/* RESPONSIVE */
@media(max-width:1100px){
  .nav{padding:1rem 2rem}
  .nav.scrolled{padding:.7rem 2rem}
  .section{padding:5rem 2rem}
  .features{padding:5rem 2rem}
  .about{padding:5rem 2rem;gap:3rem}
  .insta{padding:5rem 2rem}
  footer{padding:4rem 2rem 2rem}
  .ft-grid{grid-template-columns:1fr 1fr}
  .ft-brand{grid-column:1/-1}
}
@media(max-width:768px){
  .nav{padding:1rem 1.2rem}
  .nav.scrolled{padding:.7rem 1.2rem}
  .nav-links{display:none}
  .burger{display:flex}
  .section{padding:4rem 1.2rem}
  .features{padding:4rem 1.2rem}
  .about{padding:4rem 1.2rem;grid-template-columns:1fr;gap:2.5rem}
  .insta{padding:4rem 1.2rem}
  .insta-grid{grid-template-columns:repeat(2,1fr)}
  footer{padding:3.5rem 1.2rem 2rem}
  .ft-grid{grid-template-columns:1fr 1fr}
  .cart-dr{width:100vw}
  .fr{grid-template-columns:1fr}
}
@media(max-width:600px){
  .hero-bg-text{font-size:52vw}
  .grid{grid-template-columns:repeat(2,1fr);gap:1rem}
  .hero-btns{flex-direction:column;align-items:center}
  .ft-grid{grid-template-columns:1fr}
}
@media(max-width:380px){
  .grid{grid-template-columns:1fr}
}
</style>
</head>
<body>

<nav class="nav" id="nav">
  <a href="#" class="logo">Assmira Collection<span class="logo-sub">AS &middot; Авторская Мода</span></a>
  <ul class="nav-links">
    <li><a href="#collection" class="active">Коллекция</a></li>
    <li><a href="#about">О бренде</a></li>
    <li><a href="#contact">Контакты</a></li>
  </ul>
  <div class="nav-right">
    <button class="cart-btn" onclick="toggleCart()" aria-label="Корзина">
      Корзина&nbsp;<span class="cart-count" id="cartCount">0</span>
    </button>
    <button class="burger" id="burger" onclick="toggleMob()" aria-label="Меню">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>

<div class="mob-menu" id="mobMenu">
  <button class="mob-x" onclick="toggleMob()">&#10005;</button>
  <a href="#collection" onclick="toggleMob()">Коллекция</a>
  <a href="#about" onclick="toggleMob()">О бренде</a>
  <a href="#contact" onclick="toggleMob()">Контакты</a>
</div>

<!-- HERO -->
<section class="hero" id="home">
  <div class="hero-bg-text">AS</div>
  <div class="hero-inner">
    <div class="hero-badge">Новая коллекция&nbsp;2025</div>
    <h1 class="hero-h1">Assmira<br><em>Collection</em></h1>
    <p class="hero-tagline">Одежда, созданная быть замеченной</p>
    <div class="hero-btns">
      <a href="#collection" class="btn-primary">Смотреть коллекцию&nbsp;→</a>
      <a href="#about" class="btn-outline">О бренде</a>
    </div>
  </div>
  <div class="hero-scroll">
    <span>Scroll</span>
    <div class="hero-scroll-line"></div>
  </div>
</section>

<!-- MARQUEE -->
<div class="marquee-bar"><div class="marquee-track" id="mTrack"></div></div>

<!-- COLLECTION -->
<section class="section" id="collection">
  <div class="sec-header">
    <span class="sec-eye">Авторская Коллекция</span>
    <h2 class="sec-title">Платья &amp; <em>Ансамбли</em></h2>
    <div class="sec-line"></div>
  </div>

  <!-- FILTER -->
  <div style="display:flex;justify-content:center;gap:.5rem;flex-wrap:wrap;margin-bottom:3rem" id="filters">
    <button onclick="filter('all',this)" class="sz on" style="padding:.4rem 1.2rem">Все</button>
    <button onclick="filter('Вечернее',this)" class="sz" style="padding:.4rem 1.2rem">Вечерние</button>
    <button onclick="filter('Праздничное',this)" class="sz" style="padding:.4rem 1.2rem">Праздничные</button>
    <button onclick="filter('Casual Luxe',this)" class="sz" style="padding:.4rem 1.2rem">Casual Luxe</button>
    <button onclick="filter('Ансамбль',this)" class="sz" style="padding:.4rem 1.2rem">Ансамбли</button>
    <button onclick="filter('Resort Wear',this)" class="sz" style="padding:.4rem 1.2rem">Resort</button>
  </div>

  <div class="grid" id="grid"></div>
</section>

<!-- FEATURES -->
<div class="features">
  <div class="feat-grid">
    <div class="feat"><span class="feat-icon">✦</span><h3 class="feat-title">Авторский дизайн</h3><p class="feat-text">Каждое изделие разработано и создано вручную с вниманием к каждой детали</p></div>
    <div class="feat"><span class="feat-icon">◇</span><h3 class="feat-title">Премиум ткани</h3><p class="feat-text">Только тщательно отобранные материалы высочайшего качества</p></div>
    <div class="feat"><span class="feat-icon">♡</span><h3 class="feat-title">Индивидуальный пошив</h3><p class="feat-text">Подгонка по фигуре и индивидуальные заказы по запросу</p></div>
    <div class="feat"><span class="feat-icon">◈</span><h3 class="feat-title">Быстрая доставка</h3><p class="feat-text">Доставляем по всей России и странам СНГ в кратчайшие сроки</p></div>
  </div>
</div>

<!-- ABOUT -->
<div id="about">
  <div class="about">
    <div class="about-mono">AS</div>
    <div>
      <span class="about-eye">О Бренде</span>
      <h2 class="about-h">Мода как <em>искусство</em></h2>
      <p class="about-p">Assmira Collection — это авторская марка, где каждое изделие создаётся с заботой о деталях и страстью к форме. Мы верим, что одежда должна не просто одевать — она должна рассказывать историю.</p>
      <p class="about-p">Каждый силуэт продуман, каждая ткань выбрана вручную, каждый образ — произведение искусства, которое живёт вместе с вами и отражает вашу индивидуальность.</p>
      <a href="#collection" class="btn-primary" style="margin-top:1.5rem;display:inline-flex">Смотреть коллекцию&nbsp;→</a>
    </div>
  </div>
</div>

<!-- INSTAGRAM -->
<div class="insta" id="contact">
  <span class="sec-eye">Следите за нами</span>
  <h2 class="sec-title" style="margin-top:.5rem">Instagram <em>Gallery</em></h2>
  <div class="sec-line"></div>
  <div class="insta-grid" id="instaGrid"></div>
  <p class="insta-handle">@assmira.collection</p>
</div>

<!-- FOOTER -->
<footer>
  <div class="ft-grid">
    <div class="ft-brand">
      <div class="ft-logo">Assmira Collection</div>
      <p class="ft-about">Авторская одежда для тех, кто хочет быть собой — с шиком. Каждое изделие создаётся с любовью и вниманием к деталям.</p>
      <div class="ft-socials">
        <a href="#" class="ft-soc">Instagram</a>
        <a href="#" class="ft-soc">WhatsApp</a>
        <a href="#" class="ft-soc">Telegram</a>
      </div>
    </div>
    <div>
      <p class="ft-h">Навигация</p>
      <ul class="ft-ul">
        <li><a href="#collection">Коллекция</a></li>
        <li><a href="#about">О бренде</a></li>
        <li><a href="#contact">Контакты</a></li>
      </ul>
    </div>
    <div>
      <p class="ft-h">Покупателям</p>
      <ul class="ft-ul">
        <li><a href="#">Доставка</a></li>
        <li><a href="#">Возврат</a></li>
        <li><a href="#">Размерная сетка</a></li>
        <li><a href="#">Уход за изделием</a></li>
      </ul>
    </div>
    <div>
      <p class="ft-h">Контакты</p>
      <ul class="ft-ul">
        <li><a href="#">+7 (___) ___-__-__</a></li>
        <li><a href="#">info@assmira.ru</a></li>
        <li><a href="#">WhatsApp</a></li>
        <li><a href="#">Telegram</a></li>
      </ul>
    </div>
  </div>
  <div class="ft-bottom">
    <span>© 2025 Assmira Collection · AS · Все права защищены</span>
    <span>Сделано с ♡</span>
  </div>
</footer>

<!-- CART -->
<div class="cart-ov" id="cartOv" onclick="toggleCart()"></div>
<div class="cart-dr" id="cartDr">
  <div class="cart-hd">
    <h2>Корзина</h2>
    <button class="cart-x" onclick="toggleCart()">&#10005;</button>
  </div>
  <div class="cart-body" id="cartBody"></div>
  <div id="cartFt" style="display:none">
    <div class="cart-ft">
      <div class="cart-tot">
        <span class="cart-tot-lbl">Итого</span>
        <span class="cart-tot-val" id="cartTot">0 ₽</span>
      </div>
      <button class="btn-primary" style="width:100%;justify-content:center" onclick="openOrder()">Оформить заказ</button>
    </div>
  </div>
</div>

<!-- ORDER MODAL -->
<div class="modal-ov" id="orderOv">
  <div class="modal">
    <button class="modal-x" onclick="closeOrder()">&#10005;</button>
    <div id="orderForm">
      <h2 class="modal-title">Оформление заказа</h2>
      <p class="modal-sub">Заполните данные — мы свяжемся с вами для подтверждения</p>
      <div class="fg"><label class="fl">Имя *</label><input class="fi" id="fn" type="text" placeholder="Ваше имя"></div>
      <div class="fg"><label class="fl">Телефон *</label><input class="fi" id="fp" type="tel" placeholder="+7 (___) ___-__-__"></div>
      <div class="fg"><label class="fl">Email</label><input class="fi" id="fe" type="email" placeholder="example@mail.ru"></div>
      <div class="fg"><label class="fl">Адрес доставки *</label><input class="fi" id="fa" type="text" placeholder="Город, улица, дом, квартира"></div>
      <div class="fg"><label class="fl">Комментарий</label><textarea class="fi" id="fc" rows="3" style="resize:none" placeholder="Пожелания к заказу..."></textarea></div>
      <div style="background:var(--r50);padding:1rem;margin-bottom:1rem;font-size:.8rem;color:var(--tmuted);line-height:1.6" id="orderSummary"></div>
      <button class="btn-primary" style="width:100%;justify-content:center" onclick="submitOrder()">Подтвердить заказ</button>
    </div>
    <div id="orderOk" class="success-wrap" style="display:none">
      <div class="success-ico">🌸</div>
      <h2 class="success-title">Заказ принят!</h2>
      <p class="success-txt">Спасибо за ваш заказ.<br>Мы свяжемся с вами в ближайшее время для подтверждения.</p>
    </div>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
""" + imgs_js + """

const PRODUCTS=[
  {id:1,name:'Emerald Dream',desc:'Изысканное вечернее платье-русалка с открытыми плечами. Атласная ткань изумрудного цвета подчёркивает каждую линию силуэта — для тех, кто хочет быть замеченной.',price:32000,tag:'Вечернее',imgs:['green1','green2','green3']},
  {id:2,name:'Blossom Garden',desc:'Романтичный ансамбль с цветочным принтом на нежно-голубом фоне. Баска и воланы создают образ, достойный особого дня.',price:27500,tag:'Праздничное',imgs:['blue1','blue2','blue3']},
  {id:3,name:'Midnight Tulip',desc:'Миди-платье на тонких бретелях с акварельным принтом тюльпанов. Идеально для вечерних прогулок и элегантных ужинов.',price:21000,tag:'Casual Luxe',imgs:['tulip1','tulip2','tulip3']},
  {id:4,name:'Parisian Dot',desc:'Лаконичное платье с запахом в горошек — классика, переосмысленная через призму современного шика. Незаменимо для любого выхода.',price:18500,tag:'Классика',imgs:['dot1']},
  {id:5,name:'Flamingo Sunset',desc:'Огненный ансамбль из рубашки и широких брюк в оранжево-розовом принте. Дерзко, ярко, незабываемо.',price:29000,tag:'Ансамбль',imgs:['pink1','pink2','pink3']},
  {id:6,name:'Palm Royale',desc:'Кафтан-накидка с монументальным принтом пальмовых листьев. Свобода, роскошь и лёгкость в каждом движении.',price:24000,tag:'Resort Wear',imgs:['palm1','palm2','palm3']},
  {id:7,name:'Azzurro Tile',desc:'Облегающее платье с орнаментом в стиле итальянской майолики. Синий и белый — вечный дуэт средиземноморского шика.',price:26000,tag:'Вечернее',imgs:['tile1','tile2','tile3']}
];

let cart=JSON.parse(localStorage.getItem('as_cart')||'[]');
const sizes={},qtys={},slides={};
PRODUCTS.forEach(p=>{sizes[p.id]='S';qtys[p.id]=1;slides[p.id]=0});

function saveCart(){localStorage.setItem('as_cart',JSON.stringify(cart))}
function updCount(){document.getElementById('cartCount').textContent=cart.reduce((s,i)=>s+i.qty,0)}

// MARQUEE
const mt=document.getElementById('mTrack');
const mw=['Assmira Collection','Авторская Мода','AS 2025','Элегантность','Женственность','Ручная работа','Exclusive Design','Новая Коллекция'];
let mh='';for(let i=0;i<5;i++)mw.forEach(t=>{mh+=`<span class="mi">${t}</span><span class="mi-dot">✦</span>`});
mt.innerHTML=mh;

// INSTA GRID — показываем все 19 фото
const instaKeys=['green1','green2','green3','blue1','blue2','blue3','tulip1','tulip2','tulip3','dot1','pink1','pink2','pink3','palm1','palm2','palm3','tile1','tile2','tile3'];
const ig=document.getElementById('instaGrid');
ig.style.gridTemplateColumns='repeat(auto-fill,minmax(160px,1fr))';
instaKeys.slice(0,8).forEach(k=>{
  const d=document.createElement('div');d.className='insta-cell';
  d.innerHTML=`<img src="${IMGS[k]}" alt="Assmira Collection" loading="lazy">`;
  ig.appendChild(d);
});

function renderGrid(tag='all'){
  const g=document.getElementById('grid');
  const list=tag==='all'?PRODUCTS:PRODUCTS.filter(p=>p.tag===tag);
  g.innerHTML=list.map(p=>{
    const dots=p.imgs.length>1?p.imgs.map((_,i)=>`<button class="gal-dot${i===0?' active':''}" onclick="goSlide(${p.id},${i})"></button>`).join(''):'';
    const imgs=p.imgs.map((k,i)=>`<img src="${IMGS[k]}" class="${i===0?'active':''}" alt="${p.name}" loading="lazy">`).join('');
    const nav=p.imgs.length>1?`<button class="gal-nav pr" onclick="mv(${p.id},-1)">&#8249;</button><button class="gal-nav nx" onclick="mv(${p.id},1)">&#8250;</button>`:'';
    const szBtns=['XS','S','M','L','XL'].map(s=>`<button class="sz${s==='S'?' on':''}" onclick="selSz(${p.id},'${s}',this)">${s}</button>`).join('');
    return `<div class="card" id="c${p.id}">
      <div class="card-gal">
        <span class="card-tag">${p.tag}</span>
        ${imgs}${nav}
        ${p.imgs.length>1?`<div class="gal-dots">${dots}</div>`:''}
      </div>
      <div class="card-info">
        <h3 class="card-name">${p.name}</h3>
        <p class="card-desc">${p.desc}</p>
        <div class="sizes">${szBtns}</div>
        <div class="qty-row">
          <span class="ql">Кол-во:</span>
          <div class="qc">
            <button class="qb" onclick="chQ(${p.id},-1)">&#8722;</button>
            <span class="qn" id="q${p.id}">1</span>
            <button class="qb" onclick="chQ(${p.id},1)">&#43;</button>
          </div>
        </div>
        <div class="card-foot">
          <span class="card-price">${p.price.toLocaleString('ru-RU')} &#8381;</span>
          <button class="add-btn" onclick="addCart(${p.id})">В корзину</button>
        </div>
      </div>
    </div>`;
  }).join('');
}

function filter(tag,btn){
  document.querySelectorAll('#filters .sz').forEach(b=>b.classList.remove('on'));
  btn.classList.add('on');
  renderGrid(tag);
}
function goSlide(id,idx){
  const c=document.getElementById('c'+id);
  c.querySelectorAll('.card-gal img').forEach(i=>i.classList.remove('active'));
  c.querySelectorAll('.gal-dot').forEach(d=>d.classList.remove('active'));
  const imgs=c.querySelectorAll('.card-gal img'),dots=c.querySelectorAll('.gal-dot');
  if(imgs[idx])imgs[idx].classList.add('active');
  if(dots[idx])dots[idx].classList.add('active');
  slides[id]=idx;
}
function mv(id,d){const p=PRODUCTS.find(x=>x.id===id);goSlide(id,(slides[id]+d+p.imgs.length)%p.imgs.length)}
function selSz(id,s,btn){document.getElementById('c'+id).querySelectorAll('.sz').forEach(b=>b.classList.remove('on'));btn.classList.add('on');sizes[id]=s}
function chQ(id,d){qtys[id]=Math.max(1,(qtys[id]||1)+d);const el=document.getElementById('q'+id);if(el)el.textContent=qtys[id]}

function addCart(id){
  const p=PRODUCTS.find(x=>x.id===id),s=sizes[id],q=qtys[id];
  const ex=cart.find(i=>i.id===id&&i.size===s);
  if(ex)ex.qty+=q;else cart.push({...p,size:s,qty:q,thumb:p.imgs[0]});
  saveCart();updCount();toast(`«${p.name}» добавлен в корзину 🌸`);
}

function renderCart(){
  const b=document.getElementById('cartBody'),ft=document.getElementById('cartFt');
  if(!cart.length){b.innerHTML='<p class="cart-empty-msg">Ваша корзина пуста</p>';ft.style.display='none';return}
  ft.style.display='block';
  b.innerHTML=cart.map((it,i)=>`<div class="ci">
    <img class="ci-img" src="${IMGS[it.thumb]||''}" alt="${it.name}">
    <div class="ci-info">
      <p class="ci-name">${it.name}</p>
      <p class="ci-meta">Размер: ${it.size} · ${it.qty} шт.</p>
      <p class="ci-price">${(it.price*it.qty).toLocaleString('ru-RU')} ₽</p>
    </div>
    <button class="ci-rm" onclick="rmCart(${i})">&#10005;</button>
  </div>`).join('');
  document.getElementById('cartTot').textContent=cart.reduce((s,i)=>s+i.price*i.qty,0).toLocaleString('ru-RU')+' ₽';
}
function rmCart(i){cart.splice(i,1);saveCart();updCount();renderCart()}
function toggleCart(){
  const d=document.getElementById('cartDr'),o=document.getElementById('cartOv');
  const op=d.classList.toggle('on');o.classList.toggle('on',op);
  if(op)renderCart();document.body.style.overflow=op?'hidden':'';
}
function openOrder(){
  toggleCart();
  const sum=cart.map(i=>`${i.name} (${i.size}) × ${i.qty} = ${(i.price*i.qty).toLocaleString('ru-RU')} ₽`).join('<br>');
  const total=cart.reduce((s,i)=>s+i.price*i.qty,0);
  document.getElementById('orderSummary').innerHTML=`${sum}<br><strong>Итого: ${total.toLocaleString('ru-RU')} ₽</strong>`;
  document.getElementById('orderOv').classList.add('on');
  document.getElementById('orderForm').style.display='block';
  document.getElementById('orderOk').style.display='none';
}
function closeOrder(){document.getElementById('orderOv').classList.remove('on');document.body.style.overflow=''}
function submitOrder(){
  const n=document.getElementById('fn').value.trim(),ph=document.getElementById('fp').value.trim(),addr=document.getElementById('fa').value.trim();
  if(!n||!ph||!addr){toast('Заполните обязательные поля (*)');return}
  const orders=JSON.parse(localStorage.getItem('as_orders')||'[]');
  orders.push({id:Date.now(),date:new Date().toLocaleString('ru-RU'),customer:{name:n,phone:ph,email:document.getElementById('fe').value,address:addr,comment:document.getElementById('fc').value},items:cart.map(i=>({name:i.name,size:i.size,qty:i.qty,price:i.price})),total:cart.reduce((s,i)=>s+i.price*i.qty,0)});
  localStorage.setItem('as_orders',JSON.stringify(orders));
  cart=[];saveCart();updCount();
  document.getElementById('orderForm').style.display='none';
  document.getElementById('orderOk').style.display='block';
  setTimeout(closeOrder,3500);
}
function toast(msg){const t=document.getElementById('toast');t.textContent=msg;t.classList.add('on');setTimeout(()=>t.classList.remove('on'),2800)}
function toggleMob(){document.getElementById('mobMenu').classList.toggle('on')}

// NAV scroll
window.addEventListener('scroll',()=>{document.getElementById('nav').classList.toggle('scrolled',scrollY>60)});
// Nav active
document.querySelectorAll('.nav-links a').forEach(a=>{
  a.addEventListener('click',()=>{document.querySelectorAll('.nav-links a').forEach(x=>x.classList.remove('active'));a.classList.add('active')});
});

renderGrid();updCount();
</script>
</body>
</html>"""

with open('index.html','w',encoding='utf-8') as f:
    f.write(html)
size=os.path.getsize('index.html')/1024/1024
print(f"\\n✅ index.html готов! ({size:.1f} MB)")
print("   Откройте index.html в браузере — всё встроено внутри.")
