import src.sql.test as api
import PyQt5.QtGui as QtGui

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

api.execute()
api.test("Hiszpania")


if __name__ == '__main__':
    import sys
    import src.app.modules.start as start
    app = QApplication(sys.argv)
    window = start.Start()
    sys.exit(app.exec_())
