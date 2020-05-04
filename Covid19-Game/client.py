import pygame
import socket
import select
import errno
import time

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
my_username = input("Username: ")

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(False)

# Prepare username and header and send them
# We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

while True:

    # Wait for user to input a message
    message = input(f'{my_username} > ')

    # If message is not empty - send it
    if message:

        # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        # Now we want to loop over received messages (there might be more than one) and print them
        while True:

            # Receive our "header" containing username length, it's size is defined and constant
            username_header = client_socket.recv(HEADER_LENGTH)

            # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())

            # Receive and decode username
            username = client_socket.recv(username_length).decode('utf-8')

            # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            # Print message
            print(f'{username} > {message}')

    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        # We just did not receive anything
        continue

    except Exception as e:
        # Any other exception - something happened, exit
        print('Reading error: '.format(str(e)))
        sys.exit()

'''
clock1 = time.time()
clock2 = time.time()
mystring = 'Client #?'
client.send(mystring.encode('utf-8'))
data = client.recv(4096)
comp = 0
while comp < 100:
    if clock2 - clock1 >= 5:
        client.send((str(data) + '*').encode('utf-8'))
        clock1 = clock2
        clock2 = time.time()
    else:
        clock2 = time.time()
    data = client.recv(4096)
    if not data: break
client.close()

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