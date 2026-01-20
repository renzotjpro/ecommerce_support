import asyncio
from dotenv import load_dotenv

load_dotenv()
from agents import Runner, SQLiteSession
from agents_config import triage_agent

async def main():
    # Initialize session for a specific user
    session = SQLiteSession("customer_123", "database/conversations.db")
    
    print("--- E-Commerce Support Active ---")
    
    # Turn 1: Initial Request
    user_input_1 = "Where is my order #1299?"
    print(f"User: {user_input_1}")
    
    result = await Runner.run(triage_agent, user_input_1, session=session)
    print(f"Agent: {result.final_output}")

    # Turn 2: Follow-up (Context is maintained by the session)
    user_input_2 = "Can I get a refund for it instead?"
    print(f"\nUser: {user_input_2}")
    
    result = await Runner.run(triage_agent, user_input_2, session=session)
    print(f"Agent: {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
