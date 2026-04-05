#!/usr/bin/python3
# -*- encoding=utf8 -*-

# This is example shows how we can manage failed tests
# and make screenshots after any failed test case.

import pytest
import allure
import uuid

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

import pytest
from selenium import webdriver
import uuid

@pytest.fixture(scope="function")
def web_browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--log-level=DEBUG')
    return options

def wait_for_error_message(wait):
    try:
        return wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".rt-input-container__meta--error"))
        )
    except:
        return None

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


def get_test_case_docstring(item):
    full_name = ''
    if item._obj.__doc__:
        name = str(item._obj.__doc__.split('.')[0]).strip()
        full_name = ' '.join(name.split())
        if hasattr(item, 'callspec'):
            params = item.callspec.params
            res_keys = sorted(params.keys())
            res = [f'{key}_{params[key]!r}' for key in res_keys]
            full_name += ' Parameters ' + ', '.join(res)
            full_name = full_name.replace(':', '')
    return full_name


def pytest_itemcollected(item):
    if item._obj.__doc__:
        item._nodeid = get_test_case_docstring(item)


def pytest_collection_finish(session):
    if session.config.option.collectonly:
        for item in session.items:
            if item._obj.__doc__:
                print(get_test_case_docstring(item))
        pytest.exit('Done!')
