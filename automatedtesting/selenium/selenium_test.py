# #!/usr/bin/env python
import imp
import datetime
from lib2to3.pgen2 import driver
import string
from attr import s
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def login(user, password):
    log('Starting the browser...')
    # --uncomment when running in Azure DevOps.
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    # # Local version
    # driver = webdriver.Chrome()

    log('Browser started successfully. Navigating to the demo page to login.')
    driver.get('https://www.saucedemo.com/')
    # Enter the login data
    log(f"Logging in with ${user} and ${password}")
    driver.find_element(
        By.CSS_SELECTOR, "input[id='user-name']").send_keys(user)
    driver.find_element(
        By.CSS_SELECTOR, "input[id='password']").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "input[id='login-button']").click()

    num_shopelements = len(driver.find_elements(
        By.CSS_SELECTOR, "div[class=inventory_item]"))
    loginsucessfull = num_shopelements == 6
    assert loginsucessfull
    if(loginsucessfull):
        log(
            f"Login sucessfull, found {num_shopelements} items after logging in with Username {user} and Password {password}")
    return driver


def add_and_remove_cartitems(driver):
    log("Adding and removing all items to and from the cart.")
    items = driver.find_elements(By.CSS_SELECTOR, "div[class=inventory_item]")
    current_number_of_items = 0
    for item in items:
        current_number_of_items += 1
        # Find the name of the element
        name = item.find_element(
            By.CSS_SELECTOR, "div[class=inventory_item_name]").text
        log(f"Adding item `${name}` to the shopping cart.")
        item.find_element(By.CSS_SELECTOR, "button.btn_inventory").click()

        shoppingcartstatus = find_cart_status(driver)
        assert int(shoppingcartstatus) == current_number_of_items
        log(f"{shoppingcartstatus} item(s) in shopping cart.")

    log("Remove the items from the shopping cart.")
    for item in items:
        current_number_of_items -= 1
        # Find the name of the element
        name = item.find_element(
            By.CSS_SELECTOR, "div[class=inventory_item_name]").text
        log(f"Removing item `${name}` from the shopping cart.")
        item.find_element(By.CSS_SELECTOR, "button.btn_inventory").click()

        if(current_number_of_items > 0):
            shoppingcartstatus = find_cart_status(driver)
            assert int(shoppingcartstatus) == current_number_of_items
            log(f"{shoppingcartstatus} item(s) in shopping cart.")
        else:
            assert len(driver.find_elements(
                By.CSS_SELECTOR, "span[class=shopping_cart_badge")) == current_number_of_items
            log("Shopping cart empty.")


def find_cart_status(driver):
    shoppingcartstatus = driver.find_element(
        By.CSS_SELECTOR, "span[class=shopping_cart_badge").text

    return shoppingcartstatus


def log(input: str):
    datestring = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    print(datestring+': ' + input)


if __name__ == "__main__":
    log("Running UI tests for saucedemo.com demo website.")
    driver = login('standard_user', 'secret_sauce')
    add_and_remove_cartitems(driver)
    log("Selenium test sucessfully finished.")
