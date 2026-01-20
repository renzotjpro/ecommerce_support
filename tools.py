from agents import function_tool

@function_tool
def check_order_status(order_id: str) -> str:
    """Retrieves the current status of a customer order."""
    # In a production environment, this would call an external API
    return f"Order {order_id} is 'Shipped' and expected to arrive on Friday."

@function_tool
def process_refund(order_id: str) -> str:
    """Initiates a refund for a specific order."""
    return f"Refund for order {order_id} has been initiated successfully."