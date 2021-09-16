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
            #i = 0
            self.socket.bind((self.ip, self.port))
            self.socket.listen()
            print("Servidor iniciado em {}:{}".format(self.ip, self.port))
   
            while(True):
                print(server.queue)
                conn, address = self.socket.accept()
                print("Nova conexão de : {}".format(address))
                start_new_thread(self.start_or_queue_game, (conn, address))
                
                #i += 1
                
                
        
        except socket.error:
            sys.exit("Não foi possível criar a conexão. Execução interrompida.")  
    
    def start_or_queue_game(self, conn, address):
        if len(self.queue) > 0:
            #já tinha um jogo na fila
            #inicia o jogo
            game = self.queue.get_game() 
            game.add_player(conn, address)
            game.start()
        else:
            #vai criar um novo jogo
            #coloca o jogo na fila
            game = Game()
            game.add_player(conn, address)
            self.queue.add_game(game)
            game.wait()
    
    def close_server(self):
        self.socket.close()
    
if __name__ == "__main__":
    server = Server('localhost', 7455)
    server.serve()
    server.close_server()