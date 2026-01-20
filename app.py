import gradio as gr
import os
import asyncio
from dotenv import load_dotenv
from agents import Runner, SQLiteSession
from agents_config import triage_agent

# Load environment variables
load_dotenv()

# Define the database path
# For Hugging Face Spaces, we might want to use a persistent storage path if available,
# but for a simple demo, the default local path is fine.
DB_PATH = "database/conversations.db"

async def interact_with_agent(message, history):
    """
    Function to handle user interaction with the agent.
    Gradio's ChatInterface passes 'message' (str) and 'history' (list).
    """
    # Use a static session ID for this demo to maintain context within a session run,
    # or arguably we could generate one per browser session if we could access the request.
    # For simplicity and to match the console demo, we'll use a fixed ID.
    # PRO TIP: In a real app, you'd handle session management more robustly.
    session_id = "demo_user"
    
    session = SQLiteSession(session_id, DB_PATH)
    
    try:
        # Run the agent
        result = await Runner.run(triage_agent, message, session=session)
        return result.final_output
    except Exception as e:
        return f"Error: {str(e)}"

# Create the Gradio Interface
app = gr.ChatInterface(
    fn=interact_with_agent,
    title="E-Commerce Support Agent",
    description="Ask about your orders or request refunds. Try asking: 'Where is my order #55442?'",
    examples=["Where is my order #55442?", "Can I get a refund for order #1299?"],
)

if __name__ == "__main__":
    app.launch()
