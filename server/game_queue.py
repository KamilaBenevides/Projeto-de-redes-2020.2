
from game import Game


class Queue:
    """
    Essa classe contém todos os jogos que estão em espera(na fila)
    Provê mecanismos de semaforos para ganarantir confiabilidade
    no funcionamento da fila entre threads
    """

    def __init__(self):
        self.queue = []
        self.locked = False
    
    def lock(self):
        if not self.locked:
            self.locked = True
        else:
            raise Exception('Operação inválida. Fila já bloqueada.')
    
    def unlock(self):
        if self.locked:
            self.locked = False
        else:
            raise Exception('Operação inválida. Fila já desbloqueada')
    
    def add_game(self, game : Game): 
        add = False
        
        while( not add):
            try:
                self.lock()
                self.queue.append(game)
                self.unlock()
                add = True
            except:
                pass
       
    
    def get_game(self) -> Game:
        if (len(self.queue) > 0):
            get = False
            game = None
            while(not get):
                try:
                    self.lock()
                    game =  self.queue.pop(0)
                    self.unlock()
                    get = True
                except:
                    pass
            return game
        else:
            raise Exception('Fila vazia. Impossível obter jogo.')
    
    def __len__(self):
        return len(self.queue)

    def __str__(self):
        return "Jogos na fila: {}".format(self.__len__())

if __name__ == '__main__':
    pass