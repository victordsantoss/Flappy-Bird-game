import pyxel
from random import randint 

def desenhar_fundo ():
    # Cor de fundo 
    pyxel.cls (12)

def desenhar_chao ():
    # Posições dos blocos no eixo X
    x1 = (pyxel.frame_count * -1) % largura_tela
    x2 = (pyxel.frame_count * -1) % largura_tela - largura_tela
    y = altura_tela - 16
    
    # Posição do ladrilho no tilemap (Uma imagem formada pela repetição de várias outras)
    i = 0
    j = 0

    # Número de ladrilhos usados na largura e altura da imagem
    largura = 32
    altura = 2    
    pyxel.bltm (x1, y, 0, i, j, largura, altura)
    pyxel.bltm (x2, y, 0, i, j, largura, altura)

def desenhar_instrucoes ():
    cor = 7

    if morto:
        msg = "Precione R para reinciar"
    elif ativo:
        msg = str (score)
    else:
        msg =  "SPACE para INICIAR"
        
    largura_texto = pyxel.FONT_WIDTH * len (msg)
    x = largura_tela / 2 - largura_texto / 2
    y = altura_tela /3
    pyxel.text (x, y, msg, cor)

def desenhar_canos ():
    img = 1
    u = 0 
    v = 0 
    largura = 25
    altura = 135
    cor = 0
    for x, y in canos:
        pyxel.blt (x, y, img, u, v, largura, altura, cor)
        pyxel.blt (x, y + abertura_cano, img, u, v, largura, -altura, cor) 

def desenhar_nuvens ():
    # Deslocamento base em x
    x = (pyxel.frame_count * -1) / 2

    # Largura da nuvem e tamanho do intervalo a ser percorrido e cada ciclo
    largura_nuvem = 32
    altura_nuvem = 32
    largura_maxima = largura_tela + largura_nuvem

    # Posições de cada nuvem 
    x1 = (x + largura_tela * 0.25) % largura_maxima - largura_nuvem
    y1 = altura_tela / 2
    x2 = (x + largura_tela * 0.50) % largura_maxima - largura_nuvem
    y2 = altura_tela  / 4
    x3 = (x + largura_maxima * 0.75) % largura_maxima - largura_nuvem
    y3 = altura_nuvem / 1.5

    pyxel.blt (x1, y1, 2, 0, 16, largura_nuvem, altura_nuvem, 12)
    pyxel.blt (x2, y2, 2, 0, 48, largura_nuvem, altura_nuvem, 12)
    pyxel.blt (x3, y3, 2, 0, 80, largura_nuvem, altura_nuvem, 12)

def desenhar_flappy ():

    global flappy_x, flappy_y, inicio

    # Muda a imagem do bird a cada 4 frames 
    frame = (pyxel.frame_count // 4) % 3

    # Posição inicial no pixelEditor (Define quais das 3 imagens serão usadas)
    u = 0
    v = frame * 16
    
    # Indice da imagem no pixel editor (passaro, nuvens, obstáculos)
    img = 0
    largura = 17
    altura = 13
    mascara = 0

    if inicio == False:
        flappy_x = largura_tela / 2
        flappy_y = altura_tela / 2

    # Função responsável por desenhar o bird que se encontra no PixelEditor
    pyxel.blt (flappy_x, flappy_y, img, u, v, largura, altura, mascara)

def atualizar_flappy ():
    global velocidade, flappy_x, flappy_y, gravidade

    pulando = pyxel.btnp (pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_UP)
    
    # Atualiza a velocidade
    velocidade += gravidade

    # Verifica se está pulando antes de atualizar a posição
    if pulando and not morto:
        velocidade = -pulo
         
   # Atualiza a posição
    flappy_y += velocidade
    
    if flappy_y > altura_tela - 29:
        flappy_y = altura_tela - 29

    if morto:
        flappy_x -= 1

def atualizar_canos ():
    global distancia_canos
    
    i = 0
    for x, y in canos:
        if x < -30:
            x = x + distancia_canos * 4
            y = -10 * randint (1,8)
        canos[i] = x -1, y
        i += 1

def atualizar_colisoes ():
    global morto

    if flappy_y + 13 >= altura_tela - 16:
        morto = True

    for x, y in canos:
        colide_x = flappy_x + 17 > x and flappy_x < x + 25
        colide_y = flappy_y < y + 135 or flappy_y + 13 > y + abertura_cano
        if colide_x and colide_y:
            morto = True
    
def atualizar_score ():
    global score

    for x, y in canos:
        # Verifica se a posição do cano coincide com a do passarinho
        if flappy_x == x and not morto:
            score += 1

def restart_game ():
    global ativo, morto, flappy_x, flappy_y, velocidade, score, canos, distancia_canos, abertura_cano, pulo, gravidade, largura_tela, altura_tela, inicio
    
    # Tela 
    largura_tela = 150
    altura_tela = 255

    # Pássaro
    flappy_x = largura_tela / 3
    flappy_y = largura_tela / 2
    pulo = 8
    gravidade = 1
    velocidade = 0

    # Estado de Jogo 
    ativo = False
    morto = False
    score = 0
    inicio = False

    # Cria canos 
    distancia_canos = 80
    abertura_cano = 200
    cano1 = largura_tela + distancia_canos * 0, -10 * randint (1, 8)
    cano2 = largura_tela + distancia_canos * 1, -10 * randint (1, 8)
    cano3 = largura_tela + distancia_canos * 2, -10 * randint (1, 8)
    cano4 = largura_tela + distancia_canos * 3, -10 * randint (1, 8)
    canos = [cano1, cano2, cano3, cano4]

def desenhar ():
    desenhar_fundo ()
    desenhar_nuvens ()
    desenhar_canos ()
    desenhar_chao ()
    desenhar_flappy ()
    desenhar_instrucoes ()

def atualizar_jogo ():
    atualizar_flappy ()
    atualizar_canos ()
    atualizar_colisoes ()
    atualizar_score ()

def atualizar ():
    global ativo, inicio

    if pyxel.btnp (pyxel.KEY_Q):
        pyxel.quit ()
    elif pyxel.btnp (pyxel.KEY_R):
        restart_game ()
    elif ativo:
        atualizar_jogo ()
    elif pyxel.btnp (pyxel.KEY_SPACE) or pyxel.btnp (pyxel.KEY_UP):
        inicio = True
        ativo = True

# Inicializar o jogo
restart_game ()
pyxel.init (largura_tela, altura_tela, fps = 35)
pyxel.load ("data.pyxres")
pyxel.run (atualizar, desenhar)