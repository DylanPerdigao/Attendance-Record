import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager



class Marker():
    def __init__(self,url,username,password):
        self.username = username
        self.password = password
        self.url = url
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        try:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
        except Exception as e:
            print('❌ Driver not found\n',e)

    def login(self):
        #open url
        self.driver.get(self.url) 
        #email & pass  
        email_input,pass_input = self.driver.find_elements(By.TAG_NAME,"input")[:2]
        email_input.send_keys(self.username)
        pass_input.send_keys(self.password)
        #login
        login_button = self.driver.find_elements(By.TAG_NAME,"button")[0]    
        login_button.click()

    def isGreen(self,xpath):
        button = self.driver.find_element(By.XPATH,xpath)
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
        except Exception as e:
            print('❌ Button not found\n',e)
            return False
        else:
            return True

    def mark_attendance(self):
        buttonsXPath=list()
        for i in [1,2]:
            buttonsXPath.append('//*[@id="app"]/div/main/div[2]/div/div/div[4]/div[2]/div[2]/div/div[{i}]/div[2]/div[2]/div[1]/button')#cadeira (por default primeiro tem indice 6)
            buttonsXPath.append('//*[@id="app"]/div/main/div/div/div/div/div/div/div[4]/div/div[3]/div/button[1]') #local
            # buttonsXPath.append('//*[@id="app"]/div/main/div/div/div/div/div/div/div[4]/div/div[3]/div/button[2]') #online
            buttonsXPath.append('/html/body/div[2]/div[2]/footer/button[2]') #confirmar
            buttonsXPath.append('//*[@id="app"]/div/main/div/div/div/div/div/div/div[5]/button')#voltar a pagina anterior (cadeiras)

        for i in range(6,9):
            if self.hasButton(buttonsXPath[0][0]+str(i)+buttonsXPath[0][1]):
                button = self.driver.find_element(By.XPATH,buttonsXPath[0][0]+str(i)+buttonsXPath[0][1])
                button.click()

                if self.hasButton(buttonsXPath[1]):
                    """
                    When class is not in the platform
                    """
                    if not self.isGreen(buttonsXPath[1]):
                        button = self.driver.find_element(By.XPATH,buttonsXPath[1])
                        button.click() 
                        if self.hasButton(buttonsXPath[2]):
                            button = self.driver.find_element(By.XPATH,buttonsXPath[2])
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
                        button = self.driver.find_element(By.XPATH,buttonsXPath[6])
                        button.click() 
                        if self.hasButton(buttonsXPath[2]):
                            button = self.driver.find_element(By.XPATH,buttonsXPath[2])
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
                        button = self.driver.find_element(By.XPATH,buttonsXPath[3])
                        button.click()
                    else:
                        button = self.driver.find_element(By.XPATH,buttonsXPath[4])
                        button.click()
        self.end()

    def end(self):
        self.driver.quit()
        self.driver=None

if __name__=='__main__':
    m = Marker(os.environ['URL'],os.environ['USERNAME'],os.environ['KEY'])
    m.login()
    m.mark_attendance()
