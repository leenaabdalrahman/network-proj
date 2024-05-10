# Ala nidal 1212616
# Leena Abdalrahman 1211051
# Shahd Walid 1212077

import socket
import threading
import time

#configuration parameters
local_ip = '192.168.56.1' #local IP
port = 5051 #port number
buffer_size = 1024 #buffer size for receiving messages
broadcast_ip = '255.255.255.0' #broadcast IP used foe sending

#UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #initializing UDP socket
sock.bind((local_ip, port))
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #set for broadcasting

#to keep track of sent messages
messageM = []

#function to receive messages from the network
def receive_messages():
    while True:
        data, addr = sock.recvfrom(buffer_size) #data from socket being received
        received_time = time.strftime('%X') #current time
        full_message = data.decode() #decode bytes to string
        messageM.append((addr[0], full_message, received_time))

#function to send messages on the network
def send_message(first_name, last_name, message):
    full_message = f"{first_name} {last_name} says: {message}" #the message's look
    sock.sendto(full_message.encode(), (broadcast_ip, port)) #sending it to the broadcast IP
    print("Message sent.")

#function to display all received messages
def display():
    if not messageM:
        print("No messages received.") #error message
    for i, entry in enumerate(messageM, 1):
        name = " ".join(entry[1].split()[:2])  #taking the sender's name
        print(f"{i}- received a message from '{name}' at {entry[2]}")

#function to display a specific message
def display_specific_message(line_number):
    if line_number < 1 or line_number > len(messageM):
        print("Invalid message number.") #error message
    else:
        message = messageM[line_number - 1]  #get message in specified number
        message_content = " ".join(message[1].split(' ')[3:])  #taking only the message
        print(f"Message {line_number}: \"{message_content}\"")

#function to handle commands entered
def input_handler():
    while True:
        cmd = input("Enter command send, display, exit, or D#(number of message line): ").strip().lower() #taking the input command
        if cmd == "send":
            first_name = input("Enter your first name: ").strip()
            last_name = input("Enter your last name: ").strip()
            message = input("Enter message: ").strip()
            send_message(first_name, last_name, message) #calling the sending function
        elif cmd == "display":
            display() #calling the displaying function
        elif cmd.startswith('d') and cmd[1:].isdigit():  #if coomand is D followed by a number
            line_number = int(cmd[1:])  #getting the line number after 'd'
            display_specific_message(line_number) #displaying the specified message
        elif cmd == "exit":
            print("Exiting ...") #exitting message
            break

def main():
    input_handler() #calling the input function to take command inputs

if __name__ == "__main__":
    receiver_thread = threading.Thread(target=receive_messages, daemon=True) #thread to run the receiving function
    receiver_thread.start()
    main() #calling the main function
