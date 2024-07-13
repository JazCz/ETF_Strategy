from genetic_algorithm import GeneticAlgorithm
from data_loader import load_data
from config import stock_csv_files, initial_cash, ga_params, num_runs


def run_multiple_times(data_files, cash, ga_params, num_runs):
    ga = GeneticAlgorithm(ga_params)
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

    # 找到所有运行中的最大值
    max_score = max(best_scores)
    best_individual = best_individuals[best_scores.index(max_score)]

    return best_individual, max_score


def main():
    # 优化方向:精英策略, 多次运行以获得不同的初值(避免陷入局部最大)
    # 本质上是经典的非线性优化问题
    best_etf_combination, max_profit = run_multiple_times(stock_csv_files, initial_cash, ga_params, num_runs)
    print(f"Best ETF combination across all runs: {best_etf_combination}")
    print(f"Maximum profit across all runs: {max_profit:.2f}")
    print(f"Latest profit: 222128.05 [0 0 0 1 0 0 0 1 0 0 0 1 0]")


if __name__ == "__main__":
    main()
