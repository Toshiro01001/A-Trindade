(function(){
"use strict";
const geo = JSON.parse(document.getElementById("geo").textContent);
const NS="http://www.w3.org/2000/svg";
const svg=document.getElementById("map"), vp=document.getElementById("viewport");
const el=(t,a)=>{const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);return e;};
const BYSLUG={}; geo.regioes.forEach(R=>BYSLUG[R.slug]=R);

/* ---- RNG + blob ---- */
function rng(seed){let s=seed>>>0;return()=>{s=(s*1664525+1013904223)>>>0;return s/4294967296;};}
function blob(cx,cy,r,irr,seed,n){const rnd=rng(seed),pts=[];
  for(let i=0;i<n;i++){const a=i/n*2*Math.PI,rr=r*(1-irr+rnd()*irr*2);pts.push([cx+Math.cos(a)*rr,cy+Math.sin(a)*rr*0.82]);}
  return smooth(pts);}
function smooth(p){let d=`M ${p[0][0].toFixed(1)} ${p[0][1].toFixed(1)} `;const N=p.length;
  for(let i=0;i<N;i++){const p0=p[(i-1+N)%N],p1=p[i],p2=p[(i+1)%N],p3=p[(i+2)%N];
    const c1x=p1[0]+(p2[0]-p0[0])/6,c1y=p1[1]+(p2[1]-p0[1])/6,c2x=p2[0]-(p3[0]-p1[0])/6,c2y=p2[1]-(p3[1]-p1[1])/6;
    d+=`C ${c1x.toFixed(1)} ${c1y.toFixed(1)} ${c2x.toFixed(1)} ${c2y.toFixed(1)} ${p2[0].toFixed(1)} ${p2[1].toFixed(1)} `;}
  return d+"Z";}

/* ---- Glacies Lied ---- */
function iceRing(){const g=el("g",{class:"ice-band"});const rnd=rng(7),cx=800,cy=500,N=64,inner=[];
  for(let i=0;i<N;i++){const a=i/N*2*Math.PI,rx=980+rnd()*70,ry=680+rnd()*60,spike=(i%2===0)?0:-38;
    inner.push([cx+Math.cos(a)*(rx+spike),cy+Math.sin(a)*(ry+spike)]);}
  let d="M -800 -500 L 3600 -500 L 3600 1500 L -800 1500 Z M "+inner[0][0].toFixed(0)+" "+inner[0][1].toFixed(0)+" ";
  for(let i=1;i<inner.length;i++)d+="L "+inner[i][0].toFixed(0)+" "+inner[i][1].toFixed(0)+" ";
  d+="Z"; g.appendChild(el("path",{d,class:"ice","fill-rule":"evenodd"}));
  const rnd2=rng(19);
  for(let i=0;i<10;i++){const x=250+rnd2()*500,y=-40+rnd2()*120,s=16+rnd2()*22;
    g.appendChild(el("path",{d:`M ${x} ${y} L ${x+s} ${y+s*1.6} L ${x-s} ${y+s*1.6} Z`,class:"ice",opacity:.85}));}
  return g;}

/* ---- construir o mundo ---- */
let iceGroup,labelEls=[],cityEls=[],localEls=[];
let drag=null,moved=false;
function build(){
  vp.appendChild(iceGroup=iceRing());
  geo.oceanos.forEach(o=>{const t=el("text",{x:o.xy[0],y:o.xy[1],class:"olabel","font-size":24,"text-anchor":"middle"});t.textContent=o.nome;vp.appendChild(t);labelEls.push(t);});
  geo.regioes.forEach(R=>{
    const g=el("g",{class:"region","data-slug":R.slug});
    if(R.ilhas){const rnd=rng(R.seed);
      for(let i=0;i<6;i++){const ox=R.cx+(rnd()-.5)*R.r*2.2,oy=R.cy+(rnd()-.5)*R.r*1.6,rr=R.r*(0.2+rnd()*0.28);
        g.appendChild(el("path",{d:blob(ox,oy,rr,0.5,R.seed+i*7,10),class:"land",fill:R.cor}));}
    }else{
      g.appendChild(el("path",{d:blob(R.cx,R.cy,R.r,0.42,R.seed,16),class:"land",fill:R.cor}));
      const rnd=rng(R.seed+3);
      for(let i=0;i<3;i++){const ox=R.cx+(rnd()-.5)*R.r,oy=R.cy+(rnd()-.5)*R.r*0.8,rr=R.r*(0.28+rnd()*0.2);
        g.appendChild(el("path",{d:blob(ox,oy,rr,0.5,R.seed+40+i,10),fill:R.cor2,"fill-opacity":.5,stroke:"none","pointer-events":"none"}));}
    }
    const lb=el("text",{x:R.label[0],y:R.label[1],class:"rlabel","font-size":R.r>150?32:22,"text-anchor":"middle"});lb.textContent=R.nome;g.appendChild(lb);labelEls.push(lb);
    const sz=el("text",{x:R.label[0],y:R.label[1]+22,class:"rsize","font-size":15,"text-anchor":"middle"});sz.textContent=R.tamanho;g.appendChild(sz);labelEls.push(sz);
    R.paises.forEach(p=>{const x=R.cx+p.dx,y=R.cy+p.dy;
      const cg=el("g",{class:"city capital","data-slug":R.slug,"data-x":x,"data-y":y});
      cg.appendChild(el("circle",{cx:x,cy:y,r:6,class:"dot"}));
      const nm=el("text",{x:x+11,y:y+5,class:"cname"});nm.textContent=p.capital;cg.appendChild(nm);
      cg.addEventListener("click",ev=>{ev.stopPropagation();if(moved)return;openRegion(R,null);flyTo(x,y,2.4);});
      g.appendChild(cg);cityEls.push(cg);});
    g.addEventListener("click",()=>{if(moved)return;openRegion(R,null);flyTo(R.cx,R.cy,1.4);});
    vp.appendChild(g);
  });
}

/* ---- pan / zoom ---- */
let tx=160,ty=100,k=0.8;
function apply(){vp.setAttribute("transform",`translate(${tx} ${ty}) scale(${k})`);}
function toVB(evt){const pt=svg.createSVGPoint();pt.x=evt.clientX;pt.y=evt.clientY;return pt.matrixTransform(svg.getScreenCTM().inverse());}
function zoomAt(vx,vy,f){const nk=Math.max(0.45,Math.min(6,k*f));const wx=(vx-tx)/k,wy=(vy-ty)/k;k=nk;tx=vx-wx*k;ty=vy-wy*k;apply();}
const coords=document.getElementById("coords");
svg.addEventListener("wheel",e=>{e.preventDefault();const v=toVB(e);zoomAt(v.x,v.y,e.deltaY<0?1.16:0.86);},{passive:false});

svg.addEventListener("pointerdown",e=>{drag={x:e.clientX,y:e.clientY,tx,ty};moved=false;svg.classList.add("grabbing");});
window.addEventListener("pointermove",e=>{
  const v=toVB(e);coords.textContent=`SATUS · ${((v.x-tx)/k-800)/8|0} , ${(500-(v.y-ty)/k)/8|0}`;
  if(!drag)return;const dx=e.clientX-drag.x,dy=e.clientY-drag.y;if(Math.abs(dx)+Math.abs(dy)>5)moved=true;
  tx=drag.tx+dx*(svg.viewBox.baseVal.width/svg.clientWidth);ty=drag.ty+dy*(svg.viewBox.baseVal.height/svg.clientHeight);apply();
});
window.addEventListener("pointerup",()=>{drag=null;svg.classList.remove("grabbing");});
function flyTo(x,y,nk){const sx=tx,sy=ty,sk=k,ex=800-x*nk,ey=500-y*nk;let t0=null;
  function step(ts){if(!t0)t0=ts;let p=Math.min(1,(ts-t0)/500);p=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;
    tx=sx+(ex-sx)*p;ty=sy+(ey-sy)*p;k=sk+(nk-sk)*p;apply();if(p<1)requestAnimationFrame(step);}
  requestAnimationFrame(step);}
document.getElementById("zin").onclick=()=>zoomAt(800,500,1.3);
document.getElementById("zout").onclick=()=>zoomAt(800,500,0.77);
document.getElementById("reset").onclick=()=>{flyTo(800,500,0.8);closePanel();desel();};

/* ---- painel ---- */
const panel=document.getElementById("panel"),pbody=document.getElementById("pbody");
function desel(){document.querySelectorAll(".region.sel").forEach(r=>r.classList.remove("sel"));}
function closePanel(){panel.classList.remove("on");}
document.getElementById("pclose").onclick=closePanel;
function openRegion(R,focusPais){
  if(!R)return;
  desel();const g=document.querySelector(`.region[data-slug="${R.slug}"]`);if(g)g.classList.add("sel");
  const langs=R.linguas.map(l=>`<li>${l}</li>`).join("");
  const paises=R.paises.map(p=>`<div class="p-country" data-x="${R.cx+p.dx}" data-y="${R.cy+p.dy}"><h5>${p.nome}</h5><div class="cap">Capital: ${p.capital}</div><p class="cnote">${p.nota}</p></div>`).join("");
  pbody.innerHTML=`<svg class="p-seal" viewBox="0 0 300 300" data-seal="trindade"></svg>
    <div class="p-kick">REGISTRO GEOGRÁFICO</div><div class="p-name">${R.nome}</div><p class="p-size">${R.tamanho}</p>${R.area?`<p class="p-area">Área: ${R.area}</p>`:""}${R.alem?`<div class="p-alem">Além das Glacies Lied</div>`:""}
    <p class="p-desc">${R.descricao}</p>
    <div class="p-sec">Línguas</div><ul class="p-langs">${langs}</ul>
    <div class="p-sec">Império</div><p class="p-emp">${R.imperio}</p>
    <div class="p-sec">Países</div>${paises}`;
  if(window.TrindadeSeals)window.TrindadeSeals.make(pbody.querySelector(".p-seal"),"trindade");
  pbody.querySelectorAll(".p-country").forEach(c=>c.onclick=()=>flyTo(+c.dataset.x,+c.dataset.y,2.4));
  panel.classList.add("on");
}

/* ---- busca ---- */
const idx=[];
geo.regioes.forEach(R=>{idx.push({k:"Região",label:R.nome,x:R.cx,y:R.cy,R,zoom:1.4});
  R.paises.forEach(p=>{idx.push({k:"País",label:p.nome,x:R.cx+p.dx,y:R.cy+p.dy,R,zoom:2.2});
    idx.push({k:"Cidade",label:p.capital,x:R.cx+p.dx,y:R.cy+p.dy,R,zoom:2.6});});});
(geo.locais||[]).forEach(L=>idx.push({k:"Local",label:L.nome,x:L.x,y:L.y,local:L,zoom:2.6}));
const search=document.getElementById("search"),results=document.getElementById("results");
function norm(s){return s.normalize("NFD").replace(/[\u0300-\u036f]/g,"").toLowerCase();}
search.addEventListener("input",()=>{const q=norm(search.value.trim());results.innerHTML="";
  if(!q){results.classList.remove("on");return;}
  idx.filter(i=>norm(i.label).includes(q)).slice(0,8).forEach(h=>{const b=document.createElement("button");
    b.innerHTML=`<span class="rk">${h.k}</span>${h.label}`;
    b.onclick=()=>{if(h.local)openLocal(h.local);else openRegion(h.R,null);flyTo(h.x,h.y,h.zoom);results.classList.remove("on");search.value=h.label;};
    results.appendChild(b);});
  results.classList.toggle("on",results.children.length>0);});
document.addEventListener("click",e=>{if(!e.target.closest(".searchbox"))results.classList.remove("on");});

/* ---- camadas ---- */
document.getElementById("tgLabels").onchange=e=>labelEls.forEach(l=>l.style.display=e.target.checked?"":"none");
document.getElementById("tgCities").onchange=e=>cityEls.forEach(c=>c.style.display=e.target.checked?"":"none");
document.getElementById("tgIce").onchange=e=>iceGroup.style.display=e.target.checked?"":"none";
var _tl=document.getElementById("tgLocais");if(_tl)_tl.onchange=e=>localEls.forEach(l=>l.style.display=e.target.checked?"":"none");

function buildLocais(){
  (geo.locais||[]).forEach(L=>{
    const g=el("g",{class:"local","data-x":L.x,"data-y":L.y});
    g.appendChild(el("path",{d:`M ${L.x} ${L.y-9} L ${L.x+8} ${L.y} L ${L.x} ${L.y+9} L ${L.x-8} ${L.y} Z`,class:"ldot"}));
    const nm=el("text",{x:L.x+13,y:L.y+5,class:"lname"});nm.textContent=L.nome;g.appendChild(nm);
    g.addEventListener("click",ev=>{ev.stopPropagation();if(moved)return;openLocal(L);flyTo(L.x,L.y,2.6);});
    vp.appendChild(g);localEls.push(g);
  });
}
function openLocal(L){
  desel();
  pbody.innerHTML=`<svg class="p-seal" viewBox="0 0 300 300" data-seal="trindade"></svg><div class="p-kick">LOCAL NOTÁVEL</div><div class="p-name">${L.nome}</div><p class="p-desc">${L.nota}</p>`;
  if(window.TrindadeSeals)window.TrindadeSeals.make(pbody.querySelector(".p-seal"),"trindade");
  panel.classList.add("on");
}
build();buildLocais();apply();
})();
