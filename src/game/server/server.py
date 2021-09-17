from .game_queue import Queue
from .game import Game
import socket
import sys
from _thread import *

class Server:
    def __init__(self, ip, port):
        self.ip = ip#ip de escuta
        self.port = port#porta de escuta
        self.queue = Queue()#fila de jogos em espera "matchmaking"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#socket

    def serve(self):
        """
        Tenta criar o servidor. Aborta o programa caso ocorra algum erro
        """
        try:
            
            self.socket.bind((self.ip, self.port))#inicia a conexão na porta informada
            self.socket.listen()
            print("Servidor iniciado em {}:{}".format(self.ip, self.port))
   
            while(True):
                print(server.queue)
                conn, address = self.socket.accept()
                print("Nova conexão de : {}".format(address))
                start_new_thread(self.start_or_queue_game, (conn, address))#joga essa conexão pra uma nova thread

        except socket.error:
            sys.exit("Não foi possível criar a conexão. Execução interrompida.")  
    
    def start_or_queue_game(self, conn, address):
        """
        Essa função é responsavel por enfileira um jogo
        ou criar ele. 
        """
        if len(self.queue) > 0:
            #já tinha um jogo na fila
            #inicia o jogo
            game = self.queue.get_game() 
            game.add_player(conn, address)#adiciona o jogador 2 no jogo
            game.start()#inicia o jogo
        else:
            #vai criar um novo jogo
            #coloca o jogo na fila
            game = Game()#cria um jogo 
            game.add_player(conn, address)#adiciona o primeiro jogador
            self.queue.add_game(game)#coloca  jogo na fila
            game.wait()#coloca o jogador em espera
    
    def close_server(self):
        """
        Essa função fecha o socket do servidor
        """
        self.socket.close()
    
def get_port(argv = ""):
    """
    Obtem o  a porta informada na linha de comando
    Se não for informado na linha de comando o padrão é
    porta 7455
    """
    
    port = 7455
    if(len(argv)>1):#se mais de um comando for informado
        args = argv[1:]
        for arg in args:
            unpack = arg.split("=")#separa por =
            if(len(unpack) > 1):
                if unpack[0] == "port":
                    port = int(unpack[1])

    return port

if __name__ == "__main__":
    port = get_port(sys.argv)
    server = Server('localhost', port)
    server.serve()
    server.close_server()