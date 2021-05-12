from cli import parse_commandline_args
from datetime import datetime

# e.g. python cmd_create.py --importfile ./sample.csv --credentials ./.local/secret.json --share example@gmail.com
def main():
    """ Main Process

    Args:
        none
    Returns:
        code (int): exit status code.
    """
    try:
        args = parse_commandline_args()

        # create sheet title
        titlePrefix = args.title
        if not (args.title):
            titlePrefix = "NewReport"
        now = datetime.now()
        title = titlePrefix + '_' + str(now.year) + str(now.month).zfill(2) + str(now.day).zfill(2) + str(now.hour).zfill(2) + str(now.minute).zfill(2) + str(now.second).zfill(2)

        print(title)
        return 0
    except:
        return -1

main()