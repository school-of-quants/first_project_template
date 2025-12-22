import json
from pathlib import Path

import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
from first_project_template.src.utils import load_config

project_path = Path(__file__).parent.parent


class SmaCross(Strategy):
    """
    Стратегия, основанная на пересечении двух скользящих средних
    Для ее формирования мы используем bactesting.py фреймворк
    Ознакомиться с документацией можно по ссылке ниже
    https://kernc.github.io/backtesting.py/doc/backtesting/#gsc.tab=0
    """

    n1 = 7
    n2 = 30

    def init(self):
        """
        Инициализируем индикаторы стратегии
        Данный метод вам необходимо переопределить
        """
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)

    def next(self):
        """
        Определяем логику входы и выхода из позиций
        Данный метод вам необходимо переопределить
        """
        if crossover(self.sma1, self.sma2):
            self.position.close()
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.position.close()
            self.sell()

    @classmethod
    def find_best_params(cls, data):
        """
        Обучаем параметры стратегии на обучающей выборке
        Данный метод вам необходимо переопределить
        """
        cfg = load_config(project_path.parent.as_posix() + "/config.yaml")
        initial_capital = cfg["initial_capital"]
        commission = cfg["commission"]
        if cfg["optimize_params"]:
            train_bt = Backtest(data, cls, commission=commission, cash=initial_capital)
            res = train_bt.optimize(
                n1=range(10, 110, 10),
                n2=range(20, 210, 20),
                maximize="Equity Final [$]",
                constraint=lambda p: p.n1 < p.n2,
                max_tries=200,
                random_state=0,
            )
            best_params_dict = {"n1": res._strategy.n1, "n2": res._strategy.n2}
        else:
            best_params_dict = {"n1": 7, "n2": 30}
        return best_params_dict


def train_strategy():
    """
    Запускаем обучении стратегии и сохраняем обученные параметры в json
    """
    train_data = pd.read_parquet(project_path.as_posix() + "/data/train_data.parquet")
    best_params = SmaCross.find_best_params(data=train_data)
    with open(
        project_path.as_posix() + "/artifacts/best_params.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(best_params, f, ensure_ascii=False, indent=4, default=str)


if __name__ == "__main__":
    train_strategy()
