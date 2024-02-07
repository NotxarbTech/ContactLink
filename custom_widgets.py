from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QLabel, QVBoxLayout, QFrame,
                             QHBoxLayout, QPushButton, QSpacerItem,
                             QSizePolicy)
from PyQt6.QtCore import Qt
import sqlite3

from custom_windows import EditPartnersWindow, EditPartnerNotesWindow

# Connection and cursor to access and modify and read from the database
con = sqlite3.connect("database.db")
cur = con.cursor()


class PartnerContactWidget(QFrame):
    def __init__(self, name, email, phone, org, address, partner_id, main_window):
        super(PartnerContactWidget, self).__init__()

        self.top_layout = QHBoxLayout()
        self.main_layout = QVBoxLayout()

        self.name = name
        self.email = email
        self.phone = phone
        self.org = org
        self.address = address
        self.id = partner_id
        self.main_window = main_window

        self.profile_picture_label = QLabel()
        self.loadProfilePicture()

        self.name_label = QLabel(f"Name: {name}", alignment=Qt.AlignmentFlag.AlignHCenter)
        self.email_label = QLabel(f"Email: {email}", alignment=Qt.AlignmentFlag.AlignHCenter)
        self.phone_label = QLabel(f"Phone: {phone}", alignment=Qt.AlignmentFlag.AlignHCenter)
        self.org_label = QLabel(f"Organization: {org}", alignment=Qt.AlignmentFlag.AlignHCenter)
        self.address_label = QLabel(f"Mailing Address: {address}", alignment=Qt.AlignmentFlag.AlignHCenter)

        # Button that allows user to edit, delete, or add notes to the partners info
        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.editPartner)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.deletePartner)
        self.notes_button = QPushButton("Notes")
        self.notes_button.clicked.connect(self.editNotes)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.name_label)
        top_layout.addWidget(self.email_label)

        middle_layout = QHBoxLayout()
        middle_layout.addWidget(self.phone_label)
        middle_layout.addWidget(self.org_label)

        bottom_layout = QHBoxLayout()
        bottom_layout.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        bottom_layout.addWidget(self.address_label)
        bottom_layout.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.notes_button)

        self.main_layout.addLayout(top_layout)
        self.main_layout.addLayout(middle_layout)
        self.main_layout.addLayout(bottom_layout)

        self.top_layout.addLayout(self.main_layout)
        self.top_layout.addLayout(button_layout)

        self.setLayout(self.top_layout)

        # Set the frame style to have a box around the widget
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)

    # Checks if text is in the person's name
    def matchSearchText(self, text, text_to_match):
        return text.lower().find(text_to_match.lower()) != -1

    def editPartner(self):
        dialog_window = EditPartnersWindow(self.id, self.main_window)
        dialog_window.exec()

    def deletePartner(self):
        cur.execute("DELETE FROM partners WHERE id = ?", (self.id,))
        con.commit()
        self.main_window.loadPartners()

    def editNotes(self):
        dialog_window = EditPartnerNotesWindow(self.id, self.name)
        dialog_window.exec()

    def loadProfilePicture(self):
        # Get the profile picture from the database
        profile_picture_data = cur.execute("SELECT profile_picture FROM partners WHERE id = ?",
                                           (self.id,)).fetchone()

        # Pixmap the profile picture to the label (if a profile pic exists)
        if profile_picture_data and profile_picture_data[0]:
            pixmap = QPixmap()
            pixmap.loadFromData(profile_picture_data[0])

            self.profile_picture_label.setPixmap(pixmap)
            self.profile_picture_label.setFixedSize(100, 100)
            self.profile_picture_label.setScaledContents(True)

            self.top_layout.addWidget(self.profile_picture_label)
