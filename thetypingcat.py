from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

def breaks(abc):
    list_line = []
    current = 0
    line = """<div class="line">"""
    for i in range(200):
        loc = abc.find(line,current)
        if loc == -1:
            break
        list_line.append(loc)
        current = loc + len(line)
    return list_line

def space(abc):
    list_space = []
    spacer = """<i class="spacer"> </i>"""
    current = 0
    while current <= len(abc):
        loc = abc.find(spacer,current)
        if loc != -1:
            list_space.append(loc)
            current = loc + len(spacer)
        else:
            break        
    return list_space

def create(abc):
    texts = ""
    for i in range(len(spaces)):
        try:
            text = abc[spaces[i]+23:spaces[i+1]]
            escp = text.find("⏎")
            if escp !=  -1:    #vetiyo vane
                next_word = abc[spaces[i]+escp+92:spaces[i+1]]
                text = text[0:escp] + "\n" + next_word
                
            texts += text + " "
        except:
            pass
    return texts

def end(abc):
    start = spaces[-1]+23
    end = abc.find("⏎",start)
    return abc[start:end]

def last_lines(abc):
    text = ""
    for i in range(len(line_breaks)):
        try:
            end = abc.find("⏎",line_breaks[i])
            if end == -1:
                break
            start = line_breaks[i]+18
            text += abc[start:end] + "\n"
        except:
            break
    return text

def first_word(abc):
    end = abc.find("\"",55)
    word = abc[55:end]
    return word+" "

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("detach",True)


login = int(input("Do you want to login?(0 for no)"))

if login:
    #Login Process
    email = input("Your email: ")
    password = input("Your password: ")
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get("https://thetypingcat.com/sign-in")
    time.sleep(5)
    uname = browser.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div/div/div/form/div[1]/div/div/input")
    pswd = browser.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div/div/div/form/div[2]/div/div/input")
    submit = browser.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div/div/div/form/div[4]/div/button")
    uname.send_keys(email)
    pswd.send_keys(password)
    time.sleep(2)
    submit.click()
    time.sleep(3)
    browser.get("https://thetypingcat.com/typing-speed-test/1m")
    time.sleep(5)
else:
    #Homepage
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get("https://thetypingcat.com/typing-speed-test/1m")
    time.sleep(5)


#Selecting the frame and getting its code
text = browser.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div/div[1]/div[2]")
abc = text.get_attribute("innerHTML")

#First word of the line
word = first_word(abc)
#Returns an array of where lines need to be break
line_breaks = breaks(abc)
#Returns an array with position of spaces
spaces = space(abc)
#Returns the last text displayed in the screen
end_text = end(abc)
#Returns the last text of the text
last = last_lines(abc)
#Creates the paragraph to be typed
word += create(abc) + end_text + "\n" + last
#Typing to the browser
lines = word.splitlines()
actions = ActionChains(browser)
time = 0
for i in lines:
    if time > 45:
        break
    words = i.split()
    for j in words:
        actions.send_keys(j)
        if j != words[-1]:
            actions.send_keys(Keys.SPACE)
        actions.pause(.25)
        time += .25
        if time > 59:
            break
    actions.send_keys(Keys.ENTER)
actions.perform()