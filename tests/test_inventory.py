"""
Inventory Management Test Suite
================================

This module contains comprehensive tests for the inventory management system.

Test Coverage:
    - Product CRUD operations
    - Stock availability checks
    - Product search functionality
    - Stock reservations
    - Stock updates
    - Low stock alerts
    - Edge cases and error handling

Usage:
    # Run all tests
    pytest tests/test_inventory.py
    
    # Run specific test
    pytest tests/test_inventory.py::TestProductOperations::test_add_product
    
    # Run with verbose output
    pytest tests/test_inventory.py -v
    
    # Run with coverage
    pytest tests/test_inventory.py --cov=database
"""

import pytest
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.BusinessModel.models import OrderDatabase

# ============================================
# FIXTURES
# ============================================

@pytest.fixture
def db():
    """
    Create a database instance for testing.
    
    Returns:
        OrderDatabase: Database instance
    """
    return OrderDatabase()


@pytest.fixture
def sample_product():
    """
    Sample product data for testing.
    
    Returns:
        dict: Product information
    """
    return {
        "product_id": "TEST_PROD_001",
        "name": "Test Laptop",
        "description": "High-performance laptop for testing",
        "price": 999.99,
        "category": "Electronics",
        "stock_quantity": 50,
        "low_stock_threshold": 10
    }


@pytest.fixture
def sample_customer():
    """
    Sample customer data for testing.
    
    Returns:
        dict: Customer information
    """
    return {
        "customer_id": "TEST_CUST_001",
        "email": "test.customer@example.com",
        "name": "Test Customer"
    }


@pytest.fixture
def cleanup_test_data(db):
    """
    Cleanup fixture that runs after each test.
    Removes test data from database.
    """
    yield
    
    # Cleanup code runs after test
    try:
        # Delete test products
        db.supabase.table("inventory").delete().ilike("product_id", "TEST_%").execute()
        # Delete test customers
        db.supabase.table("customers").delete().ilike("customer_id", "TEST_%").execute()
        # Delete test reservations
        db.supabase.table("reservations").delete().ilike("customer_id", "TEST_%").execute()
    except Exception as e:
        print(f"Cleanup warning: {e}")


# ============================================
# PRODUCT OPERATIONS TESTS
# ============================================

class TestProductOperations:
    """Test suite for basic product operations"""
    
    def test_add_product(self, db, sample_product, cleanup_test_data):
        """
        Test adding a new product to inventory.
        
        Expected: Product should be created successfully
        """
        result = db.add_product(**sample_product)
        
        assert result["success"] == True, "Product creation should succeed"
        assert result["product"]["product_id"] == sample_product["product_id"]
        assert result["product"]["name"] == sample_product["name"]
        assert result["product"]["price"] == sample_product["price"]
        print("✅ Test passed: Add product")
    
    def test_get_product(self, db, sample_product, cleanup_test_data):
        """
        Test retrieving product information.
        
        Expected: Should return correct product details
        """
        # First add the product
        db.add_product(**sample_product)
        
        # Then retrieve it
        result = db.get_product(sample_product["product_id"])
        
        assert result["success"] == True, "Product retrieval should succeed"
        assert result["product_id"] == sample_product["product_id"]
        assert result["name"] == sample_product["name"]
        assert result["price"] == sample_product["price"]
        assert result["stock_quantity"] == sample_product["stock_quantity"]
        assert result["available_quantity"] == sample_product["stock_quantity"]
        print("✅ Test passed: Get product")
    
    def test_get_nonexistent_product(self, db):
        """
        Test retrieving a product that doesn't exist.
        
        Expected: Should return error
        """
        result = db.get_product("NONEXISTENT_PRODUCT")
        
        assert result["success"] == False, "Should fail for nonexistent product"
        assert "not found" in result["error"].lower()
        print("✅ Test passed: Get nonexistent product")
    
    def test_add_duplicate_product(self, db, sample_product, cleanup_test_data):
        """
        Test adding a product with duplicate product_id.
        
        Expected: Should fail (product_id must be unique)
        """
        # Add product first time
        db.add_product(**sample_product)
        
        # Try to add same product again
        result = db.add_product(**sample_product)
        
        assert result["success"] == False, "Duplicate product_id should fail"
        print("✅ Test passed: Add duplicate product")


# ============================================
# PRODUCT SEARCH TESTS
# ============================================

class TestProductSearch:
    """Test suite for product search functionality"""
    
    def test_search_by_name(self, db, sample_product, cleanup_test_data):
        """
        Test searching products by name.
        
        Expected: Should find products matching search term
        """
        # Add test product
        db.add_product(**sample_product)
        
        # Search for it
        result = db.search_products(search_term="Test Laptop")
        
        assert result["success"] == True
        assert len(result["products"]) > 0
        assert any(p["product_id"] == sample_product["product_id"] for p in result["products"])
        print("✅ Test passed: Search by name")
    
    def test_search_by_partial_name(self, db, sample_product, cleanup_test_data):
        """
        Test searching with partial product name.
        
        Expected: Should find products with partial match
        """
        db.add_product(**sample_product)
        
        # Search with partial name
        result = db.search_products(search_term="Laptop")
        
        assert result["success"] == True
        assert len(result["products"]) > 0
        print("✅ Test passed: Search by partial name")
    
    def test_search_by_category(self, db, sample_product, cleanup_test_data):
        """
        Test searching products by category.
        
        Expected: Should return products in specified category
        """
        db.add_product(**sample_product)
        
        result = db.search_products(category="Electronics")
        
        assert result["success"] == True
        assert len(result["products"]) > 0
        # Check all returned products are in Electronics category
        for product in result["products"]:
            assert product["category"] == "Electronics"
        print("✅ Test passed: Search by category")
    
    def test_search_in_stock_only(self, db, cleanup_test_data):
        """
        Test filtering for in-stock products only.
        
        Expected: Should only return products with stock > 0
        """
        # Add in-stock product
        db.add_product(
            product_id="TEST_PROD_IN_STOCK",
            name="In Stock Product",
            description="Test",
            price=99.99,
            category="Test",
            stock_quantity=10
        )
        
        # Add out-of-stock product
        db.add_product(
            product_id="TEST_PROD_OUT_STOCK",
            name="Out of Stock Product",
            description="Test",
            price=99.99,
            category="Test",
            stock_quantity=0
        )
        
        result = db.search_products(category="Test", in_stock_only=True)
        
        assert result["success"] == True
        # Should only find the in-stock product
        for product in result["products"]:
            assert product["is_in_stock"] == True
        print("✅ Test passed: Search in-stock only")


# ============================================
# STOCK MANAGEMENT TESTS
# ============================================

class TestStockManagement:
    """Test suite for stock management operations"""
    
    def test_update_stock_increase(self, db, sample_product, cleanup_test_data):
        """
        Test increasing stock quantity.
        
        Expected: Stock should increase by specified amount
        """
        db.add_product(**sample_product)
        
        # Increase stock by 20 units
        result = db.update_stock(sample_product["product_id"], 20, "restock")
        
        assert result["success"] == True
        assert result["previous_stock"] == sample_product["stock_quantity"]
        assert result["new_stock"] == sample_product["stock_quantity"] + 20
        assert result["change"] == 20
        print("✅ Test passed: Update stock (increase)")
    
    def test_update_stock_decrease(self, db, sample_product, cleanup_test_data):
        """
        Test decreasing stock quantity.
        
        Expected: Stock should decrease by specified amount
        """
        db.add_product(**sample_product)
        
        # Decrease stock by 10 units
        result = db.update_stock(sample_product["product_id"], -10, "sale")
        
        assert result["success"] == True
        assert result["previous_stock"] == sample_product["stock_quantity"]
        assert result["new_stock"] == sample_product["stock_quantity"] - 10
        assert result["change"] == -10
        print("✅ Test passed: Update stock (decrease)")
    
    def test_update_stock_insufficient(self, db, sample_product, cleanup_test_data):
        """
        Test decreasing stock below zero.
        
        Expected: Should fail (stock cannot be negative)
        """
        db.add_product(**sample_product)
        
        # Try to decrease stock by more than available
        result = db.update_stock(
            sample_product["product_id"], 
            -(sample_product["stock_quantity"] + 10), 
            "sale"
        )
        
        assert result["success"] == False
        assert "insufficient" in result["error"].lower()
        print("✅ Test passed: Update stock (insufficient)")
    
    def test_get_low_stock_products(self, db, cleanup_test_data):
        """
        Test getting products below low stock threshold.
        
        Expected: Should return products with low stock
        """
        # Add product with low stock
        db.add_product(
            product_id="TEST_LOW_STOCK",
            name="Low Stock Product",
            description="Test",
            price=99.99,
            category="Test",
            stock_quantity=5,
            low_stock_threshold=10
        )
        
        # Add product with adequate stock
        db.add_product(
            product_id="TEST_GOOD_STOCK",
            name="Good Stock Product",
            description="Test",
            price=99.99,
            category="Test",
            stock_quantity=50,
            low_stock_threshold=10
        )
        
        result = db.get_low_stock_products()
        
        assert result["success"] == True
        # Should include the low stock product
        low_stock_ids = [p["product_id"] for p in result["products"]]
        assert "TEST_LOW_STOCK" in low_stock_ids
        print("✅ Test passed: Get low stock products")


# ============================================
# RESERVATION TESTS
# ============================================

class TestReservations:
    """Test suite for stock reservation functionality"""
    
    def test_reserve_stock(self, db, sample_product, sample_customer, cleanup_test_data):
        """
        Test reserving stock for a customer.
        
        Expected: Stock should be reserved successfully
        """
        # Add product and customer
        db.add_product(**sample_product)
        db.create_customer(**sample_customer)
        
        # Reserve 5 units
        result = db.reserve_stock(
            sample_product["product_id"], 
            5, 
            sample_customer["customer_id"]
        )
        
        assert result["success"] == True
        assert result["product_id"] == sample_product["product_id"]
        assert result["quantity"] == 5
        assert "reservation_id" in result
        assert "expires_at" in result
        print("✅ Test passed: Reserve stock")
    
    def test_reserve_insufficient_stock(self, db, sample_product, sample_customer, cleanup_test_data):
        """
        Test reserving more stock than available.
        
        Expected: Should fail with insufficient stock error
        """
        db.add_product(**sample_product)
        db.create_customer(**sample_customer)
        
        # Try to reserve more than available
        result = db.reserve_stock(
            sample_product["product_id"], 
            sample_product["stock_quantity"] + 10,
            sample_customer["customer_id"]
        )
        
        assert result["success"] == False
        assert "insufficient" in result["error"].lower()
        print("✅ Test passed: Reserve insufficient stock")
    
    def test_release_reservation(self, db, sample_product, sample_customer, cleanup_test_data):
        """
        Test releasing a stock reservation.
        
        Expected: Reserved stock should be returned to available
        """
        # Setup: Add product, customer, and create reservation
        db.add_product(**sample_product)
        db.create_customer(**sample_customer)
        
        reserve_result = db.reserve_stock(
            sample_product["product_id"], 
            5, 
            sample_customer["customer_id"]
        )
        
        reservation_id = reserve_result["reservation_id"]
        
        # Release the reservation
        result = db.release_reservation(reservation_id)
        
        assert result["success"] == True
        
        # Check that stock is back to original
        product = db.get_product(sample_product["product_id"])
        assert product["reserved_quantity"] == 0
        assert product["available_quantity"] == sample_product["stock_quantity"]
        print("✅ Test passed: Release reservation")
    
    def test_multiple_reservations(self, db, sample_product, cleanup_test_data):
        """
        Test multiple reservations on same product.
        
        Expected: Reserved quantity should accumulate correctly
        """
        db.add_product(**sample_product)
        
        # Create first customer and reservation
        db.create_customer("TEST_CUST_001", "cust1@test.com", "Customer 1")
        db.reserve_stock(sample_product["product_id"], 5, "TEST_CUST_001")
        
        # Create second customer and reservation
        db.create_customer("TEST_CUST_002", "cust2@test.com", "Customer 2")
        db.reserve_stock(sample_product["product_id"], 10, "TEST_CUST_002")
        
        # Check product state
        product = db.get_product(sample_product["product_id"])
        
        assert product["reserved_quantity"] == 15  # 5 + 10
        assert product["available_quantity"] == sample_product["stock_quantity"] - 15
        print("✅ Test passed: Multiple reservations")


# ============================================
# AVAILABILITY TESTS
# ============================================

class TestProductAvailability:
    """Test suite for product availability calculations"""
    
    def test_available_quantity_calculation(self, db, sample_product, cleanup_test_data):
        """
        Test that available quantity is calculated correctly.
        
        Expected: available = stock - reserved
        """
        db.add_product(**sample_product)
        
        # Reserve some stock
        db.create_customer("TEST_CUST_001", "test@test.com", "Test")
        db.reserve_stock(sample_product["product_id"], 10, "TEST_CUST_001")
        
        # Get product
        product = db.get_product(sample_product["product_id"])
        
        expected_available = sample_product["stock_quantity"] - 10
        assert product["available_quantity"] == expected_available
        print("✅ Test passed: Available quantity calculation")
    
    def test_is_in_stock_true(self, db, sample_product, cleanup_test_data):
        """
        Test is_in_stock flag when product has stock.
        
        Expected: is_in_stock should be True
        """
        db.add_product(**sample_product)
        
        product = db.get_product(sample_product["product_id"])
        
        assert product["is_in_stock"] == True
        print("✅ Test passed: Is in stock (True)")
    
    def test_is_in_stock_false(self, db, cleanup_test_data):
        """
        Test is_in_stock flag when product has no stock.
        
        Expected: is_in_stock should be False
        """
        # Add product with 0 stock
        db.add_product(
            product_id="TEST_OUT_OF_STOCK",
            name="Out of Stock Product",
            description="Test",
            price=99.99,
            category="Test",
            stock_quantity=0
        )
        
        product = db.get_product("TEST_OUT_OF_STOCK")
        
        assert product["is_in_stock"] == False
        print("✅ Test passed: Is in stock (False)")
    
    def test_low_stock_detection(self, db, cleanup_test_data):
        """
        Test low stock flag detection.
        
        Expected: is_low_stock should be True when below threshold
        """
        # Add product with stock below threshold
        db.add_product(
            product_id="TEST_LOW_STOCK",
            name="Low Stock Product",
            description="Test",
            price=99.99,
            category="Test",
            stock_quantity=5,
            low_stock_threshold=10
        )
        
        product = db.get_product("TEST_LOW_STOCK")
        
        assert product["is_low_stock"] == True
        print("✅ Test passed: Low stock detection")


# ============================================
# EDGE CASES AND ERROR HANDLING
# ============================================

class TestEdgeCases:
    """Test suite for edge cases and error handling"""
    
    def test_zero_price_product(self, db, cleanup_test_data):
        """
        Test adding product with price = 0.
        
        Expected: Should succeed (free products allowed)
        """
        result = db.add_product(
            product_id="TEST_FREE_PRODUCT",
            name="Free Product",
            description="Test",
            price=0.0,
            category="Test",
            stock_quantity=10
        )
        
        assert result["success"] == True
        print("✅ Test passed: Zero price product")
    
    def test_negative_price_product(self, db, cleanup_test_data):
        """
        Test adding product with negative price.
        
        Expected: Should fail (negative prices not allowed)
        """
        result = db.add_product(
            product_id="TEST_NEGATIVE_PRICE",
            name="Negative Price Product",
            description="Test",
            price=-10.0,
            category="Test",
            stock_quantity=10
        )
        
        # Database constraint should prevent this
        assert result["success"] == False
        print("✅ Test passed: Negative price product")
    
    def test_reserve_zero_quantity(self, db, sample_product, sample_customer, cleanup_test_data):
        """
        Test reserving 0 quantity.
        
        Expected: Should fail (must reserve at least 1 unit)
        """
        db.add_product(**sample_product)
        db.create_customer(**sample_customer)
        
        result = db.reserve_stock(
            sample_product["product_id"], 
            0, 
            sample_customer["customer_id"]
        )
        
        assert result["success"] == False
        print("✅ Test passed: Reserve zero quantity")
    
    def test_long_product_name(self, db, cleanup_test_data):
        """
        Test product with very long name.
        
        Expected: Should handle long names (up to 255 chars)
        """
        long_name = "A" * 255
        
        result = db.add_product(
            product_id="TEST_LONG_NAME",
            name=long_name,
            description="Test",
            price=99.99,
            category="Test",
            stock_quantity=10
        )
        
        assert result["success"] == True
        product = db.get_product("TEST_LONG_NAME")
        assert len(product["name"]) == 255
        print("✅ Test passed: Long product name")


# ============================================
# INTEGRATION TESTS
# ============================================

class TestIntegration:
    """Integration tests for complete workflows"""
    
    def test_complete_purchase_flow(self, db, sample_product, sample_customer, cleanup_test_data):
        """
        Test complete purchase workflow:
        1. Add product
        2. Customer reserves product
        3. Complete order (deduct stock)
        4. Verify final state
        
        Expected: All steps should succeed
        """
        # Step 1: Add product
        db.add_product(**sample_product)
        initial_stock = sample_product["stock_quantity"]
        
        # Step 2: Create customer
        db.create_customer(**sample_customer)
        
        # Step 3: Reserve stock
        reserve_result = db.reserve_stock(
            sample_product["product_id"], 
            2, 
            sample_customer["customer_id"]
        )
        assert reserve_result["success"] == True
        
        # Step 4: Complete order (reduce actual stock)
        update_result = db.update_stock(
            sample_product["product_id"], 
            -2, 
            "sale"
        )
        assert update_result["success"] == True
        
        # Step 5: Release reservation (order completed)
        release_result = db.release_reservation(reserve_result["reservation_id"])
        assert release_result["success"] == True
        
        # Step 6: Verify final state
        final_product = db.get_product(sample_product["product_id"])
        assert final_product["stock_quantity"] == initial_stock - 2
        assert final_product["reserved_quantity"] == 0
        assert final_product["available_quantity"] == initial_stock - 2
        
        print("✅ Test passed: Complete purchase flow")


# ============================================
# TEST RUNNER
# ============================================

if __name__ == "__main__":
    """
    Run tests manually without pytest.
    
    Usage:
        python tests/test_inventory.py
    """
    print("🧪 Running Inventory Management Tests")
    print("=" * 60)
    
    # Simple test runner
    db = OrderDatabase()
    
    print("\n📦 Testing Product Operations...")
    test_ops = TestProductOperations()
    
    try:
        sample_prod = {
            "product_id": "TEST_MANUAL_001",
            "name": "Manual Test Product",
            "description": "Test",
            "price": 99.99,
            "category": "Test",
            "stock_quantity": 50,
            "low_stock_threshold": 10
        }
        
        test_ops.test_add_product(db, sample_prod, None)
        test_ops.test_get_product(db, sample_prod, None)
        test_ops.test_get_nonexistent_product(db)
        
        print("\n✅ All manual tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
    
    finally:
        # Cleanup
        try:
            db.supabase.table("inventory").delete().ilike("product_id", "TEST_%").execute()
        except:
            pass
    
    print("\n" + "=" * 60)
    print("For comprehensive testing, run: pytest tests/test_inventory.py -v")