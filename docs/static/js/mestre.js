/* ABA DO MESTRE — decriptação real no navegador.
   Os documentos ficam cifrados (AES-GCM, chave PBKDF2 da senha do Mestre).
   Sem a senha correta, a decriptação FALHA e nada é reconstruído.
   O conteúdo decifrado vive só na memória desta aba: recarregar exige a senha de novo. */
(function(){
  "use strict";
  var DATA = window.SATUS_MESTRE || null;

  var gate     = document.getElementById("gate");
  var content  = document.getElementById("mestrecontent");
  var form     = document.getElementById("gateform");
  var input    = document.getElementById("gatepwd");
  var err      = document.getElementById("gateerr");
  var lib      = document.getElementById("mestrelib");
  var subtle   = (window.crypto && window.crypto.subtle) ? window.crypto.subtle : null;
  var tent = 0;
  var blobUrls = [];

  // ---- utilidades base64 <-> bytes ----
  function b64ToBytes(b64){
    var bin = atob(b64), n = bin.length, out = new Uint8Array(n);
    for (var i=0;i<n;i++) out[i] = bin.charCodeAt(i);
    return out;
  }

  // ---- checagem de suporte ----
  if(!DATA){
    if(err) err.textContent = "FALHA · pacote do Mestre não encontrado (mestredata.js).";
    if(form) form.querySelector("button").disabled = true;
    return;
  }
  if(!subtle){
    if(err) err.textContent = "NAVEGADOR SEM SUPORTE · abra no Chrome, Edge ou Firefox, ou sirva a pasta por um servidor local.";
    if(form) form.querySelector("button").disabled = true;
    return;
  }

  // ---- derivar chave e decifrar ----
  function deriveKey(password){
    var enc = new TextEncoder();
    return subtle.importKey("raw", enc.encode(password), {name:"PBKDF2"}, false, ["deriveKey"])
      .then(function(baseKey){
        return subtle.deriveKey(
          { name:"PBKDF2", salt:b64ToBytes(DATA.kdf.salt), iterations:DATA.kdf.iter, hash:"SHA-256" },
          baseKey,
          { name:"AES-GCM", length:256 },
          false,
          ["decrypt"]
        );
      });
  }

  function decryptPayload(password){
    return deriveKey(password).then(function(key){
      return subtle.decrypt({ name:"AES-GCM", iv:b64ToBytes(DATA.iv) }, key, b64ToBytes(DATA.ct));
    }).then(function(buf){
      var json = new TextDecoder().decode(buf);
      return JSON.parse(json);
    });
  }

  // ---- montar a biblioteca decifrada ----
  function render(payload){
    // liberar quaisquer blobs anteriores
    blobUrls.forEach(function(u){ try{ URL.revokeObjectURL(u); }catch(e){} });
    blobUrls = [];
    lib.innerHTML = "";

    payload.categorias.forEach(function(cat){
      var label = document.createElement("div");
      label.className = "section-label wrap alt";
      label.innerHTML = "<span></span>";
      label.querySelector("span").textContent = cat.nome;
      lib.appendChild(label);

      if(cat.nota){
        var nota = document.createElement("p");
        nota.className = "cat-nota wrap";
        nota.textContent = cat.nota;
        lib.appendChild(nota);
      }

      var wrap = document.createElement("div");
      wrap.className = "resources wrap";
      lib.appendChild(wrap);

      cat.docs.forEach(function(d){
        var bytes = b64ToBytes(d.data);
        var blob  = new Blob([bytes], { type:d.mime || "application/pdf" });
        var url   = URL.createObjectURL(blob);
        blobUrls.push(url);

        var card = document.createElement("section");
        card.className = "resource mestre-doc";

        var head = document.createElement("header");
        head.className = "res-head";
        var h3 = document.createElement("h3"); h3.textContent = d.titulo;
        head.appendChild(h3);
        if(d.subtitulo){
          var note = document.createElement("p");
          note.className = "res-note";
          note.textContent = d.subtitulo;
          head.appendChild(note);
        }
        card.appendChild(head);

        var actions = document.createElement("div");
        actions.className = "doc-actions";

        var toggle = document.createElement("button");
        toggle.type = "button";
        toggle.className = "doc-btn";
        toggle.textContent = "Visualizar";

        var open = document.createElement("a");
        open.className = "doc-btn ghost";
        open.href = url; open.target = "_blank"; open.rel = "noopener";
        open.textContent = "Abrir em nova aba";

        var dl = document.createElement("a");
        dl.className = "doc-btn ghost";
        dl.href = url; dl.download = d.arquivo || (d.titulo + ".pdf");
        dl.textContent = "Baixar PDF";

        actions.appendChild(toggle);
        actions.appendChild(open);
        actions.appendChild(dl);
        card.appendChild(actions);

        var viewer = document.createElement("div");
        viewer.className = "doc-viewer";
        viewer.hidden = true;
        card.appendChild(viewer);

        toggle.addEventListener("click", function(){
          if(viewer.hidden){
            if(!viewer.firstChild){
              var frame = document.createElement("iframe");
              frame.className = "doc-frame";
              frame.src = url;
              frame.title = d.titulo;
              viewer.appendChild(frame);
            }
            viewer.hidden = false;
            toggle.textContent = "Recolher";
          } else {
            viewer.hidden = true;
            toggle.textContent = "Visualizar";
          }
        });

        wrap.appendChild(card);
      });
    });
  }

  function reveal(payload){
    render(payload);
    gate.style.display = "none";
    content.hidden = false;
    err.textContent = "";
  }

  // ---- submit ----
  form.addEventListener("submit", function(e){
    e.preventDefault();
    var val = (input.value || "");
    if(!val){ return; }
    var btn = form.querySelector("button");
    btn.disabled = true; err.textContent = "Decifrando…";
    decryptPayload(val).then(function(payload){
      btn.disabled = false;
      reveal(payload);
    }).catch(function(){
      btn.disabled = false;
      tent++;
      err.textContent = "ACESSO NEGADO · senha incorreta." + (tent>=3 ? (" · " + tent + " tentativas.") : "");
      input.value = ""; input.focus();
    });
  });

  // ---- encerrar sessão: derruba o conteúdo da memória ----
  var lock = document.getElementById("locknow");
  if(lock) lock.addEventListener("click", function(e){
    e.preventDefault();
    blobUrls.forEach(function(u){ try{ URL.revokeObjectURL(u); }catch(e){} });
    blobUrls = [];
    location.href = "index.html";
  });
})();
