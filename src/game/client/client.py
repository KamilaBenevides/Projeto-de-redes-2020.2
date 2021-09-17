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

#tabuleiro
boardMark = [
        0, 1, 2,
        3, 4, 5,
        6, 7, 8
]

#indices na matriz do servidor como posições
#da tela do cliente
positions = [
    [(150, 200), (251, 200), (352, 200)],
    [(150, 301), (251, 301), (352, 301)],
    [(150, 402), (251, 402), (352, 402)]]

#quadrados do tabuleiro do jogo
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

#quadro vazio do jogo
quadro = [(150, 200), (251, 200), (352, 200),
        (150, 301), (251, 301), (352, 301),
        (150, 402), (251, 402), (352, 402),]
quadro_skin = pygame.Surface((100,100))
quadro_skin.fill((210,255,50))

#fonte usada
arial = pygame.font.SysFont('arial', 35)

#imagens de X e O
imgO = pygame.image.load('{}/client/resources/O.png'.format(BASE_DIR)).convert_alpha()
imgX = pygame.image.load('{}/client/resources/X.png'.format(BASE_DIR)).convert_alpha()
imgXR = pygame.transform.scale(imgX, (80,80))
imgOR = pygame.transform.scale(imgO, (80,80))

def draw_ask(pos,image):
        x,y = pos
        screen.blit(image, (x, y))

def position_test(event, mouse_pos):
    """
    Essa função verifica em que posição o jogador clickou na tela
    e transforma em dois indices da matrix do jogo
    Essa matriz é mantida no servidor
    """
    global clipping
    idx_i, idx_j = [-1, -1]

    for p in clipping:
        #verifica qual foi o clipping clicado
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

def get_ip_port(argv = ""):
    """
    Obtem o ip e a porta informada na linha de comando
    Se não for informado na linha de comando o padrão é
    ip localhost na porta 7455
    """
    ip = "localhost"
    port = 7455
    if(len(argv)>1):#se mais de um comando for informado
        args = argv[1:]
        for arg in args:
            unpack = arg.split("=")#separa por =
            if(len(unpack) > 1):
                if unpack[0] == "ip":#se for ip
                    ip = unpack[1]
                elif unpack[0] == "port":
                    port = int(unpack[1])

    return [ip, port]

def game_start(socket:socket):
    """
    Essa função inicia e executa o jogo no lado do cliente
    """
    text_pygame = arial.render('Você é o jogador X',True, (210,255,50), 0)
    screen.blit(text_pygame,(200,50))
    pygame.display.update()

    #variaveis de controle
    win = False
    draw = False
    lose = False
    yourturn = False

    while (not win) and (not draw) and (not lose):
        #inicio de turno
        #recebe as mensagens de confirmação do servidor
        msg = socket.recv(4096)
        msg = Message(msg.decode())

        #se estiver tudo okay
        if msg.OKAY:
            #se for o turno desse cliente
            if msg.YOURTURN:
                text_pygame = arial.render('Você é o jogador X\nSeu turno',True, (210,255,50), 0)
                screen.blit(text_pygame,(200,50))

                yourturn= True#seta essa variavel pra desenhar o X depois
                selected_pos = False

                while not selected_pos:#aguarda o jogador clicar em algum lugar da tela
                    mouse_pos = pygame.mouse.get_pos()
                    #points(points1, points2)
                    for event in pygame.event.get():
                            if event.type == QUIT:#se o jogador clicar no X
                                    return None#sai da função start_game
                    if event.type == MOUSEBUTTONDOWN:#clicou no botão
                        selected_pos = True
                        idx_i, idx_j = position_test(event, mouse_pos)#obtem os indices da posição escolhida
                    pygame.display.update()

                #cria uma mensagem pra enviar ao servidor
                msg1 = Message()
                msg1.add_command(msg1.__MOVE__)#tipo MOVE
                msg1.set_index(idx_i, idx_j)#coloca os indices na mesnagem
                
                socket.send(msg1.create_message().encode())#envia ao servidor    

            #se for o turno do outro cliente
            elif msg.OTHERTURN:
                yourturn = False#seta essa variavel pra desenhar o O depois
                text_pygame = arial.render('Você é o jogador X\nEsperando o outro jogador',True, (210,255,50), 0)
                screen.blit(text_pygame,(200,50))
                pygame.display.update()
            
            #recebe a mensagem de fim de turno do servidor
            #essa mensagem é um MOVE
            msg = socket.recv(4096)
            msg = Message(msg.decode())
            #se estiver tudo okay
            if msg.OKAY:
                pos = positions[msg.idx_i][msg.idx_j]#obtem as posições na tela
                #do MOVE que o servidor enviou
                if yourturn:#se for o turno desse jogador
                    draw_ask(pos, imgXR)#desenha um X
                else:
                    draw_ask(pos, imgOR)#desenha um O
                if msg.WINNER:#se esse cliente venceu
                    win = True
                elif msg.LOSER:#se esse cliente perdeu
                    lose = True
                elif msg.DRAW:#se foi empate
                    draw = True
            #algum dos clientes fez algo de errado
            elif msg.REDO:
                #o próximo turno continua de onde o jogo parou
                text_pygame = arial.render('Você é o jogador X\nO jogador vai refazer a jogada',True, (210,255,50), 0)
                screen.blit(text_pygame,(200,50))
        #algum dos clientes fez algo de errado
        elif msg.REDO:
            text_pygame = arial.render('Você é o jogador X\nO jogador vai refazer a jogada',True, (210,255,50), 0)
            screen.blit(text_pygame,(200,50))
        pygame.display.update()
    if win:#cliente venceu
        text_winner('X')
    elif lose:#cliente perdeu
        text_winner('O')
    else:#empat
        text_winner('V')
    pygame.display.update()
    while(True):#aguarda o jogador clicar no botão de fechar a janela
        for event in pygame.event.get():
            if event.type == QUIT:
                    return None


if __name__ == "__main__":
    ip, port = get_ip_port(sys.argv)#obtem o ip e a porta do servidor
    
    
    for pos in quadro:#desenha o quadro vazio na tela
        screen.blit(quadro_skin,pos)
    

    print("Se conectando em {0}:{1}".format(ip, port))
    msg_conect = arial.render('Se conectando\n ao servidor em: {0}:{1}'.format(ip, port),
                                True, (210,255,50), 0)
    screen.blit(msg_conect,(200,50))
    pygame.display.update()
    #tenta se conectar com os servidor
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect((ip, port))

    #obtem o status do jogo do servidor
    msg = socket.recv(4096)
    msg = Message(msg.decode())

    if msg.INQUEUE:#aguarda na fila
        print("Aguardando fila...".format(ip, port))
        msg_inqueue = arial.render('Aguardando jogador\n na fila',True, (210,255,50), 0)
        screen.blit(msg_inqueue,(200,50))
        pygame.display.update()
        msg = socket.recv(4096)#aguarda a resposta do servidor
        msg = Message(msg.decode())
	
    if msg.START:#inicia o jogo
        print("Começando partida...".format(ip, port))
        msg_inqueue = arial.render('Começando partida',True, (210,255,50), 0)
        screen.blit(msg_inqueue,(200,50))
        pygame.display.update()
        game_start(socket)#inicica o jogo

    socket.close()#encerra a conexão com o servidor
    pygame.quit()#finaliza o pygame
