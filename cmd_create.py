from gspread.models import Spreadsheet
from cli import parse_commandline_args
from config import Configuration
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# e.g. python cmd_create.py --importfile ./data/example.csv --credentials ./.local/secret.json --share example@gmail.com --title Sample
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