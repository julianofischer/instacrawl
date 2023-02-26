import os
import pickle
import time

from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from insta import Profile, Post

install_dir = "/snap/firefox/current/usr/lib/firefox"
driver_loc = os.path.join(install_dir, "geckodriver")
binary_loc = os.path.join(install_dir, "firefox")
service = FirefoxService(driver_loc)
opts = webdriver.FirefoxOptions()
opts.binary_location = binary_loc
driver = webdriver.Firefox(service=service, options=opts)
driver.get("https://www.instagram.com/")


def login():
    driver.implicitly_wait(3)
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    txtfield_username = driver.find_element(By.XPATH, "//input[@name='username']")
    txtfield_password = driver.find_element(By.XPATH, "//input[@name='password']")
    txtfield_username.clear()
    txtfield_password.clear()
    txtfield_username.send_keys(username)
    txtfield_password.send_keys(password)
    login = driver.find_element(By.XPATH, "//button[@type='submit']").click()


def main():
    if is_login_page:
        login()
        check_2fa()

    if check_login():
        pass
    else:
        return None

    p = Profile("janelas.do.meu.quarto")
    visit_profile(p)
    posts = scroll_down()
    print("Number of found posts: ", len(posts))
    posts = [Post(p_href) for p_href in posts]
    p.posts = posts
    pickle.dump(p, open(f"{p.username}.pkl", "wb"))
    driver.quit()


def is_login_page():
    # check if it is the login page
    driver.implicitly_wait(3)
    try:
        driver.find_element(By.XPATH, "//input[@name='username']")
        print("Login page")
        login()
    except:
        print("Not login page")


def check_2fa():
    driver.implicitly_wait(3)
    # check if two factor authentication is enabled
    try:
        code_field = driver.find_element(By.XPATH, "//input[@name='verificationCode']")
        two_factor = True
    except:
        two_factor = False

    if two_factor:
        code = input("Enter two factor authentication code: ")
        code_field.clear()
        code_field.send_keys(code)
        # find the confirm button and click it
        confirm_button = driver.find_element(
            By.XPATH, "//button[contains(text(),'Confirm')]"
        )
        confirm_button.click()


def check_login():
    driver.implicitly_wait(3)
    # check if login was successful
    try:
        driver.find_element(By.XPATH, "//input[@name='username']")
        print("Login failed")
        return False
    except:
        print("Login successful")
        return True


def visit_profile(profile: Profile):
    driver.get(f"https://www.instagram.com/{profile.username}/")
    driver.implicitly_wait(3)
    try:
        driver.find_element(By.XPATH, f"//h2[text()='{profile.username}']")
        print(f"Profile found and loaded: {profile.username}")
        return True
    except:
        return False


def get_posts():
    try:
        posts = driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")
        print(f"Found {len(posts)} posts")
        return posts
    except:
        print("No posts found")
        return None


def scroll_down():
    hrefs = set()
    # scroll down a infinite page to load all posts
    SCROLL_PAUSE_TIME = 2.0
    MAX_RETRIES = 3
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    scrolling_counter = 0
    retries = 0
    while True:
        _hrefs = [p.get_attribute("href").split("/")[-2] for p in get_posts()]
        hrefs.update(_hrefs)
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        scrolling_counter += 1
        print(f"Scrolling down {scrolling_counter}")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME * max(1, retries))
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # try again
            if retries > MAX_RETRIES:
                print("Reached max retries")
                break
            else:
                print(f"Trying again...")
                retries += 1
                continue
        else:
            retries = 0
            last_height = new_height
    return hrefs


##### GET POSTS INFORMATION #####
def get_post_info(post: Post):
    # get comments
    # get likes
    pass


if __name__ == "__main__":
    main()
