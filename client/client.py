import socket
import sys

bus_addr = ("localhost", 5000)

def format_soa_transaction(service, data):
    if len(service) > 5:
        raise ValueError("Service name must be no longer than 5 characters")
    message = service + data
    length = len(message)
    formatted_message = f"{length:05d}{message}"
    return formatted_message

def main():
    service = "salud"
    data = "Hello, World!"

    try:
        transaction = format_soa_transaction(service, data)
    except ValueError as e:
        print("Error formatting transaction:", e)
        sys.exit(1)

    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(bus_addr)
    except socket.error as e:
        print("Error connecting to the server:", e)
        sys.exit(1)

    try:
        print("Sending transaction:", transaction)
        conn.sendall(transaction.encode('utf-8'))

        response = conn.recv(1024)
        print("Server response:", response.decode('utf-8'))
    except socket.error as e:
        print("Error during communication:", e)
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
