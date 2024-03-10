from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QDialog, QLabel, QLineEdit,
                             QVBoxLayout, QPushButton, QFileDialog,
                             QMessageBox, QPlainTextEdit, QHBoxLayout,
                             QCheckBox, QButtonGroup)
import sqlite3
import pandas as pd

con = sqlite3.connect("database.db")
cur = con.cursor()


class AddPartnersWindow(QDialog):
    def __init__(self):
        super(AddPartnersWindow, self).__init__()

        # Set up the main layout for the Add Partners window
        self.setWindowTitle("Add New Partners")
        self.setWindowIcon(QIcon("resources/favicon.jpg"))
        self.setGeometry(800, 200, 400, 300)
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

        self.address_label = QLabel("Address")
        self.address_input = QLineEdit()

        self.profile_pic_label = QLabel("Profile Picture (Optional)")
        self.profile_pic_input = QPushButton("Browse")

        # Add the profile picture if one is entered
        self.profile_picture_data = None
        self.profile_pic_input.clicked.connect(self.addProfilePicture)

        # Create a button to add the partner
        self.add_button = QPushButton("Add Partner")
        self.add_button.clicked.connect(self.addPartner)
        self.add_button.setDefault(True)

        # Create a button to add partners from csv (spreadsheet)
        self.import_button = QPushButton("Import from Spreadsheet")
        self.import_button.clicked.connect(self.importContacts)

        # Add widgets to the main layout
        self.main_layout.addWidget(self.first_name_label)
        self.main_layout.addWidget(self.first_name_input)

        self.main_layout.addWidget(self.last_name_label)
        self.main_layout.addWidget(self.last_name_input)

        self.main_layout.addWidget(self.profile_pic_label)
        self.main_layout.addWidget(self.profile_pic_input)

        self.main_layout.addWidget(self.email_label)
        self.main_layout.addWidget(self.email_input)

        self.main_layout.addWidget(self.phone_label)
        self.main_layout.addWidget(self.phone_input)

        self.main_layout.addWidget(self.org_label)
        self.main_layout.addWidget(self.org_input)

        self.main_layout.addWidget(self.address_label)
        self.main_layout.addWidget(self.address_input)

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
            address = self.address_input.text().strip()

            # Makes sure none of the input fields are blank
            input_fields = [first_name, last_name, email, phone, org, address]
            for field in input_fields:
                if field == "":
                    QMessageBox.warning(self, "Blank Fields", "You cannot leave any fields blank!")
                    return

            # Add the partner to the database or perform other necessary actions
            insert_data = (f"{first_name} {last_name}", email, phone, org, address)

            # Check if there's a profile picture to insert
            if self.profile_picture_data is not None:
                cur.execute("INSERT INTO partners (name, phone, email, org, address, profile_picture)"
                            " VALUES (?, ?, ?, ?, ?, ?);", (*insert_data, self.profile_picture_data))
                con.commit()
            else:
                cur.execute("INSERT INTO partners (name, phone, email, org, address) VALUES (?, ?, ?, ?, ?);",
                            insert_data)
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
                address = contacts_data["Address"]

                # Loop through all the rows and add them to the database
                for name, email, phone, org in zip(names, emails, phones, orgs, address):
                    insert_data = (name, email, phone, org, address)

                    cur.execute("INSERT INTO partners (name, phone, email, org, address) VALUES (?, ?, ?, ?, ?);",
                                insert_data)
                    con.commit()

                # Close the window
                self.accept()
            except FileNotFoundError:
                QMessageBox.warning(self, "Error", "File Not Found.")
            except KeyError:
                QMessageBox.warning(self, "Error",
                                    "You do not have the proper column names (Name, Email, Phone, Organization,"
                                    " Mailing Address)")

    def addProfilePicture(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Profile Picture File", "",
                                                   "All Files (*)")

        if file_path:
            try:
                if file_path.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    with open(file_path, "rb") as file:
                        self.profile_picture_data = file.read()
                else:
                    QMessageBox.warning(self, "Wrong or Unsupported File Type", "Supported file types are"
                                                                                " jpg, jpeg, png, and webp")
            except Exception as e:
                print(e)


class EditPartnersWindow(QDialog):
    def __init__(self, partner_id, main_window):
        super(EditPartnersWindow, self).__init__()

        self.main_window = main_window

        self.partner_info = cur.execute("SELECT * FROM partners WHERE id = ?", (partner_id,)).fetchone()

        # Set up the main layout for the Edit Partners window
        self.setWindowTitle("Edit Partners")
        self.setWindowIcon(QIcon("resources/favicon.jpg"))
        self.setGeometry(800, 200, 400, 300)
        self.main_layout = QVBoxLayout()

        # Create labels and input fields for partner information (already display the existing info)
        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        self.name_input.setText(self.partner_info[1])

        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setText(self.partner_info[2])

        self.phone_label = QLabel("Phone:")
        self.phone_input = QLineEdit()
        self.phone_input.setText(self.partner_info[3])

        self.org_label = QLabel("Organization")
        self.org_input = QLineEdit()
        self.org_input.setText(self.partner_info[4])

        self.address_label = QLabel("Mailing Address")
        self.address_input = QLineEdit()
        self.address_input.setText(self.partner_info[5])

        self.profile_picture_data = None
        self.profile_picture_label = QLabel("Add/Edit Profile Picture")
        self.profile_picture_input = QPushButton("Browse")
        self.profile_picture_input.clicked.connect(self.changeProfilePicture)

        # Create a button to save the changes
        self.add_button = QPushButton("Save Changes")
        self.add_button.clicked.connect(self.updatePartner)
        self.add_button.setDefault(True)

        # Add widgets to the main layout
        self.main_layout.addWidget(self.name_label)
        self.main_layout.addWidget(self.name_input)
        self.main_layout.addWidget(self.profile_picture_label)
        self.main_layout.addWidget(self.profile_picture_input)
        self.main_layout.addWidget(self.email_label)
        self.main_layout.addWidget(self.email_input)
        self.main_layout.addWidget(self.phone_label)
        self.main_layout.addWidget(self.phone_input)
        self.main_layout.addWidget(self.org_label)
        self.main_layout.addWidget(self.org_input)
        self.main_layout.addWidget(self.address_label)
        self.main_layout.addWidget(self.address_input)
        self.main_layout.addWidget(self.add_button)

        # Set the main layout for the Add Partners window
        self.setLayout(self.main_layout)

    def updatePartner(self):
        try:
            # Retrieve data from input fields (stripping whitespace)
            name = self.name_input.text().strip()
            email = self.email_input.text().strip()
            phone = self.phone_input.text().strip()
            org = self.org_input.text().strip()
            address = self.address_input.text().strip()

            # Add the partner to the database or perform other necessary actions
            if self.profile_picture_data is not None:
                cur.execute("UPDATE partners SET name=?, phone=?, email=?, org=?, address=?, profile_picture=?"
                            " WHERE id = ?;",
                            (name, email, phone, org, address, self.profile_picture_data, self.partner_info[0]))
                con.commit()
            else:
                cur.execute("UPDATE partners SET name=?, phone=?, email=?, org=?, address=? WHERE id = ?;",
                            (name, email, phone, org, address, self.partner_info[0]))
                con.commit()

            # Refresh the main window display
            self.main_window.loadPartners()

            # Close the window
            self.accept()
        except Exception as e:
            print(e)

    def changeProfilePicture(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Profile Picture File", "",
                                                   "All Files (*)")

        if file_path:
            try:
                if file_path.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    with open(file_path, "rb") as file:
                        self.profile_picture_data = file.read()
                else:
                    QMessageBox.warning(self, "Wrong or Unsupported File Type", "Supported file types are"
                                                                                " jpg, jpeg, png, and webp")
            except Exception as e:
                print(e)


class EditPartnerNotesWindow(QDialog):
    def __init__(self, partner_id, partner_name):
        super(EditPartnerNotesWindow, self).__init__()

        self.id = partner_id
        self.name = partner_name

        # Retrieve the partner's notes from the database
        self.notes = cur.execute("SELECT notes FROM partners WHERE id = ?", (self.id,)).fetchone()

        # Set up the window
        self.setWindowTitle(f"Edit {self.name}'s Notes")
        self.setWindowIcon(QIcon("resources/favicon.jpg"))
        self.setGeometry(800, 200, 400, 300)

        self.main_layout = QVBoxLayout()

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.saveNotes)
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clearNotes)

        # Set up a text box already populated with the partner's notes
        self.text_box = QPlainTextEdit()
        self.text_box.setPlainText(self.notes[0])

        # Toolbar with save and clear buttons
        self.toolbar_layout = QHBoxLayout()
        self.toolbar_layout.addWidget(self.save_button)
        self.toolbar_layout.addWidget(self.clear_button)

        self.main_layout.addWidget(self.text_box)
        self.main_layout.addLayout(self.toolbar_layout)
        self.setLayout(self.main_layout)

    def saveNotes(self):
        # SQL command to save the notes into the database
        cur.execute("UPDATE partners SET notes = ? WHERE id = ?", (self.text_box.toPlainText(), self.id))
        con.commit()

        # Close the window
        self.accept()

    def clearNotes(self):
        # Clears the text box
        self.text_box.setPlainText(None)


class FilterSearchWindow(QDialog):
    def __init__(self, filter_name, filter_org, filter_notes, main_window):
        super(FilterSearchWindow, self).__init__()

        # Set up the window
        self.setWindowTitle("Filter Search Results")
        self.setWindowIcon(QIcon("resources/favicon.jpg"))
        self.setGeometry(900, 300, 200, 100)
        self.main_layout = QVBoxLayout()
        self.main_window = main_window

        # Checkboxes for different filter options
        self.name_checkbox = QCheckBox("Name")
        self.org_checkbox = QCheckBox("Organization")
        self.notes_checkbox = QCheckBox("Notes")

        if filter_name:
            self.name_checkbox.setChecked(True)
        elif filter_org:
            self.org_checkbox.setChecked(True)
        elif filter_notes:
            self.notes_checkbox.setChecked(True)

        # Button group to contain the checkboxes
        self.filter_button_group = QButtonGroup()
        self.filter_button_group.addButton(self.name_checkbox)
        self.filter_button_group.addButton(self.org_checkbox)
        self.filter_button_group.addButton(self.notes_checkbox)
        self.filter_button_group.setExclusive(True)

        # Detect change and update variables in the main window
        self.name_checkbox.stateChanged.connect(lambda: self.filterStateChanged(True, False, False))
        self.org_checkbox.stateChanged.connect(lambda: self.filterStateChanged(False, True, False))
        self.notes_checkbox.stateChanged.connect(lambda: self.filterStateChanged(False, False, True))

        self.main_layout.addWidget(self.name_checkbox)
        self.main_layout.addWidget(self.org_checkbox)
        self.main_layout.addWidget(self.notes_checkbox)

        self.setLayout(self.main_layout)

    def filterStateChanged(self, filter_name, filter_org, filter_notes):
        if filter_name:
            self.main_window.filter_name = True
            self.main_window.filter_org = False
            self.main_window.filter_notes = False
        if filter_org:
            self.main_window.filter_name = False
            self.main_window.filter_org = True
            self.main_window.filter_notes = False
        if filter_notes:
            self.main_window.filter_name = False
            self.main_window.filter_org = False
            self.main_window.filter_notes = True


class HelpWindow(QDialog):
    def __init__(self):
        super(HelpWindow, self).__init__()

        # Window setup
        self.setWindowTitle("Help and FAQ")
        self.setGeometry(750, 300, 600, 600)
        self.setWindowIcon(QIcon("resources/favicon.jpg"))
        self.main_layout = QVBoxLayout()

        # Title at the top of the page, centered horizontally
        self.title_widget = QLabel("Help and FAQ")
        title_widget_font = self.title_widget.font()
        title_widget_font.setPointSize(26)
        self.title_widget.setFont(title_widget_font)
        self.title_widget.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Frequently Asked Questions/Help Section
        section_title_font = self.title_widget.font()
        section_title_font.setPointSize(20)

        section_content_font = self.title_widget.font()
        section_content_font.setPointSize(14)

        self.section1_title = QLabel("How do I add a new partner?")
        self.section1_title.setFont(section_title_font)

        self.section1_content = QLabel(
            'To add a new partner, click on the "Add New Partners" button on the main screen.'
            " This will open a window where you can enter the partner's information such as"
            " name, email, phone, organization, and address. You can also add a profile picture if desired.")
        self.section1_content.setFont(section_content_font)
        self.section1_content.setWordWrap(True)

        self.section2_title = QLabel("Can I import contacts from a spreadsheet?")
        self.section2_title.setFont(section_title_font)

        self.section2_content = QLabel(
            'Yes, you can import partner data from a CSV (spreadsheet) file. Click on the "Import from Spreadsheet"'
            ' button on the add partners window. Make sure your spreadsheet has the correct column names'
            ' (Name, Email, Phone, Organization, Address), then select the file to import.')
        self.section2_content.setFont(section_content_font)
        self.section2_content.setWordWrap(True)

        self.section3_title = QLabel("What file types are supported for profile pictures?")
        self.section3_title.setFont(section_title_font)

        self.section3_content = QLabel(
            "Profile pictures can be in JPG, JPEG, PNG, or WEBP formats. When adding or editing a partner, you can"
            " browse your computer to select a profile picture file of one of these types.")
        self.section3_content.setFont(section_content_font)
        self.section3_content.setWordWrap(True)

        self.extra_questions_link = QLabel(
            '<a href="https://forms.gle/moZka7BF5fnN2qJe9">Have additional questions or feedback? Click here!</a>')
        self.extra_questions_link.setOpenExternalLinks(True)
        self.extra_questions_link.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.main_layout.addWidget(self.title_widget)
        self.main_layout.addWidget(self.section1_title)
        self.main_layout.addWidget(self.section1_content)
        self.main_layout.addWidget(self.section2_title)
        self.main_layout.addWidget(self.section2_content)
        self.main_layout.addWidget(self.section3_title)
        self.main_layout.addWidget(self.section3_content)
        self.main_layout.addWidget(self.extra_questions_link)

        self.setLayout(self.main_layout)
