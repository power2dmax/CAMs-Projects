# car_maintenance_log_2
"""
1-27-22
Program written in Python is used to track vehicle maintenance.
This program uses PyQt5 for the UI and SQLite for the data.
The user can enter the date, millage, and the maintenance performed.
The user will also have the capability to delete a row

2-14-22
New and improved version of the original car maintenance log.
Enhancements includes the ability to not only track maintenance
but to also track gas. Additional updates includes the ability
to change the color scheme through themes in the tool menu and
a car payment calculator
"""

import sys, os, csv
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtSql as qts
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class App(qtw.QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.initializeUI()

    def initializeUI(self):
        
        self.setWindowTitle('Car Log')
        self.resize(500, 650)
        
        self.styleSheet()
        self.createActions()
        self.menuWidget()
        self.toolbarWidget()
        self.mainWindow = MainWindow(self)
        self.setCentralWidget(self.mainWindow)
        
        self.show()
        
    def createActions(self):
        # Create the actions for the "Files Menu"
        self.add_row = qtw.QAction('Add Row', self)
        self.add_row.setShortcut('Ctrl+A')
        
        self.exit_action = qtw.QAction('Exit',
                triggered=lambda: self.statusBar().showMessage('Gonna Quit'))
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.setIcon(qtg.QIcon("icons/exit.png"))
        self.exit_action.triggered.connect(self.exitMessage)
        
        theme_icon = qtg.QIcon("icons/monitor.png")
        self.defaultTheme = qtw.QAction(theme_icon, 'Default',
                triggered=lambda: self.statusBar().showMessage('Default Theme'))
        self.defaultTheme.triggered.connect(self.defaultStyleSheet)
        self.blueTheme = qtw.QAction(theme_icon, 'Blue',
                triggered=lambda: self.statusBar().showMessage('Blue Theme'))
        self.blueTheme.triggered.connect(self.blueStyleSheet)
        self.chromeTheme = qtw.QAction(theme_icon,'Chrome',
                triggered=lambda: self.statusBar().showMessage('Chrome Theme'))
        self.chromeTheme.triggered.connect(self.chromeStyleSheet)
        self.meshTheme = qtw.QAction(theme_icon,'Mesh',
                triggered=lambda: self.statusBar().showMessage('Mesh Theme'))
        self.meshTheme.triggered.connect(self.meshStyleSheet)
        self.digitalBlueTheme = qtw.QAction(theme_icon, 'Digital Blue', 
                triggered=lambda: self.statusBar().showMessage('Digital Blue Theme'))
        self.digitalBlueTheme.triggered.connect(self.digitalBlueStyleSheet)
        self.southWestTheme = qtw.QAction(theme_icon, 'South West',
                triggered=lambda: self.statusBar().showMessage('South West Theme'))
        self.southWestTheme.triggered.connect(self.southWestStyleSheet)
        self.crazyTheme = qtw.QAction(theme_icon, 'Crazy',
                triggered=lambda: self.statusBar().showMessage('Crazy Theme'))
        self.crazyTheme.triggered.connect(self.crazyStyleSheet)
        
        #self.payCalc = PaymentCalculator(self)
        self.payment_calc = qtw.QAction('Payment Calculator',
                triggered=lambda: self.statusBar().showMessage('Car Payment Calculator'))
        self.payment_calc.setIcon(qtg.QIcon("icons/calc.png"))
        self.payment_calc.triggered.connect(self.payCalc)
        
        # Create actions for the "Help Menu" menu
        self.about_action = qtw.QAction('About',
                triggered=lambda: self.statusBar().showMessage('About'))
        self.about_action.setIcon(qtg.QIcon("icons/about.png"))
        self.about_action.triggered.connect(self.aboutInfo)
        
    def menuWidget(self):
        # Create the status bar
        self.statusbar = self.statusBar()
        self.statusBar().showMessage('Welcome to your Car Log')
        
        # Create the menubar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        
       # Create the "File" menu and add the buttons/actions
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(self.exit_action)
        
        toolsMenu = menu_bar.addMenu('Tools')
        toolsMenu.addAction(self.payment_calc)
        themesMenu = toolsMenu.addMenu(qtg.QIcon("icons/theme.png"), 'Themes')
        themesMenu.addAction(self.defaultTheme)
        themesMenu.addAction(self.blueTheme)
        themesMenu.addAction(self.chromeTheme)
        themesMenu.addAction(self.meshTheme)
        themesMenu.addAction(self.digitalBlueTheme)
        themesMenu.addAction(self.southWestTheme)
        themesMenu.addAction(self.crazyTheme)
        
        help_menu = menu_bar.addMenu('Help')
        help_menu.addAction(self.about_action)
        
    def toolbarWidget(self):
        toolbar = qtw.QToolBar()
        self.addToolBar(qtc.Qt.BottomToolBarArea, toolbar)
        toolbar.addAction(self.exit_action)
        
    def exitMessage(self):
        message = qtw.QMessageBox.question(self, 'Exit',
            'This will save upon exit. \n Are you sure you want exit?',
            qtw.QMessageBox.Yes | qtw.QMessageBox.No)
        if message == qtw.QMessageBox.Yes:
            #self.database.close()
            self.close()
            
    def payCalc(self):
        calc = PaymentCalculator(self)
        calc.resize(200, 160)
        calc.show()
            
    def aboutInfo(self):
        text = "CAM's car log, written in Python\n" \
        "using PyQt5 modules for the GUI\n\n" \
        "The car log allows users to track their\n" \
        "maintence and fuel. Users are also able to \n" \
        "change the color scheme through themes in\n" \
        "the Tool Menu based on their prefrences\n\n" \
        "             Written by CAM: 2022"
        qtw.QMessageBox.about(self, "CAM's Car Log", text)
            
    def defaultStyleSheet(self):
        stylesheet = """
        QMainWindow {
            background-color: whitesmoke
        }
        QTableView {
            background-color: white
        }
        """
        self.setStyleSheet(stylesheet)
        
    def blueStyleSheet(self):
        stylesheet = """
        QMainWindow, QMessageBox {
            background-color: lightsteelblue
        }
        QPushButton {
            font-size: 10pt
            background-color: azure
        }
        QLabel {
            color: white
        }
        QTableView {
            background-color: aliceblue
        }
        QMenuBar, QTabWidget {
            background-color: powderblue
        }
        .QWidget {
           background: url(files/tile.png)
        }
        """
        self.setStyleSheet(stylesheet)
        
    def chromeStyleSheet(self):
        stylesheet = """
        QMainWindow {
            background: url(files/chrome.png)
        }
        QLabel {
            color: silver
        }
        QMessageBox {
            background: url(files/chrome.png)
        }
        """
        self.setStyleSheet(stylesheet)
        
    def meshStyleSheet(self):
        stylesheet = """
        QMainWindow, QMessageBox {
            background: url(files/mesh.png)
        }
        QTableView {
            background: lightgray
        }
        QLabel {
            color: white;
            font: bold 12px
        }
        QStatusBar {
            color: white;
            font: bold 12px
        }
        """
        self.setStyleSheet(stylesheet)
    
    def digitalBlueStyleSheet(self):
        stylesheet = """
        QMainWindow {
            background: url(files/blue_mesh.png)
        }
        QLabel {
            color: white;
            font: bold
        }
        QTableView, QMessageBox, QComboBox, QPushButton  {
            background: url(files/light_blue_steel.png)
        }
        QPushButton:hover {
            background: lightblue
        }     
        QTableView {
            selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0.75, y2: 0.75,
            stop: 0 #2E97AC, stop: 1 #C6E4E7)
        }
        QMenuBar {
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 lightgray, stop:1 darkgray);
            spacing: 3px; /* spacing between menu bar items */
        }
        QMenuBar::item {
            padding: 1px 4px;
            background: transparent;
            border-radius: 4px;
        }
        QMenuBar::item:selected { /* when selected using mouse or keyboard */
            background: #a8a8a8;
        }
        QMenuBar::item:pressed {
            background: #888888;
        }
        
        QTabWidget::pane { /* The tab widget frame */
            border-top: 2px solid #C2C7CB;
        }
        QTabWidget::tab-bar {
            left: 5px; /* move to the right by 5px */
        }
        QTabBar::tab {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
            stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
            border: 2px solid #C4C4C3;
            border-bottom-color: #C2C7CB; /* same as the pane color */
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            min-width: 8ex;
            padding: 2px;
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 #fafafa, stop: 0.4 #f4f4f4,
            stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
        }
        QTabBar::tab:selected {
            border-color: #9B9B9B;
            border-bottom-color: #C2C7CB; /* same as pane color */
        }
        QTabBar::tab:!selected {
            margin-top: 2px; /* make non-selected tabs look smaller */
        }
        QDialog {
            background: url(files/blue_mesh.png)
        }
        QDialog QLabel {
            color: white;
            font: bold 10px
        }
        QStatusBar {
            color: white;
            font: bold 12px
        }
        """
        self.setStyleSheet(stylesheet)
    
    def southWestStyleSheet(self):
        stylesheet = """
        QMainWindow {
            background: url(files/south_west.png)
        }
        QTableView {
            background: url(files/south_rug.png);
            color: white;
            font: bold 14px
        }
        QLabel {
            color: white;
            font: bold 12px
        }
        QStatusBar {
            color: white;
            font: bold 12px
        }
        """
        self.setStyleSheet(stylesheet)
    
    
    def crazyStyleSheet(self):
        stylesheet = """
        QMainWindow { 
            background-color: lightgreen
        }
        QPushButton {
            font-size: 10pt
        }
        QTableView {
            background-color: plum
        }
        QLabel, QPushButton {
            background-color: yellow
        }
        """
        self.setStyleSheet(stylesheet)
    
    
class PaymentCalculator(qtw.QDialog):
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.setWindowTitle('Payment Calculator')
        self.setLayout(qtw.QGridLayout())
        self.topLabel = qtw.QLabel("<h3>Payment Calculator<h3>")
        self.carPriceText = qtw.QLabel("Purchase Price:")
        self.carPrice = qtw.QLineEdit()
        self.carPrice.setValidator(qtg.QIntValidator(0, 100000, self))
        self.interestRateText = qtw.QLabel("Interest Rate:")
        self.interestRate = qtw.QLineEdit()
        self.interestRate.setValidator(qtg.QIntValidator(0, 10, self))
        self.termLengthText = qtw.QLabel("Number of Years:")
        self.termLength = qtw.QLineEdit()
        self.termLength.setValidator(qtg.QIntValidator(1, 10, self))
        
        
        self.payment = qtw.QLabel('Still figuring it out')
        monthlyPayment = str(10)
        self.calculationButton = qtw.QPushButton('Calculate Payment')
        #self.calculationButton.clicked.connect(self.calculatePayment(monthlyPayment))
        print(monthlyPayment)
        
        self.exitButton = qtw.QPushButton('Exit')
        self.exitButton.clicked.connect(self.close)
        
        self.layout().addWidget(self.topLabel, 0, 0)
        self.layout().addWidget(self.carPriceText, 1, 0)
        self.layout().addWidget(self.carPrice, 1, 1)
        self.layout().addWidget(self.interestRateText, 2, 0)
        self.layout().addWidget(self.interestRate, 2, 1)
        self.layout().addWidget(self.termLengthText, 3, 0)
        self.layout().addWidget(self.termLength, 3, 1)
        
        self.layout().addWidget(self.calculationButton, 4, 0)
        self.layout().addWidget(self.payment, 4, 1)
        
        self.layout().addWidget(self.exitButton, 99, 1)
        
        
    def calculatePayment(self, monthlyPayment):
        """price = self.carPrice
        monthlyInterest = self.interestRate / 12
        months = self.termLength*12
        self.monthlyPayment = int((self.price*((monthlyRate)*(1+monthlyRate)**months))/(((1+monthlyRate)**(months)-1)))
        print(self.monthlyPayment)"""
        monthlyPayment = '0'
        return monthlyPayment
    
class MainWindow(qtw.QWidget):
    
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        layout = qtw.QVBoxLayout(self)
        
        # Initialize tab screen
        tabs = qtw.QTabWidget()
        tab1 = Maintenance(self)
        tab2 = Gas(self)
        tab3 = CarInformation(self)
        tabs.resize(300,200)
        
        # Add tabs
        
        tabs.addTab(tab1,"Maintenance")
        tabs.addTab(tab2,"Gas")
        tabs.addTab(tab3,"Information")
        
        # Add tabs to widget
        layout.addWidget(tabs)
        self.setLayout(layout)
        
        
class CarInformation(qtw.QWidget):
    
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        
        layout = qtw.QVBoxLayout(self)

        
class Maintenance(qtw.QWidget):
    
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        
        # Create first tab
        self.createConnection()
        self.createTable()
        
        layout = qtw.QVBoxLayout(self)
        top_layout = qtw.QHBoxLayout(self)
        bottom_layout = qtw.QHBoxLayout(self)
        
        add_row = qtw.QPushButton("Add Row")
        add_row.setIcon(qtg.QIcon("icons/add_row.png"))
        add_row.setStyleSheet("padding: 6px")
        add_row.clicked.connect(self.addRow)
        
        del_row = qtw.QPushButton("Delete Row")
        del_row.setIcon(qtg.QIcon("icons/del_row.png"))
        del_row.setStyleSheet("padding: 6px")
        del_row.clicked.connect(self.deleteRow)
        
        sorting_options = ["Sort by Date", "Sort by Mileage", "Sort by Cost", "Sort by Description"] # Set up sorting combo box
        sort_name_cb = qtw.QComboBox()
        sort_name_cb.addItems(sorting_options)
        sort_name_cb.currentTextChanged.connect(self.setSortingOrder)
        
        sorting_text = qtw.QLabel("Sorting Options: ")
        
        top_layout.addWidget(add_row)
        top_layout.addWidget(del_row)
        top_layout.addStretch()
        top_layout.addWidget(sorting_text)
        top_layout.addWidget(sort_name_cb)
        top_layout.addStretch()
        #self.setLayout(top_layout)
        
        # Setting up the user actions for the car log tracker 
        title = qtw.QLabel("Maintenance Log")
        title.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)
        title.setStyleSheet("font: bold 24px")
        
        # Create table view and set model
        self.table_view = qtw.QTableView()
        header = self.table_view.horizontalHeader()
        self.table_view.setModel(self.model)
        header.setStretchLastSection(True)
        self.table_view.setSelectionMode(qtw.QTableView.SingleSelection)
        self.table_view.setSelectionBehavior(qtw.QTableView.SelectRows)
        
        # Calculate the total cost of the maintenance performed by adding the results in the costs column
        result = 0
        query = QSqlQuery("SELECT Cost FROM maintenance")
        while query.next():
            result = result + query.value(0)
        totalCost =str("%.2f" % (result))
        totalCostText_1 = qtw.QLabel('The Total Maintenance Cost is: $')
        totalCostText_1.setFont(qtg.QFont('Arial', 9))
        totalCostText_2 = qtw.QLabel(totalCost)
        totalCostText_2.setFont(qtg.QFont('Arial', 9))
        bottom_layout.addWidget(totalCostText_1)
        bottom_layout.addWidget(totalCostText_2)
        bottom_layout.addStretch()
                
        # Set the overall layouit
        layout.addLayout(top_layout)
        layout.addWidget(title, qtc.Qt.AlignLeft)
        layout.addWidget(self.table_view)
        layout.addLayout(bottom_layout)
        
    def createConnection(self):
        self.database = qts.QSqlDatabase.addDatabase("QSQLITE") # SQLite version 3
        self.database.setDatabaseName("files/car_log.db")

        if not self.database.open():
            print("Unable to open data source file.")
            sys.exit(1) # Error code 1 - signifies error

        # Check if the tables we need exist in the database
        tables_needed = {'maintenance'}
        tables_not_found = tables_needed - set(self.database.tables())
        if tables_not_found:
            qtw.QMessageBox.critical(None, 'Error', f'The following tables are missing from the database: {tables_not_found}')
            sys.exit(1) # Error code 1 - signifies error

    def createTable(self):
        """
        Set up the model, headers and populate the model.
        """
        self.model = qts.QSqlRelationalTableModel()
        self.model.setTable('maintenance')
        self.model.setHeaderData(self.model.fieldIndex('id'), qtc.Qt.Horizontal, "ID")
        self.model.setHeaderData(self.model.fieldIndex('Date'), qtc.Qt.Horizontal, "Date")
        self.model.setHeaderData(self.model.fieldIndex('Mileage'), qtc.Qt.Horizontal, "Mileage")
        self.model.setHeaderData(self.model.fieldIndex('Cost'), qtc.Qt.Horizontal, "Cost")
        self.model.setHeaderData(self.model.fieldIndex('Description'), qtc.Qt.Horizontal, "Description")
        
        # Populate the model with data
        self.model.select()
        
    def addRow(self):
        """
        Add a new record to the last row of the table
        """
        last_row = self.model.rowCount()
        self.model.insertRow(last_row)

        id = 0
        query = qts.QSqlQuery()
        query.exec_("SELECT MAX (id) FROM maintenance")
        if query.next():
            id = int(query.value(0))
            
    def deleteRow(self):
        """
        Delete an entire row from the table
        """
        current_item = self.table_view.selectedIndexes()
        for index in current_item:
            self.model.removeRow(index.row())
        self.model.select()
    
    def setSortingOrder(self, text):
        """
        Sort the rows in table
        """
        if text == "Sort by Date":
            self.model.setSort(self.model.fieldIndex('Date'), qtc.Qt.AscendingOrder)
        elif text == "Sort by Mileage":
            self.model.setSort(self.model.fieldIndex('Mileage'), qtc.Qt.AscendingOrder)
        elif text == "Sort by Cost":
            self.model.setSort(self.model.fieldIndex('Cost'), qtc.Qt.AscendingOrder)
        elif text == "Sort by Description":
            self.model.setSort(self.model.fieldIndex('Description'), qtc.Qt.AscendingOrder)
        
        self.model.select()


class Gas(qtw.QWidget):
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        
        # Create first tab
        self.createConnection()
        self.createTable()
        
        layout = qtw.QVBoxLayout(self)
        top_layout = qtw.QHBoxLayout(self)
        bottom_layout = qtw.QHBoxLayout(self)
        
        add_row = qtw.QPushButton("Add Row")
        add_row.setIcon(qtg.QIcon("icons/add_row.png"))
        add_row.setStyleSheet("padding: 6px")
        add_row.clicked.connect(self.addRow)
        
        del_row = qtw.QPushButton("Delete Row")
        del_row.setIcon(qtg.QIcon("icons/del_row.png"))
        del_row.setStyleSheet("padding: 6px")
        del_row.clicked.connect(self.deleteRow)
        
        # Setting up the user actions for the car log tracker 
        title = qtw.QLabel("Gas Log")
        title.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)
        title.setStyleSheet("font: bold 24px")
        
        # Calculate the MPG and display on the bottom of the table
        result = 0
        gasQuery = QSqlQuery("SELECT Gallons FROM gas")
        while gasQuery.next():
            gasUsed = int(gasQuery.value(0))
        mileQuery = QSqlQuery("SELECT Odometer_Reading FROM gas")
        while mileQuery.next():
            mileUsed = int(mileQuery.value(0))
        mpg = ("%.2f" % (mileUsed/gasUsed))
        
        avgMpgText = qtw.QLabel("Your Latest Fuel Economy is:")
        avgMpgText.setFont(qtg.QFont('Arial', 9))
        avgMpgCalc = qtw.QLabel(mpg)
        avgMpgCalc.setFont(qtg.QFont('Arial', 9))
        mpgText = qtw.QLabel("MPG")
        mpgText.setFont(qtg.QFont('Arial', 9))
        
        # Setting up the 
        top_layout.addWidget(add_row)
        top_layout.addWidget(del_row)
        top_layout.addStretch()
        top_layout.addStretch()
        
        bottom_layout.addWidget(avgMpgText)
        bottom_layout.addWidget(avgMpgCalc)
        bottom_layout.addWidget(mpgText)
        bottom_layout.addStretch()
                
        # Create table view and set model
        self.table_view = qtw.QTableView()
        self.header = self.table_view.horizontalHeader()
        self.table_view.setModel(self.model)
        self.header.setStretchLastSection(True)
        self.table_view.setSelectionMode(qtw.QTableView.SingleSelection)
        self.table_view.setSelectionBehavior(qtw.QTableView.SelectRows)
        
        layout.addLayout(top_layout)
        layout.addWidget(title, qtc.Qt.AlignLeft)
        layout.addWidget(self.table_view)
        layout.addLayout(bottom_layout)        
        
    def createTable(self):
        """
        Set up the model, headers and populate the model.
        """
        self.model = qts.QSqlRelationalTableModel()
        self.model.setTable('gas')
        self.model.setHeaderData(self.model.fieldIndex('id'), qtc.Qt.Horizontal, "ID")
        self.model.setHeaderData(self.model.fieldIndex('Date'), qtc.Qt.Horizontal, "Date")
        self.model.setHeaderData(self.model.fieldIndex('Gallons'), qtc.Qt.Horizontal, "Gallons")
        self.model.setHeaderData(self.model.fieldIndex('Cost'), qtc.Qt.Horizontal, "Cost")
        self.model.setHeaderData(self.model.fieldIndex('Odometer_Reading'), qtc.Qt.Horizontal, "Odometer Reading")
                
        # Populate the model with data
        self.model.select()
        
    def createConnection(self):
        self.database = qts.QSqlDatabase.addDatabase("QSQLITE") # SQLite version 3
        self.database.setDatabaseName("files/car_log.db")

        if not self.database.open():
            print("Unable to open data source file.")
            sys.exit(1) # Error code 1 - signifies error

        # Check if the tables we need exist in the database
        tables_needed = {'gas'}
        tables_not_found = tables_needed - set(self.database.tables())
        if tables_not_found:
            qtw.QMessageBox.critical(None, 'Error', f'The following tables are missing from the database: {tables_not_found}')
            sys.exit(1) # Error code 1 - signifies error
        
    def addRow(self):
        """
        Add a new record to the last row of the table
        """
        last_row = self.model.rowCount()
        self.model.insertRow(last_row)

        id = 0
        query = qts.QSqlQuery()
        query.exec_("SELECT MAX (id) FROM gas")
        if query.next():
            id = int(query.value(0))
            
    def deleteRow(self):
        """
        Delete an entire row from the table
        """
        current_item = self.table_view.selectedIndexes()
        for index in current_item:
            self.model.removeRow(index.row())
        self.model.select()

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    windows_style = qtw.QStyleFactory.create('Windows')
    app.setStyle(windows_style)
    window = App()
    sys.exit(app.exec_())