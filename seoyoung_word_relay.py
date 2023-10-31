from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import random
import sys
from PyQt5.QtWidgets import *

chrome_option = Options()
chrome_option.add_experimental_option("detach", True)
chrome_option.add_argument("headless")

browser = webdriver.Chrome(options=chrome_option)
browser.get("https://stdict.korean.go.kr/main/main.do")

word_list = []
word = ''        

def click_find():
    clickfind = browser.find_element(By.CLASS_NAME, 'paging')
    click_list = clickfind.find_elements(By.TAG_NAME, 'a')
    i = len(click_list)
    if i != 0:
        i = random.randint(0, len(click_list) - 1)
        if i == 11:
            click_list[i].click()
            click_list = browser.find_element(By.CLASS_NAME, 'paging').find_elements(By.TAG_NAME, 'a')
            i = random.randint(0, len(click_list) - 1)
        click_list[i].click()

def search_word(search):
    num = 0
    for check in search:             
        if check.text[1] == '-':
            check = check.text[0] + check.text[2]
        elif len(check.text) == 3 or len(search[num].text) == 4:
            check = check.text[0] + check.text[1]
            
        for word in word_list:
            if check == word:
                num += 1
    return num

def word_relay(word):    
    find_word = browser.find_element(By.CLASS_NAME, 'tit').text
    for text in find_word:
        if text == '총':
            if find_word[find_word.index(text)+2] == '0':
                return "존재하지 않는 단어입니다. 당신의 패배!"
    
    next_word = word[1] + '?'
    search = browser.find_element(By.ID, 'n_input')
    search.send_keys(next_word)
    search.send_keys("\n")
        
    find_word = browser.find_element(By.CLASS_NAME, 'tit').text
    for text in find_word:
        if text == '총':
            if find_word[find_word.index(text)+2] == '0':
                return f"{word[1]}(으)로 시작하는 단어가 없습니다. 당신의 승리!"
            
    click_find()
    
    search = browser.find_elements(By.CLASS_NAME, 't_blue1')
    num = search_word(search)
    
    while num <= 10:
        if num == 10:
            click_find()
            search = browser.find_elements(By.CLASS_NAME, 't_blue1')
            num = search_word(search)
        else:
            break
        
    r = random.randint(0, len(search)-1)
                        
    if search[r].text[1] == '-':
        search[r] = search[r].text[0] + search[r].text[2]
    elif len(search[r].text) == 3 or len(search[r].text) == 4:
        search[r] = search[r].text[0] + search[r].text[1]
    else:
        search[r] = search[r].text

    word_list.append(search[r])
    return search[r]

class TestGUI(QWidget):
    x = 0
    y = 0
    turn = 0
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("한글 두 글자 끝말잇기 게임")
        self.resize(150, 100)
        
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        
        self.grid.addWidget(QLabel('한글 두 글자 끝말잇기 게임을 시작하겠습니다.\n다섯 번의 입력까지 승부가 결정되지 않는다면 게임은 종료됩니다.'), self.x, self.y)

        self.input_word = QLineEdit(self)
        self.grid.addWidget(QLabel('단어 입력: '), self.x+1, self.y)
        self.grid.addWidget(self.input_word, self.x+1, self.y+1)
        
        btn = QPushButton("입력", self)
        self.grid.addWidget(btn, self.x+1, self.y+2)
        btn.clicked.connect(self.btn_clicked)
    
        self.show()
        
    def btn_clicked(self):
        self.turn += 1
        self.x += 3

        if self.x == 3:
            word = self.input_word.text()
            word_list.append(word)
            search = browser.find_element(By.ID, 'searchKeyword')
            search.send_keys(word)
            search.send_keys("\n")
        else:
            word = self.input_word.text()
            if word_list[len(word_list)-1][1] != word[0]:
                self.grid.addWidget(QLabel("전 단어의 끝말과 첫 단어가 일치하지 않습니다. 당신의 패배!"), self.x+1, self.y)
                self.grid.addWidget(QLabel('게임이 종료되었습니다.'), self.x+2, self.y)
                return
            for check in word_list:
                if word == check:
                    self.grid.addWidget(QLabel("이미 입력한 단어입니다. 당신의 패배!"), self.x+1, self.y)
                    self.grid.addWidget(QLabel('게임이 종료되었습니다.'), self.x+2, self.y)
                    return
            word_list.append(word)
            search = browser.find_element(By.ID, 'n_input')
            search.send_keys(word)
            search.send_keys("\n")

        self.grid.addWidget(QLabel(f"내가 입력한 단어: {word}"), self.x, self.y)
        
        c_word = word_relay(word)
        
        if len(c_word) > 2:
            self.grid.addWidget(QLabel(c_word), self.x+1, self.y)
            self.grid.addWidget(QLabel('게임이 종료되었습니다.'), self.x+2, self.y)
            return
        else:        
            self.grid.addWidget(QLabel(f"컴퓨터가 입력한 단어: {c_word}"), self.x+1, self.y)
            
            if self.turn == 5:
                self.grid.addWidget(QLabel('턴 수가 끝나 게임이 종료되었습니다.'), self.x+2, self.y)
                return
            
            self.input_word = QLineEdit(self)
            self.grid.addWidget(QLabel(f"{c_word[1]}(으)로 시작하는 단어 입력: "), self.x+2, self.y)
            self.grid.addWidget(self.input_word, self.x+2, self.y+1)
        
            btn = QPushButton("입력", self)
            self.grid.addWidget(btn, self.x+2, self.y+2)
            btn.clicked.connect(self.btn_clicked)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = TestGUI()
    sys.exit(app.exec_())
