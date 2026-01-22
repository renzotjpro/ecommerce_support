"""
Setup script to populate the inventory database with sample e-commerce products.
Run this after creating the database schema in Supabase.
"""

from .models import OrderDatabase
from dotenv import load_dotenv

load_dotenv()

def setup_sample_inventory():
    """Add sample products to the inventory"""
    
    db = OrderDatabase()
    
    print("🛍️ Setting up E-Commerce Inventory...")
    print("=" * 50)
    
    # Sample products across different categories
    products = [
        # Electronics
        {
            "product_id": "PROD001",
            "name": "MacBook Pro 14-inch",
            "description": "Apple M2 Pro chip, 16GB RAM, 512GB SSD. Perfect for professional work and creative tasks.",
            "price": 1999.99,
            "category": "Electronics",
            "stock_quantity": 25,
            "low_stock_threshold": 5
        },
        {
            "product_id": "PROD002",
            "name": "iPhone 15 Pro",
            "description": "Latest iPhone with A17 Pro chip, 256GB storage, titanium design.",
            "price": 999.99,
            "category": "Electronics",
            "stock_quantity": 50,
            "low_stock_threshold": 10
        },
        {
            "product_id": "PROD003",
            "name": "AirPods Pro (2nd Gen)",
            "description": "Active noise cancellation, spatial audio, USB-C charging.",
            "price": 249.99,
            "category": "Electronics",
            "stock_quantity": 3,  # Low stock!
            "low_stock_threshold": 10
        },
        {
            "product_id": "PROD004",
            "name": "Samsung 4K Smart TV 55-inch",
            "description": "Crystal UHD display, HDR support, built-in streaming apps.",
            "price": 599.99,
            "category": "Electronics",
            "stock_quantity": 15,
            "low_stock_threshold": 5
        },
        {
            "product_id": "PROD005",
            "name": "Sony WH-1000XM5 Headphones",
            "description": "Industry-leading noise cancellation, 30-hour battery life.",
            "price": 399.99,
            "category": "Electronics",
            "stock_quantity": 0,  # Out of stock!
            "low_stock_threshold": 8
        },
        
        # Clothing
        {
            "product_id": "PROD101",
            "name": "Classic Denim Jacket",
            "description": "100% cotton denim, available in multiple sizes. Timeless style.",
            "price": 79.99,
            "category": "Clothing",
            "stock_quantity": 100,
            "low_stock_threshold": 20
        },
        {
            "product_id": "PROD102",
            "name": "Running Shoes - ProRun Elite",
            "description": "Lightweight, breathable, excellent cushioning for long runs.",
            "price": 129.99,
            "category": "Clothing",
            "stock_quantity": 45,
            "low_stock_threshold": 15
        },
        {
            "product_id": "PROD103",
            "name": "Wool Sweater",
            "description": "Merino wool, soft and warm, perfect for winter.",
            "price": 89.99,
            "category": "Clothing",
            "stock_quantity": 8,  # Low stock!
            "low_stock_threshold": 10
        },
        
        # Home & Kitchen
        {
            "product_id": "PROD201",
            "name": "Espresso Machine - BrewMaster Pro",
            "description": "15-bar pressure, milk frother included, makes café-quality coffee at home.",
            "price": 299.99,
            "category": "Home & Kitchen",
            "stock_quantity": 20,
            "low_stock_threshold": 5
        },
        {
            "product_id": "PROD202",
            "name": "Robot Vacuum Cleaner",
            "description": "Smart navigation, auto-charging, works with Alexa and Google Home.",
            "price": 349.99,
            "category": "Home & Kitchen",
            "stock_quantity": 12,
            "low_stock_threshold": 5
        },
        {
            "product_id": "PROD203",
            "name": "Non-Stick Cookware Set",
            "description": "10-piece set, dishwasher safe, includes pots, pans, and utensils.",
            "price": 149.99,
            "category": "Home & Kitchen",
            "stock_quantity": 30,
            "low_stock_threshold": 10
        },
        
        # Sports & Outdoors
        {
            "product_id": "PROD301",
            "name": "Yoga Mat Premium",
            "description": "6mm thick, non-slip surface, eco-friendly materials.",
            "price": 39.99,
            "category": "Sports & Outdoors",
            "stock_quantity": 75,
            "low_stock_threshold": 20
        },
        {
            "product_id": "PROD302",
            "name": "Camping Tent 4-Person",
            "description": "Waterproof, easy setup, includes carrying bag.",
            "price": 199.99,
            "category": "Sports & Outdoors",
            "stock_quantity": 5,  # Low stock!
            "low_stock_threshold": 8
        },
        {
            "product_id": "PROD303",
            "name": "Hiking Backpack 40L",
            "description": "Durable, multiple compartments, ergonomic design.",
            "price": 89.99,
            "category": "Sports & Outdoors",
            "stock_quantity": 18,
            "low_stock_threshold": 10
        },
        
        # Books
        {
            "product_id": "PROD401",
            "name": "The Art of AI Engineering",
            "description": "Comprehensive guide to building AI applications.",
            "price": 49.99,
            "category": "Books",
            "stock_quantity": 40,
            "low_stock_threshold": 10
        },
        {
            "product_id": "PROD402",
            "name": "Python for Automation",
            "description": "Learn to automate tasks with Python, from basics to advanced.",
            "price": 39.99,
            "category": "Books",
            "stock_quantity": 60,
            "low_stock_threshold": 15
        }
    ]
    
    # Add products to database
    added = 0
    failed = 0
    
    for product in products:
        print(f"\nAdding: {product['name']}")
        result = db.add_product(**product)
        
        if result["success"]:
            added += 1
            stock_status = "✅ IN STOCK" if product["stock_quantity"] > 0 else "❌ OUT OF STOCK"
            if product["stock_quantity"] <= product["low_stock_threshold"] and product["stock_quantity"] > 0:
                stock_status = "⚠️ LOW STOCK"
            print(f"  {stock_status} - {product['stock_quantity']} units | ${product['price']}")
        else:
            failed += 1
            print(f"  ❌ Failed: {result.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 50)
    print(f"✅ Successfully added: {added} products")
    if failed > 0:
        print(f"❌ Failed to add: {failed} products")
    
    # Show summary
    print("\n📊 Inventory Summary:")
    print("-" * 50)
    
    categories = {}
    for p in products:
        cat = p["category"]
        if cat not in categories:
            categories[cat] = {"count": 0, "total_value": 0}
        categories[cat]["count"] += 1
        categories[cat]["total_value"] += p["price"] * p["stock_quantity"]
    
    for category, stats in categories.items():
        print(f"{category}: {stats['count']} products | Inventory value: ${stats['total_value']:,.2f}")
    
    # Check for low stock items
    print("\n⚠️ Checking for low stock items...")
    low_stock_result = db.get_low_stock_products()
    
    if low_stock_result["success"] and low_stock_result["products"]:
        print(f"\n🔴 {len(low_stock_result['products'])} product(s) need restocking:")
        for p in low_stock_result["products"]:
            print(f"  - {p['name']}: {p['available_quantity']} units (threshold: {p['threshold']})")
    else:
        print("✅ All products are adequately stocked!")


def setup_sample_customers():
    """Add sample customers for testing"""
    
    db = OrderDatabase()
    
    print("\n\n👥 Setting up Sample Customers...")
    print("=" * 50)
    
    customers = [
        {
            "customer_id": "CUST001",
            "email": "john.doe@example.com",
            "name": "John Doe"
        },
        {
            "customer_id": "CUST002",
            "email": "jane.smith@example.com",
            "name": "Jane Smith"
        },
        {
            "customer_id": "CUST003",
            "email": "bob.wilson@example.com",
            "name": "Bob Wilson"
        }
    ]
    
    for customer in customers:
        result = db.create_customer(**customer)
        if result["success"]:
            print(f"✅ Added customer: {customer['name']} ({customer['customer_id']})")
        else:
            print(f"❌ Failed to add {customer['name']}: {result.get('error', '')}")


if __name__ == "__main__":
    print("🚀 E-Commerce Inventory Setup")
    print("=" * 50)
    print("\nThis script will populate your database with sample products.")
    print("Make sure you've already created the database tables in Supabase!\n")
    
    input("Press Enter to continue...")
    
    # Setup inventory
    setup_sample_inventory()
    
    # Setup customers
    setup_sample_customers()
    
    print("\n" + "=" * 50)
    print("✅ Setup Complete!")
    print("\nYou can now run your e-commerce agent with:")
    print("  python main.py")
    print("\nOr test with Gradio:")
    print("  python app.py")