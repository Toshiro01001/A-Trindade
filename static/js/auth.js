/* Portão de senha no cliente (site estático). Hash leve só para não deixar a senha à vista. */
(function(){
  function hstr(s){let h=5381>>>0;for(let i=0;i<s.length;i++){h=(((h<<5)+h)+s.charCodeAt(i))>>>0;}return h.toString(16);}
  const AUTH=window.SATUS_AUTH||{};
  const SS=window.sessionStorage;

  // pontos de "desbloqueado" no menu e nas portas
  function marks(){
    document.querySelectorAll("[data-c][href$='.html'], a.navlink").forEach(a=>{});
    Object.keys(AUTH).forEach(slug=>{
      if(SS.getItem("unlock_"+slug)==="1"){
        document.querySelectorAll('a[href="'+slug+'.html"]').forEach(a=>{
          if(!a.querySelector(".unlock-dot")){const s=document.createElement("span");s.className="unlock-dot";s.textContent="●";s.style.marginLeft="5px";a.appendChild(s);}
          const en=a.querySelector(".enter"); if(en) en.firstChild && (en.childNodes[0].nodeValue="Entrar ");
        });
      }
    });
  }
  marks();

  const slug=window.CLASSE;
  if(!slug) return;                 // páginas neutras só ganham os pontos

  const gate=document.getElementById("gate"),
        content=document.getElementById("classcontent"),
        form=document.getElementById("gateform"),
        input=document.getElementById("gatepwd"),
        err=document.getElementById("gateerr");
  let tent=0;

  function reveal(){ gate.style.display="none"; content.hidden=false; initStars(); applyStars(); logAccess(); }
  function isOpen(){ return SS.getItem("unlock_"+slug)==="1"; }

  if(isOpen()){ reveal(); }
  else { content.hidden=true; gate.style.display=""; }

  if(form) form.addEventListener("submit",function(e){
    e.preventDefault();
    const val=(input.value||"").trim();
    if(hstr(val)===AUTH[slug]){ SS.setItem("unlock_"+slug,"1"); err.textContent=""; reveal(); marks(); }
    else { tent++; err.textContent="ACESSO NEGADO · senha incorreta."+(tent>=3?(" · "+tent+" tentativas."):""); input.value=""; input.focus(); }
  });

  // encerrar sessão
  const lock=document.getElementById("locknow");
  if(lock) lock.addEventListener("click",function(e){ e.preventDefault(); SS.removeItem("unlock_"+slug); location.href="index.html"; });

  /* ---- patente por estrelas ---- */
  function stars(){ return parseInt(SS.getItem("stars_"+slug)||"1",10); }
  function initStars(){
    document.querySelectorAll("#starform .star").forEach(b=>{
      b.addEventListener("click",()=>{ SS.setItem("stars_"+slug,b.dataset.n); paintStars(); applyStars(); });
    });
    paintStars();
  }
  function paintStars(){
    const s=stars();
    document.querySelectorAll("#starform .star").forEach(b=>b.classList.toggle("lit",+b.dataset.n<=s));
    const n=document.querySelector(".patente-num"); if(n) n.textContent=s+"★";
  }
  function applyStars(){
    const s=stars();
    document.querySelectorAll(".resource[data-minstars]").forEach(r=>{
      const need=+r.dataset.minstars||0, locked=need>s;
      r.classList.toggle("locked",locked);
      const inner=r.querySelector(".res-inner"), den=r.querySelector(".res-denied"), lk=r.querySelector(".res-lock");
      if(inner) inner.style.display=locked?"none":"";
      if(den) den.style.display=locked?"":"none";
      if(lk) lk.style.display=locked?"":"none";
    });
  }
  /* ---- registro de acesso (cliente) ---- */
  function logAccess(){
    const box=document.getElementById("accesslist"); if(!box) return;
    const now=new Date().toLocaleString("pt-BR");
    let arr=JSON.parse(SS.getItem("log_"+slug)||"[]");
    arr.unshift("✔ "+now+" · Acesso concedido"); arr=arr.slice(0,6);
    SS.setItem("log_"+slug,JSON.stringify(arr));
    box.innerHTML=arr.map(l=>"<li>"+l+"</li>").join("");
  }
})();
