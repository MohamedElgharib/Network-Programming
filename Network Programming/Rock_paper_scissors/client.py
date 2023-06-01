import socket
import tkinter as tk
from tkinter import messagebox

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
host = socket.gethostname()

# Reserve a port for your service
port = 5000

# Connect to the server
client_socket.connect((host, port))

# Create GUI window
window = tk.Tk()
window.title('Rock Paper Scissors')
window.geometry('300x200')

# Create label for player name
player_name = None
player_label = tk.Label(window, text='')
player_label.pack()

def set_player_name(name):
    global player_name
    player_name = name
    player_label.config(text=f'Player: {player_name}')

# Create label for instructions
instructions_label = tk.Label(window, text='Choose rock, paper, or scissors:')
instructions_label.pack()

# Create radio buttons for choices
choice_var = tk.StringVar()
rock_button = tk.Radiobutton(window, text='Rock', variable=choice_var, value='rock')
rock_button.pack()
paper_button = tk.Radiobutton(window, text='Paper', variable=choice_var, value='paper')
paper_button.pack()
scissors_button = tk.Radiobutton(window, text='Scissors', variable=choice_var, value='scissors')
scissors_button.pack()

# Create function to send choice to server
def send_choice():
    choice = choice_var.get()
    client_socket.send(choice.encode())

# Create button to submit choice
submit_button = tk.Button(window, text='Submit', command=send_choice)
submit_button.pack()

# Create label to display winner
winner_label = tk.Label(window, text='')
winner_label.pack()

# Create function to receive opponent's choice and determine winner
def receive_winner():
    # Wait for winner message from server
    winner_message = client_socket.recv(1024).decode()
    # Update winner label with winner message
    winner_label.config(text=winner_message)

    # Ask if players want to play again
    play_again = tk.messagebox.askquestion('Play again?', 'Do you want to play again?')
    client_socket.send(play_again.encode())
    if play_again.lower() == 'yes':
        # Reset radio buttons and winner label
        choice_var.set('')
        winner_label.config(text='')
    else:
        # Close client socket and GUI window
        client_socket.close()
        window.destroy()

# Start game loop
while True:
    # Wait for new game message from server
    new_game_message = client_socket.recv(1024).decode()
    # Display new game message in winner label
    winner_label.config(text=new_game_message)

    # Wait for player's choice
    window.wait_variable(choice_var)

    # Send player's choice to server
    send_choice()

    # Wait for winner message from server and handle game over
    receive_winner()

    # Break game loop if game over
    if winner_label.cget('text') == 'Game over!':
        break

# Run GUI window
window.mainloop()
