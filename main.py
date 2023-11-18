import requests
import time
import logging
import urllib3

urllib3.disable_warnings()

# 配置日志输出格式
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='call.log',
    encoding='utf-8'
)

stock_url = "https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json"
stock_data_previous = {}  # 初始值为 None，表示第一次访问 API
stock_param = {"pid": "-1", "category": "1", "size": "1000"}
user_dict = {
    "轮回666": "8282709675",
    "薛定谔的牛": "3639429204",
    "复旦橙子橙": "3697768583",
    "Moss_LD": "3316855169",
    # "猫猫": "9696783696"
}

cube_url = "https://xueqiu.com/cubes/rebalancing/history.json"
cube_data_previous = {}  # 第一次访问组合API
cube_param = {"count": 20, "page": 1}
cube_dict = {
    # "薛定谔的牛": "ZH3221865",
    # "行中衡": "ZH847468",
    "轮回666": "ZH3292517",
    "花盆君": "ZH3125504",
    "暮烟风雨": "ZH1739131",
    "徐富贵冲冲冲": "ZH3165213",
    "麻省锂公": "ZH3295255"
}

session = requests.Session()
session.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Cookie': "device_id=1cff0e058c5b49745650715ce680107c; bid=b300e536504d14d4617e5581f6923929_ldmhd58f; s=dw1px0n3bj; __utmz=1.1675305045.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_fe218c11eab60b6ab1b6f84fb38bcc4a=1683339616; u=9696783696; xq_is_login=1; cookiesu=731692581296810; xq_a_token=c83155692beaa7d4883a765636d1820636e2e19a; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjk2OTY3ODM2OTYsImlzcyI6InVjIiwiZXhwIjoxNzAyNTIzNTg2LCJjdG0iOjE2OTk5MzE1ODYyMzIsImNpZCI6ImQ5ZDBuNEFadXAifQ.NNbk4ztEn-D7Xc_GsqwKfAb3VpiIybisFLxAg1A_0TUlifb21yIVYqXhH4Dl6iMnhDIy8MxudSXrCfiEExIiypftcrEbTgQqBVFNTAmT0o0B_SoQ0NPgCVeDUBEMWt9jqjO5di2GeW8idJJuoa9bgCaFqzPxCUDjGzWMEnWaQTSLGU5ejJ8VEZ64nG1y8M8NnYS6FJz5o91x4sf2S5Y9BNZqhNo-GgMzRgCVMPWlbs5DorE3dBfxlhy05rQKPJVE2YVA6Y8-xS59pJ2NdT8Boa5r6-qP6z_YiESyop8yWs8N2r4aOJ_MEj3Qe1d5LgBMmle1qrQ8M4fujMhmZzyjOQ; xq_r_token=dd62bfbb74e0b8a343893a1d3c0d0f411fe5e6f6; xqat=c83155692beaa7d4883a765636d1820636e2e19a; Hm_lvt_1db88642e346389874251b5a1eded6e3=1698824552,1698919905,1699839073,1699955455; snbim_minify=true; __utmc=1; acw_tc=2760779917002959251645231e7cd1682e0f39fb3c9868ae98167321a03569; is_overseas=0; __utma=1.630488574.1675305045.1700291913.1700295931.188; __utmt=1; __utmb=1.2.10.1700295931; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1700295934",
    'cache-control': "no-cache",
}

youdao_url = "https://note.youdao.com/yws/api/personal/history"

youdao_session = requests.Session()
youdao_session.headers = {
    'Accept': "*/*",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Connection': "keep-alive",
    'Cookie': "__yadk_uid=Fnn7JXj31NI95Cv9lfcZTUJ3Y9BnPR6x; OUTFOX_SEARCH_USER_ID_NCOO=469366436.873141; OUTFOX_SEARCH_USER_ID=1647686822@120.79.41.22; YD00053006227227%3AWM_NI=VcVUxlmY4ryRt4%2BbNxlye7PYnMBAYQQk%2Feze685kM1vgglte2YIpSXJ627ysvlNKh4c6xO6gnZ5BrDgHyGpA%2FU%2F9Myrj53lJkWGD98aI%2BUuIgBs2c0qLX5Y4XuRp%2BgQtalY%3D; YD00053006227227%3AWM_NIKE=9ca17ae2e6ffcda170e2e6ee82d1688d91a89bcc4891ac8fa7c15f938e9bacc461b2a8ffb9fc5ab4e78ed9db2af0fea7c3b92a96bd9ab6fb68af87fc93fc5ab8ece583cd74b0a7abd8d353ae938ea2dc5b93b5e186f96ff6e8fb8cd03bb6b9a98df76ff2878791d2548aeafed8fc79b6b482aceb40a1eab8b0b56dae86fba3f150a598b7a8f34bed8be1dad073b2b6fbd4ef42a98989a5bc34a397e5b6f843a59ebdd3e23cb39498d6dc409cab9e91aa6d93acaf8ddc37e2a3; YD00053006227227%3AWM_TID=jqIrC2gsy1BFVFRVBFbFk6klCnEtoQsT; YNOTE_SESS=v2|oOrWsBkmhVzl64YGOMqBRquP4qynHpu0PLOLqFhLUG0JBnHwLhfpZ0TBkfJLhMqz0YGkfTZ0LYl06L0fJzhMO5RPynLwuk4P4R; YNOTE_PERS=v2|wxoa||YNOTE||web||-1||1691750805705||120.79.41.22||weixinobU7VjrefwDLtv4loMygd5lZGap8||Jyhfqu0MJF0OEkLOA0fJB0wK0fQFOLUE0TFPMY5nH6FRezhMeukMPu0JyPLOERHJu06yOMkmhLPuRwZhMgL6MeLR; YNOTE_CSTK=2lIUbj09; YNOTE_LOGIN=5||1698411769930",
    'Referer': "https://note.youdao.com/bulbhistory/?noteid=/WEBa03d21f04c4af109d348ae44889f038c&myShare=true&shareKey=4cb781117d9735394a4073897c491a94",
    'Sec-Fetch-Dest': "empty",
    'Sec-Fetch-Mode': "cors",
    'Sec-Fetch-Site': "same-origin",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    'X-Requested-With': "XMLHttpRequest",
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': "?0",
    'sec-ch-ua-platform': '"Windows"',
    'cache-control': "no-cache"
}
youdao_session.params = {"method": "listHistoryByPage", "sev": "j1", "fileId": "WEBa03d21f04c4af109d348ae44889f038c",
                         "myShare": "true", "pageNo": "1", "pageSize": "16", "cstk": "2lIUbj09"}
youdao_version_previous = 0

while True:
    for name, uid in user_dict.items():
        stock_param['uid'] = uid

        response = session.get(stock_url, params=stock_param)
        if response.status_code == 200 and response.json()['data']:
            data_current = response.json()['data']['stocks']

            # 第一次访问 API，保存数据到变量中
            if uid not in stock_data_previous:
                stock_data_previous[uid] = data_current
                logging.info(f"【{name}】股票数据初始化成功")

            # 非第一次访问 API，比较数据，找出新增和删除的股票信息
            else:
                symbols_previous = set(stock['symbol'] for stock in stock_data_previous[uid])
                symbols_current = set(stock['symbol'] for stock in data_current)

                new_symbols = symbols_current - symbols_previous
                removed_symbols = symbols_previous - symbols_current

                if new_symbols:
                    for stock in data_current:
                        if stock['symbol'] in new_symbols:
                            msg = f"【{name}】新增股票信息: " + stock['symbol'] + ":" + stock['name']
                            logging.info(msg)
                            push_deer_url = f"https://api2.pushdeer.com/message/push?pushkey=PDU23078Tvl3ShDVG3aYDrCO2Eqf9azouteT6F13q&text={msg}"
                            push_deer_url2 = f"https://api2.pushdeer.com/message/push?pushkey=PDU26203TfKUwbR46v1cDQpcHcVh9Ahw5heaMcgkR&text={msg}"
                            push_deer_url3 = f"https://api2.pushdeer.com/message/push?pushkey=PDU25746TNdVSyL1JMuocwUTR9OQGiTyzDWrv2k0B&text={msg}"
                            requests.get(push_deer_url)
                            requests.get(push_deer_url2)
                            requests.get(push_deer_url3)

                if removed_symbols:
                    for stock in stock_data_previous[uid]:
                        if stock['symbol'] in removed_symbols:
                            msg = f"【{name}】删除股票信息: " + stock['symbol'] + ":" + stock['name']
                            logging.info(msg)
                            push_deer_url2 = f"https://api2.pushdeer.com/message/push?pushkey=PDU26203TfKUwbR46v1cDQpcHcVh9Ahw5heaMcgkR&text={msg}"
                            requests.get(push_deer_url2)

                # 更新保存的数据为当前数据
                stock_data_previous[uid] = data_current

        else:
            logging.error("自选接口访问失败")
            logging.error(response.content.decode())

    for name, cube_id in cube_dict.items():
        cube_param['cube_symbol'] = cube_id

        response = session.get(cube_url, params=cube_param)
        if response.status_code == 200 and response.json()['list']:
            data_current = response.json()['list'][0]
            cube_history = response.json()['list']
            # 第一次访问 API，保存数据到变量中
            if cube_id not in cube_data_previous:
                cube_data_previous[cube_id] = data_current['id']
                logging.info(f"【{name}]组合数据初始化成功")
            # 遍历检查数据，打印组合新调仓信息
            else:
                for cube in cube_history:
                    if cube['id'] != cube_data_previous[cube_id]:
                        for one in cube['rebalancing_histories']:
                            msg = f"【{name}】组合调仓信息: {one['stock_symbol']}:{one['stock_name']}:{one['price']}: {one['prev_weight_adjusted'] if one['prev_weight_adjusted'] else 0}%->{one['target_weight']}%"
                            logging.info(msg)
                            push_deer_url = f"https://api2.pushdeer.com/message/push?pushkey=PDU23078Tvl3ShDVG3aYDrCO2Eqf9azouteT6F13q&text={msg}"
                            push_deer_url2 = f"https://api2.pushdeer.com/message/push?pushkey=PDU26203TfKUwbR46v1cDQpcHcVh9Ahw5heaMcgkR&text={msg}"
                            push_deer_url3 = f"https://api2.pushdeer.com/message/push?pushkey=PDU25746TNdVSyL1JMuocwUTR9OQGiTyzDWrv2k0B&text={msg}"
                            requests.get(push_deer_url)
                            if cube_id != "ZH3125504" and cube_id != "ZH3295255":
                                requests.get(push_deer_url2)
                                requests.get(push_deer_url3)

                    else:
                        cube_data_previous[cube_id] = data_current['id']
                        break
        else:
            logging.error("组合接口访问失败")
            logging.error(response.content.decode())

    # 获取有道云笔记更新内容
    # response = youdao_session.get(youdao_url)
    # if response.status_code == 200 and response.json()['list']:
    #     data_current = response.json()['list'][0]
    #     if youdao_version_previous == 0:
    #         youdao_version_previous = data_current['version']
    #         logging.info(f"毒老师有道文档初始化version成功:【{youdao_version_previous}】")
    #     else:
    #         if data_current['version'] > youdao_version_previous:
    #             youdao_version_previous = data_current['version']
    #             msg = f"【{youdao_version_previous}】毒老师有道文档更新了"
    #             logging.info(msg)
    #             push_deer_url = f"https://api2.pushdeer.com/message/push?pushkey=PDU23078Tvl3ShDVG3aYDrCO2Eqf9azouteT6F13q&text={msg}"
    #             push_deer_url2 = f"https://api2.pushdeer.com/message/push?pushkey=PDU26203TfKUwbR46v1cDQpcHcVh9Ahw5heaMcgkR&text={msg}"
    #             requests.get(push_deer_url)
    #             requests.get(push_deer_url2)
    #
    # else:
    #     logging.error("有道文档接口访问失败")
    #     logging.error(response.content.decode())

    # 等待一段时间后再次访问 API
    time.sleep(30)
