from selenium import webdriver
from selenium.webdriver.common.by import By
from faker import Faker
import time
import math


def safe_eval(expr, x):
    # Define allowed names
    allowed_names = {
        "abs": abs,
        "math": math,
        "sin": math.sin,
        "log": math.log,
        "ln": math.log,  # allow ln as alias to math.log
    }

    # Replace ln with log (Python syntax)
    expr = expr.replace("ln", "log")

    # Replace 'x' with its actual value
    expr = expr.replace("x", str(x))

    # Evaluate
    return str(eval(expr, {"__builtins__": None}, allowed_names))


browser = webdriver.Chrome()
link = "https://suninjuly.github.io/execute_script.html"
browser.get(link)

try:
    x = int(browser.find_element(By.ID, "input_value").text)

    label_text = browser.find_element(
        By.XPATH,
        "//*[@id='input_value']/preceding-sibling::span[contains(text(), 'What is')]",
    ).text.lower()
    formula = label_text.split("what is ")[1].split(", where x")[0].strip()

    answer = safe_eval(formula, x)

    # Fill the form
    browser.find_element(By.ID, "answer").send_keys(answer)
    browser.find_element(By.ID, "robotCheckbox").click()

    robot_rad_btn = browser.find_element(By.ID, "robotsRule")
    browser.execute_script("return arguments[0].scrollIntoView(true);", robot_rad_btn)
    robot_rad_btn.click()

    # Enable and click the submit button
    submit_btn = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    browser.execute_script("return arguments[0].scrollIntoView(true);", submit_btn)
    submit_btn.click()
finally:
    time.sleep(5)
    browser.quit()
