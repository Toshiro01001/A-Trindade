/* Gerador dos selos da Trindade (SVG procedural) */
(function(){
  const NS="http://www.w3.org/2000/svg";
  function el(t,a){const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);return e;}
  function leaf(cx,cy,ang,len,wid){return el("path",{d:`M ${-len} 0 Q 0 ${-wid} ${len} 0 Q 0 ${wid} ${-len} 0 Z`,transform:`translate(${cx} ${cy}) rotate(${ang})`,fill:"currentColor","fill-opacity":.9});}
  function wreath(g,cx,cy,r,n){
    for(const side of [-1,1]) for(let i=0;i<n;i++){
      const t=i/(n-1), a=(side<0?200-t*120:340+t*120), rad=a*Math.PI/180;
      const lx=cx+Math.cos(rad)*r, ly=cy-Math.sin(rad)*r, tang=a+(side<0?-90:90), L=13-t*4;
      g.appendChild(leaf(lx,ly,-tang,L,L*0.42));
      const li=leaf(lx,ly,-tang+(side<0?32:-32),L*0.8,L*0.34);li.setAttribute("fill-opacity",.6);g.appendChild(li);
    }
    g.appendChild(leaf(cx,cy-r-6,0,10,5));
  }
  function eye(g,cx,cy,r){
    g.appendChild(el("circle",{cx,cy,r:r*0.98,fill:"none",stroke:"currentColor","stroke-width":2.4,"data-draw":1}));
    g.appendChild(el("circle",{cx,cy,r:r*0.62,fill:"none",stroke:"currentColor","stroke-width":1.6}));
    const n=54,r1=r*0.34,r2=r*0.6;
    for(let i=0;i<n;i++){const a=i/n*2*Math.PI;g.appendChild(el("line",{x1:cx+Math.cos(a)*r1,y1:cy+Math.sin(a)*r1,x2:cx+Math.cos(a)*r2,y2:cy+Math.sin(a)*r2,stroke:"currentColor","stroke-width":1.1,"stroke-opacity":.85}));}
    g.appendChild(el("circle",{cx,cy,r:r*0.30,fill:"currentColor","fill-opacity":.14}));
    g.appendChild(el("circle",{cx,cy,r:r*0.15,fill:"currentColor"}));
    g.appendChild(el("circle",{cx:cx-r*0.05,cy:cy-r*0.05,r:r*0.04,fill:"var(--bg)"}));
  }
  function dot(g,cx,cy){g.appendChild(el("line",{x1:cx,y1:cy-9,x2:cx,y2:cy-4,stroke:"currentColor","stroke-width":2}));g.appendChild(el("circle",{cx,cy:cy+1,r:1.6,fill:"currentColor"}));g.appendChild(el("circle",{cx,cy:cy+7,r:3.2,fill:"none",stroke:"currentColor","stroke-width":1.4}));}

  function make(svg,type){
    while(svg.firstChild)svg.removeChild(svg.firstChild);
    const g=el("g",{});svg.appendChild(g);const cx=150,cy=150;
    if(type==="trindade"){
      g.appendChild(el("path",{d:"M150 34 L262 250 L38 250 Z",fill:"currentColor",stroke:"currentColor","stroke-width":2,"stroke-linejoin":"round","data-draw":1}));
      const cut="var(--bg)";
      g.appendChild(el("path",{d:"M150 96 L182 176 L150 232 L118 176 Z",fill:cut}));
      g.appendChild(el("path",{d:"M96 182 L128 244 L64 244 Z",fill:cut}));
      g.appendChild(el("path",{d:"M204 182 L236 244 L172 244 Z",fill:cut}));
    } else if(type==="conh"){
      g.appendChild(el("circle",{cx,cy,r:138,fill:"none",stroke:"currentColor","stroke-width":1.4,"stroke-opacity":.7,"data-draw":1}));
      wreath(g,cx,cy,120,7);
      g.appendChild(el("path",{d:"M150 34 L248 210 L52 210 Z",fill:"none",stroke:"currentColor","stroke-width":3,"stroke-linejoin":"round","data-draw":1}));
      g.appendChild(el("path",{d:"M150 266 L52 90 L248 90 Z",fill:"none",stroke:"currentColor","stroke-width":3,"stroke-linejoin":"round","data-draw":1}));
      eye(g,cx,cy,52);dot(g,cx,52);const d2=el("g",{transform:`rotate(180 ${cx} ${cy})`});svg.appendChild(d2);dot(d2,cx,52);
    } else if(type==="adm"){
      g.appendChild(el("circle",{cx,cy,r:138,fill:"none",stroke:"currentColor","stroke-width":1.2,"stroke-opacity":.6,"data-draw":1}));
      wreath(g,cx,cy,120,8);
      g.appendChild(el("circle",{cx,cy,r:70,fill:"none",stroke:"currentColor","stroke-width":1.6,"stroke-opacity":.55}));
      eye(g,cx,cy,58);
    } else if(type==="expl"){
      g.appendChild(el("circle",{cx,cy,r:138,fill:"none",stroke:"currentColor","stroke-width":1.2,"stroke-opacity":.55,"data-draw":1}));
      wreath(g,cx,cy,122,8);
      for(let i=0;i<8;i++){const a=i*45*Math.PI/180,main=(i%2===0),R=main?120:58,tx=cx+Math.cos(a)*R,ty=cy+Math.sin(a)*R,pa=a+Math.PI/2,w=9;
        const bx=cx+Math.cos(pa)*w,by=cy+Math.sin(pa)*w,bx2=cx-Math.cos(pa)*w,by2=cy-Math.sin(pa)*w;
        g.appendChild(el("path",{d:`M ${cx} ${cy} L ${bx} ${by} L ${tx} ${ty} Z`,fill:"currentColor","fill-opacity":main?.85:.5}));
        g.appendChild(el("path",{d:`M ${cx} ${cy} L ${bx2} ${by2} L ${tx} ${ty} Z`,fill:"currentColor","fill-opacity":main?.35:.2,stroke:"currentColor","stroke-width":.6}));}
      g.appendChild(el("circle",{cx,cy,r:12,fill:"var(--bg)",stroke:"currentColor","stroke-width":2.5}));
      g.appendChild(el("circle",{cx,cy,r:4,fill:"currentColor"}));
      [[cx,cy-132],[cx+132,cy],[cx,cy+132],[cx-132,cy]].forEach(p=>g.appendChild(el("circle",{cx:p[0],cy:p[1],r:4,fill:"none",stroke:"currentColor","stroke-width":1.6})));
    }
  }
  window.TrindadeSeals={make};
  document.addEventListener("DOMContentLoaded",()=>{
    document.querySelectorAll("svg[data-seal]").forEach(s=>make(s,s.getAttribute("data-seal")));
    if(window.TrindadeSite&&window.TrindadeSite.primeAll)window.TrindadeSite.primeAll();
  });
})();
