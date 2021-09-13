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
    
    def add_game(self, game):
        while(self.locked):
            pass
        self.lock()
        self.queue.append(game)
        self.unlock()
    
    def get_game(self):
        if (len(self.queue) > 0):
            while(self.locked):
                pass
            self.lock()
            game =  self.queue.pop(0)
            self.unlock()
            return game
        else:
            raise Exception('Fila vazia. Impossível obter jogo.')
    
    def __len__(self):
        return len(self.queue)

