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
    "薛定谔的牛": "3639429204",
    "复旦橙子橙": "3697768583",
    "Moss_LD": "3316855169",
    "robo": "5712584562",
    # "猫猫": "9696783696"
}

cube_url = "https://xueqiu.com/cubes/rebalancing/history.json"
cube_data_previous = {}  # 第一次访问组合API
cube_param = {"count": 20, "page": 1}
cube_dict = {
    "轮回666": "ZH3292517",
    "花盆君": "ZH3377835",
    "暮烟风雨": "ZH1739131",
}

push_key_dict = {
    "me": "PDU23078Tvl3ShDVG3aYDrCO2Eqf9azouteT6F13q",
    "liujunyu": "PDU26203TfKUwbR46v1cDQpcHcVh9Ahw5heaMcgkR",
    "ating": "PDU32370TzF7kDHHxbwhczlMHUvKPRCCSXX2yBWM7"
}
push_deer_url = "https://api2.pushdeer.com/message/push?pushkey="

session = requests.Session()
session.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Cookie': "u=9696783696;xq_a_token=1913d0484930cf1575179b21e84736991edde70d",
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
                                        if uid == '8282709675':
                                            send_push_deer_notification(v, msg)

                    if removed_symbols:
                        for stock in stock_data_previous[uid]:
                            if stock['symbol'] in removed_symbols:
                                msg = f"【{name}】删除股票信息: " + stock['symbol'] + ":" + stock['name']
                                logging.info(msg)
                                send_push_deer_notification(push_key_dict['liujunyu'], msg)
                                send_push_deer_notification(push_key_dict['me'], msg)
                                if uid == '8282709675':
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
                                if cube_id == "ZH3292517":
                                    send_push_deer_notification(push_key_dict['liujunyu'], msg)
                                    send_push_deer_notification(push_key_dict['ating'], msg)

                        else:
                            cube_data_previous[cube_id] = data_current['id']
                            break

        # 等待一段时间后再次访问 API
        time.sleep(15)

