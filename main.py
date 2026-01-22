import asyncio
from dotenv import load_dotenv

load_dotenv()

from agents import Runner
from src.agents.inventory_agent  import triage_agent


async def main():
    print("🛍️ E-Commerce Support with Inventory Management\n")
    
    # Test 1: Check product availability
    print("Test 1: Product Availability")
    print("-" * 40)
    user_input = "Is the MacBook Pro in stock?"
    print(f"User: {user_input}")
    
    result = await Runner.run(triage_agent, user_input)
    print(f"Agent: {result.final_output}\n")
    
    # Test 2: Search for products
    print("Test 2: Product Search")
    print("-" * 40)
    user_input = "Show me all electronics"
    print(f"User: {user_input}")
    
    result = await Runner.run(triage_agent, user_input)
    print(f"Agent: {result.final_output}\n")
    
    # Test 3: Reserve a product
    print("Test 3: Reserve Product")
    print("-" * 40)
    user_input = "I want to reserve 2 AirPods Pro for customer CUST001"
    print(f"User: {user_input}")
    
    result = await Runner.run(triage_agent, user_input)
    print(f"Agent: {result.final_output}\n")

    # Test 4: Check low stock
    print("Test 4: Low Stock Alert")
    print("-" * 40)
    user_input = "Show me products that are running low on stock"
    print(f"User: {user_input}")
    
    result = await Runner.run(triage_agent, user_input)
    print(f"Agent: {result.final_output}\n")

    # Test 5: Out of stock product
    print("Test 5: Out of Stock Product")
    print("-" * 40)
    user_input = "I want to buy the Sony WH-1000XM5 Headphones"
    print(f"User: {user_input}")
    
    result = await Runner.run(triage_agent, user_input)
    print(f"Agent: {result.final_output}\n")

    # Test 6: Multi-turn conversation
    print("Test 6: Multi-Turn Conversation")
    print("-" * 40)
    user_input = "I need a new laptop"
    print(f"User: {user_input}")
    
    result = await Runner.run(triage_agent, user_input)
    print(f"Agent: {result.final_output}\n")
    
    user_input = "What about something cheaper?"
    print(f"User: {user_input}")
    
    result = await Runner.run(triage_agent, user_input)
    print(f"Agent: {result.final_output}\n")

    # Test 7: Complex query
    print("Test 7: Complex Query")
    print("-" * 40)
    user_input = "Do you have any running shoes in stock? I need size 10."
    print(f"User: {user_input}")
    
    result = await Runner.run(triage_agent, user_input)
    print(f"Agent: {result.final_output}\n")

    # Test 8: Check stock after reservation
    print("Test 8: Check Stock After Reservation")
    print("-" * 40)
    user_input = "How many AirPods Pro are left now?"
    print(f"User: {user_input}")
    
    result = await Runner.run(triage_agent, user_input)
    print(f"Agent: {result.final_output}\n")

    # Test 9: Check stock after purchase
    print("Test 9: Check Stock After Purchase")
    print("-" * 40)
    user_input = "I just bought the 2 AirPods Pro. How many are left?"
    print(f"User: {user_input}")
    
    result = await Runner.run(triage_agent, user_input)
    print(f"Agent: {result.final_output}\n")

    # Test 10: Check stock after refund
    print("Test 10: Check Stock After Refund")
    print("-" * 40)
    user_input = "I returned the 2 AirPods Pro. How many are back in stock?"
    print(f"User: {user_input}")
    
    result = await Runner.run(triage_agent, user_input)
    print(f"Agent: {result.final_output}\n")

    # Test 11: Check stock after cancellation
    print("Test 11: Check Stock After Cancellation")
    print("-" * 40)
    user_input = "I cancelled my reservation for the 2 AirPods Pro. How many are left?"
    print(f"User: {user_input}")
    
    result = await Runner.run(triage_agent, user_input)
    print(f"Agent: {result.final_output}\n")

    # Test 12: Check stock after update
    print("Test 12: Check Stock After Update")
    print("-" * 40)
    user_input = "I added 5 more AirPods Pro to the inventory. How many are there now?"
    print(f"User: {user_input}")
    
    result = await Runner.run(triage_agent, user_input)
    print(f"Agent: {result.final_output}\n")

    # Test 13: Check stock after update
    print("Test 13: Check Stock After Update")
    print("-" * 40)
    user_input = "I added 5 more AirPods Pro to the inventory. How many are there now?"
    print(f"User: {user_input}")
    
    result = await Runner.run(triage_agent, user_input)
    print(f"Agent: {result.final_output}\n")

    # Test 14: Check stock after update
    print("Test 14: Check Stock After Update")
    print("-" * 40)
    user_input = "I added 5 more AirPods Pro to the inventory. How many are there now?"
    print(f"User: {user_input}")
    
    result = await Runner.run(triage_agent, user_input)
    print(f"Agent: {result.final_output}\n")

    # Test 15: Check stock after update
    print("Test 15: Check Stock After Update")
    print("-" * 40)
    user_input = "I added 5 more AirPods Pro to the inventory. How many are there now?"
    print(f"User: {user_input}")
    
    result = await Runner.run(triage_agent, user_input)
    print(f"Agent: {result.final_output}\n")

    # Test 16: Check stock after update
    print("Test 16: Check Stock After Update")
    print("-" * 40)
    user_input = "I added 5 more AirPods Pro to the inventory. How many are there now?"
    print(f"User: {user_input}")
    
    result = await Runner.run(triage_agent, user_input)
    print(f"Agent: {result.final_output}\n")

    # Test 17: Check stock after update
    print("Test 17: Check Stock After Update")
    print("-" * 40)
    user_input = "I added 5 more AirPods Pro to the inventory. How many are there now?"
    print(f"User: {user_input}")
    
    result = await Runner.run(triage_agent, user_input)
    print(f"Agent: {result.final_output}\n")

    # Test 18: Check stock after update
    print("Test 18: Check Stock After Update")
    print("-" * 40)
    user_input = "I added 5 more AirPods Pro to the inventory. How many are there now?"
    print(f"User: {user_input}")
    
    result = await Runner.run(triage_agent, user_input)
    print(f"Agent: {result.final_output}\n")

    # Test 19: Check stock after update
    print("Test 19: Check Stock After Update")
    print("-" * 40)
    user_input = "I added 5 more AirPods Pro to the inventory. How many are there now?"
    print(f"User: {user_input}")
    
    result = await Runner.run(triage_agent, user_input)
    print(f"Agent: {result.final_output}\n")

    # Test 20: Check stock after update
    print("Test 20: Check Stock After Update")
    print("-" * 40)
    user_input = "I added 5 more AirPods Pro to the inventory. How many are there now?"
    print(f"User: {user_input}")
    
    result = await Runner.run(triage_agent, user_input)
    print(f"Agent: {result.final_output}\n  

if __name__ == "__main__":
    asyncio.run(main())
    