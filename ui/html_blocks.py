"""Pure-HTML pieces (no Streamlit import) rendered inside isolated iframes, so animation/JS always works."""
BASE = """<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=IBM+Plex+Sans:wght@400;500&display=swap');
*{box-sizing:border-box} body{margin:0;font-family:'IBM Plex Sans',sans-serif;color:#E8EFFA;background:transparent}
h3{font-family:'Space Grotesk',sans-serif;font-size:1.5rem;margin:.2rem 0 .5rem;letter-spacing:-.02em}
</style>"""

def hero_diagram():
    banks = [(60, "Bank A", "account takeover"), (150, "Bank B", "cross-border"), (240, "Bank C", "card testing")]
    out = ""
    for i, (y, n, t) in enumerate(banks):
        cy = y + 28
        path = f"M232,{cy} C350,{cy} 390,170 470,170"
        out += f'<rect x="30" y="{y}" width="202" height="56" rx="12" fill="#12264A" stroke="#2A4170"/>'
        out += f'<text x="48" y="{y+24}" fill="#E8EFFA" font-size="15" font-weight="700">{n}</text><text x="48" y="{y+43}" fill="#8FA3C4" font-size="12">sees mostly {t}</text>'
        out += f'<path d="{path}" fill="none" stroke="#2A4170" stroke-width="2" stroke-dasharray="6 6"><animate attributeName="stroke-dashoffset" from="24" to="0" dur="1.6s" repeatCount="indefinite"/></path>'
        for k in range(2):
            out += f'<circle r="6" fill="#FFB547" opacity="0"><set attributeName="opacity" to="1" begin="{i*.5+k*1.6}s"/><animateMotion dur="3.2s" begin="{i*.5+k*1.6}s" repeatCount="indefinite" path="{path}"/><animate attributeName="fill" values="#FFB547;#FFB547;#34D3C0" dur="3.2s" begin="{i*.5+k*1.6}s" repeatCount="indefinite"/></circle>'
    out += '''<polygon points="520,105 585,135 585,205 520,235 455,205 455,135" fill="#12264A" stroke="#34D3C0" stroke-width="2.5"><animate attributeName="stroke-opacity" values="1;.35;1" dur="2.4s" repeatCount="indefinite"/></polygon>
<text x="520" y="165" fill="#34D3C0" font-size="14" font-weight="700" text-anchor="middle">LinuxONE</text><text x="520" y="185" fill="#8FA3C4" font-size="11" text-anchor="middle">s390x merge</text>
<path d="M585,170 L690,170" stroke="#34D3C0" stroke-width="2.5"/><rect x="690" y="125" width="180" height="90" rx="12" fill="#12264A" stroke="#34D3C0"/>
<text x="780" y="165" fill="#E8EFFA" font-size="15" font-weight="700" text-anchor="middle">Shared fraud model</text><text x="780" y="187" fill="#8FA3C4" font-size="12" text-anchor="middle">no raw data inside</text>
<text x="215" y="326" fill="#FFB547" font-size="12">masked updates travel</text>'''
    return BASE + f'<svg viewBox="0 0 900 340" width="100%" height="330" font-family="IBM Plex Sans">{out}</svg>'

SLIDES = [
 ("1  The problem", "Banks each see only a slice of fraud, and the law stops them pooling customer data. Criminals hit several banks at once.", '<circle cx="50" cy="50" r="30" fill="none" stroke="#FF6B6B" stroke-width="4"/><path d="M28 72 L72 28" stroke="#FF6B6B" stroke-width="4"/>'),
 ("2  Add noise on-site", "Each bank blurs its own data a little before using it. The ε slider sets how much. Nobody can rebuild a single customer from it.", '<path d="M10 55 Q25 20 40 55 T70 55 T100 55" fill="none" stroke="#FFB547" stroke-width="4"/><path d="M10 70 Q25 30 40 70 T70 70 T100 70" fill="none" stroke="#8FA3C4" stroke-width="2"/>'),
 ("3  Train locally", "Every bank trains a model on its own data inside its own walls. Only the model's numbers are kept, never the transactions.", '<rect x="20" y="30" width="60" height="45" rx="6" fill="none" stroke="#34D3C0" stroke-width="4"/><path d="M30 60 L45 48 L58 55 L72 38" fill="none" stroke="#34D3C0" stroke-width="3"/>'),
 ("4  Mask the numbers", "Before sending, each bank hides its numbers behind random masks. The masks cancel when added, so the server sees only noise-like values.", '<rect x="25" y="45" width="50" height="35" rx="6" fill="none" stroke="#B58CFF" stroke-width="4"/><path d="M35 45 V32 a15 15 0 0 1 30 0 V45" fill="none" stroke="#B58CFF" stroke-width="4"/>'),
 ("5  Merge on LinuxONE", "The merge runs on the IBM LinuxONE server. Out comes one shared model that catches all three fraud patterns.", '<polygon points="50,15 82,32 82,68 50,85 18,68 18,32" fill="none" stroke="#34D3C0" stroke-width="4"/><path d="M36 50 L47 61 L66 40" fill="none" stroke="#34D3C0" stroke-width="4"/>'),
]

def slider():
    cards = "".join(f'<section class="s"><svg viewBox="0 0 100 100" width="90" height="90">{ic}</svg><h3>{t}</h3><p>{d}</p></section>' for t, d, ic in SLIDES)
    dots = "".join(f'<i data-i="{i}"></i>' for i in range(len(SLIDES)))
    return BASE + f"""<style>
.wrap{{position:relative}} .track{{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;scroll-behavior:smooth;gap:16px;scrollbar-width:none}}
.track::-webkit-scrollbar{{display:none}}
.s{{flex:0 0 min(520px,86%);scroll-snap-align:center;background:#12264A;border:1px solid #2A4170;border-radius:16px;padding:1.4rem 1.6rem;min-height:250px}}
.s p{{color:#8FA3C4;line-height:1.55;margin:0}}
.nav{{display:flex;align-items:center;gap:12px;margin-top:12px}} button{{background:#12264A;color:#E8EFFA;border:1px solid #2A4170;border-radius:999px;width:40px;height:40px;font-size:18px;cursor:pointer}}
button{{transition:transform .2s cubic-bezier(.2,.9,.3,1.35),box-shadow .2s,border-color .2s}} button:hover,button:focus-visible{{border-color:#34D3C0;outline:none;transform:translateY(-3px) scale(1.12);box-shadow:0 0 16px rgba(52,211,192,.55)}}
.dots i{{transition:transform .2s}} .dots i:hover{{transform:scale(1.5)}} .dots{{display:flex;gap:8px}}
.dots i{{width:9px;height:9px;border-radius:50%;background:#2A4170;display:block;cursor:pointer}} .dots i.on{{background:#34D3C0}}
</style><div class="wrap"><div class="track" id="t">{cards}</div>
<div class="nav"><button id="p" aria-label="Previous">&#8592;</button><button id="n" aria-label="Next">&#8594;</button><div class="dots" id="d">{dots}</div></div></div>
<script>
const t=document.getElementById('t'),s=[...t.children],d=[...document.querySelectorAll('#d i')];let c=0;
const go=i=>{{c=Math.max(0,Math.min(s.length-1,i));t.scrollTo({{left:s[c].offsetLeft-t.offsetLeft-(t.clientWidth-s[c].clientWidth)/2}});}};
document.getElementById('p').onclick=()=>go(c-1);document.getElementById('n').onclick=()=>go(c+1);d.forEach((e,i)=>e.onclick=()=>go(i));
t.addEventListener('scroll',()=>{{const m=t.scrollLeft+t.clientWidth/2;let b=0,bd=1e9;s.forEach((e,i)=>{{const x=Math.abs(e.offsetLeft-t.offsetLeft+e.clientWidth/2-m);if(x<bd){{bd=x;b=i}}}});c=b;d.forEach((e,i)=>e.classList.toggle('on',i==b));}});
d[0].classList.add('on');
</script>"""
