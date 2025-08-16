import tkinter as tk
from tkinter import messagebox
import csv

# --- Police class ---
class Police:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def dashboard(self):
        open_police_dashboard()

# --- Validate login ---
def validate_login(role):
    if role == "police":
        username = police_username_entry.get()
        password = police_password_entry.get()
        if validate_police_credentials(username, password):
            police = Police(username, password)
            police.dashboard()
        else:
            messagebox.showerror("Error", "Invalid police credentials.")
    else:
        vehicle_number = vehicle_number_var.get().strip().upper()
        if vehicle_number:
            open_driver_dashboard(vehicle_number)
        else:
            messagebox.showerror("Error", "Please enter vehicle number.")

# --- Validate police credentials ---
def validate_police_credentials(username, password):
    try:
        with open('police_credentials.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['username'] == username and row['password'] == password:
                    return True
    except FileNotFoundError:
        messagebox.showerror("Error", "Police credentials file not found.")
    return False

# --- Police dashboard ---
def open_police_dashboard():
    def print_receipt():
        vehicle = vehicle_entry_var.get().strip().upper()
        fine = fine_entry_var.get().strip()
        offence = offence_var.get()

        if not vehicle or not fine or offence == "Select Offence":
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        with open('vehicle_fines.csv', 'a', newline='') as csvfile:
            fieldnames = ['vehicle_number', 'fine_amount', 'offence']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow({
                'vehicle_number': vehicle,
                'fine_amount': fine,
                'offence': offence
            })

        receipt_text = f"Vehicle Number: {vehicle}\nFine Amount: Rs. {fine}\nOffence: {offence}"
        receipt_window = tk.Toplevel(root)
        receipt_window.title("Receipt")
        receipt_window.geometry("400x300")
        tk.Label(receipt_window, text="Receipt", font=("Garamond", 20, "bold")).pack(pady=10)
        tk.Label(receipt_window, text=receipt_text, font=("Garamond", 16)).pack(pady=10)

        vehicle_entry_var.set("")
        fine_entry_var.set("")
        offence_var.set("Select Offence")
        print_button.config(state=tk.DISABLED)

    def enable_print_button(*args):
        if fine_entry_var.get().strip().isdigit():
            print_button.config(state=tk.NORMAL)
        else:
            print_button.config(state=tk.DISABLED)

    police_window = tk.Toplevel(root)
    police_window.title("Police Dashboard")
    police_window.geometry("1000x1000")
    police_window.configure(bg="#add8e6")

    tk.Label(police_window, text="Police Dashboard", font=("Garamond", 30, "bold"), bg="#add8e6").pack(pady=20)

    form_frame = tk.Frame(police_window, bg="#add8e6")
    form_frame.pack(pady=20)

    tk.Label(form_frame, text="Enter Vehicle Number:", font=("Garamond", 20, "bold"), bg="#add8e6").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    vehicle_entry_var = tk.StringVar()
    vehicle_entry = tk.Entry(form_frame, font=("Garamond", 18), width=20, textvariable=vehicle_entry_var)
    vehicle_entry.grid(row=0, column=1, padx=10, pady=10)
    vehicle_entry_var.trace("w", lambda *args: vehicle_entry_var.set(vehicle_entry_var.get().upper()))

    tk.Label(form_frame, text="Add Fine:", font=("Garamond", 20, "bold"), bg="#add8e6").grid(row=1, column=0, padx=10, pady=10, sticky='e')
    fine_entry_var = tk.StringVar()
    fine_entry = tk.Entry(form_frame, font=("Garamond", 18), width=10, textvariable=fine_entry_var)
    fine_entry.grid(row=1, column=1, padx=10, pady=10)
    fine_entry_var.trace("w", enable_print_button)

    validate_numeric = police_window.register(lambda P: P.isdigit() or P == "")
    fine_entry.config(validate="key", validatecommand=(validate_numeric, '%P'))

    tk.Label(form_frame, text="Rs.", font=("Garamond", 18), bg="#add8e6").grid(row=1, column=2, padx=10, pady=10, sticky='w')

    tk.Label(form_frame, text="Offence:", font=("Garamond", 20, "bold"), bg="#add8e6").grid(row=2, column=0, padx=10, pady=10, sticky='e')
    offence_var = tk.StringVar(value="Select Offence")
    offence_menu = tk.OptionMenu(form_frame, offence_var, "Speeding", "Reckless Driving", "Parking Violation")
    offence_menu.config(font=("Garamond", 18))
    offence_menu.grid(row=2, column=1, padx=10, pady=10, sticky='w')

    print_button = tk.Button(form_frame, text="Print", font=("Garamond", 18, "bold"), width=10, command=print_receipt, state=tk.DISABLED)
    print_button.grid(row=3, columnspan=3, pady=20)

# --- Driver dashboard ---
def open_driver_dashboard(vehicle_number):
    driver_window = tk.Toplevel(root)
    driver_window.title("Driver Dashboard")
    driver_window.geometry("600x400")
    driver_window.configure(bg="#add8e6")

    tk.Label(driver_window, text="Driver Dashboard", font=("Garamond", 28, "bold"), bg="#add8e6").pack(pady=20)

    fines = []
    try:
        with open('vehicle_fines.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['vehicle_number'].strip().upper() == vehicle_number:
                    fines.append(row)
    except FileNotFoundError:
        messagebox.showerror("Error", "Fines data file not found.")
        return

    if fines:
        for fine in fines:
            fine_text = f"Vehicle: {fine['vehicle_number']} | Fine: Rs. {fine['fine_amount']} | Offence: {fine['offence']}"
            tk.Label(driver_window, text=fine_text, font=("Garamond", 16), bg="#add8e6").pack(pady=5)
    else:
        tk.Label(driver_window, text="No fines found for this vehicle.", font=("Garamond", 18), bg="#add8e6").pack(pady=20)

# --- GUI Layout ---
def show_frame(frame):
    frame.tkraise()

root = tk.Tk()
root.title("Traffic Challan Management System")
root.geometry("998x668")
root.resizable(False, False)

# Frames
main_frame = tk.Frame(root, highlightbackground="black", highlightthickness=1, bg="#1B3481")
police_login_frame = tk.Frame(root, highlightbackground="black", highlightthickness=1, bg="#add8e6")
driver_login_frame = tk.Frame(root, highlightbackground="black", highlightthickness=1, bg="#add8e6")

for frame in (main_frame, police_login_frame, driver_login_frame):
    frame.place(x=0, y=0, width=998, height=668)

# --- Main Page ---
tk.Label(main_frame, text="TRAFFIC CHALLAN MANAGEMENT SYSTEM", font=("Garamond", 30, "bold"), bg="#1B3481", fg="white").pack(pady=50)
tk.Button(main_frame, text="Police Login", command=lambda: show_frame(police_login_frame), font=("Garamond", 18, "bold"), width=15).pack(pady=10)
tk.Button(main_frame, text="Driver Login", command=lambda: show_frame(driver_login_frame), font=("Garamond", 18, "bold"), width=15).pack(pady=10)

# --- Police Login ---
tk.Label(police_login_frame, text="POLICE LOGIN", font=("Garamond", 30, "bold"), bg="#add8e6").pack(pady=50)
tk.Label(police_login_frame, text="Username:", font=("Garamond", 18), bg="#add8e6").pack()
police_username_entry = tk.Entry(police_login_frame, font=("Garamond", 18))
police_username_entry.pack()
tk.Label(police_login_frame, text="Password:", font=("Garamond", 18), bg="#add8e6").pack()
police_password_entry = tk.Entry(police_login_frame, show="*", font=("Garamond", 18))
police_password_entry.pack()

tk.Button(police_login_frame, text="Login", command=lambda: validate_login("police"), font=("Garamond", 18, "bold"), width=10).pack(pady=10)
tk.Button(police_login_frame, text="Back", command=lambda: show_frame(main_frame), font=("Garamond", 18, "bold"), width=10).pack(pady=10)

# --- Driver Login ---
tk.Label(driver_login_frame, text="DRIVER LOGIN", font=("Garamond", 30, "bold"), bg="#add8e6").pack(pady=50)
tk.Label(driver_login_frame, text="Vehicle Number:", font=("Garamond", 18), bg="#add8e6").pack()
vehicle_number_var = tk.StringVar()
vehicle_number_entry = tk.Entry(driver_login_frame, font=("Garamond", 18), textvariable=vehicle_number_var)
vehicle_number_entry.pack()
vehicle_number_var.trace("w", lambda *args: vehicle_number_var.set(vehicle_number_var.get().upper()))

tk.Button(driver_login_frame, text="Login", command=lambda: validate_login("driver"), font=("Garamond", 18, "bold"), width=10).pack(pady=10)
tk.Button(driver_login_frame, text="Back", command=lambda: show_frame(main_frame), font=("Garamond", 18, "bold"), width=10).pack(pady=10)

# --- Start the app on main frame ---
show_frame(main_frame)
root.mainloop()
