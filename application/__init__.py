import sys

from PyQt5.QtWidgets import QApplication

from application import Application

app = QApplication(sys.argv)
application = Application()
application.show()
sys.exit(app.exec_())
