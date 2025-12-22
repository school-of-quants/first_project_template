import os
from pathlib import Path

import pandas as pd
import yfinance as yf

from example_project1.src.utils import load_config

project_path = Path(__file__).parent.parent


def get_data():
    """
    Скачиваем тренировочноые и бэктестовые данные и сохраняем в train_data.parquet и backtest_data.parquet соответственно
    """
    os.makedirs(project_path.as_posix() + "/data", exist_ok=True)
    os.makedirs(project_path.as_posix() + "/artifacts", exist_ok=True)
    cfg = load_config(project_path.parent.as_posix() + "/config.yaml")

    TICKER = "BTC-USD"
    TRAIN_START_DATE = cfg["train_start_date"]
    TRAIN_END_DATE = cfg["train_end_date"]
    BACKTEST_START_DATE = cfg["backtest_start_date"]
    BACKTEST_END_DATE = cfg["backtest_end_date"]

    data = yf.download(TICKER, TRAIN_START_DATE, BACKTEST_END_DATE, group_by="ticker")[
        TICKER
    ]
    data = data.dropna().iloc[1:, :]
    data = data.astype(float)
    data.index = pd.to_datetime(data.index)

    data.loc[TRAIN_START_DATE:TRAIN_END_DATE].to_parquet(
        project_path.as_posix() + "/data/train_data.parquet"
    )
    data.loc[BACKTEST_START_DATE:BACKTEST_END_DATE].to_parquet(
        project_path.as_posix() + "/data/backtest_data.parquet"
    )


if __name__ == "__main__":
    get_data()
