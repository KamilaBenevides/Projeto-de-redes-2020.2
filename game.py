class Game:
    P1 = 0
    P2 = 1
    
    def __init__(self, player1 = None, player2 = None):
        self.player1 = player1
        self.player2 = player2
        self.board =  [
                [-1, -1, -1],
                [-1, -1, -1],
                [-1, -1, -1]]
        self.winner = None
        self.p1_mark = 1
        self.p2_mark = 2
        self.turn = self.P1
    
    def set_mark(self, idx_i, idx_j):
        if (0 <= idx_i <= 2) and (0 <= idx_j <= 2) :
            if self.board[idx_i][idx_j] == -1:
                self.board[idx_i][idx_j] = self.get_pmark()
                self.change_turn()
            else:
                raise Exception('A posição fornecida já está preenchida.')
        else:
            raise Exception('Índice inválido.')

    def get_pmark(self):
        return self.p1_mark if (self.turn == self.P1) else self.p2_mark
    
    def change_turn(self):
        if self.turn == self.P1:
            self.turn = self.P2
        else:
            self.turn = self.P1
    
    def check_winner(self, tgt):
        board = self.board
        return ( board[0][0] == tgt and board[0][1] == tgt and board[0][2] == tgt ) or\
        (board[1][0] == tgt and board[1][1] == tgt and board[1][2] == tgt ) or \
        (board[2][0] == tgt and board[2][1] == tgt and board[2][2] == tgt) or \
        (board[0][0] == tgt and board[1][0] == tgt and board[2][0] == tgt ) or \
        (board[0][1] == tgt and board[1][1] == tgt and board[2][1] == tgt ) or \
        (board[0][2] == tgt and board[1][2] == tgt and board[2][2] == tgt ) or \
        (board[0][0] == tgt and board[1][1] == tgt and board[2][2] == tgt ) or \
        (board[0][2] == tgt and board[1][1] == tgt and board[2][0] == tgt )

