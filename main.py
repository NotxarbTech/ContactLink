from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QVBoxLayout, QScrollArea,
    QLineEdit, QSpacerItem, QSizePolicy,
    QHBoxLayout, QPushButton
)
import sqlite3

from custom_widgets import PartnerContactWidget
from custom_windows import AddPartnersWindow

# Connection and cursor to access and modify and read from the database
con = sqlite3.connect("database.db")
cur = con.cursor()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("ContactLink (FBLA 2024) - by Braxton Hudgins")
        self.main_layout = QVBoxLayout()
        self.central_widget = QWidget()

        # List that contains Partner Contact Widgets
        self.partner_list = []
        self.partner_layout = QVBoxLayout()
        self.loadPartners()

        # Header widget containing the application title
        self.title_widget = QLabel("ContactLink")
        title_widget_font = self.title_widget.font()
        title_widget_font.setPointSize(30)
        self.title_widget.setFont(title_widget_font)
        self.title_widget.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Section that allows user to add and search through school partners
        self.tool_bar_layout = QHBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search Contacts")
        self.search_bar.textChanged.connect(self.searchContacts)

        self.add_partners_button = QPushButton("Add New Partners")

        self.tool_bar_layout.addWidget(self.search_bar)
        self.tool_bar_layout.addWidget(self.add_partners_button)

        # Handle "Add New Partners" button click
        self.add_partners_button.clicked.connect(self.addNewPartners)

        # Scroll area that displays partner information
        self.scroll_area = QScrollArea()
        self.scroll_container = QWidget()

        self.scroll_container.setLayout(self.partner_layout)
        self.scroll_area.setWidget(self.scroll_container)

        # Scroll area properties
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)

        self.main_layout.addWidget(self.title_widget)
        self.main_layout.addLayout(self.tool_bar_layout)
        self.main_layout.addWidget(self.scroll_area)

        self.setGeometry(600, 100, 800, 600)
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    def loadPartners(self):
        # Clear the partner list
        self.partner_list = []

        # Fetch the partners from the database and loop through, creating a Partner Contact Widget for each row
        cur.execute("SELECT * FROM partners;")
        for partner in cur:
            self.partner_list.append(PartnerContactWidget(partner[1], partner[2],
                                                          partner[3], partner[4]))

        # Clear the partner layout
        for i in reversed(range(self.partner_layout.count())):
            widget = self.partner_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Iterate over the partner contact widgets in the partner list and add them to the scroll area
        for partner in self.partner_list:
            self.partner_layout.insertWidget(0, partner)

        spacer = QSpacerItem(1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.partner_layout.addItem(spacer)

    def addNewPartners(self):
        dialog_window = AddPartnersWindow()
        dialog_window.exec()
        self.loadPartners()

    def searchContacts(self, text):
        visible_widgets = []
        for widget in self.partner_list:
            if widget.matchSearchText(text):
                widget.setVisible(True)
                visible_widgets.append(widget)
            else:
                widget.setVisible(False)

        # Removes all visible widgets and reinserts them at the top
        for widget in reversed(visible_widgets):
            self.partner_layout.removeWidget(widget)
            self.partner_layout.insertWidget(0, widget)


# Create application and main window
app = QApplication([])
window = MainWindow()
window.show()

# Run the application
app.exec()

# Close the database objects
cur.close()
con.close()