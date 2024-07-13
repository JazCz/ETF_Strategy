# 股票CSV文件列表，包含所有用于遗传算法优化的股票ETF数据文件
# 每个文件名对应一个ETF的数据
stock_csv_files = ['sh510050.csv', 'sh510300.csv', 'sh510500.csv', 'sh512100.csv', 'sz159915.csv', 'sh588000.csv',
                   'sh512880.csv', 'sz159813.csv', 'sh512690.csv', 'sh512010.csv', 'sz159852.csv', 'sh515880.csv',
                   'sh512980.csv']

# 初始资金，用于遗传算法中策略的起始资金
initial_cash = 100000

# 遗传算法参数字典，包含种群大小、突变率、交叉率和迭代代数
# 这些参数控制遗传算法的行为和性能
ga_params = {
        'population_size': 32,
        'mutation_rate': 0.01,
        'crossover_rate': 0.8,
        'generations': 30
    }

# 运行遗传算法的次数，用于获取最优解
num_runs = 1
