from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs
from backend.config import CAPSOLVER_API_KEY,EMAIL,PASSWORD,LOGIN_URL
import time,requests
from backend.postt import geetest_validate
from selenium.webdriver.support.ui import WebDriverWait
# from capthsolv2 import solve_geetest_v4
# from captcha_solver import solve_captcha
from backend.testfromforum import capsolver 
# from requesttosite import req

EMAIL = EMAIL
PASSWORD = PASSWORD
running = False  # Bot çalışıyor mu?

# Chrome options
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # work in back screen

# Driver başlat
driver = webdriver.Chrome(options=options)

def run():
    # go page
    global running
    running = True
    driver.get('https://www.bydfi.com/tr/login')

    wait = WebDriverWait(driver, 10)

    # # wait mail and passposrt
    email_input = wait.until(EC.presence_of_element_located((
    By.XPATH,
    '//*[@id="__next"]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[1]/div/div/input'
    
    )))
    email_input.clear()
    email_input.send_keys(EMAIL)
    time.sleep(1)

    # find passport input
    password_input = wait.until(EC.presence_of_element_located((
        By.XPATH,
        '//*[@id="__next"]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[2]/div/div/input'
    )))
    password_input.clear()
    password_input.send_keys(PASSWORD)
    time.sleep(1)

    # enter enter button
    login_button = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        '//*[@id="__next"]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[3]/button'
    )))
    login_button.click()
    time.sleep(5)  # wait to screen load
    #time.sleep(10)
    # captcha_frame = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]")

    # # get ss
    # captcha_frame.screenshot("captcha_only.png")

    # liten network and find capth_id
    for request in driver.requests:
        if request.response:
            url = request.url
            if 'gcaptcha4.geetest.com/load' in url:
                print(f"\n[✓] Finded URL :\n{url}")

                parsed_url = urlparse(url)
                query_params = parse_qs(parsed_url.query)

                captcha_id = query_params.get('captcha_id', [None])[0]
                # lot_number = query_params.get('lot_number', [None])[0]
                # pass_token = query_params.get('pass_token', [None])[0]
                
                print(f"captcha_id: {captcha_id}")#get capth_id
                time.sleep(1)
                    # --- gett cookies with selenıum ---
                selenium_cookies = driver.get_cookies()
                print(f"Toal cookies eq: {len(selenium_cookies)}")

                # requests session 
                session = requests.Session()

                # selenium cookiees add requests session'a object
                for cookie in selenium_cookies:
                    cookie_dict = {
                        'domain': cookie['domain'],
                        'name': cookie['name'],
                        'value': cookie['value'],
                        'path': cookie.get('path', '/'),
                        'expires': cookie.get('expiry'),
                        'secure': cookie.get('secure', False),
                        'httpOnly': cookie.get('httpOnly', False)
                    }
                    session.cookies.set(cookie_dict['name'], cookie_dict['value'], domain=cookie_dict['domain'], path=cookie_dict['path'])

                print("Cookies are sended session")
                #It returns from capth id to capthsolver and discards the values as a result.
                response=capsolver(captcha_id)
                print("response",response)

                captcha_id2 = response['captcha_id']
                captcha_output = response['captcha_output']
                gen_time = response['gen_time']
                lot_number = response['lot_number']
                pass_token = response['pass_token']
                risk_type = response['risk_type']
                user_agent = response['userAgent']

                url_validate = "https://www.bydfi.com/api/geetest/validate"
                headers = {
                    "Content-Type": "application/json",
                    "User-Agent": response.get('userAgent', 'Mozilla/5.0'),
                    "Referer": "https://www.bydfi.com/"
                }
                data_validate = {
                    "captcha_id": response['captcha_id'],
                    "lot_number": response['lot_number'],
                    "captcha_output": response['captcha_output'],
                    "pass_token": response['pass_token'],
                    "gen_time": response['gen_time']
                }

                validate_resp = session.post(url_validate, headers=headers, json=data_validate)
                time.sleep(2)

                print("Validate response:", validate_resp.json())
                response_json = validate_resp.json()  # response from request
                token = response_json['data']['token']
                print("token from sessıon request",token)  # 
                try:
                    print(geetest_validate(captcha_id2,token,lot_number,captcha_output,pass_token,gen_time,user_agent))
                except:
                    print("post error")
                #secret ıuputs baypass
                # driver.execute_script("""
                # document.querySelector('input[name="captcha_id"]').value = arguments[0];
                # document.querySelector('input[name="lot_number"]').value = arguments[1];
                # document.querySelector('input[name="captcha_output"]').value = arguments[2];
                # document.querySelector('input[name="pass_token"]').value = arguments[3];
                # document.querySelector('input[name="gen_time"]').value = arguments[4];
                # """, captcha_id2, lot_number, captcha_output, pass_token, gen_time)
                # js_code = f"""
                # fetch("https://gcaptcha4.geetest.com/verify?callback=geetest_{gen_time}&captcha_id={captcha_id2}&lot_number={lot_number}&payload={captcha_output}&process_token={pass_token}&payload_protocol=1&pt=1", {{
                #     method: "GET",
                #     credentials: "include"
                # }}).then(response => response.text())
                # .then(result => console.log(result));
                # """
                # driver.execute_script(js_code)


                time.sleep(10)
                submit_button = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[1]/div[2]/div/div/div[2]')  # login buton xpath
                submit_button.click()



                                    
                
                
    time.sleep(2)
def stop():
    global running
    running = False
    print("driver closed")
    driver.close()

run()