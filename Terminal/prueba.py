import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = QMainWindow()

    # Create text entry box
    text_edit_widget = QPlainTextEdit()

    # Change font, colour of text entry box
    text_edit_widget.setStyleSheet(
        """QPlainTextEdit {background-color: #333;
                           color: #00FF00;
                           font-family: Courier;}""")

    # "Central Widget" expands to fill all available space
    main_window.setCentralWidget(text_edit_widget)

    # Print text to console whenever it changes
    text_edit_widget.textChanged.connect(
        lambda: print(text_edit_widget.document().toPlainText()))

    # Set initial value of text
    text_edit_widget.document().setPlainText("Type text in here")

    main_window.show()

    # Start event loop
    sys.exit(app.exec_())