from database import init_db, add_product, get_products, update_product, delete_product, record_sale, get_sales_history

def test_db():
    print("Testing database...")
    init_db()
    
    # Add
    add_product("Test Protein", 50.0, 10, "Suplementos")
    products = get_products()
    print(f"Products after add: {len(products)}")
    assert len(products) > 0
    
    prod_id = products[0][0]
    
    # Update
    update_product(prod_id, "Updated Protein", 55.0, 8, "Suplementos")
    products = get_products()
    assert products[0][1] == "Updated Protein"
    print("Update successful")
    
    # Sale
    record_sale(prod_id, 2, 110.0)
    products = get_products()
    assert products[0][3] == 6 # 8 - 2
    print("Sale recorded correctly, stock updated")
    
    # History
    history = get_sales_history()
    assert len(history) > 0
    print("Sales history retrieved")
    
    # Delete
    delete_product(prod_id)
    products = get_products()
    print("Product deleted")
    
    print("All tests passed!")

if __name__ == "__main__":
    test_db()
