import backtrader as bt
import os
data_cache = {}


def load_data(path, name):
    global data_cache
    current_file_path = os.path.abspath(__file__)
    # 获取包含当前脚本的目录（即src目录）
    src_dir = os.path.dirname(current_file_path)
    # 构建data目录的路径
    data_dir = os.path.join(src_dir, '..', 'data')  # 上升一级然后进入data目录
    full_path = os.path.join(data_dir, path)

    if full_path not in data_cache:
        try:
            data = bt.feeds.GenericCSVData(
                dataname=full_path,
                timeframe=bt.TimeFrame.Days,
                compression=1,
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
