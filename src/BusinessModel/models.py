"""
Database Models and Operations
===============================

This module contains all database operations for the e-commerce support system.
It uses Supabase (PostgreSQL) for data persistence.

Classes:
    - OrderDatabase: Main database operations class
    - CustomerOperations: Customer-related operations
    - InventoryOperations: Inventory-related operations
    - OrderOperations: Order-related operations

Usage:
    from src.database.models import OrderDatabase
    
    db = OrderDatabase()
    result = db.get_product("PROD001")
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional, Any

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    raise ValueError(
        "Missing Supabase credentials. Please set SUPABASE_URL and SUPABASE_KEY in .env file"
    )

supabase: Client = create_client(supabase_url, supabase_key)


# ============================================
# MAIN DATABASE CLASS
# ============================================

class OrderDatabase:
    """
    Main database operations class for the e-commerce system.
    
    This class handles all interactions with the Supabase PostgreSQL database,
    including customers, orders, inventory, refunds, and conversations.
    
    Attributes:
        supabase (Client): Supabase client instance
    
    Example:
        >>> db = OrderDatabase()
        >>> product = db.get_product("PROD001")
        >>> print(product["name"])
        'MacBook Pro 14-inch'
    """
    
    def __init__(self):
        """Initialize database connection"""
        self.supabase = supabase
    
    # ============================================
    # CUSTOMER OPERATIONS
    # ============================================
    
    def create_customer(
        self, 
        customer_id: str, 
        email: str, 
        name: str,
        phone: Optional[str] = None,
        address: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new customer in the database.
        
        Args:
            customer_id: Unique customer identifier (e.g., "CUST001")
            email: Customer email address (must be unique)
            name: Customer full name
            phone: Optional phone number
            address: Optional street address
            
        Returns:
            Dict with 'success' bool and 'customer' data or 'error' message
            
        Example:
            >>> db.create_customer("CUST001", "john@example.com", "John Doe")
            {'success': True, 'customer': {...}}
        """
        try:
            data = {
                "customer_id": customer_id,
                "email": email,
                "name": name,
                "phone": phone,
                "address": address,
                "created_at": datetime.now().isoformat()
            }
            
            result = self.supabase.table("customers").insert(data).execute()
            return {"success": True, "customer": result.data[0]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """
        Get customer information by customer ID.
        
        Args:
            customer_id: The customer identifier
            
        Returns:
            Dict with customer information or error
        """
        try:
            result = self.supabase.table("customers")\
                .select("*")\
                .eq("customer_id", customer_id)\
                .execute()
            
            if result.data:
                return {"success": True, "customer": result.data[0]}
            else:
                return {"success": False, "error": "Customer not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_customer_orders(self, customer_id: str) -> Dict[str, Any]:
        """
        Get all orders for a specific customer.
        
        Args:
            customer_id: The customer identifier
            
        Returns:
            Dict with list of orders or error
        """
        try:
            result = self.supabase.table("orders")\
                .select("*")\
                .eq("customer_id", customer_id)\
                .order("created_at", desc=True)\
                .execute()
            
            return {"success": True, "orders": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ============================================
    # ORDER OPERATIONS
    # ============================================
    
    def create_order(
        self, 
        order_id: str, 
        customer_id: str, 
        items: List[Dict], 
        total: float
    ) -> Dict[str, Any]:
        """
        Create a new order in the database.
        
        Args:
            order_id: Unique order identifier (e.g., "ORD1299")
            customer_id: Customer who placed the order
            items: List of order items with product details
            total: Total order amount
            
        Returns:
            Dict with success status and order data
            
        Example:
            >>> items = [{"product_id": "PROD001", "quantity": 1, "price": 999.99}]
            >>> db.create_order("ORD001", "CUST001", items, 999.99)
        """
        try:
            data = {
                "order_id": order_id,
                "customer_id": customer_id,
                "items": json.dumps(items),
                "total": total,
                "status": "pending",
                "created_at": datetime.now().isoformat(),
                "tracking_number": None,
                "expected_delivery": None
            }
            
            result = self.supabase.table("orders").insert(data).execute()
            return {"success": True, "order": result.data[0]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_order_status(self, order_id: str) -> Dict[str, Any]:
        """
        Retrieve order status and details.
        
        Args:
            order_id: The order identifier
            
        Returns:
            Dict with order information including status, tracking, items
        """
        try:
            result = self.supabase.table("orders")\
                .select("*")\
                .eq("order_id", order_id)\
                .execute()
            
            if result.data:
                order = result.data[0]
                return {
                    "success": True,
                    "order_id": order["order_id"],
                    "status": order["status"],
                    "tracking_number": order.get("tracking_number"),
                    "expected_delivery": order.get("expected_delivery"),
                    "total": order["total"],
                    "items": json.loads(order["items"])
                }
            else:
                return {"success": False, "error": "Order not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def update_order_status(
        self, 
        order_id: str, 
        status: str, 
        tracking_number: Optional[str] = None, 
        expected_delivery: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update order status and tracking information.
        
        Args:
            order_id: Order to update
            status: New status (pending, processing, shipped, delivered, etc.)
            tracking_number: Optional shipping tracking number
            expected_delivery: Optional expected delivery date
            
        Returns:
            Dict with success status and updated order
        """
        try:
            update_data = {"status": status}
            
            if tracking_number:
                update_data["tracking_number"] = tracking_number
            if expected_delivery:
                update_data["expected_delivery"] = expected_delivery
            
            result = self.supabase.table("orders")\
                .update(update_data)\
                .eq("order_id", order_id)\
                .execute()
            
            return {"success": True, "order": result.data[0]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ============================================
    # REFUND OPERATIONS
    # ============================================
    
    def create_refund(self, order_id: str, reason: str, amount: float) -> Dict[str, Any]:
        """
        Initiate a refund for an order.
        
        Args:
            order_id: Order to refund
            reason: Reason for refund
            amount: Refund amount
            
        Returns:
            Dict with refund details or error
        """
        try:
            # First check if order exists
            order_result = self.get_order_status(order_id)
            if not order_result["success"]:
                return {"success": False, "error": "Order not found"}
            
            # Create refund record
            refund_data = {
                "order_id": order_id,
                "reason": reason,
                "amount": amount,
                "status": "pending",
                "created_at": datetime.now().isoformat()
            }
            
            result = self.supabase.table("refunds").insert(refund_data).execute()
            
            # Update order status to refunded
            self.update_order_status(order_id, "refunded")
            
            return {
                "success": True,
                "refund_id": result.data[0]["id"],
                "amount": amount,
                "status": "pending"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_refund_status(self, refund_id: int) -> Dict[str, Any]:
        """
        Check refund status.
        
        Args:
            refund_id: The refund identifier
            
        Returns:
            Dict with refund information
        """
        try:
            result = self.supabase.table("refunds")\
                .select("*")\
                .eq("id", refund_id)\
                .execute()
            
            if result.data:
                return {"success": True, "refund": result.data[0]}
            else:
                return {"success": False, "error": "Refund not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ============================================
    # INVENTORY OPERATIONS
    # ============================================
    
    def add_product(
        self, 
        product_id: str, 
        name: str, 
        description: str, 
        price: float, 
        category: str, 
        stock_quantity: int,
        low_stock_threshold: int = 10
    ) -> Dict[str, Any]:
        """
        Add a new product to inventory.
        
        Args:
            product_id: Unique product identifier
            name: Product name
            description: Product description
            price: Product price
            category: Product category
            stock_quantity: Initial stock quantity
            low_stock_threshold: When to alert for low stock
            
        Returns:
            Dict with success status and product data
        """
        try:
            data = {
                "product_id": product_id,
                "name": name,
                "description": description,
                "price": price,
                "category": category,
                "stock_quantity": stock_quantity,
                "reserved_quantity": 0,
                "low_stock_threshold": low_stock_threshold,
                "is_active": True,
                "created_at": datetime.now().isoformat()
            }
            
            result = self.supabase.table("inventory").insert(data).execute()
            return {"success": True, "product": result.data[0]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_product(self, product_id: str) -> Dict[str, Any]:
        """
        Get product details and availability.
        
        Args:
            product_id: The product identifier
            
        Returns:
            Dict with complete product information including:
            - Basic info (name, price, description)
            - Stock levels (total, reserved, available)
            - Availability status (in stock, low stock)
        """
        try:
            result = self.supabase.table("inventory")\
                .select("*")\
                .eq("product_id", product_id)\
                .execute()
            
            if result.data:
                product = result.data[0]
                available = product["stock_quantity"] - product["reserved_quantity"]
                
                return {
                    "success": True,
                    "product_id": product["product_id"],
                    "name": product["name"],
                    "description": product["description"],
                    "price": product["price"],
                    "category": product["category"],
                    "stock_quantity": product["stock_quantity"],
                    "reserved_quantity": product["reserved_quantity"],
                    "available_quantity": available,
                    "is_in_stock": available > 0,
                    "is_low_stock": available <= product["low_stock_threshold"],
                    "low_stock_threshold": product["low_stock_threshold"],
                    "is_active": product["is_active"]
                }
            else:
                return {"success": False, "error": "Product not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def search_products(
        self, 
        search_term: Optional[str] = None, 
        category: Optional[str] = None, 
        in_stock_only: bool = False
    ) -> Dict[str, Any]:
        """
        Search for products by name or category.
        
        Args:
            search_term: Product name or keyword to search
            category: Filter by category
            in_stock_only: If True, only return products with stock > 0
            
        Returns:
            Dict with list of matching products
        """
        try:
            query = self.supabase.table("inventory").select("*")
            
            if search_term:
                query = query.ilike("name", f"%{search_term}%")
            
            if category:
                query = query.eq("category", category)
            
            if in_stock_only:
                query = query.gt("stock_quantity", 0)
            
            query = query.eq("is_active", True)
            result = query.execute()
            
            products = []
            for product in result.data:
                available = product["stock_quantity"] - product["reserved_quantity"]
                products.append({
                    "product_id": product["product_id"],
                    "name": product["name"],
                    "price": product["price"],
                    "category": product["category"],
                    "available_quantity": available,
                    "is_in_stock": available > 0
                })
            
            return {"success": True, "products": products}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def update_stock(
        self, 
        product_id: str, 
        quantity_change: int, 
        reason: str = "manual_update"
    ) -> Dict[str, Any]:
        """
        Update stock quantity (positive to add, negative to remove).
        
        Args:
            product_id: Product to update
            quantity_change: Amount to change (+ to add, - to remove)
            reason: Reason for stock change
            
        Returns:
            Dict with previous stock, new stock, and change amount
        """
        try:
            # Get current product
            product_result = self.get_product(product_id)
            if not product_result["success"]:
                return {"success": False, "error": "Product not found"}
            
            current_stock = product_result["stock_quantity"]
            new_stock = current_stock + quantity_change
            
            if new_stock < 0:
                return {"success": False, "error": "Insufficient stock"}
            
            # Update stock
            result = self.supabase.table("inventory")\
                .update({"stock_quantity": new_stock})\
                .eq("product_id", product_id)\
                .execute()
            
            # Log the stock movement
            self.log_stock_movement(
                product_id, 
                quantity_change, 
                reason, 
                current_stock, 
                new_stock
            )
            
            return {
                "success": True,
                "product_id": product_id,
                "previous_stock": current_stock,
                "new_stock": new_stock,
                "change": quantity_change
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def reserve_stock(
        self, 
        product_id: str, 
        quantity: int, 
        customer_id: str
    ) -> Dict[str, Any]:
        """
        Reserve stock for a customer (during checkout).
        Reservation expires after 15 minutes.
        
        Args:
            product_id: Product to reserve
            quantity: Number of units to reserve
            customer_id: Customer making the reservation
            
        Returns:
            Dict with reservation details including expiry time
        """
        try:
            # Get current product
            product_result = self.get_product(product_id)
            if not product_result["success"]:
                return {"success": False, "error": "Product not found"}
            
            available = product_result["available_quantity"]
            
            if available < quantity:
                return {
                    "success": False, 
                    "error": f"Insufficient stock. Available: {available}, Requested: {quantity}"
                }
            
            # Update reserved quantity
            new_reserved = product_result["reserved_quantity"] + quantity
            
            result = self.supabase.table("inventory")\
                .update({"reserved_quantity": new_reserved})\
                .eq("product_id", product_id)\
                .execute()
            
            # Create reservation record
            reservation_data = {
                "product_id": product_id,
                "customer_id": customer_id,
                "quantity": quantity,
                "status": "active",
                "expires_at": (datetime.now() + timedelta(minutes=15)).isoformat(),
                "created_at": datetime.now().isoformat()
            }
            
            reservation = self.supabase.table("reservations")\
                .insert(reservation_data)\
                .execute()
            
            return {
                "success": True,
                "reservation_id": reservation.data[0]["id"],
                "product_id": product_id,
                "quantity": quantity,
                "expires_at": reservation_data["expires_at"]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def release_reservation(self, reservation_id: int) -> Dict[str, Any]:
        """
        Release a reservation (if order is cancelled or expired).
        
        Args:
            reservation_id: The reservation to release
            
        Returns:
            Dict with success status
        """
        try:
            # Get reservation details
            reservation = self.supabase.table("reservations")\
                .select("*")\
                .eq("id", reservation_id)\
                .execute()
            
            if not reservation.data:
                return {"success": False, "error": "Reservation not found"}
            
            res_data = reservation.data[0]
            
            if res_data["status"] != "active":
                return {"success": False, "error": "Reservation already released"}
            
            # Get current product
            product = self.supabase.table("inventory")\
                .select("*")\
                .eq("product_id", res_data["product_id"])\
                .execute()
            
            if not product.data:
                return {"success": False, "error": "Product not found"}
            
            # Update reserved quantity
            new_reserved = max(0, product.data[0]["reserved_quantity"] - res_data["quantity"])
            
            self.supabase.table("inventory")\
                .update({"reserved_quantity": new_reserved})\
                .eq("product_id", res_data["product_id"])\
                .execute()
            
            # Mark reservation as released
            self.supabase.table("reservations")\
                .update({"status": "released"})\
                .eq("id", reservation_id)\
                .execute()
            
            return {"success": True, "message": "Reservation released successfully"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_low_stock_products(self) -> Dict[str, Any]:
        """
        Get products with stock below threshold.
        
        Returns:
            Dict with list of low stock products
        """
        try:
            result = self.supabase.table("inventory")\
                .select("*")\
                .eq("is_active", True)\
                .execute()
            
            low_stock = []
            for product in result.data:
                available = product["stock_quantity"] - product["reserved_quantity"]
                if available <= product["low_stock_threshold"]:
                    low_stock.append({
                        "product_id": product["product_id"],
                        "name": product["name"],
                        "available_quantity": available,
                        "threshold": product["low_stock_threshold"]
                    })
            
            return {"success": True, "products": low_stock}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def log_stock_movement(
        self, 
        product_id: str, 
        quantity_change: int, 
        reason: str, 
        previous_stock: int, 
        new_stock: int
    ) -> Dict[str, Any]:
        """
        Log stock movements for audit trail.
        
        Args:
            product_id: Product that changed
            quantity_change: Amount of change
            reason: Reason for change
            previous_stock: Stock before change
            new_stock: Stock after change
            
        Returns:
            Dict with success status
        """
        try:
            data = {
                "product_id": product_id,
                "quantity_change": quantity_change,
                "reason": reason,
                "previous_stock": previous_stock,
                "new_stock": new_stock,
                "timestamp": datetime.now().isoformat()
            }
            
            self.supabase.table("stock_movements").insert(data).execute()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ============================================
    # CONVERSATION OPERATIONS
    # ============================================
    
    def save_conversation(
        self, 
        customer_id: str, 
        message: str, 
        role: str
    ) -> Dict[str, Any]:
        """
        Save conversation messages.
        
        Args:
            customer_id: Customer in conversation
            message: Message content
            role: Message role (user, assistant, agent name)
            
        Returns:
            Dict with success status
        """
        try:
            data = {
                "customer_id": customer_id,
                "message": message,
                "role": role,
                "timestamp": datetime.now().isoformat()
            }
            
            result = self.supabase.table("conversations").insert(data).execute()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_conversation_history(
        self, 
        customer_id: str, 
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Retrieve conversation history for a customer.
        
        Args:
            customer_id: Customer identifier
            limit: Maximum number of messages to retrieve
            
        Returns:
            Dict with list of messages
        """
        try:
            result = self.supabase.table("conversations")\
                .select("*")\
                .eq("customer_id", customer_id)\
                .order("timestamp", desc=True)\
                .limit(limit)\
                .execute()
            
            return {"success": True, "messages": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}