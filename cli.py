import argparse
import os

def parse_commandline_args():
    """ Parse commandline argument

    Parse the command line arguments.It also checks for the existence of files and directories.

    Args:
        none
    Returns:
        void
    """

    parser = argparse.ArgumentParser()

    # set optional flag
    parser.add_argument('-i', '--importfile', help='set up a csv file', required=True)
    parser.add_argument('-c', '--credentials', help='set your credentials', required=True)
    parser.add_argument('-s', '--share', help='set up an account for the user you want to shar', required=True)
    parser.add_argument('-t', '--title', help="set the title of the sheet")

    args = parser.parse_args()

    if not (os.path.exists(args.importfile)):
        raise FileNotFoundError(args.importfile + ' not such file or directory')

    if not (os.path.exists(args.credentials)):
        raise FileNotFoundError(args.credentials + ' not such file or directory')

    # parsing & return
    return parser.parse_args()