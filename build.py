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
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes, serialization
import config, content, world, lore, codex, regras

# Iterações do PBKDF2 (mesmo valor lido pelo navegador para reconstruir a chave)
MESTRE_ITER = 200000
# Iterações do PBKDF2 que protegem a chave privada de cada classe
CLASSE_ITER = 600000

OUT = pathlib.Path("docs")

VER = "5"  # muda a cada build para furar o cache do navegador

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

env = Environment(loader=FileSystemLoader("templates"),
                  autoescape=select_autoescape(["html"]))
env.globals.update(url_for=url_for, CLASSES=content.CLASSES, unlocked={}, patente=1, VER=VER)
env.filters["classif"] = classif

def render(tpl, out, **ctx):
    html = env.get_template(tpl).render(**ctx)
    (OUT / out).write_text(html, encoding="utf-8")
    print("  gerado:", out)

def mestre_disponivel():
    """A cifra só é refeita com a senha, o manifesto privado e todos os PDFs.
    Fora disso, o build mantém o pacote cifrado que já está publicado."""
    if not config.SENHA_MESTRE or not pathlib.Path("mestre.py").exists():
        return False
    import mestre
    return all((pathlib.Path("mestre_docs") / arq).exists()
               for cat in mestre.CATEGORIAS for _, _, arq in cat["docs"])

def build_mestre():
    """Lê os PDFs de mestre_docs/, monta um pacote JSON e o CIFRA com AES-GCM
    (chave derivada da SENHA_MESTRE por PBKDF2). Grava só o cifrado em mestredata.js.
    Sem a senha, nada do conteúdo (nem os títulos) é legível no site."""
    import mestre
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

# ---------- Classes cifradas ----------
# Cada classe tem um par de chaves ECDH P-256. A chave PÚBLICA fica no site e
# basta para cifrar: por isso a lore pode ser atualizada sem as senhas.
# A chave PRIVADA também fica no site, mas cifrada com AES-GCM por uma chave
# derivada da senha da classe (PBKDF2). Sem a senha, o conteúdo é ruído.

def b64(b): return base64.b64encode(b).decode("ascii")
def unb64(s): return base64.b64decode(s)

def ler_pacote_classe(arq):
    if not arq.exists(): return None
    txt = arq.read_text(encoding="utf-8").strip()
    return json.loads(txt[len("window.SATUS_CLASSE="):].rstrip(";"))

def abrir_chave(pkg, senha):
    """Devolve a chave privada da classe, ou None se a senha não abre o pacote."""
    k = pkg["chave"]
    chave = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), unb64(k["salt"]), k["iter"], dklen=32)
    try:
        der = AESGCM(chave).decrypt(unb64(k["iv"]), unb64(k["ct"]), None)
    except Exception:
        return None
    return serialization.load_der_private_key(der, password=None)

def nova_chave(senha):
    priv = ec.generate_private_key(ec.SECP256R1())
    der = priv.private_bytes(serialization.Encoding.DER, serialization.PrivateFormat.PKCS8,
                             serialization.NoEncryption())
    salt, iv = os.urandom(16), os.urandom(12)
    chave = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, CLASSE_ITER, dklen=32)
    pub = priv.public_key().public_bytes(serialization.Encoding.X962,
                                         serialization.PublicFormat.UncompressedPoint)
    return {"pub": b64(pub), "chave": {"salt": b64(salt), "iter": CLASSE_ITER,
            "iv": b64(iv), "ct": b64(AESGCM(chave).encrypt(iv, der, None))}}

def cifrar_conteudo(slug, chaves, html):
    """Cifra o HTML com a chave pública da classe (ECDH efêmero + HKDF + AES-GCM)."""
    pub = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), unb64(chaves["pub"]))
    eph = ec.generate_private_key(ec.SECP256R1())
    segredo = eph.exchange(ec.ECDH(), pub)
    hsalt, iv = os.urandom(16), os.urandom(12)
    chave = HKDF(algorithm=hashes.SHA256(), length=32, salt=hsalt,
                 info=("trindade-classe-v1:" + slug).encode()).derive(segredo)
    eph_pub = eph.public_key().public_bytes(serialization.Encoding.X962,
                                            serialization.PublicFormat.UncompressedPoint)
    return {"eph": b64(eph_pub), "hsalt": b64(hsalt), "iv": b64(iv),
            "ct": b64(AESGCM(chave).encrypt(iv, html.encode("utf-8"), None))}

def chaves_das_classes(pacotes):
    """Usa as senhas, se houver, para conferir ou criar as chaves. Sem senha,
    reaproveita as chaves públicas já publicadas."""
    chaves = {}
    for slug in content.CLASSES:
        senha, atual = config.SENHAS.get(slug, ""), pacotes.get(slug)
        if senha:
            if atual and abrir_chave(atual, senha):
                chaves[slug] = {"pub": atual["pub"], "chave": atual["chave"]}
            else:
                chaves[slug] = nova_chave(senha)
                print("  chave nova:", slug, "(primeira vez ou senha trocada)")
        elif atual:
            chaves[slug] = {"pub": atual["pub"], "chave": atual["chave"]}
        else:
            raise SystemExit("Defina SENHA_%s: a classe ainda não tem chave publicada." % slug.upper())
    return chaves

def gravar_classe(slug, chaves, html, atual):
    arq = OUT / ("static/js/classe-%s.js" % slug)
    resumo = hashlib.sha256((chaves["pub"] + html).encode("utf-8")).hexdigest()
    if atual and atual.get("resumo") == resumo and atual.get("pub") == chaves["pub"]:
        pkg = atual          # nada mudou: mantém a mesma cifra, sem diferença no Git
    else:
        pkg = {"v": 1, "slug": slug, "pub": chaves["pub"], "chave": chaves["chave"],
               "resumo": resumo, "conteudo": cifrar_conteudo(slug, chaves, html)}
        print("  cifrado: conteúdo da classe", slug)
    arq.write_text("window.SATUS_CLASSE=" + json.dumps(pkg) + ";", encoding="utf-8")

def main():
    # Pacotes já publicados: ficam como estão se faltarem as senhas ou os PDFs privados.
    mestre_arq = OUT / "static/js/mestredata.js"
    mestre_atual = mestre_arq.read_bytes() if mestre_arq.exists() else None
    pacotes = {slug: ler_pacote_classe(OUT / ("static/js/classe-%s.js" % slug)) for slug in content.CLASSES}
    chaves = chaves_das_classes(pacotes)
    tem_mestre = mestre_disponivel()
    if not tem_mestre and mestre_atual is None:
        raise SystemExit("Defina SENHA_MESTRE e coloque mestre.py e mestre_docs/ na raiz do projeto.")

    if OUT.exists(): shutil.rmtree(OUT)
    (OUT / "static").mkdir(parents=True)
    shutil.copytree("static", OUT / "static", dirs_exist_ok=True)
    if pathlib.Path("img").exists():
        shutil.copytree("img", OUT / "img", dirs_exist_ok=True)

    # pacote cifrado da aba do Mestre
    if tem_mestre:
        build_mestre()
    else:
        mestre_arq.write_bytes(mestre_atual)
        print("  mantido: mestredata.js (senha do Mestre ou arquivos privados ausentes)")

    print("Gerando site estático em ./docs")
    render("index.html", "index.html", boasvindas=codex.BOASVINDAS)
    render("mundo.html", "mundo.html",
           geo=json.dumps({"regioes": world.REGIOES, "oceanos": world.OCEANOS, "locais": world.LOCAIS}, ensure_ascii=False))
    render("mestre.html", "mestre.html", active="mestre")
    render("codex.html", "codex.html", codex=codex.CODEX, active="codex")
    render("cacadores.html", "cacadores.html", roster=codex.ROSTER, legenda=codex.STAR_LEGEND, active="cacadores")
    render("regras.html", "regras.html", regras=regras.REGRAS, active="regras")
    for slug, c in content.CLASSES.items():
        render("classe_static.html", slug + ".html", c=c, active=slug)
        html = env.get_template("classe_conteudo.html").render(
            c=c, lore=lore.LORE.get(slug, []), classificado=codex.ALEM.get(slug, ""))
        gravar_classe(slug, chaves[slug], html, pacotes[slug])
    print("Pronto. Abra docs/index.html no navegador.")

if __name__ == "__main__":
    main()
