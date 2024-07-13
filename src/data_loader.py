import backtrader as bt
import os
import akshare as ak
import pandas as pd
from config import date

# 全局字典，用于缓存加载的数据
data_cache = {}


def load_data(path, name):
    """

    加载CSV数据文件并根据需要缓存数据。

    参数:
    - path (str): 相对于‘data'目录的文件路径。
    - name (str): 数据源的名称，用于在Backtrader中标识。

    返回:
    - bt.feeds.GenericCSVData: 加载的数据源对象，或者在加载失败时返回None。

    """
    global data_cache
    current_file_path = os.path.abspath(__file__)
    # 获取包含当前脚本的目录（即src目录）
    src_dir = os.path.dirname(current_file_path)
    # 构建data目录的路径
    data_dir = os.path.join(src_dir, '..', 'data')  # 上升一级然后进入data目录
    full_path = os.path.join(data_dir, path)

    if not os.path.exists(full_path):
        data = get_data(path, date)
        if data is None:
            print(f"Failed to retrieve data for {path} using get_data method.")
            return None

    if full_path not in data_cache:
        try:
            # 如果数据不在缓存中，加载数据
            data = bt.feeds.GenericCSVData(
                dataname=full_path,
                timeframe=bt.TimeFrame.Days,
                compression=1,  # 设置数据压缩级别，1表示每根K线代表一天
                openinterest=-1,
                dtformat='%Y-%m-%d',
                header=True,
                parse_dates=True,
                name=name,
            )
            data_cache[full_path] = data  # 缓存数据
            return data
        except IOError as e:
            print(f"Error loading data from {full_path}: {e}")
            return None
    else:
        # 从缓存中获取数据
        return data_cache[full_path]


def get_data(symbol, date):
    """

    从新浪获取ETF的历史数据，并保存到’data‘目录下的CSV文件。

    参数:
    - symbol (str): ETF的代码.csv
    - date (str): 需要的数据的起始日期，格式为 'YYYY-MM-DD'。

    返回:
     - file_name (str): 保存数据的CSV文件名称。

    """

    df = ak.fund_etf_hist_sina(symbol=symbol.split('.')[0])

    current_file_path = os.path.abspath(__file__)
    # 获取包含当前脚本的目录（即src目录）
    src_dir = os.path.dirname(current_file_path)
    # 构建data目录的路径
    data_dir = os.path.join(src_dir, '..', 'data')  # 上升一级然后进入data目录

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    file_name = os.path.join(data_dir, symbol)
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    df = df[df.index >= pd.to_datetime(date)]
    df.to_csv(file_name, index=True)
    print(f"Data saved to {file_name}.")

    return file_name
