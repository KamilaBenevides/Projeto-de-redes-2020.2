import socket

class Game:
    P1 = 0
    P2 = 1
    
    def __init__(self):
        self.player1 = None 
        self.player2 = None
        
        self.board =  [
                [-1, -1, -1],
                [-1, -1, -1],
                [-1, -1, -1]]
        self.winner = None
        self.turn = self.P1
        self.pos_left = 9
    
    def set_mark(self, idx_i, idx_j):
        if (0 <= idx_i <= 2) and (0 <= idx_j <= 2) :
            if self.board[idx_i][idx_j] == -1:
                self.board[idx_i][idx_j] = self.get_pmark()
                self.pos_left -= 1
            else:
                raise Exception('A posição fornecida já está preenchida.')
        else:
            raise Exception('Índice inválido.')

    def get_pmark(self) -> int:
        return self.player1.mark if (self.turn == self.P1) else self.player2.mark
    
    def change_turn(self):
        if self.turn == self.P1:
            self.turn = self.P2
        else:
            self.turn = self.P1
    
    def check_winner(self, player) -> bool:
        board = self.board
        return ( board[0][0] == player.mark and board[0][1] == player.mark and board[0][2] == player.mark ) or\
        (board[1][0] == player.mark and board[1][1] == player.mark and board[1][2] == player.mark ) or \
        (board[2][0] == player.mark and board[2][1] == player.mark and board[2][2] == player.mark) or \
        (board[0][0] == player.mark and board[1][0] == player.mark and board[2][0] == player.mark ) or \
        (board[0][1] == player.mark and board[1][1] == player.mark and board[2][1] == player.mark ) or \
        (board[0][2] == player.mark and board[1][2] == player.mark and board[2][2] == player.mark ) or \
        (board[0][0] == player.mark and board[1][1] == player.mark and board[2][2] == player.mark ) or \
        (board[0][2] == player.mark and board[1][1] == player.mark and board[2][0] == player.mark )

    def add_player(self, conn, address):
        if self.player1 == None:
            self.player1 = Player(conn, address, mark = 0)
        elif self.player2 == None:
            self.player2 = Player(conn, address, mark = 1)
        else:
            raise Exception('Jogadores já definidos.')
    
    def start(self):
        if (self.player1 == None) or (self.player2 == None):
            raise Exception("Os jogadores ainda não foram definidos.")
        
        msg = "START\n"
        self.player1.conn.send(msg.encode())
        self.player2.conn.send(msg.encode())

        player_turn, another_player = (self.player1, self.player2) if self.turn == self.P1 else (self.player2, self.player1)
        player_turn.setblocking(True)
        another_player.setblocking(True)
        win = False
        draw = False
        while (not win) and (not draw):
            try:
                # ---------- Envia mensagem de preparação de turno -------------
                msg1 = "YOUTURN\n"
                msg2 = "OTHERTURN\n"
                
                player_turn.conn.send(msg1.encode())
                another_player.conn.send(msg2.encode())

                # ---------- Recebe movimentos do jogador do turno -------------
                move = player_turn.conn.recv(4096)
                command, idx_i, idx_j = move.split(" ")#recebe mensagem: MOVE num1 num2
                self.set_mark(int(idx_i), int(idx_j))

                # ------ Envia mensagens pros jogadores sobre ações tomadas nesse turno 
                msg1 = ""
                msg2 = ""
                if(self.check_winner(player_turn)):
                    #jogador venceu a partida
                    msg1 = "WINNER\n"
                    msg2 = "LOSER\n"
                    win = True
                elif self.pos_left == 0:
                    #deu empate
                    msg1 = "DRAW\n"
                    msg2 = "DRAW\n"
                    draw = True
                
                msg1 += "OKAY\n"
                msg2 += "MOVE: {} {}\n".format(idx_i, idx_j)

                player_turn.conn.send(msg1.encode())
                another_player.conn.send(msg2.encode())#envia ao outro jogador qual foi posição jogada
                
                #---------- Muda o turno
                
                self.change_turn()
                #troca simples de contéudo de variáveis
                aux = player_turn
                player_turn = another_player
                another_player = aux

            except:
                #ocorreu algum erro
                #o jogador precisa refazer seu turno
                #envia comandos para os jogadores
                msg1 = "REDO\n"
                msg2 = "REDO\n"
                
                player_turn.conn.send(msg1.encode())
                another_player.conn.send(msg2.encode())



    def wait(self):
        if self.player1 == None:
            raise Exception("Player 1 não foi definidido.")
        
        msg = "INQUEUE\n"
        self.player1.conn.send(msg.encode())
        
class Player:
    def __init__(self, conn : socket.socket, address: tuple, mark = 0):
        self.conn = conn
        self.address = address
        self.mark = mark

class Message:
    types = ['INQUEUE','START', 'YOURTURN', 'OTHERTURN',
     'WINNER', 'LOSER', 'OKAY', 'DRAW', 'REDO', 'MOVE']
    def __init__(self, type, **kwargs):
        if type not in self.types:
            raise Exception("O tipo de mensagem informado não é suportado.")
        self.type = type
        if self.type == "MOVE":
            self.idx_i = kwargs["idx_i"]
            self.idx_j = kwargs["idx_j"]