from gspread.models import Spreadsheet
from cli import parse_commandline_args
from config import Configuration
from datetime import datetime
import gspread
import csv
from google.oauth2.service_account import Credentials

# e.g. python main.py --importfile ./data/example.csv --credentials ./.local/secret.json --share example@gmail.com --title Sample
def main():
    """ Main Process

    Args:
        none
    Returns:
        code (int): exit status code.
    """
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
        wk.add_rows(config.row_buffer)
        wk.add_cols(config.column_buffer)

        # input worksheet
        with open(file=args.importfile, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=",", doublequote=False, lineterminator="\r")
            
            # set header
            h_row_count = 1
            h_col_count = 1
            for h in reader.fieldnames:
                wk.update_cell(h_row_count, h_col_count, h)
                h_col_count += 1

            # set value
            fileds = reader.fieldnames
            v_row_count = 2
            for row in reader:
                v_col_count = 1
                for f in fileds:
                    wk.update_cell(v_row_count, v_col_count, row[f])
                    v_col_count += 1
                v_row_count += 1

    except:
        raise
    finally:
        info(sheet)
    
    print('Complete🎉')
    return 0

def info(sheet: Spreadsheet):
    print()
    print('##### SpredSheet Info #####')
    print('* ID    : ', sheet.id)
    print('* URL   : ', sheet.url)
    print()

main()