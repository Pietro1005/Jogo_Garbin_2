# ============================================================
# A MANSÃO ENDIABRADA - adaptação para FRAMEWORK PYSCRIPT GAME JAM V2
# ============================================================
#
# Base narrativa: "A mansão endiabrada".
# Estrutura adaptada ao framework:
# - cenas/nós;
# - estado do jogador;
# - inventário;
# - ações;
# - eventos especiais do assassino;
# - múltiplos finais.
#
# As imagens da prancha enviada foram recortadas e vinculadas aos nós abaixo.
# ============================================================

import random
from pyscript import web, when, window


CONFIG = {
    "titulo": "A MANSÃO ENDIABRADA",
    "subtitulo": "Jogo de terror slasher — você sobreviverá?",
    "autor": "Pietro",
    "icone": "🔪",
    "capa": "assets/imagens/hall.png",
    "trilha_inicial": "assets/audios/The Dawn of Aethelgard.mp3",
    "volume_inicial": 0.5,
    "vida_inicial": 5,
    "pontos_iniciais": 0,
    "cena_inicial": "inicio",
}


state = {
    "vida": CONFIG["vida_inicial"],
    "inventario": [],
    "pontos": CONFIG["pontos_iniciais"],
    "cena": CONFIG["cena_inicial"],
    "cena_anterior": CONFIG["cena_inicial"],

    # Flags narrativas
    "assassino_alertado": False,
    "gerador_ligado": False,
    "sobrevivente_salvo": False,
    "radio_ajuda": False,
    "fita_assistida": False,
}


# ============================================================
# CENAS / NÓS
# ============================================================
#
# Cada cena possui no máximo 4 opções porque o HTML do framework
# disponibiliza quatro botões.
#
# Nós de ação (acao_*) existem para transformar as ações da
# história original em escolhas visuais do framework.
# ============================================================

SCENES = {

    # --------------------------------------------------------
    # INÍCIO
    # --------------------------------------------------------
    "inicio": {
        "title": "23:47 — A mansão",
        "image": "assets/imagens/hall.png",
        "text": (
            "Uma tempestade cai sobre a estrada.\n\n"
            "Seu carro para repentinamente. O motor morreu e o celular "
            "não possui sinal.\n\n"
            "No alto de uma colina existe uma enorme mansão. Uma única "
            "luz está acesa em uma das janelas.\n\n"
            "Você decide procurar ajuda."
        ),
        "options": [
            ("Entrar na mansão", "entrada_mansao"),
        ],
    },

    "entrada_mansao": {
        "title": "CLAC!",
        "image": "assets/imagens/hall.png",
        "text": (
            "Assim que você entra, a porta se fecha atrás de você.\n\n"
            "Está trancada.\n\n"
            "Um trovão ilumina o corredor. Por uma fração de segundo, "
            "você vê uma figura no segundo andar: máscara branca com "
            "marcas vermelhas, casaco vermelho gasto e um grande "
            "machado de lenhador.\n\n"
            "Quando o próximo relâmpago acontece, ela desaparece.\n\n"
            "Agora começa sua luta para sobreviver."
        ),
        "options": [
            ("Explorar o hall", "hall"),
        ],
    },

    # --------------------------------------------------------
    # HALL
    # --------------------------------------------------------
    "hall": {
        "title": "Hall de entrada",
        "image": "assets/imagens/hall.png",
        "text": (
            "Você está no enorme hall de entrada.\n\n"
            "Uma escadaria leva aos outros andares e várias portas "
            "dão acesso aos cômodos da mansão.\n\n"
            "Talvez exista uma saída, um telefone ou alguém vivo aqui."
        ),
        "options": [
            ("Explorar a cozinha", "cozinha"),
            ("Explorar a biblioteca", "biblioteca"),
            ("Explorar o banheiro", "banheiro"),
            ("Mais áreas / inventário", "hall_2"),
        ],
    },

    "hall_2": {
        "title": "Hall de entrada — outras áreas",
        "image": "assets/imagens/hall.png",
        "text": (
            "Você está novamente no hall. Agora pode acessar as áreas "
            "mais perigosas da mansão ou cuidar dos seus recursos."
        ),
        "options": [
            ("Ir para o escritório", "escritorio"),
            ("Ir para as escadas", "escadas"),
            ("Ir para a garagem", "verificar_garagem"),
            ("Abrir inventário / usar item", "inventario"),
        ],
    },

    "inventario": {
        "title": "Inventário",
        "image": "assets/imagens/inventario.png",
        "text": (
            "Consulte os itens carregados e escolha uma ação."
        ),
        "options": [
            ("Usar kit médico", "usar_kit"),
            ("Usar lanterna", "usar_lanterna"),
            ("Voltar ao hall", "hall_2"),
        ],
    },

    "verificar_garagem": {
        "title": "Porta da garagem",
        "image": "assets/imagens/garagem.png",
        "text": (
            "A porta da garagem está trancada.\n\n"
            "Talvez a chave enferrujada encontrada na mansão consiga "
            "abri-la."
        ),
        "options": [
            ("Usar chave enferrujada", "abrir_garagem"),
            ("Voltar ao hall", "hall_2"),
        ],
    },

    "abrir_garagem": {
        "title": "Garagem",
        "image": "assets/imagens/garagem.png",
        "text": (
            "A chave funciona.\n\n"
            "Você abre a porta e entra em uma grande garagem. Uma "
            "caminhonete antiga está estacionada ali.\n\n"
            "Se conseguir fazê-la funcionar, talvez consiga escapar."
        ),
        "options": [
            ("Examinar caminhonete", "garagem"),
            ("Voltar ao hall", "hall_2"),
        ],
    },

    # --------------------------------------------------------
    # COZINHA
    # --------------------------------------------------------
    "cozinha": {
        "title": "Cozinha",
        "image": "assets/imagens/cozinha.png",
        "text": (
            "A cozinha está completamente abandonada. Pratos quebrados "
            "estão espalhados pelo chão e a geladeira faz um barulho "
            "estranho.\n\n"
            "Há gavetas, uma geladeira e um armário antigo."
        ),
        "options": [
            ("Procurar nas gavetas", "cozinha_faca"),
            ("Abrir a geladeira", "cozinha_kit"),
            ("Procurar no armário", "cozinha_lanterna"),
            ("Voltar ao hall", "hall_2"),
        ],
    },

    "cozinha_faca": {
        "title": "Faca",
        "image": "assets/imagens/cozinha.png",
        "text": (
            "Entre os talheres e a madeira úmida da gaveta, você "
            "encontra uma faca de cozinha. A lâmina ainda parece utilizável."
        ),
        "options": [
            ("Pegar a faca", "pegar_faca"),
            ("Deixar a faca", "cozinha"),
        ],
    },

    "pegar_faca": {
        "title": "Item obtido",
        "image": "assets/imagens/faca.png",
        "text": "Você guarda a faca. Pode ser útil para se defender.",
        "options": [
            ("Continuar explorando", "cozinha"),
        ],
    },

    "cozinha_kit": {
        "title": "Kit médico",
        "image": "assets/imagens/kit_medico.png",
        "text": (
            "Atrás de algumas caixas na geladeira existe um pequeno "
            "kit médico. É uma das poucas coisas daquela cozinha que "
            "ainda parece estar em condições de uso."
        ),
        "options": [
            ("Pegar o kit médico", "pegar_kit"),
            ("Deixar o kit", "cozinha"),
        ],
    },

    "pegar_kit": {
        "title": "Item obtido",
        "image": "assets/imagens/kit_medico.png",
        "text": "Você guarda o kit médico.",
        "options": [
            ("Continuar explorando", "cozinha"),
        ],
    },

    "cozinha_lanterna": {
        "title": "Lanterna",
        "image": "assets/imagens/lanterna.png",
        "text": (
            "No fundo do armário, sob uma camada de poeira, há uma "
            "lanterna antiga. Ela ainda consegue emitir luz."
        ),
        "options": [
            ("Pegar a lanterna", "pegar_lanterna"),
            ("Deixar a lanterna", "cozinha"),
        ],
    },

    "pegar_lanterna": {
        "title": "Item obtido",
        "image": "assets/imagens/lanterna.png",
        "text": "Você guarda a lanterna. Talvez ela seja útil no escuro.",
        "options": [
            ("Continuar explorando", "cozinha"),
        ],
    },

    # --------------------------------------------------------
    # BIBLIOTECA
    # --------------------------------------------------------
    "biblioteca": {
        "title": "Biblioteca",
        "image": "assets/imagens/biblioteca.png",
        "text": (
            "A biblioteca é enorme. As estantes chegam até o teto e "
            "uma grossa camada de poeira cobre os livros.\n\n"
            "No centro existe uma mesa com um diário antigo."
        ),
        "options": [
            ("Ler o diário", "ler_diario"),
            ("Procurar nas estantes", "achar_chave"),
            ("Abrir a gaveta da mesa", "gaveta_biblioteca"),
            ("Voltar ao hall", "hall"),
        ],
    },

    "ler_diario": {
        "title": "Diário",
        "image": "assets/imagens/diario.png",
        "text": (
            "Você lê a última página:\n\n"
            "\"Se alguém encontrar este diário, não confie no homem da "
            "máscara e do machado. Ele conhece todos os caminhos da casa. "
            "A única forma de escapar é encontrar a chave da garagem.\"\n\n"
            "A página seguinte foi arrancada."
        ),
        "options": [
            ("Guardar o diário", "pegar_diario"),
            ("Voltar", "biblioteca"),
        ],
    },

    "pegar_diario": {
        "title": "Diário encontrado",
        "image": "assets/imagens/diario.png",
        "text": "Você guarda o diário. Ele pode ser uma das peças para descobrir a verdade.",
        "options": [
            ("Continuar na biblioteca", "biblioteca"),
        ],
    },

    "achar_chave": {
        "title": "Livro secreto",
        "image": "assets/imagens/biblioteca.png",
        "text": (
            "Um livro parece diferente dos outros.\n\n"
            "Ao puxá-lo, uma pequena passagem se abre na parede. "
            "Atrás dela existe uma chave coberta de ferrugem."
        ),
        "options": [
            ("Pegar a chave enferrujada", "pegar_chave"),
            ("Deixar a chave", "biblioteca"),
        ],
    },

    "pegar_chave": {
        "title": "Chave enferrujada",
        "image": "assets/imagens/chave_enferrujada.png",
        "text": (
            "Você guarda a chave enferrujada.\n\n"
            "Ela parece importante. Talvez abra uma saída ou a garagem."
        ),
        "options": [
            ("Continuar explorando", "biblioteca"),
        ],
    },

    "gaveta_biblioteca": {
        "title": "Gaveta trancada",
        "image": "assets/imagens/biblioteca.png",
        "text": (
            "A gaveta da mesa está trancada. Você tenta puxá-la, "
            "mas nada acontece.\n\n"
            "Talvez seja necessário encontrar uma ferramenta."
        ),
        "options": [
            ("Procurar outra pista", "biblioteca"),
        ],
    },

    "usar_lanterna": {
        "title": "Lanterna",
        "image": "assets/imagens/lanterna.png",
        "text": (
            "Você acende a lanterna. O feixe corta a escuridão e revela "
            "detalhes que seriam difíceis de perceber sem luz."
        ),
        "options": [
            ("Voltar ao inventário", "inventario"),
        ],
    },

    # --------------------------------------------------------
    # BANHEIRO
    # --------------------------------------------------------
    "banheiro": {
        "title": "Banheiro",
        "image": "assets/imagens/banheiro.png",
        "text": (
            "O banheiro está completamente escuro.\n\n"
            "PING... PING...\n\n"
            "O espelho está quebrado e existem manchas estranhas nas "
            "paredes. Você vê um armário, uma pia e uma pequena janela."
        ),
        "options": [
            ("Abrir o armário", "banheiro_pilhas"),
            ("Examinar o espelho", "espelho"),
            ("Procurar na pia", "chave_pequena"),
            ("Tentar abrir a janela", "janela_banheiro"),
        ],
    },

    "banheiro_pilhas": {
        "title": "Pilhas",
        "image": "assets/imagens/banheiro.png",
        "text": (
            "Dentro do armário você encontra duas pilhas novas. "
            "Elas parecem perfeitas para alimentar a lanterna."
        ),
        "options": [
            ("Pegar as pilhas", "pegar_pilhas"),
            ("Voltar", "banheiro"),
        ],
    },

    "pegar_pilhas": {
        "title": "Item obtido",
        "image": "assets/imagens/pilhas.png",
        "text": "Você guarda as pilhas.",
        "options": [
            ("Continuar no banheiro", "banheiro"),
        ],
    },

    "espelho": {
        "title": "O espelho",
        "image": "assets/imagens/banheiro.png",
        "text": (
            "Por um instante, você vê uma pessoa atrás de você.\n\n"
            "Você se vira rapidamente. Não existe ninguém.\n\n"
            "Quando olha novamente para o espelho, a figura desapareceu."
        ),
        "options": [
            ("Respirar fundo", "hall"),
        ],
    },

    "chave_pequena": {
        "title": "Pequena chave",
        "image": "assets/imagens/banheiro.png",
        "text": (
            "Entre alguns objetos enferrujados, seus dedos encontram "
            "uma pequena chave. Você não sabe o que ela abre."
        ),
        "options": [
            ("Pegar a chave", "pegar_chave_pequena"),
            ("Deixar a chave", "banheiro"),
        ],
    },

    "pegar_chave_pequena": {
        "title": "Item obtido",
        "image": "assets/imagens/chave_pequena.png",
        "text": "Você guarda a pequena chave.",
        "options": [
            ("Continuar no banheiro", "banheiro"),
        ],
    },

    "janela_banheiro": {
        "title": "Janela",
        "image": "assets/imagens/jardim.png",
        "text": (
            "Você força a janela. Depois de alguns segundos, ela abre.\n\n"
            "Do outro lado existe um pequeno jardim abandonado.\n\n"
            "Talvez seja uma possível rota de fuga."
        ),
        "options": [
            ("Sair para o jardim", "jardim"),
            ("Voltar", "banheiro"),
        ],
    },

    # --------------------------------------------------------
    # ESCRITÓRIO
    # --------------------------------------------------------
    "escritorio": {
        "title": "Escritório",
        "image": "assets/imagens/escritorio.png",
        "text": (
            "O escritório parece ter pertencido ao antigo dono da mansão.\n\n"
            "Há uma grande escrivaninha, um computador antigo e fotografias "
            "da família Blackwood."
        ),
        "options": [
            ("Examinar a escrivaninha", "cartao_seguranca"),
            ("Ler documentos", "documentos"),
            ("Ligar o computador", "computador"),
            ("Examinar fotografias", "fotografias"),
        ],
    },

    "cartao_seguranca": {
        "title": "Cartão de segurança",
        "image": "assets/imagens/cartao_seguranca.png",
        "text": (
            "Escondido na escrivaninha há um cartão de segurança. "
            "Ele parece dar acesso a uma área restrita da mansão."
        ),
        "options": [
            ("Pegar o cartão", "pegar_cartao"),
            ("Voltar", "escritorio"),
        ],
    },

    "pegar_cartao": {
        "title": "Item obtido",
        "image": "assets/imagens/cartao_seguranca.png",
        "text": "Você guarda o cartão de segurança.",
        "options": [
            ("Continuar no escritório", "escritorio"),
        ],
    },

    "documentos": {
        "title": "Documentos",
        "image": "assets/imagens/documentos.png",
        "text": (
            "Você encontra documentos antigos sobre diversos "
            "desaparecimentos.\n\n"
            "Todos aconteceram dentro da mansão.\n\n"
            "A última anotação diz:\n\n"
            "\"Não deixe o assassino chegar ao porão.\""
        ),
        "options": [
            ("Continuar procurando", "escritorio"),
        ],
    },

    "computador": {
        "title": "Computador antigo",
        "image": "assets/imagens/escritorio.png",
        "text": (
            "O computador pede uma senha.\n\n"
            "Você não sabe a senha. Talvez exista alguma pista em outro cômodo."
        ),
        "options": [
            ("Voltar", "escritorio"),
        ],
    },

    "fotografias": {
        "title": "A família Blackwood",
        "image": "assets/imagens/escritorio.png",
        "text": (
            "Em uma das fotografias aparece um homem usando a mesma "
            "máscara branca marcada de vermelho que você viu na mansão.\n\n"
            "No verso está escrito:\n\n"
            "\"Michael Blackwood - 1987\""
        ),
        "options": [
            ("Guardar a informação", "escritorio"),
        ],
    },

    # --------------------------------------------------------
    # ESCADAS
    # --------------------------------------------------------
    "escadas": {
        "title": "Escadaria",
        "image": "assets/imagens/escadas.png",
        "text": (
            "Você está diante da enorme escadaria.\n\n"
            "O andar de cima está completamente escuro. O vento entra "
            "pelas janelas.\n\n"
            "Existem dois caminhos."
        ),
        "options": [
            ("Subir para o sótão", "sotao"),
            ("Descer para o porão", "porao"),
            ("Voltar ao hall", "hall_2"),
        ],
    },

    # --------------------------------------------------------
    # GARAGEM
    # --------------------------------------------------------
    "garagem": {
        "title": "Garagem",
        "image": "assets/imagens/garagem.png",
        "text": (
            "A caminhonete antiga está estacionada no centro da garagem.\n\n"
            "Caixas, ferramentas e um armário ocupam as paredes.\n\n"
            "Se encontrar gasolina e um fusível, talvez o veículo funcione."
        ),
        "options": [
            ("Examinar a caminhonete", "tentar_carro"),
            ("Procurar ferramentas", "achar_machado"),
            ("Procurar gasolina", "achar_gasolina"),
            ("Abrir o armário", "achar_fusivel"),
        ],
    },

    "tentar_carro": {
        "title": "Caminhonete",
        "image": "assets/imagens/garagem.png",
        "text": (
            "A caminhonete está sem combustível e sem energia.\n\n"
            "Você precisa encontrar gasolina e um fusível."
        ),
        "options": [
            ("Verificar itens", "verificar_carro"),
            ("Voltar", "garagem"),
        ],
    },

    "verificar_carro": {
        "title": "Preparar a fuga",
        "image": "assets/imagens/garagem.png",
        "text": "Você verifica o inventário e se prepara para tentar ligar a caminhonete.",
        "options": [
            ("Tentar ligar", "ligar_carro"),
            ("Voltar", "garagem"),
        ],
    },

    "ligar_carro": {
        "title": "A caminhonete",
        "image": "assets/imagens/garagem.png",
        "text": (
            "Você coloca a gasolina no tanque e instala o fusível.\n\n"
            "BRUM...\n\n"
            "BRUUUM!\n\n"
            "O motor liga. Você acelera para fora da garagem enquanto "
            "o assassino observa no meio da estrada."
        ),
        "options": [
            ("Escapar", "fim_carro"),
        ],
    },

    "achar_machado": {
        "title": "Machado",
        "image": "assets/imagens/machado.png",
        "text": (
            "Entre as ferramentas da garagem, você encontra um pesado "
            "machado de lenhador. O cabo gasto mostra que ele já foi "
            "usado muitas vezes."
        ),
        "options": [
            ("Pegar o machado", "pegar_machado"),
            ("Voltar", "garagem"),
        ],
    },

    "pegar_machado": {
        "title": "Item obtido",
        "image": "assets/imagens/machado.png",
        "text": "Você guarda o machado. Talvez seja sua melhor defesa.",
        "options": [
            ("Continuar na garagem", "garagem"),
        ],
    },

    "achar_gasolina": {
        "title": "Gasolina",
        "image": "assets/imagens/garagem.png",
        "text": (
            "Atrás das caixas existe um galão de gasolina. "
            "Talvez seja exatamente o que a caminhonete precisa."
        ),
        "options": [
            ("Pegar gasolina", "pegar_gasolina"),
            ("Deixar", "garagem"),
        ],
    },

    "pegar_gasolina": {
        "title": "Item obtido",
        "image": "assets/imagens/garagem.png",
        "text": "Você guarda o galão de gasolina.",
        "options": [
            ("Continuar", "garagem"),
        ],
    },

    "achar_fusivel": {
        "title": "Fusível",
        "image": "assets/imagens/fusivel.png",
        "text": (
            "No armário existe um fusível antigo, ainda inteiro. "
            "Talvez ele possa restaurar a energia."
        ),
        "options": [
            ("Pegar o fusível", "pegar_fusivel"),
            ("Deixar", "garagem"),
        ],
    },

    "pegar_fusivel": {
        "title": "Item obtido",
        "image": "assets/imagens/fusivel.png",
        "text": "Você guarda o fusível.",
        "options": [
            ("Continuar", "garagem"),
        ],
    },

    # --------------------------------------------------------
    # PORÃO
    # --------------------------------------------------------
    "porao": {
        "title": "Porão",
        "image": "assets/imagens/porao.png",
        "text": (
            "A temperatura cai rapidamente. A luz do teto pisca.\n\n"
            "Você encontra um gerador antigo e uma porta de metal com "
            "um painel eletrônico."
        ),
        "options": [
            ("Examinar o gerador", "gerador"),
            ("Examinar a porta de metal", "porta_seguranca"),
            ("Procurar objetos", "achar_radio"),
            ("Voltar às escadas", "escadas"),
        ],
    },

    "gerador": {
        "title": "Gerador",
        "image": "assets/imagens/porao.png",
        "text": (
            "Um gerador antigo ocupa o canto do porão. "
            "Ele parece estar sem um fusível."
        ),
        "options": [
            ("Instalar o fusível", "ligar_gerador"),
            ("Voltar", "porao"),
        ],
    },

    "ligar_gerador": {
        "title": "Energia restaurada",
        "image": "assets/imagens/porao.png",
        "text": (
            "Você coloca o fusível no gerador.\n\n"
            "Depois de algumas tentativas...\n\n"
            "BRUUUUM!\n\n"
            "A energia da mansão volta."
        ),
        "options": [
            ("Ir para a porta de segurança", "porta_seguranca"),
            ("Voltar", "porao"),
        ],
    },

    "porta_seguranca": {
        "title": "Porta de segurança",
        "image": "assets/imagens/porao.png",
        "text": (
            "Uma porta de metal bloqueia o caminho.\n\n"
            "O painel eletrônico pede um cartão de segurança."
        ),
        "options": [
            ("Usar cartão de segurança", "abrir_seguranca"),
            ("Voltar", "porao"),
        ],
    },

    "abrir_seguranca": {
        "title": "Sala de segurança",
        "image": "assets/imagens/seguranca.png",
        "text": (
            "O cartão funciona.\n\n"
            "A porta se abre para uma pequena sala de segurança, "
            "cheia de monitores e equipamentos."
        ),
        "options": [
            ("Entrar", "seguranca"),
        ],
    },

    "achar_radio": {
        "title": "Rádio",
        "image": "assets/imagens/radio.png",
        "text": (
            "Dentro de uma caixa de madeira há um rádio antigo. "
            "Apesar da poeira, os botões ainda se movem."
        ),
        "options": [
            ("Pegar o rádio", "pegar_radio"),
            ("Deixar", "porao"),
        ],
    },

    "pegar_radio": {
        "title": "Item obtido",
        "image": "assets/imagens/radio.png",
        "text": "Você guarda o rádio.",
        "options": [
            ("Continuar no porão", "porao"),
        ],
    },

    # --------------------------------------------------------
    # SÓTÃO
    # --------------------------------------------------------
    "sotao": {
        "title": "Sótão",
        "image": "assets/imagens/sotao.png",
        "text": (
            "O sótão está cheio de caixas. Uma pequena janela deixa "
            "entrar a luz da lua.\n\n"
            "Você escuta alguém respirando.\n\n"
            "Há uma pessoa escondida atrás de algumas caixas."
        ),
        "options": [
            ("Conversar com a pessoa", "sarah"),
            ("Procurar nas caixas", "achar_fita"),
            ("Examinar a janela", "janela_sotao"),
            ("Descer ao hall", "hall_2"),
        ],
    },

    "sarah": {
        "title": "Sarah",
        "image": "assets/imagens/sotao.png",
        "text": (
            "A pessoa está assustada.\n\n"
            "Ela diz:\n\n"
            "\"Meu nome é Sarah. Estou presa aqui há dois dias. "
            "O assassino conhece todos os cômodos. Existe uma saída "
            "secreta na sala de segurança.\"\n\n"
            "Ela entrega uma chave pesada para você."
        ),
        "options": [
            ("Aceitar a chave mestra", "salvar_sarah"),
            ("Voltar", "sotao"),
        ],
    },

    "salvar_sarah": {
        "title": "Chave mestra",
        "image": "assets/imagens/chave_mestra.png",
        "text": (
            "Sarah coloca uma chave pesada em sua mão. Ela parece "
            "diferente de todas as outras chaves da mansão.\n\n"
            "\"Precisamos sair daqui.\""
        ),
        "options": [
            ("Continuar explorando", "sotao"),
        ],
    },

    "achar_fita": {
        "title": "Fita VHS",
        "image": "assets/imagens/fita_vhs.png",
        "text": (
            "Entre as caixas você encontra uma fita VHS empoeirada. "
            "Uma etiqueta quase apagada indica que ela foi gravada "
            "dentro da mansão."
        ),
        "options": [
            ("Pegar a fita", "pegar_fita"),
            ("Deixar a fita", "sotao"),
        ],
    },

    "pegar_fita": {
        "title": "Item obtido",
        "image": "assets/imagens/fita_vhs.png",
        "text": "Você guarda a fita VHS.",
        "options": [
            ("Continuar no sótão", "sotao"),
        ],
    },

    "janela_sotao": {
        "title": "Janela do sótão",
        "image": "assets/imagens/sotao.png",
        "text": "A janela dá para o telhado. A queda é muito alta. Você não pode escapar por aqui.",
        "options": [
            ("Voltar", "sotao"),
        ],
    },

    # --------------------------------------------------------
    # JARDIM
    # --------------------------------------------------------
    "jardim": {
        "title": "Jardim abandonado",
        "image": "assets/imagens/jardim.png",
        "text": (
            "Você sai pela janela do banheiro.\n\n"
            "O jardim está completamente abandonado. Árvores enormes "
            "cercam uma pequena cabana.\n\n"
            "Ao longe existe um portão.\n\n"
            "Você percebe uma sombra entre as árvores."
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
        "image": "assets/imagens/jardim.png",
        "text": (
            "O enorme portão está trancado.\n\n"
            "Você precisa da chave enferrujada para abrir o cadeado."
        ),
        "options": [
            ("Usar chave enferrujada", "abrir_portao"),
            ("Voltar ao jardim", "jardim"),
        ],
    },

    "abrir_portao": {
        "title": "Fuga pelo portão",
        "image": "assets/imagens/fuga_portao.png",
        "text": (
            "CLIC!\n\n"
            "O cadeado se abre. Você atravessa o portão e corre "
            "pela estrada.\n\n"
            "Depois de alguns minutos, encontra um carro passando."
        ),
        "options": [
            ("Continuar fugindo", "fim_fuga"),
        ],
    },

    "cabana": {
        "title": "Cabana",
        "image": "assets/imagens/jardim.png",
        "text": (
            "Dentro da caixa de ferramentas existe um pé de cabra. "
            "Pode ser útil para forçar alguma passagem ou abrir algo emperrado."
        ),
        "options": [
            ("Pegar o pé de cabra", "pegar_pe_cabra"),
            ("Voltar", "jardim"),
        ],
    },

    "pegar_pe_cabra": {
        "title": "Item obtido",
        "image": "assets/imagens/jardim.png",
        "text": "Você guarda o pé de cabra.",
        "options": [
            ("Voltar ao jardim", "jardim"),
        ],
    },

    "esconder_jardim": {
        "title": "Escondido entre as árvores",
        "image": "assets/imagens/jardim.png",
        "text": (
            "Você se esconde atrás de uma árvore.\n\n"
            "A sombra passa lentamente.\n\n"
            "Por sorte, o assassino não percebe você."
        ),
        "options": [
            ("Voltar para a casa", "hall_2"),
        ],
    },

    # --------------------------------------------------------
    # SALA DE SEGURANÇA
    # --------------------------------------------------------
    "seguranca": {
        "title": "Sala de segurança",
        "image": "assets/imagens/seguranca.png",
        "text": (
            "Vários monitores mostram diferentes partes da mansão.\n\n"
            "Uma mesa possui um rádio e há um painel com vários botões.\n\n"
            "Uma câmera mostra o assassino caminhando pelo corredor."
        ),
        "options": [
            ("Ver câmeras", "cameras"),
            ("Usar o rádio", "usar_radio"),
            ("Procurar saída secreta", "saida_secreta"),
            ("Assistir à fita VHS", "assistir_fita"),
        ],
    },

    "cameras": {
        "title": "Câmeras de segurança",
        "image": "assets/imagens/seguranca.png",
        "text": (
            "Câmera 1: Hall principal.\n"
            "Câmera 2: Cozinha.\n"
            "Câmera 3: Biblioteca.\n"
            "Câmera 4: Jardim.\n"
            "Câmera 5: Segundo andar.\n\n"
            "De repente, a câmera do hall mostra o assassino. "
            "A máscara branca encara diretamente a lente."
        ),
        "options": [
            ("Continuar", "seguranca"),
        ],
    },

    "usar_radio": {
        "title": "Rádio",
        "image": "assets/imagens/radio.png",
        "text": (
            "Você tenta encontrar uma frequência.\n\n"
            "CHIADO...\n\n"
            "Uma voz responde:\n\n"
            "\"Se alguém estiver ouvindo... saia dessa casa imediatamente.\"\n\n"
            "\"Ele já sabe onde você está.\""
        ),
        "options": [
            ("Pedir ajuda", "pedir_ajuda"),
            ("Perguntar sobre o assassino", "perguntar_assassino"),
            ("Desligar o rádio", "seguranca"),
        ],
    },

    "pedir_ajuda": {
        "title": "Pedido de socorro",
        "image": "assets/imagens/radio.png",
        "text": (
            "Você pede ajuda pelo rádio.\n\n"
            "A voz responde:\n\n"
            "\"Continue transmitindo. A polícia está a caminho.\""
        ),
        "options": [
            ("Esperar na sala de segurança", "fim_policia"),
            ("Continuar investigando", "seguranca"),
        ],
    },

    "perguntar_assassino": {
        "title": "Michael Blackwood",
        "image": "assets/imagens/radio.png",
        "text": (
            "Você pergunta quem é o assassino.\n\n"
            "Depois de alguns segundos, a voz responde:\n\n"
            "\"Michael Blackwood.\"\n\n"
            "O rádio desliga. Você lembra da fotografia encontrada "
            "no escritório."
        ),
        "options": [
            ("Continuar", "seguranca"),
        ],
    },

    "saida_secreta": {
        "title": "Porta secreta",
        "image": "assets/imagens/seguranca.png",
        "text": (
            "Atrás dos monitores existe uma porta escondida.\n\n"
            "Ela está trancada. Uma chave especial parece ser necessária."
        ),
        "options": [
            ("Usar chave mestra", "abrir_tunel"),
            ("Voltar", "seguranca"),
        ],
    },

    "abrir_tunel": {
        "title": "Túnel secreto",
        "image": "assets/imagens/tunel_secreto.png",
        "text": (
            "A chave mestra funciona.\n\n"
            "Atrás da porta existe um túnel antigo que leva para fora "
            "da propriedade."
        ),
        "options": [
            ("Entrar no túnel", "tunel"),
            ("Voltar", "seguranca"),
        ],
    },

    "assistir_fita": {
        "title": "Fita VHS",
        "image": "assets/imagens/fita_vhs.png",
        "text": (
            "A gravação mostra a mansão muitos anos atrás.\n\n"
            "Um homem chamado Michael Blackwood aparece na gravação "
            "e fala sobre a casa e sua família.\n\n"
            "No final aparece uma mensagem:\n\n"
            "\"Se você está vendo isso... ele ainda está aqui.\""
        ),
        "options": [
            ("Continuar", "seguranca"),
        ],
    },

    # --------------------------------------------------------
    # TÚNEL
    # --------------------------------------------------------
    "tunel": {
        "title": "Túnel secreto",
        "image": "assets/imagens/tunel_secreto.png",
        "text": (
            "Você entra no túnel.\n\n"
            "As paredes são antigas. Depois de alguns metros, encontra "
            "duas saídas: uma leva para a floresta e outra parece voltar "
            "para a mansão."
        ),
        "options": [
            ("Ir para a floresta", "fim_tunel"),
            ("Voltar para a sala de segurança", "seguranca"),
        ],
    },

    # --------------------------------------------------------
    # EVENTOS ESPECIAIS DO ASSASSINO
    # --------------------------------------------------------
    "evento_passos": {
        "title": "SOM DOS PASSOS",
        "image": "assets/imagens/som_passos.png",
        "text": (
            "Você ouve passos atrás de você.\n\n"
            "Quando se vira...\n\n"
            "Não há ninguém.\n\n"
            "O som para. Por alguns segundos, a mansão fica em silêncio."
        ),
        "options": [
            ("Continuar", "voltar_evento"),
        ],
    },

    "evento_distancia": {
        "title": "ASSASSINO À DISTÂNCIA",
        "image": "assets/imagens/assassino_a_distancia.png",
        "text": (
            "No fim do corredor, uma figura observa você.\n\n"
            "A máscara branca marcada de vermelho permanece imóvel.\n\n"
            "Você pisca.\n\n"
            "Ele desapareceu."
        ),
        "options": [
            ("Continuar", "voltar_evento"),
            ("Seguir para as escadas", "escadas"),
        ],
    },

    "evento_corredor": {
        "title": "APARIÇÃO NO CORREDOR",
        "image": "assets/imagens/aparicao_corredor.png",
        "text": (
            "Uma sombra atravessa o corredor.\n\n"
            "Você reconhece a máscara branca e o casaco vermelho.\n\n"
            "Quando olha novamente, não há ninguém."
        ),
        "options": [
            ("Continuar", "voltar_evento"),
            ("Correr", "perseguicao"),
        ],
    },

    "evento_respiracao": {
        "title": "RESPIRAÇÃO PESADA",
        "image": "assets/imagens/respiracao_pesada.png",
        "text": (
            "Você escuta uma respiração pesada muito perto.\n\n"
            "O som vem do outro lado da porta.\n\n"
            "Alguém está ali."
        ),
        "options": [
            ("Abrir a porta", "combate"),
            ("Afastar-se em silêncio", "voltar_evento"),
        ],
    },

    "evento_mascara": {
        "title": "MÁSCARA ENSANGUENTADA",
        "image": "assets/imagens/mascara_ensanguentada.png",
        "text": (
            "Você encontra uma máscara branca marcada de vermelho.\n\n"
            "Ela está suja de sangue.\n\n"
            "Alguém esteve aqui recentemente."
        ),
        "options": [
            ("Continuar", "voltar_evento"),
        ],
    },

    "evento_sala": {
        "title": "ASSASSINO NA SALA",
        "image": "assets/imagens/assassino_na_sala.png",
        "text": (
            "Você entra em uma sala e percebe tarde demais que não está sozinho.\n\n"
            "O assassino está ali."
        ),
        "options": [
            ("Correr", "perseguicao"),
            ("Esconder-se", "esconder_assassino"),
            ("Enfrentar", "combate"),
        ],
    },

    "evento_seguranca": {
        "title": "ASSASSINO NA SEGURANÇA",
        "image": "assets/imagens/assassino_na_seguranca.png",
        "text": (
            "As câmeras mostram o corredor.\n\n"
            "Então você percebe algo assustador: o assassino aparece "
            "na imagem da sala de segurança."
        ),
        "options": [
            ("Correr", "perseguicao"),
            ("Trancar a porta", "seguranca"),
        ],
    },

    "evento_assassino": {

        "title": "VOCÊ NÃO ESTÁ SOZINHO",
        "image": "assets/imagens/encontro_repentino.png",
        "text": (
            "Um barulho vem do outro lado da sala.\n\n"
            "Uma sombra passa pela porta.\n\n"
            "Você percebe a máscara branca marcada de vermelho e o "
            "brilho metálico do machado.\n\n"
            "O assassino está perto."
        ),
        "options": [
            ("Correr / fugir", "perseguicao"),
            ("Se esconder", "esconder_assassino"),
            ("Enfrentar", "combate"),
        ],
    },

    "esconder_assassino": {
        "title": "Esconder-se",
        "image": "assets/imagens/esconder_se.png",
        "text": (
            "Você entra rapidamente em um armário e segura a respiração.\n\n"
            "O assassino passa pelo corredor.\n\n"
            "Depois de alguns segundos, ele vai embora."
        ),
        "options": [
            ("Voltar ao hall", "hall_2"),
        ],
    },

    # --------------------------------------------------------
    # PERSEGUIÇÃO
    # --------------------------------------------------------
    "perseguicao": {
        "title": "PERSEGUIÇÃO",
        "image": "assets/imagens/perseguicao.png",
        "text": (
            "Você corre pelos corredores da mansão.\n\n"
            "Os passos do assassino ficam cada vez mais próximos.\n\n"
            "Você chega a uma bifurcação."
        ),
        "options": [
            ("Ir pela esquerda", "perseguicao_esquerda"),
            ("Ir pela direita", "perseguicao_direita"),
            ("Esconder-se", "perseguicao_esconder"),
        ],
    },

    "perseguicao_esquerda": {
        "title": "Corredor esquerdo",
        "image": "assets/imagens/perseguicao.png",
        "text": (
            "Você entra em um quarto e fecha a porta.\n\n"
            "O assassino passa direto."
        ),
        "options": [
            ("Continuar", "hall_2"),
            ("Tentar pela janela", "jardim"),
            ("A porta não segura...", "combate"),
        ],
    },

    "perseguicao_direita": {
        "title": "Corredor direito",
        "image": "assets/imagens/perseguicao.png",
        "text": (
            "Você corre pelo corredor. Uma porta leva à cozinha; "
            "outro caminho conduz às escadas."
        ),
        "options": [
            ("Entrar na cozinha", "cozinha"),
            ("Ir para as escadas", "sotao"),
            ("Tropeçar e perder vida", "dano_perseguicao"),
        ],
    },

    "dano_perseguicao": {
        "title": "Você tropeçou",
        "image": "assets/imagens/perseguicao.png",
        "text": "Você tropeça em alguns objetos e o assassino se aproxima. Você perde 1 ponto de vida.",
        "options": [
            ("Levantar e correr", "perder_vida_perseguicao"),
        ],
    },

    "perseguicao_esconder": {
        "title": "Esconder-se",
        "image": "assets/imagens/esconder_se.png",
        "text": (
            "Você se esconde atrás de uma cortina.\n\n"
            "O assassino entra e procura por alguns segundos..."
        ),
        "options": [
            ("Esperar", "resultado_esconder"),
        ],
    },

    "resultado_esconder": {
        "title": "Silêncio",
        "image": "assets/imagens/esconder_se.png",
        "text": "O assassino vai embora. Você consegue respirar novamente.",
        "options": [
            ("Voltar ao hall", "hall_2"),
        ],
    },

    # --------------------------------------------------------
    # COMBATE
    # --------------------------------------------------------
    "combate": {
        "title": "ÚLTIMO CONFRONTO",
        "image": "assets/imagens/combater.png",
        "text": (
            "O assassino aparece no final do corredor.\n\n"
            "A máscara branca esconde completamente seu rosto. "
            "O casaco vermelho balança enquanto ele segura o pesado "
            "machado de lenhador.\n\n"
            "Ele bloqueia a saída. Você precisa agir rapidamente."
        ),
        "options": [
            ("Usar a faca", "combate_faca"),
            ("Usar o machado", "combate_machado"),
            ("Correr / fugir", "perseguicao"),
            ("Se esconder", "esconder_assassino"),
        ],
    },

    "combate_faca": {
        "title": "Ataque com faca",
        "image": "assets/imagens/combater.png",
        "text": (
            "Você usa a faca para criar uma oportunidade e consegue "
            "escapar do corredor. O assassino continua atrás de você."
        ),
        "options": [
            ("Continuar fugindo", "perseguicao"),
        ],
    },

    "combate_machado": {
        "title": "Ataque com machado",
        "image": "assets/imagens/combater.png",
        "text": (
            "Você segura o machado.\n\n"
            "Quando o assassino avança, você consegue afastá-lo e fugir.\n\n"
            "Ele não consegue continuar seguindo você por alguns instantes."
        ),
        "options": [
            ("Voltar ao hall", "hall_2"),
        ],
    },

    # --------------------------------------------------------
    # FINAIS
    # --------------------------------------------------------
    "fim_fuga": {
        "title": "FINAL BOM — FUGA PELO PORTÃO",
        "image": "assets/imagens/fuga_portao.png",
        "text": (
            "Você atravessa o portão e corre pela estrada.\n\n"
            "Um motorista para e chama a polícia.\n\n"
            "Quando olha para trás, a mansão está completamente escura.\n\n"
            "Você sobreviveu. Mas ninguém acredita quando você conta "
            "sobre o homem mascarado."
        ),
        "options": [],
    },

    "fim_carro": {
        "title": "FINAL BOM — FUGA DE CARRO",
        "image": "assets/imagens/fuga_carro.png",
        "text": (
            "A caminhonete liga e você acelera para fora da garagem.\n\n"
            "O portão se abre lentamente.\n\n"
            "Pelo retrovisor, você vê o assassino parado no meio da estrada.\n\n"
            "Ele observa você desaparecer na tempestade.\n\n"
            "Você conseguiu escapar."
        ),
        "options": [],
    },

    "fim_tunel": {
        "title": "FINAL BOM — TÚNEL SECRETO",
        "image": "assets/imagens/tunel_secreto.png",
        "text": (
            "Você atravessa o túnel. Finalmente vê a luz da lua.\n\n"
            "Você sai no meio da floresta e encontra uma estrada.\n\n"
            "Um carro da polícia passa pelo local. Você pede ajuda.\n\n"
            "Quando os policiais chegam à mansão, ela parece completamente "
            "abandonada. Apenas uma máscara é encontrada no chão."
        ),
        "options": [],
    },

    "fim_policia": {
        "title": "FINAL BOM — PEDIDO DE SOCORRO",
        "image": "assets/imagens/ajuda_policia.png",
        "text": (
            "Você se tranca na sala de segurança.\n\n"
            "Minutos depois...\n\n"
            "SIRENES.\n\n"
            "As portas da mansão são arrombadas. Policiais entram no prédio.\n\n"
            "Você finalmente está seguro.\n\n"
            "Mas o assassino desapareceu. A polícia encontra apenas "
            "uma máscara em um dos corredores."
        ),
        "options": [],
    },

    "fim_secreto": {
        "title": "FINAL SECRETO — A VERDADE DE BLACKWOOD",
        "image": "assets/imagens/final_secreto.png",
        "text": (
            "Você reuniu todas as pistas: o diário, a fita VHS, os documentos "
            "e a chave mestra.\n\n"
            "Michael Blackwood não era apenas um assassino. Ele era o antigo "
            "dono da mansão. Depois que sua família desapareceu, ele enlouqueceu "
            "e passou a perseguir qualquer pessoa que entrasse na propriedade.\n\n"
            "A fita revela que ele criou túneis secretos para observar todos "
            "os cômodos.\n\n"
            "A polícia nunca encontrou o corpo dele.\n\n"
            "Você escapa com as provas. Dias depois, a investigação é reaberta "
            "e a verdade sobre a família Blackwood finalmente vem à tona."
        ),
        "options": [],
    },

    "fim_morte": {
        "title": "FINAL RUIM — A ÚLTIMA NOITE",
        "image": "assets/imagens/final_ruim.png",
        "stop_audio": True,
        "text": (
            "Você já não consegue continuar.\n\n"
            "Sua visão fica cada vez mais fraca. Os passos do assassino "
            "se aproximam.\n\n"
            "Você tenta encontrar uma saída...\n\n"
            "Mas é tarde demais.\n\n"
            "A mansão volta ao silêncio."
        ),
        "options": [],
    },

    "fim_preso": {
        "title": "FINAL RUIM — PRESO PARA SEMPRE",
        "image": "assets/imagens/preso_mansao.png",
        "stop_audio": True,
        "text": (
            "Você procura uma saída durante horas.\n\n"
            "Cada porta leva a outro corredor. Cada corredor parece igual.\n\n"
            "A mansão parece não ter fim.\n\n"
            "O amanhecer chega, mas você continua dentro da casa.\n\n"
            "Dias passam. Ninguém vem.\n\n"
            "Você nunca consegue encontrar a saída."
        ),
        "options": [],
    },
}


# ============================================================
# FUNÇÕES DO FRAMEWORK
# ============================================================

def el(id_elemento):
    return web.page[id_elemento]


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
    trilha = CONFIG.get("trilha_inicial")

    audio.dataset.inicial = trilha or ""
    audio.dataset.volume = str(CONFIG.get("volume_inicial", 0.5))


def atualizar_status():
    vida = state["vida"]

    if vida > 0:
        el("vida").innerText = " ".join(["❤️"] * vida)
        el("vida").classList.remove("danger")
    else:
        el("vida").innerText = "💀"
        el("vida").classList.add("danger")

    if state["inventario"]:
        el("inventario").innerText = ", ".join(state["inventario"])
    else:
        el("inventario").innerText = "Vazio"

    el("pontos").innerText = str(state["pontos"])


def mostrar_imagem(caminho, titulo=""):
    """Mostra no HTML a imagem correspondente ao nó/cena escolhida."""
    if hasattr(window, "frameworkImage"):
        window.frameworkImage.show(caminho or "", titulo or "")
        return

    # Fallback caso o helper JS ainda não esteja disponível.
    window.frameworkVideo.stop()
    imagem = el("imagem-cena")

    if not caminho:
        imagem.style.display = "none"
        return

    imagem.src = caminho
    imagem.alt = f"Imagem: {titulo}" if titulo else "Imagem da cena atual"
    imagem.style.display = "block"


def mostrar_video(caminho, autoplay=False):
    if not caminho:
        window.frameworkVideo.stop()
        return

    window.frameworkVideo.play(caminho, autoplay)


def trocar_audio(caminho):
    if not caminho:
        return

    window.frameworkAudio.play(
        caminho,
        CONFIG.get("volume_inicial", 0.5),
        True
    )


def parar_audio():
    window.frameworkAudio.stop()


def configurar_botao(numero, texto="", ativo=False):
    botao = el(f"opcao{numero}")
    botao.innerText = texto
    botao.disabled = not ativo

    if ativo:
        botao.style.display = "block"
    else:
        botao.style.display = "none"


def atualizar_botoes(opcoes):
    for i in range(1, 5):
        if i <= len(opcoes):
            configurar_botao(i, opcoes[i - 1][0], True)
        else:
            configurar_botao(i, "", False)


def adicionar_item(item, pontos=0):
    if item not in state["inventario"]:
        state["inventario"].append(item)
        state["pontos"] += pontos

    atualizar_status()


def remover_item(item):
    if item in state["inventario"]:
        state["inventario"].remove(item)

    atualizar_status()


def possui_item(item):
    return item in state["inventario"]


def ganhar_pontos(quantidade):
    state["pontos"] += quantidade
    atualizar_status()


def perder_vida(quantidade=1, cena_sem_vida="fim_morte"):
    state["vida"] -= quantidade

    if state["vida"] <= 0:
        state["vida"] = 0
        atualizar_status()
        mostrar_cena(cena_sem_vida, permitir_evento=False)
        return True

    atualizar_status()
    return False


def usar_kit():
    if not possui_item("kit medico"):
        return False

    if state["vida"] >= CONFIG["vida_inicial"]:
        return False

    remover_item("kit medico")
    state["vida"] = min(CONFIG["vida_inicial"], state["vida"] + 2)
    ganhar_pontos(5)
    return True


def verificar_final_secreto():
    itens = {
        "diario",
        "fita",
        "cartao seguranca",
        "chave mestra",
    }
    return itens.issubset(set(state["inventario"]))


# ============================================================
# EVENTO ALEATÓRIO DO ASSASSINO
# ============================================================

EVENTOS_ASSASSINO = [
    "evento_passos",
    "evento_distancia",
    "evento_corredor",
    "evento_respiracao",
    "evento_mascara",
    "evento_sala",
    "evento_seguranca",
    "evento_assassino",
]

CENAS_FINAIS = {
    "fim_fuga",
    "fim_carro",
    "fim_tunel",
    "fim_policia",
    "fim_secreto",
    "fim_morte",
    "fim_preso",
}

def deve_ativar_assassino(nome):
    if nome in CENAS_FINAIS:
        return False

    if nome in {"inicio", "entrada_mansao", "evento_assassino"}:
        return False

    if state["assassino_alertado"]:
        return False

    # 20%, como na história original.
    return random.randint(1, 10) <= 2


# ============================================================
# MOSTRAR CENA
# ============================================================

def mostrar_cena(nome, permitir_evento=True):

    if nome not in SCENES:
        el("titulo-cena").innerText = "Erro de cena"
        el("texto-cena").innerText = f"A cena '{nome}' não existe."
        atualizar_botoes([])
        return

    # Evento global: o assassino pode interromper uma exploração.
    if permitir_evento and deve_ativar_assassino(nome):
        state["cena_anterior"] = nome
        state["assassino_alertado"] = True
        evento = random.choice(EVENTOS_ASSASSINO)
        mostrar_cena(evento, permitir_evento=False)
        return

    state["cena"] = nome
    cena = SCENES[nome]

    el("titulo-cena").innerText = cena.get("title", nome)

    texto = cena.get("text", "")

    if nome == "inventario":
        itens = ", ".join(state["inventario"]) if state["inventario"] else "Nenhum"
        texto = (
            "Itens carregados:\n\n"
            f"{itens}\n\n"
            "Você pode usar o kit médico, acender a lanterna ou voltar."
        )

    el("texto-cena").innerText = texto

    video = cena.get("video")

    if video:
        mostrar_video(video, cena.get("video_autoplay", False))
    else:
        mostrar_imagem(cena.get("image"), cena.get("title", nome))

    if "audio" in cena:
        if cena["audio"]:
            trocar_audio(cena["audio"])
        else:
            parar_audio()

    if cena.get("stop_audio"):
        parar_audio()

    atualizar_botoes(cena.get("options", []))
    atualizar_status()


# ============================================================
# AÇÕES
# ============================================================

def executar_acao(acao):

    # ---------- ITENS ----------
    if acao == "pegar_faca":
        adicionar_item("faca", 10)
        mostrar_cena("cozinha")

    elif acao == "pegar_kit":
        adicionar_item("kit medico", 10)
        mostrar_cena("cozinha")

    elif acao == "pegar_lanterna":
        adicionar_item("lanterna", 10)
        mostrar_cena("cozinha")

    elif acao == "pegar_diario":
        adicionar_item("diario", 15)
        mostrar_cena("biblioteca")

    elif acao == "pegar_chave":
        adicionar_item("chave enferrujada", 15)
        mostrar_cena("biblioteca")

    elif acao == "pegar_pilhas":
        adicionar_item("pilhas", 5)
        mostrar_cena("banheiro")

    elif acao == "pegar_chave_pequena":
        adicionar_item("chave pequena", 5)
        mostrar_cena("banheiro")

    elif acao == "pegar_cartao":
        adicionar_item("cartao seguranca", 15)
        mostrar_cena("escritorio")

    elif acao == "pegar_machado":
        adicionar_item("machado", 20)
        mostrar_cena("garagem")

    elif acao == "pegar_gasolina":
        adicionar_item("gasolina", 10)
        mostrar_cena("garagem")

    elif acao == "pegar_fusivel":
        adicionar_item("fusivel", 10)
        mostrar_cena("garagem")

    elif acao == "pegar_radio":
        adicionar_item("radio", 10)
        mostrar_cena("porao")

    elif acao == "salvar_sarah":
        state["sobrevivente_salvo"] = True
        adicionar_item("chave mestra", 25)
        mostrar_cena("sotao")

    elif acao == "pegar_fita":
        adicionar_item("fita", 15)
        mostrar_cena("sotao")

    elif acao == "pegar_pe_cabra":
        adicionar_item("pe de cabra", 5)
        mostrar_cena("jardim")

    # ---------- GARAGEM ----------
    elif acao == "abrir_garagem":
        if possui_item("chave enferrujada"):
            ganhar_pontos(5)
            mostrar_cena("garagem")
        else:
            mostrar_cena("verificar_garagem")

    elif acao == "ligar_carro":
        if possui_item("gasolina") and possui_item("fusivel"):
            ganhar_pontos(40)
            mostrar_cena("fim_carro")
        else:
            mostrar_cena("tentar_carro")

    # ---------- PORÃO / SEGURANÇA ----------
    elif acao == "ligar_gerador":
        if possui_item("fusivel"):
            state["gerador_ligado"] = True
            ganhar_pontos(15)
            mostrar_cena("ligar_gerador")
        else:
            mostrar_cena("gerador")

    elif acao == "abrir_seguranca":
        if possui_item("cartao seguranca"):
            ganhar_pontos(20)
            mostrar_cena("seguranca")
        else:
            mostrar_cena("porta_seguranca")

    # ---------- RÁDIO ----------
    elif acao == "pedir_ajuda":
        if possui_item("radio"):
            state["radio_ajuda"] = True
            ganhar_pontos(30)
            mostrar_cena("fim_policia")
        else:
            mostrar_cena("usar_radio")

    # ---------- TÚNEL / FINAL SECRETO ----------
    elif acao == "abrir_tunel":
        if possui_item("chave mestra"):
            ganhar_pontos(25)
            mostrar_cena("tunel")
        else:
            mostrar_cena("saida_secreta")

    elif acao == "assistir_fita":
        if possui_item("fita"):
            state["fita_assistida"] = True
            ganhar_pontos(20)

            if verificar_final_secreto():
                mostrar_cena("fim_secreto")
            else:
                mostrar_cena("assistir_fita")
        else:
            mostrar_cena("seguranca")

    # ---------- PORTÃO ----------
    elif acao == "abrir_portao":
        if possui_item("chave enferrujada"):
            ganhar_pontos(30)
            mostrar_cena("fim_fuga")
        else:
            mostrar_cena("portao_jardim")

    # ---------- PERSEGUIÇÃO ----------
    elif acao == "perder_vida_perseguicao":
        morreu = perder_vida(1)

        if not morreu:
            mostrar_cena("hall_2")

    # ---------- COMBATE ----------
    elif acao == "combate_faca":
        if possui_item("faca"):
            remover_item("faca")
            ganhar_pontos(10)
            mostrar_cena("perseguicao")
        else:
            mostrar_cena("perseguicao")

    elif acao == "combate_machado":
        if possui_item("machado"):
            state["assassino_alertado"] = False
            ganhar_pontos(20)
            mostrar_cena("hall_2")
        else:
            mostrar_cena("perseguicao")

    elif acao == "esconder_assassino":
        state["assassino_alertado"] = False
        ganhar_pontos(5)
        mostrar_cena("hall_2")

    # ---------- KIT MÉDICO ----------
    elif acao == "usar_kit":
        usar_kit()
        mostrar_cena(state["cena"], permitir_evento=False)

    # ---------- FINAL SECRETO ----------
    elif acao == "decidir_final":
        if verificar_final_secreto():
            mostrar_cena("fim_secreto")
        else:
            mostrar_cena("fim_preso")

    # ---------- RETORNO DE EVENTO ----------
    elif acao == "voltar_evento":
        state["assassino_alertado"] = False
        mostrar_cena(state.get("cena_anterior", "hall_2"), permitir_evento=False)

    # ---------- AÇÃO NORMAL ----------
    elif acao in SCENES:
        # Ao terminar uma perseguição/encontro, o assassino perde o rastro.
        if state["cena"] in {
            "perseguicao",
            "perseguicao_esquerda",
            "perseguicao_direita",
            "perseguicao_esconder",
            "resultado_esconder",
        } and acao not in {
            "perseguicao",
            "combate",
            "fim_morte",
        }:
            state["assassino_alertado"] = False

        mostrar_cena(acao)

    else:
        el("texto-cena").innerText = f"A ação '{acao}' não foi cadastrada."


# ============================================================
# ESCOLHER OPÇÃO
# ============================================================

def escolher_opcao(numero):
    cena = SCENES[state["cena"]]
    opcoes = cena.get("options", [])
    indice = numero - 1

    if indice < len(opcoes):
        executar_acao(opcoes[indice][1])


# ============================================================
# BOTÕES
# ============================================================

@when("click", "#opcao1")
def clicar_opcao1(event):
    escolher_opcao(1)


@when("click", "#opcao2")
def clicar_opcao2(event):
    escolher_opcao(2)


@when("click", "#opcao3")
def clicar_opcao3(event):
    escolher_opcao(3)


@when("click", "#opcao4")
def clicar_opcao4(event):
    escolher_opcao(4)


@when("click", "#reiniciar")
def reiniciar(event):
    state["vida"] = CONFIG["vida_inicial"]
    state["inventario"] = []
    state["pontos"] = CONFIG["pontos_iniciais"]
    state["cena"] = CONFIG["cena_inicial"]
    state["cena_anterior"] = CONFIG["cena_inicial"]

    state["assassino_alertado"] = False
    state["gerador_ligado"] = False
    state["sobrevivente_salvo"] = False
    state["radio_ajuda"] = False
    state["fita_assistida"] = False

    trilha = CONFIG.get("trilha_inicial")

    if trilha:
        trocar_audio(trilha)

    mostrar_cena(CONFIG["cena_inicial"], permitir_evento=False)


# ============================================================
# INICIALIZAÇÃO
# ============================================================

configurar_identidade()
mostrar_cena(CONFIG["cena_inicial"], permitir_evento=False)
el("botao-iniciar").disabled = False
el("botao-iniciar").innerText = "▶ INICIAR JOGO"
