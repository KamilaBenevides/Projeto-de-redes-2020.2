# Projeto de Redes de Computadores 2020.2
Para rodar a aplicação é necessário que o python esteja instalado.

Baixar a [versão do python](https://www.python.org/downloads/release/python-388/) usada: https://www.python.org/downloads/release/python-388/

No diretório ```game```, usar o comando para instalar as bibliotecas usadas:
```
pip install -r requirements.txt
```

### Rodar o servidor

No diretório ```src```, usar o comando para iniciar o servidor:

```
python -m game.server.server
```

O servidor vai ser iniciado no IP ```'localhost'``` e porta ```7455```.

É possível alterar o IP e porta de escuta passando os paramêtros ```ip``` e ```port``` na linha de comando.
Segue exemplo:

```
python -m game.server.server port=4648 ip=127.0.0.1
```

Nesse exemplo, o servidor vai iniciar no IP ```127.0.0.1``` e porta ```4648```.


### Rodar o cliente

No diretório ```src```, usar o comando para iniciar o cliente:

```
python -m game.client.client
```

O cliente vai ser iniciado e vai se conectar com o servidor no IP ```'localhost'``` e porta ```7455```.

É possível alterar o IP e a porta para se conectar passando os paramêtros ```ip``` e ```port``` na linha de comando.
Segue exemplo:

```
python -m game.client.client ip=127.168.99.1 port=5555
```

Nesse exemplo, o cliente vai se conectar com o servidor no IP ```127.168.99.1``` e porta ```5555```.
