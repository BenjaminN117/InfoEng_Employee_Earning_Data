import pandas as pd
import matplotlib.pyplot as plt

class Employee_Earnings():
    def __init__(self) -> None:
        self.csvFilepath1 = "./dataset/batch1_jobID_00A32TE.csv"
        self.csvFilepath2 = "./dataset/batch2_jobID_00B80TR.csv"
    def db_import(self):
        '''
        Imports both csv files as seperate dataframes and then combines them into a single one
        '''
        df1 = pd.read_csv(self.csvFilepath1)
        df2 = pd.read_csv(self.csvFilepath2)
        
        self.df = pd.concat([df1, df2])
        #self.df.info()
        #print(self.df.head(10))
        
    def df_cleaning(self):
        '''
        Cleans the dataframe ready for analysis
        '''
        # Checks for missing values in the df
        #print(self.df.isnull().sum())        
        
        # Removes the companyId row from the dataframe
        del self.df["companyId"]
        #print(self.df.head(10))

        ##df_subset = self.df.loc[(self.df['companyId'] == 'COMP1') & (self.df['jobType'] == 'CEO')]
        #print(df_subset)
    def df_analysis(self):
        
        '''
        Question: Which industries job see the fastest scaling pay rate vs years experience?
        
        New Question: Pay difference for CEOs in each industry
        
        Measuring pay rate with years experience = Industry name
        1) Exclude any data that has no salary using a subset dataframe
        2) calculate years experience range for each industry and pick the largest range as the base
        3) calculate pay range for each job type in an industry
        
        1) For each type of job in an industry average out the salary and the years experience
        
        X axis = Years experience
        
        y axis = Salary
        
        Each graph is for a specific job type
        
        '''
        df_subset_Nnull = self.df.loc[self.df["salary"].notnull()]
        del df_subset_Nnull['degree'], df_subset_Nnull["major"], df_subset_Nnull["milesFromMetropolis"]
    
        listOfIndustries = df_subset_Nnull.industry.unique()
        listOfJobs = df_subset_Nnull.jobType.unique()

        df_subset_final = df_subset_Nnull[0:0] 
        
        for industry in listOfIndustries:
            for job in listOfJobs:
                # Add all of the rows to a dataframe that contain the same industry and job
                df_subset_temp = df_subset_Nnull.loc[(df_subset_Nnull["jobType"] == job) & (df_subset_Nnull["industry"] == industry)]
               # print(df_subset_temp.head(5))
                # Average the salary and years experience and add it to another data frame
                df_subset_final = df_subset_final.append({'jobType':job, 'industry':industry, 'yearsExperience':round(df_subset_temp["yearsExperience"].mean(), 1), 'salary':round(df_subset_temp["salary"].mean(), 1)}, ignore_index=True)
                #print(df_subset_final.head(10))
                # Empty the temporary dataframe before the next iteration
                df_subset_temp = df_subset_temp[0:0]
                #print(df_subset_temp.head(5))
                
        # fig, ax = plt.subplots()
        # ax.set_xlim()
        
        ceoSalary = df_subset_final[df_subset_final['jobType'] == "CEO"]['salary']
        industryName = df_subset_final[df_subset_final['jobType'] == "CEO"]['industry']
        
        '''
        X axis = Industries
        Y axis = Salary
        '''
        
        plt.bar(industryName, ceoSalary)
        # Labels
        plt.xlabel("Industry")
        plt.ylabel("Salary")
        
        plt.bar_label(plt.bar, padding=3)
        
        
        plt.show()
        

if __name__ == "__main__":
    inst = Employee_Earnings()
    
    inst.db_import()
    inst.df_cleaning()
    inst.df_analysis()