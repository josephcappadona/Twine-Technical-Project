from find_pairs import find_pairs
from data_io import parse_people_csv, parse_config_csv, save_groups_data
import sys


def main():
    args = sys.argv
    if len(args) < 4:
        print "Usage: python twine.py people.csv config.csv outfile.csv"
        exit(1)
    people_filename = args[1]
    config_filename = args[2]
    output_filename = args[3]

    people = parse_people_csv(people_filename)
    config = parse_config_csv(config_filename)
    groups = find_pairs(people, config)

    save_groups_data(groups, output_filename)
    

if __name__ == '__main__':
    main()
