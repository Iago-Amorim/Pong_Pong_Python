import socket
from threading import Thread
import time
import pygame
from pygame.locals import *
import os

os.system("cls")

HOST = "127.0.0.1"
PORT = 50000

# Conectar com o servidor
Cliente_Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Cliente_Server.connect((HOST, PORT))

# Saber qual é o numero do jogador
Sou_Jogador = eval(Cliente_Server.recv(1024).decode())
Sou_Jogador = Sou_Jogador["Sou_o_jogador"]

pygame.init() # Iniciar pygame
TELA = pygame.display.set_mode((600, 330)) # Tamanho da tela
pygame.display.set_caption(("Jogador " + str(Sou_Jogador))) # Nome da Tela
FPS = 20 # Frames do jogo
clock = pygame.time.Clock()

# Variaveis --------------

Posicao_Y_1 = 110
Posicao_Y_2 = 110

Adversario = "OFF"

Jogo_Rodando = False

Pontos_J_1 = 0
Pontos_J_2 = 0

# Bola
Pos_X_Bola = 295
Pos_Y_Bola = 145

Imprimir = {}
Texto_imprimir = True

# Variaveis Fim --------------

# Imprimir informações no terminal
def Imprimir_Informacao():
    while Texto_imprimir:
        global Imprimir
        
        os.system("cls")
        
        for Chave, Valor in Imprimir.items():
            print("{0}: {1}".format(Chave, Valor))
        
        time.sleep(0.5)

# Comandos do jogador
def Comandos():
    global Adversario, Imprimir, Jogo_Rodando
    global Posicao_Y_1, Posicao_Y_2
    global Pos_X_Bola, Pos_Y_Bola
    global Pontos_J_1, Pontos_J_2
    
    # Variavel para mandar ao servidor
    comando = {'Jogador': Sou_Jogador}
    
    # Botão de iniciar jogo
    if Adversario == "ON" and (not Jogo_Rodando):
        (Posicao_Mouse_X, Posicao_Mouse_Y) = pygame.mouse.get_pos()
        Mouse_Click = pygame.mouse.get_pressed()
        if (Posicao_Mouse_X >= 225 and Posicao_Mouse_X <= (225+140)):
            if (Posicao_Mouse_Y >= 150 and Posicao_Mouse_Y <= (150+40)):
                if Mouse_Click[0]:
                    comando['Jogar'] = True
    
    # Teclas de movimentação
    Tecla = pygame.key.get_pressed()
    if Tecla[pygame.K_w]:
        comando['Movimento'] = "W"
    elif Tecla[pygame.K_s]:
        comando['Movimento'] = "S"
        
    # Enviar comandos para o servidor
    Cliente_Server.sendall(str.encode(str(comando)))
    
    # Recebre comandos do servidor
    Comandos_Recebidos = eval(Cliente_Server.recv(1024).decode())
    Imprimir = Comandos_Recebidos # Imprimir as imformações
    
    Adversario = Comandos_Recebidos['Adversario'] # Verificar se o oponente esta on ou off
    
    Jogo_Rodando = Comandos_Recebidos['Jogo_Rodando'] # Verificar se a partida iniciou
    
    # Posição dos jogadores na tela
    try:
        if Sou_Jogador == 1:
            Posicao_Y_1 = Comandos_Recebidos['Posicao_Y_1']
            Posicao_Y_2 = Comandos_Recebidos['Posicao_Y_2']
        else:
            Posicao_Y_1 = Comandos_Recebidos['Posicao_Y_2']
            Posicao_Y_2 = Comandos_Recebidos['Posicao_Y_1']
    except KeyError:
        pass
    
    # Posição da Bola
    try:
        Pos_X_Bola = Comandos_Recebidos['Posicao_X_Bola']
        Pos_Y_Bola = Comandos_Recebidos['Posicao_Y_Bola']
    except KeyError:
        pass
    
    # Quantidade de pontos
    try:
        Pontos_J_1 = Comandos_Recebidos['Pontos_1']
        Pontos_J_2 = Comandos_Recebidos['Pontos_2']
    except KeyError:
        pass

# Para encerrar o jogo
def Fechar_Jogo():
    for event in pygame.event.get():
            if event.type == QUIT:
                global Texto_imprimir
                Texto_imprimir = False
                pygame.quit()
                exit()

# Para imprimir texto na tela             
class Texto:   
    def __init__(self, Tx, Ta, Cor, TPos_x, TPos_y): # texto, tamanho, cor, posição X e Y
        font = pygame.font.Font('freesansbold.ttf', Ta)   
        Texto_skin = font.render(Tx, True, Cor)
        TELA.blit(Texto_skin, (TPos_x,TPos_y))

# Cor do botão        
COR_Botao = (255,255,255)
COR_Letra_Botao = (0,0,0)

# Iniciar o texto no terminal
Texto_terminal = Thread(target=Imprimir_Informacao).start()

while True:
    clock.tick(FPS)
    Fechar_Jogo()

    TELA.fill((0,0,0))
    
    Comandos()
    
    # Efeito de mouse no botão
    if Adversario == "ON":
        (Posicao_Mouse_X, Posicao_Mouse_Y) = pygame.mouse.get_pos()
        if (Posicao_Mouse_X >= 225 and Posicao_Mouse_X <= (225+140)) :
            if (Posicao_Mouse_Y >= 150 and Posicao_Mouse_Y <= (150+40)):
                COR_Botao = (100,100,100)
                COR_Letra_Botao = (255,255,255)
        else:
            COR_Botao = (255,255,255)
            COR_Letra_Botao = (0,0,0)

    # Imprimir objetos na tela inicial
    Texto("PONG PONG", 40, (255,255,255), 175, 62)
    pygame.draw.rect(TELA, COR_Botao, (225,140,150,40))
    Texto("PLAY", 20, COR_Letra_Botao, 275, 152)
    if Sou_Jogador == 1:
        Texto(("JOGADOR 2: " + Adversario), 20, (255,255,255), 215, 195)
    else:
        Texto(("JOGADOR 1: " + Adversario), 20, (255,255,255), 220, 195)

    # Tela de partida
    while Jogo_Rodando: 
        clock.tick(FPS)
        Fechar_Jogo()   
        
        TELA.fill((0,0,0))
        
        Comandos()
        
        # Imprimir objetos na tela
        Jogador = pygame.draw.rect(TELA, (255,255,255), (20, Posicao_Y_1, 15, 80)) # Jogador 1
        Cpu = pygame.draw.rect(TELA, (255,255,255), (565, Posicao_Y_2, 15, 80)) # Jogador 2
        Bola = pygame.draw.rect(TELA, (255,255,255), (Pos_X_Bola, Pos_Y_Bola, 10, 10))
        pygame.draw.rect(TELA, (40,40,40), (0, 300, 600, 30))
        Texto(("JOGADOR 1: {}".format(Pontos_J_1)), 15, (255,255,255), 10, 310)
        Texto(("JOGADOR 2: {}".format(Pontos_J_2)), 15, (255,255,255), 470, 310)
    
        pygame.display.update()
        
    pygame.display.update()
