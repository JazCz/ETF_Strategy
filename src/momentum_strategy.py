
import backtrader as bt
import datetime


class MomentumETFStrategy(bt.Strategy):
    params = (
        ('period', 20),  # 动量周期
        ('num', 2),  # 选择动量前num大的ETF，按照1/num分配仓位
        ('trade_period', 0),  # 交易周期
        ('wave', 0.05),  # 波动率
        ('prob', 0),  # 波动概率
    )

    def __init__(self):
        self.momentum = bt.indicators.Momentum(period=self.params.period)
        self.next_trade = None  # 下一次允许交易的时间
        self.trade_start_times = {}
        self.holding_days = {}  # 持仓总天数
        self.total_pnl = {}  # 盈利总数

    def next(self):
        if self.next_trade is None or self.next_trade <= self.datetime.datetime():

            momentums = [(data.close[0] / data.open[-self.params.period] - 1, data) for data in self.datas]
            all_negative = all(mom[0] < 0 for mom in momentums)

            if all_negative:
                # 使用动量的绝对值进行排序
                momentums.sort(reverse=True, key=lambda mom: abs(mom[0]))
            else:
                # 正常排序
                momentums.sort(reverse=True, key=lambda mom: mom[0])

            top_num_momentums = momentums[:self.params.num]

            for mom, data in momentums[self.params.num:]:
                self.order_target_size(data, 0)
            # 每次都先清空所有股票
            # 交易
            for mom, data in top_num_momentums:
                self.order_target_percent(data, 1 / self.params.num)

            self.next_trade = self.datetime.datetime() + datetime.timedelta(days=self.params.trade_period)
