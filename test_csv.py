from maeda.Csv import Csv

if __name__ == "__main__":
    test = Csv(labels = ['Data', 'canal1', 'canal2', 'canal3'])
    test.load_value(["20/8/1974", "98.0", "122.6", "5.7"])
    test.load_value(["20/8/1974", "100.0", "123.4", "5.6"])
    test.load_value(["20/8/1974", "101.8.0", "124.4", "5.8"])