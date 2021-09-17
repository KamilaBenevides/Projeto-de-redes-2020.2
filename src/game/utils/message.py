class Message:
    """
    Essa classe serve para facilitar a troca de mensagens entre o cliente e o servidor
    """
    #tipos de mensagens/comandos
    __INQUEUE__ = "INQUEUE"#jogador em fila
    __START__ = "START"#jogo começou
    __YOURTURN__ = "YOURTURN"#turno do jogador
    __OTHERTURN__ = "OTHERTURN"#turno do outro jogador
    __WINNER__ = "WINNER"#jogador venceu
    __LOSER__ = "LOSER"#jogador perdeu
    __OKAY__ = "OKAY"#tudo certo com a requisição
    __DRAW__ = "DRAW"#jogo deu empate
    __REDO__ = "REDO"#refazer o movimento do jogador
    __MOVE__ = "MOVE"#movimento do jogador

    #lista de tipos
    types = [__INQUEUE__,__START__, __YOURTURN__, __OTHERTURN__,
    __WINNER__, __LOSER__, __OKAY__, __DRAW__, __REDO__, __MOVE__]

    def __init__(self, message = ""):
        """
        Essa função incializa a mensagem recebida ou que vai ser enviada
        Se message não for uma string vazia, o texto é analisado e os 
        comandos presentes no texto são ativados
        Os comandos devem ser separados por quebra de linha
        """
        #incializa a classe com todos os comandos desativados
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

        self.idx_i = -1#as posições do movimentos são inválidas
        self.idx_j = -1#as posições do movimentos são inválidas
        if isinstance(message, str):
            message = message.split("\n")#separa a string por comandos

            for msg in message:
                msg = msg.split(" ")#separa o comando por espaços
                if msg[0] in self.types:#se for um comando válido
                    self.__dict__[msg[0]] = True#ativa ele
                    if msg[0] == self.__MOVE__:#se for um comando de movimento
                        #analise os índices
                        self.idx_i = int(msg[1])
                        self.idx_j = int(msg[2])
        else:
            raise Exception("Parametro message não é do tipo str.")
    
    def add_command(self, command):
        """
        Essa função ativa o comando(commando)
        informado na mensagem
        """
        if command in self.types:#verifica se é um comando válido
            self.__dict__[command] = True
    
    def set_index(self, idx_i, idx_j):
        """
        Essa função configura os índices informados
        na mensagem
        """
        self.idx_i = idx_i
        self.idx_j = idx_j

    def create_message(self):
        """
        Transforma a instância classe em uma string no formato de mensagem
        """
        msg = ""
        for type_ in self.types:
            if self.__dict__[type_] == True:#o tipo está ativo
                msg += type_#concatena o tipo
                if type_ == self.__MOVE__:#adiciona os movimentos
                    msg += " {0} {1}".format(self.idx_i, self.idx_j)
                msg += "\n"#concatena a quebra de linha
        
        return msg