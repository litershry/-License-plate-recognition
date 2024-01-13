import sys
import model_qt

if __name__ == "__main__":
    app = model_qt.QtWidgets.QApplication(sys.argv)
    my = model_qt.picture()
    my.show()
    sys.exit(app.exec_())
