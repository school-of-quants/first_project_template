from example_project1.src.get_data import get_data
from example_project1.src.run_backtest import run_backtest
from example_project1.src.strategy import train_strategy


def main():
    get_data()
    train_strategy()
    run_backtest()


if __name__ == "__main__":
    main()
