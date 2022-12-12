import csv
import sys

ROOMS_FILE = '_rooms/negotiation.txt'


def create_rooms_from_csv_file(csv_file):
    """
    Create rooms from csv file
    """
    rooms = []
    try:
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                # if progreess is 100%
                if row[4] == '100':
                    rooms.append(row[8])
    except Exception as e:
        print(e)
    finally:
        return rooms

def export_rooms_to_txt_file(rooms, txt_file):
    """
    Export rooms to txt file
    """
    with open(txt_file, 'w') as f:
        for room in rooms:
            f.write(room + '\n')

if __name__ == '__main__':
    args = sys.argv
    if len(args) != 2:
        print('Usage: python create_rooms.py <csv_file>')
        exit(1)
    csv_file = args[1]
    rooms = create_rooms_from_csv_file(csv_file)
    export_rooms_to_txt_file(rooms, ROOMS_FILE)
    print(f'Exported {len(rooms)} rooms to {ROOMS_FILE}')