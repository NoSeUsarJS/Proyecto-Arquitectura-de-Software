import socket

def format_soa_transaction(service, data):
    if len(service) > 5:
        raise ValueError("Service name must be no longer than 5 characters")
    message = service + data
    length = len(message)
    formatted_message = f"{length:05d}{message}"
    return formatted_message

class SOAService:
    def __init__(self, name, conn):
        self.name = name
        self.conn = conn

    def init_service(self):
        try:
            transaction = format_soa_transaction("sinit", self.name)
        except ValueError as e:
            return "", e

        print("Sending init transaction to bus:", transaction)
        try:
            self.conn.sendall(transaction.encode('utf-8'))
        except socket.error as e:
            return "", e

        buffer = self.conn.recv(1024)
        response = buffer.decode('utf-8')
        return response, None

    def process_data(self, processor):
        while True:
            print("Waiting for transactions...")
            try:
                buffer = self.conn.recv(1024)
                if len(buffer) < 5:
                    print("Invalid transaction format")
                    return
                transaction = buffer.decode('utf-8')
            except socket.error as e:
                print("Error reading from connection:", e)
                return

            service = transaction[5:10].strip()
            data = transaction[10:].strip()
            print("Received data:", data)

            print("Processing data...")
            response_data = processor(data)

            try:
                response = format_soa_transaction(service, response_data)
            except ValueError as e:
                print("Error formatting response transaction:", e)
                return

            print("Sending response transaction:", response)
            try:
                self.conn.sendall(response.encode('utf-8'))
            except socket.error as e:
                print("Error sending response transaction:", e)
                return

def example_data_processor(data):
    return "Processed" + data

if __name__ == "__main__":
    # Example usage:
    service_name = "example"
    bus_addr = ("localhost", 5000)

    try:
        conn = socket.create_connection(bus_addr)
    except socket.error as e:
        print("Error connecting to the server:", e)
        exit(1)

    soa_service = SOAService(service_name, conn)

    response, err = soa_service.init_service()
    if err:
        print("Error initializing service:", err)
        exit(1)
    print("Service initialized with response:", response)

    soa_service.process_data(example_data_processor)
