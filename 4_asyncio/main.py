from src import database
from src import parser


if __name__ == '__main__':
    while True:
        choice = input('Download new/missing files? (Y/N): ')
        if choice == 'Y' or choice == 'y':
            files = parser.get_files(missing=True)
            parser.download_files(files)
        elif choice != 'N' and choice != 'n':
            print('Sorry, try again.')
            continue
        database.add_to_db(parser.get_files())
        exit()
