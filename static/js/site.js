/* Interações: acordeão de regalias + animação de gravação (etch) */
(function(){
  function prime(svg){svg.querySelectorAll("[data-draw]").forEach(p=>{try{const l=Math.ceil(p.getTotalLength?p.getTotalLength():600);p.style.setProperty("--len",l);}catch(e){p.style.setProperty("--len",600);}});}
  function primeAll(){document.querySelectorAll("svg.etch").forEach(prime);}
  window.TrindadeSite={prime,primeAll};
  document.addEventListener("DOMContentLoaded",()=>{
    document.querySelectorAll(".reg").forEach(reg=>{
      const head=reg.querySelector(".reg-head"),body=reg.querySelector(".reg-body");
      head.addEventListener("click",()=>{
        const open=reg.classList.toggle("open");
        head.setAttribute("aria-expanded",open);
        body.style.maxHeight=open?body.scrollHeight+"px":0;
      });
    });
  });

  document.addEventListener("DOMContentLoaded",()=>{
    const here=(location.pathname.split("/").pop()||"index.html");
    document.querySelectorAll(".topbar a").forEach(a=>{
      const href=(a.getAttribute("href")||"").split("/").pop();
      if(href===here) a.addEventListener("click",e=>e.preventDefault());
    });
  });
})();
