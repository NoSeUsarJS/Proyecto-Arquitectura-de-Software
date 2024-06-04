from services_mapping import services_mapping

def soa_formatter(service_name: str, content: str) -> str | None:
    try:
        service = services_mapping[service_name]
    except KeyError:
        print(f"ERROR: '{service_name}' does not exist.")
        return None
    
    payload_length = len(service) + len(content)
    padding_length = 5 - len(str(payload_length))
    padding = ""

    for _ in range(padding_length):
        padding += "0"
    
    formatted_response = padding + str(payload_length) + service + content

    return formatted_response
