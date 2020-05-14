from selenium import webdriver

#edge=webdriver.Edge(executable_path=os.getcwd()+'\drivers\MicrosoftWebDriver.exe')

try:
    browser=webdriver.Edge()
except:
    browser.quit()
finally:
    browser.get('https://api.overtrack.gg/games')
    text=browser.find_element_by_tag_name('body')
    file=open("games_list.txt","w")
    file.write(text.text)
    file.close() 
    browser.quit()