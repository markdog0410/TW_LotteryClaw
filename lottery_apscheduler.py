import requests
import sqlite3
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
import time
import threading
from datetime import datetime
import pytz

taipei_zone = pytz.timezone('Asia/Taipei')
taipei_time = datetime.now(taipei_zone)
year = taipei_time.year - 1911
month = taipei_time.month
current_time = str(year) + taipei_time.strftime("/%m/%d")


# 爬取當天開獎「威力彩」號碼
def get_super_lottery_history():
    print(f'{taipei_time}--> Start super lottery crawler process ...')
    try:
        ori_url: str = 'https://www.taiwanlottery.com.tw/lotto/superlotto638/history.aspx'
        res = requests.get(ori_url)

        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            payload = {'SuperLotto638Control_history1$chk': 'radYM',
                       'SuperLotto638Control_history1$dropYear': year,
                       'SuperLotto638Control_history1$dropMonth': month,
                       'SuperLotto638Control_history1$btnSubmit': '查詢',
                       '__VIEWSTATE': soup.select_one('#__VIEWSTATE')['value'],
                       '__VIEWSTATEGENERATOR': soup.select_one('#__VIEWSTATEGENERATOR'),
                       '__EVENTVALIDATION': soup.select_one('#__EVENTVALIDATION')['value']}

            search_url: str = 'https://www.taiwanlottery.com.tw/lotto/superlotto638/history.aspx'
            search_res = requests.post(search_url, data=payload)

            # connect to db
            # con = sqlite3.connect('lottery_data.db')
            # cur = con.cursor()
            search_soup = BeautifulSoup(search_res.text, 'html.parser')
            topic_title = search_soup.select_one('.font_red18.tx_md').text.strip()
            special_nums = search_soup.select('.td_w.font_red14b_center')
            normal_nums = search_soup.select('.td_w.font_black14b_center')
            # int(len(normal_nums) / 12)
            if len(special_nums) <= 0:
                print(f'{topic_title}--Not found match data on {year}/{month}.')
            for i in range(0, int(len(special_nums) / 2)):
                title = search_soup.select('#SuperLotto638Control_history1_dlQuery_DrawTerm_' + str(i))[0].text
                date = search_soup.select('#SuperLotto638Control_history1_dlQuery_Date_' + str(i))[0].text
                if date == current_time:
                    num1 = search_soup.select('#SuperLotto638Control_history1_dlQuery_No1_' + str(i))[0].text
                    num2 = search_soup.select('#SuperLotto638Control_history1_dlQuery_No2_' + str(i))[0].text
                    num3 = search_soup.select('#SuperLotto638Control_history1_dlQuery_No3_' + str(i))[0].text
                    num4 = search_soup.select('#SuperLotto638Control_history1_dlQuery_No4_' + str(i))[0].text
                    num5 = search_soup.select('#SuperLotto638Control_history1_dlQuery_No5_' + str(i))[0].text
                    num6 = search_soup.select('#SuperLotto638Control_history1_dlQuery_No6_' + str(i))[0].text
                    num7 = search_soup.select('#SuperLotto638Control_history1_dlQuery_No7_' + str(i))[0].text
                    data = [title, date, num1, num2, num3, num4, num5, num6, num7]
                    print(f'{topic_title}--', data)
                    # cur.execute("INSERT INTO SUPER_LOTTERY VALUES (?,?,?,?,?,?,?,?,?)",
                    #             (title, date, num1, num2, num3, num4, num5, num6, num7))
                    # con.commit()

        else:
            return f'{taipei_time}--> Failed to get super lottery data.'
    except ConnectionError as ce:
        print(f'Super lottery connection error: {ce}')
    except TimeoutError as te:
        print(f'Super lottery timeout error: {te}')
    except Exception as e:
        print(f'Super lottery other error: {e}')
    finally:
        print(f'{taipei_time}--> Finish super lottery crawler process ...')
        # cur.close()
        # con.close()


# 爬取當天開獎「大樂透」號碼
def get_lotto_lottery_history():
    print(f'{taipei_time}--> Start lotto lottery crawler process ...')
    try:
        url: str = 'https://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx'
        res = requests.get(url)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            payload = {'Lotto649Control_history$chk': 'radYM',
                       'Lotto649Control_history$dropYear': year,
                       'Lotto649Control_history$dropMonth': month,
                       'Lotto649Control_history$btnSubmit': '查詢',
                       '__VIEWSTATE': soup.select_one('#__VIEWSTATE')['value'],
                       '__VIEWSTATEGENERATOR': soup.select_one('#__VIEWSTATEGENERATOR'),
                       '__EVENTVALIDATION': soup.select_one('#__EVENTVALIDATION')['value']}
            url_post: str = 'https://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx'
            res_post = requests.post(url_post, data=payload)

            # connect to db
            # con = sqlite3.connect('lottery_data.db')
            # cur = con.cursor()
            res_post_soup = BeautifulSoup(res_post.text, 'html.parser')
            special_nums = res_post_soup.select('.td_w.font_red14b_center')
            normal_nums = res_post_soup.select('.td_w.font_black14b_center')
            topic_title = res_post_soup.select_one('.font_red18.tx_md').text.strip()

            if len(special_nums) <= 0:
                print(f'{topic_title}--Not found match data on {year}/{month}.')
            for i in range(0, int(len(special_nums) / 2)):
                title = res_post_soup.select('#Lotto649Control_history_dlQuery_L649_DrawTerm_' + str(i))[0].text
                date = res_post_soup.select('#Lotto649Control_history_dlQuery_L649_DDate_' + str(i))[0].text
                if date == current_time:
                    num1 = res_post_soup.select('#Lotto649Control_history_dlQuery_No1_' + str(i))[0].text
                    num2 = res_post_soup.select('#Lotto649Control_history_dlQuery_No2_' + str(i))[0].text
                    num3 = res_post_soup.select('#Lotto649Control_history_dlQuery_No3_' + str(i))[0].text
                    num4 = res_post_soup.select('#Lotto649Control_history_dlQuery_No4_' + str(i))[0].text
                    num5 = res_post_soup.select('#Lotto649Control_history_dlQuery_No5_' + str(i))[0].text
                    num6 = res_post_soup.select('#Lotto649Control_history_dlQuery_No6_' + str(i))[0].text
                    numS = res_post_soup.select('#Lotto649Control_history_dlQuery_SNo_' + str(i))[0].text
                    data = [title, date, num1, num2, num3, num4, num5, num6, numS]
                    print(f'{topic_title}--', data)
                    # cur.execute("INSERT INTO LOTTO_LOTTERY VALUES (?,?,?,?,?,?,?,?)",
                    #             (title, date, num1, num2, num3, num4, num5, num6))
                    # con.commit()

        else:
            return f'{taipei_time}--> Failed to get lotto lottery data.'
    except ConnectionError as ce:
        print(f'Lotto lottery connection error: {ce}')
    except TimeoutError as te:
        print(f'Lotto lottery timeout error: {te}')
    except Exception as e:
        print(f'Lotto lottery other error: {e}')
    finally:
        print(f'{taipei_time}--> Finish lotto lottery crawler process ...')
        # cur.close()
        # con.close()


# 爬取當天開獎「今彩539」號碼
def get_539_lottery_history():
    print(f'{taipei_time}--> Start 539 lotto lottery crawler process ...')
    url: str = 'https://www.taiwanlottery.com.tw/lotto/DailyCash/history.aspx'
    res = requests.get(url)
    try:
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            # con = sqlite3.connect('lottery_data.db')
            # cur = con.cursor()
            payload = {'D539Control_history1$chk': 'radYM',
                       'D539Control_history1$dropYear': year,
                       'D539Control_history1$dropMonth': month,
                       'D539Control_history1$btnSubmit': '查詢',
                       '__VIEWSTATE': soup.select_one('#__VIEWSTATE')['value'],
                       '__VIEWSTATEGENERATOR': soup.select_one('#__VIEWSTATEGENERATOR'),
                       '__EVENTVALIDATION': soup.select_one('#__EVENTVALIDATION')['value']}
            url_post: str = 'https://www.taiwanlottery.com.tw/lotto/DailyCash/history.aspx'
            ori_res = requests.post(url_post, data=payload)
            res_soup = BeautifulSoup(ori_res.text, 'html.parser')
            topic_title = res_soup.select_one('.font_red18.tx_md').text.strip()
            count = int(len(res_soup.select('.table_gre.td_hm')) + len(res_soup.select('.table_org.td_hm')))
            if count <= 0:
                print(f'{topic_title}--Not found match data on {year}/{month}.')
            for i in range(0, count):
                title = res_soup.select('#D539Control_history1_dlQuery_D539_DrawTerm_' + str(i))[0].text
                date = res_soup.select('#D539Control_history1_dlQuery_D539_DDate_' + str(i))[0].text
                if date == current_time:
                    num1 = res_soup.select('#D539Control_history1_dlQuery_No1_' + str(i))[0].text
                    num2 = res_soup.select('#D539Control_history1_dlQuery_No2_' + str(i))[0].text
                    num3 = res_soup.select('#D539Control_history1_dlQuery_No3_' + str(i))[0].text
                    num4 = res_soup.select('#D539Control_history1_dlQuery_No4_' + str(i))[0].text
                    num5 = res_soup.select('#D539Control_history1_dlQuery_No5_' + str(i))[0].text
                    data = [title, date, num1, num2, num3, num4, num5]
                    print(f'{topic_title}--', data)
                    # cur.execute("INSERT INTO LOTTERY_539 VALUES (?,?,?,?,?,?,?)",
                    #             (title, date, num1, num2, num3, num4, num5))
                    # con.commit()
        else:
            return f'{taipei_time}--> Failed to get lotto 539 lottery data.'
    except ConnectionError as ce:
        print(f'Lotto539 lottery connection error: {ce}')
    except TimeoutError as te:
        print(f'Lotto539 lottery timeout error: {te}')
    except Exception as e:
        print(f'Lotto539 lottery other error: {e}')
    finally:
        print(f'{taipei_time}--> Finish 539 lotto lottery crawler process ...')
        # cur.close()
        # con.close()


# 爬取當天開獎「雙贏彩」號碼
def get_winwin_lottery_history():
    print(f'{taipei_time}--> Start winwin lottery crawler process ...')
    url: str = 'https://www.taiwanlottery.com.tw/lotto/Lotto1224/history.aspx'
    res = requests.get(url)
    try:
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            payload = {'Lotto1224Control_history$chk': 'radYM',
                       'Lotto1224Control_history$dropYear': year,
                       'Lotto1224Control_history$dropMonth': month,
                       'Lotto1224Control_history$btnSubmit': '查詢',
                       '__VIEWSTATE': soup.select_one('#__VIEWSTATE')['value'],
                       '__VIEWSTATEGENERATOR': soup.select_one('#__VIEWSTATEGENERATOR'),
                       '__EVENTVALIDATION': soup.select_one('#__EVENTVALIDATION')['value']}
            url_post: str = 'https://www.taiwanlottery.com.tw/lotto/Lotto1224/history.aspx'
            ori_res = requests.post(url_post, data=payload)
            res_soup = BeautifulSoup(ori_res.text, 'html.parser')
            # con = sqlite3.connect('lottery_data.db')
            # cur = con.cursor()
            topic_title = res_soup.select_one('.font_red18.tx_md').text.strip()
            count = int(len(res_soup.select('.table_gre')) + len(res_soup.select('.table_org')))
            if count <= 0:
                print(f'{topic_title}--Not found match data on {year}/{month}.')
            for i in range(0, count):
                title = res_soup.select('#Lotto1224Control_history_dlQuery_Lotto1224_DrawTerm_' + str(i))[0].text
                date = res_soup.select('#Lotto1224Control_history_dlQuery_Lotto1224_DDate_' + str(i))[0].text
                if date == current_time:
                    num1 = res_soup.select('#Lotto1224Control_history_dlQuery_No1_' + str(i))[0].text.strip()
                    num2 = res_soup.select('#Lotto1224Control_history_dlQuery_No2_' + str(i))[0].text.strip()
                    num3 = res_soup.select('#Lotto1224Control_history_dlQuery_No3_' + str(i))[0].text.strip()
                    num4 = res_soup.select('#Lotto1224Control_history_dlQuery_No4_' + str(i))[0].text.strip()
                    num5 = res_soup.select('#Lotto1224Control_history_dlQuery_No5_' + str(i))[0].text.strip()
                    num6 = res_soup.select('#Lotto1224Control_history_dlQuery_No6_' + str(i))[0].text.strip()
                    num7 = res_soup.select('#Lotto1224Control_history_dlQuery_No7_' + str(i))[0].text.strip()
                    num8 = res_soup.select('#Lotto1224Control_history_dlQuery_No8_' + str(i))[0].text.strip()
                    num9 = res_soup.select('#Lotto1224Control_history_dlQuery_No9_' + str(i))[0].text.strip()
                    num10 = res_soup.select('#Lotto1224Control_history_dlQuery_No10_' + str(i))[0].text.strip()
                    num11 = res_soup.select('#Lotto1224Control_history_dlQuery_No11_' + str(i))[0].text.strip()
                    num12 = res_soup.select('#Lotto1224Control_history_dlQuery_No12_' + str(i))[0].text.strip()
                    data = [title, date, num1, num2, num3, num4, num5, num6, num7, num8, num9, num10, num11, num12]
                    print(f'{topic_title}--', data)
                    # cur.execute("INSERT INTO WINWIN_LOTTERY VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    #             (
                    #                 title, date, num1, num2, num3, num4, num5, num6, num7, num8, num9, num10, num11,
                    #                 num12))
                    # con.commit()
        else:
            return f'{taipei_time}--> Failed to get winwin lottery data.'
    except ConnectionError as ce:
        print(f'winwin lottery connection error: {ce}')
    except TimeoutError as te:
        print(f'winwin lottery timeout error: {te}')
    except Exception as e:
        print(f'winwin lottery other error: {e}')
    finally:
        print(f'{taipei_time}--> Finish winwin lottery crawler process ...')
        # cur.close()
        # con.close()


# 爬取當天開獎「3星彩」號碼
def get_3star_lottery_history():
    print(f'{taipei_time}--> Start 3star lottery crawler process ...')
    url: str = 'https://www.taiwanlottery.com.tw/Lotto/3D/history.aspx'
    res = requests.get(url)
    try:
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            payload = {'L3DControl_history1$chk': 'radYM',
                       'L3DControl_history1$dropYear': year,
                       'L3DControl_history1$dropMonth': month,
                       'L3DControl_history1$btnSubmit': '查詢',
                       '__VIEWSTATE': soup.select_one('#__VIEWSTATE')['value'],
                       '__VIEWSTATEGENERATOR': soup.select_one('#__VIEWSTATEGENERATOR'),
                       '__EVENTVALIDATION': soup.select_one('#__EVENTVALIDATION')['value']}
            url_post: str = 'https://www.taiwanlottery.com.tw/Lotto/3D/history.aspx'
            ori_res = requests.post(url_post, data=payload)
            res_soup = BeautifulSoup(ori_res.text, 'html.parser')

            # con = sqlite3.connect('lottery_data.db')
            # cur = con.cursor()
            topic_title = res_soup.select_one('.font_red18.tx_md').text.strip()
            gre = res_soup.find_all('table', class_='table_gre')
            org = res_soup.find_all('table', class_='table_org')

            for i in range(0, int(len(gre))):
                gre_all_elements = gre[i].find_all('td', class_='td_w')
                title = gre_all_elements[0].text.strip()
                date = gre_all_elements[1].text.strip()[2:]
                if date == current_time:
                    nums = gre_all_elements[2].find_all('span', class_='td_w font_black14b_center')
                    num1 = nums[0].text.strip()
                    num2 = nums[1].text.strip()
                    num3 = nums[2].text.strip()
                    data = [title, date, num1, num2, num3]
                    print(f'{topic_title}--', data)
                    # cur.execute("INSERT INTO LOTTERY_3STAR VALUES (?,?,?,?,?)",
                    #             (title, date, num1, num2, num3))
                    # con.commit()
            for i in range(0, int(len(org))):
                org_all_elements = org[i].find_all('td', class_='td_w')
                title = org_all_elements[0].text.strip()
                date = org_all_elements[1].text.strip()[2:]
                if date == current_time:
                    nums = org_all_elements[2].find_all('span', class_='td_w font_black14b_center')
                    num1 = nums[0].text.strip()
                    num2 = nums[1].text.strip()
                    num3 = nums[2].text.strip()
                    data = [title, date, num1, num2, num3]
                    print(f'{topic_title}--', data)
                    # cur.execute("INSERT INTO LOTTERY_3STAR VALUES (?,?,?,?,?)",
                    #             (title, date, num1, num2, num3))
                    # con.commit()
        else:
            return f'{taipei_time}--> Failed to get 3star lottery data.'
    except ConnectionError as ce:
        print(f'3star lottery connection error: {ce}')
    except TimeoutError as te:
        print(f'3star lottery timeout error: {te}')
    except Exception as e:
        print(f'3star lottery other error: {e}')
    finally:
        print(f'{taipei_time}--> Finish 3star lottery crawler process ...')
        # cur.close()
        # con.close()


# 爬取當天開獎「4星彩」號碼
def get_4star_lottery_history():
    print(f'{taipei_time}--> Start 4star lottery crawler process ...')
    url: str = 'https://www.taiwanlottery.com.tw/Lotto/4D/history.aspx'
    res = requests.get(url)
    try:
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            payload = {'L4DControl_history1$chk': 'radYM',
                       'L4DControl_history1$dropYear': year,
                       'L4DControl_history1$dropMonth': month,
                       'L4DControl_history1$btnSubmit': '查詢',
                       '__VIEWSTATE': soup.select_one('#__VIEWSTATE')['value'],
                       '__VIEWSTATEGENERATOR': soup.select_one('#__VIEWSTATEGENERATOR'),
                       '__EVENTVALIDATION': soup.select_one('#__EVENTVALIDATION')['value']}
            url_post: str = 'https://www.taiwanlottery.com.tw/Lotto/4D/history.aspx'
            ori_res = requests.post(url_post, data=payload)
            res_soup = BeautifulSoup(ori_res.text, 'html.parser')
            # con = sqlite3.connect('lottery_data.db')
            # cur = con.cursor()
            topic_title = res_soup.select_one('.font_red18.tx_md').text.strip()
            gre = res_soup.find_all('table', class_='table_gre')
            org = res_soup.find_all('table', class_='table_org')

            for i in range(0, int(len(gre))):
                gre_all_elements = gre[i].find_all('td', class_='td_w')
                title = gre_all_elements[0].text.strip()
                date = gre_all_elements[1].text.strip()[2:]
                if date == current_time:
                    nums = gre_all_elements[2].find_all('span', class_='td_w')
                    num1 = nums[0].text.strip()
                    num2 = nums[1].text.strip()
                    num3 = nums[2].text.strip()
                    num4 = nums[3].text.strip()
                    data = [title, date, num1, num2, num3, num4]
                    print(f'{topic_title}--', data)
                    # cur.execute("INSERT INTO LOTTERY_4STAR VALUES (?,?,?,?,?,?)",
                    #             (title, date, num1, num2, num3, num4))
                    # con.commit()
            for i in range(0, int(len(org))):
                org_all_elements = org[i].find_all('td', class_='td_w')
                title = org_all_elements[0].text.strip()
                date = org_all_elements[1].text.strip()[2:]
                if date == current_time:
                    nums = org_all_elements[2].find_all('span', class_='td_w')
                    num1 = nums[0].text.strip()
                    num2 = nums[1].text.strip()
                    num3 = nums[2].text.strip()
                    num4 = nums[3].text.strip()
                    data = [title, date, num1, num2, num3, num4]
                    print(f'{topic_title}--', data)
                    # cur.execute("INSERT INTO LOTTERY_4STAR VALUES (?,?,?,?,?,?)",
                    #             (title, date, num1, num2, num3, num4))
                    # con.commit()
    except ConnectionError as ce:
        print(f'4star lottery connection error: {ce}')
    except TimeoutError as te:
        print(f'4star lottery timeout error: {te}')
    except Exception as e:
        print(f'4star lottery other error: {e}')
    finally:
        print(f'{taipei_time}--> Finish 4star lottery crawler process ...')
        # cur.close()
        # con.close()


if __name__ == '__main__':
    get_super_lottery_history()
