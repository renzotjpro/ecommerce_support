from agents import function_tool
from src.BusinessModel.models import OrderDatabase

# Initialize database connection
db = OrderDatabase()

# ============ PRODUCT AVAILABILITY TOOLS ============

@function_tool
def check_product_availability(product_id: str) -> str:
    """
    Check if a product is in stock and get availability details.
    
    Args:
        product_id: The product ID (e.g., "PROD001")
    
    Returns:
        Product availability information including stock levels
    """
    result = db.get_product(product_id)
    
    if result["success"]:
        p = result
        status = "✅ IN STOCK" if p["is_in_stock"] else "❌ OUT OF STOCK"
        
        response = f"""Product: {p['name']} ({product_id})
{status}

📦 Stock Information:
- Available: {p['available_quantity']} units
- Reserved: {p['reserved_quantity']} units
- Total Stock: {p['stock_quantity']} units
- Price: ${p['price']:.2f}
- Category: {p['category']}
"""
        
        if p["is_low_stock"] and p["is_in_stock"]:
            response += f"\n⚠️ LOW STOCK WARNING: Only {p['available_quantity']} units remaining!"
        
        return response
    else:
        return f"Sorry, I couldn't find product {product_id}. {result.get('error', '')}"


@function_tool
def search_products_by_name(search_term: str, in_stock_only: bool = False) -> str:
    """
    Search for products by name.
    
    Args:
        search_term: Product name or keyword to search
        in_stock_only: If True, only show products in stock
    
    Returns:
        List of matching products with availability
    """
    result = db.search_products(search_term=search_term, in_stock_only=in_stock_only)
    
    if result["success"]:
        if not result["products"]:
            return f"No products found matching '{search_term}'."
        
        response = f"Found {len(result['products'])} product(s) matching '{search_term}':\n\n"
        
        for p in result["products"]:
            stock_icon = "✅" if p["is_in_stock"] else "❌"
            response += f"{stock_icon} {p['name']} (ID: {p['product_id']})\n"
            response += f"   Price: ${p['price']:.2f} | Available: {p['available_quantity']} units\n"
            response += f"   Category: {p['category']}\n\n"
        
        return response
    else:
        return f"Error searching products: {result.get('error', 'Unknown error')}"


@function_tool
def search_products_by_category(category: str, in_stock_only: bool = False) -> str:
    """
    Get all products in a specific category.
    
    Args:
        category: Category name (e.g., "Electronics", "Clothing")
        in_stock_only: If True, only show products in stock
    
    Returns:
        List of products in the category
    """
    result = db.search_products(category=category, in_stock_only=in_stock_only)
    
    if result["success"]:
        if not result["products"]:
            return f"No products found in category '{category}'."
        
        response = f"Products in '{category}' category ({len(result['products'])} items):\n\n"
        
        for p in result["products"]:
            stock_icon = "✅" if p["is_in_stock"] else "❌"
            response += f"{stock_icon} {p['name']} (ID: {p['product_id']})\n"
            response += f"   Price: ${p['price']:.2f} | Available: {p['available_quantity']} units\n\n"
        
        return response
    else:
        return f"Error searching category: {result.get('error', 'Unknown error')}"


@function_tool
def get_product_details(product_id: str) -> str:
    """
    Get complete product information including description and pricing.
    
    Args:
        product_id: The product ID
    
    Returns:
        Detailed product information
    """
    result = db.get_product(product_id)
    
    if result["success"]:
        p = result
        
        response = f"""📦 Product Details
        
Name: {p['name']}
ID: {p['product_id']}
Price: ${p['price']:.2f}
Category: {p['category']}

Description:
{p['description']}

📊 Inventory Status:
- Available: {p['available_quantity']} units
- Reserved: {p['reserved_quantity']} units
- Total in Stock: {p['stock_quantity']} units
- Status: {'✅ IN STOCK' if p['is_in_stock'] else '❌ OUT OF STOCK'}
"""
        
        if p["is_low_stock"] and p["is_in_stock"]:
            response += f"\n⚠️ LOW STOCK: Only {p['available_quantity']} units left!"
        
        return response
    else:
        return f"Product {product_id} not found. {result.get('error', '')}"


# ============ STOCK RESERVATION TOOLS ============

@function_tool
def reserve_product(product_id: str, quantity: int, customer_id: str) -> str:
    """
    Reserve stock for a customer during checkout (holds for 15 minutes).
    
    Args:
        product_id: The product to reserve
        quantity: Number of units to reserve
        customer_id: Customer ID making the reservation
    
    Returns:
        Reservation confirmation or error message
    """
    result = db.reserve_stock(product_id, quantity, customer_id)
    
    if result["success"]:
        return f"""✅ Reservation Successful!

Product ID: {product_id}
Quantity Reserved: {quantity} units
Customer: {customer_id}
Reservation ID: {result['reservation_id']}

⏰ This reservation will expire in 15 minutes: {result['expires_at']}
Please complete your purchase before the reservation expires."""
    else:
        return f"❌ Unable to reserve product: {result.get('error', 'Unknown error')}"


@function_tool
def cancel_reservation(reservation_id: int) -> str:
    """
    Cancel a product reservation and return stock to available inventory.
    
    Args:
        reservation_id: The reservation ID to cancel
    
    Returns:
        Cancellation confirmation
    """
    result = db.release_reservation(reservation_id)
    
    if result["success"]:
        return f"✅ Reservation #{reservation_id} has been cancelled. Stock returned to inventory."
    else:
        return f"❌ Unable to cancel reservation: {result.get('error', 'Unknown error')}"


# ============ STOCK MANAGEMENT TOOLS ============

@function_tool
def update_product_stock(product_id: str, quantity_change: int, reason: str = "manual adjustment") -> str:
    """
    Add or remove stock from inventory (for staff use).
    
    Args:
        product_id: The product ID
        quantity_change: Positive number to add stock, negative to remove
        reason: Reason for the change (e.g., "restock", "damaged goods")
    
    Returns:
        Stock update confirmation
    """
    result = db.update_stock(product_id, quantity_change, reason)
    
    if result["success"]:
        action = "added to" if quantity_change > 0 else "removed from"
        
        return f"""✅ Stock Updated Successfully

Product ID: {product_id}
Previous Stock: {result['previous_stock']} units
Change: {abs(quantity_change)} units {action} inventory
New Stock: {result['new_stock']} units
Reason: {reason}
"""
    else:
        return f"❌ Unable to update stock: {result.get('error', 'Unknown error')}"


@function_tool
def get_low_stock_alerts() -> str:
    """
    Get all products that are running low on stock.
    
    Returns:
        List of products below their low stock threshold
    """
    result = db.get_low_stock_products()
    
    if result["success"]:
        if not result["products"]:
            return "✅ All products are adequately stocked!"
        
        response = f"⚠️ LOW STOCK ALERT - {len(result['products'])} product(s) need restocking:\n\n"
        
        for p in result["products"]:
            response += f"🔴 {p['name']} (ID: {p['product_id']})\n"
            response += f"   Available: {p['available_quantity']} units\n"
            response += f"   Threshold: {p['threshold']} units\n"
            response += f"   Action needed: Restock recommended\n\n"
        
        return response
    else:
        return f"Error checking stock levels: {result.get('error', 'Unknown error')}"


# ============ PRODUCT MANAGEMENT TOOLS ============

@function_tool
def add_new_product(product_id: str, name: str, description: str, 
                   price: float, category: str, initial_stock: int = 0) -> str:
    """
    Add a new product to the inventory system.
    
    Args:
        product_id: Unique product identifier
        name: Product name
        description: Product description
        price: Product price
        category: Product category
        initial_stock: Starting stock quantity (default: 0)
    
    Returns:
        Confirmation of product creation
    """
    result = db.add_product(
        product_id=product_id,
        name=name,
        description=description,
        price=price,
        category=category,
        stock_quantity=initial_stock
    )
    
    if result["success"]:
        return f"""✅ New Product Added Successfully!

Product ID: {product_id}
Name: {name}
Price: ${price:.2f}
Category: {category}
Initial Stock: {initial_stock} units

The product is now available in the inventory system."""
    else:
        return f"❌ Unable to add product: {result.get('error', 'Unknown error')}"