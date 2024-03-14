from DrissionPage import ChromiumPage
from DrissionPage._elements.chromium_element import ChromiumElement
from DrissionPage._pages.chromium_frame import ChromiumFrame
import DrissionPage.common
from printqrcode import print_qrcode
import requests

BASE_URL = 'https://work.weixin.qq.com'
CONFIG_URL = BASE_URL + '/wework_admin/frame'
LOGIN_URL = BASE_URL + '/wework_admin/loginpage_wx'
APP_NAME = 'NASTools'


def get_login_qrcode(login_frame: ChromiumFrame) -> str:
    login_qr_code: ChromiumElement = login_frame.eles('tag:img')[0]
    return str(login_qr_code.attr('src'))


def get_now_ip(retry_times: int = 3) -> str | None:
    times = 0
    ret = None
    while retry_times > times:
        try:
            respon = requests.get('https://4.ipw.cn')
            if respon.status_code == 200:
                ret = respon.text
                break
        except:
            pass
        times += 1
    return ret


def combined_ips(old_ips: str, new_ip: str) -> str:
    ips = old_ips.split(';')
    if new_ip in ips:
        return old_ips
    ips.append(new_ip)
    return ';'.join(ips)


def login_handler(page: ChromiumPage) -> bool:
    page.get(LOGIN_URL)
    page.wait.load_start()
    if page.url == CONFIG_URL:
        return True

    login_frame: ChromiumFrame = page.get_frame(0)
    kwargs = {
        'login_frame': login_frame
    }
    DrissionPage.common.wait_until(get_login_qrcode, kwargs, timeout=60)

    login_qr_code_url = BASE_URL + \
        get_login_qrcode(login_frame)
    print(login_qr_code_url)
    print_qrcode(login_qr_code_url)
    return page.wait.url_change(CONFIG_URL, timeout=60)


def main() -> None:
    page = ChromiumPage()

    login_handler(page)

    # After Login
    menu_apps_btn = page.ele('#menu_apps')
    menu_apps_btn.click()

    all_apps_div = page.ele('@class=app_index_section_cnt js_openapi_block')
    print(all_apps_div)
    all_apps = all_apps_div.eles('@class=app_index_item app_index_item_Open')
    print(all_apps)
    for apps in all_apps:
        app_name = apps.ele('@class=app_index_item_title ').text
        if app_name == APP_NAME:
            apps.click()
            break

    all_app_card = page.eles('@class=app_card apiApp_mod_card')
    setting_btn = all_app_card[-1].ele(
        '@class=app_card_operate app_card_operate_Init js_show_ipConfig_dialog')
    setting_btn.click()
    ip_textarea = page.ele('@class=js_ipConfig_textarea')
    old_ips = ip_textarea.value

    now_ip = get_now_ip()
    new_ips = None
    if now_ip:
        new_ips = combined_ips(str(old_ips), now_ip)

    ip_textarea.input(new_ips)

    submit_btn = page.ele('@d_ck=submit')
    submit_btn.click()


if __name__ == '__main__':
    main()
