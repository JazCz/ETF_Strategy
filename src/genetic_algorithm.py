import time

import numpy as np
import backtrader as bt

from config import commission
from momentum_strategy import MomentumETFStrategy


class GeneticAlgorithm:
    """

    GeneticAlgorithm是一个遗传算法类，用于通过模拟自然选择过程来优化策略参数。

    参数:
    - params (dict): 包含遗传算法参数的字典，包括：种群大小、突变率、交叉率和迭代代数。

    属性:
    - population_size (int): 种群大小。
    - mutation_rate (float): 突变率。
    - crossover_rate (float): 交叉率。
    - generations (int): 迭代代数。
    - population (list): 当前种群的个体列表。
    - fitness_scores (np.array): 个体的适应度分数数组。

    """

    def __init__(self, params):
        """

        初始化遗传算法的参数和种群。

        """
        self.population_size = params.get('population_size')
        self.mutation_rate = params.get('mutation_rate')
        self.crossover_rate = params.get('crossover_rate')
        self.generations = params.get('generations')
        self.population = []
        self.fitness_scores = []

    def initialize_population(self, data_files):
        """

        初始化种群，随机生成个体，确保每个个体至少选择两个数据文件（也就是至少要选择两个以上的ETF）。

        """
        # 随机初始化种群
        self.population = []
        for _ in range(self.population_size):
            individual = np.random.choice([0, 1], size=len(data_files))

            # 确保至少有两个1
            while individual.sum() < 2:
                individual = np.random.choice([0, 1], size=len(data_files))

            self.population.append(individual)

        self.fitness_scores = np.zeros(self.population_size)

    def calculate_fitness(self, data_files, cash):
        """

        计算每个个体的适应度，即策略的最终投资组合价值。

        参数:
        - data_files (list): 用于策略的数据文件列表。
        - cash (float): 初始资金。

        """
        data_index_map = {i: key for i, key in enumerate(data_files)}
        # 计算适应度，即策略的最终投资组合价值
        for idx, individual in enumerate(self.population):
            cerebro = bt.Cerebro(stdstats=False)  # 只关心收益，省去Observer提升速度

            selected_data_keys = [data_index_map[i] for i, gene in enumerate(individual) if gene == 1]

            for data_key in selected_data_keys:
                cerebro.adddata(data_key)

            cerebro.broker.setcash(cash)
            cerebro.broker.setcommission(commission=commission)
            cerebro.addstrategy(MomentumETFStrategy)
            cerebro.run()
            self.fitness_scores[idx] = cerebro.broker.getvalue()

    def selection(self):
        """

        选择过程，根据适应度分数选择个体以用于下一代的繁殖。

        """
        # 选择过程，根据适应度选择个体
        selected_indices = np.random.choice(range(self.population_size), size=self.population_size, replace=True,
                                            p=self.fitness_scores / np.sum(self.fitness_scores))
        return [self.population[idx] for idx in selected_indices]

    def crossover(self, parents):
        """

        交叉过程，通过交换父母的基因来生成新的后代。

        参数:
        - parents (list): 被选中用于繁殖的父母个体列表。

        """
        offspring = []
        num_parents = len(parents)
        for i in range(0, len(parents) - 1, 2):
            parent1, parent2 = parents[i], parents[i + 1]
            if np.random.rand() < self.crossover_rate:
                crossover_point = np.random.randint(1, len(parent1))
                child1 = np.concatenate([parent1[:crossover_point], parent2[crossover_point:]])
                child2 = np.concatenate([parent2[:crossover_point], parent1[crossover_point:]])

                # 确保交叉后的后代至少有两个1
                while child1.sum() < 2:
                    crossover_point = np.random.randint(1, len(parent1))
                    child1 = np.concatenate([parent1[:crossover_point], parent2[crossover_point:]])
                while child2.sum() < 2:
                    crossover_point = np.random.randint(1, len(parent1))
                    child2 = np.concatenate([parent2[:crossover_point], parent1[crossover_point:]])

                offspring.extend([child1, child2])
            else:
                offspring.extend([parent1, parent2])
        if num_parents % 2 == 1:  # 父母数量是奇数
            if np.random.rand() < self.crossover_rate:
                offspring.append(parents[-1].copy())
            else:
                offspring.append(parents[-1])
        return offspring

    def mutation(self, offspring):
        """

        突变过程，随机改变个体的某些基因以增加遗传多样性。

        参数:
        - offspring (list): 由交叉过程生成的后代个体列表。

        """
        for individual in offspring:
            if np.random.rand() < self.mutation_rate:
                mutation_point1 = np.random.randint(len(individual))
                mutation_point2 = np.random.randint(len(individual))

                tmp = individual[mutation_point1]
                individual[mutation_point1] = individual[mutation_point2]
                individual[mutation_point1] = tmp

        return offspring

    def evolve(self):
        """

        进化过程，通过选择、交叉和突变生成新一代的种群。

        """
        new_population = self.selection()
        new_population = self.crossover(new_population)
        new_population = self.mutation(new_population)
        return new_population

    def run(self, data_files, cash):
        """

        运行遗传算法，通过多代迭代寻找最优策略参数。

        参数:
        - data_files (list): 用于策略的数据文件列表。
        - cash (float): 初始资金。

        返回:
        - tuple: 包含最优个体和其适应度分数的元组。

        """
        self.initialize_population(data_files)

        best_score = 0
        best_individual = None
        no_improvement_counter = 0  # 连续几代没有提升的次数
        iteration_times = []  # 用于存储每次迭代的用时

        for generation in range(self.generations):
            start_time = time.time()
            self.calculate_fitness(data_files, cash)
            max_fitness_idx = np.argmax(self.fitness_scores)
            current_max = self.fitness_scores[max_fitness_idx]
            print(f"Generation {generation + 1}, Current Fittness: {current_max}")

            if current_max > best_score:
                best_score = current_max
                best_individual = self.population[max_fitness_idx]
                no_improvement_counter = 0
            else:
                no_improvement_counter += 1

            if no_improvement_counter >= 3:  # 如果连续N代没有提升

                self.mutation_rate += 0.02
                self.crossover_rate += 0.03

                no_improvement_counter = 0

                if self.crossover_rate >= 1:
                    self.crossover_rate = 0.85
                    print("Reset crossover_rate")

                if self.mutation_rate >= 0.1:
                    self.mutation_rate = 0.01
                    print("Reset mutation_rate")

            self.population = self.evolve()
            end_time = time.time()  # 记录迭代结束时间
            iteration_time = end_time - start_time  # 计算迭代用时
            iteration_times.append(iteration_time)  # 将用时添加到列表

            # 打印当前迭代的最佳适应度和用时
            print(
                f"Best Fitness = {best_score}, Time Elapsed = {iteration_time:.2f} seconds")

        return best_individual, best_score
