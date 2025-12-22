import json
from pathlib import Path

import pandas as pd
from backtesting import Backtest
from first_project_template.src.strategy import SmaCross
from first_project_template.src.utils import load_config

project_path = Path(__file__).parent.parent


def run_backtest():
    """
    Запускает бэктест на бэктестовых данных
    Сохраняет:
        - Основные бэктестовые метрики в /artifacts/backtest_metrics.json
        - График PnL стратегии в /artifacts/equity_curve.html
    """
    cfg = load_config(project_path.parent.as_posix() + "/config.yaml")

    INITIAL_CAPITAL = cfg["initial_capital"]
    COMMISSION = cfg["commission"]

    backtest_data = pd.read_parquet(
        project_path.as_posix() + "/data/backtest_data.parquet"
    )

    with open(
        project_path.as_posix() + "/artifacts/best_params.json",
        "r",
        encoding="utf-8",
    ) as f:
        res = json.load(f)

    for k, v in res.items():
        setattr(SmaCross, k, int(v))

    bt = Backtest(
        backtest_data,
        SmaCross,
        cash=INITIAL_CAPITAL,
        commission=COMMISSION,
        exclusive_orders=True,
    )
    metrics = bt.run().drop(["_strategy", "_equity_curve", "_trades"])

    metrics.to_json(
        project_path.as_posix() + "/artifacts/backtest_metrics.json", indent=4
    )
    bt.plot(
        filename=project_path.as_posix() + "/artifacts/equity_curve.html",
        open_browser=False,
    )


if __name__ == "__main__":
    run_backtest()
