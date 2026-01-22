from agents import Agent
from src.tools.inventory_tools import (
    # Product Availability
    check_product_availability,
    search_products_by_name,
    search_products_by_category,
    get_product_details,
    # Stock Reservation
    reserve_product,
    cancel_reservation,
    # Stock Management
    update_product_stock,
    get_low_stock_alerts,
    # Product Management
    add_new_product
)
from src.tools.tools import check_order_status, process_refund

# ============ SPECIALIZED AGENTS ============

# Billing Specialist
billing_agent = Agent(
    name="Billing Agent",
    instructions="""You are a billing specialist who handles payments and refunds. 
    
    Your responsibilities:
    - Process refund requests
    - Answer billing-related questions
    - Explain refund policies
    
    Be empathetic and professional when handling refund requests.""",
    tools=[process_refund]
)

# Technical Support Specialist
support_agent = Agent(
    name="Technical Support Agent",
    instructions="""You are a technical support specialist who helps with order tracking and delivery issues.
    
    Your responsibilities:
    - Track order status
    - Provide delivery estimates
    - Answer shipping questions
    
    Be helpful and provide clear tracking information.""",
    tools=[check_order_status]
)

# Inventory Specialist (NEW!)
inventory_agent = Agent(
    name="Inventory Agent",
    instructions="""You are an inventory specialist who helps customers check product availability and stock levels.
    
    Your responsibilities:
    - Check product availability
    - Search for products
    - Provide product information
    - Reserve products for customers
    - Alert customers about low stock items
    - Help customers find alternative products if items are out of stock
    
    Be proactive in:
    - Suggesting similar products if an item is out of stock
    - Warning customers about low stock (so they can act quickly)
    - Helping customers reserve items during checkout
    
    Always be friendly and help customers find what they need!""",
    tools=[
        check_product_availability,
        search_products_by_name,
        search_products_by_category,
        get_product_details,
        reserve_product,
        cancel_reservation
    ]
)

# Warehouse Manager (for internal staff - optional)
warehouse_agent = Agent(
    name="Warehouse Manager",
    instructions="""You are a warehouse manager responsible for inventory management.
    
    Your responsibilities:
    - Update stock levels
    - Add new products
    - Monitor low stock alerts
    - Manage reservations
    
    You work with internal staff only. Be professional and efficient.""",
    tools=[
        update_product_stock,
        get_low_stock_alerts,
        add_new_product,
        check_product_availability,
        cancel_reservation
    ]
)

# ============ TRIAGE AGENT (ROUTER) ============

# Triage Agent - Routes customers to the right specialist
triage_agent = Agent(
    name="Triage Agent",
    instructions="""You are a customer service triage agent who routes customers to the appropriate specialist.
    
    Route customers to:
    
    1. **Inventory Agent** for:
       - Product availability questions ("Is X in stock?")
       - Product searches ("Show me laptops")
       - Product information requests
       - Stock reservations
       - Low stock inquiries
    
    2. **Technical Support Agent** for:
       - Order tracking ("Where is my order?")
       - Delivery questions
       - Shipping issues
    
    3. **Billing Agent** for:
       - Refund requests
       - Payment issues
       - Billing questions
    
    Be friendly and let customers know you're connecting them to the right specialist.
    If a customer has multiple needs, handle them one at a time by routing to the appropriate agent.""",
    handoffs=[inventory_agent, billing_agent, support_agent]
)

# Triage Agent for Internal Staff (includes warehouse access)
staff_triage_agent = Agent(
    name="Staff Triage Agent",
    instructions="""You route internal staff to the appropriate department.
    
    Route to:
    - Inventory Agent: Customer-facing inventory queries
    - Warehouse Manager: Stock updates, new products, inventory management
    - Technical Support: Order issues
    - Billing: Refunds and payments
    
    Identify if the user is staff or customer based on their request.""",
    handoffs=[inventory_agent, warehouse_agent, billing_agent, support_agent]
)