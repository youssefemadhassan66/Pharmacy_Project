import pandas as pd

class Inventory:
    def __init__(self, inventory_file):
        self.inventory_file = inventory_file

    def create_medicine(self, name, quantity, price_per_unit, expiry_date):
        try:
            inventory_df = pd.read_csv(self.inventory_file)
        except FileNotFoundError:
            inventory_df = pd.DataFrame(columns=['Name', 'Quantity', 'Price Per Unit', 'Expiry Date'])

        if name in inventory_df['Name'].values:
            print(f"{name} is already in the inventory.")
            return
        else:
            empty_row_index = inventory_df.index[inventory_df['Name'].isna()].tolist()
            if empty_row_index:
                new_row_data = pd.DataFrame([[name, quantity, price_per_unit, expiry_date]], columns=['Name', 'Quantity', 'Price Per Unit', 'Expiry Date'])
                inventory_df.loc[empty_row_index[0]] = new_row_data.iloc[0]
            else:
                new_row_data = pd.DataFrame([[name, quantity, price_per_unit, expiry_date]], columns=['Name', 'Quantity', 'Price Per Unit', 'Expiry Date'])
                inventory_df = pd.concat([inventory_df, new_row_data], ignore_index=True)

        inventory_df.to_csv(self.inventory_file, index=False, mode='w')

    def delete_medicine(self, name):
        try:
            inventory_df = pd.read_csv(self.inventory_file)
        except FileNotFoundError:
            print("Inventory file not found.")
            return

        if name in inventory_df['Name'].values:
            index = inventory_df.index[inventory_df['Name'] == name][0]
            inventory_df.drop(index, inplace=True)
            inventory_df.to_csv(self.inventory_file, index=False)
            print(f"{name} has been successfully deleted from the inventory.")
        else:
            print(f"{name} does not exist in the inventory.")

    def update_medicine(self, name, new_name=None, new_quantity=None, new_price_per_unit=None, new_expiry_date=None):
        try:
            inventory_df = pd.read_csv(self.inventory_file)
        except FileNotFoundError:
            print("Inventory file not found.")
            return

        if name in inventory_df['Name'].values:
            index = inventory_df.index[inventory_df['Name'] == name][0]

            # Update the medicine details
            if new_name is not None:
                inventory_df.at[index, 'Name'] = new_name
            if new_quantity is not None:
                inventory_df.at[index, 'Quantity'] = new_quantity
            if new_price_per_unit is not None:
                inventory_df.at[index, 'Price Per Unit'] = new_price_per_unit
            if new_expiry_date is not None:
                inventory_df.at[index, 'Expiry Date'] = new_expiry_date

            inventory_df.to_csv(self.inventory_file, index=False)
            print(f"{name} has been successfully updated in the inventory.")
        else:
            print(f"{name} does not exist in the inventory.")

    def read_inventory_units(self):
        try:
            inventory_df = pd.read_csv(self.inventory_file)
        except FileNotFoundError:
            print("Inventory file not found.")
            return {}

        inventory_data = {}

        for index, row in inventory_df.iterrows():
            name = row['Name']
            quantity = row['Quantity']
            price_per_unit = row['Price Per Unit']
            expiry_date = row['Expiry Date']
            inventory_data[name] = {'Quantity': quantity, 'Price Per Unit': price_per_unit, 'Expiry Date': expiry_date}
        total_items = len(inventory_data)

        return inventory_data, total_items


# Example usage:
inventory = Inventory("Medcine.csv")
inventory.create_medicine("Asprin", 400, 1.9, "2024-4-12")
inventory_data, total_items = inventory.read_inventory_units()
print(inventory_data)
