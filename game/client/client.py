from typing import Tuple
import pygame
from pygame.locals import *
import os
import socket
import sys 
from ..utils.message import Message

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pygame.init()
screen = pygame.display.set_mode((600,600))
pygame.display.set_caption('Jogo da Velha')

STATE = 'JOGANDO'
TURN = 'JOGADOR1'
CHOICE = 'X'
espaco = 0
points1 = 0
points2 = 0

boardMark = [
        0, 1, 2,
        3, 4, 5,
        6, 7, 8
]
positions = [
    [(150, 200), (251, 200), (352, 200)],
    [(150, 301), (251, 301), (352, 301)],
    [(150, 402), (251, 402), (352, 402)]]

clipping1 = Rect((150, 200), (100, 100))
clipping2 = Rect((251, 200), (100, 100))
clipping3 = Rect((352, 200), (100, 100))
clipping4 = Rect((150, 301), (100, 100))
clipping5 = Rect((251, 301), (100, 100))
clipping6 = Rect((352, 301), (100, 100))
clipping7 = Rect((150, 402), (100, 100))
clipping8 = Rect((251, 402), (100, 100))
clipping9 = Rect((352, 402), (100, 100))

clipping = [clipping1, clipping2, clipping3, clipping4, clipping5, 
                clipping6, clipping7, clipping8, clipping9 ]

quadro = [(150, 200), (251, 200), (352, 200),
        (150, 301), (251, 301), (352, 301),
        (150, 402), (251, 402), (352, 402),]
quadro_skin = pygame.Surface((100,100))
quadro_skin.fill((210,255,50))
arial = pygame.font.SysFont('arial', 35)

imgO = pygame.image.load('{}/client/resources/O.png'.format(BASE_DIR)).convert_alpha()
imgX = pygame.image.load('{}/client/resources/X.png'.format(BASE_DIR)).convert_alpha()
imgXR = pygame.transform.scale(imgX, (80,80))
imgOR = pygame.transform.scale(imgO, (80,80))

def draw_ask(pos,image):
        x,y = pos
        screen.blit(image, (x, y))

def position_test(event, mouse_pos):
    global clipping
    idx_i, idx_j = [-1, -1]

    for p in clipping:
        if event.type == MOUSEBUTTONDOWN and p.collidepoint(mouse_pos):
            if p == clipping1:
                idx_i, idx_j = 0, 0
                #confirmar(0, [200,250])
            if p == clipping2:
                idx_i, idx_j = 0, 1
                #confirmar(1, [300,250])
            if p == clipping3:
                idx_i, idx_j = 0, 2
                #confirmar(2, [400,250])
            if p == clipping4:
                idx_i, idx_j = 1, 0
                #confirmar(3, [200,350])
            if p == clipping5:
                idx_i, idx_j = 1, 1
                #confirmar(4, [300,350])
            if p == clipping6:
                idx_i, idx_j = 1, 2
                #confirmar(5, [400,350])
            if p == clipping7:
                idx_i, idx_j = 2, 0
                #confirmar(6, [200,450])
            if p == clipping8:
                idx_i, idx_j = 2, 1
                #confirmar(7, [300,450])
            if p == clipping9:
                idx_i, idx_j = 2, 2
                #confirmar(8, [400,450])
    return idx_i, idx_j

def confirmar(indice, pos):
        global CHOICE, TURN, espaco
        if boardMark[indice] == 'X':
               print("x") 
        elif boardMark[indice] == 'O':
                print("o") 
        else:
                boardMark[indice] = CHOICE
                draw_ask(pos)
                print(boardMark)
                if TURN == 'JOGADOR1':
                        TURN = 'JOGADOR2'
                else: TURN = 'JOGADOR1'
                espaco += 1

def test_winner(l):
        return ((boardMark[0] == l and boardMark[1] == l and boardMark[2] == l) or
        (boardMark[3] == l and boardMark[4] == l and boardMark[5] == l) or
        (boardMark[6] == l and boardMark[7] == l and boardMark[8] == l) or
        (boardMark[0] == l and boardMark[3] == l and boardMark[6] == l) or
        (boardMark[1] == l and boardMark[4] == l and boardMark[7] == l) or
        (boardMark[2] == l and boardMark[5] == l and boardMark[8] == l) or
        (boardMark[0] == l and boardMark[4] == l and boardMark[8] == l) or
        (boardMark[2] == l and boardMark[4] == l and boardMark[6] == l))

def text_winner(t):
        arial = pygame.font.SysFont('arial', 35)
        if t == 'V':
                mensagem_vitoria = arial.render('DEU VELHA!', True, (210,255,50), 0)
                screen.blit(mensagem_vitoria,(200,50))
        elif t == 'X':
                mensagem_vitoria = arial.render('JOGADOR X VENCEU!', True, (210,255,50), 0)
                screen.blit(mensagem_vitoria,(110,50))
        else:
                mensagem_vitoria = arial.render('JOGADOR O VENCEU!', True, (210,255,50), 0)
                screen.blit(mensagem_vitoria,(110,50))

def points(p1, p2):
        arial = pygame.font.SysFont('arial', 25)
        play1 = 'Jogador X = {}'.format(p1)
        play2 = 'Jogador O = {}'.format(p2)
        pl1 = arial.render(play1, True, (210,255,50))
        pl2 = arial.render(play2, True, (210,255,50))
        screen.blit(pl1,(10,520))
        screen.blit(pl2,(10,555))

def reset():
        global STATE, TURN, CHOICE, boardMark, espaco
        STATE = 'JOGANDO'
        TURN = 'JOGADOR1'
        CHOICE = 'X'
        espaco = 0
        boardMark = [
            0, 1, 2,
            3, 4, 5,
            6, 7, 8
        ]
        screen.fill(0)

def get_ip_port(argv = ""):
    ip = "localhost"
    port = 7455
    if(len(argv)>1):
        args = argv[1:]
        for arg in args:
            unpack = arg.split("=")
            if(len(unpack) > 1):
                if unpack[0] == "ip":
                    ip = unpack[1]
                elif unpack[0] == "port":
                    port = int(unpack[1])

    return [ip, port]

def game_start(socket:socket):
    text_pygame = arial.render('Você é o jogador X',True, (210,255,50), 0)
    screen.blit(text_pygame,(200,50))
    pygame.display.update()

    win = False
    draw = False
    lose = False
    yourturn = False

    while (not win) and (not draw) and (not lose):
        #inicio de turno
        msg = socket.recv(4096)
        msg = Message(msg.decode())

        if msg.OKAY:
            if msg.YOURTURN:
                text_pygame = arial.render('Você é o jogador X\nSeu turno',True, (210,255,50), 0)
                screen.blit(text_pygame,(200,50))

                yourturn= True
                selected_pos = False

                while not selected_pos:
                    mouse_pos = pygame.mouse.get_pos()
                    #points(points1, points2)
                    for event in pygame.event.get():
                            if event.type == QUIT:
                                    return None
                    if event.type == MOUSEBUTTONDOWN:
                        selected_pos = True
                        idx_i, idx_j = position_test(event, mouse_pos)
                    pygame.display.update()

                msg1 = Message()
                msg1.add_command(msg1.__MOVE__)
                msg1.set_index(idx_i, idx_j)
                
                socket.send(msg1.create_message().encode())    

            elif msg.OTHERTURN:
                yourturn = False
                text_pygame = arial.render('Você é o jogador X\nEsperando o outro jogador',True, (210,255,50), 0)
                screen.blit(text_pygame,(200,50))
                pygame.display.update()
            
            msg = socket.recv(4096)
            msg = Message(msg.decode())
            if msg.OKAY:
                pos = positions[msg.idx_i][msg.idx_j]
                if yourturn:
                    draw_ask(pos, imgXR)
                else:
                    draw_ask(pos, imgOR)
                if msg.WINNER:
                    win = True
                elif msg.LOSER:
                    lose = True
                elif msg.DRAW:
                    draw = True
            elif msg.REDO:
                text_pygame = arial.render('Você é o jogador X\nO jogador vai refazer a jogada',True, (210,255,50), 0)
                screen.blit(text_pygame,(200,50))
        elif msg.REDO:
            text_pygame = arial.render('Você é o jogador X\nO jogador vai refazer a jogada',True, (210,255,50), 0)
            screen.blit(text_pygame,(200,50))
        pygame.display.update()
    if win:
        text_winner('X')
        
    elif lose:
        text_winner('O')
    else:
        text_winner('V')
    pygame.display.update()
    while(True):
        for event in pygame.event.get():
            if event.type == QUIT:
                    return None


if __name__ == "__main__":
    ip, port = get_ip_port(sys.argv)
    
    
    for pos in quadro:
        screen.blit(quadro_skin,pos)
    

    print("Se conectando em {0}:{1}".format(ip, port))
    msg_conect = arial.render('Se conectando\n ao servidor em: {0}:{1}'.format(ip, port),
                                True, (210,255,50), 0)
    screen.blit(msg_conect,(200,50))
    pygame.display.update()
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect((ip, port))

    msg = socket.recv(4096)
    msg = Message(msg.decode())

    if msg.INQUEUE:
        print("Aguardando fila...".format(ip, port))
        msg_inqueue = arial.render('Aguardando jogador\n na fila',True, (210,255,50), 0)
        screen.blit(msg_inqueue,(200,50))
        pygame.display.update()
        msg = socket.recv(4096)
        msg = Message(msg.decode())
	
    if msg.START:
        print("Começando partida...".format(ip, port))
        msg_inqueue = arial.render('Começando partida',True, (210,255,50), 0)
        screen.blit(msg_inqueue,(200,50))
        pygame.display.update()
        game_start(socket)

    socket.close()
    pygame.quit()
