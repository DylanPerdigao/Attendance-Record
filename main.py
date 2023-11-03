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
            wait = WebDriverWait(self.driver,10,2)
            wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        except Exception as e:
            print('❌ Button not found\n',e)
            return False
        else:
            return True

    def mark_attendance(self):
        buttonsXPath=[] 
        buttonsXPath.append(('login','//*[@id="app"]/div/main/div/div/div/div/div[2]/div[1]/div/form/div[3]/button'))  #login button
        buttonsXPath.append(("course",'//*[@id="app"]/div/main/div/div/div[3]/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/button'))#cadeira (por default primeiro tem indice 6)                           
        buttonsXPath.append(("location",'//*[@id="app"]/div/main/div/div/div/div/div/div/div[4]/div/div[3]/div/button[1]')) #local
        # buttonsXPath.append('//*[@id="app"]/div/main/div/div/div/div/div/div/div[4]/div/div[3]/div/button[2]') #online
        buttonsXPath.append(("confirm",'//*[@class="dialog modal is-active"]/div[1]/footer/button[1]')) #confirmar 
        buttonsXPath.append(("return",'//*[@id="app"]/div/main/div/div/div/div/div/div/div[5]/button'))#voltar a pagina anterior (cadeiras)
        for i, (name,b) in enumerate(buttonsXPath):
            print(name)
            if self.hasButton(b):
                if name in ["login","course", "return","location"]:
                    if self.isGreen(b) and name == "location":
                        print('❎ Attendance already marked ⚠️')
                        self.end()
                    else:
                        button = self.driver.find_element(By.XPATH,b)
                        button.click() 
            if name == 'confirm':
                try:
                    button = self.driver.find_element(By.CSS_SELECTOR,'.dialog.modal.is-active .button.is-primary')
                    button.click() 
                    print('✅ Attendance marked')
                except:
                    pass                   
        self.end()

    def end(self):
        self.driver.quit()
        print('👋 Bye')
        exit()

if __name__=='__main__':
    m = Marker(os.environ['URL'],os.environ['USERNAME'],os.environ['KEY'])
    m.login()
    m.mark_attendance()
