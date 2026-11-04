# Ecos das Ruínas

Portal estático da campanha SATUS (Hunter x Hunter 5e), com mapa, páginas por classe e aba do Mestre cifrada.

## Como este projeto funciona

- O site é gerado por Python: `pip install -r requirements.txt` e `python build.py`. A saída vai para `docs/`, que é a versão publicada.
- Não edite `docs/` à mão: altere `content.py`, `world.py`, `lore.py`, `codex.py`, `regras.py`, `mestre.py`, `templates/` ou `static/` e gere de novo.
- Rode o build com as senhas nas variáveis de ambiente `SENHA_CONHECIMENTO`, `SENHA_EXPLORACAO`, `SENHA_ADMINISTRACAO` e `SENHA_MESTRE`. Não escreva senhas em arquivos.
- `mestre.py` e `mestre_docs/` são privados e ficam fora do repositório. Sem eles ou sem as senhas, o build mantém os arquivos `authdata.js` e `mestredata.js` já publicados, então edições de lore funcionam normalmente.
- Ao atualizar a lore de um tema, inclua tudo por completo, sem resumir nem alterar o conteúdo. Remova só os apartes de narrador ou de IA.
- Separe a lore pelas classes: povos em Conhecimento, áreas e criaturas por explorar em Exploração, conflitos e relações de poder em Administração. Só deixe de separar se ele pedir.

## Regras de trabalho

- Responda em português do Brasil, sem travessões, e chame o dono de Rodrigo Jr.
- Altere só o que foi pedido. Publicar ou fazer merge no `main` depende de pedido dele.
- Toda função criada ou alterada precisa funcionar também no celular. Teste a versão mobile, não só a de computador.
- Ao criar ou alterar o site, explique como ele funciona.
- Ao terminar uma alteração, entregue a mensagem de commit em dois blocos rotulados: "Título" (até 50 caracteres) e "Descrição" (estendida, com exatamente o que foi feito).
- Entregue arquivos soltos, nunca em `.zip`.
- O repositório é público: não coloque senhas, chaves secretas nem dados pessoais em arquivos versionados.
