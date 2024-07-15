# 股票CSV文件列表，包含所有用于遗传算法优化的股票ETF数据文件
# 每个文件名对应一个ETF的数据
stock_csv_files = ['sz159985.csv',
                   'sh513300.csv',
                   'sh515100.csv',
                   'sz159920.csv',
                   'sh513080.csv',
                   'sz162703.csv',
                   'sz159866.csv',
                   'sz159915.csv',
                   'sh518880.csv',
                   'sh588000.csv',
                   'sh510500.csv',
                   'sz161716.csv',
                   'sz161005.csv']

# 初始资金，用于遗传算法中策略的起始资金
initial_cash = 100000

# 遗传算法参数字典，包含种群大小、突变率、交叉率和迭代代数
ga_params = {
    'population_size': 32,
    'mutation_rate': 0.01,
    'crossover_rate': 0.8,
    'generations': 30
}

# 运行遗传算法的次数，用于获取最优解
# 预估用时 mean(time of each generation) * num_generations * num_runs
num_runs = 5

# 回测起点（新获取的数据）
date = '2020-11-05'

# 动量周期
period = 20

# 选择动量前num大的ETF，按照1/num分配仓位
num = 2

# 手续费
commission=0.0005
