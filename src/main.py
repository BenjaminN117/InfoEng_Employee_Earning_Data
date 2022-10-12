import pandas as pd


class Employee_Earnings():
    def __init__(self) -> None:
        self.filepath = "./dataset/batch2_jobID_00B80TR.csv"
    
    def db_import(self):
        df = pd.read_csv(self.filepath)
        print(df.head(10))

if __name__ == "__main__":
    inst = Employee_Earnings()
    
    inst.db_import()
    