import untitled_ui
import sys
import os
import json
import math
import tkinter.messagebox as msgbox
from PySide6 import QtWidgets as QTW

class mainUI(QTW.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = untitled_ui.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.horizontalSlider.valueChanged.connect(self.updateSliderValue)
        self.ui.horizontalSlider_2.valueChanged.connect(self.updateSliderValue)
        self.ui.horizontalSlider_3.valueChanged.connect(self.updateSliderValue)

        self.ui.pushButton.clicked.connect(self.calculateThis)
        self.ui.pushButton_2.clicked.connect(self.saveConfigAssistant)

        self.ui.lineEdit.textChanged.connect(self.setMoneyValueViewer)

        self.readConfig()

    def readableAmount(self,moneh):
        value = math.floor(moneh)
        formatted = f"{value:,}".replace(",", ".")
        return formatted
    
    def setMoneyValueViewer(self):
        moneyValue = int(self.ui.lineEdit.text())
        self.ui.lineEdit_2.setText(f"Money Amount = Rp.{self.readableAmount(moneyValue)}")
    
    def saveConfig(self, data):
        with open('config.json', 'w') as file:
                json.dump(data, file)

    def saveConfigAssistant(self):
        if self.ui.horizontalSlider.value() + self.ui.horizontalSlider_2.value() + self.ui.horizontalSlider_3.value() > 100 :
            msgbox.showerror(title="Error !", message= "TOTAL Percentage Must be <= 100%")
        else:
            msgbox.showinfo(title="Success !", message= "Config Successfully updated")
            self.saveConfig([self.ui.horizontalSlider.value(), self.ui.horizontalSlider_2.value(), self.ui.horizontalSlider_3.value()])
    
    def readConfig(self):
        if os.path.exists("config.json"):
            with open("config.json", "r") as file:
                try:
                    configData = json.load(file)
                    self.config = configData if isinstance(configData, list) else list(map(int, configData.split(",")))
                except:
                    msgbox.showerror(title = "Config CORRUPT!", message="Your Config has been corrupted! \nRestart The APP NOW")
                    self.saveConfig([45, 35, 20])
                    self.readConfig()
                    exit()
                self.setVariableSlider()
        else : 
            self.saveConfig([45, 35, 20])
            self.readConfig()
        
    def setVariableSlider(self):
        self.ui.horizontalSlider.setValue(self.config[0])
        self.ui.horizontalSlider_2.setValue(self.config[1])
        self.ui.horizontalSlider_3.setValue(self.config[2])
        
    def updateSliderValue(self):
        self.percentageTotal = self.ui.horizontalSlider_3.value() + self.ui.horizontalSlider_2.value() + self.ui.horizontalSlider.value()
        self.ui.textEdit.setText(f" Emergency Funds  : {self.ui.horizontalSlider.value()}% \n Daily Needs            : {self.ui.horizontalSlider_2.value()}% \n Stocks                     : {self.ui.horizontalSlider_3.value()}% \n TOTAL                     : {self.percentageTotal}% ")

    def calculateThis(self):
        self.moneyAmount = float(self.ui.lineEdit.text())
        self.moneyTotal = float(self.ui.horizontalSlider.value()/100 * self.moneyAmount) + float(self.ui.horizontalSlider_2.value()/100 * self.moneyAmount) + float(self.ui.horizontalSlider_3.value()/100 * self.moneyAmount)
        self.ui.textEdit_2.setText(f" Emergency Funds  : Rp.{self.readableAmount(float(self.ui.horizontalSlider.value()/100 * self.moneyAmount))} \n Daily Needs            : Rp.{self.readableAmount(float(self.ui.horizontalSlider_2.value()/100 * self.moneyAmount))} \n Stocks                     : Rp.{self.readableAmount(float(self.ui.horizontalSlider_3.value()/100 * self.moneyAmount))} \n TOTAL                     : Rp.{self.readableAmount(self.moneyTotal)} ")


if __name__ == "__main__":
    app = QTW.QApplication(sys.argv)
    window = mainUI()
    window.show()
    sys.exit(app.exec())
