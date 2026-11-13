/* Portão das classes: decriptação real no navegador.
   O conteúdo de cada classe chega cifrado em classe-<slug>.js (AES-GCM).
   A senha abre a chave privada da classe (PBKDF2 + AES-GCM), que abre o conteúdo
   (ECDH + HKDF + AES-GCM). Sem a senha certa, nada é montado.
   A chave aberta fica só nesta aba (sessionStorage), para não pedir a senha a cada página. */
(function(){
  "use strict";
  var SLUGS=["conhecimento","exploracao","administracao"];
  var SS=window.sessionStorage;
  var subtle=(window.crypto&&window.crypto.subtle)?window.crypto.subtle:null;
  var enc=new TextEncoder();

  function ssGet(k){ try{ return SS.getItem(k); }catch(e){ return null; } }
  function ssSet(k,v){ try{ SS.setItem(k,v); }catch(e){} }
  function ssDel(k){ try{ SS.removeItem(k); }catch(e){} }
  function bytes(b64){ var s=atob(b64),o=new Uint8Array(s.length); for(var i=0;i<s.length;i++)o[i]=s.charCodeAt(i); return o; }
  function texto64(buf){ var u=new Uint8Array(buf),s=""; for(var i=0;i<u.length;i++)s+=String.fromCharCode(u[i]); return btoa(s); }

  // pontos de "desbloqueado" no menu e nas portas
  function marks(){
    SLUGS.forEach(function(slug){
      if(!ssGet("chave_"+slug)) return;
      document.querySelectorAll('a[href="'+slug+'.html"]').forEach(function(a){
        if(!a.querySelector(".unlock-dot")){var s=document.createElement("span");s.className="unlock-dot";s.textContent="●";s.style.marginLeft="5px";a.appendChild(s);}
        var en=a.querySelector(".enter"); if(en&&en.firstChild) en.childNodes[0].nodeValue="Entrar ";
      });
    });
  }
  marks();

  var slug=window.CLASSE;
  if(!slug) return;                 // páginas neutras só ganham os pontos

  var PKG=window.SATUS_CLASSE||null;
  var gate=document.getElementById("gate"),
      content=document.getElementById("classcontent"),
      form=document.getElementById("gateform"),
      input=document.getElementById("gatepwd"),
      err=document.getElementById("gateerr"),
      botao=form?form.querySelector("button"):null;
  var tent=0;

  if(!PKG||PKG.slug!==slug){
    if(err) err.textContent="FALHA · arquivo da classe não encontrado.";
    if(botao) botao.disabled=true;
    return;
  }
  if(!subtle){
    if(err) err.textContent="NAVEGADOR SEM SUPORTE · abra no Chrome, Edge, Firefox ou Safari atualizado.";
    if(botao) botao.disabled=true;
    return;
  }

  // senha -> chave privada da classe (PKCS8)
  function abrirChave(senha){
    var k=PKG.chave;
    return subtle.importKey("raw",enc.encode(senha),{name:"PBKDF2"},false,["deriveKey"])
      .then(function(base){
        return subtle.deriveKey({name:"PBKDF2",salt:bytes(k.salt),iterations:k.iter,hash:"SHA-256"},
          base,{name:"AES-GCM",length:256},false,["decrypt"]);
      })
      .then(function(chave){ return subtle.decrypt({name:"AES-GCM",iv:bytes(k.iv)},chave,bytes(k.ct)); });
  }
  // chave privada -> HTML da classe
  function abrirConteudo(der){
    var c=PKG.conteudo, curva={name:"ECDH",namedCurve:"P-256"};
    return Promise.all([
      subtle.importKey("pkcs8",der,curva,false,["deriveBits"]),
      subtle.importKey("raw",bytes(c.eph),curva,false,[])
    ]).then(function(k){ return subtle.deriveBits({name:"ECDH",public:k[1]},k[0],256); })
      .then(function(bits){ return subtle.importKey("raw",bits,"HKDF",false,["deriveKey"]); })
      .then(function(hk){
        return subtle.deriveKey({name:"HKDF",hash:"SHA-256",salt:bytes(c.hsalt),info:enc.encode("trindade-classe-v1:"+slug)},
          hk,{name:"AES-GCM",length:256},false,["decrypt"]);
      })
      .then(function(chave){ return subtle.decrypt({name:"AES-GCM",iv:bytes(c.iv)},chave,bytes(c.ct)); })
      .then(function(buf){ return new TextDecoder().decode(buf); });
  }

  // monta o conteúdo decifrado (HTML gerado pelo build, não por usuários)
  function montar(html){
    content.innerHTML=html;
    if(window.TrindadeSeals) content.querySelectorAll("svg[data-seal]").forEach(function(s){ window.TrindadeSeals.make(s,s.getAttribute("data-seal")); });
    if(window.TrindadeSite){ window.TrindadeSite.bindRegs(content); window.TrindadeSite.primeAll(); }
    var lock=document.getElementById("locknow");
    if(lock) lock.addEventListener("click",function(e){ e.preventDefault(); ssDel("chave_"+slug); location.href="index.html"; });
    gate.style.display="none"; gate.style.visibility=""; content.hidden=false;
    initStars(); applyStars(); logAccess(); marks();
  }
  function mostrarPortao(){ gate.style.display=""; gate.style.visibility=""; content.hidden=true; }

  // reabrir nesta aba, se a chave já foi aberta antes
  var guardada=ssGet("chave_"+slug);
  if(guardada){
    gate.style.visibility="hidden";
    abrirConteudo(bytes(guardada)).then(montar).catch(function(){ ssDel("chave_"+slug); mostrarPortao(); });
  } else { mostrarPortao(); }

  if(form) form.addEventListener("submit",function(e){
    e.preventDefault();
    var val=(input.value||"").trim();
    if(!val) return;
    botao.disabled=true; var rot=botao.textContent; botao.textContent="Verificando…"; err.textContent="";
    var der;
    abrirChave(val)
      .then(function(d){ der=d; return abrirConteudo(d); })
      .then(function(html){ ssSet("chave_"+slug,texto64(der)); montar(html); })
      .catch(function(){
        tent++; err.textContent="ACESSO NEGADO · senha incorreta."+(tent>=3?(" · "+tent+" tentativas."):"");
        input.value=""; input.focus();
      })
      .then(function(){ botao.disabled=false; botao.textContent=rot; });
  });

  /* ---- patente por estrelas ---- */
  function stars(){ return parseInt(ssGet("stars_"+slug)||"1",10); }
  function initStars(){
    document.querySelectorAll("#starform .star").forEach(function(b){
      b.addEventListener("click",function(){ ssSet("stars_"+slug,b.dataset.n); paintStars(); applyStars(); });
    });
    paintStars();
  }
  function paintStars(){
    var s=stars();
    document.querySelectorAll("#starform .star").forEach(function(b){ b.classList.toggle("lit",+b.dataset.n<=s); });
    var n=document.querySelector(".patente-num"); if(n) n.textContent=s+"★";
  }
  function applyStars(){
    var s=stars();
    document.querySelectorAll(".resource[data-minstars]").forEach(function(r){
      var need=+r.dataset.minstars||0, locked=need>s;
      r.classList.toggle("locked",locked);
      var inner=r.querySelector(".res-inner"), den=r.querySelector(".res-denied"), lk=r.querySelector(".res-lock");
      if(inner) inner.style.display=locked?"none":"";
      if(den) den.style.display=locked?"":"none";
      if(lk) lk.style.display=locked?"":"none";
    });
  }
  /* ---- registro de acesso (cliente) ---- */
  function logAccess(){
    var box=document.getElementById("accesslist"); if(!box) return;
    var now=new Date().toLocaleString("pt-BR"), arr;
    try{ arr=JSON.parse(ssGet("log_"+slug)||"[]"); }catch(e){ arr=[]; }
    arr.unshift("✔ "+now+" · Acesso concedido"); arr=arr.slice(0,6);
    ssSet("log_"+slug,JSON.stringify(arr));
    box.textContent="";
    arr.forEach(function(l){ var li=document.createElement("li"); li.textContent=l; box.appendChild(li); });
  }
})();
