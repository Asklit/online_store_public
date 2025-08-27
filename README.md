# Online Store

## Project Author: Alexander Khanzhin

## Project Description
  The project is a desktop application developed using the **PyQt5** library, implementing the functionality of an online store. Users can register, log in, search for products, add them to the cart, manage cart contents, and proceed to payment.

## Launch Instructions
  1. Install the **PyQt5** library:
     ```bash
     pip install pyqt5
     ```
  2. Run the entry.py file.

## Main Functionality

1. Authorization and Registration
    - Upon launching the application, a login/registration window (class Entry) is displayed.
    - Users can create a new account or log in to an existing one.
    - Data input is handled via QLineEdit, and actions are performed using QPushButton.
    - Data validation:
        - Phone number: format +7 *** *** ** ** or 8 *** *** ** **.
        - Password: maximum 20 characters.
    
    - Validation is implemented using try, except, raise constructs.
    - User data is stored in an SQL table during registration.
    - During login, the entered data is verified against the database.Login Window

2. Product Search and Addition

    - After successful login, the main window opens. 
    - Users can:
      - Search for products in the SQL table using QLineEdit.
      - View products in a QTableWidget.
      - Add products to the cart using QPushButton.
    - Adding to the cart triggers a dialog window for confirmation.
    - If no products are selected, an error message is displayed (try, except, raise).Product Window

3. Cart

     - In the cart window, users can:
       - Remove products.
       - Adjust product quantities.
       - Return to the product selection window if the cart is empty.
    - Product removal prompts a dialog window for confirmation.
    - If no products are selected for removal, an error message is shown (try, except, raise).
    - Products are displayed in a QTableWidget.Cart Window

4. Order Payment

    - If the cart contains products, users can proceed to payment.
    - Features:
      - Selection of payment method and delivery location via QTabWidget.
      - For online payment, users enter bank card details:
          - Card number: 16 digits (1–9).
          - Month: 01–12.
          - Year: 01–99.
          - CVC: 001–999.
    - Input validation is handled using setValidator.
    - After payment, users can save a receipt as a .txt file.
    - A button to return to the cart is available.Payment Window

## Databade
  
  The application uses a database with four tables:
  
  1. Users: stores phone number and password.
  2. Products: contains product name and price.
  3. Orders: stores order status and client ID.
  4. Order Items: links product ID, order ID, and product quantity.
  
  Tables 3 and 4 are interconnected for accurate order tracking.
  

