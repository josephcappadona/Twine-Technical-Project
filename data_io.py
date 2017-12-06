def parse_people_csv(filename):
    parsed_csv = parse_csv(filename)
    attribute_labels = parsed_csv.pop(0)

    people_info = {}
    for person_info in parsed_csv:
        name = person_info.pop(0)
        people_info[name] = {}
        for i, label in enumerate(attribute_labels[1:]):
            people_info[name][label] = person_info[i]
    return people_info


def parse_config_csv(filename):
    parsed_csv = parse_csv(filename)
    config = {attribute: (direction, int(weight))
              for attribute, direction, weight in parsed_csv}
    return config


def parse_groups_csv(filename):
    parsed_csv = parse_csv(filename)
    attribute_labels = parsed_csv.pop(0)    # assume this returns ['group', 'fit', 'name']

    groups = {}
    for group, fit, name in parsed_csv:
        group = int(group)
        fit = int(fit)
        if group not in groups:
            groups[group] = {}
            groups[group]['people'] = set()
            groups[group]['fit'] = None

        groups[group]['people'].add(name)
        groups[group]['fit'] = fit
    return groups


def parse_csv(filename):
    data = []
    with open(filename) as f:
        for line in f.read().splitlines():
            data.append(line.split(','))
    return data


def save_groups_data(groups, filename):
    labels = ['group', 'fit', 'name']
    data = []
    data.append(labels)

    for group_num, group_info in sorted(groups.items()):
        fit = group_info['fit']
        for name in sorted(group_info['people']):
            data.append([group_num, fit, name])

    return save_csv(data, filename)


def save_csv(data, filename):
    with open(filename, 'w+') as f:
        for i, datum in enumerate(data):
            f.write(','.join([str(e) for e in datum]))
            if i != len(data)-1:
                f.write('\n')
