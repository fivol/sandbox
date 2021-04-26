from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import requests


def check_works(driver):
    """Делает проверки, то драйвер валиден и готов и эксплуатации"""
    print('BEGIN CHECK')
    # Проверяем что на 4444 порту вообще работает selenium
    driver.get('https://google.com')
    # driver.save_screenshot('google.png')
    driver.get("http://www.python.org")
    # driver.save_screenshot('files/screenshot.png')
    assert "Python" in driver.title
    elem = driver.find_element_by_name("q")
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    driver.close()
    print('DONE')


if __name__ == '__main__':
    print('RUN MAIN')
    resp = requests.get('http://localhost:4444')
    print("REQUEST STATUS", resp.status_code)
    exit(0)
    resp.raise_for_status()
    print('ACCESS DOCKER SELENOID')
    chrome_options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'javascript': 2,
                                                        'plugins': 2, 'popups': 2, 'geolocation': 2,
                                                        'css': 2,
                                                        'notifications': 2, 'auto_select_certificate': 2,
                                                        # 'fullscreen': 3,
                                                        'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                                                        'media_stream_mic': 2, 'media_stream_camera': 2,
                                                        'protocol_handlers': 2,
                                                        'ppapi_broker': 2, 'automatic_downloads': 2,
                                                        'midi_sysex': 2,
                                                        'push_messaging': 2, 'ssl_cert_decisions': 2,
                                                        'metro_switch_to_desktop': 2,
                                                        'protected_media_identifier': 2, 'app_banner': 2,
                                                        'site_engagement': 2,
                                                        'durable_storage': 2}}
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--headless')
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Remote(
        command_executor='http://selenoid:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME,
    )

    check_works(driver)
