import backtrader as bt
import datetime
from config import num, period


class MomentumETFStrategy(bt.Strategy):
    """

    MomentumETFStrategy是一个策略类，它实现了基于Backtrader框架的动量轮动策略

    参数:
    - period (int): 动量指标的周期长度，用于计算动量。
    - num (int): 选择动量最大的前num个ETF进行交易，同时每个ETF持有1/num仓位。

    属性:
    - momentum (bt.indicators.Momentum): 动量指标。

    用法示例:
    >>> cerebro.addstrategy(MomentumETFStrategy)
    在配置好数据和cash的cerebro引擎上直接加入策略。

    """
    # 定义策略参数
    params = (
        ('period', period),  # 动量周期
        ('num', num),  # 选择动量前num大的ETF，按照1/num分配仓位
        ('trade_period', 0),  # 交易周期
    )

    def __init__(self):
        """

        初始化策略，设置动量指标，并初始化用于记录交易和持仓的变量。

        """
        self.momentum = bt.indicators.Momentum(period=self.params.period)
        self.next_trade = None  # 下一次允许交易的时间
        self.trade_start_times = {}  # 初始化交易开始时间字典

    def next(self):
        """

        策略逻辑的执行函数，每个周期都会被调用。

        1. 检查是否到了下一次允许交易的时间。
        2. 计算所有ETF的动量值，并根据动量值选择前num个ETF。
        3. 如果所有ETF的动量值都是负的，则按照动量的绝对值排序，选择波动最大的ETF。
        4. 对于排名在num之后的ETF，清空其仓位。
        5. 对于选中的ETF，按照1/num的比例分配仓位。
        6. 更新下一次交易的时间。

        """
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
            # 对于排名在num之后的ETF，清空其仓位。
            for mom, data in momentums[self.params.num:]:
                self.order_target_size(data, 0)

            # 对于选中的ETF，按照1/num的比例分配仓位。
            for mom, data in top_num_momentums:
                self.order_target_percent(data, 1 / self.params.num)

            self.next_trade = self.datetime.datetime() + datetime.timedelta(days=self.params.trade_period)
