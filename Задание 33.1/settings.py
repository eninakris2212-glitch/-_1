import pytest

# Эта фикстура нужна для использования pytest.wait в тестах
@pytest.fixture(scope="session")
def wait(selenium):
    return selenium.WebDriverWait(selenium, 15)

# Новая фикстура для открытия страницы
@pytest.fixture
def open_auth_page(selenium):
    """Открывает страницу авторизации и выбирает вкладку 'Почта'."""
    selenium.get("https://b2c.passport.rt.ru/")
    # Ждем и кликаем на вкладку "Почта"
    email_tab = selenium.find_element("css selector", "button[data-tab='email']")
    email_tab.click()
    # Возвращаем драйвер для дальнейших действий в тесте
    return selenium

import os

from dotenv import load_dotenv

load_dotenv()

valid_email = os.getenv('valid_email')
valid_phone = os.getenv('valid_phone')
valid_login = os.getenv('valid_login')

valid_password_email = os.getenv('valid_password_email')
valid_password_phone = os.getenv('valid_password_phone')

invalid_phone = os.getenv('invalid_phone')
invalid_email = os.getenv('invalid_email')
invalid_login = os.getenv('invalid_login')

invalid_password = os.getenv('invalid_password')
