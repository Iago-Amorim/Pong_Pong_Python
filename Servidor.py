import socket
from threading import Thread
import time
import random
import pygame
from pygame.locals import *
import os

os.system("cls")

HOST = "localhost"
PORT = 50000

# Abrir servidor
Meu_Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Meu_Server.bind((HOST, PORT))
Meu_Server.listen()

# Informações nasicas do jogador
class Jogador_Registra:
    def __init__(self, jogador, conn, ender):
        self.Jogador = jogador
        self.Connect = conn
        self.Endereco = ender
        self.Pronto = False
        self.Posicao_Y = 110 
       
# Informações basicas da bola 
class Bola_Iniciar:
    def __init__(self):
        self.Posicao_Bola_X = 295
        self.Posicao_Bola_Y = 145
        self.Direcao_X = random.uniform(-1.0,1.0)
        if self.Direcao_X <= 0:
            self.Direcao_X = -1
        else:
            self.Direcao_X = 1
        self.Direcao_Y = random.uniform(-0.5,0.5)

# Variaveis ----------------

Jogadores_Cadastrados = [0, 0] # Guardar as informações dos jogadores

Jogo_Rodando = False # A partida começa

Bola = False # Guardar as informações da bola

Pontos_J_1 = 0 # Pontos Jogador 1
Pontos_J_2 = 0 # Pontos Jogador 2

# Variaveis Fim ----------------

# Reiniciar o jogo com bola e jogadores no centro
def Reiniciar():
    global Jogadores_Cadastrados
    global Bola
    
    Jogadores_Cadastrados[0].Posicao_Y = 110
    Jogadores_Cadastrados[1].Posicao_Y = 110
    Bola = Bola_Iniciar()

# Codigo do Jogador
def Jogador(Num, Num2):
    while True:
        global Jogo_Rodando, Jogadores_Cadastrados, Bola
        global Pontos_J_1, Pontos_J_2
        
        # Zerar os pontos quando os dois sairem
        if (not Jogadores_Cadastrados[Num-1]) and (not Jogadores_Cadastrados[Num2-1]):
            Pontos_J_1 = 0
            Pontos_J_2 = 0
        
        # Iniciar o Jogador
        if not Jogadores_Cadastrados[Num-1]:
            conn, ender = Meu_Server.accept() # Receber o Endereço
            Jogadores_Cadastrados[Num-1] = Jogador_Registra(Num, conn, ender) # Adicionar novo jogador
            conn.sendall(str.encode("{'Sou_o_jogador': " + str(Num) + "}")) # Enviar número do jogador
        else:
            try:
                Comando_Recebido = eval(conn.recv(1024).decode()) # Comandos recebido do jogador
                try:
                    if Comando_Recebido['Jogar']: # Verificar se o jogador esta pronto
                        Jogadores_Cadastrados[Num-1].Pronto = True
                except KeyError:
                    pass
                
                try:  # Movimento do jogador
                    if Jogo_Rodando:
                        if Comando_Recebido['Movimento'] == "W":
                            Jogadores_Cadastrados[Num-1].Posicao_Y -= 5 # Subir
                        elif Comando_Recebido['Movimento'] == "S":
                            Jogadores_Cadastrados[Num-1].Posicao_Y += 5 # Descer
                        
                        if Jogadores_Cadastrados[Num-1].Posicao_Y < 15: # Barreira Superior 
                            Jogadores_Cadastrados[Num-1].Posicao_Y = 15
                        elif Jogadores_Cadastrados[Num-1].Posicao_Y > 205: # Barreira Inferior
                            Jogadores_Cadastrados[Num-1].Posicao_Y = 205
                except KeyError:
                    pass
                
                Comandos_Enviar = {} # Variavel para manda os comandos aos jogadores
                
                # Avisar se o oponente esta conectado
                if not Jogadores_Cadastrados[Num2-1]:
                    Comandos_Enviar['Adversario'] = "OFF"
                else:
                    Comandos_Enviar['Adversario'] = "ON"
                    
                # Verificar se os dois jogadores estão prontos
                if Jogadores_Cadastrados[Num-1].Pronto and Jogadores_Cadastrados[Num2-1].Pronto:
                    Comandos_Enviar['Jogo_Rodando'] = True
                    if not Jogo_Rodando:
                        Bola = Bola_Iniciar()    
                        Jogo_Rodando = True
                else:
                    Comandos_Enviar['Jogo_Rodando'] = False
                    Bola = False
                    Jogo_Rodando = False

                if Jogo_Rodando:  
                    # posição dos jogadores
                    if Jogadores_Cadastrados[Num2-1]:
                        Comandos_Enviar['Posicao_Y_1'] = Jogadores_Cadastrados[Num-1].Posicao_Y
                        Comandos_Enviar['Posicao_Y_2'] = Jogadores_Cadastrados[Num2-1].Posicao_Y
                        
                    if Jogadores_Cadastrados[Num-1].Jogador == 1:
                        # Mudar a posição da bola
                        Bola.Posicao_Bola_X += 5 * Bola.Direcao_X
                        Bola.Posicao_Bola_Y += 5 * Bola.Direcao_Y
                        
                        # Limite inferior e superior
                        if Bola.Posicao_Bola_Y <= 10 or Bola.Posicao_Bola_Y >= 280:
                            Bola.Direcao_Y *= -1
                            
                        # Colisão jogador 1
                        if((Bola.Posicao_Bola_X <= 20 + 15) and ((Bola.Posicao_Bola_Y + 10 >= Jogadores_Cadastrados[Num-1].Posicao_Y) and (Bola.Posicao_Bola_Y <= Jogadores_Cadastrados[Num-1].Posicao_Y + 80))):
                            Bola.Direcao_Y = (((Bola.Posicao_Bola_Y + (10/2)) - (Jogadores_Cadastrados[Num-1].Posicao_Y + (80/2)))/16)
                            Bola.Direcao_X = 1     
                        
                        # Colisão jogador 2   
                        if((Bola.Posicao_Bola_X >= 565 - 15) and ((Bola.Posicao_Bola_Y + 10 >= Jogadores_Cadastrados[Num2-1].Posicao_Y) and (Bola.Posicao_Bola_Y <= Jogadores_Cadastrados[Num2-1].Posicao_Y + 80))):
                            Bola.Direcao_X = (((Bola.Posicao_Bola_Y + (10/2)) - (Jogadores_Cadastrados[Num2-1].Posicao_Y + (80/2)))/16)
                            Bola.Direcao_X = -1
                        
                        # Verificar vitoria e reiniciar a partida
                        if Bola.Posicao_Bola_X <= 5:
                            Pontos_J_2 += 1
                            Reiniciar()
                        elif Bola.Posicao_Bola_X >= 595:
                            Pontos_J_1 += 1
                            Reiniciar()
                  
                    # Enviar posição da bola
                    Comandos_Enviar['Posicao_X_Bola'] = int(Bola.Posicao_Bola_X)
                    Comandos_Enviar['Posicao_Y_Bola'] = int(Bola.Posicao_Bola_Y)
                    
                    # Enviar os pontos dos jogadores
                    Comandos_Enviar['Pontos_1'] = Pontos_J_1
                    Comandos_Enviar['Pontos_2'] = Pontos_J_2
                    
                conn.sendall(str.encode(str(Comandos_Enviar))) # enviar toda retorno
                
            except (ConnectionError, SyntaxError): # Em caso de erro não parar o thread
                Jogadores_Cadastrados[Num-1] = 0 # Remover o usuario
                if Jogadores_Cadastrados[Num2-1]: 
                    Jogadores_Cadastrados[Num2-1].Posicao_Y = 110 # Mover o adversario para a posição inicial
                    Jogadores_Cadastrados[Num2-1].Pronto = False # Voltar o botão do jogador adversario
                    Bola = False # Em caso de estar em jogo não marcar ponto extra

# INICIAR JOGADOR 1
def Jogador1():
    Jogador(1, 2)
Jogador_1 = Thread(target=Jogador1).start() # Codigo Jogador 1

# INICIAR JOGADOR 2
def Jogador2():
    Jogador(2, 1)
Jogador_2 = Thread(target=Jogador2).start() # Codigo Jogador 2

while True:
    # Mostrar quem esta conectado
    os.system("cls")
    print("Servidor:")
    if not Jogadores_Cadastrados[0]:
        print("   Jogador 1: OFF")
    else:
        print("   Jogador 1: ON")
    if not Jogadores_Cadastrados[1]:
        print("   Jogador 2: OFF")
    else:
        print("   Jogador 2: ON")
    if Jogo_Rodando:
        print("      Jogando: Sim")
    else:
        print("      Jogando: Não")
    time.sleep(3)
