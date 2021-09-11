from typing import Tuple
import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((600,600))
pygame.display.set_caption('Game of old')

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



def draw_ask(pos):
        global TURN
        x,y = pos
        if TURN == 'JOGADOR2':
                imgO = pygame.image.load('O.png').convert_alpha()
                imgOR = pygame.transform.scale(imgO, (80,80))
                screen.blit(imgOR, (x-50, y-50))
        else:
                imgX = pygame.image.load('X.png').convert_alpha()
                imgXR = pygame.transform.scale(imgX, (80,80))
                screen.blit(imgXR, (x-50, y-50))

def position_test():
        for p in clipping:
                if event.type == MOUSEBUTTONDOWN and p.collidepoint(mouse_pos):
                        if p == clipping1:
                                confirmar(0, [200,250])
                        if p == clipping2:
                                confirmar(1, [300,250])
                        if p == clipping3:
                                confirmar(2, [400,250])
                        if p == clipping4:
                                confirmar(3, [200,350])
                        if p == clipping5:
                                confirmar(4, [300,350])
                        if p == clipping6:
                                confirmar(5, [400,350])
                        if p == clipping7:
                                confirmar(6, [200,450])
                        if p == clipping8:
                                confirmar(7, [300,450])
                        if p == clipping9:
                                confirmar(8, [400,450])
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

def reset(): #inicia novamente
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
for pos in quadro:
        screen.blit(quadro_skin,pos)
while True:
        mouse_pos = pygame.mouse.get_pos()
        if STATE == 'JOGANDO':
                points(points1, points2)
                for event in pygame.event.get():
                        if event.type == QUIT:
                                pygame.quit()

                if event.type == MOUSEBUTTONDOWN:
                        if TURN == 'JOGADOR1':
                                CHOICE = 'X'
                                position_test()
                        else:
                                CHOICE = 'O'
                                position_test()
                if test_winner('X'):
                        text_winner('X')
                        STATE = 'RESET'
                        points1 += 1
                elif test_winner('O'):
                        text_winner('O')
                        STATE = 'RESET'
                        points2 += 1
                elif espaco >= 9:
                        text_winner('V')
                        STATE = 'RESET'
        else:
                for u in pygame.event.get():
                        if u.type == QUIT:
                                pygame.quit()
                                exit()
                        if u.type == MOUSEBUTTONDOWN:
                                reset()
                                for pos in quadro:
                                        screen.blit(quadro_skin,pos)
                        
        pygame.display.update()