from seleniumwire import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs
from backend.config import CAPSOLVER_API_KEY,EMAIL,PASSWORD,LOGIN_URL
import time,requests

from backend.listen_mail import checkmail
from selenium.webdriver.support.ui import WebDriverWait
# from capthsolv2 import solve_geetest_v4
# from captcha_solver import solve_captcha
from backend.testfromforum import capsolver 

# from requesttosite import req
import gzip,requests
import re

EMAIL = EMAIL
PASSWORD = PASSWORD
running = False  # Bot çalışıyor mu?

validate__token = None
cikti_json = None
driver = None
wait = None
import gzip

import json


def combined_interceptor(request, response):
    global cikti_json, validate__token
    print(f"[Interceptor] URL: {request.url}")

    # === Geetest verify cevabı ===
    if cikti_json and "gcaptcha4.geetest.com/verify" in request.url:
        print("[Interceptor] verify cevabı değiştiriliyor...")

        # URL'den callback parametresini al
        parsed = urlparse(request.url)
        callback_name = parse_qs(parsed.query).get("callback", ["callback"])[0]

        # JSON'u stringe çevir
        json_str = json.dumps(cikti_json)

        # JSONP formatına çevir: geetest_xxxxx({...})
        jsonp_body = f"{callback_name}({json_str})"

        # Body'yi yaz
        response.body = jsonp_body.encode("utf-8")
        response.headers["Content-Type"] = "application/javascript"
        if "Content-Encoding" in response.headers:
            del response.headers["Content-Encoding"]

        print("Yeni verify cevabı eklendi:", jsonp_body[:200], "...")

    # === bydfi validate cevabı ===
    elif validate__token and "bydfi.com/api/geetest/validate" in request.url:
        print("[Interceptor] Validate cevabı değiştiriliyor...")
        json_str = json.dumps(validate__token)
        response.body = json_str.encode("utf-8")
        response.headers["Content-Type"] = "application/json"
        if "Content-Encoding" in response.headers:
            del response.headers["Content-Encoding"]
        print("Yeni validate cevabı eklendi:", json_str)


# Chrome options

def run():
    # go page
    global running,driver,wait
    running = True
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # work in back screen

    # Driver başlat
    driver = webdriver.Chrome(options=options)
    options.add_experimental_option("detach", True)
    driver.response_interceptor = combined_interceptor
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
        if request.response and "gcaptcha4.geetest.com/load" in request.url:
            raw_body = request.response.body
            time.sleep(1)
            # Önce gzip çözmeyi dene
            try:
                decompressed = gzip.decompress(raw_body).decode('utf-8')
            except:
                # Eğer gzip değilse direkt UTF-8 çöz
                decompressed = raw_body.decode('utf-8', errors='ignore')

            #print("Çözülmüş yanıt:\n", decompressed)
            response_text = decompressed  # senin yanıtın buraya

            # 1. Callback parantezinden JSON'u çıkar
            match = re.search(r'\((\{.*\})\)', response_text, re.S)
            if match:
                json_str = match.group(1)
                data = json.loads(json_str)

                # 2. Payload değerini al
                payload_value = data["data"]["payload"]
                process_token = data["data"]["process_token"]
                lot_number = data["data"]["lot_number"]
                #print("Payload:", payload_value)

            #print("process token",process_token)
            url = request.url
            if 'gcaptcha4.geetest.com/load' in url:
                #print(f"\n[✓] Bulunan URL:\n{url}")
                time.sleep(1)
                parsed_url = urlparse(url)
                
                query_params = parse_qs(parsed_url.query)
                #print(query_params)

                captcha_id = query_params.get('captcha_id', [None])[0]
                call_back=query_params.get('callback', [None])[0]
                #payload=query_params.get('payload', [None])[0]
                # lot_number = query_params.get('lot_number', [None])[0]
                # pass_token = query_params.get('pass_token', [None])[0]
                #print("callback:",call_back)
                
                
                # print(f"challenge: {lot_number}")
                # print(f"captcha_id: {pass_token}")
                response=capsolver(captcha_id)
                time.sleep(5)

                

                #print(response)
                captcha_id2 = response['captcha_id']
                captcha_output = response['captcha_output']
                gen_time = response['gen_time']
                lot_number2 = response['lot_number']
                pass_token = response['pass_token']
                risk_type = response['risk_type']
                user_agent = response['userAgent']

                
                print("cıktı:",{
                "status": "success",
                "data": {
                    "lot_number": lot_number,
                    "result": "success",
                    "fail_count": 0,
                    "seccode": 
                    {'captcha_id': captcha_id2, 
                        'lot_number': lot_number, 
                        'pass_token': pass_token,
                        'gen_time': gen_time,
                    'captcha_output': captcha_output
                    
                    
                    },

                    "score": "2",
                    "payload": payload_value,
                    "process_token": process_token,
                    "payload_protocol": 1
                }
                })
                global cikti_json
                cikti_json={
                "status": "success",
                "data": {
                    "lot_number": lot_number,
                    "result": "success",
                    "fail_count": 0,
                    "seccode": 
                    {'captcha_id': captcha_id2, 
                    'captcha_output': captcha_output, 
                    'gen_time': gen_time,
                    'lot_number': lot_number, 
                    'pass_token': pass_token},

                    "score": "12",
                    "payload": payload_value,
                    "process_token": process_token,
                    "payload_protocol": 1
                }
                }
                
                # # =========================
                # # Token ekle + butonu aktif yap,
                # # =========================
                # verify_url = f"https://gcaptcha4.geetest.com/verify" \
                # f"?callback={call_back}" \
                # f"&captcha_id={captcha_id2}" \
                # f"&client_type=web" \
                # f"&lot_number={lot_number}" \
                # f"&payload={payload_value}" \
                # f"&process_token={process_token}" \
                # f"&payload_protocol=1" \
                # f"&pt=1" \
                # f"&w={response['captcha_output']}"

                # headers = {
                #     "User-Agent": user_agent,
                #     "Referer": "https://www.bydfi.com"
                # }

                # verify_res = requests.get(verify_url, headers=headers)
                # print("response: ",verify_res.text)
                # time.sleep(2)
                    # --- Burada selenium'dan cookie'leri alıyoruz ---
                # selenium_cookies = driver.get_cookies()
                # print(f"Toplam çerez sayısı: {len(selenium_cookies)}")

                # # requests session oluştur
                # session = requests.Session()

                # # selenium cookie'lerini requests session'a ekle
                # for cookie in selenium_cookies:
                #     cookie_dict = {
                #         'domain': cookie['domain'],
                #         'name': cookie['name'],
                #         'value': cookie['value'],
                #         'path': cookie.get('path', '/'),
                #         'expires': cookie.get('expiry'),
                #         'secure': cookie.get('secure', False),
                #         'httpOnly': cookie.get('httpOnly', False)
                #     }
                #     # requests cookies objesine ekle
                #     session.cookies.set(cookie_dict['name'], cookie_dict['value'], domain=cookie_dict['domain'], path=cookie_dict['path'])

                # print("Cookies session'a aktarıldı.")
                # #capth ıd den capthsolvera dönüyor ve sonucları değerlere atıyor.
                # response=capsolver(captcha_id)
                # print(response)

                # captcha_id2 = response['captcha_id']
                # captcha_output = response['captcha_output']
                # gen_time = response['gen_time']
                # lot_number = response['lot_number']
                # pass_token = response['pass_token']
                # risk_type = response['risk_type']
                # user_agent = response['userAgent']

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

                validate_resp = requests.post(url_validate, headers=headers, json=data_validate)
                #print("validate resp: ",validate_resp.json())
                time.sleep(2)
                print("validate resp",validate_resp)
                global validate__token
                validate__token={
                                "code": 200,
                                "message": "",
                                "data": {
                                    "valid": "true",
                                    "token": validate_resp.json()["data"]["token"]
                                }
                            } 
                
                    # XPath ile elementi bul
                element = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[1]/div[2]/div/div/div[2]')

                # JavaScript ile class'ı kaldır
                driver.execute_script("""
                arguments[0].classList.remove('geetest_disable');
                """, element)
                time.sleep(1)
                submit_button = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[1]/div[2]/div/div/div[2]')  # login butonun xpath'i
                submit_button.click()
                time.sleep(10)
                #print(checkmail())

                
                # find passport input
                mail_code = wait.until(EC.presence_of_element_located((
                    By.XPATH,
                    '/html/body/div[4]/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/input'
                )))
                mail_code.clear()
                mail_code.send_keys(checkmail())
                time.sleep(1)

                #get_bl()

                
    
                
                
                # print("Validate response:", validate_resp.json())
                # response_json = validate_resp.json()  # Örneğin validate_resp, requests'ten dönen response
                # token = response_json['data']['token']
                # print(token)  # HhMDlkMJs0UWE31X0flLeny3lTWsvUrd
                # try:
                #     print(geetest_validate(captcha_id2,token,lot_number,captcha_output,pass_token,gen_time,user_agent))
                # except:
                #     print("post hatasi")
                # # Örnek olarak gizli inputlara çözüm değerlerini koy
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

    while running:
        time.sleep(1)

                                    
                
                
    time.sleep(2)
def stop():
    global running, driver,wait
    running = False
    if driver:
        driver.quit()
        driver = None

