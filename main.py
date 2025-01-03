import requests
import time
import logging
import urllib3
from requests.exceptions import RequestException

urllib3.disable_warnings()

# 配置日志输出格式
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='call.log',
    #    encoding='utf-8'
)

stock_url = "https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json"
stock_data_previous = {}  # 初始值为 None，表示第一次访问 API
stock_param = {"pid": "-1", "category": "1", "size": "1000"}
user_dict = {
    "轮回666": "8282709675",
    # "薛定谔的牛": "3639429204",
    "复旦橙子橙": "3697768583",
    "Moss_LD": "3316855169",
    "robo": "5712584562",
    "只胡清一色": "7013173046",
    # "猫猫": "9696783696"
}

cube_url = "https://xueqiu.com/cubes/rebalancing/history.json"
cube_data_previous = {}  # 第一次访问组合API
cube_param = {"count": 20, "page": 1}
cube_dict = {
    "轮回666": "ZH3292517",
    "花盆君": "ZH3377835",
    "花盆君": "ZH3394904",
    "暮烟风雨": "ZH1739131",
    "只胡清一色": "ZH3337506",
    "板块领涨龙": "ZH3335166",
}

# 全局变量，存储文章标题
global_titles = {}

# 微信公众号信息
gzh = {
    "猫比刀": "Mzg2NzcxMjE1NA==",
    # 可以添加更多的公众号
}

# 请求头
Cookie = "appmsglist_action_3885240684=card; ptcz=af37a65e6383dd175ad7d2e3d4a875121205540c385fc1ba21eea797cd3b96d8; pgv_pvid=3868357759; iip=0; _qimei_q36=; _qimei_h38=fded8356a3fe8fbc1c50b5ff02000000018102; RK=GpUgQRyXXN; pac_uid=0_97f4890689ccc; qq_domain_video_guid_verify=7f9421e3f68bb889; eas_sid=k1q7q2J0K5E7L5E957y9U3J0k7; suid=user_0_97f4890689ccc; _uetvid=c428f2e07ae911ef812d9b383187bd74; wxuin=35887555214419; ua_id=ZPCBxBjPLIA0hSQPAAAAAC5kkNXluE1p-C5WII0MjYM=; _clck=rbn39m|1|fs9|0; uuid=49b80a743576e4a6dabbc5f83c387c16; slave_bizuin=3885240684; rand_info=CAESIJVC7zIweyKc6S1alMXWN1zNA0p5iRf0Vr3YquUSaUf5; xid=1ed81e170374f1021465256db13b62eb; mm_lang=zh_CN; slave_user=gh_ded3be315838; slave_sid=RUM0eVhtbzFlWFFPd2s0XzFUeWdVMGoxbVJYcVN3bExjcDduTFpqYVNGWV9xaTZkQ0JmNW1Rd2ZHTDZIZmhmaml3YVN6WmdsQWRsdVRDVmdieVNvZFlqR18wZk1SOHdOWlhrNGFkbGd2SHNGUW5iVEN3bm9VVmlqN1pNb3ozdzJYWjZlamlrRmZSU1NwdFBW; bizuin=3885240684; data_bizuin=3885240684; data_ticket=K5hfq3E3ki1KRFkV0U2pjjRiFw1KFsDbEeKwT1TcSzHiEwYGmsXcY0aKPa/834Ce; _clsk=1r7gsgx|1735889059997|3|1|mp.weixin.qq.com/weheat-agent/payload/record; rewardsn=; wxtokenkey=777"
headers = {
    "Cookie": Cookie,
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; YAL-AL00 Build/HUAWEIYAL-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.64 HuaweiBrowser/10.0.1.335 Mobile Safari/537.36"
}

# 微信公众号的token
token = "1316911862"

# 定时访问间隔（例如，每15秒访问一次）
INTERVAL = 15  # 15 s

push_key_dict = {
    "me": "PDU23078Tvl3ShDVG3aYDrCO2Eqf9azouteT6F13q",
    "liujunyu": "PDU26203TfKUwbR46v1cDQpcHcVh9Ahw5heaMcgkR",
    "ating": "PDU32370TzF7kDHHxbwhczlMHUvKPRCCSXX2yBWM7"
}
push_deer_url = "https://api2.pushdeer.com/message/push?pushkey="

session = requests.Session()
session.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Cookie': "u=9696783696;xq_a_token=2e9a942d3a1aa872ababff4336ca5b610e31fe7e",
    'cache-control': "no-cache",
}


def get_stock_data(stock_uid):
    """获取股票数据"""
    params = {"pid": "-1", "category": "1", "size": "1000", "uid": stock_uid}
    try:
        response = session.get(stock_url, params=params)
        response.raise_for_status()
        return response.json()['data']['stocks']
    except RequestException as e:
        logging.error(f"获取股票数据失败：{e}")
        return None


def get_cube_data(cube_symbol):
    """获取组合数据"""
    params = {"count": 20, "page": 1, "cube_symbol": cube_symbol}
    try:
        response = session.get(cube_url, params=params)
        response.raise_for_status()
        return response.json()['list']
    except RequestException as e:
        logging.error(f"获取组合数据失败：{e}")
        return None


def send_push_deer_notification(push_key, message):
    """发送推送通知"""
    url = f"{push_deer_url}{push_key}&text={message}"
    try:
        requests.get(url)
    except RequestException as e:
        logging.error(f"发送推送通知失败：{e}")


def get_article_titles(fake_id):
    url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
    params = {
        "token": token,
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
        "action": "list_ex",
        "begin": 0,
        "count": "2",
        "query": "",
        "fakeid": fake_id,
        "type": "9",
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("app_msg_list", [])
    return []


def check_updates():
    for gzh_name, fake_id in gzh.items():
        article_list = get_article_titles(fake_id)
        new_titles = [article['title'] for article in article_list]
        if fake_id not in global_titles:
            # 第一次访问，不发送通知
            global_titles[fake_id] = new_titles
            logging.info(f"【{gzh_name}】公众号文章初始化成功")
        elif global_titles[fake_id] != new_titles:
            # 标题不相同，发送通知
            gzh_msg = f"【{gzh_name}】有文章更新【{new_titles}】!"
            global_titles[fake_id] = new_titles
            for _, push_value in push_key_dict.items():
                send_push_deer_notification(push_value, gzh_msg)
            logging.info(gzh_msg)


if __name__ == "__main__":

    while True:
        for name, uid in user_dict.items():
            data_current = get_stock_data(uid)

            if data_current:
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
                                for k, v in push_key_dict.items():
                                    if k != "ating":
                                        send_push_deer_notification(v, msg)
                                    else:
                                        if uid == '8282709675' or uid == '7013173046':
                                            send_push_deer_notification(v, msg)

                    if removed_symbols:
                        for stock in stock_data_previous[uid]:
                            if stock['symbol'] in removed_symbols:
                                msg = f"【{name}】删除股票信息: " + stock['symbol'] + ":" + stock['name']
                                logging.info(msg)
                                send_push_deer_notification(push_key_dict['liujunyu'], msg)
                                send_push_deer_notification(push_key_dict['me'], msg)
                                if uid == '8282709675' or uid == '7013173046':
                                    send_push_deer_notification(push_key_dict['ating'], msg)

                    # 更新保存的数据为当前数据
                    stock_data_previous[uid] = data_current

        for name, cube_id in cube_dict.items():
            cube_param['cube_symbol'] = cube_id

            cube_history = get_cube_data(cube_id)
            if cube_history:
                data_current = cube_history[0]
                # 第一次访问 API，保存数据到变量中
                if cube_id not in cube_data_previous:
                    cube_data_previous[cube_id] = data_current['id']
                    logging.info(f"【{name}】组合数据初始化成功")
                # 遍历检查数据，打印组合新调仓信息
                else:
                    for cube in cube_history:
                        if cube['id'] != cube_data_previous[cube_id]:
                            for one in cube['rebalancing_histories']:
                                msg = f"【{name}】组合调仓信息: {one['stock_symbol']}:{one['stock_name']}:{one['price']}【{one['prev_weight_adjusted'] if one['prev_weight_adjusted'] else 0}%->{one['target_weight']}%】"
                                logging.info(msg)
                                send_push_deer_notification(push_key_dict['me'], msg)
                                if cube_id == "ZH3292517" or cube_id == "ZH3337506":
                                    send_push_deer_notification(push_key_dict['ating'], msg)

                        else:
                            cube_data_previous[cube_id] = data_current['id']
                            break

        # 检查公众号是否更新
        check_updates()
        # 等待一段时间后再次访问 API
        time.sleep(INTERVAL)
