from playwright.sync_api import Page
import pytest

# using pytest-playwright
# browser executes automatically in the hood, it can be visually by added --headed in the execution of pytest

def test_title(page: Page):
    page.goto("https://www.saucedemo.com/")
    assert page.title() == "Swag Labs"

def test_inventory_site(page: Page):
    page.goto("https://www.saucedemo.com/inventory.html")
    assert page.inner_text('h3') == "Epic sadface: You can only access '/inventory.html' when you are logged in."

@pytest.mark.skip_browser("chromium") # skip testing in chromium
def test_without_chromium(page: Page):
    page.goto("https://www.saucedemo.com/")
    assert page.title() == "Swag Labs"

@pytest.mark.only_browser("chromium") # testing in chromium
def test_only_in_chromium(page: Page):
    page.goto("https://www.saucedemo.com/")
    assert page.title() == "Swag Labs"

# pytest --headed --base-url https://www.costam.com/ # to pass url as an arg, without hardcoded url in code

# pytest --headed --browser chromium --browser firefox # to pass browsers as an args

# pytest --headed --browser-channel chrome # to execute in real browser, installed in computer, same as Edge/Firefox

# pytest --headed --tracing on # produces testlog from execution

# pytest --headed --tracing retain-on-failure # produces testlog from execution while test its failed

# playwright show-trace /trace-results.zip # display logs in console as a table of summary

# in pytest.ini we can specify browser, headed state, slowmo, tracing etc.