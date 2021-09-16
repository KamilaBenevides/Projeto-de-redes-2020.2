import socket
from ..utils.message import Message

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
       
        msg = Message()
        msg.add_command(msg.__START__)
        msg.add_command(msg.__OKAY__)
        self.player1.conn.send(msg.create_message().encode())
        self.player2.conn.send(msg.create_message().encode())

        player_turn, another_player = (self.player1, self.player2) if self.turn == self.P1 else (self.player2, self.player1)
        #player_turn.conn.setblocking(True)
        #another_player.conn.setblocking(True)
        win = False
        draw = False
        while (not win) and (not draw):
            msg1 = Message()
            msg2 = Message()
            msg1.add_command(msg1.__YOURTURN__)
            msg2.add_command(msg2.__OTHERTURN__)
            msg1.add_command(msg1.__OKAY__)
            msg2.add_command(msg2.__OKAY__)
            try:
                # ---------- Envia mensagem de preparação de turno -------------
                player_turn.conn.send(msg1.create_message().encode())
                another_player.conn.send(msg2.create_message().encode())

                # ---------- Recebe movimentos do jogador do turno -------------
                move = player_turn.conn.recv(4096)
                msg = Message(move.decode())
                if not msg.MOVE:
                    raise Exception()
                
                self.set_mark(msg.idx_i, msg.idx_j)

                msg1 = Message()
                msg2 = Message()
                msg1.add_command(msg1.__YOURTURN__)
                msg2.add_command(msg2.__OTHERTURN__)
                # ------ Envia mensagens pros jogadores sobre ações tomadas nesse turno 
                if(self.check_winner(player_turn)):
                    #jogador venceu a partida
                    msg1.add_command(msg1.__WINNER__)
                    msg2.add_command(msg2.__LOSER__)
                    win = True
                elif self.pos_left == 0:
                    #deu empate
                    msg1.add_command(msg1.__DRAW__)
                    msg2.add_command(msg2.__DRAW__)
                    draw = True

                msg1.add_command(msg1.__OKAY__)
                msg2.add_command(msg2.__OKAY__)

                msg1.add_command(msg1.__MOVE__)
                msg2.add_command(msg2.__MOVE__)

                msg1.set_index(msg.idx_i, msg.idx_j)
                msg2.set_index(msg.idx_i, msg.idx_j)

                player_turn.conn.send(msg1.create_message().encode())
                another_player.conn.send(msg2.create_message().encode())#envia ao outro jogador qual foi posição jogada
                
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
                msg = Message()
                msg.add_command(msg.__REDO__)
                
                player_turn.conn.send(msg.create_message().encode())
                another_player.conn.send(msg.create_message().encode())



    def wait(self):
        if self.player1 == None:
            raise Exception("Player 1 não foi definidido.")
        msg = Message()
        msg.add_command(msg.__INQUEUE__)
        text = msg.create_message()
        self.player1.conn.send(text.encode())
        
class Player:
    def __init__(self, conn : socket.socket, address: tuple, mark = 0):
        self.conn = conn
        self.address = address
        self.mark = mark



if __name__ == "__main__":
    #testes
    
    msg = "MOVE 1 2\nSTART\n"
    message = Message()
    print(message.MOVE, message.idx_i, message.idx_j)
    print(message.START)
    print(message.create_message())

    game = Game()
    game.wait()
    