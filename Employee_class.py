import pandas as pd

class EmployeeManagement:
    def __init__(self, employee_file):
        self.employee_file = employee_file

    def add_employee(self, name, position, salary):
        try:
            employee_df = pd.read_csv(self.employee_file)
        except FileNotFoundError:
            employee_df = pd.DataFrame(columns=['Name', 'Position', 'Salary'])

        if name in employee_df['Name'].values:
            print(f"{name} is already in the employee list.")
            return
        else:
            new_row_data = pd.DataFrame([[name, position, salary]], columns=['Name', 'Position', 'Salary'])
            employee_df = pd.concat([employee_df, new_row_data], ignore_index=True)

        employee_df.to_csv(self.employee_file, index=False)

    def remove_employee(self, name):
        try:
            employee_df = pd.read_csv(self.employee_file)
        except FileNotFoundError:
            print("Employee file not found.")
            return

        if name in employee_df['Name'].values:
            index = employee_df.index[employee_df['Name'] == name][0]
            employee_df.drop(index, inplace=True)
            employee_df.to_csv(self.employee_file, index=False)
            print(f"{name} has been successfully removed from the employee list.")
        else:
            print(f"{name} does not exist in the employee list.")

    def update_employee(self, name, new_name=None, new_position=None, new_salary=None):
        try:
            employee_df = pd.read_csv(self.employee_file)
        except FileNotFoundError:
            print("Employee file not found.")
            return

        if name in employee_df['Name'].values:
            index = employee_df.index[employee_df['Name'] == name][0]

            # Update the employee details
            if new_name is not None:
                employee_df.at[index, 'Name'] = new_name
            if new_position is not None:
                employee_df.at[index, 'Position'] = new_position
            if new_salary is not None:
                employee_df.at[index, 'Salary'] = new_salary

            employee_df.to_csv(self.employee_file, index=False)
            print(f"{name}'s information has been successfully updated.")
        else:
            print(f"{name} does not exist in the employee list.")

    def list_employees(self):
        try:
            employee_df = pd.read_csv(self.employee_file)
        except FileNotFoundError:
            print("Employee file not found.")
            return {}

        employee_data = {}

        for index, row in employee_df.iterrows():
            name = row['Name']
            position = row['Position']
            salary = row['Salary']
            employee_data[name] = {'Position': position, 'Salary': salary}
        total_employees = len(employee_data)

        return employee_data, total_employees

# Example usage:
employee_management = EmployeeManagement("employees.csv")
employee_management.add_employee("John Doe", "Manager", 50000)
employee_data, total_employees = employee_management.list_employees()
print(employee_data)
