import os
import time
import openai
from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize the OpenAI API
API_CHATGPT = os.getenv("OPENAI_APIKEY")
openai.api_key = API_CHATGPT


class WppBot:
    
    # The constructor will take the input of the name of the bot 
    def __init__(self, nome_bot):
        self.driver = webdriver.Firefox()
    
    def send_keys(self, box, msg):
        for key in msg:
            box.send_keys(key)
    
    def start(self, contact_name):
        # Selenium will open WhatsApp and wait for 15 seconds until the DOM is ready.
        self.driver.get('https://web.whatsapp.com/')
        self.driver.implicitly_wait(60)
        # We selected the element of the WhatsApp search box by its class.
        self.search_box = self.driver.find_element(By.XPATH, 
                                                   "//div[@title='Caixa de texto de pesquisa']")

        # We will write the contact's name in the search box and wait for 2 seconds.
        self.send_keys(self.search_box, contact_name)
        time.sleep(2)
        
        # We will search for the contact/group that is in a `span` element and
        # has the title we are looking for, and then click on it. 
        self.contact = self.driver.find_element(By.XPATH, 
                                                '//span[@title = "{}"]'.format(contact_name))
        self.contact.click()
        time.sleep(2)

    # By using this method, we should send the greeting message from a list.
    def greeting(self, greeting_phrase):
        # We set the message box as the element with the Xpath.
        self.message_box = self.driver.find_element(By.XPATH, 
                                                    "//div[@title = 'Digite uma mensagem']")
        
        # We validate if the initial phrase is a list.
        if type(greeting_phrase) == list:
            # We use a 'for' loop to send each message from the list.
            for frase in greeting_phrase:
                # We write the sentence in the message box.
                self.send_keys(self.message_box, greeting_phrase)
                time.sleep(1)
                
                # We set the send button and click to send.
                self.send_button = self.driver.find_element(By.XPATH, 
                                                            "//button[@aria-label='Enviar']")
                self.send_button.click()
                time.sleep(1)
        else:
            return False
    
    def listen(self):
        # Let's set all messages in the group.
        post = self.driver.find_elements(By.XPATH, "//div[@tabindex='-1']")
        
        # Let's take the text of the last conversation and return.
        while True:
            try:
                text = post[-2].text.split('\n')
                if len(text) > 2:
                    text = text[1]
                else:
                    text = text[0]
                break
            except Exception as e:
                print(e)
        
        return text
    
    
    def answer(self, phrase):
        # We are the bot's response in the response variable.
        # We conect with the OpenAI API
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                  messages=[
                                                      {"role": "user", 
                                                       "content": phrase}
                                                      ]
                                                  )
        answer = completion.choices[0].message
        response = answer['content']
        
        # We put the prefix bot: at the beginning.
        response = 'bot: ' + response
        
        # We select the message box, fill in the response and click send.
        self.send_keys(self.message_box, response)
        time.sleep(1)
        
        self.send_button = self.driver.find_element(By.XPATH, 
                                                    "//button[@aria-label='Enviar']")
        self.send_button.click()
    
