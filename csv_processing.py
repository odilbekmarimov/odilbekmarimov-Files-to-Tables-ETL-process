import os
import pandas as pd
from logger import log_print


filetype = '.csv' #editable, give with leading '.' (dot)
    
def csv2sql(FilePath, TableName, con):
    df = pd.read_csv(FilePath).fillna(0.0)
    cursor = con.cursor()
# TO DO
# change pd.read_csv to pd.read_{filetype}
    log_print(f"Table name: {TableName}")
        # dbo is assumed to be default schema
    cursor.execute(f'IF OBJECT_ID(\'dbo.{TableName}\', \'U\') IS NOT NULL DROP TABLE dbo.{TableName}')
    con.commit()

    create_query = f"create table {TableName} ("
    for columnName, dtype in zip(df.columns, df.dtypes): #several errors occured when i 
        #used pd.to_sql function, will fix that and upload to sql
        #solution to problem is to install sqlalchemy library
        if dtype == "object":
            sqltype = 'NVARCHAR(MAX)'
        elif dtype == "int64":
            sqltype = 'INT'
        elif dtype == "float64":
            sqltype = 'FLOAT'
        elif dtype == "bool":
            sqltype = 'BIT'
        else:
            sqltype = 'NVARCHAR(MAX)'

        create_query += f"[{columnName}] {sqltype}, "
    create_query = create_query.rstrip(', ') + ")"

    log_print(f"Creating table with query: {create_query}")
    cursor.execute(create_query)
    con.commit()

   
    for row in df.itertuples(index=False):
        placeholders = ', '.join(['?'] * len(row))
        insert_query = f'INSERT INTO {TableName} VALUES ({placeholders})'
        try:
            cursor.execute(insert_query, *row)
        except Exception as E:
            log_print(f'Error inserting row: {row}')
            log_print(f'Error details: {E}')

    con.commit()
    cursor.close()


def process_csv(FolderPath, con):
    for file in os.listdir(FolderPath):
        if file.endswith(filetype):
            FilePath = os.path.join(FolderPath, file)
            TableName = os.path.splitext(file)[0]
            log_print(f"Processing {file} into table {TableName}")
            csv2sql(FilePath=FilePath, TableName=TableName, con=con)
            log_print(f'Table {TableName} created')