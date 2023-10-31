from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys
import time
from PyQt5.QtWidgets import *

chrome_option = Options()
chrome_option.add_experimental_option("detach", True)
#chrome_option.add_argument("headless")

browser = webdriver.Chrome(options=chrome_option)
browser.get("https://www.16personalities.com/ko/")

radio_btn = []
i = 0

def click():
    try:
        browser.find_element(By.XPATH, '//*[@id="main-app"]/main/div[1]/div/a/span[1]').click()
    except:
        if browser.find_element(By.XPATH, '//*[@id="main-app"]/div[1]/div/form/div[2]/button/span[1]').text == "검사 결과":
            browser.find_element(By.XPATH, '//*[@id="main-app"]/div[1]/div/form/div[2]/button/span[1]').click()
            time.sleep(2)
            return browser.find_element(By.CLASS_NAME, 'results__type__code').text
        browser.find_element(By.XPATH, '//*[@id="main-app"]/div[1]/div/form/div[2]/button/span[1]').click()
    return
    
def question():
    time.sleep(0.5)
    question_list = browser.find_elements(By.CLASS_NAME, 'input__label')
    return question_list[i].text

def choose(num):
    group = browser.find_elements(By.CLASS_NAME, 'group__options')
    radio = group[i].find_elements(By.CLASS_NAME, 'sp-radio')
    radio[num].click()
        
class startGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("mbti 검사 프로그램")
        self.resize(150, 100)
        
        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        
        text = QLabel('mbti 검사를 시작하시겠습니까?')
        btn = QPushButton("네", self)
        
        self.hbox.addWidget(text)
        self.hbox.addWidget(btn)
        self.hbox.addStretch(1)
        
        self.vbox = QVBoxLayout()        
        self.vbox.addLayout(self.hbox)
        
        self.setLayout(self.vbox)
        
        self.text = QLabel(self)
        
        btn.clicked.connect(self.btn_clicked)
        
        self.show()
        
    def btn_clicked(self):
        click()
        
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.text)
        self.vbox.addStretch(1)
        
        radio_btn.append(QRadioButton('매우 동의', self))
        radio_btn.append(QRadioButton('약간 동의', self))
        radio_btn.append(QRadioButton('동의', self))
        radio_btn.append(QRadioButton('보통', self))
        radio_btn.append(QRadioButton('비동의', self))
        radio_btn.append(QRadioButton('약간 비동의', self))
        radio_btn.append(QRadioButton('매우 비동의', self))
        
        rbox = QHBoxLayout()
        
        for btn in radio_btn:
            rbox.addWidget(btn)

        self.vbox.addLayout(rbox)
        self.setLayout(self.vbox)
        
        radio_btn[0].clicked.connect(lambda: self.radio_click(0))
        radio_btn[1].clicked.connect(lambda: self.radio_click(1))
        radio_btn[2].clicked.connect(lambda: self.radio_click(2))
        radio_btn[3].clicked.connect(lambda: self.radio_click(3))
        radio_btn[4].clicked.connect(lambda: self.radio_click(4))
        radio_btn[5].clicked.connect(lambda: self.radio_click(5))
        radio_btn[6].clicked.connect(lambda: self.radio_click(6))   

        self.test_list()
        
    def test_list(self):
        question_str = question()

        self.text.setText(f"{question_str}")  

    def radio_click(self, num):
        result = ' '
        global i
        choose(num)
        i += 1
        if i == 6:
            i = 0
            result = click()
            if result != None:
                self.text.setText(f"당신의 mbti는 {result}입니다.")
                self.vbox.addStretch(1)
                self.vbox.addWidget(self.text)
                self.vbox.addStretch(1)
                return
        self.test_list()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = startGUI()
    sys.exit(app.exec_())