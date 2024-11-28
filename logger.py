from datetime import datetime
import os

LogFile = 'program_log.txt'

def log_print(Message):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    LogMessage = f'[{time}]\t{Message}'
    if not os.path.isfile(LogFile):
        with open(LogFile, 'w') as logTextFile:
            logTextFile.write(f'[{time}]\t Log file: {LogFile} created.\n')
    with open(LogFile, 'a') as logTextFile:
        logTextFile.write(f'{LogMessage}\n')
    print(LogMessage)