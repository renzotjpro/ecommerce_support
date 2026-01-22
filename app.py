import gradio as gr
import os
import asyncio
from dotenv import load_dotenv
from agents import Runner
from src.agents.inventory_agent import triage_agent

# Load environment variables
load_dotenv()

async def chat_async(message, history):
    """Handle chat interactions"""
    try:
        result = await Runner.run(triage_agent, message)
        return result.final_output
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

def chat(message, history):
    """Wrapper for Gradio"""
    return asyncio.run(chat_async(message, history))

# Create Gradio interface
demo = gr.ChatInterface(
    fn=chat,
    title="🛍️ E-Commerce Support Agent with Inventory",
    description="Ask about products, check stock, track orders, or request refunds!",
    examples=[
        "Is the MacBook Pro in stock?",
        "Show me all electronics",
        "Search for yoga mat",
        "What's the cheapest product in Home & Kitchen?",
        "Reserve 1 iPhone 15 Pro for me",
        "Where is my order #ORD1299?",
        "I want a refund for order #ORD1299"
    ]
)

if __name__ == "__main__":
    demo.launch()