import streamlit as st
import Sheets
import pandas as pd

# Load all sheets data at the start
if 'sheets_data' not in st.session_state:
    st.session_state.sheets_data = Sheets.load_all_sheets()  # Load all sheet data into session state

# Initialize session state for orders and order items
if "order_items" not in st.session_state:
    st.session_state.order_items = []  # Current items in the order
if "orders" not in st.session_state:
    st.session_state.orders = []  # List of all orders

# Function to display the current order details in a table
def show_order_details():
    if len(st.session_state.order_items) > 0:
        st.write("Products in the order:")
        order_df = pd.DataFrame(st.session_state.order_items)
        st.table(order_df)  # Display order items as a table

# Function to check inventory and update DB if necessary
def check_inventory_and_update_order(order_details):
    """
    Verifies if there's enough inventory for the ingredients in the order,
    and returns a list of missing ingredients if some are insufficient.
    The inventory in the DB will NOT be modified.
    """
    spreadsheet = Sheets.get_table()  # Get the spreadsheet
    db_df = Sheets.get_worksheet(spreadsheet, 'DB')  # Get the DB worksheet

    # Create a dictionary of the ingredients and their quantities from the DB
    db_inventory = dict(zip(db_df['Item'], db_df['Qty']))

    missing_ingredients = []  # List to accumulate missing ingredients

    # Iterate through each item in the order to check if inventory is sufficient
    for item in order_details:
        product_name = item['Producto']
        size = item['Tamaño']
        quantity = item['Cantidad']

        # Load the product's specific worksheet (e.g., 'Nodol')
        product_df = Sheets.get_worksheet(spreadsheet, product_name)

        # Check ingredients for the specific product
        for index, row in product_df.iterrows():
            ingredient = row['Item']  # Ingredient name
            required_qty = row['Qty'] * quantity  # Total required quantity for this ingredient

            # Check if we have enough stock in the DB
            if ingredient in db_inventory:
                db_qty = db_inventory[ingredient]  # Quantity in inventory

                # Ensure db_qty is a valid number, handle if it's not a number
                try:
                    db_qty = float(db_qty)
                except (ValueError, TypeError):
                    # If there's an issue converting to float, return an error for that ingredient
                    missing_ingredients.append({
                        'Item': ingredient,
                        'Required': required_qty,
                        'Available': "Invalid quantity in DB"
                    })
                    continue  # Skip to the next ingredient

                # Compare the quantities
                if db_qty < required_qty:
                    # If not enough stock, add to the missing ingredients list
                    missing_ingredients.append({
                        'Item': ingredient,
                        'Required': required_qty,
                        'Available': db_qty,
                        'Requerido': required_qty - db_qty
                    })

    # If there are missing ingredients, return the list of what's missing
    if missing_ingredients:
        return missing_ingredients

    # If everything is fine, return a success message without modifying the DB
    return None

# Function to finalize the order
def finalize_order():
    st.title("📦 Finalize Order")

    # Inicializar 'order_name' si no está en session_state
    if "order_name" not in st.session_state:
        # Usa un key único basado en algún valor que sea específico
        st.session_state.order_name = st.text_input("Order Name", key=f"order_name_input_{len(st.session_state.orders)}")

    if len(st.session_state.order_items) > 0:
        # Check inventory and update the DB
        result = check_inventory_and_update_order(st.session_state.order_items)

        # Display the result
        if result is not None:
            st.write(pd.DataFrame(result))
        else:
            st.success('Order can be completed')
            

        # If everything is fine, save the order to session state
        st.session_state.orders.append({
            "Order Name": st.session_state.order_name,
            "Details": st.session_state.order_items
        })
        st.session_state.order_items.clear()  # Clear items after finalizing the order
    else:
        st.warning("No products in the order.")

# Function to create a new order
def create_order():
    st.title("📝 Create New Order")

    # Input for the order name
    order_name = st.text_input("Order Name", key="order_name_input")

    # Display available products
    selected_sheet_name = st.selectbox("Select a product", Sheets.get_titles(Sheets.get_table()), key="select_sheet")
    selected_sheet_content = st.session_state.sheets_data[selected_sheet_name]  # Get the sheet content from session state

    # Select size and quantity
    selected_size = st.selectbox('Select Size', options={'Full', 'Medium', 'Individual'}, key="select_size")
    quantity = st.number_input('Quantity', min_value=1, step=1, format="%d", key="quantity_input")

    # Add product button
    if st.button("Add Product"):
        item = {
            "Producto": selected_sheet_name,
            "Tamaño": selected_size,
            "Cantidad": quantity
        }
        st.session_state.order_items.append(item)  # Add the product to the current order

    # Show the current order details
    show_order_details()

    # Finalize the order button
    if st.button("Finalize Order"):
        finalize_order()

# Function to view existing orders
def view_orders():
    st.title("📋 Existing Orders")
    if len(st.session_state.orders) > 0:
        for order in st.session_state.orders:
            st.markdown(f"**Order**: {order['Order Name']}")
            st.markdown("**Details:**")
            
            # Display the order details as a table
            order_df = pd.DataFrame(order['Details'])
            st.table(order_df)  # Display the order details table

            st.write("---")  # Line separator
    else:
        st.write("No orders registered.")

# Main function to manage navigation
def main():
    st.title("📦 Order Management System")
    create_order()  # Create order section
    view_orders()  # View existing orders section

if __name__ == "__main__":
    main()