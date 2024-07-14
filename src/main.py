from genetic_algorithm import GeneticAlgorithm
from data_loader import load_data
from config import stock_csv_files, initial_cash, ga_params, num_runs


# 由于要兼容绘图库backtrader_plotting，导致其他库的版本较低，这可能会导致一些库无法引入
# 如没有绘图需求，请忽略绘图库，并在互相兼容的前提下使用新的版本，backtrader_plotting的依赖包是backtrader、bokeh、jinja2、pandas、matplotlib 和 markdown2
# TODO: 输出最优解的投资图，与全仓沪深300做对比图
# TODO：检查所有文件以统一回测起点，否则重新获取数据
# TODO：为提升运行速率，用C++实现策略类
# TODO：优化遗传算法，如精英策略，适应度共享，局部搜索
# TODO: 为每次交易计算手续费
# TODO: 添加其他的交易指标，如RSI
# TODO: 用并行处理提高计算速度
# TODO: 用其他方法解决最优化问题，如XGBoost算法，蚁群算法，模拟退火算法，或强化学习，深度学习等方法
def run_multiple_times(data_files, cash, ga_params, num_runs):
    """

    多次运行遗传算法，寻找最优ETF组合。

    参数:
    - data_files (list): 包含所有CSV文件路径的列表。
    - cash (float): 初始资金。
    - ga_params (dict): 遗传算法的参数。
    - num_runs (int): 要运行的遗传算法的次数。

    返回:
    - tuple: 包含最优ETF组合和所有运行中的最大利润。

    """
    ga = GeneticAlgorithm(ga_params)
    # 预加载数据并缓存，键为数据对象，值为文件名
    preloaded_data = {load_data(file, file.split('.')[0]): file for file in data_files}
    best_individuals = []
    best_scores = []

    for _ in range(num_runs):
        print(f"Running iteration {_ + 1}")
        individual, score = ga.run(preloaded_data, cash)
        best_individuals.append(individual)
        best_scores.append(score)

        # 可以选择在这里打印每次运行的最佳结果
        print(f"Iteration {_ + 1} - Best Individual: {individual}, Best Score: {score}")

    # 从所有运行中找到最大利润及其对应的ETF组合
    max_score = max(best_scores)
    best_individual = best_individuals[best_scores.index(max_score)]

    return best_individual, max_score


def main():
    """

    主函数，用于设置遗传算法参数并启动多次运行，最后输出最优结果。

    """
    # 本质上是经典的非线性优化问题
    best_etf_combination, max_profit = run_multiple_times(stock_csv_files, initial_cash, ga_params, num_runs)
    print(f"Best ETF combination across all runs: {best_etf_combination}")
    print(f"Maximum profit across all runs: {max_profit:.2f}")
    print(f"Latest profit: 222128.05 [0 0 0 1 0 0 0 1 0 0 0 1 0]")


if __name__ == "__main__":
    main()
