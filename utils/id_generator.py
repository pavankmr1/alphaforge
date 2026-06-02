import uuid

def generate_strategy_id():

    return f"AF-{uuid.uuid4().hex[:8]}"