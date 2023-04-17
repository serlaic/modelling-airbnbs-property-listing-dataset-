import pandas as pd
from ast import literal_eval
import os.path

class clean_tabular_data(object):
    '''
    Class:
    -----------------------------------------------------------------------------------

    clean_tabular_data: This class has several methods which will allow you to convert 
    csv to dataframe and perform different data cleaning techniques.

    Methods:
    -----------------------------------------------------------------------------------

    airbnb_df(df): Reads the file and returns dataframe.

        Variables:
        ----------
        df - (type: DataFrame) - dataframe loaded from the file
        file_link - (type: str) - path to the file
    
    checks_df(df): Checks dataframe and counts null data, % of null data for each 
    column. Also prints column names and dataframe. Takes Dataframe as argument.
    Returns DataFrame

        Variables:
        ----------
        df - (type: DataFrame) - dataframe loaded from the file
        df_null - (type: DataFrame) - dataframe which returns all 
        null/NA values as "False" and everything else as "True"
        df_columns - (type: list) - list of all column names in dataframe

    remove_rows_with_missing_ratings(df): Removes rows with NaN values from 
    all columns with ratings. Returns dataframe. Takes Dataframe as argument.
    Returns DataFrame

        Variables:
        ----------
        df - (type: DataFrame) - dataframe loaded from the file
        df_columns - (type: list) - list of all column names in dataframe
        df_rating_columns - (type: list) - list of all column names with string "rating"
    
    combine_description_strings(df): Converts string to a list in "Description" 
    column of the dataframe. Deletes "About this space" prefix and all empty quotes in 
    a list.Remows rows with NaN values and converts the list back to the string. Takes 
    Dataframe as argument. Returns DataFrame

        Variables:
        ----------
        df - (type: DataFrame) - dataframe loaded from the file
        desc - (type: string), (type: list) - description from "Description" column

        Functions:
        ----------
        string_to_list(desc) - converts string (desc) to a list (desc)
        list_check(desc) - deletes "About this space prefix" and all empty quotes in a 
        list. Changes empty list to None.
    
    set_default_feature_values(df): Fills empty(null/none) rows in columns with 1. Takes 
    Dataframe as argument. Returns DataFrame.
        
        Variables:
        ----------
        column_list (type: list): - list of column names

    clean_tabular_data(df): Calls remove_rows_with_missing_ratings(df), 
    combine_description_strings(df), set_default_feature_values(df) methods
    '''

    @staticmethod
    def airbnb_df():
        '''
        Reads the file and returns dataframe.
        '''
        try:
            file_link = 'airbnb-property-listings/tabular_data/listing.csv'
            df = pd.read_csv(file_link)
        except NameError:
            pass

        return df
    
    @staticmethod    
    def checks_df(df):
        '''
        Checks dataframe and counts null data, % of null data for each column. 
        Also prints column names and dataframe.
        '''
        df_null = df.isnull()
        print(df_null.sum())
        print(df_null.mean() * 100)
        df_columns = df.columns
        print(df_columns)
        print(df)

    @staticmethod
    def remove_rows_with_missing_ratings(df):
        '''
        Removes rows with NaN values from all columns with ratings. Returns dataframe.
        '''
        try:
            df_columns = df.columns
            df_rating_columns = [i for i in df_columns if "rating" in i]
            df = df.dropna(subset = df_rating_columns).reset_index(drop = True) # drops all columns with null values
        except:
            pass

        return df

    @staticmethod
    def combine_description_strings(df):

        '''
        Converts string to a list in "Description" column of the dataframe. Deletes "About this space" prefix and all empty quotes in a list.
        Remows rows with NaN values and converts the list back to the string.
        '''
        df = df.dropna(subset = "Description").reset_index(drop = True)
    
        def string_to_list_ast(desc):
            '''
            Converts string to list
            '''
            try:
                return literal_eval(str(desc))
            except Exception as e:
                print(e)
                print(desc)
            return []
        
        def list_check(desc):
            '''
            Deletes About this space prefix and all empty quotes in a list. Changes empty list to None.
            '''
            try:
                desc = list(desc)
                if len(desc) == 0:
                    desc = None
                del desc[0]
            except:
                print(desc)
            return desc
      
        df['Description'] = df['Description'].apply(lambda desc: string_to_list_ast(desc))
        df['Description'] = df['Description'].apply(lambda desc: list(filter(None, desc))) # removes empty list items
        df['Description'] = df['Description'].apply(list_check)
        df = df.dropna(subset = "Description").reset_index(drop = True)
        df['Description'] = df['Description'].apply(lambda desc: ''.join(desc))
 
        return df
    
    @staticmethod
    def set_default_feature_values(df):
        '''
        Fills empty(null/none) rows in columns with 1
        '''
        
        column_list = ["guests", "beds", "bathrooms", "bedrooms"]
        df[(column_list)] = df[(column_list)].fillna(1)

        return df
    
    @staticmethod
    def clean_tabular_data(df):
        
        df = clean_tabular_data.remove_rows_with_missing_ratings(df)
        df = clean_tabular_data.combine_description_strings(df)
        df = clean_tabular_data.set_default_feature_values(df)

        return df


if __name__ == "main": # to only run the code inside the if statement when the program is run directly by the Python interpreter
    df = clean_tabular_data.airbnb_df()
    df = clean_tabular_data.clean_tabular_data(df)
    df.to_csv(os.path.join('airbnb-property-listings/tabular_data', 'clean_tabular_data.csv'))