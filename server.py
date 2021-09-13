from .queue import Queue
from.game import Game
import socket
import sys

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
            self.socket.server_socket.bind((self.ip, self.port))
            self.socket.listen()
        except socket.error:
            sys.exit("Não foi possível criar a conexão. Execução interrompida.")  
    
    def put_game_queue(self, conn):
        added = False
        game = Game(player1 = conn)
        while(not added):

            try:
                self.queue.add_game(game)
                added = True
            except:
                pass
    

