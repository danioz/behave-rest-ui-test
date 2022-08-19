from behave import *
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def before_all(context):
    context.api_url = 'https://restful-booker.herokuapp.com'
    context.ui_url = 'https://www.saucedemo.com/'


def before_tag(context, tag):
    if tag == "ui":
        use_fixture(browser_chrome, context, timeout=10)
        context.driver.delete_all_cookies()
        context.driver.get(context.ui_url)


@fixture
def browser_chrome(context, timeout=30, **kwargs):
    options = webdriver.ChromeOptions()
    options.headless = False
    context.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    yield context.driver

    context.driver.quit()




def before_scenario(context, scenario):
    pass
def after_scenario(context, scenario):
    pass
