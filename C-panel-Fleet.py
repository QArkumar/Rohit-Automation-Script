import pytest
import allure
from playwright.sync_api import sync_playwright
import random
import string

def random_alpha(n):
    return ''.join(random.choices(string.ascii_letters, k=n))

def random_alphanum(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


@allure.feature("Fleet Management")
@allure.story("Create Fleet")
def test_create_fleet():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        with allure.step("Open application URL"):
            page.goto("https://afm2020.com/")

        with allure.step("Login to application"):
            page.fill("#txtCorporateId", "AFMDEMO")
            page.fill("#txtUserName", "rohitk")
            page.fill("#txtPassword", "Rohit@123")
            page.click("#signin")

        with allure.step("Wait for dashboard to load"):
            page.wait_for_selector("#divMenuHTML")

        with allure.step("Navigate to C Panel"):
            page.click('xpath=//*[@id="divMenuHTML"]/div[1]/ul/li[5]/a/span')

        with allure.step("Open Fleet section"):
            page.click('xpath=//*[@id="MNU00005"]/ul/li[2]/a')

        with allure.step("Click Add Fleet button"):
            page.wait_for_selector("#btnAddFleet")
            page.click("#btnAddFleet")

        with allure.step("Fill Fleet details"):
            page.fill("#txtFleetName", random_alpha(4))
            page.fill("#txtFleetFirstAddress", random_alphanum(8))
            page.fill("#txtFleetPhone", "(802) 549-6734")

        with allure.step("Select State"):
            page.click("#select2-ddlFleetStates-container")
            page.fill(".select2-search__field", "Ontario")
            page.wait_for_selector(".select2-results__option")
            page.click(".select2-results__option")

        with allure.step("Select City"):
            page.wait_for_timeout(2000)
            page.click("#select2-ddlFleetCities-container")
            page.fill(".select2-search__field", "Brampton")
            page.wait_for_selector(".select2-results__option")
            page.click(".select2-results__option")

        with allure.step("Enter Zip Code"):
            page.fill("#txtFleetZip", "12345")

        with allure.step("Submit Fleet form"):
            page.click("#btnFleetSubmit")

        with allure.step("Wait for success and capture screenshot"):
            page.wait_for_timeout(5000)
            page.screenshot(path="fleet.png")
            allure.attach.file("fleet.png", name="Fleet Created", attachment_type=allure.attachment_type.PNG)

        browser.close()
