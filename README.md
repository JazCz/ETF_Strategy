# ETF_Strategy

这是一个使用Python编写的量化交易策略开发和测试框架，能够从一系列股票组合中找出在当前策略下得到最大收益的组合并可视化。

其中用到了动量轮动和遗传算法。

## 安装

你可以通过以下命令，在虚拟环境中安装所需的Python库：

```bash
pip install -r requirements.txt
```

## 运行项目

克隆项目仓库到本地机器：

```bash
git clone https://github.com/JazCz/ETF_Strategy.git
```

进入项目目录：

```bash
cd Quant_Strategy
```

运行主程序：

```bash
python main.py
```

## 代码结构

- `momentum_strategy.py`：定义了`MomentumETFStrategy`类，实现动量ETF轮动策略。
- `genetic_algorithm.py`：定义了`GeneticAlgorithm`类，实现遗传算法优化策略。
- `data_loader.py`：包含 `load_data` 函数和 `get_data` 函数。`load_data` 函数用于加载和缓存CSV数据文件，如果本地数据文件缺失，`get_data` 函数将被调用来获取数据。
- `config.py`：包含项目配置参数，如CSV文件列表、初始资金、遗传算法参数等。
- `init.py`：项目初始化文件，导入主要模块和类。
- `main.py`：主程序入口，设置参数并启动策略优化过程。
- `plotting.py`：绘图文件，用backtrader_plotting库显示了最优组合的信息
