---
title: Ecommerce_Support
app_file: app.py
sdk: gradio
sdk_version: 6.3.0
---

# 🛍️ E-Commerce Support Agent

An intelligent multi-agent customer support system built with OpenAI's Swarm framework for handling e-commerce inquiries. The system uses specialized agents to route and handle customer requests for order tracking and refund processing.

## 🌟 Features

- **Multi-Agent Architecture**: Intelligent triage system that routes requests to specialized agents
- **Order Tracking**: Check real-time order status and delivery information
- **Refund Processing**: Automated refund initiation for customer orders
- **Persistent Conversations**: SQLite-based session management for conversation history
- **Context Awareness**: Maintains conversation context across multiple interactions

## 🏗️ Architecture

The system uses three specialized agents:

### 1. **Triage Agent (Router)**
- Analyzes customer requests
- Routes queries to appropriate specialist agents
- Handles initial customer interaction

### 2. **Technical Support Agent**
- Manages order tracking inquiries
- Provides delivery status updates
- Handles technical issues

### 3. **Billing Agent**
- Processes refund requests
- Handles payment-related queries
- Manages billing operations

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key
- pip or uv package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/renzotjpro/ecommerce_support.git
cd ecommerce_support
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

Or using `uv`:
```bash
uv pip install -r requirements.txt
```

4. Set up environment variables:

Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Running the Application

```bash
python main.py
```

## 📁 Project Structure

```
ecommerce_support/
├── .git/                    # Git repository
├── .venv/                   # Virtual environment
├── __pycache__/             # Python cache files
├── database/                # SQLite database storage
│   └── conversations.db     # Conversation history
├── .env                     # Environment variables (not in git)
├── .gitignore              # Git ignore rules
├── .python-version         # Python version specification
├── agents_config.py        # Agent definitions and configuration
├── main.py                 # Main application entry point
├── pyproject.toml          # Project metadata and dependencies
├── README.md               # This file
├── tools.py                # Agent tools and functions
└── uv.lock                 # UV package manager lock file
```

## 💡 Usage Examples

### Example 1: Order Tracking

```python
User: Where is my order #1299?
Agent: Order #1299 is 'Shipped' and expected to arrive on Friday.
```

### Example 2: Refund Request with Context

```python
User: Where is my order #1299?
Agent: Order #1299 is 'Shipped' and expected to arrive on Friday.

User: Can I get a refund for it instead?
Agent: Refund for order #1299 has been initiated successfully.
```

## 🔧 Configuration

### Agents Configuration (`agents_config.py`)

The system uses three agents defined in `agents_config.py`:

- **Triage Agent**: Routes customer requests
- **Technical Support Agent**: Handles order tracking
- **Billing Agent**: Processes refunds

You can customize agent behavior by modifying their instructions and tools.

### Tools (`tools.py`)

Two main tools are available:

1. **check_order_status(order_id: str)**: Retrieves order status
2. **process_refund(order_id: str)**: Initiates refunds

To add more tools, use the `@function_tool` decorator:

```python
from agents import function_tool

@function_tool
def your_custom_tool(parameter: str) -> str:
    """Description of your tool."""
    # Your logic here
    return "Result"
```

## 🗄️ Database

The application uses SQLite to store conversation history:

- **Location**: `database/conversations.db`
- **Session Management**: Each customer has a unique session ID
- **Persistence**: Conversation context is maintained across interactions

## 🚀 Deploying to Hugging Face Spaces

### Step 1: Create `app.py` for Gradio Interface

```python
import gradio as gr
import asyncio
import os
from dotenv import load_dotenv
from agents import Runner, SQLiteSession
from agents_config import triage_agent

load_dotenv()

# Store sessions for different users
sessions = {}

async def chat(message, history, session_id="default_user"):
    """Handle chat interactions"""
    if session_id not in sessions:
        sessions[session_id] = SQLiteSession(session_id, "database/conversations.db")
    
    result = await Runner.run(
        triage_agent, 
        message, 
        session=sessions[session_id]
    )
    
    return result.final_output

def chat_wrapper(message, history):
    """Wrapper for Gradio async support"""
    return asyncio.run(chat(message, history))

# Create Gradio interface
demo = gr.ChatInterface(
    fn=chat_wrapper,
    title="🛍️ E-Commerce Support Agent",
    description="Ask about order tracking or request refunds for your orders!",
    examples=[
        "Where is my order #1299?",
        "I want to track order #5678",
        "Can I get a refund for order #1299?",
        "What's the status of my package?"
    ],
    theme=gr.themes.Soft(),
    retry_btn=None,
    undo_btn=None,
    clear_btn="Clear Chat"
)

if __name__ == "__main__":
    demo.launch()
```

### Step 2: Create `requirements.txt`

```txt
openai-swarm
python-dotenv
gradio
openai
```

### Step 3: Deploy

1. Create a new Space on [Hugging Face](https://huggingface.co/spaces)
2. Select "Gradio" as SDK
3. Upload your files or connect via Git
4. Add `OPENAI_API_KEY` in Space Settings → Repository Secrets

## 🛠️ Tech Stack

- **OpenAI Swarm**: Multi-agent orchestration framework
- **Python 3.8+**: Core programming language
- **SQLite**: Conversation persistence
- **python-dotenv**: Environment variable management
- **asyncio**: Asynchronous execution

## 📝 How It Works

1. **User sends a message** to the Triage Agent
2. **Triage Agent analyzes** the request and determines the appropriate specialist
3. **Request is handed off** to either Technical Support or Billing Agent
4. **Specialist agent** uses appropriate tools to fulfill the request
5. **Response is returned** to the user with context maintained

## 🔐 Security

- Never commit `.env` files with API keys
- Use environment variables for sensitive data
- Store API keys in Hugging Face Secrets when deploying

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [OpenAI Swarm](https://github.com/openai/swarm)
- Powered by OpenAI's GPT models
- UI powered by [Gradio](https://gradio.app/)

## 📧 Contact

**Developer**: Renzo  
**GitHub**: [@renzotjpro](https://github.com/renzotjpro)  
**Project Link**: [https://github.com/renzotjpro/ecommerce_support](https://github.com/renzotjpro/ecommerce_support)

---

Made with ❤️ for better customer support automation