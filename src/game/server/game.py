import socket
from ..utils.message import Message

class Game:
    """
    Essa classe representa uma intancia de um jogo.
    Um jogo possuiu dois jogadores e só inicia quando 
    os dois jogadores forem encontrados.
    """
    P1 = 0#turno do primeiro jogador
    P2 = 1#turno do segundo jogador
    
    def __init__(self):
        """
        Inicia o jogo sem jogadores.
        Tabuleiro com todas as posições vazias.
        Inicia o jogo no turno do primeiro jogador
        """
        self.player1 = None 
        self.player2 = None
        
        self.board =  [
                [-1, -1, -1],
                [-1, -1, -1],
                [-1, -1, -1]]
        self.winner = None
        self.turn = self.P1
        self.pos_left = 9#tabuleiro inicia ocm 9 posições livres
    
    def set_mark(self, idx_i, idx_j):
        """
        Essa função adiciona a marca do jogador do turno no tabuleiro
        nas posições idx_i idx_j informadas.
        """
        if (0 <= idx_i <= 2) and (0 <= idx_j <= 2) :#valida os indices
            if self.board[idx_i][idx_j] == -1:#verifica se a posição está vazia
                self.board[idx_i][idx_j] = self.get_pmark()#adiciona a marcação
                self.pos_left -= 1#o tabuleiro agora tem -1 posição livr
            else:
                raise Exception('A posição fornecida já está preenchida.')
        else:
            raise Exception('Índice inválido.')

    def get_pmark(self) -> int:
        """
        Obtem a marca do jogador do turno
        """
        return self.player1.mark if (self.turn == self.P1) else self.player2.mark
    
    def change_turn(self):
        """
        Muda o turno do jogo.

        """
        if self.turn == self.P1:#se o turno for do jogador 1 muda pro 2
            self.turn = self.P2
        else:#se o turno for do jogador 2 muda pro 1
            self.turn = self.P1
    
    def check_winner(self, player) -> bool:
        """
        Checa se o jogador(player) informado venceu o jogo.
        Checa todas as combinações posiveis.
        """
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
        """
        Adiciona um jogador no jogo.
        """
        if self.player1 == None:#se o primeiro jogador não foi adicionado ainda
            self.player1 = Player(conn, address, mark = 0)#a marca do jogador 1 é 0
        elif self.player2 == None:#se o segundo jogador não foi adicionado ainda
            self.player2 = Player(conn, address, mark = 1)#a marca do jogador 2 é 1
        else:#todos os jogadores já foram adicionados
            raise Exception('Jogadores já definidos.')
    
    def start(self):
        """
        Inicia o jogo. Essa função é responsável por toda
        a execução do jogo.
        """
        if (self.player1 == None) or (self.player2 == None):#checa se todos os jogadores foram encontrados
            raise Exception("Os jogadores ainda não foram definidos.")
       
        #envia mensagem de começo de jogo pros jogadores
        msg = Message()
        msg.add_command(msg.__START__)
        msg.add_command(msg.__OKAY__)
        self.player1.conn.send(msg.create_message().encode())
        self.player2.conn.send(msg.create_message().encode())

        #identifica o jogador do primeiro turno e o que vai esperar
        player_turn, another_player = (self.player1, self.player2) if self.turn == self.P1 else (self.player2, self.player1)
        #player_turn.conn.setblocking(True)
        #another_player.conn.setblocking(True)
        win = False#ninguém venceu ainda
        draw = False#não deu empate
        while (not win) and (not draw):
            #envia mensagens de começo de turno
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

                #deu tudo certo no turno
                #prepara as mensagens de finalização de turno
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
        """
        Essa função envia uma mensagem de espera de fila pro jogador 1
        """
        if self.player1 == None:
            raise Exception("Player 1 não foi definidido.")
        msg = Message()
        msg.add_command(msg.__INQUEUE__)
        text = msg.create_message()
        self.player1.conn.send(text.encode())
        
class Player:
    """
    Essa classe represeta um jogador do jogo
    Contém seu socket e marcação no tabuleiro
    """
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
    