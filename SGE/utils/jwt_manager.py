from jwt import encode, decode


def create_token(data:dict):
    token: str = encode(payload = data, key="2444", algorithm="HS256")
    return token


def validate_token(token: str) -> dict:
    data : str = decode(token, key = "2444", algorithms = ['HS256'])
    return data
