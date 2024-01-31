from PyQt6.QtWidgets import QLabel, QVBoxLayout, QFrame, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt
import sqlite3

from custom_windows import EditPartnersWindow

# Connection and cursor to access and modify and read from the database
con = sqlite3.connect("database.db")
cur = con.cursor()


class PartnerContactWidget(QFrame):
    def __init__(self, name, email, phone, org, partner_id, main_window):
        super(PartnerContactWidget, self).__init__()

        self.name_label = QLabel(f"Name: {name}", alignment=Qt.AlignmentFlag.AlignHCenter)
        self.email_label = QLabel(f"Email: {email}", alignment=Qt.AlignmentFlag.AlignHCenter)
        self.phone_label = QLabel(f"Phone: {phone}", alignment=Qt.AlignmentFlag.AlignHCenter)
        self.org_label = QLabel(f"Organization: {org}", alignment=Qt.AlignmentFlag.AlignHCenter)
        self.id = partner_id
        self.main_window = main_window

        # Button that allows user to edit the partner's info or delete
        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.editPartner)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.deletePartner)

        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.name_label)
        top_layout.addWidget(self.email_label)
        top_layout.addWidget(self.edit_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.phone_label)
        bottom_layout.addWidget(self.org_label)
        bottom_layout.addWidget(self.delete_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

        # Set the frame style to have a box around the widget
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)

    # Checks if text is in the person's name
    def matchSearchText(self, text):
        text_to_match = self.name_label.text().lower()
        return text.lower() in text_to_match

    def editPartner(self):
        dialog_window = EditPartnersWindow(self.id, self.main_window)
        dialog_window.exec()

    def deletePartner(self):
        cur.execute("DELETE FROM partners WHERE id = ?", str(self.id))
        con.commit()
        self.main_window.loadPartners()
