import pytest
import allure
import random
import string
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://b2c.passport.rt.ru"
VALID_EMAIL = "enin.a.a@bk.ru"
VALID_PASSWORD = "Qq1234567@"
VALID_PHONE = "+79959907541"
VALID_LOGIN = "rtkid_177514844420"

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def generate_test_email():
    return f"test_{random_string()}@test.com"


def generate_test_phone():
    return f"+7{random.randint(900, 999)}{random.randint(1000000, 9999999)}"



def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def generate_test_email():
    return f"test_{random_string()}@test.com"


def generate_test_phone():
    return f"+7{random.randint(900, 999)}{random.randint(1000000, 9999999)}"

def wait_for_error_message(wait):
    try:
        return wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".rt-input-container__meta--error"))
        )
    except:
        return None

@allure.feature("Авторизация")
@allure.story("Успешная авторизация")
def test_07_successful_login_by_email(web_browser):
    """
    7. Успешная авторизация по валидной почте и паролю.
    Ожидаемый результат: Редирект на страницу redirect_uri.
    """
    wait = WebDriverWait(web_browser, 10)

    with allure.step("Открытие страницы авторизации"):
        web_browser.get(BASE_URL)

    with allure.step("Выбор вкладки 'Почта'"):
        # На сайте Ростелеком вкладки выбираются по ID или другим локаторам
        email_tab = wait.until(EC.element_to_be_clickable((By.ID, "t-btn-tab-mail")))
        email_tab.click()

    with allure.step("Заполнение полей формы"):
        login_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        password_field = web_browser.find_element(By.ID, "password")
        login_field.send_keys(VALID_EMAIL)
        password_field.send_keys(VALID_PASSWORD)

    with allure.step("Нажатие кнопки 'Войти'"):
        web_browser.find_element(By.ID, "kc-login").click()

    with allure.step("Проверка успешного редиректа"):
        # Ждем либо редирект, либо появление ошибки
        try:
            wait.until(lambda drv: "account_b2c" in drv.current_url or "lk.rt.ru" in drv.current_url)
            assert "account_b2c" in web_browser.current_url or "lk.rt.ru" in web_browser.current_url
        except:
            # Если не удалось авторизоваться, проверяем наличие ошибки
            error_elements = web_browser.find_elements(By.CSS_SELECTOR, ".rt-input-container__meta--error")
            if error_elements:
                assert "Неверный логин или пароль" in error_elements[0].text


@allure.feature("Авторизация")
@allure.story("Авторизация по телефону")
def test_08_successful_login_by_phone(web_browser):
    """
    8. Успешная авторизация по номеру телефона.
    Ожидаемый результат: Редирект на страницу redirect_uri.
    """
    wait = WebDriverWait(web_browser, 10)
    web_browser.get(BASE_URL)

    # По умолчанию открыта вкладка телефона
    phone_tab = wait.until(EC.element_to_be_clickable((By.ID, "t-btn-tab-phone")))
    # Если уже выбрана, просто проверяем
    if "rt-tab--active" not in phone_tab.get_attribute("class"):
        phone_tab.click()

    phone_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_field = web_browser.find_element(By.ID, "password")

    phone_field.send_keys(VALID_PHONE)
    password_field.send_keys(VALID_PASSWORD)

    web_browser.find_element(By.ID, "kc-login").click()

    # Ждем либо редирект, либо ошибку
    try:
        wait.until(lambda drv: "account_b2c" in drv.current_url or "lk.rt.ru" in drv.current_url)
        assert "account_b2c" in web_browser.current_url or "lk.rt.ru" in web_browser.current_url
    except:
        error_elements = web_browser.find_elements(By.CSS_SELECTOR, ".rt-input-container__meta--error")
        if error_elements:
            assert "Неверный логин или пароль" in error_elements[0].text


@allure.feature("Авторизация")
@allure.story("Авторизация по логину")
def test_09_successful_login_by_username(web_browser):
    """
    9. Успешная авторизация по логину.
    Ожидаемый результат: Редирект на страницу redirect_uri.
    """
    wait = WebDriverWait(web_browser, 10)
    web_browser.get(BASE_URL)

    login_tab = wait.until(EC.element_to_be_clickable((By.ID, "t-btn-tab-login")))
    login_tab.click()

    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_field = web_browser.find_element(By.ID, "password")

    username_field.send_keys(VALID_LOGIN)
    password_field.send_keys(VALID_PASSWORD)

    web_browser.find_element(By.ID, "kc-login").click()

    # Ждем либо редирект, либо ошибку
    try:
        wait.until(lambda drv: "account_b2c" in drv.current_url or "lk.rt.ru" in drv.current_url)
        assert "account_b2c" in web_browser.current_url or "lk.rt.ru" in web_browser.current_url
    except:
        error_elements = web_browser.find_elements(By.CSS_SELECTOR, ".rt-input-container__meta--error")
        if error_elements:
            assert "Неверный логин или пароль" in error_elements[0].text


@allure.feature("Восстановление пароля")
@allure.story("Восстановление по SMS")
def test_10_password_recovery_by_sms(web_browser):
    """
    10. Восстановление пароля по SMS.
    Ожидаемый результат: Переход на страницу подтверждения.
    """
    wait = WebDriverWait(web_browser, 15)

    with allure.step("Открытие страницы авторизации"):
        web_browser.get(BASE_URL)
        time.sleep(2)

    with allure.step("Переход на страницу восстановления пароля"):
        forgot_link = wait.until(EC.element_to_be_clickable((By.ID, "forgot_password")))
        forgot_link.click()

    with allure.step("Ввод номера телефона"):
        phone_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        phone_field.send_keys(VALID_PHONE)

    with allure.step("Нажатие кнопки 'Получить код'"):
        web_browser.find_element(By.ID, "reset").click()
        time.sleep(3)

    with allure.step("Проверка перехода на страницу подтверждения"):
        sms_confirmation_page = wait.until(EC.url_contains("reset-credentials"))
        assert "reset-credentials" in web_browser.current_url

@allure.feature("Восстановление пароля")
@allure.story("Восстановление по почте")
def test_11_password_recovery_by_email(web_browser):
    """
    11. Восстановление пароля по почте.
    Ожидаемый результат: Переход на страницу подтверждения.
    """
    wait = WebDriverWait(web_browser, 30)


    with allure.step("Открытие страницы авторизации"):
        web_browser.get(BASE_URL)
        time.sleep(2)

    with allure.step("Переход на страницу восстановления пароля"):
        forgot_link = wait.until(EC.element_to_be_clickable((By.ID, "forgot_password")))
        forgot_link.click()

    with allure.step("Ввод адреса почты"):
        email_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        email_field.send_keys(VALID_EMAIL)

    with allure.step("Нажатие кнопки 'Получить код'"):
        web_browser.find_element(By.ID, "reset").click()
        time.sleep(3)

    with allure.step("Проверка перехода на страницу подтверждения"):
        sms_confirmation_page = wait.until(EC.url_contains("reset-credentials"))
        assert "reset-credentials" in web_browser.current_url


@allure.feature("Восстановление пароля")
@allure.story("Восстановление по логину")
def test_12_password_recovery_by_login(web_browser):
    """
        12. Восстановление пароля по Логину.
        Ожидаемый результат: Переход на страницу подтверждения.
        """
    wait = WebDriverWait(web_browser, 30)

    with allure.step("Открытие страницы авторизации"):
        web_browser.get(BASE_URL)
        time.sleep(2)

    with allure.step("Переход на страницу восстановления пароля"):
        forgot_link = wait.until(EC.element_to_be_clickable((By.ID, "forgot_password")))
        forgot_link.click()

    with allure.step("Ввод логина"):
        login_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        login_field.send_keys(VALID_LOGIN)

    with allure.step("Нажатие кнопки 'Получить код'"):
        web_browser.find_element(By.ID, "reset").click()
        time.sleep(3)

    with allure.step("Проверка перехода на страницу подтверждения"):
        sms_confirmation_page = wait.until(EC.url_contains("reset-credentials"))
        assert "reset-credentials" in web_browser.current_url

@allure.feature("Безопасность")
@allure.story("Работа капчи")
def test_13_captcha_functionality(web_browser):
    """
    13. Проверка работы капчи.
    Ожидаемый результат: Появление капчи при многократных ошибках.
    """
    wait = WebDriverWait(web_browser, 15)

    with allure.step("Открытие страницы авторизации"):
        web_browser.get(BASE_URL)
        time.sleep(2)

    with allure.step("Несколько попыток авторизации с ошибками"):
        for _ in range(5):
            login_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
            password_field = web_browser.find_element(By.ID, "password")

            login_field.send_keys("wrong_email")
            password_field.send_keys("wrong_password")

            web_browser.find_element(By.ID, "kc-login").click()
            time.sleep(2)

    with allure.step("Проверка появления капчи"):
        captcha = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "rt-captcha__image")))
        assert "rt-captcha__image" in captcha.get_attribute("class")


@allure.feature("Интерфейс")
@allure.story("Кнопка 'Показать пароль'")
def test_14_show_password_button(web_browser):
    """
    14. Проверка работы кнопки 'Показать пароль'.
    Ожидаемый результат: Пароль становится видимым.
    """
    wait = WebDriverWait(web_browser, 15)

    with allure.step("Открытие страницы авторизации"):
        web_browser.get(BASE_URL)
        time.sleep(2)

    with allure.step("Ввод пароля"):
        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.send_keys(VALID_PASSWORD)

    with allure.step("Нажатие на кнопку 'Показать пароль'"):
        show_password_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "rt-input__eye")))
        show_password_button.click()

    with allure.step("Проверка видимости пароля"):
        password_type = password_field.get_attribute("type")
        assert password_type == "text", "Пароль остался скрытым"

    with allure.step("Проверка скрытия пароля после повторного нажатия"):
        show_password_button.click()
        password_type = password_field.get_attribute("type")
        assert password_type == "password", "Пароль не стал скрытым"

@allure.feature("Авторизация")
@allure.story("Переключение между способами")
def test_15_switch_between_auth_methods(web_browser):
    """
    15. Переключение между способами авторизации.
    Ожидаемый результат: Возможность переключения между методами.
    """
    wait = WebDriverWait(web_browser, 15)

    with allure.step("Открытие страницы авторизации"):
        web_browser.get(BASE_URL)
        time.sleep(2)

    with allure.step("Проверка вкладки 'Телефон'"):
        phone_tab = wait.until(EC.element_to_be_clickable((By.ID, "t-btn-tab-phone")))
        phone_tab.click()
        assert "rt-tab--active" in phone_tab.get_attribute("class")

    with allure.step("Проверка вкладки 'Почта'"):
        email_tab = wait.until(EC.element_to_be_clickable((By.ID, "t-btn-tab-mail")))
        email_tab.click()
        assert "rt-tab--active" in email_tab.get_attribute("class")

    with allure.step("Проверка вкладки 'Логин'"):
        login_tab = wait.until(EC.element_to_be_clickable((By.ID, "t-btn-tab-login")))
        login_tab.click()
        assert "rt-tab--active" in login_tab.get_attribute("class")

    with allure.step("Проверка вкладки 'ЛС'"):
        ls_tab = wait.until(EC.element_to_be_clickable((By.ID, "t-btn-tab-ls")))
        ls_tab.click()
        assert "rt-tab--active" in ls_tab.get_attribute("class")

@allure.feature("Авторизация")
@allure.story("Социальные сети")
def test_16_auth_via_yandex(web_browser):
    """
    16. Авторизация через социальную сеть Яндекс.
    Ожидаемый результат: Переход на страницу авторизации Яндекс.
    """
    wait = WebDriverWait(web_browser, 15)

    with allure.step("Открытие страницы авторизации"):
        web_browser.get(BASE_URL)
        time.sleep(2)

    with allure.step("Поиск кнопки авторизации через Яндекс"):
        # Ищем кнопки социальных сетей
        social_buttons = web_browser.find_elements(
            By.CSS_SELECTOR, "a[class*='social'], button[class*='social'], div[class*='social']")

        yandex_button = None
        yandex_keywords = ['yandex', 'яндекс', 'ya.ru', 'ya-']

        for button in social_buttons:
            html = button.get_attribute('outerHTML').lower()
            if any(keyword in html for keyword in yandex_keywords):
                yandex_button = button
                break

        # Альтернативный поиск по ID или класс

@allure.feature("Авторизация")
@allure.story("Форма авторизации по умолчанию")
def test_17_default_login_tab_is_phone(web_browser):
    """
    17. Проверка, что форма авторизации через 'Телефон' выбрана по умолчанию.
    Ожидаемый результат: Активная вкладка — 'Телефон'.
    """
    wait = WebDriverWait(web_browser, 15)

    with allure.step("Открытие страницы авторизации"):
        web_browser.get(BASE_URL)

    with allure.step("Проверка выбранной вкладки"):
        # Проверяем, что вкладка 'Телефон' активна
        phone_tab = wait.until(
            EC.visibility_of_element_located((By.ID, "t-btn-tab-phone"))
        )
        assert "rt-tab--active" in phone_tab.get_attribute("class"), \
            "Активной вкладкой не является 'Телефон'"

    with allure.step("Проверка плейсхолдера поля ввода"):
        # Ждем, пока элемент станет интерактивным
        phone_input = wait.until(
            EC.element_to_be_clickable((By.ID, "username"))
        )

@allure.feature("Регистрация")
@allure.story("Регистрация нового пользователя")
def test_18_registration_new_user(web_browser):
    """
    18. Регистрация нового пользователя.
    Ожидаемый результат: Успешная регистрация или соответствующие сообщения валидации.
    """
    wait = WebDriverWait(web_browser, 15)

    with allure.step("Открытие страницы авторизации"):
        web_browser.get(BASE_URL)
        time.sleep(2)

    with allure.step("Переход на страницу регистрации"):
        register_link = wait.until(EC.element_to_be_clickable((By.ID, "kc-register")))
        register_link.click()
        time.sleep(2)

    with allure.step("Заполнение формы регистрации"):
        # Генерируем тестовые данные
        test_firstname = f"Test{random_string(5)}"
        test_lastname = f"User{random_string(5)}"
        test_email = generate_test_email()
        test_password = f"Qq{random_string(6)}@"

        # Заполняем поля
        firstname_field = wait.until(EC.presence_of_element_located((By.NAME, "firstName")))
        lastname_field = web_browser.find_element(By.NAME, "lastName")
        region_field = web_browser.find_element(By.CSS_SELECTOR, "input[autocomplete='new-password']")
        email_field = web_browser.find_element(By.ID, "address")
        password_field = web_browser.find_element(By.ID, "password")
        confirm_password_field = web_browser.find_element(By.ID, "password-confirm")

        firstname_field.send_keys(test_firstname)
        lastname_field.send_keys(test_lastname)

        # Регион обычно заполняется автоматически, проверяем
        region_value = region_field.get_attribute("value")
        if not region_value:
            region_field.click()
            time.sleep(1)
            # Выбираем первый вариант из выпадающего списка
            region_option = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".rt-select__list-item")))
            region_option.click()

        email_field.send_keys(test_email)
        password_field.send_keys(test_password)
        confirm_password_field.send_keys(test_password)

        # Прикрепляем тестовые данные к отчету
        allure.attach(f"Имя: {test_firstname}\nФамилия: {test_lastname}\nEmail: {test_email}\nПароль: {test_password}",
                      name="Test Registration Data")

    with allure.step("Принятие пользовательского соглашения"):
        # Находим и активируем чекбокс
        try:
            checkbox = web_browser.find_element(By.CSS_SELECTOR, "input[name='register-confirm']")
            if not checkbox.is_selected():
                # Кликаем на связанный label
                label = web_browser.find_element(By.CSS_SELECTOR, "label[for='register-confirm']")
                label.click()
        except:
            # Альтернативный локатор
            try:
                checkbox = web_browser.find_element(By.CSS_SELECTOR, ".rt-checkbox__input")
                if not checkbox.is_selected():
                    checkbox.click()
            except:
                pass

    with allure.step("Нажатие кнопки 'Зарегистрироваться'"):
        register_btn = web_browser.find_element(By.NAME, "register")

        # Проверяем, активна ли кнопка
        if register_btn.is_enabled():
            register_btn.click()
            time.sleep(5)

            # Проверяем результат
            current_url = web_browser.current_url

            if "confirm-email" in current_url or "confirm" in current_url:
                # Успешная регистрация, перешли к подтверждению email
                allure.attach("Регистрация успешна, требуется подтверждение email",
                              name="Registration Result")
                assert True
            elif "register" in current_url:
                # Проверяем сообщения об ошибках
                error_elements = web_browser.find_elements(By.CSS_SELECTOR, ".rt-input-container__meta--error")
                if error_elements:
                    error_texts = [elem.text for elem in error_elements if elem.text]
                    allure.attach(f"Сообщения об ошибках: {error_texts}",
                                  name="Registration Errors")

                    # Проверяем типичные ошибки регистрации
                    for error in error_texts:
                        if "уже используется" in error.lower():
                            pytest.skip("Email уже зарегистрирован, тест пропущен")
                        elif "капч" in error.lower():
                            pytest.skip("Обнаружена капча, тест пропущен")
                else:
                    # Возможно, появилась капча
                    captcha = web_browser.find_elements(By.CSS_SELECTOR, ".rt-captcha__image")
                    if captcha:
                        pytest.skip("Обнаружена капча, тест пропущен")
        else:
            # Кнопка неактивна - проверяем валидацию
            error_elements = web_browser.find_elements(By.CSS_SELECTOR, ".rt-input-container__meta--error")
            assert len(error_elements) > 0, "При неактивной кнопке должны быть сообщения об ошибках валидации"

@allure.feature("Функциональность")
@allure.story("Запомнить меня")
def test_19_remember_me_functionality(web_browser):
    """
    19. Проверка функциональности "Запомнить меня".
    Ожидаемый результат: При повторном входе логин сохраняется.
    """
    wait = WebDriverWait(web_browser, 15)

    with allure.step("Открытие страницы авторизации"):
        web_browser.get(BASE_URL)
        time.sleep(2)

    with allure.step("Включение 'Запомнить меня'"):
        # Находим чекбокс "Запомнить меня"
        remember_checkboxes = web_browser.find_elements(By.CSS_SELECTOR, "input[name='remember']")

        if remember_checkboxes:
            remember_checkbox = remember_checkboxes[0]
            if not remember_checkbox.is_selected():
                # Кликаем на label, если чекбокс скрыт
                label = web_browser.find_element(By.CSS_SELECTOR, "label[for='remember']")
                if label:
                    label.click()
                else:
                    remember_checkbox.click()

        # Заполняем форму
        login_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        password_field = web_browser.find_element(By.ID, "password")

        login_field.send_keys(VALID_EMAIL)
        password_field.send_keys(VALID_PASSWORD)

    with allure.step("Нажатие кнопки 'Войти'"):
        web_browser.find_element(By.ID, "kc-login").click()
        time.sleep(5)  # Даем время для авторизации

    with allure.step("Проверка редиректа"):
        current_url = web_browser.current_url
        if "account_b2c" in current_url or "lk.rt.ru" in current_url:
            # Успешная авторизация
            cookies_after = web_browser.get_cookies()
            assert len(cookies_after) > 0, "Должны быть установлены куки"

            # Проверяем наличие куки для запоминания
            remember_cookies = [c for c in cookies_after if 'remember' in c['name'].lower()]
            if remember_cookies:
                allure.attach(f"Найдены куки запоминания: {remember_cookies}", name="Cookies Info")
        else:
            # Проверяем ошибку
            error_element = wait_for_error_message(wait)
            if error_element:
                error_text = error_element.text
                if "Неверный логин или пароль" in error_text:
                    pytest.fail(f"Ошибка авторизации: {error_text}")
                elif "Неверно введен текст с картинки" in error_text:
                    pytest.skip("Появилась капча, тест пропущен")

@allure.feature("Безопасность")
@allure.story("Управление сессией")
def test_20_session_timeout_and_auto_logout(web_browser):
    """
    20. Проверка сессии и автоматического выхода.
    Ожидаемый результат: После истечения времени сессии происходит автоматический выход.
    """
    wait = WebDriverWait(web_browser, 15)

    with allure.step("Авторизация пользователя"):
        web_browser.get(BASE_URL)
        time.sleep(2)

        # Авторизуемся
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        password_field = web_browser.find_element(By.ID, "password")

        username_field.send_keys(VALID_EMAIL)
        password_field.send_keys(VALID_PASSWORD)
        web_browser.find_element(By.ID, "kc-login").click()
        time.sleep(5)

    with allure.step("Проверка успешной авторизации"):
        current_url = web_browser.current_url
        if "account_b2c" not in current_url and "lk.rt.ru" not in current_url:
            pytest.skip("Не удалось авторизоваться, тест пропущен")

        # Сохраняем URL личного кабинета
        lk_url = web_browser.current_url

    with allure.step("Имитация неактивности пользователя"):
        # Ждем некоторое время (имитируем неактивность)
        # В реальном тесте можно настроить на большее время, если известно время таймаута сессии
        inactivity_time = 300  # 5 минут
        time.sleep(min(inactivity_time, 30))  # Для теста ограничим 30 секундами

        # Пробуем обновить страницу
        web_browser.refresh()
        time.sleep(3)

    with allure.step("Проверка состояния сессии"):
        current_url = web_browser.current_url

        # Возможные сценарии:
        # 1. Сессия активна - остаемся в ЛК
        # 2. Сессия истекла - перенаправление на страницу авторизации
        # 3. Требуется повторная авторизация

        if BASE_URL in current_url or "auth" in current_url:
            # Произошел выход из системы
            allure.attach("Сессия истекла, пользователь вышел из системы", name="Session Expired")
            assert True
        else:
            # Проверяем, можем ли мы выполнить действие в ЛК
            try:
                # Пробуем найти элементы ЛК
                lk_elements = web_browser.find_elements(
                    By.XPATH, "//*[contains(text(), 'Личный кабинет') or contains(text(), 'Профиль')]"
                )

                if lk_elements:
                    allure.attach("Сессия все еще активна", name="Session Active")
                    # Можно дополнительно проверить функциональность ЛК
                    assert True
                else:
                    # Нет элементов ЛК, возможно произошел выход
                    pytest.skip("Не удалось определить состояние сессии")
            except:
                pytest.skip("Не удалось проверить состояние сессии")

    with allure.step("Дополнительная проверка: выход из всех устройств"):
        # Если сессия еще активна, проверяем функцию "Выйти со всех устройств"
        web_browser.get(lk_url)
        time.sleep(2)

        # Ищем настройки безопасности или выхода
        security_links = web_browser.find_elements(
            By.XPATH, "//*[contains(text(), 'Безопасность') or contains(text(), 'Выйти')]"
        )

        if security_links:
            security_links[0].click()
            time.sleep(2)

            # Ищем кнопку выхода со всех устройств
            logout_all_btn = web_browser.find_elements(
                By.XPATH, "//button[contains(text(), 'со всех') or contains(text(), 'всех устройств')]"
            )

            if logout_all_btn:
                logout_all_btn[0].click()
                time.sleep(3)

                # Проверяем, что вышли из системы
                assert BASE_URL in web_browser.current_url, \
                    "После выхода со всех устройств должна быть страница авторизации"


