#MAKING CHANGES- ALL UPDATE DO HERE
from tkinter import *
import mysql.connector
from datetime import datetime,timedelta
import ttkbootstrap as ttk
import math
from tkcalendar import Calendar
from functools import partial


connection = mysql.connector.connect(host="localhost", user="root", password="root1234", database="parking")
cursor = connection.cursor()
    
root = ttk.Window(themename='flatly')
root.title("Car Parking Management System")
root.geometry("3000x1500")
#root.config(bg="lightblue")
login_frame = None
login_username = None
login_password = None

#updating:
def calculate_and_update_charges(car_number):
    try:
        # Fetch the car's entry time, exit time, complex_ID, and grace time
        cursor.execute("SELECT entry_time, exit_time, complex_ID FROM car_details WHERE car_number=%s", (car_number,))
        car_details = cursor.fetchone()

        if car_details:
            entry_time = car_details[0]
            exit_time = car_details[1]
            complex_id = car_details[2]

            # Fetch grace time from complex_details for the corresponding complex_ID
            cursor.execute("SELECT grace_time FROM complex_details WHERE complex_ID=%s", (complex_id,))
            grace_time = cursor.fetchone()

            if grace_time:
                grace_time = grace_time[0]  # Grace time in minutes

                # Ensure entry_time and exit_time are in datetime.time format
                if isinstance(entry_time, timedelta):
                    entry_time = (datetime.min + entry_time).time()
                if isinstance(exit_time, timedelta):
                    exit_time = (datetime.min + exit_time).time()

                # Combine entry_time and exit_time with today's date
                today_date = datetime.today().date()
                entry_datetime = datetime.combine(today_date, entry_time)
                exit_datetime = datetime.combine(today_date, exit_time)

                # Calculate the duration between entry time and exit time
                duration = exit_datetime - entry_datetime  # Duration in timedelta

                # Convert duration to total minutes
                total_minutes = duration.total_seconds() / 60  # Convert seconds to minutes

                # Check if the duration between entry and exit is 10 minutes or less
                if total_minutes <= 10:
                    # Apply grace time if the difference is 10 minutes or less
                    total_charges = 0  # No charge if within grace time
                else:
                    # Calculate the charge after grace time
                    chargeable_minutes = total_minutes - grace_time  # Subtract grace time

                    # Ensure chargeable time is positive
                    if chargeable_minutes <= 0:
                        total_charges = 0  # No charge if within grace time
                    else:
                        # Calculate total hours and round it up to the next whole number
                        total_hours = (chargeable_minutes + 59) // 60  # Round up to the nearest hour

                        # Calculate the total charges
                        total_charges = total_hours * 60  # Assuming 60 units per hour charge

                # Update the charges in the Car_Details table
                cursor.execute("UPDATE car_details SET Charges=%s WHERE car_number=%s", (total_charges, car_number))
                connection.commit()

                # Show the "Proceed to Pay?" message
                show_payment_interface(car_number, total_charges)
            else:
                print("Grace time not found for the complex")
        else:
            print("Car details not found")
    except Exception as e:
        print(f"Error calculating charges: {e}")
        ttk.Label(root, text="An error occurred", font=("Helvetica", 16), foreground="red").grid(row=10, column=0, columnspan=2, pady=(40, 10))

def remove_exit_update_label():
    # This function will destroy the label if it exists
    global exit_update_label
    try:
        exit_update_label.destroy()
    except NameError:
        pass  # If the label doesn't exist, this will pass without error

def show_payment_interface(car_number, total_charges):
    remove_exit_update_label()
    for widget in root.winfo_children():
        widget.destroy()

    # Configure the root to center the widgets
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    global form_frame
    # Frame for Form Elements

    global back_button
    form_frame = ttk.Frame(root)
    form_frame.grid(row=1, column=0, pady=10)  # Centered using grid

    heading_label = ttk.Label(form_frame, text="Proceed to Pay?", font=("Helvetica", 30, "bold"))
    heading_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="n")  # Centered using grid

    # Total Charges Label
    charges_label = ttk.Label(form_frame, text=f"Total Charges: ₹{total_charges:.2f}", font=("Helvetica", 16))
    charges_label.grid(row=1, column=0, columnspan=2, padx=20, pady=20)

    # Pay Button
    pay_button = ttk.Button(form_frame, text="Pay", style="success.TButton", command=lambda: process_payment(car_number))
    pay_button.grid(row=2, column=0, padx=20, pady=20)

    # Back Button
    back_button = ttk.Button(form_frame, text="Back", command=update_records, style="secondary.TButton")
    back_button.grid(row=3, column=0, columnspan=2, pady=10)

def process_payment(car_number):
    try:
        # Update the status to 'Paid'
        cursor.execute("UPDATE car_details SET status='Paid' WHERE car_number=%s", (car_number,))
        connection.commit()

        if back_button.winfo_exists():
            back_button.destroy()

        # Show the payment success message
        ttk.Label(form_frame, text="Payment Successful", font=("Helvetica", 16), foreground="green").grid(row=4, column=0, columnspan=2, pady=(40, 10))

        # Back button to return to the update records screen
        back_button1 = ttk.Button(form_frame, text="Back", command=update_records, style="secondary.TButton")
        back_button1.grid(row=6,column=0, columnspan=2, pady=20)  # Adjust grid placement

    except Exception as e:
        print(f"Error processing payment: {e}")
        ttk.Label(form_frame, text="An error occurred", font=("Helvetica", 16), foreground="red").grid(
            row=0, column=0, columnspan=2, pady=(40, 10))


def update_car_number(serial_number, new_car_number, modal_window):
    try:
        cursor.execute("SELECT Serial_No FROM car_details WHERE Serial_No=%s", (serial_number,))
        if cursor.fetchone():
            # Update the car number in the database
            cursor.execute(
                "UPDATE car_details SET Car_Number=%s, modifiedby=%s, modifieddate=%s WHERE Serial_No=%s",
                (new_car_number, username, datetime.now(), serial_number)
            )
            connection.commit()

            # After updating, close the modal and show success message
            modal_window.destroy()
            ttk.Label(form_frame, text="Car Number Updated Successfully", font=("Helvetica", 16), foreground="green").grid(row=10, column=0, columnspan=2, pady=(40, 10))
        else:
            ttk.Label(form_frame, text="Serial Number Not Found", font=("Helvetica", 16), foreground="red").grid(row=10, column=0, columnspan=2, pady=(40, 10))
    
    except Exception as e:
        print(f"Error: {e}")
        ttk.Label(form_frame, text="An error occurred", font=("Helvetica", 16), foreground="red").grid(row=10, column=0, columnspan=2, pady=(40, 10))

def update_exit_time(car_number):
    try:
        current_datetime = datetime.now()
        cursor.execute("SELECT Car_Number FROM car_details WHERE Car_Number=%s", (car_number,))
        if cursor.fetchone():
            # Update the exit time in the database
            cursor.execute(
                "UPDATE car_details SET exit_time=%s, modifiedby=%s, modifieddate=%s WHERE car_number=%s",
                (current_datetime.time(), username, current_datetime.date(), car_number)
            )
            connection.commit()

            # After updating the exit time, calculate and update charges
            calculate_and_update_charges(car_number)

        else:
            error_label = ttk.Label(form_frame, text="Car Number Not Found", font=("Helvetica", 16), foreground="red")
            error_label.grid(row=10, column=0, columnspan=2, pady=(40, 10))

    except Exception as e:
        print(f"Error: {e}")
        error_label = ttk.Label(form_frame, text="An error occurred", font=("Helvetica", 16), foreground="red")
        error_label.grid(row=10, column=0, columnspan=2, pady=(40, 10))

def display_active_car_records_with_update_buttons():
    try:
        # Query to fetch all active car records (including serial number and current car number)
        cursor.execute("SELECT Serial_No, Car_Number FROM Car_details WHERE isactive = 1")
        rows = cursor.fetchall()

        if rows:
            headers = ["Serial No.", "Car Number", "Update"]
            
            # Create a Canvas and a Vertical Scrollbar with increased size
            canvas = ttk.Canvas(form_frame, width=900, height=600)  # Increased vertical size (height=600)
            scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=scrollbar.set)

            # Create a frame inside the canvas to hold the records
            records_frame = ttk.Frame(canvas)

            # Add header labels
            for col_num, header in enumerate(headers):
                label = ttk.Label(records_frame, text=header, font=("Helvetica", 14, "bold"), width=20, anchor="center")
                label.grid(row=0, column=col_num, padx=5, pady=5)

            # Displaying rows with an "Update" button for each
            for row_num, row in enumerate(rows, start=1):
                for col_num, value in enumerate(row):
                    ttk.Label(records_frame, text=value, font=("Helvetica", 12), width=20, anchor="center").grid(row=row_num, column=col_num, padx=5, pady=5)

                # Add Update button for each row
                update_button = ttk.Button(records_frame, text="Update", style="success.TButton", command=lambda serial_number=row[0]: show_update_car_number_modal(serial_number))
                update_button.grid(row=row_num, column=len(row), padx=5, pady=5)

            # Place the frame inside the canvas and configure scrolling
            canvas.create_window((0, 0), window=records_frame, anchor="nw")
            records_frame.update_idletasks()  # Ensure the frame size is updated

            # Configure the scrollbar and canvas
            scrollbar.grid(row=0, column=1, sticky="ns", padx=5, pady=5)
            canvas.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

            # Set scrolling region (extend canvas size based on the number of records)
            canvas.config(scrollregion=canvas.bbox("all"))

        else:
            no_data_label = ttk.Label(form_frame, text="No active car records found.", font=("Helvetica", 14), foreground="red")
            no_data_label.grid(row=1, column=0, columnspan=3, pady=5)

    except Exception as e:
        error_label = ttk.Label(form_frame, text="Error fetching records.", font=("Helvetica", 16), foreground="red")
        error_label.grid(row=1, column=0, columnspan=3, pady=5)
        print(f"Error: {e}")


def show_update_car_number_modal(serial_number):
    modal_window = Toplevel(root)
    modal_window.title("Update Car Number")

    modal_label = ttk.Label(modal_window, text="Enter New Car Number", font=("Helvetica", 14))
    modal_label.pack(pady=10)

    new_car_entry = ttk.Entry(modal_window, font=("Helvetica", 12), width=20)
    new_car_entry.pack(pady=10)

    # Button to update car number
    update_button = ttk.Button(modal_window, text="Update", style="success.TButton", command=lambda: update_car_number(serial_number, new_car_entry.get(), modal_window))
    update_button.pack(pady=20)

def update_car_number_interface():
    # Clear all widgets from the root window
    for widget in root.winfo_children():
        widget.destroy()
    
    # Heading Label
    heading_label = ttk.Label(root, text="Update Car Number", font=("Helvetica", 30, "bold"))
    heading_label.pack(pady=(20, 10))

    # Frame for form elements
    global form_frame
    form_frame = ttk.Frame(root)
    form_frame.pack(pady=10)

    # Display the records and update button for each
    display_active_car_records_with_update_buttons()

    # Back Button
    back_button = ttk.Button(root, text="Back", command=main_menu, style="secondary.TButton")
    back_button.pack(pady=10)

def update_records():
    for widget in root.winfo_children():
        widget.destroy()

    heading_label = ttk.Label(root, text="Update Record", font=("Helvetica", 30, "bold"))
    heading_label.pack(pady=(20, 10))

    global form_frame
    form_frame = ttk.Frame(root)
    form_frame.pack(pady=10)

    car_number_button = ttk.Button(form_frame, text="Update Car Number", style="primary.TButton",
                                   command=update_car_number_interface)
    car_number_button.grid(row=0, column=0, padx=20, pady=10)

    exit_time_button = ttk.Button(form_frame, text="Update Exit Time", style="primary.TButton",
                               command=lambda: update_exit_time_interface())
    exit_time_button.grid(row=1, column=0, padx=20, pady=10)

    back_button = ttk.Button(root, text="Back", command=main_menu, style="secondary.TButton")
    back_button.pack(pady=10)

def update_exit_time_interface():
    # Clear all widgets from the root window
    for widget in root.winfo_children():
        widget.destroy()

    # Heading Label
    heading_label = ttk.Label(root, text="Update Exit Time", font=("Helvetica", 30, "bold"))
    heading_label.pack(pady=(20, 10))

    # Frame for form elements
    global form_frame
    form_frame = ttk.Frame(root)
    form_frame.pack(pady=10)

    # Display the records and update button for each
    display_records_with_update_buttons()

    # Back Button
    back_button = ttk.Button(root, text="Back", command=main_menu, style="secondary.TButton")
    back_button.pack(pady=10)

def display_records_with_update_buttons():
    try:
        # Query to fetch all active car records
        cursor.execute("SELECT Car_Number, Serial_No, Date_Car, Entry_time, Exit_time, Charges FROM Car_details WHERE isactive = 1")
        rows = cursor.fetchall()

        if rows:
            headers = ["Car Number", "Serial No.", "Date", "Entry Time", "Exit Time", "Charges", "Update"]
            
            # Create a Canvas and a Vertical Scrollbar with increased vertical size
            canvas = ttk.Canvas(form_frame, width=900, height=600)  # Increased vertical size (height=600)
            scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=scrollbar.set)

            # Create a frame inside the canvas to hold the records
            records_frame = ttk.Frame(canvas)

            # Add header labels
            for col_num, header in enumerate(headers):
                label = ttk.Label(records_frame, text=header, font=("Helvetica", 14, "bold"), width=15, anchor="center")
                label.grid(row=0, column=col_num, padx=5, pady=5)

            # Displaying rows with an "Update" button for each
            for row_num, row in enumerate(rows, start=1):
                for col_num, value in enumerate(row):
                    ttk.Label(records_frame, text=value, font=("Helvetica", 12), width=15, anchor="center").grid(row=row_num, column=col_num, padx=5, pady=5)

                # Add Update button for each row
                update_button = ttk.Button(records_frame, text="Update", style="success.TButton", command=lambda car_number=row[0]: update_exit_time(car_number))
                update_button.grid(row=row_num, column=len(row), padx=5, pady=5)

            # Place the frame inside the canvas and configure scrolling
            canvas.create_window((0, 0), window=records_frame, anchor="nw")
            records_frame.update_idletasks()  # Ensure the frame size is updated

            # Configure the scrollbar and canvas
            scrollbar.grid(row=0, column=1, sticky="ns", padx=5, pady=5)
            canvas.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

            # Set scrolling region (extend canvas size based on the number of records)
            canvas.config(scrollregion=canvas.bbox("all"))

        else:
            no_data_label = ttk.Label(form_frame, text="No active car records found.", font=("Helvetica", 14), foreground="red")
            no_data_label.grid(row=1, column=0, columnspan=3, pady=5)

    except Exception as e:
        error_label = ttk.Label(form_frame, text="Error fetching records.", font=("Helvetica", 16), foreground="red")
        error_label.grid(row=1, column=0, columnspan=3, pady=5)
        print(f"Error: {e}")
   

def add_qns(entry, txt):
    entry.insert(0, txt)

    style = ttk.Style()
    style.configure('TEntry', foreground='grey')
    entry.configure(style='TEntry')
    
    def on_focus_in(event):
        if entry.get() == txt:
            entry.delete(0, "end")
            entry.configure(style='TEntry')

    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, txt)
            entry.configure(style='TEntry')

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

def view_car_record(date, table_frame):
    try:
        # Clear existing widgets
        for widget in table_frame.winfo_children():
            widget.destroy()
        
        # Example query: Make sure you have a working database connection
        cursor.execute("SELECT Car_Number, Serial_No, Date_Car, Entry_time, Exit_time, Charges FROM car_details WHERE Date_Car = %s AND isactive = 1", (date,))
        rows = cursor.fetchall()

        if rows:
            headers = ["S. No", "Car Number", "Serial No.", "Date", "Entry Time", "Exit Time", "Charges"]

            # Create a Canvas and a Vertical Scrollbar with increased size
            canvas = ttk.Canvas(table_frame, width=900, height=500)  # Increase the canvas size
            scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=scrollbar.set)

            # Create a frame inside the canvas to hold the records
            records_frame = ttk.Frame(canvas)

            # Add header labels
            for col_num, header in enumerate(headers):
                label = ttk.Label(records_frame, text=header, font=("Helvetica", 14, "bold"), width=15)
                label.grid(row=0, column=col_num, padx=5, pady=5)
            
            # Display records
            for row_num, row in enumerate(rows, start=1):
                ttk.Label(records_frame, text=row_num, font=("Helvetica", 12), width=15).grid(row=row_num, column=0, padx=5, pady=5)
                for col_num, value in enumerate(row, start=1):
                    ttk.Label(records_frame, text=value, font=("Helvetica", 12), width=15).grid(row=row_num, column=col_num, padx=5, pady=5)
            
            # Back button
            back_button = ttk.Button(records_frame, text="Back", command=main_menu)
            back_button.grid(row=len(rows) + 1, column=0, columnspan=len(headers), pady=20)

            # Place the frame inside the canvas and configure scrolling
            canvas.create_window((0, 0), window=records_frame, anchor="nw")
            records_frame.update_idletasks()  # Ensure the frame size is updated

            # Configure the scrollbar and canvas
            scrollbar.grid(row=0, column=1, sticky="ns", padx=5, pady=5)
            canvas.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

            # Set scrolling region based on the number of records
            canvas.config(scrollregion=canvas.bbox("all"))

        else:
            no_data_label = ttk.Label(table_frame, text="No records found for the given date.", font=("Helvetica", 14))
            no_data_label.grid(row=1, column=0, columnspan=3, padx=5, pady=10)
    
    except Exception as e:
        error_label = ttk.Label(table_frame, text="Error fetching data.", font=("Helvetica", 16), foreground="red")
        error_label.grid(row=10, column=0, columnspan=2, pady=(40, 10))

        back_button = ttk.Button(table_frame, text="Back", command=view_records)
        back_button.grid(row=4, column=0, padx=5, pady=5)
        
        print(f"Error: {e}")

def delete_car_record_with_ui(car_number):
    try:
        # Mark the record as inactive in the database
        cursor.execute("UPDATE car_details SET isactive=0 WHERE Car_Number=%s", (car_number,))
        connection.commit()

        # Refresh the displayed records
        for widget in form_frame.winfo_children():
            widget.destroy()

        # Show success message and refresh
        success_label = ttk.Label(form_frame, text=f"Record with Car Number {car_number} deleted successfully.", font=("Helvetica", 16), foreground="green")
        success_label.pack(pady=(20, 10))

        # Redisplay the updated list of records
        display_records_with_delete_buttons()

    except Exception as e:
        # Handle errors during deletion
        error_label = ttk.Label(form_frame, text="An error occurred during deletion.", font=("Helvetica", 16), foreground="red")
        error_label.pack(pady=(20, 10))
        print(f"Error: {e}")

def view_records():
    try:
        for widget in root.winfo_children():
            widget.destroy()
        
        heading_label = ttk.Label(root, text="View Records", font=("Helvetica", 30, "bold"))
        heading_label.pack(pady=(20, 10))
        
        # Table Frame
        table_frame = ttk.Frame(root)
        table_frame.pack(expand=True, padx=50, pady=50)
        
        # Calendar Frame
        cal_frame = ttk.Frame(table_frame)
        cal_frame.grid(row=0, column=0, padx=5, pady=10)
        
        # Use Spinboxes for date selection
        date_frame = ttk.Frame(cal_frame)
        date_frame.pack(pady=5)
        
        # Year spinbox
        year_var = StringVar(value='2024')
        year_spin = ttk.Spinbox(date_frame, from_=2000, to=2100, width=6, textvariable=year_var)
        year_spin.pack(side=LEFT, padx=2)
        
        # Month spinbox
        month_var = StringVar(value='12')
        month_spin = ttk.Spinbox(date_frame, from_=1, to=12, width=4, textvariable=month_var)
        month_spin.pack(side=LEFT, padx=2)
        
        # Day spinbox
        day_var = StringVar(value='30')
        day_spin = ttk.Spinbox(date_frame, from_=1, to=31, width=4, textvariable=day_var)
        day_spin.pack(side=LEFT, padx=2)

        def get_selected_date():
            # Format date as YYYY-MM-DD
            year = year_var.get().zfill(4)
            month = month_var.get().zfill(2)
            day = day_var.get().zfill(2)
            return f"{year}-{month}-{day}"
        
        # Search Button
        search_button = ttk.Button(
            table_frame,
            text="Search",
            command=lambda: view_car_record(get_selected_date(), table_frame)
        )
        search_button.grid(row=1, column=0, padx=5, pady=10)
        
        # Back Button
        back_button = ttk.Button(
            table_frame,
            text="Back",
            command=main_menu
        )
        back_button.grid(row=2, column=0, padx=5, pady=10)
        
    except Exception as e:
        print(f"Error in view_records: {e}")        

def save_car_record(car_number):
    try:
        current_datetime = datetime.now()
        cursor.execute(
            "INSERT INTO Car_details (Car_Number, Date_Car, Entry_Time, Complex_ID, isactive, Createdby, createddate)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s)", 
            (car_number, current_datetime.date(), current_datetime.time(), 1, 1, username, current_datetime.date())
        )
        connection.commit()
        ttk.Label(form_frame, text="Record Inserted", font=("Helvetica", 14), foreground="green").grid(row=8, column=0, columnspan=2, pady=5)
        display_existing_records()
    except Exception as e:
        print(f"Error in save_car_record: {e}")
        ttk.Label(form_frame, text="An error occurred", font=("Helvetica", 14), foreground="red").grid(row=8, column=0, columnspan=2, pady=5)

def insert_records():
    try:
        for widget in root.winfo_children(): widget.destroy()
        ttk.Label(root, text="Insert Record", font=("Helvetica", 24, "bold")).pack(pady=5)
        
        global form_frame
        form_frame = ttk.Frame(root)
        form_frame.pack(pady=5)
        
        ttk.Label(form_frame, text="Car Number", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=2)
        car_number_entry = ttk.Entry(form_frame, font=("Helvetica", 12), width=20)
        car_number_entry.grid(row=0, column=1, padx=10, pady=2)
        
        ttk.Button(form_frame, text="Save", command=lambda: save_car_record(car_number_entry.get()), 
                  style="success.TButton").grid(row=1, column=0, columnspan=2, pady=5)
        ttk.Button(form_frame, text="Back", command=main_menu, 
                  style="secondary.TButton").grid(row=2, column=0, columnspan=2, pady=2)
        
        display_existing_records(form_frame)
    except Exception as e:
        print(f"Error in insert_records: {e}")

def display_existing_records(parent_frame):
    for widget in parent_frame.winfo_children():
        if isinstance(widget, ttk.Label) and widget.grid_info().get("row") > 1:
            widget.destroy()
    try:
        cursor.execute("SELECT Car_Number, Date_Car, Entry_Time FROM Car_details WHERE isactive = 1")
        rows = cursor.fetchall()
        
        canvas = ttk.Canvas(parent_frame, width=800, height=100)
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        records_frame = ttk.Frame(canvas)
        
        if rows:
            for col_num, header in enumerate(["Car Number", "Date", "Entry Time"]):
                ttk.Label(records_frame, text=header, font=("Helvetica", 11, "bold")).grid(
                    row=0, column=col_num, padx=15, pady=2)
            
            for row_num, row in enumerate(rows, start=1):
                for col_num, value in enumerate(row):
                    ttk.Label(records_frame, text=value, font=("Helvetica", 11)).grid(
                        row=row_num, column=col_num, padx=15, pady=2)
            
            canvas.create_window((0, 0), window=records_frame, anchor="nw")
            records_frame.update_idletasks()
            canvas.grid(row=3, column=0, sticky="nsew", padx=5, pady=2)
            scrollbar.grid(row=3, column=1, sticky="ns", padx=2, pady=2)
            canvas.config(scrollregion=canvas.bbox("all"))
        else:
            ttk.Label(records_frame, text="No existing records found", font=("Helvetica", 11)).grid(
                row=1, column=0, columnspan=3, pady=2)
        records_frame.pack(fill="both", expand=True)
    except Exception as e:
        print(f"Error in display_existing_records: {e}")
        ttk.Label(parent_frame, text="Error fetching records", font=("Helvetica", 11, "red")).grid(
            row=3, column=0, columnspan=2, pady=2)

def delete_records():
    # Clear existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Create a frame to hold all widgets, centered in the window
    central_frame = ttk.Frame(root)
    central_frame.place(relx=0.5, rely=0.5, anchor="center")

    ttk.Label(
        central_frame, text="Delete Record", font=("Helvetica", 24, "bold")
    ).pack(pady=10)

    global form_frame
    form_frame = ttk.Frame(central_frame)
    form_frame.pack(pady=10, fill="both", expand=True)

    display_records_with_delete_buttons()
    ttk.Button(
        central_frame, text="Back", command=main_menu, style="secondary.TButton"
    ).pack(pady=10)

def display_records_with_delete_buttons():
    try:
        # Clear existing widgets in the frame
        for widget in form_frame.winfo_children():
            widget.destroy()

        # Create a canvas with scrollbar
        canvas = Canvas(form_frame, width=800, height=400)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Fetch records from the database
        cursor.execute("SELECT Serial_No, Car_Number FROM car_details WHERE isactive=1")
        rows = cursor.fetchall()

        if rows:
            # Display headers
            headers = ["Serial No.", "Car Number", "Delete"]
            for col_num, header in enumerate(headers):
                ttk.Label(
                    scrollable_frame, text=header, font=("Helvetica", 12, "bold"),
                    width=20, anchor="center"
                ).grid(row=0, column=col_num, padx=5, pady=2)

            # Display each record with a delete button
            for row_num, row in enumerate(rows, start=1):
                for col_num, value in enumerate(row):
                    ttk.Label(
                        scrollable_frame, text=value, font=("Helvetica", 11),
                        width=20, anchor="center"
                    ).grid(row=row_num, column=col_num, padx=5, pady=2)
                ttk.Button(
                    scrollable_frame, text="Delete", style="danger.TButton",
                    command=partial(delete_car_record_with_ui, car_number=row[1])
                ).grid(row=row_num, column=len(row), padx=5, pady=2)
        else:
            ttk.Label(
                scrollable_frame, text="No active records found.",
                font=("Helvetica", 12), foreground="red"
            ).grid(row=1, column=0, columnspan=3, pady=5)

    except Exception as e:
        print(f"Error: {e}")
        ttk.Label(
            form_frame, text="Error fetching records.",
            font=("Helvetica", 12), foreground="red"
        ).pack(pady=5)

def delete_car_record_with_ui(car_number):
    try:
        cursor.execute("UPDATE car_details SET isactive = 0 WHERE Car_Number = %s", (car_number,))
        con.commit()
        display_records_with_delete_buttons()

        success_label = ttk.Label(
            root, text=f"Record {car_number} deleted successfully.",
            font=("Helvetica", 12), foreground="green"
        )
        success_label.pack(before=form_frame, pady=2)
        root.after(3000, success_label.destroy)
    except Exception as e:
        print(f"Error deleting record: {e}")
        error_label = ttk.Label(
            root, text="Error deleting record.",
            font=("Helvetica", 12), foreground="red"
        )
        error_label.pack(before=form_frame, pady=2)
        root.after(3000, error_label.destroy)

   
def main_menu():
    for widget in root.winfo_children():
        widget.destroy()
    my_style = ttk.Style()
    my_style.configure("But.TLabel", font=("Helvetica", 50, "bold"), anchor="center", padding=10)
    my_style.configure("But.TButton", font=("Helvetica", 14, "bold"), width=20, padding=10)
    main_frame = ttk.Frame(root, padding=(20, 20))
    main_frame.pack(expand=True, padx=50, pady=50)
    heading_label = ttk.Label(main_frame, text="Operations", style="But.TLabel", bootstyle="primary")
    heading_label.grid(row=0, column=0, padx=20, pady=20, sticky="n")
    view_button = ttk.Button(main_frame, text="View Records", command=view_records, style="But.TButton", bootstyle="SUCCESS")
    view_button.grid(row=1, column=0, pady=(10, 20))
    insert_button = ttk.Button(main_frame, text="Insert Record", command=insert_records, style="But.TButton", bootstyle="SUCCESS")
    insert_button.grid(row=2, column=0, pady=(10, 20))

    update_button = ttk.Button(main_frame, text="Update Record", command=update_records, style="But.TButton", bootstyle="SUCCESS")
    update_button.grid(row=3, column=0, pady=(10, 20))

    delete_button = ttk.Button(main_frame, text="Delete Record", command=delete_records, style="But.TButton", bootstyle="SUCCESS")
    delete_button.grid(row=4, column=0, pady=(10, 20))
    logout_button = ttk.Button(main_frame, text="Logout", command=logout, style="But.TButton", bootstyle="DANGER")
    logout_button.grid(row=5, column=0, pady=(40, 10))

def logout():
    for widget in root.winfo_children():
        widget.destroy()
    username=""
    password=""
    login_page()
    ttk.Label(login_frame, text="You have successfully been logged out", font=("Helvetica", 14), bootstyle="Danger").grid(row=7,column=0, columnspan=1,sticky="n")
    

def sign_up():
    employee_id = employee_id_entry.get()
    designation = designation_entry.get()
    name = name_entry.get()
    mail = mail_entry.get()
    password = password_entry.get()
    try:
        phone_no = int(phone_no_entry.get())
        complex_no = int(complex_no_entry.get())
    except ValueError:
        show_error("Phone number and complex number must be integers!")
        return
    cursor.execute("SELECT POS_ID FROM EMP_TYPE WHERE POS = %s", (designation,))
    val = cursor.fetchone()
    if not val:
        show_error("Invalid Designation")
        return
    pos = int(val[0])

    current_datetime = datetime.now()
    current_date = current_datetime.date()
    cursor.execute("INSERT INTO EMP_DETAILS (EMP_ID, POS_ID, EMP_NAME, MAIL, PASS, PH_NO, COMPLEX_ID, ISACTIVE, CREATEDBY, CREATEDDATE)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(employee_id, pos, name, mail, password, phone_no, complex_no, 1, name, current_date))
    connection.commit()
    Label(sign_up_frame, text="Account Created", font=("Helvetica", 16), bg="lightblue", fg="green").grid(row=10, column=0, columnspan=2, pady=(40, 10))

def login_page():
    global login_frame, login_username, login_password
    login_frame = ttk.Frame(root, padding=(20, 20))
    login_frame.pack(expand=True, padx=50, pady=50)
    ttk.Label(login_frame, text="Login", font=("Helvetica", 50, "bold"), bootstyle="primary").grid(row=0, column=0, pady=(20, 10), sticky="n")
    login_username = ttk.Entry(login_frame, width=40, font=("Helvetica", 14))
    login_username.grid(row=1, column=0, padx=20, pady=10)
    add_qns(login_username, "Employee ID")
    login_password = ttk.Entry(login_frame, show="", width=40, font=("Helvetica", 14))
    login_password.grid(row=2, column=0, padx=20, pady=10)
    add_qns(login_password, "Password")
    ttk.Button(login_frame, text="Submit", command=check_user, bootstyle="SUCCESS").grid(row=3, column=0, columnspan=2, pady=(10, 40))
    ttk.Label(login_frame, text="Don't have an account?", font=("Helvetica", 14), bootstyle="secondary").grid(row=4, column=0, columnspan=1)
    ttk.Button(login_frame, text="Sign Up", command=open_sign_up_page, bootstyle="info-outline").grid(row=5, column=0, columnspan=2, pady=10)

def check_user():
    global username, password

    username = login_username.get()
    password = login_password.get()

    try:
        # Query the database to check if the user exists
        cursor.execute("SELECT * FROM EMP_DETAILS WHERE EMP_ID = %s AND PASS = %s AND ISACTIVE = 1", (username, password))
        user = cursor.fetchone()

        if user:
            # Clear the login frame and proceed to main menu
            for widget in root.winfo_children():
                widget.destroy()
            main_menu()
        else:
            ttk.Label(login_frame, text="Invalid Employee ID or Password", font=("Helvetica", 14), bootstyle="danger").grid(row=6, column=0, pady=10)
    except Exception as e:
        print(f"Error during login: {e}")
        ttk.Label(login_frame, text="An error occurred during login", font=("Helvetica", 14), bootstyle="danger").grid(row=6, column=0, pady=10)
 

    
def open_sign_up_page():
    sign_up_window = Toplevel(root)
    sign_up_window.title("Sign Up")
    sign_up_window.geometry("3000x1500")
    global sign_up_frame
    sign_up_frame = ttk.Frame(sign_up_window, padding=(20, 20))
    sign_up_frame.pack(expand=True, padx=50, pady=50)
    heading_label = ttk.Label(sign_up_frame, text="Sign Up", font=("Helvetica", 50, "bold"), bootstyle="primary")
    heading_label.grid(row=0, column=0, columnspan=1, pady=(20, 40), sticky="n")
    global employee_id_entry, designation_entry, name_entry, mail_entry, password_entry, phone_no_entry, complex_no_entry
    employee_id_entry = ttk.Entry(sign_up_frame, width=40, font=("Helvetica", 14))
    employee_id_entry.grid(row=1, column=0, padx=20, pady=10)
    add_qns(employee_id_entry, "Employee ID")
    designation_entry = ttk.Entry(sign_up_frame, width=40, font=("Helvetica", 14))
    designation_entry.grid(row=2, column=0, padx=20, pady=10)
    add_qns(designation_entry, "Designation")
    name_entry = ttk.Entry(sign_up_frame, width=40, font=("Helvetica", 14))
    name_entry.grid(row=3, column=0, padx=20, pady=10)
    add_qns(name_entry, "Name")
    mail_entry = ttk.Entry(sign_up_frame, width=40, font=("Helvetica", 14))
    mail_entry.grid(row=4, column=0, padx=20, pady=10)
    add_qns(mail_entry, "Mail ID")
    password_entry = ttk.Entry(sign_up_frame, width=40, font=("Helvetica", 14))
    password_entry.grid(row=5, column=0, padx=20, pady=10)
    add_qns(password_entry, "Password")
    phone_no_entry = ttk.Entry(sign_up_frame, width=40, font=("Helvetica", 14))
    phone_no_entry.grid(row=6, column=0, padx=20, pady=10)
    add_qns(phone_no_entry, "Phone number")
    complex_no_entry = ttk.Entry(sign_up_frame, width=40, bootstyle="secondary", font=("Helvetica", 14))
    complex_no_entry.grid(row=7, column=0, padx=20, pady=10)
    add_qns(complex_no_entry, "Complex ID")
    sign_up_button = ttk.Button(sign_up_frame, text="Sign Up", bootstyle="SUCCESS", command=sign_up)
    sign_up_button.grid(row=8, column=0, columnspan=1, pady=(40, 10))
    
def show_error(message):
    error_box = Toplevel(root)
    error_box.title("Error")
    error_box.geometry("400x100")
    ttk.Label(error_box, text=message, font=("Helvetica", 14), bootstyle="Danger").pack(pady=20)
    ttk.Button(error_box, text="OK", command=error_box.destroy, bootstyle="Light").pack()


login_page()
root.mainloop()
cursor.close()
connection.close()
