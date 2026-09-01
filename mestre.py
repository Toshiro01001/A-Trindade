# -*- coding: utf-8 -*-
"""
Manifesto da ABA DO MESTRE (material reservado, cifrado).

Aqui o MESTRE lista os documentos que quer trancar atrás da senha do Mestre.
Cada item aponta para um arquivo dentro de 'mestre_docs/'. O build.py lê estes
arquivos, cifra tudo (AES-GCM, chave derivada da SENHA_MESTRE por PBKDF2) e grava
apenas o resultado cifrado no site. Sem a senha, nada aqui é legível no navegador.

Para acrescentar um documento novo: jogue o PDF em 'mestre_docs/' e adicione uma
linha na categoria certa. Rode 'python build.py' de novo.
"""

# Cada doc: (titulo, subtitulo, arquivo em mestre_docs/)
CATEGORIAS = [
    {
        "nome": "Roteiros de Sessão",
        "nota": "Condução de mesa. Falas, atos e reviravoltas.",
        "docs": [
            ("Sessão 13 · O Duelo de Tir'Vahal",
             "Roteiro de mesa · o início da Segunda Grande Dissensão · Arena Aurexis, 09/12/430 D.T.",
             "SATUS_Sessao13_Roteiro.pdf"),
            ("Sessão 13 · Dossiê de Planejamento do Mestre",
             "As três frentes simultâneas · a fuga-cilada, o duelo e o atentado · as Naturezas-Mortas assassinas e a traição do Loki",
             "SATUS_Sessao13_Dossie.pdf"),
            ("Cena de Mesa · O Camarote D3LUX3",
             "O reencontro e a confissão da Rosa do Oeste · falas da Nina para ler em voz alta",
             "SATUS_Cena_Camarote_D3LUX3.pdf"),
            ("Prep de Cena · A Audiência com o Loki",
             "Void × Giovanni Silver · o jogo do EVANC · o que ele oferece e o preço de cada camada",
             "SATUS_Audiencia_Loki.pdf"),
        ],
    },
    {
        "nome": "Panorama Político · A Trindade por Dentro",
        "nota": "Quem move a Trindade, quem cava a cova dela, e onde a linha borra.",
        "docs": [
            ("As Facções da Trindade",
             "Internas, Ordem e Inimigas · Conclave, Círculo-Ponte, Vigilância Silenciosa, Vigília do Primeiro Véu, Confraria do Vazio e Comunhão Carmesim",
             "SATUS_Faccoes_da_Trindade.pdf"),
        ],
    },
    {
        "nome": "Fichas · Confraria do Vazio",
        "nota": "Os generais do atentado. As lâminas que Leichmann move em Tir'Vahal.",
        "docs": [
            ("Nina · A Pintora do Vazio",
             "Ficha tipo Calamidade · no corpo de Hanna Aurel · Especialista · Body Hopping e a Pintura no Ar",
             "SATUS_Nina_Ficha.pdf"),
            ("Novissime 2.0 · Aleister Hawkins",
             "Ficha tipo Calamidade · o Rei do Não-Lugar · Especialista · The Yellow Kingdom e o comando das Naturezas-Mortas",
             "SATUS_Novissime_Ficha.pdf"),
            ("Stefan Koss · O Ogro",
             "Reforço · irmão de Novak Koss · o bruto das geleiras de Antalor · Hatsu Big Bang Impact · Recompensa J$ 400.000.001",
             "SATUS_Stefan_Ficha.pdf"),
            ("Jacob Burial · O Senhor do Mórpheum",
             "Perto de Calamidade · Manipulação · o carcereiro de sonhos e pesadelos lúcidos da Confraria",
             "SATUS_Jacob_Ficha.pdf"),
            ("A Raposa de Mudang · yata'i Müdång",
             "Perto de Calamidade · Conjuração e Emissão · neto do Dragão de Mudang · o fogo negro que só ele apaga",
             "SATUS_Raposa_Ficha.pdf"),
            ("Ren Matsuda · O Filho do Akuma",
             "Nível 12 · Transmutação · relâmpago · rápido como o trovão · o pagamento do Akira, cuja morte deve vir da mão do próprio pai",
             "SATUS_Ren_Ficha.pdf"),
            ("Altair Orsini · O Envenenador da Família Orsini",
             "Nível 10 · Conjuração · gás e ácido · a lâmina da máfia de Eurona · luta de atrito que sufoca o campo inteiro",
             "SATUS_Altair_Ficha.pdf"),
        ],
    },
    {
        "nome": "Fichas de Ameaça · Calamidades, Semideusa e Deus Maior",
        "nota": "As lâminas nomeadas e o teto do mundo. Régua de poder.",
        "docs": [
            ("Nina Vorynne Ostrad · A Rosa do Oeste",
             "Ficha de Semideusa · corpo divino original · filha de Maal e Arhyssa · acima do Tipo Calamidade · a verdade por trás de todas as máscaras",
             "SATUS_NinaDivina_Ficha.pdf"),
            ("Villis Saint Holmes · O Auge",
             "Ficha tipo Calamidade · o Demônio da Ventania no auge absoluto · 6ª Calamidade · o mais forte do mundo · Chaos Wind",
             "SATUS_Villis_Ficha_Auge.pdf"),
            ("Villis Saint Holmes · O Crepúsculo",
             "Ficha tipo Calamidade · versão envelhecida e enfraquecida · o que resta da tempestade · a versão que morre na fuga de Pentarion",
             "SATUS_Villis_Ficha_Enfraquecido.pdf"),
            ("Vahangir · O Terrível-Mor",
             "Ficha tipo Calamidade · a fera na fumaça · feita para matar Annika",
             "SATUS_Vahangir_Ficha.pdf"),
            ("Anátema · O Devorador do Vento",
             "Ficha tipo Calamidade · a muralha anti-Nen · base Tarrasque",
             "SATUS_Anatema_Ficha.pdf"),
            ("Nihil · O Vazio que Ceifa",
             "Ficha tipo Calamidade · a negação da Lâmina · forjada para matar Alma",
             "SATUS_Nihil_Ficha.pdf"),
            ("Maal · O Senhor do Breu",
             "Ficha de Deus Maior · a forma física no Continente Negro · acima de qualquer Calamidade",
             "SATUS_Maal_Ficha.pdf"),
        ],
    },
    {
        "nome": "Fichas · Os Sem Era",
        "nota": "O degrau de poder acima das Calamidades. A era é força, não alinhamento.",
        "docs": [
            ("Robert Walton · O Ilimitado",
             "Tipo Calamidade · Especialista · o caçador mais forte da atualidade · portador do Seis Olhos e do Mugen · do lado do bem, treinado pelo próprio Villis",
             "SATUS_Robert_Ficha.pdf"),
        ],
    },
    {
        "nome": "Bestiário do Breu · Naturezas-Mortas",
        "nota": "A horda. Mecânica de enxame por tier.",
        "docs": [
            ("Naturezas-Mortas · Tier 1",
             "O Algoz e o Arauto · a elite: comandante e artilharia",
             "SATUS_NM_Tier1.pdf"),
            ("Naturezas-Mortas · Tier 2",
             "O Carniceiro e o Amálgama · os brutamontes: aríete e devorador",
             "SATUS_NM_Tier2.pdf"),
            ("Naturezas-Mortas · Tier 3",
             "O Espreitador e o Estrige · os rápidos: furtivo e voador",
             "SATUS_NM_Tier3.pdf"),
            ("Naturezas-Mortas · Tier 4",
             "A Escória e o Cuspidor · o enxame: corpo a corpo e à distância",
             "SATUS_NM_Tier4.pdf"),
        ],
    },
    {
        "nome": "Compêndio do Sistema · Mecânicas de Mesa",
        "nota": "As regras que sustentam o mundo. Referência de números para o Mestre.",
        "docs": [
            ("As Cores · O Poder que Nasce da Alma",
             "Observação, Armamento e Conquistador · os três graus, os efeitos nucleares e a Pintura no Ar da Nina",
             "SATUS_As_Cores.pdf"),
            ("O Sangue Abençoado · O Dom dos Aurelianos",
             "Cura que revive, hemorragia que drena o doador e o vício que escraviza · o dilema do Kael em números",
             "SATUS_Sangue_Aureliano.pdf"),
            ("O Grimório das Bênçãos · O Poder que Vem de Fora",
             "A segunda progressão paralela ao Nen · a trilha de Devoção e as dádivas dos deuses · Fagulha, Favor, Comunhão e a barganha de Gan",
             "SATUS_Grimorio_das_Bencaos.pdf"),
        ],
    },
]
