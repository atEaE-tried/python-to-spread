from typing import Any
from gspread.models import Spreadsheet
import stopwatch
from cli import parse_commandline_args
from config import Configuration
from datetime import datetime
import gspread
import csv
from google.oauth2.service_account import Credentials
from stopwatch import Stopwatch

# e.g. python main.py --importfile ./data/example.csv --credentials ./.local/secret.json --share example@gmail.com --title Sample
def main():
    """ Main Process

    Args:
        none
    Returns:
        code (int): exit status code.
    """
    stopwatch = Stopwatch()
    stopwatch.start()

    args = parse_commandline_args()

    # create sheet title
    titlePrefix = args.title
    if not (args.title):
        titlePrefix = "NewReport"
    now = datetime.now()
    title = titlePrefix + '_' + str(now.year) + str(now.month).zfill(2) + str(now.day).zfill(2) + str(now.hour).zfill(2) + str(now.minute).zfill(2) + str(now.second).zfill(2)

    # load configuraion
    config = Configuration()

    # create sheet
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    try:
        credentials = Credentials.from_service_account_file(args.credentials, scopes=scopes)
        gc = gspread.authorize(credentials)
        sheet = gc.create(title)
    
        # share user
        sheet.share(args.share, perm_type='user', role='owner')

        # update worksheet
        wk = sheet.sheet1
        wk.update_title('Result')

        # input worksheet
        with open(file=args.importfile, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=",", doublequote=False, lineterminator="\r")

            # update worksheet
            wk.add_rows(len(reader.fieldnames) + config.row_buffer)
            wk.add_cols(config.column_buffer)
            
            # set header
            headers = wk.range(1, 1, 1, len(reader.fieldnames))
            for i in range(len(reader.fieldnames)):
                headers[i].value = reader.fieldnames[i]
            wk.update_cells(headers)

            # set value
            fileds = reader.fieldnames
            v_row_count = 2
            total_cells = []
            for row in reader:
                cells = wk.range(v_row_count, 1, v_row_count, len(fileds))
                for i in range(len(fileds)):
                    cells[i].value = row[fileds[i]]
                total_cells.extend(cells)
                v_row_count += 1
            wk.update_cells(total_cells)

    except:
        raise

    finally:
        stopwatch.stop()
        info(sheet)
    
    print('Complete🎉 : time = ', stopwatch.duration)
    return 0

def info(sheet: Spreadsheet):
    """ Show information.

    Args:
        sheet (Spreadsheet)
    Returns:
        void
    """

    print()
    print('##### SpredSheet Info #####')
    print('* ID    : ', sheet.id)
    print('* URL   : ', sheet.url)
    print()

main()