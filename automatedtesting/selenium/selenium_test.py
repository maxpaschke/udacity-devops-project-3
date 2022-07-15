# #!/usr/bin/env python
import imp
from lib2to3.pgen2 import driver
from attr import s
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def login(user, password):
    print('Starting the browser...')
    # --uncomment when running in Azure DevOps.
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    # # Local version
    # driver = webdriver.Chrome()

    print('Browser started successfully. Navigating to the demo page to login.')
    driver.get('https://www.saucedemo.com/')
    # Enter the login data
    print(f"Logging in with ${user} and ${password}")
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
        print(
            f"Login sucessfull, found {num_shopelements} items after logging in with Username {user} and Password {password}")
    return driver


def add_and_remove_cartitems(driver):
    print("Adding and removing all items to and from the cart.")
    items = driver.find_elements(By.CSS_SELECTOR, "div[class=inventory_item]")
    current_number_of_items = 0
    for item in items:
        current_number_of_items += 1
        # Find the name of the element
        name = item.find_element(
            By.CSS_SELECTOR, "div[class=inventory_item_name]").text
        print(f"Adding item `${name}` to the shopping cart.")
        item.find_element(By.CSS_SELECTOR, "button.btn_inventory").click()

        shoppingcartstatus = find_cart_status(driver)
        assert int(shoppingcartstatus) == current_number_of_items
        print(f"{shoppingcartstatus} item(s) in shopping cart.")

    print("Remove the items from the shopping cart.")
    for item in items:
        current_number_of_items -= 1
        # Find the name of the element
        name = item.find_element(
            By.CSS_SELECTOR, "div[class=inventory_item_name]").text
        print(f"Removing item `${name}` from the shopping cart.")
        item.find_element(By.CSS_SELECTOR, "button.btn_inventory").click()

        if(current_number_of_items > 0):
            shoppingcartstatus = find_cart_status(driver)
            assert int(shoppingcartstatus) == current_number_of_items
            print(f"{shoppingcartstatus} item(s) in shopping cart.")
        else:
            assert len(driver.find_elements(
                By.CSS_SELECTOR, "span[class=shopping_cart_badge")) == current_number_of_items
            print("Shopping cart empty.")


def find_cart_status(driver):
    shoppingcartstatus = driver.find_element(
        By.CSS_SELECTOR, "span[class=shopping_cart_badge").text

    return shoppingcartstatus


if __name__ == "__main__":
    print("Running UI tests for saucedemo.com demo website.")
    driver = login('standard_user', 'secret_sauce')
    add_and_remove_cartitems(driver)
    print("Selenium test sucessfully finished.")
