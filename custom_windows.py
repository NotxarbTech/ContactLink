from PyQt6.QtWidgets import (QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QFileDialog, QMessageBox)
import sqlite3
import pandas as pd

con = sqlite3.connect("database.db")
cur = con.cursor()


class AddPartnersWindow(QDialog):
    def __init__(self):
        super(AddPartnersWindow, self).__init__()

        # Set up the main layout for the Add Partners window
        self.setWindowTitle("Add New Partners")
        self.main_layout = QVBoxLayout()

        # Create labels and input fields for partner information
        self.first_name_label = QLabel("First Name:")
        self.first_name_input = QLineEdit()

        self.last_name_label = QLabel("Last Name:")
        self.last_name_input = QLineEdit()

        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()

        self.phone_label = QLabel("Phone:")
        self.phone_input = QLineEdit()

        self.org_label = QLabel("Organization")
        self.org_input = QLineEdit()

        # Create a button to add the partner
        self.add_button = QPushButton("Add Partner")
        self.add_button.clicked.connect(self.addPartner)

        # Create a button to add partners from csv (spreadsheet)
        self.import_button = QPushButton("Import from Spreadsheet")
        self.import_button.clicked.connect(self.importContacts)

        # Add widgets to the main layout
        self.main_layout.addWidget(self.first_name_label)
        self.main_layout.addWidget(self.first_name_input)
        self.main_layout.addWidget(self.last_name_label)
        self.main_layout.addWidget(self.last_name_input)
        self.main_layout.addWidget(self.email_label)
        self.main_layout.addWidget(self.email_input)
        self.main_layout.addWidget(self.phone_label)
        self.main_layout.addWidget(self.phone_input)
        self.main_layout.addWidget(self.org_label)
        self.main_layout.addWidget(self.org_input)
        self.main_layout.addWidget(self.add_button)
        self.main_layout.addWidget(self.import_button)

        # Set the main layout for the Add Partners window
        self.setLayout(self.main_layout)

    def addPartner(self):
        try:
            # Retrieve data from input fields (stripping whitespace)
            first_name = self.first_name_input.text().strip()
            last_name = self.last_name_input.text().strip()
            email = self.email_input.text().strip()
            phone = self.phone_input.text().strip()
            org = self.org_input.text().strip()

            # Add the partner to the database or perform other necessary actions
            insert_data = (f"{first_name} {last_name}", email, phone, org)

            cur.execute("INSERT INTO partners (name, phone, email, org) VALUES (?, ?, ?, ?);", insert_data)
            con.commit()

            # Close the window
            self.accept()
        except Exception as e:
            print(e)

    def importContacts(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Contacts File", "", "CSV Files (*.csv)")

        if file_path:
            try:
                contacts_data = pd.read_csv(file_path)

                # Get the data based on column names
                names = contacts_data["Name"]
                emails = contacts_data["Email"]
                phones = contacts_data["Phone"]
                orgs = contacts_data["Organization"]

                # Loop through all the rows and add them to the database
                for name, email, phone, org in zip(names, emails, phones, orgs):
                    insert_data = (name, email, phone, org)

                    cur.execute("INSERT INTO partners (name, phone, email, org) VALUES (?, ?, ?, ?);", insert_data)
                    con.commit()

                # Close the window
                self.accept()
            except FileNotFoundError:
                QMessageBox.warning(self, "Error", "File Not Found.")
            except KeyError:
                QMessageBox.warning(self, "Error",
                                    "You do not have the proper column names (Name, Email, Phone, Organization)")
