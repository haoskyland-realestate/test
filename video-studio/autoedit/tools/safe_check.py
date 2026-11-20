#!/usr/bin/env python3
"""Kiểm tra vùng an toàn của lớp đồ họa/chữ (TikTok, Reels, Shorts).
Chạy: python tools/safe_check.py --html work/ten/index.html --times 2,5.5,9 [--root "#stage"] [--seek "window.seekTo({t})"]
- Vùng an toàn (tỉ lệ khung): trên 15%, dưới 25%, trái/phải 10%.
- Phần tử bỏ qua: nằm trong [data-safe="ignore"] (video người nói, nền); riêng phần tử có thuộc tính data-bg (thẻ nền rộng hơn vùng an toàn) chỉ bỏ qua chính nó, chữ bên trong vẫn được kiểm.
- Mọi chữ, svg, img, và phần tử có data-safe nằm ngoài vùng an toàn bị báo. Thoát mã 1 nếu có vi phạm.
- --seek: lệnh JS đưa composition tới giây {t}. Xem tài liệu HyperFrames để biết lệnh seek đúng. Bỏ trống thì chỉ chờ theo thời gian thật.
Cần: pip install playwright && playwright install chromium
"""
import argparse,asyncio,sys,os
from playwright.async_api import async_playwright
JS='''([rootSel,lim])=>{const root=document.querySelector(rootSel)||document.body,S=root.getBoundingClientRect(),out=[],tol=.004;
root.querySelectorAll('*').forEach(el=>{
 if(el.closest('[data-safe="ignore"]')||el.hasAttribute('data-bg'))return;
 const cs=getComputedStyle(el);if(cs.display==='none'||cs.visibility==='hidden'||parseFloat(cs.opacity)<.05)return;
 const tag=el.tagName.toLowerCase();if(el.closest('svg')&&tag!=='svg')return;
 const own=[...el.childNodes].some(n=>n.nodeType===3&&n.textContent.trim());
 if(!(own||tag==='svg'||tag==='img'||el.hasAttribute('data-safe')))return;
 let r=el.getBoundingClientRect();
 if(own&&tag!=='svg'){const g=document.createRange();g.selectNodeContents(el);const q=g.getBoundingClientRect();if(q.width>1)r=q}
 if(r.width<2||r.height<2)return;
 if(r.width>S.width*.97&&r.height>S.height*.5)return;
 const L=(r.left-S.left)/S.width,R=(r.right-S.left)/S.width,T=(r.top-S.top)/S.height,B=(r.bottom-S.top)/S.height,bad=[];
 if(T<lim.t-tol)bad.push('trên '+((lim.t-T)*S.height).toFixed(0)+'px');
 if(B>lim.b+tol)bad.push('dưới '+((B-lim.b)*S.height).toFixed(0)+'px');
 if(L<lim.l-tol)bad.push('trái '+((lim.l-L)*S.width).toFixed(0)+'px');
 if(R>lim.r+tol)bad.push('phải '+((R-lim.r)*S.width).toFixed(0)+'px');
 if(bad.length)out.push((tag+(el.id?'#'+el.id:'')+' "'+(el.textContent||'').trim().slice(0,24)+'" tràn '+bad.join(', ')));
});return out}'''
async def main():
    ap=argparse.ArgumentParser();ap.add_argument('--html',required=True);ap.add_argument('--times',default='0')
    ap.add_argument('--root',default='body');ap.add_argument('--seek',default='');ap.add_argument('--size',default='1080x1920')
    a=ap.parse_args();w,h=map(int,a.size.split('x'));lim={'t':.15,'b':.75,'l':.10,'r':.90};bad=0
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={'width':w,'height':h})
        await pg.goto('file://'+os.path.abspath(a.html));await pg.wait_for_timeout(800)
        for t in [float(x) for x in a.times.split(',')]:
            if a.seek:await pg.evaluate(a.seek.replace('{t}',str(t)))
            await pg.wait_for_timeout(300)
            o=await pg.evaluate(JS,[a.root,lim])
            print('t=%.2fs: %s'%(t,'OK' if not o else '%d chỗ tràn'%len(o)))
            for x in o[:10]:print('   -',x)
            bad+=len(o)
        await b.close()
    sys.exit(1 if bad else 0)
asyncio.run(main())
