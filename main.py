import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Marker():
    def __init__(self,url,username,password):
        self.username = username
        self.password = password
        self.url = url
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
        buttonsXPath.append(('//*[@id="app"]/div/div[1]/div/div/div/div/div[',']/div/div[8]/button[1]'))#cadeira (por default primeiro tem indice 6)
        buttonsXPath.append('//*[@id="app"]/div/div[1]/div/div/div/div/div/div[4]/div/div[3]/div/button[2]')#online
        buttonsXPath.append('/html/body/div[2]/div[2]/footer/button[2]')#confirmar
        buttonsXPath.append('//*[@id="app"]/div/div[1]/div/div/div/div/div/div[4]/button')#voltar
        buttonsXPath.append('//*[@id="app"]/div/div[1]/div/div/div/div/div/div[6]/button')#voltar
        buttonsXPath.append('//*[@id="app"]/div/div[1]/div/div/div/div/div/div[4]/div/div/button')#entrar sala
        buttonsXPath.append('//*[@id="app"]/div/div[1]/div/div/div/div/div/div[5]/div/div[3]/div/button[2]')#online when sala


        for i in range(6,9):
            if self.hasButton(buttonsXPath[0][0]+str(i)+buttonsXPath[0][1]):
                button = self.driver.find_element_by_xpath(buttonsXPath[0][0]+str(i)+buttonsXPath[0][1])
                button.click()

                if self.hasButton(buttonsXPath[1]):
                    """
                    When class is not in the platform
                    """
                    if not self.isGreen(buttonsXPath[1]):
                        button = self.driver.find_element_by_xpath(buttonsXPath[1])
                        button.click() 
                        if self.hasButton(buttonsXPath[2]):
                            button = self.driver.find_element_by_xpath(buttonsXPath[2])
                            button.click() 
                            print('✅ Attendance marked')
                        break
                    else:
                        print('❎ Attendance already marked ⚠️')
                        break

                elif self.hasButton(buttonsXPath[5]):
                    """
                    When class is in the platform
                    """
                    if not self.isGreen(buttonsXPath[6]):
                        button = self.driver.find_element_by_xpath(buttonsXPath[6])
                        button.click() 
                        if self.hasButton(buttonsXPath[2]):
                            button = self.driver.find_element_by_xpath(buttonsXPath[2])
                            button.click() 
                            print('✅ Attendance marked')
                        break
                    else:
                        print('❎ Attendance already marked ⚠️')
                        break
                else:
                    """
                    Return
                    """
                    if self.hasButton(buttonsXPath[3]):
                        button = self.driver.find_element_by_xpath(buttonsXPath[3])
                        button.click()
                    else:
                        button = self.driver.find_element_by_xpath(buttonsXPath[4])
                        button.click()
        self.end()

    def end(self):
        self.driver.quit()
        self.driver=None

if __name__=='__main__':
    m = Marker(os.environ['URL'],os.environ['USERNAME'],os.environ['KEY'])
    m.login()
    m.mark_attendance()
