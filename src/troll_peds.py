__fname = 'troll_peds'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
cStrDivider_1 = '#----------------------------------------------------------------#'
print('', cStrDivider, f'GO _ {__filename} -> starting IMPORTs & declaring globals', cStrDivider, sep='\n')

#------------------------------------------------------------#
#   IMORTS                                                
#------------------------------------------------------------#
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
from lxml import html
from datetime import datetime
import time, os, traceback, sys#, json
import pickle

#------------------------------------------------------------#
#   GLOBALS                                                
#------------------------------------------------------------#
DICT_LOGINS ={
    "<email@domain.com>":"<password>",
}

COOKIES_FILE = "twitter_cookies.pkl"

#------------------------------------------------------------#
#   FUNCTIONS                                                
#------------------------------------------------------------#
def save_cookies(driver, location):
    funcname = f'save_cookies(..)'
    print(funcname + ' - ENTER')
    with open(location, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)
    print(funcname + ' - DONE')

def load_cookies(driver, location):
    funcname = f'load_cookies(..)'
    print(funcname + ' - ENTER')
    with open(location, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        driver.delete_all_cookies()
        for cookie in cookies:
            print('  adding cookie ...')
            driver.add_cookie(cookie)
        # cookies = pickle.load(open("cookies.pkl", "rb"))
        # for cookie in cookies:
        #     driver.add_cookie(cookie)
    print(funcname + ' - DONE')
    return driver

# ref: gen_img.py (class BingImgGenerator)
def perform_login(_driver):
    funcname = f'perform_login(.)'
    print(funcname + ' - ENTER')

    # INP_EMAIL = (By.ID, "i0116")
    # BTN_NEXT = (By.ID, "idSIButton9")
    # INP_PW = (By.ID, "i0118")
    BTN_SIGNIN = (By.ID, "idSIButton9")
    BTN_ACCEPT= (By.ID, "acceptButton") # stay signed in
    # BTN_DECLINE = (By.ID, "declineButton") # stay signed in (decline)
    # BTN_CONTINUE = (By.ID, "id__0") # Misc
    # WebDriverWait(_driver, 10).until(EC.element_to_be_clickable(INP_EMAIL)).send_keys('self.email') # wait for and enter email
    # WebDriverWait(_driver, 10).until(EC.element_to_be_clickable(BTN_NEXT)).click() # click next
    # WebDriverWait(_driver, 10).until(EC.element_to_be_clickable(INP_PW)).send_keys('self.password') # wait for and enter pw
    # WebDriverWait(_driver, 10).until(EC.element_to_be_clickable(BTN_SIGNIN)).click() # click signin 
    # WebDriverWait(_driver, 10).until(EC.element_to_be_clickable(BTN_ACCEPT)).click() # click accept (stay logged in) ... should we?

    # enter twitter account email login
    css_selector = ".r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7"
    INP_EMAIL = (By.CSS_SELECTOR, css_selector)
    WebDriverWait(_driver, 10).until(EC.element_to_be_clickable(INP_EMAIL)).send_keys(TWITTER_EMAIL) # wait for and enter email

    # click next
    css_selector = ".css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-ywje51.r-184id4b.r-13qz1uu.r-2yi16.r-1qi8awa.r-3pj75a.r-1loqt21.r-o7ynqc.r-6416eg.r-1ny4l3l"
    BTN_NEXT = (By.CSS_SELECTOR, css_selector)
    WebDriverWait(_driver, 10).until(EC.element_to_be_clickable(BTN_NEXT)).click() # click next

    # enter twitter account password
    css_selector = ".r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7"
    INP_PW = (By.CSS_SELECTOR, css_selector)
    WebDriverWait(_driver, 10).until(EC.element_to_be_clickable(INP_PW)).send_keys(TWITTER_PW) # wait for and enter email

    # click next
    css_selector = ".css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-19yznuf.r-64el8z.r-1fkl15p.r-1loqt21.r-o7ynqc.r-6416eg.r-1ny4l3l"
    BTN_NEXT = (By.CSS_SELECTOR, css_selector)
    WebDriverWait(_driver, 10).until(EC.element_to_be_clickable(BTN_NEXT)).click() # click next

    # Save cookies after successful login
    save_cookies(_driver, COOKIES_FILE)    
    wait_sleep(5, b_print=True, bp_one_line=True)
    print()

#     err = '''
# Enter your phone number or username
# There was unusual login activity on your account. To help keep your account safe, please enter your phone number or username to verify it’s you.
# '''
#     print(f' LEFT OFF HERE ... \n {err}')
#     print('\n\ntest end ... sleep 10')
#     time.sleep(10)
#     print()

def gen_driver_options(_headless=False):
    funcname = f'gen_driver_options(.)'
    print(funcname + ' - ENTER')
    options = Options()
    if _headless:
        print(f' using --headless={_headless}')
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.111 Safari/537.36" # AWS ubuntu instance
            # ALT testing ...
            # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
            # user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15"

        options.add_argument("--no-sandbox") # ref: https://stackoverflow.com/a/53073789 (required for 'headless' on AWS ubuntu instance)
        options.add_argument("--headless")  # Run Chrome in headless mode
        options.add_argument(f"user-agent={user_agent}") # required, else '--headless' fails
        options.add_argument("--enable-javascript")
    return options

def go_do_something(_pg_url='https://x.com/i/flow/login', _headless=False):
    # global WEB_DRIVER_WAIT_CNT, WEB_DRIVER_WAIT_SEC, WEB_DRIVE_WAIT_SLEEP_SEC
    funcname = f'go_do_something(..)'
    print(funcname + ' - ENTER')

    try:
        # Initialize a Selenium WebDriver w/ driver options
        options = gen_driver_options(_headless)
        driver = webdriver.Chrome(options=options)
        # driver = load_cookies(driver, COOKIES_FILE)

        # get tweet_url page
        # print(f' getting page: {_pg_url} _ {get_time_now(dt=False)}')
        # driver.get(_pg_url)
        # print(f' getting page: {_pg_url} _ {get_time_now(dt=False)} _ DONE')

        # perform_login(driver)
        ans = input("\n Try 'COOKIES_FILE' or try new login?\n 0 = new login\n 1 = use cookie\n > ")
        use_cookie = True if ans == '1' or ans.lower() == 'y' else False
        # use_cookie = True
        print(f' use_cookie={use_cookie}')
        if not use_cookie:
            print(f" proceeding w/ new login attempt ...")
            print(f' getting page: {_pg_url} _ {get_time_now(dt=False)}')
            driver.get('https://x.com/i/flow/login')
            print(f' getting page: {_pg_url} _ {get_time_now(dt=False)} _ DONE')
            perform_login(driver)
        else:
            print(f" trying COOKIES_FILE={COOKIES_FILE}")
            if os.path.exists(COOKIES_FILE):
                print(f" found 'COOKIES_FILE' ...")
                driver.get('https://x.com/home')
                driver = load_cookies(driver, COOKIES_FILE)
                # _pg_url=
                # driver.get('https://x.com/home')
                driver.refresh()
            else:
                print(f" no 'COOKIES_FILE' found\n proceeding w/ new login attempt ...")
                perform_login(driver)

        wait_sleep(20, b_print=True, bp_one_line=True)

    except Exception as e:
        print(f" Error scraping tweet\n  **Exception** e: '{e}'\n  returning False")
        return False, 'network error, check your tweet url'
    finally:
        # Close the browser
        driver.quit()

#------------------------------------------------------------#
#   DEFAULT SUPPORT                                          
#------------------------------------------------------------#
READ_ME = f'''
    *DESCRIPTION*
        execute headless twitter integration
         for login/cookie based automation

    *NOTE* INPUT PARAMS...
        nil
        
    *EXAMPLE EXECUTION*
        $ python3 {__filename} -<nil> <nil>
        $ python3 {__filename}
'''

#ref: https://stackoverflow.com/a/1278740/2298002
def print_except(e, debugLvl=0):
    #print(type(e), e.args, e)
    if debugLvl >= 0:
        print('', cStrDivider, f' Exception Caught _ e: {e}', cStrDivider, sep='\n')
    if debugLvl >= 1:
        print('', cStrDivider, f' Exception Caught _ type(e): {type(e)}', cStrDivider, sep='\n')
    if debugLvl >= 2:
        print('', cStrDivider, f' Exception Caught _ e.args: {e.args}', cStrDivider, sep='\n')
    if debugLvl >= 3:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        strTrace = traceback.format_exc()
        print('', cStrDivider, f' type: {exc_type}', f' file: {fname}', f' line_no: {exc_tb.tb_lineno}', f' traceback: {strTrace}', cStrDivider, sep='\n')

def wait_sleep(wait_sec : int, b_print=True, bp_one_line=True): # sleep 'wait_sec'
    print(f'waiting... {wait_sec} sec')
    for s in range(wait_sec, 0, -1):
        if b_print and bp_one_line: print(wait_sec-s+1, end=' ', flush=True)
        if b_print and not bp_one_line: print('wait ', s, sep='', end='\n')
        time.sleep(1)
    if bp_one_line and b_print: print() # line break if needed
    print(f'waiting... {wait_sec} sec _ DONE')

def get_time_now(dt=True):
    if dt: return '['+datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[0:-4]+']'
    return '['+datetime.now().strftime("%H:%M:%S.%f")[0:-4]+']'

def read_cli_args():
    print(f'\nread_cli_args...\n # of args: {len(sys.argv)}\n argv lst: {str(sys.argv)}')
    for idx, val in enumerate(sys.argv): print(f' argv[{idx}]: {val}')
    print('read_cli_args _ DONE\n')
    return sys.argv, len(sys.argv)

if __name__ == "__main__":
    ## start ##
    RUN_TIME_START = get_time_now()
    print(f'\n\nRUN_TIME_START: {RUN_TIME_START}\n'+READ_ME)
    lst_argv_OG, argv_cnt = read_cli_args()

    ## exe ##
    go_do_something()
    
    ## end ##
    print(f'\n\nRUN_TIME_START: {RUN_TIME_START}\nRUN_TIME_END:   {get_time_now()}\n')

print('', cStrDivider, f'# END _ {__filename}', cStrDivider, sep='\n')

#------------------------------------------------------------#
#------------------------------------------------------------#
#   LEGACY - ref                          
#------------------------------------------------------------#
# # ref: gen_img.py (class BingImgGenerator)
# def perform_login(self, _driver):
#     INP_EMAIL = (By.ID, "i0116")
#     BTN_NEXT = (By.ID, "idSIButton9")
#     INP_PW = (By.ID, "i0118")
#     BTN_SIGNIN = (By.ID, "idSIButton9")
#     BTN_ACCEPT= (By.ID, "acceptButton") # stay signed in
#     # BTN_DECLINE = (By.ID, "declineButton") # stay signed in (decline)
#     # BTN_CONTINUE = (By.ID, "id__0") # Misc
#     WebDriverWait(_driver, 10).until(EC.element_to_be_clickable(INP_EMAIL)).send_keys(self.email) # wait for and enter email
#     WebDriverWait(_driver, 10).until(EC.element_to_be_clickable(BTN_NEXT)).click() # click next
#     WebDriverWait(_driver, 10).until(EC.element_to_be_clickable(INP_PW)).send_keys(self.password) # wait for and enter pw
#     WebDriverWait(_driver, 10).until(EC.element_to_be_clickable(BTN_SIGNIN)).click() # click signin 
#     WebDriverWait(_driver, 10).until(EC.element_to_be_clickable(BTN_ACCEPT)).click() # click accept (stay logged in) ... should we?

# # ref: req_handler.py
# def search_tweet_for_text(tweet_url, _lst_text=[], _headless=True):
#     global WEB_DRIVER_WAIT_CNT, WEB_DRIVER_WAIT_SEC, WEB_DRIVE_WAIT_SLEEP_SEC
#     funcname = f'{__filename} search_tweet_for_text'
#     print(funcname + ' - ENTER')

#     try:
#         options = Options()
#         print(f' using --headless={_headless}')
#         if _headless:
#             # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
#             # user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15"
#             user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.111 Safari/537.36" # AWS ubuntu instance

#             options.add_argument("--no-sandbox") # ref: https://stackoverflow.com/a/53073789 (required for 'headless' on AWS ubuntu instance)
#             options.add_argument("--headless")  # Run Chrome in headless mode
#             options.add_argument(f"user-agent={user_agent}") # required, else '--headless' fails
#             options.add_argument("--enable-javascript")  

#         # Initialize a Selenium WebDriver & get tweet_url page
#         print(f' getting page: {tweet_url} _ {get_time_now(dt=False)}')
#         driver = webdriver.Chrome(options=options)
#         # if '?' in tweet_url: 
#         #     tweet_url = tweet_url.split('?')[0]
#         #     print(" found '?' in tweet_url; parsed out and going with:\n  "+tweet_url)
#         driver.get(tweet_url)
#         print(f' getting page: {tweet_url} _ {get_time_now(dt=False)} _ DONE')
        
#         # loop setup
#         title = ''
#         title_check = 'X:' # end loop when found (signifies full tweet text is extractable)
#         check_cnt = 1

#         # loop through 'WebDriverWait' to find a meta tag w/ specific 'property' & 'content'
#         #   keep trying until 'title_check' is found or WEB_DRIVER_WAIT_CNTWEB_DRIVER_WAIT_CNT reached 
#         while title_check not in title and check_cnt <= WEB_DRIVER_WAIT_CNT:
#             try:
#                 print(f' Waiting for meta tag _ *ATTEMPT* # {check_cnt} _ {get_time_now()}')    
#                 WebDriverWait(driver, WEB_DRIVER_WAIT_SEC).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'meta[property="og:title"]')))
#                 meta_tag = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:title"]')
#                 title = str(meta_tag.get_attribute("content"))
#                 print(f' Found meta tag w/ Title:\n  {title} _ {get_time_now()}')
#             except Exception as e:
#                 print(f'  Error waiting for html text _ {get_time_now()} _ {WEB_DRIVER_WAIT_SEC} sec TIMEOUT (maybe)')
#                 if check_cnt == WEB_DRIVER_WAIT_CNT:
#                     raise # end loop, break & raise if last check is exception
#                 else:
#                     print(f"   **Exception** e: '{e}'\n  continuing while loop ...")
#             check_cnt += 1
#             time.sleep(WEB_DRIVE_WAIT_SLEEP_SEC) # sleep sec before next web driver attempt

#     except Exception as e:
#         print(f" Error scraping tweet\n  **Exception** e: '{e}'\n  returning False")
#         return False, 'network error, check your tweet url'
#     finally:
#         # Close the browser
#         driver.quit()

#     search_text = str(title)
#     print(f' searching html text for items in _lst_text: {_lst_text}')
#     for t in _lst_text:
#         if t.lower() in search_text.lower(): 
#             print(f' FOUND text: {t}')
#         else:
#             print(f' FAILED to find text: {t.lower()} _ returning False')
#             return False, 'must contain '+t
#     print(f' SUCCESS found all text in _lst_text _ returning True')
#     return True, ''

# # ref: teddy_bot.py
# def tweet_promo(str_tweet, img_url):
#     funcname = 'tweet_promo'
#     print(cStrDivider_1, f'ENTER - {funcname}', sep='\n')

#     # Authenticate to Twitter
#     client = tweepy.Client(
#         consumer_key=CONSUMER_KEY,
#         consumer_secret=CONSUMER_SECRET,
#         access_token=ACCESS_TOKEN,
#         access_token_secret=ACCESS_TOKEN_SECRET
#     )
#     auth = tweepy.OAuth1UserHandler(
#         CONSUMER_KEY,
#         CONSUMER_SECRET,
#         ACCESS_TOKEN,
#         ACCESS_TOKEN_SECRET,
#     )

#     # Create API object
#     api = tweepy.API(auth, wait_on_rate_limit=True)

#     # download image
#     img_file, success = get_img_from_url(img_url)
#     if not success:
#         print("FAILED - Tweeted promo with image!")
#         print('', f'EXIT - {funcname}', cStrDivider_1, sep='\n')
#         return None, False

#     # Upload image and tweet
#     media = api.media_upload(img_file)
#     response = client.create_tweet(text=str_tweet, media_ids=[media.media_id])
#     print("Tweeted promo with image!")

#     # clean up
#     delete_img_file(img_file)

#     print('', f'EXIT - {funcname}', cStrDivider_1, sep='\n')
#     return response, True