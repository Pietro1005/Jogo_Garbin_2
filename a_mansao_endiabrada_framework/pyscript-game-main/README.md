# 🎮 Framework PyScript Game Jam V2

Framework didático para criação de **jogos narrativos, aventuras, suspense, romance, RPG textual e visual novels em Python**, executados diretamente no navegador com **PyScript**.

A proposta é permitir que o jogo seja desenvolvido principalmente em **Python**, enquanto o HTML fornece a interface gráfica, a responsividade e os recursos multimídia.

---

## ✨ Recursos disponíveis

O framework já possui suporte para:

- cenas e caminhos narrativos;
- até 4 opções por cena;
- imagens diferentes em cada cena;
- vídeos;
- trilha sonora;
- troca de música durante o jogo;
- vida;
- inventário;
- pontuação;
- decisões condicionadas a itens;
- múltiplos finais;
- final secreto ou alternativo;
- botão para reiniciar a aventura;
- tela inicial com título, autor e capa;
- interface responsiva para telas horizontais e verticais;
- execução diretamente no navegador;
- publicação em hospedagem estática.

A versão V2 **não utiliza `input()` nem terminal**. As escolhas do jogador são feitas por botões.

---

# 🚀 Começando rapidamente

## 1. Estrutura do projeto

```text
framework_pyscript_gamejam_v2/
│
├── index.html
├── main.py
├── README.md
├── INICIAR_JOGO.bat
│
└── assets/
    ├── imagens/
    ├── audios/
    └── videos/
```

### Função dos arquivos

| Arquivo | Função |
|---|---|
| `index.html` | Interface, layout, responsividade e recursos de mídia |
| `main.py` | História, regras, cenas, inventário, vida, pontos e finais |
| `assets/imagens/` | Imagens e capas |
| `assets/audios/` | Trilhas sonoras e efeitos |
| `assets/videos/` | Vídeos utilizados nas cenas |
| `INICIAR_JOGO.bat` | Inicia um servidor local no Windows |

Na maior parte do projeto, o aluno trabalhará somente no:

```text
main.py
```

---

# ▶️ Como executar

## Windows

Dê dois cliques em:

```text
INICIAR_JOGO.bat
```

O navegador deverá abrir em:

```text
http://localhost:8000
```

---

## Terminal

Abra o terminal dentro da pasta do projeto e execute:

```bash
python -m http.server 8000
```

Depois acesse:

```text
http://localhost:8000
```

> Não é recomendado abrir `index.html` diretamente por `file://`. Use um servidor HTTP local.

Para encerrar o servidor:

```text
CTRL + C
```

---

# 🧩 Como o framework funciona

O jogo é dividido em três partes principais no arquivo `main.py`:

```text
CONFIG
  ↓
STATE
  ↓
SCENES
  ↓
executar_acao()
```

## `CONFIG`

Define as informações gerais do jogo.

Exemplo:

```python
CONFIG = {
    "titulo": "ALVORECER DOS DEUSES",
    "subtitulo": "Uma aventura mitológica interativa",
    "autor": "Nome do autor",
    "icone": "⚔️",

    "capa": None,

    "trilha_inicial":
        "assets/audios/trilha.mp3",

    "volume_inicial": 0.5,

    "vida_inicial": 3,
    "pontos_iniciais": 0,

    "cena_inicial": "inicio",
}
```

### Capa opcional

```python
"capa": "assets/imagens/capa.jpg",
```

Sem capa:

```python
"capa": None,
```

---

# 🎬 Criando cenas

As cenas ficam dentro do dicionário:

```python
SCENES = {
    ...
}
```

Uma cena básica:

```python
"inicio": {

    "title": "O começo",

    "image":
        "assets/imagens/inicio.jpg",

    "text": (
        "Você acorda em uma sala desconhecida.\n\n"
        "Há duas portas diante de você."
    ),

    "options": [
        ("Abrir a porta esquerda", "corredor"),
        ("Abrir a porta direita", "laboratorio"),
    ],
},
```

Cada opção possui:

```python
("Texto mostrado no botão", "acao")
```

Exemplo:

```python
("Entrar na floresta", "floresta")
```

Se `"floresta"` também for o nome de uma cena, o framework abre essa cena automaticamente.

---

# 🖼️ Imagens

Coloque as imagens em:

```text
assets/imagens/
```

E informe o arquivo dentro da cena:

```python
"image":
    "assets/imagens/floresta.jpg",
```

Formatos comuns:

```text
.jpg
.jpeg
.png
.webp
```

---

# 🎥 Vídeos

Coloque os vídeos em:

```text
assets/videos/
```

Use:

```python
"video":
    "assets/videos/introducao.mp4",

"video_autoplay": False,
```

Quando uma cena possui vídeo, ele substitui a imagem daquela cena.

Exemplo:

```python
"gravacao": {

    "title": "Arquivo encontrado",

    "video":
        "assets/videos/mensagem.mp4",

    "video_autoplay": False,

    "text":
        "Uma gravação antiga começa a ser exibida.",

    "options": [
        ("Continuar", "corredor"),
    ],
},
```

Para maior compatibilidade, prefira:

```text
.mp4
.webm
```

---

# 🎵 Áudio e trilha sonora

Coloque os arquivos em:

```text
assets/audios/
```

## Trilha inicial

Defina em `CONFIG`:

```python
"trilha_inicial":
    "assets/audios/trilha.mp3",
```

A música começa após o jogador clicar em:

```text
▶ INICIAR JOGO
```

Esse comportamento evita os bloqueios de reprodução automática dos navegadores.

---

## Trocar a música em uma cena

Adicione:

```python
"audio":
    "assets/audios/batalha.mp3",
```

Exemplo:

```python
"batalha": {

    "title": "A batalha",

    "image":
        "assets/imagens/batalha.jpg",

    "audio":
        "assets/audios/batalha.mp3",

    "text":
        "Uma criatura surge diante de você.",

    "options": [
        ("Lutar", "lutar"),
        ("Fugir", "fugir"),
    ],
},
```

Se a cena não possuir `audio`, a música atual continua tocando.

---

## Parar a música

Use:

```python
"stop_audio": True,
```

---

# ❤️ Sistema de vida

A quantidade inicial é definida em:

```python
"vida_inicial": 3,
```

Para retirar uma vida:

```python
perder_vida()
```

Para retirar mais de uma:

```python
perder_vida(2)
```

Quando a vida chega a zero, por padrão o jogo envia o jogador para:

```text
fim_ruim
```

---

# 🎒 Inventário

## Adicionar item

```python
adicionar_item("chave")
```

Também é possível dar pontos:

```python
adicionar_item(
    "chave",
    pontos=10
)
```

---

## Verificar se o jogador possui um item

```python
if possui_item("chave"):
    ...
```

Exemplo:

```python
if possui_item("chave"):

    mostrar_cena("sala_secreta")

else:

    mostrar_cena("porta_trancada")
```

---

## Remover um item

```python
remover_item("chave")
```

---

# ⭐ Pontuação

Adicionar pontos:

```python
ganhar_pontos(10)
```

A pontuação aparece automaticamente na interface.

Ela pode ser usada para:

- premiar exploração;
- criar rankings;
- liberar finais;
- identificar caminhos secretos;
- diferenciar desempenhos.

---

# ⚙️ Ações especiais

Uma escolha simples pode apontar diretamente para outra cena:

```python
("Seguir", "floresta")
```

Quando a escolha precisa executar alguma regra, registre a ação dentro de:

```python
def executar_acao(acao):
```

Exemplo:

```python
elif acao == "abrir_porta":

    if possui_item("chave"):

        ganhar_pontos(10)

        mostrar_cena(
            "sala_secreta"
        )

    else:

        morreu = perder_vida()

        if not morreu:

            mostrar_cena(
                "porta_falha"
            )
```

A opção na cena seria:

```python
("Tentar abrir a porta", "abrir_porta")
```

---

# 🧠 Consequências devem ser cenas

Evite fazer:

```text
clicou
↓
perde vida
↓
imediatamente outra cena
```

O jogador pode não conseguir perceber o que aconteceu.

Prefira criar uma cena de consequência:

```python
"porta_falha": {

    "title": "A porta reage",

    "image":
        "assets/imagens/porta.jpg",

    "text": (
        "Você tenta forçar a porta.\n\n"
        "Uma descarga atravessa sua mão.\n\n"
        "Você perdeu uma vida."
    ),

    "options": [
        ("Voltar", "corredor"),
    ],
},
```

Assim, a decisão produz uma consequência narrativa clara.

---

# 🏁 Múltiplos finais

Um jogo pode possuir vários finais:

```text
fim_bom
fim_ruim
fim_neutro
fim_alternativo
fim_secreto
```

Exemplo:

```python
"fim_bom": {

    "title": "FINAL BOM",

    "image":
        "assets/imagens/final_bom.jpg",

    "text":
        "Você conseguiu escapar!",

    "options": [],
},
```

Uma cena sem opções representa naturalmente um final.

---

# 🔐 Final dependente do inventário

Exemplo:

```python
elif acao == "decidir_final":

    itens_necessarios = {
        "chave",
        "lanterna",
        "fragmento",
    }

    itens_jogador = set(
        state["inventario"]
    )

    if itens_necessarios.issubset(
        itens_jogador
    ):

        mostrar_cena("fim_bom")

    else:

        mostrar_cena(
            "fim_alternativo"
        )
```

Isso aumenta a rejogabilidade: diferentes decisões podem gerar finais diferentes.

---

# 🔀 Até quatro opções por cena

O framework suporta até quatro botões:

```python
"options": [
    ("Opção A", "acao_a"),
    ("Opção B", "acao_b"),
    ("Opção C", "acao_c"),
    ("Opção D", "acao_d"),
],
```

Botões não utilizados são escondidos automaticamente.

---

# 📱 Responsividade

O `index.html` já possui comportamento diferente conforme a orientação da tela.

## Horizontal

```text
┌─────────────────────────────────────┐
│          TÍTULO / AUTOR             │
├──────────────────┬──────────────────┤
│                  │                  │
│  IMAGEM / VÍDEO  │  TEXTO / STATUS │
│                  │     / OPÇÕES     │
│      ÁUDIO       │                  │
│                  │                  │
└──────────────────┴──────────────────┘
```

## Vertical

```text
┌──────────────────────┐
│    TÍTULO / AUTOR    │
├──────────────────────┤
│    IMAGEM / VÍDEO    │
│        ÁUDIO         │
├──────────────────────┤
│     TEXTO DA CENA    │
│                     │
│ VIDA / INV. / PONTOS │
│                     │
│      OPÇÕES          │
└──────────────────────┘
```

A página evita rolagem global. Quando necessário, o texto da cena possui rolagem interna.

---

# 🔄 Reiniciar o jogo

O botão:

```text
↻ Reiniciar aventura
```

restaura:

- vida;
- inventário;
- pontuação;
- cena inicial;
- trilha inicial.

---

# 🧪 Testando alterações

Depois de editar o `main.py`, normalmente basta atualizar o navegador:

```text
CTRL + R
```

Se o navegador estiver mantendo uma versão antiga dos arquivos, utilize:

```text
CTRL + F5
```

ou:

```text
CTRL + SHIFT + R
```

---

# 🌐 Publicação

Como esta versão não utiliza `worker`, `input()` nem terminal, ela pode ser publicada como um site estático.

Uma estrutura típica de repositório é:

```text
/
├── index.html
├── main.py
├── README.md
└── assets/
```

## GitHub Pages

No GitHub:

1. envie todos os arquivos mantendo a estrutura de pastas;
2. abra **Settings**;
3. acesse **Pages**;
4. escolha a publicação a partir de uma branch;
5. selecione a branch principal e a pasta raiz;
6. salve;
7. aguarde a geração do endereço público.

O arquivo principal deve se chamar:

```text
index.html
```

---

# ⚠️ Atenção aos nomes dos arquivos

Os caminhos precisam ser exatamente iguais.

Se o código possui:

```python
"image":
    "assets/imagens/Floresta.jpg",
```

mas o arquivo se chama:

```text
floresta.jpg
```

o jogo pode funcionar no Windows e falhar quando for publicado.

Por isso, recomenda-se utilizar:

- letras minúsculas;
- sem espaços;
- sem acentos.

Exemplo:

```text
assets/imagens/sala_secreta.jpg
assets/audios/trilha_batalha.mp3
assets/videos/introducao.mp4
```

---

# 📋 Requisitos sugeridos para o projeto

Como referência para a atividade:

- mínimo de **6 cenas**;
- mínimo de **2 finais diferentes**;
- pelo menos **3 itens possíveis** no inventário;
- pelo menos uma decisão dependente de um item;
- decisões que realmente alterem a história;
- sistema de vida, risco ou recurso equivalente;
- interface responsiva;
- tratamento coerente das consequências;
- autoria e identidade próprias.

---

# 🚀 Desafios opcionais

Para ampliar o projeto:

- final secreto;
- múltiplas trilhas;
- efeitos sonoros;
- eventos aleatórios;
- enigmas;
- batalhas;
- personagens;
- sistema de moedas;
- pontuação máxima;
- rotas alternativas;
- escolhas dependentes de vida;
- escolhas dependentes de pontos;
- itens consumíveis;
- inventário mais complexo;
- vídeos narrativos;
- sistema de conquistas.

---

# 🛠️ Referência rápida

| Objetivo | Código |
|---|---|
| Mostrar cena | `mostrar_cena("nome")` |
| Adicionar item | `adicionar_item("item")` |
| Testar item | `possui_item("item")` |
| Remover item | `remover_item("item")` |
| Perder vida | `perder_vida()` |
| Ganhar pontos | `ganhar_pontos(10)` |
| Trocar música | `trocar_audio("assets/audios/musica.mp3")` |
| Parar música | `parar_audio()` |
| Mostrar imagem | definido pelo campo `"image"` da cena |
| Mostrar vídeo | definido pelo campo `"video"` da cena |

---

# 📌 Modelo mínimo de nova cena

```python
"nome_da_cena": {

    "title": "Título da cena",

    "image":
        "assets/imagens/imagem.jpg",

    "text": (
        "Texto narrativo da cena."
    ),

    "options": [
        ("Primeira escolha", "outra_cena"),
        ("Segunda escolha", "alguma_acao"),
    ],
},
```

---

# 🧱 Filosofia do framework

A ideia central é separar:

```text
CONTEÚDO
SCENES

REGRAS
executar_acao()

ESTADO
state

INTERFACE
index.html
```

Isso permite criar histórias maiores sem transformar todo o jogo em uma sequência extensa de `if`, `elif` e `else`.

---

## 👨‍🏫 Projeto educacional

Framework desenvolvido como base para atividades de programação e criação de jogos narrativos em Python/PyScript.

**Prof. Felipe Garbin**
