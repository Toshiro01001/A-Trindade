# -*- coding: utf-8 -*-
"""Conteúdo do mundo: mandatos, regalias e recursos privilegiados de cada classe."""

def C():  # marcador de informação classificada (o template renderiza a tarja)
    return "\u0007"  # substituído por <span class="redacted"> no template

CLASSES = {
"conhecimento": {
  "slug":"conhecimento","nome":"Conhecimento","tema":"conh","seal":"conh",
  "papel":"O coração intelectual e científico da Trindade",
  "mandato":"Reúne os Caçadores e Viajantes mais dedicados à busca do saber. Quem escolhe esta classe tem por missão expandir os limites do conhecimento humano, desvendando mistérios do passado, descobrindo novas tecnologias e movendo a ciência de SATUS adiante.",
  "regalias":[
    ("Acesso à Educação de Elite",[
      "Prioridade de entrada e redução de até 50% nas taxas das melhores universidades, laboratórios e institutos de SATUS.",
      "Programas de intercâmbio entre continentes, principalmente Eurona, Azora e Antalor, com acesso a centros de pesquisa renomados."]),
    ("Bônus em Descobertas Científicas",[
      "Bônus de até 45% em recompensas ou créditos por descobertas científicas significativas.",
      "Inclui achados arqueológicos, inovações tecnológicas e avanços em biologia, química e física que beneficiem a humanidade ou a Trindade."]),
    ("Acesso Exclusivo a Registros Classificados",[
      "Por votação no Conselho Supremo das 3 Classes, é possível requisitar registros acadêmicos e científicos confiscados ou censurados por governos e agências de SATUS.",
      "Esses documentos incluem estudos sobre o Continente Negro, teorias proibidas sobre a origem do planeta e registros ligados às ruínas de civilizações perdidas."]),
    ("Parcerias Estratégicas com Instituições",[
      "Instituições científicas e acadêmicas, muitas sob patrocínio da Trindade, oferecem financiamento, equipamentos e suporte logístico para expedições em busca de novas informações ou tecnologias."]),
    ("Proteção e Preservação do Conhecimento",[
      "Papel crucial em garantir que descobertas importantes sejam preservadas e não caiam em mãos que as usem para fins destrutivos.",
      "Algumas descobertas passam por votação no Conselho Supremo antes de serem publicadas ou compartilhadas."]),
  ],
  "recursos":[
    {"kind":"docs","titulo":"Registros Classificados","nota":"Requisitados ao Conselho Supremo. Alguns trechos permanecem selados.","itens":[
      {"t":"Estudo sobre o Continente Negro","b":"Dossiê sobre a terra de onde a humanidade veio, hoje território proibido além do muro.","classif":False},
      {"t":"Teoria proibida da origem do planeta","b":"Manuscrito confiscado em Antalor. Contradiz a versão oficial da fundação de SATUS.","classif":True},
      {"t":"Registros das civilizações perdidas","b":"Fragmentos recuperados das ruínas. Escrita ainda não decifrada por completo.","classif":False},
    ]},
    {"kind":"table","titulo":"Educação de Elite · Convênios Ativos","nota":"Redução de até 50% nas taxas.","cols":["Instituição","Continente","Benefício"],"rows":[
      ["Universidade de Eurona","Eurona","−50% · prioridade"],
      ["Instituto Azoriano de Ciências","Azora","−45% · intercâmbio"],
      ["Laboratórios de Antalor","Antalor","−40% · pesquisa de campo"],
    ]},
    {"kind":"meter","titulo":"Bônus por Descobertas","nota":"Crédito adicional sobre achados significativos.","valor":45,"rotulo":"até 45% em recompensas científicas"},
  ],
},
"exploracao": {
  "slug":"exploracao","nome":"Exploração","tema":"expl","seal":"expl",
  "papel":"Os desbravadores mais corajosos de SATUS",
  "mandato":"Movidos pela vontade de revelar os segredos do planeta, seus membros desafiam limites e mapeiam territórios inexplorados, trazendo à luz riquezas culturais, naturais e históricas. São a vanguarda das expedições da Trindade, frequentemente enviados a áreas de alta periculosidade, como o Domínio Obscuro, os desertos gélidos de Antalor ou as profundezas dos oceanos.",
  "regalias":[
    ("Isenção Tributária em Relíquias e Itens Raros",[
      "Isenção de impostos ao vender ou adquirir relíquias, artefatos e recursos raros obtidos em missões.",
      "Maior lucratividade e incentivo ao comércio de descobertas únicas."]),
    ("Bônus ao Final de Expedições",[
      "Bônus de até 45% em recompensas por concluir expedições patrocinadas pela Trindade ou por governos aliados.",
      "Vale para missões de mapeamento, coleta de amostras ou recuperação de artefatos de alto valor."]),
    ("Acesso Exclusivo a Equipamentos de Alta Tecnologia",[
      "A Trindade fornece equipamentos de ponta: veículos para terrenos inóspitos, trajes protetores para ambientes hostis e ferramentas avançadas de escavação e análise."]),
    ("Prioridade em Missões Patrocinadas",[
      "Prioridade nas expedições financiadas por governos ou entidades privadas, sendo os primeiros a explorar locais recém-descobertos."]),
    ("Permissão para Reivindicar Descobertas",[
      "Direito de reivindicar partes de territórios inexplorados ou descobertas significativas, registrando-as sob seu nome: cavernas, ruínas ou fontes naturais de recursos."]),
    ("Redução em Custos de Transporte e Logística",[
      "Descontos significativos, ou até isenção, em transporte marítimo, aéreo e terrestre para expedições autorizadas pela Trindade."]),
    ("Acesso a Mapas e Dados de Navegação Exclusivos",[
      "Consulta a mapas detalhados e registros de expedições anteriores, muitas vezes confidenciais, com áreas inexploradas, perigos conhecidos e locais de interesse."]),
    ("Rede de Suporte Local",[
      "Acesso a uma rede de apoio em continentes aliados durante as missões: guias experientes, tradutores e recursos médicos."]),
  ],
  "recursos":[
    {"kind":"table","titulo":"Mapas Confidenciais · Frentes de Expedição","nota":"Classificação de perigo por zona.","cols":["Zona","Perigo","Status"],"rows":[
      ["Cume das Glacies Lied","Extremo","Mapeamento parcial"],
      ["Desertos gélidos de Antalor","Alto","Expedição ativa"],
      ["Profundezas do Oceano Umbral","Extremo","Selado"],
      ["O Domínio Obscuro","Desconhecido","Acesso negado"],
    ]},
    {"kind":"table","titulo":"Mercado de Relíquias · Isento de Impostos","nota":"Transações registradas sob patente de Exploração.","cols":["Artefato","Origem","Valor"],"rows":[
      ["Fragmento de Seiva Inversa","Ruína submersa","— · isento"],
      ["Bússola aureliana","Antalor","— · isento"],
      ["Selo de civilização perdida","Continente Negro","— · isento"],
    ]},
    {"kind":"list","titulo":"Rede de Suporte Local","nota":"Apoio em continentes aliados.","itens":[
      "Guias experientes de terreno hostil","Tradutores de dialetos regionais","Postos médicos de campo da Trindade"]},
  ],
},
"administracao": {
  "slug":"administracao","nome":"Administração","tema":"adm","seal":"adm",
  "papel":"O coração estratégico e político de SATUS",
  "mandato":"Seus membros moldam os rumos do mundo como líderes, coordenadores e gestores de recursos, garantindo que cada engrenagem da Trindade funcione. Equilibram interesses conflitantes, promovem estabilidade e traçam estratégias para o avanço global. São, mais que burocratas, os arquitetos de um mundo coeso.",
  "regalias":[
    ("Acesso à Governança Superior",[
      "Caçadores de 4 estrelas ou mais têm assento garantido no Conselho Supremo das 3 Classes, decidindo os rumos estratégicos de SATUS.",
      "Influência direta sobre políticas interclasses e globais, consultados em reformas legais e decisões estruturais."]),
    ("Controle sobre Recursos e Financiamento",[
      "Supervisão da alocação de recursos financeiros, humanos e materiais em pesquisa, expedições e infraestrutura.",
      "Acesso a fundos de contingência secretos, usados em situações críticas ou iniciativas discretas."]),
    ("Bônus em Poder Político e Econômico",[
      "A partir de 4 estrelas, bônus de influência política: negociação com governos e corporações sem intermediários.",
      "Autoridade para criar ou reestruturar sistemas de tributos e redirecionar riquezas em crises.",
      "Poder de barganha superior em qualquer negociação."]),
    ("Acesso Exclusivo a Informações Estratégicas",[
      "Controle de relatórios confidenciais: dados econômicos, ameaças políticas e análises sociais.",
      "Pode requisitar informações das outras classes, como mapas secretos da Exploração ou descobertas da classe de Conhecimento.",
      "Decide o que é divulgado ou mantido em sigilo, regulando o fluxo de informação."]),
    ("Controle sobre Forças Militares e Segurança",[
      "Pode mobilizar forças militares, unidades de segurança ou agentes especiais em caso de necessidade.",
      "Coordena vigilância e monitoramento de regiões instáveis, neutralizando ameaças internas ou externas.",
      "Acesso direto às unidades de elite da Trindade, para proteção de locais estratégicos ou missões de alto risco."]),
    ("Parcerias e Alianças Estratégicas",[
      "Negocia tratados com nações, corporações ou facções poderosas, dentro e fora de SATUS.",
      "Cria redes de aliança que promovem desenvolvimento econômico, militar e tecnológico global.",
      "Os únicos com poder para estabelecer tratados intercontinentais em nome da Trindade."]),
    ("Proteção Legal e Imunidade",[
      "Imunidade jurídica nas atividades exercidas dentro da Trindade.",
      "Não podem ser processados por decisões tomadas no cumprimento de suas funções, salvo traição comprovada.",
      "Protocolo de proteção prioritária, com segurança constante em tempos de crise."]),
    ("Responsabilidade pela Ordem e Equilíbrio",[
      "Garante que as outras classes operem dentro de seus limites, evitando disputas internas ou abusos de poder.",
      "Equilibra as necessidades da ciência, da exploração e da governança para um progresso harmonioso.",
      "Atua como mediadora em conflitos entre classes ou regiões, restabelecendo a ordem."]),
  ],
  "recursos":[
    {"kind":"council","titulo":"Sala do Conselho Supremo","nota":"Requer patente 4★ ou superior.","min_stars":4,"itens":[
      {"t":"Reforma tributária de Askar","b":"Votação em aberto · 2 a favor, 1 contra"},
      {"t":"Publicação do registro sobre o Continente Negro","b":"Votação em aberto · selado até deliberação"},
      {"t":"Mobilização de elite em zona instável","b":"Aprovado · execução discreta"},
    ]},
    {"kind":"docs","titulo":"Fundos de Contingência","nota":"Valores mantidos em sigilo.","itens":[
      {"t":"Reserva estratégica da Trindade","b":"Contingência contra o Domínio Obscuro · uso restrito a crise declarada","classif":False},
      {"t":"Iniciativas discretas","b":"Destino: expedições ao Domínio Obscuro","classif":False},
    ]},
    {"kind":"list","titulo":"Relatórios Requisitáveis das Outras Classes","nota":"Fluxo de informação controlado pela Administração.","itens":[
      "Mapas secretos da Classe de Exploração","Descobertas científicas da Classe de Conhecimento","Análises econômicas, políticas e sociais"]},
  ],
},
}
