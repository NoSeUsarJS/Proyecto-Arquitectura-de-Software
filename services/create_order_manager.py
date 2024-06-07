from common.services import Service
import json

SERVICE_NAME = "create_order_manager"
host, port = "localhost", 5000
service = Service(SERVICE_NAME, host, port)

def create_order(data: str) -> str:
    data = json.loads(data)
    response = {
        "message": f"Orden: {data["food"]} was created."
    }

    return str(json.dumps(response))

service.run_service(create_order)