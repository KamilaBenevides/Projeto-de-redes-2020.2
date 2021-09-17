
from .game import Game


class Queue:
    """
    Essa classe contém todos os jogos que estão em espera(na fila)
    Provê mecanismos de semaforos para ganarantir confiabilidade
    no funcionamento da fila entre threads
    """

    def __init__(self):
        self.queue = []
        self.locked = False#serve como um semaforo
    
    def lock(self):
        #adiquire o bloqueio da fila
        if not self.locked:#se não estiver bloqueada
            self.locked = True
        else:
            raise Exception('Operação inválida. Fila já bloqueada.')
    
    def unlock(self):
        #desbloqueia a fila
        if self.locked:
            self.locked = False
        else:
            raise Exception('Operação inválida. Fila já desbloqueada')
    
    def add_game(self, game : Game): 
        """
        Essa função adiciona o jogo na fila.
        Fica esperando até a fila ser desbloqueada
        """
        add = False
        
        while( not add):#enquanto não tiver inserido
            try:#tenta inserir na fila
                self.lock()
                self.queue.append(game)
                self.unlock()
                add = True#inseriu
            except:
                pass
       
    
    def get_game(self) -> Game:
        """
        Essa função desinfileirar um jogo na fila.
        Fica esperando até a fila ser desbloqueada
        """
        if (len(self.queue) > 0):
            get = False
            game = None
            while(not get):#enquanto não tiver obtido o jogo
                try:
                    self.lock()
                    game =  self.queue.pop(0)
                    self.unlock()
                    get = True#obteu o jogo
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