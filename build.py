# -*- coding: utf-8 -*-
"""
GERADOR DO SITE (Python) — Ecos das Ruínas.
Lê os dados (content.py, world.py) e as senhas (config.py) e gera o site
ESTÁTICO na pasta 'site/'. Depois é só abrir 'site/index.html' no navegador.

    python build.py

Para trocar senhas ou textos: edite config.py / content.py / world.py e rode de novo.
"""
import json, shutil, pathlib, os, base64, hashlib
from markupsafe import Markup, escape
from jinja2 import Environment, FileSystemLoader, select_autoescape
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import config, content, world, lore, codex, regras, mestre

# Iterações do PBKDF2 (mesmo valor lido pelo navegador para reconstruir a chave)
MESTRE_ITER = 200000

OUT = pathlib.Path("docs")

VER = "4"  # muda a cada build para furar o cache do navegador

def url_for(endpoint, **kw):
    if endpoint == "static":
        f = kw["filename"]
        return "static/" + f + (("?v=" + VER) if f.endswith((".js", ".css")) else "")
    if endpoint == "index":   return "index.html"
    if endpoint == "mundo":   return "mundo.html"
    if endpoint == "mestre":  return "mestre.html"
    if endpoint == "classe":  return kw["slug"] + ".html"
    return "#"

def classif(text):
    span = ('<span class="redacted" tabindex="0" role="button" '
            'aria-label="Informacao classificada">........</span>')
    parts = [str(escape(p)) for p in (text or "").split("\u0007")]
    return Markup(span.join(parts))

def hstr(s):  # mesmo hash usado no auth.js
    h = 5381
    for ch in s:
        h = ((h << 5) + h + ord(ch)) & 0xFFFFFFFF
    return format(h, "x")

env = Environment(loader=FileSystemLoader("templates"),
                  autoescape=select_autoescape(["html"]))
env.globals.update(url_for=url_for, CLASSES=content.CLASSES, unlocked={}, patente=1)
env.filters["classif"] = classif

def render(tpl, out, **ctx):
    html = env.get_template(tpl).render(**ctx)
    (OUT / out).write_text(html, encoding="utf-8")
    print("  gerado:", out)

def build_mestre():
    """Lê os PDFs de mestre_docs/, monta um pacote JSON e o CIFRA com AES-GCM
    (chave derivada da SENHA_MESTRE por PBKDF2). Grava só o cifrado em mestredata.js.
    Sem a senha, nada do conteúdo (nem os títulos) é legível no site."""
    docs_dir = pathlib.Path("mestre_docs")
    categorias, faltando = [], []
    for cat in mestre.CATEGORIAS:
        itens = []
        for titulo, subtitulo, arq in cat["docs"]:
            p = docs_dir / arq
            if not p.exists():
                faltando.append(arq); continue
            data = p.read_bytes()
            itens.append({
                "titulo": titulo, "subtitulo": subtitulo, "arquivo": arq,
                "mime": "application/pdf",
                "data": base64.b64encode(data).decode("ascii"),
            })
        if itens:
            categorias.append({"nome": cat["nome"], "nota": cat.get("nota", ""), "docs": itens})

    if faltando:
        print("  AVISO · arquivos não encontrados em mestre_docs/:", ", ".join(faltando))

    plaintext = json.dumps({"categorias": categorias}, ensure_ascii=False).encode("utf-8")

    salt = os.urandom(16)
    iv   = os.urandom(12)
    key  = hashlib.pbkdf2_hmac("sha256", config.SENHA_MESTRE.encode("utf-8"), salt, MESTRE_ITER, dklen=32)
    ct   = AESGCM(key).encrypt(iv, plaintext, None)   # ciphertext + tag (16 bytes), padrão Web Crypto

    pkg = {
        "v": 1,
        "kdf": {"salt": base64.b64encode(salt).decode(), "iter": MESTRE_ITER, "hash": "SHA-256"},
        "iv": base64.b64encode(iv).decode(),
        "ct": base64.b64encode(ct).decode(),
    }
    (OUT / "static/js/mestredata.js").write_text(
        "window.SATUS_MESTRE=" + json.dumps(pkg) + ";", encoding="utf-8")
    total = sum(len(d["docs"]) for d in categorias)
    print("  cifrado: %d documento(s) do Mestre (%d KB de cifra)" % (total, len(pkg["ct"]) // 1024))

def main():
    if OUT.exists(): shutil.rmtree(OUT)
    (OUT / "static").mkdir(parents=True)
    shutil.copytree("static", OUT / "static", dirs_exist_ok=True)
    if pathlib.Path("img").exists():
        shutil.copytree("img", OUT / "img", dirs_exist_ok=True)

    # authdata.js com as senhas em hash (não em texto)
    auth = {slug: hstr(pw) for slug, pw in config.SENHAS.items()}
    (OUT / "static/js/authdata.js").write_text(
        "window.SATUS_AUTH=" + json.dumps(auth) + ";", encoding="utf-8")

    # pacote cifrado da aba do Mestre
    build_mestre()

    print("Gerando site estático em ./docs")
    render("index.html", "index.html", boasvindas=codex.BOASVINDAS)
    render("mundo.html", "mundo.html",
           geo=json.dumps({"regioes": world.REGIOES, "oceanos": world.OCEANOS, "locais": world.LOCAIS}, ensure_ascii=False))
    render("mestre.html", "mestre.html", active="mestre")
    render("codex.html", "codex.html", codex=codex.CODEX, active="codex")
    render("cacadores.html", "cacadores.html", roster=codex.ROSTER, legenda=codex.STAR_LEGEND, active="cacadores")
    render("regras.html", "regras.html", regras=regras.REGRAS, active="regras")
    for slug, c in content.CLASSES.items():
        render("classe_static.html", slug + ".html", c=c, active=slug, lore=lore.LORE.get(slug, []), classificado=codex.ALEM.get(slug, ""))
    print("Pronto. Abra docs/index.html no navegador.")

if __name__ == "__main__":
    main()
