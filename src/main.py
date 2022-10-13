import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Employee_Earnings():
    def __init__(self):
        self.csvFilepath1 = "./dataset/batch1_jobID_00A32TE.csv"
        self.csvFilepath2 = "./dataset/batch2_jobID_00B80TR.csv"
    def db_import(self):
        '''
        Imports both csv files as seperate dataframes and then combines them into a single one
        '''
        df1 = pd.read_csv(self.csvFilepath1)
        df2 = pd.read_csv(self.csvFilepath2)
        
        self.df = pd.concat([df1, df2])
        
    def df_cleaning(self):
        '''
        Cleans the dataframe ready for analysis
        '''
        # Checks for missing values in the df
        print(self.df.isnull().sum())        
        
        # Removes the companyId row from the dataframe
        del self.df["companyId"]
        
        ## Creates a subset dataframe ##
        
        # Remove rows that have no salary information
        self.df_subset_Nnull = self.df.loc[self.df["salary"].notnull()]
        # Remove the 'degree', 'major' and milesFromMetropolis columns
        del self.df_subset_Nnull['degree'], self.df_subset_Nnull["major"], self.df_subset_Nnull["milesFromMetropolis"]
   
   
    def df_analysis(self):
        # Add the Industries and Job types to a list
        listOfIndustries = self.df_subset_Nnull.industry.unique()
        listOfJobs = self.df_subset_Nnull.jobType.unique()
        # Create a blank subset dataframe while using the headers from the main subset
        df_subset_final = self.df_subset_Nnull[0:0] 
        ## Average out all of the job types and industries so their is only one entry for each and apply that to df_subset_final ##
        for industry in listOfIndustries:
            for job in listOfJobs:
                # Add all of the rows to a dataframe that contain the same industry and job
                df_subset_temp = self.df_subset_Nnull.loc[(self.df_subset_Nnull["jobType"] == job) & (self.df_subset_Nnull["industry"] == industry)]
                # Average the salary and years experience and add it to another data frame
                df_subset_final = df_subset_final.append({'jobType':job, 'industry':industry, 'yearsExperience':round(df_subset_temp["yearsExperience"].mean(), 1), 'salary':round(df_subset_temp["salary"].mean(), 1)}, ignore_index=True)
                # Empty the temporary dataframe before the next iteration
                df_subset_temp = df_subset_temp[0:0]
        
        seniorSalary = df_subset_final[df_subset_final['jobType'] == "SENIOR"]['salary']
        juniorSalary = df_subset_final[df_subset_final['jobType'] == "JUNIOR"]['salary']
        janitorSalary = df_subset_final[df_subset_final['jobType'] == "JANITOR"]['salary']

        
        x = np.arange(len(listOfIndustries))
        width = 0.25

        fig, ax = plt.subplots()
        
        bar1= ax.bar(x, seniorSalary, width, label='SENIOR')
        bar2= ax.bar(x + width, juniorSalary, width, label='JUNIOR')
        bar3= ax.bar(x + width*2, janitorSalary, width, label='JANITOR')
        
        ax.set_xticks(x+width, listOfIndustries)
        ax.set_xticklabels(listOfIndustries)
        ax.legend()
        
        # Labels
        plt.xlabel("Industry")
        plt.ylabel("Salary")    
        
        plt.show()
        

if __name__ == "__main__":
    inst = Employee_Earnings()
    
    inst.db_import()
    inst.df_cleaning()
    inst.df_analysis()