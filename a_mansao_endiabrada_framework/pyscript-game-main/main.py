# ============================================================
# A MANSÃO ENDIABRADA
# Aplicação da história no Framework PyScript Game Jam V2
# ============================================================

import random
from pyscript import web, when, window

CONFIG = {
    "titulo": "A MANSÃO ENDIABRADA",
    "subtitulo": "Uma aventura de terror slasher interativa",
    "autor": "Pietro",
    "icone": "🔪",
    "capa": None,
    "trilha_inicial": "assets/audios/The Dawn of Aethelgard.mp3",
    "volume_inicial": 0.35,
    "vida_inicial": 5,
    "pontos_iniciais": 0,
    "cena_inicial": "inicio",
}

state = {
    "vida": CONFIG["vida_inicial"],
    "inventario": [],
    "pontos": CONFIG["pontos_iniciais"],
    "cena": CONFIG["cena_inicial"],
    "assassino_alertado": False,
    "gerador_ligado": False,
    "sobrevivente_salvo": False,
    "radio_ajuda": False,
    "fita_assistida": False,
}

def el(id_elemento):
    return web.page[id_elemento]

# ============================================================
# CENAS
# ============================================================

SCENES = {
    "inicio": {
        "title": "23:47 — A estrada",
        "image": "assets/imagens/inicio.png",
        "text": (
            "Uma tempestade cai sobre a estrada. Seu carro para "
            "repentinamente e o celular está sem sinal.\n\n"
            "No alto de uma colina existe uma enorme mansão. "
            "Uma única luz está acesa.\n\n"
            "Você entra procurando ajuda. A porta bate e trava atrás de você.\n\n"
            "Um relâmpago ilumina o segundo andar. Por um instante, "
            "você vê uma figura de máscara branca, marcas vermelhas, "
            "casaco vermelho gasto e um pesado machado de lenhador.\n\n"
            "Quando o próximo relâmpago acontece, a figura desaparece.\n\n"
            "Você precisa encontrar uma saída."
        ),
        "options": [("Entrar no hall", "hall")],
    },

    "hall": {
        "title": "Hall principal",
        "text": (
            "O enorme hall de entrada possui várias portas. "
            "Uma escadaria leva aos andares superiores.\n\n"
            "Explore a mansão e procure uma forma de escapar."
        ),
        "options": [
            ("Ir para a cozinha", "cozinha"),
            ("Ir para a biblioteca", "biblioteca"),
            ("Ir para o banheiro", "banheiro"),
            ("Ir para o escritório", "escritorio"),
        ],
    },

    "hall2": {
        "title": "Hall principal",
        "text": (
            "Você retorna ao hall. As sombras parecem mais próximas agora.\n\n"
            "A garagem está trancada, mas você possui a chave enferrujada."
        ),
        "options": [
            ("Cozinha", "cozinha"),
            ("Biblioteca", "biblioteca"),
            ("Banheiro", "banheiro"),
            ("Escritório", "escritorio"),
        ],
    },

    "hall3": {
        "title": "Hall principal",
        "text": "A mansão continua silenciosa. Para onde você vai?",
        "options": [
            ("Escadas", "escadas"),
            ("Garagem", "garagem"),
            ("Cozinha", "cozinha"),
            ("Biblioteca", "biblioteca"),
        ],
    },

    "cozinha": {
        "title": "Cozinha",
        "text": (
            "A cozinha está abandonada. Pratos quebrados cobrem o chão. "
            "A geladeira faz um barulho estranho e existe uma enorme faca "
            "sobre a bancada.\n\n"
            "Escolha o que examinar."
        ),
        "options": [
            ("Procurar nas gavetas", "cozinha_gavetas"),
            ("Abrir a geladeira", "cozinha_geladeira"),
            ("Procurar no armário", "cozinha_armario"),
            ("Sair da cozinha", "hall3"),
        ],
    },
    "cozinha_gavetas": {
        "title": "Gavetas",
        "text": "Entre talheres espalhados, você encontra uma faca de cozinha. A lâmina ainda parece utilizável.",
        "options": [("Pegar a faca", "pegar_faca"), ("Voltar", "cozinha")],
    },
    "cozinha_geladeira": {
        "title": "Geladeira",
        "text": "Não há comida. Atrás de algumas caixas existe um pequeno kit médico.",
        "options": [("Pegar o kit médico", "pegar_kit"), ("Voltar", "cozinha")],
    },
    "cozinha_armario": {
        "title": "Armário",
        "text": "O armário está emperrado. Dentro, sob uma camada de poeira, há uma lanterna antiga.",
        "options": [("Pegar a lanterna", "pegar_lanterna"), ("Voltar", "cozinha")],
    },

    "biblioteca": {
        "title": "Biblioteca",
        "text": (
            "Estantes enormes chegam até o teto. No centro há uma mesa "
            "com um diário antigo.\n\n"
            "O que você deseja examinar?"
        ),
        "options": [
            ("Ler o diário", "diario"),
            ("Procurar nas estantes", "estantes"),
            ("Abrir a gaveta", "gaveta_trancada"),
            ("Sair da biblioteca", "hall3"),
        ],
    },
    "diario": {
        "title": "O diário",
        "text": (
            "A última página diz:\n\n"
            "“Se alguém encontrar este diário, não confie no homem da máscara "
            "e do machado. Ele conhece todos os caminhos da casa.\n\n"
            "A única forma de escapar é encontrar a chave da garagem.”\n\n"
            "A página seguinte foi arrancada."
        ),
        "options": [("Guardar o diário", "pegar_diario"), ("Voltar", "biblioteca")],
    },
    "estantes": {
        "title": "A passagem secreta",
        "text": (
            "Um livro parece diferente. Ao puxá-lo, uma pequena passagem "
            "se abre na parede. Atrás dela há uma pequena chave coberta de ferrugem."
        ),
        "options": [("Pegar a chave", "pegar_chave_enferrujada"), ("Voltar", "biblioteca")],
    },
    "gaveta_trancada": {
        "title": "Gaveta trancada",
        "text": "Você tenta abrir a gaveta, mas ela está trancada. Talvez precise de uma ferramenta.",
        "options": [("Voltar", "biblioteca")],
    },

    "banheiro": {
        "title": "Banheiro",
        "text": (
            "O banheiro está completamente escuro. A torneira pinga lentamente. "
            "O espelho está quebrado e há manchas estranhas nas paredes.\n\n"
            "Você vê um armário, uma pia e uma pequena janela."
        ),
        "options": [
            ("Abrir o armário", "banheiro_armario"),
            ("Examinar o espelho", "espelho"),
            ("Procurar na pia", "pia"),
            ("Tentar abrir a janela", "jardim"),
        ],
    },
    "banheiro_armario": {
        "title": "Armário do banheiro",
        "text": "Dentro do armário há duas pilhas novas, perfeitas para alimentar uma lanterna.",
        "options": [("Pegar as pilhas", "pegar_pilhas"), ("Voltar", "banheiro")],
    },
    "espelho": {
        "title": "O espelho",
        "text": (
            "Por um instante, você vê uma pessoa atrás de você.\n\n"
            "Você se vira rapidamente. Não há ninguém.\n\n"
            "Quando olha novamente para o espelho, a figura desapareceu.\n\n"
            "Você tem a sensação de que o assassino sabe que está aqui."
        ),
        "options": [("Continuar", "alertar_assassino"), ("Voltar", "banheiro")],
    },
    "pia": {
        "title": "A pia",
        "text": "Entre objetos enferrujados, seus dedos encontram uma pequena chave.",
        "options": [("Pegar a chave", "pegar_chave_pequena"), ("Voltar", "banheiro")],
    },

    "escritorio": {
        "title": "Escritório",
        "text": (
            "O escritório parece ter pertencido ao antigo dono da mansão. "
            "Uma escrivaninha, um computador e fotografias da família Blackwood "
            "ocupam o cômodo."
        ),
        "options": [
            ("Examinar a escrivaninha", "cartao"),
            ("Ler documentos", "documentos"),
            ("Ligar o computador", "computador"),
            ("Examinar fotografias", "fotografias"),
        ],
    },
    "cartao": {
        "title": "Cartão de segurança",
        "text": "Escondido na escrivaninha há um cartão de segurança que parece dar acesso a uma área restrita.",
        "options": [("Pegar o cartão", "pegar_cartao"), ("Voltar", "escritorio")],
    },
    "documentos": {
        "title": "Documentos",
        "text": (
            "Os documentos mencionam diversos desaparecimentos. Todos aconteceram "
            "dentro da mansão.\n\nA última anotação diz: “Não deixe o assassino chegar ao porão.”"
        ),
        "options": [("Continuar investigando", "escritorio")],
    },
    "computador": {
        "title": "Computador",
        "text": "O computador pede uma senha. Você não sabe qual é.",
        "options": [("Voltar", "escritorio")],
    },
    "fotografias": {
        "title": "Fotografias",
        "text": (
            "Em uma fotografia aparece um homem usando a mesma máscara branca "
            "marcada de vermelho.\n\nNo verso está escrito:\n\n"
            "“Michael Blackwood — 1987”"
        ),
        "options": [("Guardar a informação", "escritorio")],
    },

    "escadas": {
        "title": "Escadas",
        "text": "A enorme escadaria divide a mansão. O andar superior está completamente escuro.",
        "options": [
            ("Subir para o sótão", "sotao"),
            ("Descer para o porão", "porao"),
            ("Voltar ao hall", "hall3"),
        ],
    },

    "sotao": {
        "title": "Sótão",
        "text": (
            "O sótão está cheio de caixas. Uma pequena janela deixa entrar a luz da lua.\n\n"
            "Você escuta alguém respirando atrás das caixas."
        ),
        "options": [
            ("Conversar com a pessoa", "sarah"),
            ("Procurar nas caixas", "fita"),
            ("Examinar a janela", "janela_sotao"),
            ("Descer", "hall3"),
        ],
    },
    "sarah": {
        "title": "Sarah",
        "text": (
            "A pessoa está assustada.\n\n"
            "“Meu nome é Sarah. Estou presa aqui há dois dias. "
            "O assassino conhece todos os cômodos. Existe uma saída secreta "
            "na sala de segurança.”\n\n"
            "Ela entrega uma chave pesada."
        ),
        "options": [("Aceitar a chave mestra", "pegar_chave_mestra"), ("Voltar", "sotao")],
    },
    "fita": {
        "title": "Fita VHS",
        "text": "Entre as caixas existe uma fita VHS empoeirada, gravada dentro da mansão.",
        "options": [("Pegar a fita", "pegar_fita"), ("Voltar", "sotao")],
    },
    "janela_sotao": {
        "title": "Janela do sótão",
        "text": "A janela dá para o telhado. A queda é muito alta. Não é uma rota segura de fuga.",
        "options": [("Voltar", "sotao")],
    },

    "porao": {
        "title": "Porão",
        "text": (
            "A temperatura cai rapidamente. A luz do teto pisca. "
            "Você encontra um gerador antigo e uma porta de metal com um painel eletrônico."
        ),
        "options": [
            ("Examinar o gerador", "gerador"),
            ("Examinar a porta de metal", "porta_seguranca"),
            ("Procurar objetos", "radio"),
            ("Subir para o hall", "hall3"),
        ],
    },
    "gerador": {
        "title": "Gerador",
        "text": "O gerador está quebrado. Está faltando um fusível.",
        "options": [("Tentar instalar o fusível", "ligar_gerador"), ("Voltar", "porao")],
    },
    "porta_seguranca": {
        "title": "Porta de metal",
        "text": "O painel pede um cartão de segurança.",
        "options": [("Usar o cartão", "abrir_seguranca"), ("Voltar", "porao")],
    },
    "radio": {
        "title": "Caixa de madeira",
        "text": "Dentro da caixa há um rádio antigo. Os botões ainda funcionam.",
        "options": [("Pegar o rádio", "pegar_radio"), ("Voltar", "porao")],
    },

    "garagem": {
        "title": "Garagem",
        "text": (
            "Uma caminhonete antiga está estacionada. Existem caixas, ferramentas "
            "e um armário. Se conseguir fazer o veículo funcionar, talvez consiga escapar."
        ),
        "options": [
            ("Examinar a caminhonete", "caminhonete"),
            ("Procurar ferramentas", "machado"),
            ("Procurar gasolina", "gasolina"),
            ("Abrir o armário", "fusivel"),
        ],
    },
    "caminhonete": {
        "title": "Caminhonete",
        "text": "A caminhonete precisa de gasolina e de energia elétrica para funcionar.",
        "options": [("Tentar ligar", "ligar_carro"), ("Voltar", "garagem")],
    },
    "machado": {
        "title": "Ferramentas",
        "text": "Entre as ferramentas existe um machado de lenhador pesado. O cabo gasto mostra que foi usado muitas vezes.",
        "options": [("Pegar o machado", "pegar_machado"), ("Voltar", "garagem")],
    },
    "gasolina": {
        "title": "Galão de gasolina",
        "text": "Atrás das caixas há um galão de gasolina. Talvez seja exatamente o que a caminhonete precisa.",
        "options": [("Pegar gasolina", "pegar_gasolina"), ("Voltar", "garagem")],
    },
    "fusivel": {
        "title": "Fusível",
        "text": "No armário existe um fusível antigo, ainda inteiro. Ele pode restaurar a energia do gerador.",
        "options": [("Pegar o fusível", "pegar_fusivel"), ("Voltar", "garagem")],
    },

    "jardim": {
        "title": "Jardim",
        "text": (
            "Você sai pela janela do banheiro. O jardim está abandonado. "
            "Ao longe existe um portão. Uma sombra se move entre as árvores.\n\n"
            "Você precisa decidir rapidamente."
        ),
        "options": [
            ("Correr até o portão", "portao_jardim"),
            ("Ir até a cabana", "cabana"),
            ("Esconder-se", "esconder_jardim"),
            ("Voltar para a casa", "banheiro"),
        ],
    },
    "portao_jardim": {
        "title": "Portão da propriedade",
        "text": "O portão está trancado. Você precisa de uma chave.",
        "options": [("Tentar abrir", "abrir_portao"), ("Voltar", "jardim")],
    },
    "cabana": {
        "title": "Cabana",
        "text": "Dentro da caixa de ferramentas há um pé de cabra. Pode ser útil para abrir algo emperrado.",
        "options": [("Pegar o pé de cabra", "pegar_pe_cabra"), ("Voltar", "jardim")],
    },
    "esconder_jardim": {
        "title": "Escondido entre as árvores",
        "text": "Você se esconde atrás de uma árvore. A sombra passa lentamente e não percebe você.",
        "options": [("Voltar para a casa", "hall3")],
    },

    "seguranca": {
        "title": "Sala de segurança",
        "text": (
            "Monitores mostram diferentes partes da mansão. Uma das câmeras "
            "mostra o assassino caminhando pelo corredor. Ele parece estar procurando você."
        ),
        "options": [
            ("Ver câmeras", "cameras"),
            ("Usar o rádio", "usar_radio"),
            ("Procurar saída secreta", "saida_secreta"),
            ("Assistir à fita VHS", "assistir_fita"),
        ],
    },
    "cameras": {
        "title": "As câmeras",
        "text": (
            "Câmera 1: Hall. Câmera 2: Cozinha. Câmera 3: Biblioteca. "
            "Câmera 4: Jardim. Câmera 5: Segundo andar.\n\n"
            "De repente, a câmera do hall mostra o assassino encarando diretamente a lente."
        ),
        "options": [("Continuar", "alertar_assassino"), ("Voltar", "seguranca")],
    },
    "usar_radio": {
        "title": "Rádio",
        "text": "Você tenta encontrar uma frequência.\n\nCHIADO...\n\nUma voz responde: “Ele já sabe onde você está.”",
        "options": [
            ("Pedir ajuda", "pedir_ajuda"),
            ("Perguntar quem é o assassino", "perguntar_assassino"),
            ("Voltar", "seguranca"),
        ],
    },
    "saida_secreta": {
        "title": "Porta secreta",
        "text": "Atrás dos monitores existe uma porta escondida. Ela precisa de uma chave especial.",
        "options": [("Usar a chave mestra", "abrir_tunel"), ("Voltar", "seguranca")],
    },
    "assistir_fita": {
        "title": "A gravação",
        "text": "A gravação mostra Michael Blackwood falando sobre a mansão. No final aparece a mensagem: “Se você está vendo isso... ele ainda está aqui.”",
        "options": [("Guardar a pista", "marcar_fita"), ("Voltar", "seguranca")],
    },

    "tunel": {
        "title": "Túnel secreto",
        "text": "O túnel é antigo. Depois de alguns metros, você encontra duas saídas: uma para a floresta e outra de volta para a mansão.",
        "options": [("Ir para a floresta", "fim_tunel"), ("Voltar para a segurança", "seguranca")],
    },

    "evento_assassino": {
        "title": "VOCÊ NÃO ESTÁ SOZINHO",
        "text": (
            "Um barulho vem do outro lado da sala.\n\n"
            "Uma sombra passa pela porta. A máscara branca marcada de vermelho "
            "surge por um instante, seguida pelo brilho do machado.\n\n"
            "O assassino está perto."
        ),
        "options": [("Fugir!", "perseguicao")],
    },

    "perseguicao": {
        "title": "Perseguição",
        "text": "Você corre pelos corredores. Os passos do assassino ficam cada vez mais próximos. Você chega a uma bifurcação.",
        "options": [
            ("Ir pela esquerda", "perseg_esquerda"),
            ("Ir pela direita", "perseg_direita"),
            ("Esconder-se", "perseg_esconder"),
        ],
    },
    "perseg_esquerda": {
        "title": "Corredor esquerdo",
        "text": "Você entra em um quarto. O assassino passa direto... ou talvez não.",
        "options": [("Continuar correndo", "resultado_esquerda")],
    },
    "perseg_direita": {
        "title": "Corredor direito",
        "text": "Você corre pela cozinha e pelas escadas. O assassino continua atrás de você.",
        "options": [("Tentar escapar", "resultado_direita")],
    },
    "perseg_esconder": {
        "title": "Esconderijo",
        "text": "Você entra rapidamente em um armário e tenta não fazer barulho.",
        "options": [("Esperar", "resultado_esconder")],
    },
    "combate": {
        "title": "Confronto",
        "text": (
            "O assassino bloqueia a saída. A máscara branca esconde o rosto "
            "e o pesado machado está em suas mãos.\n\n"
            "Você precisa agir."
        ),
        "options": [
            ("Usar a faca", "combate_faca"),
            ("Usar o machado", "combate_machado"),
            ("Tentar fugir", "perseguicao"),
            ("Se esconder", "esconder_combate"),
        ],
    },
    "esconder_combate": {
        "title": "Armário",
        "text": "Você entra em um armário. Depois de alguns segundos, os passos se afastam.",
        "options": [("Sair", "hall3")],
    },

    # ========================================================
    # FINAIS
    # ========================================================
    "fim_fuga": {
        "title": "FINAL 1 — FUGA PELO JARDIM",
        "text": (
            "Com a chave enferrujada, você abre o portão e corre pela estrada.\n\n"
            "Um motorista chama a polícia. Quando olha para trás, a mansão está escura.\n\n"
            "Você sobreviveu."
        ),
        "options": [],
    },
    "fim_carro": {
        "title": "FINAL 2 — FUGA DE CARRO",
        "text": (
            "Você coloca a gasolina e restaura a energia da caminhonete.\n\n"
            "O motor finalmente funciona. Você acelera para fora da propriedade.\n\n"
            "No retrovisor, o assassino observa você desaparecer na tempestade."
        ),
        "options": [],
    },
    "fim_tunel": {
        "title": "FINAL 4 — O TÚNEL SECRETO",
        "text": (
            "Você atravessa o túnel e finalmente chega à floresta.\n\n"
            "A polícia encontra apenas uma máscara na propriedade. "
            "Nenhum sinal do assassino."
        ),
        "options": [],
    },
    "fim_policia": {
        "title": "FINAL 5 — O PEDIDO DE SOCORRO",
        "text": (
            "Você mantém o rádio funcionando. Uma equipe de resgate chega à mansão.\n\n"
            "Os policiais entram, mas o assassino desapareceu. "
            "Apenas uma máscara é encontrada no corredor."
        ),
        "options": [],
    },
    "fim_secreto": {
        "title": "FINAL SECRETO — A VERDADE DE BLACKWOOD",
        "text": (
            "Você reuniu as principais pistas: diário, fita, cartão de segurança e chave mestra.\n\n"
            "Michael Blackwood era o antigo dono da mansão. Após o desaparecimento "
            "de sua família, ele passou a perseguir quem entrava na propriedade.\n\n"
            "Os túneis secretos permitiam que ele observasse todos os cômodos. "
            "Você escapa com as provas e a investigação é reaberta.\n\n"
            "A verdade sobre a família Blackwood finalmente vem à tona."
        ),
        "options": [],
    },
    "fim_ruim": {
        "title": "FINAL RUIM — A ÚLTIMA NOITE",
        "text": (
            "Suas forças chegam ao fim.\n\n"
            "Os passos do assassino se aproximam e a mansão volta ao silêncio.\n\n"
            "A casa continua esperando sua próxima vítima."
        ),
        "options": [],
        "stop_audio": True,
    },
    "fim_preso": {
        "title": "FINAL RUIM — PRESO PARA SEMPRE",
        "text": (
            "Você procura uma saída durante horas. Cada corredor parece igual.\n\n"
            "O amanhecer chega, mas você continua dentro da casa.\n\n"
            "A mansão parece não ter fim."
        ),
        "options": [],
    },
}

# ============================================================
# INTERFACE
# ============================================================

def configurar_identidade():
    window.document.title = CONFIG["titulo"]
    el("titulo-jogo").innerText = CONFIG["titulo"]
    el("autor-jogo").innerText = f"Autor: {CONFIG['autor']}"
    el("titulo-abertura").innerText = CONFIG["titulo"]
    el("subtitulo-abertura").innerText = CONFIG["subtitulo"]
    el("autor-abertura").innerText = f"Criado por {CONFIG['autor']}"
    el("icone-abertura").innerText = CONFIG["icone"]
    capa = CONFIG.get("capa")
    if capa:
        el("capa-jogo").src = capa
        el("capa-jogo").style.display = "block"
        el("icone-abertura").style.display = "none"
    else:
        el("capa-jogo").style.display = "none"
        el("icone-abertura").style.display = "block"
    audio = el("audio-fundo")
    audio.dataset.inicial = CONFIG.get("trilha_inicial") or ""
    audio.dataset.volume = str(CONFIG.get("volume_inicial", 0.5))

def atualizar_status():
    vida = state["vida"]
    el("vida").innerText = " ".join(["❤️"] * vida) if vida > 0 else "💀"
    if vida <= 0:
        el("vida").classList.add("danger")
    else:
        el("vida").classList.remove("danger")
    el("inventario").innerText = ", ".join(state["inventario"]) if state["inventario"] else "Vazio"
    el("pontos").innerText = str(state["pontos"])

def mostrar_imagem(caminho):
    window.frameworkVideo.stop()
    imagem = el("imagem-cena")
    if not caminho:
        imagem.style.display = "none"
        return
    imagem.src = caminho
    imagem.style.display = "block"

def mostrar_video(caminho, autoplay=False):
    if caminho:
        window.frameworkVideo.play(caminho, autoplay)

def trocar_audio(caminho):
    if caminho:
        window.frameworkAudio.play(caminho, CONFIG.get("volume_inicial", 0.5), True)

def parar_audio():
    window.frameworkAudio.stop()

def atualizar_botoes(opcoes):
    for i in range(1, 5):
        botao = el(f"opcao{i}")
        if i <= len(opcoes):
            botao.innerText = opcoes[i-1][0]
            botao.disabled = False
            botao.style.display = "block"
        else:
            botao.innerText = ""
            botao.disabled = True
            botao.style.display = "none"

def mostrar_cena(nome, permitir_evento=True):
    if nome not in SCENES:
        return
    state["cena"] = nome
    cena = SCENES[nome]
    el("titulo-cena").innerText = cena.get("title", nome)
    el("texto-cena").innerText = cena.get("text", "")
    if cena.get("video"):
        mostrar_video(cena["video"], cena.get("video_autoplay", False))
    else:
        mostrar_imagem(cena.get("image"))
    if "audio" in cena:
        trocar_audio(cena["audio"]) if cena["audio"] else parar_audio()
    if cena.get("stop_audio"):
        parar_audio()
    atualizar_botoes(cena.get("options", []))
    atualizar_status()

    # Encontro aleatório do assassino, mas nunca interrompe finais,
    # cenas de perseguição/combate ou cenas de coleta.
    bloqueadas = {
        "inicio", "evento_assassino", "perseguicao", "combate",
        "fim_fuga", "fim_carro", "fim_tunel", "fim_policia",
        "fim_secreto", "fim_ruim", "fim_preso"
    }
    if permitir_evento and nome not in bloqueadas and random.randint(1, 10) <= 2:
        state["cena"] = "evento_assassino"
        cena = SCENES["evento_assassino"]
        el("titulo-cena").innerText = cena["title"]
        el("texto-cena").innerText = cena["text"]
        atualizar_botoes(cena["options"])
        state["assassino_alertado"] = True

def adicionar_item(item, pontos=0):
    if item not in state["inventario"]:
        state["inventario"].append(item)
        state["pontos"] += pontos
    atualizar_status()

def possui_item(item):
    return item in state["inventario"]

def perder_vida(quantidade=1):
    state["vida"] -= quantidade
    atualizar_status()
    if state["vida"] <= 0:
        state["vida"] = 0
        mostrar_cena("fim_ruim", permitir_evento=False)
        return True
    return False

def ganhar_pontos(q):
    state["pontos"] += q
    atualizar_status()

# ============================================================
# AÇÕES
# ============================================================

def executar_acao(acao):
    if acao in SCENES:
        mostrar_cena(acao)
        return

    if acao == "pegar_faca":
        adicionar_item("faca", 10); mostrar_cena("cozinha")
    elif acao == "pegar_kit":
        adicionar_item("kit medico", 10); mostrar_cena("cozinha")
    elif acao == "pegar_lanterna":
        adicionar_item("lanterna", 10); mostrar_cena("cozinha")
    elif acao == "pegar_diario":
        adicionar_item("diario", 15); mostrar_cena("biblioteca")
    elif acao == "pegar_chave_enferrujada":
        adicionar_item("chave enferrujada", 15); mostrar_cena("biblioteca")
    elif acao == "pegar_pilhas":
        adicionar_item("pilhas", 5); mostrar_cena("banheiro")
    elif acao == "pegar_chave_pequena":
        adicionar_item("chave pequena", 5); mostrar_cena("banheiro")
    elif acao == "alertar_assassino":
        state["assassino_alertado"] = True
        ganhar_pontos(5); mostrar_cena("banheiro")
    elif acao == "pegar_cartao":
        adicionar_item("cartao seguranca", 20); mostrar_cena("escritorio")
    elif acao == "pegar_chave_mestra":
        state["sobrevivente_salvo"] = True
        adicionar_item("chave mestra", 30); mostrar_cena("sotao")
    elif acao == "pegar_fita":
        adicionar_item("fita", 20); mostrar_cena("sotao")
    elif acao == "ligar_gerador":
        if possui_item("fusivel"):
            state["gerador_ligado"] = True
            ganhar_pontos(20)
            SCENES["gerador"]["text"] = "Você instala o fusível. BRUUUUM! O gerador volta a funcionar e a energia da mansão retorna."
        else:
            SCENES["gerador"]["text"] = "O gerador está quebrado. Está faltando um fusível."
        mostrar_cena("porao")
    elif acao == "abrir_seguranca":
        if possui_item("cartao seguranca"):
            mostrar_cena("seguranca")
        else:
            SCENES["porta_seguranca"]["text"] = "O painel pede um cartão de segurança. Você ainda não possui um."
            mostrar_cena("porta_seguranca")
    elif acao == "pegar_radio":
        adicionar_item("radio", 10); mostrar_cena("porao")
    elif acao == "pegar_machado":
        adicionar_item("machado", 15); mostrar_cena("garagem")
    elif acao == "pegar_gasolina":
        adicionar_item("gasolina", 15); mostrar_cena("garagem")
    elif acao == "pegar_fusivel":
        adicionar_item("fusivel", 15); mostrar_cena("garagem")
    elif acao == "pegar_pe_cabra":
        adicionar_item("pe de cabra", 10); mostrar_cena("jardim")
    elif acao == "abrir_portao":
        if possui_item("chave enferrujada"):
            mostrar_cena("fim_fuga", permitir_evento=False)
        else:
            mostrar_cena("portao_jardim")
    elif acao == "ligar_carro":
        if possui_item("gasolina") and possui_item("fusivel"):
            mostrar_cena("fim_carro", permitir_evento=False)
        else:
            SCENES["caminhonete"]["text"] = "A caminhonete está sem combustível e/ou energia. Você precisa encontrar gasolina e um fusível."
            mostrar_cena("caminhonete")
    elif acao == "cameras":
        state["assassino_alertado"] = True; mostrar_cena("cameras")
    elif acao == "usar_radio":
        if possui_item("radio"): mostrar_cena("usar_radio")
        else:
            SCENES["usar_radio"]["text"] = "Você não possui um rádio. Talvez exista um no porão."
            mostrar_cena("seguranca")
    elif acao == "pedir_ajuda":
        state["radio_ajuda"] = True
        mostrar_cena("fim_policia", permitir_evento=False)
    elif acao == "perguntar_assassino":
        SCENES["usar_radio"]["text"] = "A voz responde: “Michael Blackwood.” O rádio desliga. Você se lembra da fotografia do escritório."
        state["assassino_alertado"] = True
        mostrar_cena("usar_radio")
    elif acao == "marcar_fita":
        state["fita_assistida"] = True; ganhar_pontos(20); mostrar_cena("seguranca")
    elif acao == "abrir_tunel":
        if possui_item("chave mestra"):
            mostrar_cena("tunel", permitir_evento=False)
        else:
            SCENES["saida_secreta"]["text"] = "A porta secreta está trancada. Você precisa de uma chave especial."
            mostrar_cena("saida_secreta")
    elif acao == "resultado_esquerda":
        r = random.randint(1,3)
        if r == 1: mostrar_cena("hall3")
        elif r == 2: mostrar_cena("combate", permitir_evento=False)
        else: mostrar_cena("jardim")
    elif acao == "resultado_direita":
        r = random.randint(1,3)
        if r == 1: mostrar_cena("cozinha")
        elif r == 2:
            if perder_vida(): return
            mostrar_cena("hall3")
        else: mostrar_cena("sotao")
    elif acao == "resultado_esconder":
        if random.randint(1,2) == 1:
            mostrar_cena("hall3")
        else:
            if perder_vida(): return
            mostrar_cena("hall3")
    elif acao == "combate_faca":
        if possui_item("faca"):
            state["inventario"].remove("faca")
            atualizar_status()
            mostrar_cena("perseguicao", permitir_evento=False)
        else:
            mostrar_cena("perseguicao", permitir_evento=False)
    elif acao == "combate_machado":
        if possui_item("machado"):
            state["assassino_alertado"] = False
            mostrar_cena("hall3")
        else:
            mostrar_cena("perseguicao", permitir_evento=False)
    else:
        # ações simples usadas pelo fluxo
        if acao == "marcar_fita":
            state["fita_assistida"] = True
        mostrar_cena("hall3")

def escolher_opcao(numero):
    cena = SCENES[state["cena"]]
    opcoes = cena.get("options", [])
    if numero <= len(opcoes):
        executar_acao(opcoes[numero-1][1])

@when("click", "#opcao1")
def clicar_opcao1(event): escolher_opcao(1)

@when("click", "#opcao2")
def clicar_opcao2(event): escolher_opcao(2)

@when("click", "#opcao3")
def clicar_opcao3(event): escolher_opcao(3)

@when("click", "#opcao4")
def clicar_opcao4(event): escolher_opcao(4)

@when("click", "#reiniciar")
def reiniciar(event):
    state.update({
        "vida": CONFIG["vida_inicial"],
        "inventario": [],
        "pontos": CONFIG["pontos_iniciais"],
        "cena": CONFIG["cena_inicial"],
        "assassino_alertado": False,
        "gerador_ligado": False,
        "sobrevivente_salvo": False,
        "radio_ajuda": False,
        "fita_assistida": False,
    })
    if CONFIG.get("trilha_inicial"):
        trocar_audio(CONFIG["trilha_inicial"])
    mostrar_cena(CONFIG["cena_inicial"], permitir_evento=False)

configurar_identidade()
mostrar_cena(CONFIG["cena_inicial"], permitir_evento=False)
el("botao-iniciar").disabled = False
el("botao-iniciar").innerText = "▶ INICIAR JOGO"
