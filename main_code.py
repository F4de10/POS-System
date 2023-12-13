"""
Exercise: lab 5 / cash_register version 3 (DD1321)
Usage: main program, use cash_register_interface_v2.py for GUI
Author: Nils Olivier
Date: 12-12-2023
"""

# Imports
import os
from datetime import datetime

import customtkinter as ctk

# Constants:
INVENTORY_FILE = "inventory.txt"
MEMBERS_FILE = "members.txt"


class Product:
    """
    A class representing a product with basic information.

    Attributes:
     - name (str): The name of the product.
     - product_id (int): The unique identifier for the product.
     - price (float): The price of the product.
     - quantity (int): The quantity of the product available.

    Methods:
        __init__(self, name, product_id, price, quantity):
            Initializes a new Product instance.

        __repr__(self):
            Returns a string representation of the product.

        add_quantity(self, quantity):
            Adds the specified quantity to the product's existing quantity.

        remove_quantity(self, quantity):
            Removes the specified quantity from the product's existing quantity.
    """

    def __init__(self, name, product_id, price, quantity):
        self.name = name
        self.product_id = product_id
        self.price = float(price)
        self.quantity = int(quantity)

    def __repr__(self):
        return f"{self.name} ({self.product_id}): {self.price} kr, {self.quantity} st"

    def add_quantity(self, quantity):
        """
        Adds the specified quantity to the product's existing quantity.

        Args:
         - quantity (int): The quantity to be added.
        """
        self.quantity += quantity

    def remove_quantity(self, quantity):
        """
        Removes the specified quantity from the product's existing quantity.

        Args:
         - quantity (int): The quantity to be removed.
        """
        self.quantity -= quantity


class Menu(ctk.CTkFrame):
    """
    A class representing the menu frame of the Cash Register application.

    Methods:
        __init__(self, master, **kwargs):
            Initializes a new Menu instance.

        create_widgets(self):
            Creates the widgets for the menu frame.

        create_layout(self):
            Sets up the layout for the menu frame.

        end_program(self):
            Destroys the main application window, ending the program.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.place(x=0, y=0, relwidth=0.3, relheight=1)

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        """
        Creates and configures the widgets for the menu frame.
        """

        # Add buttons
        self.new_customer_button = ctk.CTkButton(
            master=self,
            text="New customer",
            font=("Inter", 12),
            width=200,
            height=50,
            border_width=2,
            border_color="#2D313C",
            fg_color="transparent",
            hover_color="#5889F0",
            command=lambda: self.master.switch_frame("New Customer"),
        )
        self.return_item_button = ctk.CTkButton(
            master=self,
            text="Return item",
            font=("Inter", 12),
            width=200,
            height=50,
            border_width=2,
            border_color="#2D313C",
            fg_color="transparent",
            hover_color="#5889F0",
            command=lambda: self.master.switch_frame("Return Item"),
        )
        self.update_inventory_button = ctk.CTkButton(
            master=self,
            text="Update inventory",
            font=("Inter", 12),
            width=200,
            height=50,
            border_width=2,
            border_color="#2D313C",
            fg_color="transparent",
            hover_color="#5889F0",
            command=lambda: self.master.switch_frame("Update Inventory"),
        )
        self.end_program_button = ctk.CTkButton(
            master=self,
            text="End Program",
            font=("Inter", 12),
            width=150,
            height=40,
            border_width=2,
            border_color="#F80077",
            fg_color="transparent",
            hover_color="#F80077",
            command=lambda: self.end_program(),
        )

    def create_layout(self):
        """
        Configures the layout and places the widgets in the appropriate positions.
        """

        # Place widgets
        self.new_customer_button.pack(
            pady=20,
        )
        self.return_item_button.pack(
            pady=20,
        )
        self.update_inventory_button.pack(
            pady=20,
        )
        self.end_program_button.pack(pady=20, side="bottom")

    def end_program(self):
        """
        Destroys the main application window, ending the program.
        """
        self.master.destroy()


class Main(ctk.CTkFrame):
    """
    A class representing the main frame of the Cash Register application.

    Methods:
        __init__(self, master, **kwargs):
            Initializes a new Main instance.

        switch_frame(self, frame_name):
            Switches the current frame in the application to the specified frame.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.place(relx=0.3, y=0, relwidth=0.7, relheight=1)

        self.frames = {}
        self.current_frame = None

        # Create frames
        for frame_class in [
            New_customer_frame,
            Return_item_frame,
            Update_inventory_frame,
        ]:
            frame_instance = frame_class(self, fg_color="#2D313C", bg_color="#2D313C")
            self.frames[frame_instance.frame_name] = frame_instance

        # Show the initial frame
        self.switch_frame("New Customer")

    def switch_frame(self, frame_name):
        """
        Switches the current frame to the specified frame.

        Args:
        - frame_name (str): The name of the frame to switch to.
        """
        # Hide the current frame
        if self.current_frame:
            self.current_frame.place_forget()

        # Show the new frame
        self.frames[frame_name].place(relwidth=1, relheight=1)
        self.current_frame = self.frames[frame_name]


class New_customer_frame(ctk.CTkFrame):
    """
    A class representing the frame for a new customer.

    Attributes:
    - frame_name (str): The name of the frame.
    - shopping_cart (dict): A dictionary representing the shopping cart.

    Methods:
    - create_widgets(): Creates the widgets for the frame.
    - create_layout(): Creates the layout for the frame.
    - add_item(product_id, quantity): Adds an item to the shopping cart.
    - remove_item(product_id, quantity): Removes an item from the shopping cart.
    - checkout(): Performs the checkout process.
    - update_text_box(text): Updates the text box with the given text.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.frame_name = "New Customer"
        self.create_widgets()
        self.create_layout()
        self.shopping_cart = {}

    def create_widgets(self):
        """
        Creates and initializes the widgets for the New Customer interface.
        """
        self.title_label = ctk.CTkLabel(
            self,
            text="New Customer",
            font=("Inter", 24, "bold"),
            width=200,
            height=50,
        )

        # Product ID
        self.product_id_entry = ctk.CTkEntry(
            master=self, placeholder_text="Enter Product ID"
        )

        # Quantity combo box
        self.quantity_combo_box = ctk.CTkComboBox(
            master=self,
            values=[str(i) for i in range(1, 101)],
        )

        # Add button
        self.add_button = ctk.CTkButton(
            master=self,
            text="Add",
            font=("Inter", 14),
            width=120,
            height=40,
            fg_color="#5988F4",
            command=lambda: self.add_item(
                self.product_id_entry.get(), self.quantity_combo_box.get()
            ),
        )

        # Remove button
        self.remove_button = ctk.CTkButton(
            master=self,
            text="Remove",
            font=("Inter", 11),
            border_width=1,
            border_color="#FC0079",
            hover_color="#FC0079",
            width=100,
            height=30,
            fg_color="transparent",
            command=lambda: self.remove_item(
                self.product_id_entry.get(), self.quantity_combo_box.get()
            ),
        )

        self.text_box = ctk.CTkTextbox(
            self,
            corner_radius=10,
            width=400,
            height=150,
        )

        # Checkout button
        self.checkout_button = ctk.CTkButton(
            master=self,
            text="Checkout",
            font=("Inter", 14),
            width=300,
            height=50,
            fg_color="#5988F4",
            command=lambda: self.checkout(),
        )
        self.clear_shopping_cart_button = ctk.CTkButton(
            master=self,
            text="Clear shopping cart",
            font=("Inter", 11),
            border_width=1,
            border_color="#FC0079",
            hover_color="#FC0079",
            width=150,
            height=30,
            fg_color="transparent",
            command=lambda: self.clear_shopping_cart(),
        )

    def create_layout(self):
        """
        Creates the layout for the New Customer interface.

        """
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(6, weight=1)

        self.title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")
        self.product_id_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ne")
        self.quantity_combo_box.grid(row=1, column=1, padx=10, pady=10, sticky="nw")
        self.add_button.grid(
            row=2, column=0, columnspan=2, padx=10, pady=10, sticky="n"
        )
        self.remove_button.grid(
            row=3, column=0, columnspan=2, padx=10, pady=10, sticky="n"
        )
        self.checkout_button.grid(
            row=4, column=0, columnspan=2, padx=20, pady=20, sticky="s"
        )
        self.clear_shopping_cart_button.grid(
            row=5, column=0, columnspan=2, padx=10, pady=10, sticky="n"
        )
        self.text_box.grid(row=6, columnspan=2, padx=10, pady=10, sticky="nsew")

    def add_item(self, product_id, quantity):
        """
        Adds an item to the shopping cart based on the given product ID and quantity.

        Args:
            product_id (str): The ID of the product to be added.
            quantity (int): The quantity of the product to be added.
        """
        try:
            quantity = abs(int(quantity))
        except ValueError:
            self.update_text_box(f"\nInvalid quantity")
            return
        inventory = read_file(INVENTORY_FILE)
        if product_id in inventory:
            available_quantity = int(inventory[product_id].quantity)
            if available_quantity < int(quantity):
                self.update_text_box(
                    f"\nNot enough quantity, only {available_quantity} left\n"
                )
            elif product_id in self.shopping_cart:
                self.shopping_cart[product_id].add_quantity(quantity)
                self.update_text_box(
                    f"\n{quantity}st {self.shopping_cart[product_id].name} added to shopping cart"
                )
            else:
                self.shopping_cart[product_id] = Product(
                    inventory[product_id].name,
                    inventory[product_id].product_id,
                    inventory[product_id].price,
                    quantity,
                )
                self.update_text_box(
                    f"\n{self.shopping_cart[product_id]} added to shopping cart"
                )
        else:
            self.update_text_box(f"\nProduct not found\n")

    def remove_item(self, product_id, quantity):
        """
        Removes a specified quantity of a product from the shopping cart.

        Args:
            product_id (int): The ID of the product to be removed.
            quantity (int): The quantity of the product to be removed.
        """
        try:
            quantity = abs(int(quantity))
        except ValueError:
            self.update_text_box(f"\nInvalid quantity\n")
            return
        if (
            product_id in self.shopping_cart
            and quantity <= self.shopping_cart[product_id].quantity
        ):
            if quantity == self.shopping_cart[product_id].quantity:
                self.update_text_box(
                    f"\nRemoved {self.shopping_cart[product_id]} from shopping cart"
                )
                del self.shopping_cart[product_id]
            else:
                self.shopping_cart[product_id].remove_quantity(quantity)
                self.update_text_box(
                    f"\nRemoved {quantity} {self.shopping_cart[product_id].name} from shopping cart, {self.shopping_cart[product_id].quantity} remains"
                )
        else:
            self.update_text_box(
                f"\nProduct not in shopping cart or not enough quantity"
            )

    def checkout(self):
        """
        Performs the checkout process for the shopping cart.

        Reads the inventory file, creates a receipt, saves the receipt, updates the text box,
        removes the purchased products from the inventory, and saves the updated inventory file.

        If the shopping cart is empty, it updates the text box with a message indicating that
        the shopping cart is empty.
        """
        inventory = read_file(INVENTORY_FILE)
        if len(self.shopping_cart) > 0:
            checkout_receipt = create_receipt(self.shopping_cart)
            try:
                save_receipt("purchase", checkout_receipt)
                self.update_text_box(f"{checkout_receipt} \n\nReceipt saved!\n\n")
            except FileNotFoundError:
                self.update_text_box(f"\n\nReceipt not saved\n\n")
            for product in self.shopping_cart.values():
                inventory[product.product_id].remove_quantity(product.quantity)
            save_file(INVENTORY_FILE, inventory)
        else:
            self.update_text_box(f"\n\nShopping cart is empty\n")

    def clear_shopping_cart(self):
        """
        Clears the shopping cart.
        """
        self.shopping_cart.clear()
        self.text_box.delete("1.0", "end")

    def update_text_box(self, text):
        """
        Updates the text box with the given text.

        Args:
        - text (str): The text to be inserted into the text box.
        """
        self.text_box.insert("end", text)


class Return_item_frame(ctk.CTkFrame):
    """
    A class representing the frame for returning an item.

    Attributes:
        frame_name (str): The name of the frame.

    Methods:
        __init__(self, master, **kwargs): Initializes the Return_item_frame.
        create_widgets(self): Creates the widgets for the frame.
        create_layout(self): Creates the layout for the frame.
        return_item(self, product_id, quantity, shopping_cart={}): Returns an item.
        update_text_box(self, text): Updates the text box with the given text.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.frame_name = "Return Item"
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        """
        Create and initialize the widgets for the Return Item interface.
        """
        self.title_label = ctk.CTkLabel(
            self, text="Return Item", font=("Inter", 24, "bold")
        )
        self.product_id_entry = ctk.CTkEntry(
            master=self, placeholder_text="Enter Product ID"
        )
        self.quantity_combo_box = ctk.CTkComboBox(
            master=self,
            values=[str(i) for i in range(1, 11)],
        )
        self.return_button = ctk.CTkButton(
            master=self,
            text="Return",
            font=("Inter", 12),
            fg_color="#5988F4",
            command=lambda: self.return_item(
                self.product_id_entry.get(), self.quantity_combo_box.get()
            ),
        )
        self.text_box = ctk.CTkTextbox(self)

    def create_layout(self):
        """
        Creates the layout for the Return Item interface.
        """
        self.title_label.pack(pady=20)
        self.product_id_entry.pack(pady=10)
        self.quantity_combo_box.pack(pady=10)
        self.return_button.pack(pady=10)
        self.text_box.pack(padx=10, pady=10, fill="both", expand=True)

    def return_item(self, product_id, quantity, shopping_cart={}):
        """
        Returns an item based on the given product ID and quantity.

        Args:
            product_id (str): The ID of the product to be returned.
            quantity (str): The quantity of the product to be returned.
            shopping_cart (dict): The shopping cart dictionary.
        """
        inventory = read_file(INVENTORY_FILE)
        if product_id in inventory:
            try:
                inventory[product_id].add_quantity(int(quantity))
                shopping_cart[product_id] = Product(
                    inventory[product_id].name,
                    inventory[product_id].product_id,
                    inventory[product_id].price,
                    quantity,
                )
                return_receipt = create_receipt(shopping_cart, return_receipt=True)
                save_receipt("return", return_receipt)
                save_file(INVENTORY_FILE, inventory)
                self.update_text_box(f"{return_receipt} \n\nReceipt saved!\n")
            except ValueError:
                self.update_text_box(f"\nInvalid quantity\n")
        else:
            self.update_text_box(f"\nProduct not found\n")
        return

    def update_text_box(self, text):
        """
        Updates the text box with the given text.

        Args:
            text (str): The text to be displayed in the text box.
        """
        self.text_box.insert("end", text)


class Update_inventory_frame(ctk.CTkFrame):
    """
    A class representing the frame for updating the inventory.

    Attributes:
    - frame_name: The name of the frame.

    Methods:
    - __init__(self, master, **kwargs): Initializes the Update_inventory_frame.
    - create_widgets(self): Creates the widgets for the frame.
    - create_layout(self): Creates the layout for the frame.
    - view_inventory(self): Displays the inventory in the text box.
    - add_product(self, name, product_id, price, quantity): Adds a product to the inventory.
    - update_product(self, product_id, price, quantity): Updates a product in the inventory.
    - delete_product(self, product_id): Deletes a product from the inventory.
    - update_text_box(self, text): Updates the text box with the given text.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.frame_name = "Update Inventory"
        self.create_widgets()
        self.create_layout()

    # Rest of the code...


class Update_inventory_frame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.frame_name = "Update Inventory"
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        """
        Create and configure the widgets for the Update Inventory interface.
        """
        self.title_label = ctk.CTkLabel(
            self, text="Update Inventory", font=("Inter", 24, "bold")
        )
        self.tab_view = ctk.CTkTabview(
            self,
            width=500,
            height=0,
            fg_color="#2D313C",
            segmented_button_selected_color="#5988F4",
        )
        # Add tabs
        self.tab_view.add("Add Product")
        self.tab_view.add("Update Product")
        self.tab_view.add("Delete Product")

        self.add_product_tab = self.tab_view.tab("Add Product")
        self.update_product_tab = self.tab_view.tab("Update Product")
        self.delete_product_tab = self.tab_view.tab("Delete Product")

        # Buttons in Add Product tab
        self.add_product_tab.name_entry = ctk.CTkEntry(
            master=self.add_product_tab,
            placeholder_text="Enter Product Name",
        )

        self.add_product_tab.product_id_entry = ctk.CTkEntry(
            master=self.add_product_tab,
            placeholder_text="Enter Product ID",
        )

        self.add_product_tab.price_entry = ctk.CTkEntry(
            master=self.add_product_tab,
            placeholder_text="Enter Product Price",
        )

        self.add_product_tab.quantity_combo_box = ctk.CTkEntry(
            master=self.add_product_tab,
            placeholder_text="Enter Product Quantity",
        )

        self.add_product_tab.confirm_button = ctk.CTkButton(
            master=self.add_product_tab,
            text="Confirm",
            font=("Inter", 12),
            fg_color="#5988F4",
            width=200,
            height=30,
            command=lambda: self.add_product(
                self.add_product_tab.name_entry.get(),
                self.add_product_tab.product_id_entry.get(),
                self.add_product_tab.price_entry.get(),
                self.add_product_tab.quantity_combo_box.get(),
            ),
        )

        # Buttons in Update Product tab
        self.update_product_tab.product_id_entry = ctk.CTkEntry(
            master=self.update_product_tab,
            placeholder_text="Enter Product ID",
        )
        self.update_product_tab.price_entry = ctk.CTkEntry(
            master=self.update_product_tab,
            placeholder_text="Enter Product Price",
        )
        self.update_product_tab.quantity_combo_box = ctk.CTkEntry(
            master=self.update_product_tab,
            placeholder_text="Enter Product Quantity",
        )
        self.update_product_tab.confirm_button = ctk.CTkButton(
            master=self.update_product_tab,
            text="Confirm",
            font=("Inter", 12),
            fg_color="#5988F4",
            width=200,
            height=30,
            command=lambda: self.update_product(
                self.update_product_tab.product_id_entry.get(),
                self.update_product_tab.price_entry.get(),
                self.update_product_tab.quantity_combo_box.get(),
            ),
        )

        # Buttons in Delete Product tab
        self.delete_product_tab.product_id_entry = ctk.CTkEntry(
            master=self.delete_product_tab,
            placeholder_text="Enter Product ID",
        )
        self.delete_product_tab.confirm_button = ctk.CTkButton(
            master=self.delete_product_tab,
            text="Confirm",
            font=("Inter", 12),
            fg_color="#5988F4",
            width=200,
            height=30,
            command=lambda: self.delete_product(
                self.delete_product_tab.product_id_entry.get(),
            ),
        )

        # Text box
        self.text_box = ctk.CTkTextbox(
            self,
            corner_radius=10,
            width=400,
            height=200,
        )
        self.view_inventory_button = ctk.CTkButton(
            master=self,
            text="View Inventory",
            font=("Inter", 10),
            width=150,
            height=30,
            border_width=2,
            border_color="#465372",
            hover_color="#465372",
            fg_color="transparent",
            command=lambda: self.view_inventory(),
        )

    def create_layout(self):
        """
        Creates the layout for the Update Inventory interface.
        """
        self.title_label.pack(pady=20)
        self.tab_view.pack(fill="both", expand=True)

        # Add product tab
        self.add_product_tab.name_entry.pack(padx=10, pady=10)
        self.add_product_tab.product_id_entry.pack(padx=10, pady=10)
        self.add_product_tab.price_entry.pack(padx=10, pady=10)
        self.add_product_tab.quantity_combo_box.pack(padx=10, pady=10)
        self.add_product_tab.confirm_button.pack(padx=10, pady=10)

        # Update product tab
        self.update_product_tab.product_id_entry.pack(padx=10, pady=10)
        self.update_product_tab.price_entry.pack(padx=10, pady=10)
        self.update_product_tab.quantity_combo_box.pack(padx=10, pady=10)
        self.update_product_tab.confirm_button.pack(padx=10, pady=10)

        # Delete product tab
        self.delete_product_tab.product_id_entry.pack(padx=10, pady=10)
        self.delete_product_tab.confirm_button.pack(padx=10, pady=10)

        # textbox and view inventory button
        self.view_inventory_button.pack(side="top", padx=10, pady=10)
        self.text_box.pack(side="top", pady=10, padx=10, fill="both", expand=True)

    def view_inventory(self):
        """
        Displays the inventory of the cash register.

        Reads the inventory from a file and displays it in the text box.
        """
        inventory = read_file(INVENTORY_FILE)
        self.update_text_box(f"\nInventory:\n")
        for product in inventory:
            self.update_text_box(f"{inventory[product]} \n\n")

    def add_product(self, name, product_id, price, quantity):
        """
        Adds a product to the inventory.

        Args:
         - name (str): The name of the product.
         - product_id (int): The ID of the product.
         - price (float): The price of the product.
         - quantity (int): The quantity of the product.
        """
        inventory = read_file(INVENTORY_FILE)
        try:
            price = abs(float(price))
            quantity = abs(int(quantity))
            inventory[product_id] = Product(name, product_id, price, quantity)
            self.update_text_box(f"\n{inventory[product_id]} \n\nInventory updated!")
            save_file(INVENTORY_FILE, inventory)
        except ValueError:
            self.update_text_box(f"\nInvalid value, please enter a number")
            pass

    def update_product(self, product_id, price, quantity):
        """
        Updates the information of a product in the inventory.

        Args:
         - product_id (str): The ID of the product.
         - price (float): The new price of the product.
         - quantity (int): The new quantity of the product.
        """
        inventory = read_file(INVENTORY_FILE)
        if product_id in inventory:
            try:
                name = inventory[product_id].name
                price = abs(float(price))
                quantity = abs(int(quantity))
                inventory[product_id] = Product(name, product_id, price, quantity)
                self.update_text_box(
                    f"\n{inventory[product_id]} \n\nInventory updated!"
                )
                save_file(INVENTORY_FILE, inventory)
            except ValueError:
                self.update_text_box(f"\nInvalid value, please enter a number")
        else:
            self.update_text_box(f"\nProduct not found")
            pass

    def delete_product(self, product_id):
        """
        Deletes a product from the inventory based on the given product ID.

        Args:
            product_id (int): The ID of the product to be deleted.
        """
        inventory = read_file(INVENTORY_FILE)
        if product_id in inventory:
            self.update_text_box(
                f"\n{inventory[product_id]} deleted! \n\nInventory updated!"
            )
            del inventory[product_id]
            save_file(INVENTORY_FILE, inventory)
        else:
            self.update_text_box(f"\nProduct not found")
        pass

    def update_text_box(self, text):
        """
        Updates the text box with the given text.

        Args:
         - text (str): The text to be inserted into the text box.
        """
        self.text_box.insert("end", text)


def read_file(filename):
    """
    Reads data from a file and returns a dictionary.

    Args:
     - filename (str): The name of the file to read.
     - entity_class (class): The class of the entity to create.

    Returns:
     - dict: A dictionary containing entity instances.
    """
    data = {}
    try:
        with open(filename, "r") as file:
            for line in file:
                attributes = line.strip().split(",")
                product_id = attributes[1]  # Assuming the ID is at index 1
                data[product_id] = Product(*attributes)
    except FileNotFoundError:
        print(f"\nFile {filename} not found\nProgram stopped!\n")
        exit()

    return data


def save_file(filename, dictionary):
    """
    Saves data to a file.

    Args:
     - filename (str): The name of the file to save.
     - dictionary (dict): A dictionary containing entity instances.
    """
    with open(filename, "w") as file:
        for item in dictionary.values():
            file.write(f"{item.name},{item.product_id},{item.price},{item.quantity}\n")


def create_receipt(shopping_cart, return_receipt=False):
    """
    Creates a receipt for the items in the shopping cart.

    Args:
     - shopping_cart (dict): A dictionary representing the shopping cart.
     - return_receipt (bool): If True, indicates a return receipt.

    Returns:
     - str: The receipt as a string.
    """
    total_price = 0
    receipt = "\n\nReceipt\n-------\nItems:\n"
    for item in shopping_cart.values():
        receipt += (
            f"{item.name} ({item.product_id}): {item.price} kr, {item.quantity} st\n"
        )
        total_price += round(item.price * item.quantity)
    if return_receipt:
        receipt += f"Money returned: {total_price} kr"
    else:
        receipt += f"Total price: {total_price} kr"
    return receipt


def save_receipt(filename, receipt):
    """
    Save the receipt to a file with the given filename.

    Args:
     - filename (str): The name of the file to save the receipt to.
     - receipt (str): The content of the receipt to be saved.
    """
    folder = "receipts"
    if not os.path.exists(folder):
        os.makedirs(folder)

    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename_with_datetime = f"{filename}_{current_datetime}.txt"
    try:
        with open(os.path.join(folder, filename_with_datetime), "w") as file:
            file.write(receipt)
    except Exception as e:
        print(f"\nError: {e}\nReceipt not saved\n")
        exit()
