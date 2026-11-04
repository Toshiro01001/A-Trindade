# -*- coding: utf-8 -*-
"""
Configuração do Arquivo da Trindade.
As senhas vêm só de variáveis de ambiente (SENHA_CONHECIMENTO, SENHA_EXPLORACAO,
SENHA_ADMINISTRACAO e SENHA_MESTRE). Nunca escreva senhas neste arquivo: o repositório é público.
"""
import os

SECRET_KEY = os.environ.get("TRINDADE_SECRET", "troque-esta-chave-secreta-do-mestre")

# Senhas de acesso por classe (definidas nas variáveis de ambiente)
SENHAS = {
    "conhecimento":  os.environ.get("SENHA_CONHECIMENTO", ""),
    "exploracao":    os.environ.get("SENHA_EXPLORACAO", ""),
    "administracao": os.environ.get("SENHA_ADMINISTRACAO", ""),
}

# Patente mínima (estrelas) para recursos mais sensíveis
PATENTE_CONSELHO = 4

# Senha da ABA DO MESTRE (material reservado, cifrado de verdade).
# Ao contrário das senhas de classe, esta NÃO é publicada em hash: ela é a chave
# de criptografia AES-GCM dos documentos. Sem ela, o conteúdo é ruído no arquivo.
# Só é usada no momento do build (na sua máquina). Nada dela vai para o site.
SENHA_MESTRE = os.environ.get("SENHA_MESTRE", "")
