import socket
import threading
import time
import datetime

HOST = ''
PORT_TCP = 5000
PORT_UDP = 5001
LOG_FILE = 'server_log.txt'

conexoes = {}

def registrar_log(mensagem):
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f'{datetime.datetime.now()} - {mensagem}\n')

def processar_comando(comando, endereco):
    comando = comando.strip().lower()
    if comando == 'date':
        return str(datetime.datetime.now())
    elif comando == 'uptime':
        tempo_atividade = time.time() - start_time
        return f'Uptime do servidor: {tempo_atividade:.2f} segundos'
    elif comando == 'help':
        return 'Comandos disponíveis: DATE, UPTIME, HELP'
    elif comando == 'chat':
        return f"Bem-vindo ao modo chat! Digite sua mensagem ou 'exit' para sair."
    else:
        return f'Comando desconhecido: {comando}. Use HELP para ver os comandos válidos.'

# Lidar com conexões TCP
def lidar_com_cliente(conexao, endereco):
    global conexoes
    print(f'Conexão estabelecida com {endereco}')
    registrar_log(f'Conexão iniciada com {endereco}')
    modo_chat = False
    conexoes[endereco] = conexao
    try:
        while True:
            dados = conexao.recv(1024)
            if not dados:
                print(f'Conexão encerrada pelo cliente {endereco}')
                registrar_log(f'Conexão encerrada pelo cliente {endereco}')
                break
            mensagem_cliente = dados.decode()
            registrar_log(f'Cliente {endereco}: {mensagem_cliente}')

            if mensagem_cliente.strip().lower() == 'chat':
                modo_chat = True
                resposta = processar_comando('chat', endereco)
            elif modo_chat:
                if mensagem_cliente.strip().lower() == 'exit':
                    modo_chat = False
                    resposta = "Saindo do modo chat. Você pode enviar comandos novamente."
                else:
                    resposta = f"Mensagem do chat recebida: {mensagem_cliente}"
            else:
                resposta = processar_comando(mensagem_cliente, endereco)

            conexao.sendall(resposta.encode())

            print(f'\nMensagem recebida do cliente {endereco}: {mensagem_cliente}')
            print(f'Resposta enviada para {endereco}: {resposta}')

    except ConnectionResetError:
        print(f'Conexão com {endereco} foi encerrada abruptamente.')
        registrar_log(f'Conexão com {endereco} foi encerrada abruptamente.')
    finally:
        conexao.close()
        del conexoes[endereco]
        print(f'Conexão fechada com {endereco}')
        registrar_log(f'Conexão fechada com {endereco}')


def enviar_mensagens_manualmente():
    while True:
        if conexoes:
            print("\nClientes conectados:")
            for idx, endereco in enumerate(conexoes.keys(), start=1):
                print(f"{idx}. {endereco}")
            try:
                escolha = int(input("Selecione o cliente para enviar uma mensagem (0 para sair): "))
                if escolha == 0:
                    break
                endereco = list(conexoes.keys())[escolha - 1]
                mensagem = input(f"Mensagem para {endereco}: ")
                if mensagem.strip():
                    conexoes[endereco].sendall(mensagem.encode())
                    registrar_log(f"Servidor para {endereco}: {mensagem}")
            except (ValueError, IndexError):
                print("Escolha inválida. Tente novamente.")
        else:
            print("Nenhum cliente conectado.")
            time.sleep(2)

def lidar_com_udp():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((HOST, PORT_UDP))
    print(f'Servidor UDP escutando na porta {PORT_UDP}...')
    while True:
        dados, endereco = udp_socket.recvfrom(1024)
        mensagem_cliente = dados.decode()
        registrar_log(f'Cliente UDP {endereco}: {mensagem_cliente}')
        resposta = processar_comando(mensagem_cliente, endereco)
        udp_socket.sendto(resposta.encode(), endereco)

start_time = time.time()
servidor_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor_tcp.bind((HOST, PORT_TCP))
servidor_tcp.listen()
print(f'Servidor TCP escutando na porta {PORT_TCP}...')
registrar_log('Servidor iniciado')

thread_udp = threading.Thread(target=lidar_com_udp, daemon=True)
thread_udp.start()


while True:
    conexao, endereco = servidor_tcp.accept()
    thread_cliente = threading.Thread(target=lidar_com_cliente, args=(conexao, endereco), daemon=True)
    thread_cliente.start()


thread_manual = threading.Thread(target=enviar_mensagens_manualmente, daemon=True)
thread_manual.start()
