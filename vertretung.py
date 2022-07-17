import json
import re
import time
from datetime import datetime as dt
from datetime import date as d
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True

driver = webdriver.Chrome(options=options)  # Optional argument, if not specified will search path. (main error source when trying things out on windows first)
driver.get('https://freygym.eltern-portal.org/')
#time.sleep(1) # Let the user actually see something!
user = driver.find_element_by_id('inputEmail')
user.send_keys('elke.neuenfeld@googlemail.com')
password = driver.find_element_by_id('inputPassword')
password.send_keys('Gymmi12')
form = driver.find_element_by_class_name('form-signin')
form.submit()
#time.sleep(1) # Let the user actually see something!
kids = driver.find_element_by_class_name('pupil-selector')
kids = [ k.text for k in kids.find_elements_by_tag_name('option') ]

time.sleep(2)
v = driver.find_elements_by_tag_name('button')
for e in v:
    if 'Toggle navigation' in e.text:
        e.click()
        break

time.sleep(2)
x = driver.find_element_by_link_text('Service')
x.click()

x = driver.find_element_by_link_text('Klassen Vertretungsplan')
x.click()

outp = []
for k in kids:
    kids = driver.find_element_by_class_name('pupil-selector')
    for kk in kids.find_elements_by_tag_name('option'):
        if kk.text == k:# and kk.text != 'Maya Neuenfeld (12Q)':
            print(kk.text)
            kk.click()
            break

    time.sleep(2)
    res = driver.find_element_by_id('asam_content')
#    print(f'\n{k}\n\n{res.text}')

    plan = []
    day = {}
    content = []
    for l in res.text.split('\n'):
        if l.startswith('Stand:'): break
        if re.match('\w{2}., \d\d.\d\d.\d\d\d\d - KW \d\d', l):
            content = []
            
            day = { 'day': l, 'content': content }
            plan.append(day)
            
            continue
        if len(day) == 0: continue
        else:
            if l.startswith('Std.'):
                continue
            elif l.startswith('Keine Vertretungen'):
                continue
            elif int(dt.now().strftime("%H")) >= 9 and day['day'].split(' ')[1] == d.today().strftime('%d.%m.%Y'):
                continue
            else:
                if l not in content:
                    content.append(l)
        

    res = {
        'name': ' '.join(k.strip().split(' ')[0:2]),
        'klasse' : k.strip().split(' ')[-1][1:-1],
        'plan' : plan
    }

    #print('RES', res)
    outp.append(res)

    time.sleep(3)

#print(outp)

time.sleep(3)
#with open('/home/pi/vertretung.json', 'w') as f:
with open('vertretung.json', 'w') as f:
   json.dump(outp, f)
    
driver.quit()