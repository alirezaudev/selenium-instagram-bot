'''
github: https://github.com/alirezaudev
'''

# pip install selenium
# download edge driver(stable channel): https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains



def login(driver, user_name, password):
    print("\nlogin... please wait")
    try:
        # open login page
        driver.get("https://www.instagram.com/")

        # Login
        driver.find_element(By.XPATH, "//input[@name='username']").send_keys(user_name)
        driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)

        # find and click on "login" button
        driver.find_element(By.CLASS_NAME, "L3NKy").click()
        sleep(5)

        # find and click on "save info" button
        driver.find_element(By.CLASS_NAME, "L3NKy").click()
        sleep(5)

        # turn of notification
        driver.find_element(By.CLASS_NAME, "HoLwm").click()
        sleep(2)
        return True

    except:
        error = driver.find_element(By.ID, "slfErrorAlert")
        print("\n", error.text)
        return False


def save(users):

    with open("users.txt", "w") as f:
        for user in users:
            f.write(f"\n@{user}")

    sleep(1)



def extract_users(driver, link):

    driver.get(link)

    # click on "likes" button to show users id
    try:
        driver.find_element(By.XPATH, '//a[text()=" likes"]').click()
        sleep(2)

    except:
        driver.find_element(By.XPATH, '//a[text()=" others"]').click()
        sleep(2)


    try:
        users = []

        # Match to show the number of times when he saved 9 usernames in users
        match = 0

        # number of likes
        try:
            likes = driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[2]/div/div[2]/a/span').text

        except:
            likes = driver.find_element(By.XPATH, '//a[text()=" likes"]').text.split()[0]

        # count is the number of times that add 9 usernames in users
        # divide the number of likes by 9(likes//9)
        count = int(likes)//9 + 1

        while match < count:

            match += 1

            # get all 9 Usernames in page
            elements = driver.find_elements(By.XPATH, "//a[@class='FPmhX notranslate MBL3Z']")

            # Add all users names to users
            for element in elements:
                if element.get_attribute('title') not in users:
                    i = element.get_attribute('title')
                    users.append(i)

            print(f"{match:<5} of  {count}")


            # Scroll down
            # if your internet is so slow change the sleep time to 1 or 2 second
            driver.execute_script("return arguments[0].scrollIntoView();", elements[-1])
            sleep(.5)
            driver.execute_script("return arguments[0].scrollIntoView(true);", elements[-1])
            sleep(.5)
            driver.execute_script("return arguments[0].scrollIntoView();", elements[-1])



    # Finally, save all the users, who you got
    finally:
        save(users)

        print(f"successfully saved {len(users)} User id in users.txt")
        driver.quit()



def main():
    user_name = input("Enter User name: ")
    password = input("Enter password: ")
    url = input("enter post url: ")

    driver = webdriver.Edge(executable_path='msedgedriver.exe')

    # if login was successfully continue
    if login(driver, user_name, password):
        extract_users(driver, url)




if __name__ == '__main__':
    main()

