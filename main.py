from first_project_template.src.get_data import get_data
from first_project_template.src.run_backtest import run_backtest
from first_project_template.src.strategy import train_strategy


def main():
    get_data()
    train_strategy()
    run_backtest()


if __name__ == "__main__":
    main()
