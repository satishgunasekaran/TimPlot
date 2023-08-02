import pandas as pd

def convert_date_column(df: pd.DataFrame 
    , col_name: str) -> bool:
    """
    Checks if the column is a date column or not.
    :param df: The dataframe
    :param col_name: The column name
    :return: True if the column is a date column, False otherwise
    """
    
    # try different date formats
    formats = ['%d-%b', '%Y-%m-%d', '%m-%d-%Y', '%m/%d/%Y']
    
    for fmt in formats:
        try:
            df[col_name] = pd.to_datetime(df[col_name], format=fmt)
        except ValueError:
            pass
        

    
def convert_all_date_columns(df):
    """
    Gets all the date columns in the dataframe.
    :param df: The dataframe
    :return: A list of all the date columns
    """
    for col in df.columns:
        if df[col].dtype == 'object':
            convert_date_column(df, col)
     
    return df


 
    
