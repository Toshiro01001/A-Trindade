# -*- coding: utf-8 -*-
"""
Configuração do Arquivo da Trindade.
O MESTRE edita as senhas aqui. Cada jogador que escolher uma classe recebe a senha dela.
Pode também sobrescrever por variáveis de ambiente (SENHA_CONHECIMENTO, etc.).
"""
import os

SECRET_KEY = os.environ.get("TRINDADE_SECRET", "troque-esta-chave-secreta-do-mestre")

# Senhas de acesso por classe (troque à vontade)
SENHAS = {
    "conhecimento":  os.environ.get("SENHA_CONHECIMENTO",  "codex-espiral"),
    "exploracao":    os.environ.get("SENHA_EXPLORACAO",    "glacies-lied"),
    "administracao": os.environ.get("SENHA_ADMINISTRACAO", "conselho-supremo"),
}

# Patente mínima (estrelas) para recursos mais sensíveis
PATENTE_CONSELHO = 4

# Senha da ABA DO MESTRE (material reservado, cifrado de verdade).
# Ao contrário das senhas de classe, esta NÃO é publicada em hash: ela é a chave
# de criptografia AES-GCM dos documentos. Sem ela, o conteúdo é ruído no arquivo.
# Só é usada no momento do build (na sua máquina). Nada dela vai para o site.
SENHA_MESTRE = os.environ.get("SENHA_MESTRE", "Toshiro01001@2003")
