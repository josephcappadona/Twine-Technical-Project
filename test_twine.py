from find_pairs import compute_attribute_fit, compute_fit, find_pairs
from data_io import (
    parse_people_csv,
    parse_config_csv,
    parse_groups_csv,
    save_groups_data)
import os


TEST_DATA_DIR = "test_data/"
example1_people = parse_people_csv(TEST_DATA_DIR+'example1_people.csv')
example1_config = parse_config_csv(TEST_DATA_DIR+'example1_config.csv')
example1_groups = parse_groups_csv(TEST_DATA_DIR+'example1_groups.csv')

example2_people = parse_people_csv(TEST_DATA_DIR+'example2_people.csv')
example2_config = parse_config_csv(TEST_DATA_DIR+'example2_config.csv')
example2_groups = parse_groups_csv(TEST_DATA_DIR+'example2_groups.csv')


def test_parse_people_csv():
    res = []

    res.append("Adam" in example1_people)
    res.append("Diana" in example1_people)

    res.append("gender" in example1_people["Adam"])
    res.append("occupation" not in example1_people["Adam"])

    res.append("Male" == example1_people["Adam"]["gender"])
    res.append("USA" == example1_people["Adam"]["country"])
    res.append("Green" == example1_people["Adam"]["color"])
    res.append("Female" == example1_people["Diana"]["gender"])
    res.append("Canada" == example1_people["Diana"]["country"])
    res.append("Blue" == example1_people["Diana"]["color"])

    return all(res)


def test_parse_config_csv():
    res = []

    config = example1_config
    res.append("gender" in config)
    res.append("country" in config)
    res.append("color" in config)
    res.append(("different", 10) == config["gender"])
    res.append(("similar", 5) == config["country"])
    res.append(("similar", 1) == config["color"])

    return all(res)


def test_parse_groups_csv():
    res = []

    groups = example1_groups
    res.append("Adam" in groups[0]["people"])
    res.append("Cathy" in groups[0]["people"])
    res.append(16 == groups[0]["fit"])

    res.append("Bob" in groups[1]["people"])
    res.append("Diana" in groups[1]["people"])
    res.append(15 == groups[1]["fit"])

    return all(res)


def test_compute_attribute_fit():
    res = []

    res.append(1 == compute_attribute_fit("Male", "Male", "similar"))
    res.append(0 == compute_attribute_fit("Male", "Female", "similar"))
    res.append(0 == compute_attribute_fit("Male", "Male", "different"))
    res.append(1 == compute_attribute_fit("Male", "Female", "different"))

    return all(res)


def test_compute_fit():
    res = []

    people = example1_people
    config = example1_config
    res.append(0+0+0 == compute_fit(people["Adam"], people["Bob"], config))
    res.append(10+5+1 == compute_fit(people["Adam"], people["Cathy"], config))
    res.append(10+0+0 == compute_fit(people["Adam"], people["Diana"], config))
    res.append(10+0+0 == compute_fit(people["Bob"], people["Cathy"], config))
    res.append(10+5+0 == compute_fit(people["Bob"], people["Diana"], config))
    res.append(0+0+0 == compute_fit(people["Cathy"], people["Diana"], config))

    return all(res)


def test_find_pairs():
    res = []

    groups1 = find_pairs(example1_people, example1_config)
    res.append(groups1 == example1_groups)

    groups2 = find_pairs(example2_people, example2_config)
    res.append(groups2 == example2_groups)

    return all(res)


def test_save_groups_data():
    filename = 'sample_groups.csv'

    did_save = save_groups_data(example1_groups, filename)
    sample_groups = parse_groups_csv(filename)
    os.remove(filename)

    return example1_groups == sample_groups


def main():
    print "parse_people_csv Tests:", test_parse_people_csv()
    print "parse_config_csv Tests:", test_parse_config_csv()
    print "parse_groups_csv Tests:", test_parse_groups_csv()
    print "compute_attribute_fit Tests:", test_compute_attribute_fit()
    print "compute_fit Tests:", test_compute_fit()
    print "find_pairs Tests:", test_find_pairs()
    print "save_groups_data Tests:", test_save_groups_data()


if __name__ == '__main__':
    main()
