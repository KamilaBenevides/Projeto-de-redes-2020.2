class Message:
    __INQUEUE__ = "INQUEUE"
    __START__ = "START"
    __YOURTURN__ = "YOURTURN"
    __OTHERTURN__ = "OTHERTURN"
    __WINNER__ = "WINNER"
    __LOSER__ = "LOSER"
    __OKAY__ = "OKAY"
    __DRAW__ = "DRAW"
    __REDO__ = "REDO"
    __MOVE__ = "MOVE"

    types = [__INQUEUE__,__START__, __YOURTURN__, __OTHERTURN__,
    __WINNER__, __LOSER__, __OKAY__, __DRAW__, __REDO__, __MOVE__]

    def __init__(self, message = ""):
        self.INQUEUE = False
        self.START = False
        self.YOURTURN = False
        self.OTHERTURN = False
        self.WINNER = False
        self.LOSER = False
        self.OKAY = False
        self.DRAW = False
        self.REDO = False
        self.MOVE = False

        self.idx_i = -1
        self.idx_j = -1
        if isinstance(message, str):
            message = message.split("\n")

            for msg in message:
                msg = msg.split(" ")
                if msg[0] in self.types:
                    self.__dict__[msg[0]] = True
                    if msg[0] == self.__MOVE__:
                        self.idx_i = int(msg[1])
                        self.idx_j = int(msg[2])
        else:
            raise Exception("Parametro message não é do tipo str.")
    
    def add_command(self, command):
        if command in self.types:
            self.__dict__[command] = True
    
    def set_index(self, idx_i, idx_j):
        self.idx_i = idx_i
        self.idx_j = idx_j

    def create_message(self):
        """
        Transforma a instância classe em uma string no formato de mensagem
        """
        msg = ""
        for type_ in self.types:
            if self.__dict__[type_] == True:#o tipo está ativo
                msg += type_
                if type_ == self.__MOVE__:#adiciona os movimentos
                    msg += " {0} {1}".format(self.idx_i, self.idx_j)
                msg += "\n"
        
        return msg