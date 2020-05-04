import pygame
import socket
import select
import time

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# SO_ - socket option
# SOL_ - socket option level
# Sets REUSEADDR (as a socket option) to 1 on socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind, so server informs operating system that it's going to use given IP and port
# For a server using 0.0.0.0 means to listen on all available interfaces, useful to connect locally to 127.0.0.1 and remotely to LAN interface IP
server_socket.bind((IP, PORT))

# This makes server listen to new connections
server_socket.listen()

# List of sockets for select.select()
sockets_list = [server_socket]

# List of connected clients - socket as a key, user header and name as data
clients = {}

print(f'Listening for connections on {IP}:{PORT}...')

# Handles message receiving
def receive_message(client_socket):

    try:

        # Receive our "header" containing message length, it's size is defined and constant
        message_header = client_socket.recv(HEADER_LENGTH)

        # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
        if not len(message_header):
            return False

        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())

        # Return an object of message header and message data
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:

        # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
        # or just lost his connection
        # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
        # and that's also a cause when we receive an empty message
        return False

while True:

    # Calls Unix select() system call or Windows select() WinSock call with three parameters:
    #   - rlist - sockets to be monitored for incoming data
    #   - wlist - sockets for data to be send to (checks if for example buffers are not full and socket is ready to send some data)
    #   - xlist - sockets to be monitored for exceptions (we want to monitor all sockets for errors, so we can use rlist)
    # Returns lists:
    #   - reading - sockets we received some data on (that way we don't have to check sockets manually)
    #   - writing - sockets ready for data to be send thru them
    #   - errors  - sockets with some exceptions
    # This is a blocking call, code execution will "wait" here and "get" notified in case any action should be taken
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)


    # Iterate over notified sockets
    for notified_socket in read_sockets:

        # If notified socket is a server socket - new connection, accept it
        if notified_socket == server_socket:

            # Accept new connection
            # That gives us new socket - client socket, connected to this given client only, it's unique for that client
            # The other returned object is ip/port set
            client_socket, client_address = server_socket.accept()

            # Client should send his name right away, receive it
            user = receive_message(client_socket)

            # If False - client disconnected before he sent his name
            if user is False:
                continue

            # Add accepted socket to select.select() list
            sockets_list.append(client_socket)

            # Also save username and username header
            clients[client_socket] = user

            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))

        # Else existing socket is sending a message
        else:

            # Receive message
            message = receive_message(notified_socket)

            # If False, client disconnected, cleanup
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                # Remove from list for socket.socket()
                sockets_list.remove(notified_socket)

                # Remove from our list of users
                del clients[notified_socket]

                continue

            # Get user by notified socket, so we will know who sent the message
            user = clients[notified_socket]

            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            # Iterate over connected clients and broadcast message
            for client_socket in clients:

                # But don't sent it to sender
                if client_socket != notified_socket:

                    # Send user and message (both with their headers)
                    # We are reusing here message header sent by sender, and saved username header send by user when he connected
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    # It's not really necessary to have this, but will handle some socket exceptions just in case
    for notified_socket in exception_sockets:

        # Remove from list for socket.socket()
        sockets_list.remove(notified_socket)

        # Remove from our list of users
        del clients[notified_socket]

'''
clock1 = time.time()
clock2 = time.time()
CID = 1
Clients = [2]
while True:
    conn, addr = serv.accept()
    data = conn.recv(4096)
    if data.decode('utf-8') == 'Client #?':
        conn.send(str(CID).encode('utf-8'))
        Clients.append(2)
        CID += 1
    data = conn.recv(4096)
    if data.decode('utf-8')[1:]=='*':
        value=data.decode('utf-8')[slice(2,3)]
        print(Clients[value])
        Clients[value]==2
    if clock2 - clock1 >= 5:
        for i in range(1,len(Clients)):
            if Clients[i]==1:
                removeplayer(i)
                Clients[i]=0
            else:
                Clients[i]==1
        clock1 = clock2
        clock2 = time.time()
    else:
        clock2 = time.time()


# Board Values Matrix
B = [['WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL'],
     ['WL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'WL'],
     ['WL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'WL'],
     ['WL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'WL'],
     ['WL', 'FL', 'FL', 'FL', 'FL', 'CH', 'FL', 'FL', 'FL', 'FL', 'FL', 'CH', 'FL', 'FL', 'FL', 'FL', 'FL', 'CH', 'FL', 'FL', 'FL', 'FL', 'WL'],
     ['WL', 'FL', 'FL', 'FL', 'CH', 'TB', 'CH', 'FL', 'FL', 'FL', 'CH', 'TB', 'CH', 'FL', 'FL', 'FL', 'CH', 'TB', 'CH', 'FL', 'FL', 'FL', 'WL'],
     ['WL', 'FL', 'FL', 'FL', 'FL', 'CH', 'FL', 'FL', 'FL', 'FL', 'FL', 'CH', 'FL', 'FL', 'FL', 'FL', 'FL', 'CH', 'FL', 'FL', 'FL', 'FL', 'WL'],
     ['WL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'WL'],
     ['WL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'WL'],
     ['WL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'WL'],
     ['WL', 'FL', 'FL', 'FL', 'FL', 'CH', 'FL', 'FL', 'FL', 'FL', 'FL', 'CH', 'FL', 'FL', 'FL', 'FL', 'FL', 'CH', 'FL', 'FL', 'FL', 'FL', 'WL'],
     ['WL', 'FL', 'FL', 'FL', 'CH', 'TB', 'CH', 'FL', 'FL', 'FL', 'CH', 'TB', 'CH', 'FL', 'FL', 'FL', 'CH', 'TB', 'CH', 'FL', 'FL', 'FL', 'WL'],
     ['WL', 'FL', 'FL', 'FL', 'FL', 'CH', 'FL', 'FL', 'FL', 'FL', 'FL', 'CH', 'FL', 'FL', 'FL', 'FL', 'FL', 'CH', 'FL', 'FL', 'FL', 'FL', 'WL'],
     ['WL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'WL'],
     ['WL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'WL'],
     ['WL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'FL', 'WL'],
     ['WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL', 'WL']]

completion = 0
prog = 1
incr = 0
measure1 = time.time()
measure2 = time.time()

# Display colors
wall,floor,chair,table = (224, 224, 209),(183, 183, 149),(153, 187, 255),(172, 115, 57)
# Sets the display
gameDisplay = pygame.display.set_mode((460,340))
# Size of each square
size = 20
# Board length and width
boardLength = 16
boardWidth = 22

all_sprites = pygame.sprite.Group()
P1 = charicters.player()
all_sprites.add(P1)
all_sprites.draw(gameDisplay)

i=0
while i <= boardLength:
    j = 0
    while j <= boardWidth:
        if B[i][j] == 'WL':
            B[i][j] = blocks.wall()
        elif B[i][j] == 'FL':
            B[i][j] = blocks.floor()
        elif B[i][j] == 'CH':
            B[i][j] = blocks.chair()
        elif B[i][j] == 'TB':
            B[i][j] = blocks.table()
        j += 1
    i += 1

# Colors the board by the values in the matrix
i=0
while i <= boardLength:
    j = 0
    while j <= boardWidth:
        pygame.draw.rect(gameDisplay, B[i][j].color, [j * size, i * size, size, size])
        j += 1
    i += 1

# Updates the display for the colors
pygame.display.update()
# Sets the exit value as false
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            color = (0,0,0)
            if event.key == pygame.K_UP:
                if B[P1.y-1][P1.x].standable:
                    color = B[P1.y][P1.x].color
                    pygame.draw.rect(gameDisplay, color, [P1.x * 20, P1.y * 20, size, size])
                    P1.y -= 1
                    B[P1.y][P1.x].interact(P1)
                else:
                    B[P1.y-1][P1.x].interact(P1)
            elif event.key == pygame.K_DOWN:
                if B[P1.y+1][P1.x].standable:
                    color = B[P1.y][P1.x].color
                    pygame.draw.rect(gameDisplay, color, [P1.x * 20, P1.y * 20, size, size])
                    P1.y += 1
                    B[P1.y][P1.x].interact(P1)
                else:
                    B[P1.y+1][P1.x].interact(P1)
            elif event.key == pygame.K_RIGHT:
                if B[P1.y][P1.x+1].standable:
                    color = B[P1.y][P1.x].color
                    pygame.draw.rect(gameDisplay, color, [P1.x * 20, P1.y * 20, size, size])
                    P1.x += 1
                    B[P1.y][P1.x].interact(P1)
                else:
                    B[P1.y][P1.x+1].interact(P1)
            elif event.key == pygame.K_LEFT:
                if B[P1.y][P1.x-1].standable:
                    color = B[P1.y][P1.x].color
                    pygame.draw.rect(gameDisplay, color, [P1.x * 20, P1.y * 20, size, size])
                    P1.x -= 1
                    B[P1.y][P1.x].interact(P1)
                else:
                    B[P1.y-1][P1.x-1].interact(P1)
        P1.update()
        all_sprites.draw(gameDisplay)
        pygame.display.update()

    # Increments the completion bar while a character is on a chair position
    if B[P1.y][P1.x].name == 'chair' and measure2 - measure1 >= 1:
        completion += 1
        measure1 = measure2
        measure2 = time.time()
    else:
        measure2 = time.time()
    if completion > 100:
        pygame.init()
        white = (255, 255, 255)
        red = (230, 0, 0)
        display_surface = pygame.display.set_mode((460, 340))
        pygame.display.set_caption('Yippeeeeeee')
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('You Beat Coronavirus!', True, white, red)
        textRect = text.get_rect()
        textRect.center = (230, 170)
        while True:
            display_surface.fill(white)
            display_surface.blit(text, textRect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
    elif completion > 5.95 + incr:
        incr += 4.76
        prog += 1
    elif completion > 4.76 + incr:
        pygame.draw.rect(gameDisplay, (31, 31, 20), [prog * size, 0, size, size])
    elif completion > 3.57 + incr:
        pygame.draw.rect(gameDisplay, (61, 61, 41), [prog * size, 0, size, size])
    elif completion > 2.38 + incr:
        pygame.draw.rect(gameDisplay, (91, 91, 62), [prog * size, 0, size, size])
    elif completion > 1.19 + incr:
        pygame.draw.rect(gameDisplay, (152, 152, 103), [prog * size, 0, size, size])
    pygame.display.update()
'''