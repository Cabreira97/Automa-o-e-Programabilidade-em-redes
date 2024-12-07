import socket

# Configurações do cliente
HOST = 'localhost'
PORT_TCP = 5000
PORT_UDP = 5001

def mostrar_menu_inicial():
    print("\nBem-vindo ao sistema de comunicação!")
    print("1. Conhecer nossos serviços")
    print("2. Ver informações disponíveis")
    print("3. Chat")
    print("4. Sair")
    return input("Escolha uma opção: ").strip()

def mostrar_menu_servicos():
    print("\nConheça nossos serviços:")
    print("- TCP: Conexão estável e confiável para troca de mensagens.")
    print("- UDP: Comunicação rápida e eficiente para mensagens simples.")
    input("Pressione Enter para continuar...")

def mostrar_menu_comandos():
    print("\nInformações disponíveis:")
    print("- DATE: Retorna a data e hora atual do servidor.")
    print("- UPTIME: Informa o tempo de funcionamento do servidor.")
    print("- HELP: Lista os comandos disponíveis.")
    input("Pressione Enter para continuar...")

def autenticar_usuario():
    print("Autenticação do usuário")
    usuario = input("Usuário: ")
    senha = input("Senha: ")

    try:
        with open('usuarios.txt', 'r') as file:
            usuarios = file.readlines()
            for usuario_salvo in usuarios:
                u, s = usuario_salvo.strip().split(',')
                if u == usuario and s == senha:
                    return True
    except FileNotFoundError:
        print("Arquivo de usuários não encontrado.")

    return False

def conectar_tcp():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((HOST, PORT_TCP))
        print('Conectado ao servidor via TCP.')
        return cliente
    except ConnectionRefusedError:
        print('Não foi possível conectar ao servidor via TCP.')
        return None

def processar_comando(cliente, comando):
    cliente.sendall(comando.encode())
    data = cliente.recv(1024)
    print(f'Servidor: {data.decode()}')

def interagir_com_servidor(cliente):
    try:
        while True:
            comando = input("Digite um comando (DATE, UPTIME, HELP, ou CHAT): ")
            if comando.lower() == 'chat':
                print("\nEntrando no chat com o servidor...")
                cliente.sendall('chat'.encode())
                data = cliente.recv(1024)
                print(f'Servidor: {data.decode()}')
                while True:
                    mensagem = input('Você (cliente): ')
                    if mensagem.lower() == 'sair':
                        print('Encerrando conexão.')
                        break
                    cliente.sendall(mensagem.encode())
                    data = cliente.recv(1024)
                    print(f'Servidor: {data.decode()}')
            elif comando.lower() in ['date', 'uptime', 'help']:
                processar_comando(cliente, comando)  # Envia o comando e recebe a resposta
            elif comando.lower() == 'sair':
                print('Saindo...')
                break
            else:
                print("Comando desconhecido. Use DATE, UPTIME, HELP ou CHAT.")
    except KeyboardInterrupt:
        print('\nConexão interrompida pelo usuário.')
    finally:
        cliente.close()
        print('Conexão fechada.')

while True:
    autenticado = autenticar_usuario()
    if autenticado:
        print("Usuário autenticado com sucesso!")
        while True:
            opcao = mostrar_menu_inicial()
            if opcao == '1':
                mostrar_menu_servicos()
            elif opcao == '2':
                mostrar_menu_comandos()
            elif opcao == '3':
                cliente = conectar_tcp()
                if cliente:
                    interagir_com_servidor(cliente)
            elif opcao == '4':
                print("Saindo do sistema. Até logo!")
                break
            else:
                print("Opção inválida. Tente novamente.")
    else:
        print("Credenciais inválidas. Tente novamente.")
