import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
host = socket.gethostname()

# Reserve a port for your service
port = 5000

# Bind the socket to a public host, and a well-known port
server_socket.bind((host, port))

# Max number of clients that can connect simultaneously
max_clients = 2

# Wait for client connections
server_socket.listen(max_clients)
print('Waiting for players to connect...')

# List to hold client sockets
clients = []

# Accept connections from clients
while len(clients) < max_clients:
    # Wait for a connection
    client_socket, client_address = server_socket.accept()
    print(f'Connection from {client_address[0]}:{client_address[1]}')

    # Add client socket to list
    clients.append(client_socket)

# Send welcome message to each client
for i in range(max_clients):
    clients[i].send('Welcome to Rock Paper Scissors!'.encode())

# Game logic
rules = {'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper'}
player1_choice = None
player2_choice = None

while True:
  # Wait for player 1's choice
  player1_choice = clients[0].recv(1024).decode()
  print(f'Player 1 choice: {player1_choice}')

  # Wait for player 2's choice
  player2_choice = clients[1].recv(1024).decode()
  print(f'Player 2 choice: {player2_choice}')

  # Determine winner
  if player1_choice == player2_choice:
      winner = 'Tie'
  elif rules[player1_choice] == player2_choice:
      winner = 'Player 1'
  else:
      winner = 'Player 2'

  # Send winner message to both clients
  for i in range(max_clients):
      clients[i].send(f'{winner} wins!'.encode())

  # Ask if players want to play again
  play_again = clients[0].recv(1024).decode()
  if play_again.lower() == 'yes':
      # Reset choices for new game
      player1_choice = None
      player2_choice = None
      # Send play again message to both clients
      for i in range(max_clients):
          clients[i].send('New game starting...'.encode())
  else:
      # Send game over message to both clients
      for i in range(max_clients):
          clients[i].send('Game over!'.encode())
      break

# Close connections
for client in clients:
    client.close()

