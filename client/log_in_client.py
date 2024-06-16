import socket
import json
from common.soa_formatter import soa_formatter
import client_table
import client_meal
import client_inventory
import client_personal
import client_pedidos
import client_generar_pedido
import client_venta
import client_generate_excel
def login_client():
    server_address = ('localhost', 5001)
    print('Connecting to {} port {}'.format(*server_address))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    try:
        rut = input("Ingrese el rut: ")
        password = input("ingrese la contraseña: ")
        data = {"action": "0", "rut": rut ,"password":password }
        
        #No tocar
        message = soa_formatter("account_manager", json.dumps(data))
        sock.sendall(message)

        amount_received = 0
        amount_expected = int(sock.recv(5))
        data = b''

        while amount_received < amount_expected:
            packet = sock.recv(amount_expected - amount_received)
            amount_received += len(packet)
            data += packet
        print("Received raw data:", data)
        
        return data.decode()[7:]
                    
    finally:
        print('Closing socket')
        sock.close()
        #print(data.decode()[7:])

def main():
    while True:
        print("\nIniciar Sesion:")
        var = login_client()
        if(var == "t"):
            while True:
                print("\nMain Menu:")
                print("1. Gestor de Mesas")
                print("2. Gestor de personal")
                print("3. Gestor de inventario")
                print("4. Gestor de comidas")
                print("5. Generar Excel")
                print("6. Ver Dashboard")
                print("7. Gestor de Ventas")
                print("8. Gestor de comidas")
                #print("9. Linkear comida e ingrediente") 
                print("9. Cerrar sesion")

                valor = input("Seleccione Cliente: ")
                if(valor == "1"):
                    client_table.main()
                elif(valor == "2"):
                    client_personal.main()
                elif(valor == "3"):
                    client_inventory.main()
                elif(valor == "4"):
                    client_meal.main()
                elif(valor == "5"):
                    client_generate_excel.main() #arreglar client_excel y acoplarlo al servicio 
                elif(valor == "6"):
                    print("Proximamente") #arreglar client_dashboard y acoplarlo al servicio 
                elif(valor == "7"):
                    client_venta.main()
                elif(valor == "8"):
                    client_pedidos.main()
                elif(valor == "9"):
                    break
                else:
                    print("Ingrese valor valido")
        elif(var == "f"):
            while True:
                print("\nMain Menu:")
                print("1. Ver menu")
                print("2. Generar Pedido")
                print("3. Cerrar Pedido")
                print("4. Cambiar contraseña")
                print("5. Cerrar sesion")

                valor = input("Seleccione Cliente: ")
                if(valor == "1"):
                    client_meal.watch_client()
                elif(valor == "2"):
                    client_generar_pedido.main() # Crear servicio?
                elif(valor == "3"):
                    client_venta.cerrar_cuenta() #crear todo?
                elif(valor == "4"):
                    client_personal.editpass() 
                elif(valor == "5"):
                    break
                else:
                    print("Ingrese valor valido")
        else:
            print("Ocurrio un error en el inicio de sesion")
        
        
if __name__ == "__main__":
    main()

#"account_manager": "SV009"