import pyodbc
from logger import log_print

def getSQLcon(server, database=None, username=None, password=None, trusted_connection=True):
    try:
        constr = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};"  # Connection string
        if trusted_connection:
            constr += "Trusted_Connection=yes;"
        else:
            if not username or not password:
                raise ValueError('Username and password must be provided for non-Trusted connections')
            constr += f"UID={username};PWD={password};"
        
        log_print(f'Connecting to server [{server}]')
        con = pyodbc.connect(constr)
        log_print(f'Connected to server [{server}]')
        return con
    
    except pyodbc.InterfaceError as e:
        log_print(f"Interface error while connecting to server '{server}': {e}")
        raise
    except pyodbc.OperationalError as e:
        log_print(f"Operational error while connecting to server '{server}': {e}")
        log_print("Ensure SQL Server is running, the instance name is correct, and the credentials are correct.")
        raise
    except Exception as e:
        log_print(f"Unexpected error while connecting to server '{server}': {e}")
        raise
    
def db_exists(server, database):
    try:
        con = getSQLcon(server)
        con.autocommit = True
        cursor = con.cursor()

        cursor.execute('SELECT name FROM sys.databases WHERE name = ?', (database,))
        if not cursor.fetchone():
            log_print(f'Database [{database}] does not exist.')
            cursor.execute(f'CREATE DATABASE [{database}]')
            log_print(f'Database [{database}] created.')
        else:
            log_print(f'Database [{database}] already exists.')

    except pyodbc.Error as e:
        log_print(f"Database operation error: {e}")
        raise
    except Exception as e:
        log_print(f"Unexpected error while ensuring database existence: {e}")
        raise
    finally:
        cursor.close()
