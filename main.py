import sys
from PyQt6.QtWidgets import QApplication
from app import init_app, CONFIG
import logging


def main():
    logging.info("Program started")
    app = QApplication(sys.argv)
    window = init_app()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
