from logger import log_print
from database import db_exists, getSQLcon
from csv_processing import process_csv
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')


FolderPath = 'csv_files'
ServerName = os.getenv('Servername')
DatabaseName = os.getenv('DatabaseName')
userid = os.getenv('userid')
password = os.getenv('password')


def main():
    log_print("Processing files has started")
    
    if not (ServerName and DatabaseName and userid and password):
        log_print("Missing environment variables (ServerName, DatabaseName, userid, or password)")
        return
    
    db_exists(server=ServerName, database=DatabaseName)
    
    try:
        log_print(f"Connecting to server [{ServerName}] ")
        con = getSQLcon(server=ServerName, database=DatabaseName, username=userid, password=password, trusted_connection=False)
    except Exception as e:
        log_print(f'Failed to connect to database with error: {e}')
        return
    
    try:
        process_csv(FolderPath, con)
    except Exception as e:
        log_print(f'Error while processing CSV files: {e}')
    finally:
        con.close()
        log_print("Processing files has finished\n")

if __name__ == "__main__":
    main()