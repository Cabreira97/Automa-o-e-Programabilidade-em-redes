# Projeto Final - Servidor Tech UniSenac 
## Introdução

O sistema de comunicação TCP/UDP desenvolvido consiste em um servidor que oferece múltiplas funcionalidades de interação com o cliente, através de dois tipos de protocolos: TCP e UDP. O objetivo é permitir que o cliente envie comandos e mensagens para o servidor, que responde com informações sobre o status do servidor, como data, tempo de atividade (uptime) e uma funcionalidade de chat. Este sistema pode ser utilizado para diversos fins, como monitoramento do servidor e troca de mensagens em tempo real. O código é dividido entre a parte do servidor e a parte do cliente, onde ambos interagem utilizando os protocolos definidos.

## Estrutura do Código

### 1. **Cliente**
O cliente foi desenvolvido utilizando a biblioteca `socket` e oferece uma interface interativa para o usuário, permitindo realizar autenticação e selecionar opções de interação com o servidor.

#### Funções do Cliente
- **Mostrar Menu Inicial**: Apresenta as opções disponíveis para o usuário, como conhecer os serviços, ver informações, interagir com o chat ou sair.
- **Mostrar Menu de Serviços**: Exibe informações sobre os serviços oferecidos pelo servidor (TCP e UDP).
- **Mostrar Menu de Comandos**: Apresenta os comandos disponíveis para o usuário, como `DATE`, `UPTIME` e `HELP`.
- **Autenticação do Usuário**: Solicita o nome de usuário e senha e valida se as credenciais informadas correspondem a algum registro no arquivo `usuarios.txt`. O arquivo `usuarios.txt` deve estar localizado na raiz do projeto e ter o seguinte formato: `usuario1,senha123` (um usuário por linha).
- **Conectar via TCP**: Estabelece a conexão com o servidor utilizando o protocolo TCP e mantém a comunicação até que o cliente decida sair.
- **Processar Comando**: Envia o comando ao servidor e recebe a resposta.
- **Interagir com o Servidor**: Permite que o cliente envie comandos como `DATE`, `UPTIME`, `HELP` e entre no modo de chat.

### 2. **Servidor**
O servidor foi desenvolvido utilizando `socket` e `threading` para gerenciar múltiplas conexões simultâneas. Ele escuta as requisições dos clientes e responde conforme os comandos recebidos.

#### Funções do Servidor
- **Registrar Log**: Registra todas as interações e eventos do servidor em um arquivo de log chamado `server_log.txt`.
- **Processar Comando**: Responde de acordo com os comandos recebidos, como `DATE` (data atual), `UPTIME` (tempo de atividade do servidor), `HELP` (comandos disponíveis) e `CHAT` (entrar no modo chat).
- **Lidar com Conexões TCP**: Gerencia as conexões com os clientes via TCP, mantendo uma sessão de interação contínua. Também lida com o modo de chat, onde o servidor envia e recebe mensagens em tempo real.
- **Lidar com UDP**: O servidor também escuta e responde a requisições via UDP, que são mais rápidas e eficientes, mas não garantem a entrega das mensagens.
- **Enviar Mensagens Manualmente**: Permite que o servidor envie mensagens manualmente para os clientes conectados, selecionando o cliente desejado.

### 3. **Interação entre Cliente e Servidor**
- **Autenticação**: O cliente deve fornecer credenciais válidas para acessar o sistema. Caso contrário, a autenticação falha.
- **Comandos TCP**: O cliente pode interagir com o servidor utilizando comandos, e o servidor retorna respostas de acordo com o comando.
- **Chat**: O cliente pode entrar no modo de chat, onde poderá trocar mensagens com o servidor em tempo real. O servidor mantém a conversa enquanto o cliente não sair do modo chat.

### 4. **Operações de Log**
O servidor registra todas as interações no arquivo de log, incluindo conexões, comandos processados e mensagens trocadas. Isso facilita o monitoramento e depuração do sistema.

### 5. **Multi-threading**
O servidor é projetado para lidar com múltiplas conexões simultâneas. Para isso, ele utiliza threads para processar cada cliente em paralelo, garantindo que o servidor não fique bloqueado por uma única conexão.

## Conclusão

O sistema de comunicação TCP/UDP desenvolvido oferece uma solução robusta para interações cliente-servidor, com suporte a comandos simples como data, uptime e chat. A utilização de multi-threading permite que o servidor gerencie várias conexões simultaneamente, enquanto o uso de TCP garante uma comunicação estável e confiável, e o UDP oferece uma alternativa mais rápida e eficiente para mensagens simples. O registro de logs facilita o monitoramento das atividades do servidor, e o código pode ser expandido para incluir novas funcionalidades conforme necessário. O cliente, por sua vez, oferece uma interface amigável para o usuário, permitindo interações intuitivas com o servidor.
