---
title: E-Commerce Support Agent
emoji: 🛍️
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 6.3.0
app_file: app.py
pinned: false
license: mit
---



An intelligent multi-agent customer support system powered by OpenAI's Swarm framework. This AI agent handles customer inquiries for e-commerce operations including order tracking, inventory management, and refund processing.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-Swarm-412991.svg)](https://github.com/openai/swarm)
[![Supabase](https://img.shields.io/badge/Database-Supabase-3ECF8E.svg)](https://supabase.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌟 Features

### Multi-Agent Architecture
- **🎯 Triage Agent** - Intelligently routes customer requests to specialized agents
- **📦 Inventory Agent** - Handles product availability, searches, and stock reservations
- **🔧 Technical Support Agent** - Manages order tracking and delivery inquiries
- **💰 Billing Agent** - Processes refunds and payment-related queries

### Core Capabilities
- ✅ **Order Tracking** - Real-time order status and delivery information
- ✅ **Inventory Management** - Product search, availability checks, and stock alerts
- ✅ **Refund Processing** - Automated refund request handling
- ✅ **Stock Reservations** - 15-minute checkout holds to prevent overselling
- ✅ **Conversation History** - Persistent chat context across sessions
- ✅ **Low Stock Alerts** - Automatic notifications for products running low

### Technical Highlights
- 🤖 **OpenAI Swarm Framework** - Advanced multi-agent orchestration
- 🗄️ **PostgreSQL/Supabase** - Production-ready database with full ACID compliance
- 🔄 **Async Operations** - Fast, non-blocking agent responses
- 📊 **Complete Audit Trail** - Stock movement tracking and conversation logs
- 🎨 **Gradio Interface** - User-friendly web UI for testing and demos

---

## 📸 Demo

```
User: "Is the MacBook Pro in stock?"

Agent: [Routing to Inventory Agent...]

Inventory Agent: "Product: MacBook Pro 14-inch (PROD001)
✅ IN STOCK

📦 Stock Information:
- Available: 25 units
- Price: $1,999.99
- Category: Electronics

Great news! We have plenty in stock. Would you like to place an order?"
```

---

## 🏗️ Architecture

### Agent Flow

```
┌─────────────┐
│    User     │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Triage Agent   │ ◄── Routes to appropriate specialist
└────────┬────────┘
         │
    ┌────┴────┬──────────┬─────────────┐
    │         │          │             │
    ▼         ▼          ▼             ▼
┌─────┐  ┌────────┐  ┌──────┐  ┌──────────┐
│Bills│  │Support │  │Inven-│  │Warehouse │
│Agent│  │ Agent  │  │ tory │  │ Manager  │
└─────┘  └────────┘  └──────┘  └──────────┘
```

### Database Schema

```
customers ──┬── orders ──── refunds
            │
            └── conversations
            
inventory ──┬── reservations
            │
            └── stock_movements
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Supabase account (free tier works great!)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/renzotjpro/ecommerce_support.git
   cd ecommerce_support
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   # OpenAI Configuration
   OPENAI_API_KEY=sk-your-openai-api-key-here
   
   # Supabase Configuration
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=your-supabase-anon-key-here
   ```

5. **Create database tables**
   
   - Go to your [Supabase Dashboard](https://app.supabase.com)
   - Navigate to SQL Editor
   - Copy and run the SQL schema from `docs/complete_database_schema.sql`

6. **Load sample data**
   ```bash
   python setup_inventory_data.py
   ```

7. **Run the application**
   
   **CLI Mode:**
   ```bash
   python main.py
   ```
   
   **Web Interface (Gradio):**
   ```bash
   python app.py
   ```
   
   Then open `http://localhost:7860` in your browser

---

## 📁 Project Structure

```
ecommerce_support/
├── 📄 agents_config.py          # Agent definitions and configurations
├── 📄 app.py                    # Gradio web interface
├── 📄 database.py               # Database operations (Supabase)
├── 📄 inventory_tools.py        # Inventory management tools
├── 📄 main.py                   # CLI interface
├── 📄 tools.py                  # Order and refund tools
├── 📄 setup_inventory_data.py   # Sample data loader
├── 📄 requirements.txt          # Python dependencies
├── 📄 .env                      # Environment variables (not in git)
├── 📄 .env.example              # Example environment file
├── 📄 .gitignore                # Git ignore rules
└── 📄 README.md                 # This file
```

---

## 🎯 Usage Examples

### Example 1: Check Product Availability

```python
User: "Do you have the iPhone 15 Pro in stock?"

Agent: Product: iPhone 15 Pro (PROD002)
✅ IN STOCK

📦 Stock Information:
- Available: 50 units
- Reserved: 0 units
- Total Stock: 50 units
- Price: $999.99
- Category: Electronics
```

### Example 2: Search Products by Category

```python
User: "Show me all electronics"

Agent: Products in 'Electronics' category (5 items):

✅ MacBook Pro 14-inch (ID: PROD001)
   Price: $1,999.99 | Available: 25 units

✅ iPhone 15 Pro (ID: PROD002)
   Price: $999.99 | Available: 50 units

⚠️ AirPods Pro (2nd Gen) (ID: PROD003)
   Price: $249.99 | Available: 3 units
   LOW STOCK WARNING!
```

### Example 3: Order Tracking

```python
User: "Where is my order #ORD1299?"

Agent: Order ORD1299 status:
- Status: SHIPPED
- Tracking Number: TRK123456789
- Expected Delivery: Friday, January 25, 2026
- Total: $1,024.99
```

### Example 4: Refund Request

```python
User: "I want a refund for order #ORD1299"

Agent: Refund initiated successfully!
- Order ID: ORD1299
- Refund Amount: $1,024.99
- Refund ID: REF-78910
- Status: PENDING

The refund will be processed within 5-7 business days.
```

### Example 5: Reserve Product (Checkout)

```python
User: "Reserve 2 AirPods Pro for me"

Agent: ✅ Reservation Successful!

Product ID: PROD003
Quantity Reserved: 2 units
Customer: CUST001
Reservation ID: 123

⏰ This reservation will expire in 15 minutes
Please complete your purchase before it expires.
```

---

## 🔧 Configuration

### Agent Customization

Modify agent behavior in `agents_config.py`:

```python
inventory_agent = Agent(
    name="Inventory Agent",
    instructions="""You are an inventory specialist...""",
    tools=[
        check_product_availability,
        search_products_by_name,
        reserve_product,
        # Add more tools here
    ]
)
```

### Adding New Products

Use the database interface:

```python
from database import OrderDatabase

db = OrderDatabase()
db.add_product(
    product_id="PROD999",
    name="New Product",
    description="Product description",
    price=99.99,
    category="Electronics",
    stock_quantity=100
)
```

### Adjusting Stock Thresholds

Modify low stock alerts:

```python
db.add_product(
    product_id="PROD001",
    name="MacBook Pro",
    # ... other fields
    low_stock_threshold=5  # Alert when ≤ 5 units
)
```

---

## 🗄️ Database

### Tables

| Table | Purpose |
|-------|---------|
| `customers` | Customer profiles and information |
| `orders` | Order history and tracking |
| `inventory` | Product catalog and stock levels |
| `refunds` | Refund requests and processing |
| `reservations` | Temporary stock holds (15-min expiry) |
| `stock_movements` | Complete audit trail of inventory changes |
| `conversations` | Customer support chat history |
| `product_categories` | Product category definitions |

### Key Relationships

- **Orders** → **Customers** (Many-to-One)
- **Refunds** → **Orders** (Many-to-One)
- **Reservations** → **Inventory** + **Customers** (Many-to-One each)
- **Stock Movements** → **Inventory** (Many-to-One)

### Sample Queries

**Get customer order history:**
```sql
SELECT * FROM orders 
WHERE customer_id = 'CUST001' 
ORDER BY created_at DESC;
```

**Check low stock products:**
```sql
SELECT * FROM inventory 
WHERE (stock_quantity - reserved_quantity) <= low_stock_threshold;
```

**View stock movement audit:**
```sql
SELECT * FROM stock_movements 
WHERE product_id = 'PROD001' 
ORDER BY timestamp DESC;
```

---

## 🛠️ Tools Available

### Order Management Tools
- `check_order_status(order_id)` - Get order details and tracking
- `get_customer_orders(customer_id)` - List all customer orders
- `update_order_tracking(order_id, tracking, delivery_date)` - Update shipping info
- `create_new_order(customer_id, items, total)` - Create new order

### Inventory Tools
- `check_product_availability(product_id)` - Check stock levels
- `search_products_by_name(search_term)` - Search products
- `search_products_by_category(category)` - Filter by category
- `get_product_details(product_id)` - Get complete product info
- `reserve_product(product_id, quantity, customer_id)` - Reserve stock
- `cancel_reservation(reservation_id)` - Release reservation
- `update_product_stock(product_id, quantity_change, reason)` - Update inventory
- `get_low_stock_alerts()` - Get products needing restock
- `add_new_product(...)` - Add product to catalog

### Refund Tools
- `process_refund(order_id, reason)` - Initiate refund
- `check_refund_status(refund_id)` - Check refund progress

---

## 🚀 Deployment

### Deploy to Hugging Face Spaces

1. **Create a Space on Hugging Face**
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Choose "Gradio" as SDK
   - Name it `ecommerce-support`

2. **Push your code**
   ```bash
   git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/ecommerce-support
   git push hf main
   ```

3. **Add secrets in Space Settings**
   - `OPENAI_API_KEY` - Your OpenAI API key
   - `SUPABASE_URL` - Your Supabase project URL
   - `SUPABASE_KEY` - Your Supabase anon/public key

4. **Wait for build** (~2-3 minutes)

5. **Your agent is live!** 🎉
   - Access at: `https://huggingface.co/spaces/YOUR_USERNAME/ecommerce-support`

### Deploy to Other Platforms

The application can also be deployed to:
- **Render** - For production hosting
- **Railway** - Easy deployment with databases
- **Vercel** - For serverless deployment
- **AWS/GCP/Azure** - Enterprise hosting

---

## 🧪 Testing

### Run CLI Tests

```bash
python main.py
```

### Run Web Interface

```bash
python app.py
```

### Test Database Connection

```python
from database import OrderDatabase

db = OrderDatabase()
print(db.get_product("PROD001"))
```

### Test Individual Tools

```python
from inventory_tools import check_product_availability

result = check_product_availability("PROD001")
print(result)
```

---

## 📊 Performance

### Response Times
- **Simple queries** (product availability): ~1-2 seconds
- **Complex queries** (multi-step reservations): ~2-4 seconds
- **Database operations**: <100ms average

### Scalability
- **Concurrent users**: Supports multiple simultaneous conversations
- **Database**: PostgreSQL handles 1000+ TPS
- **Agent routing**: Sub-second decision making

---

## 🔐 Security

### Best Practices Implemented
- ✅ Environment variables for sensitive data
- ✅ No API keys in code
- ✅ Input validation on all database operations
- ✅ SQL injection prevention (parameterized queries)
- ✅ Error handling with safe messages
- ✅ Audit logging for all inventory changes

### Data Privacy
- Customer conversations stored securely
- PII (email, phone) encrypted at rest in Supabase
- No data sharing with third parties

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Areas for Contribution
- 🎨 UI/UX improvements
- 🌐 Multi-language support
- 📧 Email notification system
- 📊 Analytics dashboard
- 🤖 Additional agent types
- ✅ More test coverage

---

## 🐛 Troubleshooting

### Common Issues

**Issue: "Module not found" error**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue: "Supabase connection failed"**
```bash
# Solution: Check .env file
# Verify SUPABASE_URL and SUPABASE_KEY are correct
```

**Issue: "Product not found"**
```bash
# Solution: Load sample data
python setup_inventory_data.py
```

**Issue: "OpenAI API error"**
```bash
# Solution: Verify API key in .env
# Check OpenAI account has credits
```

**Issue: Database tables don't exist**
```bash
# Solution: Run SQL schema in Supabase SQL Editor
# See installation step 5
```

---

## 📚 Documentation

- **[Setup Guide](docs/SETUP.md)** - Detailed installation instructions
- **[Database Schema](docs/DATABASE_SCHEMA.md)** - Complete database documentation
- **[API Reference](docs/API_REFERENCE.md)** - Tool and function documentation
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment steps

---

## 🎓 Learning Resources

### Built With
- [OpenAI Swarm](https://github.com/openai/swarm) - Multi-agent orchestration
- [Supabase](https://supabase.com/docs) - PostgreSQL database
- [Gradio](https://gradio.app/docs/) - Web interface framework
- [Python AsyncIO](https://docs.python.org/3/library/asyncio.html) - Async operations

### Recommended Reading
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Agent Design Patterns](https://www.anthropic.com/research/building-effective-agents)
- [PostgreSQL Best Practices](https://wiki.postgresql.org/wiki/Don%27t_Do_This)

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨💻 Author

**Renzo**  
- GitHub: [@renzotjpro](https://github.com/renzotjpro)
- LinkedIn: [https://www.linkedin.com/in/renzotellojimenez/](https://www.linkedin.com/in/renzotellojimenez/)
- Email: [renzotj@outlook.com](mailto:renzotj@outlook.com)

---

## 🙏 Acknowledgments

- **OpenAI** for the Swarm framework and GPT models
- **Supabase** for the excellent PostgreSQL hosting
- **Gradio** for the user-friendly interface framework
- **Anthropic** for Claude assistance in development

---

## 📈 Roadmap

### Phase 1 - Core Features ✅
- [x] Multi-agent architecture
- [x] Order tracking
- [x] Inventory management
- [x] Refund processing
- [x] Stock reservations
- [x] Web interface

### Phase 2 - Enhancements 🚧
- [ ] Email notifications
- [ ] Product recommendations
- [ ] Analytics dashboard
- [ ] Multi-language support
- [ ] Voice interface

### Phase 3 - Advanced Features 🔮
- [ ] Machine learning for demand forecasting
- [ ] Automated restocking suggestions
- [ ] Customer sentiment analysis
- [ ] Integration with shipping APIs
- [ ] Mobile app

---

## 💬 Support

Need help? Here's how to get support:

1. **📖 Check the documentation** in the `docs/` folder
2. **🐛 Open an issue** on GitHub for bugs
3. **💡 Start a discussion** for feature requests
4. **📧 Email me** for private inquiries

---

## ⭐ Star History

If you find this project helpful, please consider giving it a star! ⭐

---

<div align="center">

**Made with ❤️ and AI**

[Report Bug](https://github.com/renzotjpro/ecommerce_support/issues) · [Request Feature](https://github.com/renzotjpro/ecommerce_support/issues) · [Documentation](docs/)

</div>