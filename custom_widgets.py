# custom_widgets.py

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QFrame, QHBoxLayout


class PartnerContactWidget(QFrame):
    def __init__(self, name, email, phone, org):
        super(PartnerContactWidget, self).__init__()

        self.name_label = QLabel(f"Name: {name}")
        self.email_label = QLabel(f"Email: {email}")
        self.phone_label = QLabel(f"Phone: {phone}")
        self.org_label = QLabel(f"Organization: {org}")

        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.name_label)
        top_layout.addWidget(self.email_label)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.phone_label)
        bottom_layout.addWidget(self.org_label)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

        # Set the frame style to have a box around the widget
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)

    # Checks if text is in the person's name
    def matchSearchText(self, text):
        text_to_match = self.name_label.text().lower()
        return text.lower() in text_to_match
