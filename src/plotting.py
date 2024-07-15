import backtrader as bt
from momentum_strategy import MomentumETFStrategy
from config import initial_cash, stock_csv_files
from data_loader import load_data
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Tradimo


def plot_strategy(combination):
    cerebro = bt.Cerebro()

    preloaded_data = {load_data(file, file.split('.')[0]): file for file in stock_csv_files}
    data_index_map = {i: key for i, key in enumerate(preloaded_data)}

    selected_data_keys = [data_index_map[i] for i, selected in enumerate(combination) if selected == 1]

    for data_key in selected_data_keys:
        cerebro.adddata(data_key)

    cerebro.broker.setcash(initial_cash)
    cerebro.addstrategy(MomentumETFStrategy)
    cerebro.run()

    b = Bokeh(style='bar', plot_mode='single', scheme=Tradimo())
    cerebro.plot(b)