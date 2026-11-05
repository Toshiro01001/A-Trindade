<h1 align="center">ECOS DAS RUÍNAS</h1>
<p align="center"><i>O Arquivo da Trindade. O mundo de SATUS na palma da mesa.</i></p>

<p align="center">
  <img alt="Offline" src="https://img.shields.io/badge/abre%20e%20funciona-offline-111">
  <img alt="Estático" src="https://img.shields.io/badge/sem%20servidor-100%25%20est%C3%A1tico-B41717">
  <img alt="Cifrado" src="https://img.shields.io/badge/aba%20do%20Mestre-AES--GCM-2E7D32">
  <img alt="RPG" src="https://img.shields.io/badge/HxH%205e-SATUS-C9A227">
</p>

---

## Um arquivo vivo para a sua campanha

Esqueça o calhamaço de PDFs soltos e a pasta bagunçada no Drive. **Ecos das Ruínas** é o portal da campanha SATUS reunido num só lugar: capa cinematográfica, mapa-múndi navegável e todo o material de mesa organizado por quem pode ver o quê. Você dá um duplo clique e o mundo abre. Sem instalar nada, sem internet, sem servidor.

## O que espera quem entra

🗺️ **O mapa de SATUS, ao vivo.** Oito regiões, três oceanos, línguas, impérios e países. Um mundo inteiro dentro das Glacies Lied, pronto para o jogador passear e se perder.

🔐 **Três portas, três classes.** Conhecimento, Exploração e Administração. Cada uma guarda mandato, regalias e lore próprios atrás de uma senha. O jogador entra na dele e encontra só o que a sua classe deveria saber. Os segredos das outras continuam segredos.

🕯️ **O cofre do Mestre.** A aba mais perigosa do site. Roteiros de sessão, fichas de ameaça, o bestiário do Breu e as mecânicas que sustentam o mundo. Tudo cifrado de verdade, com AES-GCM. Sem a senha do Mestre, nem os títulos aparecem: é ruído puro no arquivo. O jogador curioso que abrir o código-fonte não leva nada.

⚡ **Feito para a mesa.** Carrega rápido, roda no celular ou no notebook, funciona no meio do mato sem sinal. É o tipo de recurso que você abre na frente do grupo e ninguém precisa esperar.

## Como entrar

```
docs/index.html
```

Duplo clique. É isso. Funciona offline.

## Por trás da cortina

Quer mudar textos, senhas ou soltar um documento novo no cofre do Mestre? O site é gerado por um script em Python que lê os seus dados e remonta tudo, cifrando o material reservado no caminho.

```bash
pip install -r requirements.txt
python build.py
```

Um comando, e o arquivo inteiro renasce atualizado.

---

<p align="center"><b>SATUS não é um cenário. É um lugar onde a sua mesa vai morar.</b></p>
<p align="center"><i>Ecos das Ruínas · Arquivo da Trindade</i></p>

---

Desenvolvido por Rodrigo Terroso Junior. O Claude, da Anthropic, foi usado como ferramenta durante o desenvolvimento.
