import socket
from common.soa_formatter import soa_formatter
import json
import ast
import matplotlib.pyplot as plt

def watch_client():
    server_address = ('localhost', 5001)
    print('Connecting to {} port {}'.format(*server_address))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    try:
        data = {"action": "1"}
        
        #No tocar
        message = soa_formatter("dashboard", json.dumps(data))
        sock.sendall(message)

        amount_received = 0
        amount_expected = int(sock.recv(5))
        data = b''

        while amount_received < amount_expected:
            packet = sock.recv(amount_expected - amount_received)
            amount_received += len(packet)
            data += packet
        
        print("Received raw data:", data)
        # Agregar manejo de errores
        data1 = json.loads(data.decode()[7:])
        #data1 = f"{json.loads(data.decode()[7:])}" 
        #print(data1[0][1])
        SumP = 0
        Tiempo_actual = '0'
        y = []
        x = []

        for i in range(len(data1)):
            Precio = data1[i][0]
            #print(Precio)
            SumP += Precio
            
            Tiempo = data1[i][1]
            #print(Tiempo)
            timestamp_str = Tiempo['timestamp']
            start_index = timestamp_str.find("'") + 1
            end_index = timestamp_str.find("T")
            fecha = timestamp_str[start_index:end_index]
            print(fecha)

            x.append(fecha)         
            y.append(Precio)  
        
        plt.bar(x, y)
        plt.show()
        #list_of_strings = ast.literal_eval(data1)
        #print(list_of_strings)
        return True
                    
    finally:
        print('Closing socket')
        sock.close()
        


def main():
    while True:
        print("\nMain Menu:")
        print("1. Generar dashboard de ventas")
        print("2. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            watch_client()
        elif choice == "2":
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
