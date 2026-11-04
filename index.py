# Import the main Tkinter module for GUI elements
import tkinter as tk
# Import ttk for themed widgets and messagebox for pop-up alerts
from tkinter import ttk, messagebox
# Import json module to handle reading and writing application data
import json
# Import os module to check file system paths
import os

# Define the JSON file name used for saving transaction history
FILE_NAME = "budget.json"

# Define the main application class for the Modern Budget App
class ModernBudgetApp:
    # Constructor method that runs when the application starts
    def __init__(self, root):
        # Store reference to the main Tkinter root window
        self.root = root
        # Set the title bar text of the application window
        self.root.title("Budget Planner")
        # Set initial dimensions (width x height) of the application window
        self.root.geometry("1000x720")
        # Set the main window background color to light gray
        self.root.configure(bg="#f3f6f9")

        # Bring window to front
        # Raise the application window above other open windows
        self.root.lift()
        # Temporarily lock the window as top-most on screen
        self.root.attributes('-topmost', True)
        # Remove the top-most lock after the event loop becomes idle
        self.root.after_idle(self.root.attributes, '-topmost', False)

        # Load existing transaction data from the JSON storage file
        self.transactions = self.load_data()

        # Container Frame
        # Create a top-level outer frame with padding inside the root window
        main_container = tk.Frame(root, bg="#f3f6f9", padx=25, pady=20)
        # Expand and fill the container frame to occupy the entire root area
        main_container.pack(fill="both", expand=True)

        # ---------------- 1. TOP KPI CARDS ----------------
        # Create a container frame for top metric display cards
        kpi_frame = tk.Frame(main_container, bg="#f3f6f9")
        # Pack the KPI frame horizontally across the top with bottom padding
        kpi_frame.pack(fill="x", pady=(0, 20))
        # Configure grid columns to share equal width for uniform card sizes
        kpi_frame.columnconfigure((0, 1, 2), weight=1, uniform="kpi")

        # Total Balance Card
        # Create background card frame for Total Balance
        card1 = tk.Frame(kpi_frame, bg="#ffffff", bd=0, highlightthickness=0, padx=20, pady=18)
        # Position card in column 0 of the KPI grid
        card1.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        # Add cash emoji icon with light blue background
        lbl_b_icon = tk.Label(card1, text="💵", font=("Segoe UI Emoji", 22), bg="#f0f4ff", width=2, height=1)
        # Pack icon to the left side of the card
        lbl_b_icon.pack(side="left", padx=(0, 15))
        # Container frame for balance text labels
        f1_info = tk.Frame(card1, bg="#ffffff")
        # Pack info frame to the left of the icon
        f1_info.pack(side="left")
        # Title label for Total Balance card
        tk.Label(f1_info, text="Total Balance", font=("Segoe UI", 10, "bold"), fg="#5c677d", bg="#ffffff").pack(anchor="w")
        # Value label displaying dynamic Total Balance amount
        self.lbl_balance = tk.Label(f1_info, text="₱0.00", font=("Segoe UI", 16, "bold"), fg="#1e40af", bg="#ffffff")
        # Align dynamic balance label to the left
        self.lbl_balance.pack(anchor="w")

        # Total Income Card
        # Create background card frame for Total Income
        card2 = tk.Frame(kpi_frame, bg="#ffffff", bd=0, highlightthickness=0, padx=20, pady=18)
        # Position card in column 1 of the KPI grid
        card2.grid(row=0, column=1, padx=5, sticky="ew")
        # Add trending up emoji icon with light green background
        lbl_i_icon = tk.Label(card2, text="📈", font=("Segoe UI Emoji", 22), bg="#ebfaf0", width=2, height=1)
        # Pack icon to the left side of the card
        lbl_i_icon.pack(side="left", padx=(0, 15))
        # Container frame for income text labels
        f2_info = tk.Frame(card2, bg="#ffffff")
        # Pack info frame to the left of the icon
        f2_info.pack(side="left")
        # Title label for Total Income card
        tk.Label(f2_info, text="Total Income", font=("Segoe UI", 10, "bold"), fg="#5c677d", bg="#ffffff").pack(anchor="w")
        # Value label displaying dynamic Total Income amount
        self.lbl_income = tk.Label(f2_info, text="₱0.00", font=("Segoe UI", 16, "bold"), fg="#10b981", bg="#ffffff")
        # Align dynamic income label to the left
        self.lbl_income.pack(anchor="w")

        # Total Expenses Card
        # Create background card frame for Total Expenses
        card3 = tk.Frame(kpi_frame, bg="#ffffff", bd=0, highlightthickness=0, padx=20, pady=18)
        # Position card in column 2 of the KPI grid
        card3.grid(row=0, column=2, padx=(10, 0), sticky="ew")
        # Add trending down emoji icon with light red background
        lbl_e_icon = tk.Label(card3, text="📉", font=("Segoe UI Emoji", 22), bg="#fff1f2", width=2, height=1)
        # Pack icon to the left side of the card
        lbl_e_icon.pack(side="left", padx=(0, 15))
        # Container frame for expenses text labels
        f3_info = tk.Frame(card3, bg="#ffffff")
        # Pack info frame to the left of the icon
        f3_info.pack(side="left")
        # Title label for Total Expenses card
        tk.Label(f3_info, text="Total Expenses", font=("Segoe UI", 10, "bold"), fg="#5c677d", bg="#ffffff").pack(anchor="w")
        # Value label displaying dynamic Total Expenses amount
        self.lbl_expenses = tk.Label(f3_info, text="₱0.00", font=("Segoe UI", 16, "bold"), fg="#ef4444", bg="#ffffff")
        # Align dynamic expenses label to the left
        self.lbl_expenses.pack(anchor="w")

        # ---------------- 2. WORKSPACE GRID ----------------
        # Middle section container for input form and overview summary
        workspace = tk.Frame(main_container, bg="#f3f6f9")
        # Pack workspace frame horizontally with bottom spacing
        workspace.pack(fill="x", pady=(0, 20))
        # Set workspace grid columns to expand evenly
        workspace.columnconfigure((0, 1), weight=1, uniform="work")

        # Left Card: Add Transaction Form
        # White card container for input form elements
        form_card = tk.Frame(workspace, bg="#ffffff", padx=25, pady=22)
        # Place form card in column 0 filling available vertical/horizontal space
        form_card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")

        # Form header title label
        tk.Label(form_card, text="Add Transaction", font=("Segoe UI", 14, "bold"), fg="#111827", bg="#ffffff").pack(anchor="w", pady=(0, 15))

        # Description input label
        tk.Label(form_card, text="Description", font=("Segoe UI", 9, "bold"), fg="#1f2937", bg="#ffffff").pack(anchor="w", pady=(5, 2))
        # Entry box for user to type transaction description
        self.ent_desc = tk.Entry(form_card, font=("Segoe UI", 10), bd=1, relief="solid", bg="#ffffff")
        # Pack description entry box horizontally
        self.ent_desc.pack(fill="x", ipady=6, pady=(0, 10))

        # Amount input label
        tk.Label(form_card, text="Amount", font=("Segoe UI", 9, "bold"), fg="#1f2937", bg="#ffffff").pack(anchor="w", pady=(5, 2))
        # Entry box for user to enter numeric transaction amount
        self.ent_amount = tk.Entry(form_card, font=("Segoe UI", 10), bd=1, relief="solid", bg="#ffffff")
        # Pack amount entry box horizontally
        self.ent_amount.pack(fill="x", ipady=6, pady=(0, 10))

        # Transaction Type selection label
        tk.Label(form_card, text="Transaction Type", font=("Segoe UI", 9, "bold"), fg="#1f2937", bg="#ffffff").pack(anchor="w", pady=(5, 2))
        # Dropdown selection menu for picking income or expense
        self.combo_type = ttk.Combobox(form_card, values=["income", "expense"], state="readonly", font=("Segoe UI", 10))
        # Set default value of dropdown menu to "income"
        self.combo_type.set("income")
        # Pack dropdown menu horizontally
        self.combo_type.pack(fill="x", ipady=4, pady=(0, 15))

        # Action button to trigger transaction creation
        btn_add = tk.Button(form_card, text="+ Add Transaction", font=("Segoe UI", 10, "bold"), bg="#2563eb", fg="#ffffff", activebackground="#1d4ed8", activeforeground="#ffffff", bd=0, cursor="hand2", command=self.add_transaction)
        # Pack submit button horizontally across card width
        btn_add.pack(fill="x", ipady=8)

        # Right Card: Budget Overview
        # White card container for right side summary overview
        overview_card = tk.Frame(workspace, bg="#ffffff", padx=25, pady=22)
        # Place overview card in column 1 filling grid cell area
        overview_card.grid(row=0, column=1, padx=(10, 0), sticky="nsew")

        # Budget Overview section title label
        tk.Label(overview_card, text="Budget Overview", font=("Segoe UI", 14, "bold"), fg="#111827", bg="#ffffff").pack(anchor="w", pady=(0, 20))

        # Overview Item 1: Income
        # Row frame for income overview display
        f_inc = tk.Frame(overview_card, bg="#ffffff")
        # Pack income summary row horizontally
        f_inc.pack(fill="x", pady=8)
        # Static label naming income field
        tk.Label(f_inc, text="Income", font=("Segoe UI", 10), fg="#4b5563", bg="#ffffff").pack(side="left")
        # Dynamic label showing total overview income
        self.lbl_ov_income = tk.Label(f_inc, text="₱0.00", font=("Segoe UI", 10, "bold"), fg="#111827", bg="#ffffff")
        # Align income value to the right side
        self.lbl_ov_income.pack(side="right")

        # Overview Item 2: Expenses
        # Row frame for expense overview display
        f_exp = tk.Frame(overview_card, bg="#ffffff")
        # Pack expense summary row horizontally
        f_exp.pack(fill="x", pady=8)
        # Static label naming expenses field
        tk.Label(f_exp, text="Expenses", font=("Segoe UI", 10), fg="#4b5563", bg="#ffffff").pack(side="left")
        # Dynamic label showing total overview expenses
        self.lbl_ov_expenses = tk.Label(f_exp, text="₱0.00", font=("Segoe UI", 10, "bold"), fg="#111827", bg="#ffffff")
        # Align expense value to the right side
        self.lbl_ov_expenses.pack(side="right")

        # Overview Item 3: Remaining
        # Row frame for remaining balance overview display
        f_rem = tk.Frame(overview_card, bg="#ffffff")
        # Pack remaining balance summary row horizontally
        f_rem.pack(fill="x", pady=8)
        # Static label naming remaining field
        tk.Label(f_rem, text="Remaining", font=("Segoe UI", 10), fg="#4b5563", bg="#ffffff").pack(side="left")
        # Dynamic label showing overview remaining balance
        self.lbl_ov_remaining = tk.Label(f_rem, text="₱0.00", font=("Segoe UI", 10, "bold"), fg="#111827", bg="#ffffff")
        # Align remaining value to the right side
        self.lbl_ov_remaining.pack(side="right")

        # ---------------- 3. TRANSACTION HISTORY PANEL ----------------
        # White card container for transaction history list section
        history_card = tk.Frame(main_container, bg="#ffffff", padx=25, pady=20)
        # Pack history section to expand and fill lower area
        history_card.pack(fill="both", expand=True)

        # Header wrapper frame for history panel
        h_header = tk.Frame(history_card, bg="#ffffff")
        # Pack header frame horizontally with bottom space
        h_header.pack(fill="x", pady=(0, 12))

        # Container frame for history titles
        f_titles = tk.Frame(h_header, bg="#ffffff")
        # Pack title text container to left side of header
        f_titles.pack(side="left")
        # Main title label for transaction history section
        tk.Label(f_titles, text="Transaction History", font=("Segoe UI", 14, "bold"), fg="#111827", bg="#ffffff").pack(anchor="w")
        # Subtitle description label for history section
        tk.Label(f_titles, text="View and manage your transactions", font=("Segoe UI", 9), fg="#6b7280", bg="#ffffff").pack(anchor="w")

        # Button element to clear all stored history items
        btn_clear = tk.Button(h_header, text="Clear All", font=("Segoe UI", 9, "bold"), bg="#fee2e2", fg="#ef4444", activebackground="#fca5a5", bd=0, cursor="hand2", padx=12, pady=6, command=self.clear_all)
        # Position clear button to the far right side of header
        btn_clear.pack(side="right")

        # Listbox widget to render recorded transaction entries
        self.listbox = tk.Listbox(history_card, font=("Segoe UI", 10), bd=0, highlightthickness=0, bg="#ffffff", selectbackground="#e5e7eb", selectforeground="#111827")
        # Pack listbox to fill remaining history card space
        self.listbox.pack(fill="both", expand=True)

        # Refresh interface display with current data on launch
        self.update_ui()

    # Function to read transactions from JSON file
    def load_data(self):
        # Check if stored JSON data file does not exist
        if not os.path.exists(FILE_NAME):
            # Return empty list if no saved file found
            return []
        # Attempt to open and parse existing JSON file
        try:
            # Open file stream in read mode
            with open(FILE_NAME, "r") as file:
                # Load and return JSON structured array
                return json.load(file)
        # Handle potential file reading or format exceptions safely
        except Exception:
            # Return empty list if reading fails
            return []

    # Function to save current transactions array to JSON file
    def save_data(self):
        # Open destination JSON file in write mode
        with open(FILE_NAME, "w") as file:
            # Write transactions list to file formatted with 4 spaces indent
            json.dump(self.transactions, file, indent=4)

    # Function to recalculate totals and refresh UI view
    def update_ui(self):
        # Clear all elements currently rendered in listbox
        self.listbox.delete(0, tk.END)
        # Reset running total accumulator for income
        income = 0
        # Reset running total accumulator for expenses
        expenses = 0

        # Loop through every transaction entry dictionary
        for t in self.transactions:
            # Determine prefix indicator sign based on transaction category
            symbol = "+" if t["type"] == "income" else "-"
            # Format row text string showing sign, description, and currency value
            display_text = f"  {symbol} {t['description']}  -  ₱{t['amount']:,.2f}"
            # Append formatted entry string to the end of listbox
            self.listbox.insert(tk.END, display_text)

            # Sum transaction amount into income total if income category
            if t["type"] == "income":
                income += t["amount"]
            # Otherwise sum transaction amount into expenses total
            else:
                expenses += t["amount"]

        # Calculate remaining net balance total
        balance = income - expenses

        # Update Top KPI Cards
        # Refresh top total balance card label text
        self.lbl_balance.config(text=f"₱{balance:,.2f}")
        # Refresh top total income card label text
        self.lbl_income.config(text=f"₱{income:,.2f}")
        # Refresh top total expense card label text
        self.lbl_expenses.config(text=f"₱{expenses:,.2f}")

        # Update Budget Overview Section
        # Refresh budget overview income item label text
        self.lbl_ov_income.config(text=f"₱{income:,.2f}")
        # Refresh budget overview expenses item label text
        self.lbl_ov_expenses.config(text=f"₱{expenses:,.2f}")
        # Refresh budget overview remaining balance label text
        self.lbl_ov_remaining.config(text=f"₱{balance:,.2f}")

    # Function called when submitting the transaction form
    def add_transaction(self):
        # Get description string input removing surrounding whitespace
        desc = self.ent_desc.get().strip()
        # Get amount string input removing surrounding whitespace
        amount_raw = self.ent_amount.get().strip()
        # Get currently selected transaction type value
        trans_type = self.combo_type.get()

        # Validate that description and amount are not empty
        if not desc or not amount_raw:
            # Display warning dialog if any required field is missing
            messagebox.showwarning("Input Error", "Please fill in all fields!")
            # Exit function early
            return

        # Attempt converting raw string amount into floating point number
        try:
            amount = float(amount_raw)
        # Catch conversion errors if input isn't a valid number
        except ValueError:
            # Display error message box for invalid numeric input
            messagebox.showerror("Input Error", "Please enter a valid numeric amount!")
            # Exit function early
            return

        # Append valid new transaction record dictionary to memory array
        self.transactions.append({
            "description": desc,
            "amount": amount,
            "type": trans_type
        })

        # Save updated data array permanently to file
        self.save_data()
        # Update user interface to reflect newly added transaction
        self.update_ui()

        # Clear description entry field content
        self.ent_desc.delete(0, tk.END)
        # Clear amount entry field content
        self.ent_amount.delete(0, tk.END)

    # Function to clear all stored application transaction records
    def clear_all(self):
        # Prompt user with a confirmation prompt before clearing data
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all transaction history?"):
            # Re-initialize transaction memory list to empty
            self.transactions = []
            # Persist empty array to JSON file
            self.save_data()
            # Refresh user interface components
            self.update_ui()

# Check if script is run directly as the main application entry point
if _name_ == "_main_":
    # Instantiate root Tkinter application window
    root = tk.Tk()
    # Instantiate custom budget planner app class instance
    app = ModernBudgetApp(root)
    # Start main event loop listening for user interaction events
    root.mainloop()