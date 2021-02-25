import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Marker():
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.url = 'https://ucstudent.uc.pt/login'
        self.options = webdriver.FirefoxOptions()
        self.options.headless = True
        try:
            self.driver = webdriver.Firefox(executable_path='./geckodriver_linux', options=self.options)
        except:
            self.driver = webdriver.Firefox(executable_path='./geckodriver', options=self.options)

    def login(self):
        #open url
        self.driver.get(self.url) 
        #email   
        email_input = self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div[2]/div/div/form/div[1]/div/input')    
        email_input.send_keys(self.username)
        #password
        pass_input = self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div[2]/div/div/form/div[2]/div/input')    
        pass_input.send_keys(self.password)
        #login
        login_button = self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div[2]/div/div/form/div[3]/button')    
        login_button.click()

    def isGreen(self,xpath):
        button = self.driver.find_element_by_xpath(xpath)
        color = button.value_of_css_property('background-color')
        if 'rgb' in color:
            rgb_color=color[4:-1].split(', ')
            green = int(rgb_color[1])
            if green>70:
                return True
            else:
                return False

    def hasButton(self, xpath):
        try:
            wait = WebDriverWait(self.driver,10)
            wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        except:
            print('❌ Button not found')
            return False
        else:
            return True

    def mark_attendance(self):
        buttonsXPath=list()
        buttonsXPath.append('//*[@id="app"]/div/div[1]/div/div/div/div/div[6]/div/div[8]/button[1]')
        buttonsXPath.append('//*[@id="app"]/div/div[1]/div/div/div/div/div/div[4]/div/div[3]/div/button[2]')
        buttonsXPath.append('/html/body/div[2]/div[2]/footer/button[2]')
        if self.hasButton(buttonsXPath[0]):
            button = self.driver.find_element_by_xpath(buttonsXPath[0])
            button.click() 
            if self.hasButton(buttonsXPath[1]) and not self.isGreen(buttonsXPath[1]):
                button = self.driver.find_element_by_xpath(buttonsXPath[1])
                button.click() 
                if self.hasButton(buttonsXPath[2]):
                    button = self.driver.find_element_by_xpath(buttonsXPath[2])
                    button.click() 
                    print('✅ Attendance marked')
            else:
                print('❎ Attendance already marked ⚠️')
        self.end()

    def end(self):
        self.driver.quit()
        self.driver=None

if __name__=='__main__':
    m = Marker(os.environ['UCSTUDENT_USERNAME'],os.environ['UCSTUDENT_KEY'])
    m.login()
    m.mark_attendance()
