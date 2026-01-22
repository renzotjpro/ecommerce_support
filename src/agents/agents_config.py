from agents import Agent
from src.tools.tools import check_order_status, process_refund

# Billing Specialist
billing_agent = Agent(
    name="Billing Agent",
    instructions="You handle payments and refunds. Use tools for processing refunds.",
    tools=[process_refund]
)

# Technical Support Specialist
support_agent = Agent(
    name="Technical Support Agent",
    instructions="You help with order tracking and technical issues.",
    tools=[check_order_status]
)

# Triage Agent (The Router)
triage_agent = Agent(
    name="Triage Agent",
    instructions="Determine if the user needs help with billing or technical support and hand off.",
    handoffs=[billing_agent, support_agent]
)