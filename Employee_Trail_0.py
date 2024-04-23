import pandas as pd
import numpy as np

# Function to load employee data from CSV file
def load_employee_data(filename):
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        print("Employee data file not found. Starting with empty data.")
        return pd.DataFrame(columns=['ID', 'Name', 'Check-in', 'Check-out'])

# Function to save employee data to CSV file
def save_employee_data(employee_data, filename):
    employee_data.to_csv(filename, index=False)

# Function to handle employee check-in
def check_in(employee_id, employee_name):
    global employee_data  # Declare employee_data as global
    if employee_id in employee_data['ID'].values:
        print(f"Employee {employee_name} is already checked in.")
        return
    employee_data.loc[len(employee_data)] = [employee_id, employee_name, pd.Timestamp.now(), None]
    print(f"Employee {employee_name} checked in at {employee_data.loc[len(employee_data) - 1, 'Check-in']}.")

# Function to handle employee check-out
def check_out(employee_id):
    global employee_data  # Declare employee_data as global
    if employee_id not in employee_data['ID'].values:
        print("Employee ID not found.")
        return
    index = employee_data.index[employee_data['ID'] == employee_id].tolist()[0]
    employee_data.at[index, 'Check-out'] = pd.Timestamp.now()
    print(f"Employee {employee_data.at[index, 'Name']} checked out at {employee_data.at[index, 'Check-out']}.")

# Function to record sales
def record_sales(employee_id, item_sold, quantity, amount):
    global employee_data  # Declare employee_data as global
    employee_name = employee_data.loc[employee_data['ID'] == employee_id, 'Name'].iloc[0]
    new_record = pd.DataFrame([[employee_id, employee_name, None, None, item_sold, quantity, amount]],
                              columns=['ID', 'Name', 'Check-in', 'Check-out', 'Item Sold', 'Quantity', 'Amount'])
    employee_data = pd.concat([employee_data, new_record], ignore_index=True)  # Use global employee_data
    print(f"Sales recorded for {employee_name}: {quantity} {item_sold} sold for ${amount}.")

# Function to generate daily sales report
def generate_daily_sales_report(date):
    global employee_data  # Declare employee_data as global
    employee_data['Check-in'] = pd.to_datetime(employee_data['Check-in'])  # Convert to datetime
    daily_sales = employee_data[employee_data['Check-in'].dt.date == date]
    if not daily_sales.empty:
        print(f"Daily Sales Report for {date}:")
        print(daily_sales[['ID', 'Name', 'Item Sold', 'Quantity', 'Amount']])
        total_sales = daily_sales['Amount'].sum()
        print(f"Total Sales: ${total_sales}")
    else:
        print(f"No sales recorded for {date}.")

    # Save daily sales report to CSV
    daily_sales.to_csv(f'daily_sales_report_{date}.csv', index=False)

# Example usage
# Load existing employee data or start with an empty DataFrame
employee_data = load_employee_data("employee_data.csv")

# Add some dummy employee data if the file was empty
if employee_data.empty:
    employee_data.loc[len(employee_data)] = [1, 'John Doe', None, None]
    employee_data.loc[len(employee_data)] = [2, 'Jane Smith', None, None]





# Employee John Doe checks in
check_in(1, 'John Doe')

# Employee Jane Smith checks in
check_in(2, 'Jane Smith')

# Record sales
record_sales(1, 'Paracetamol', 10, 50.00)
record_sales(2, 'Aspirin', 5, 25.00)

# Employee John Doe checks out
check_out(1)

# Save the updated employee data to the CSV file
save_employee_data(employee_data, "employee_data.csv")

# Generate daily sales report for today
generate_daily_sales_report(pd.Timestamp.now().date())
