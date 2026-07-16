from typing import Union

def process_input(data: Union[str, bytes])-> None:
    if isinstance(data, str):
        print(f"Processing string data: {data}")
    elif isinstance(data, bytes):
        print(f"Processing bytes data: {data.decode('utf-8')}")
    else:
        raise ValueError("Unsupported data type")
process_input("AI")
process_input(b'\X89PNG\r\n')
