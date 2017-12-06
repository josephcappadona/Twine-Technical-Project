def compute_attribute_fit(attribute1, attribute2, direction):
    if direction == "similar":
        return 1 * (attribute1 == attribute2)
    elif direction == "different":
        return 1 * (attribute1 != attribute2)
    return None


def compute_fit(person1, person2, config):
    fit_score = 0
    for attribute, (direction, weight) in config.items():
        attribute_fit = compute_attribute_fit(person1[attribute],
                                              person2[attribute], direction)
        fit_score += weight * attribute_fit
    return fit_score


def find_pairs(people_info, config):
    """First computes fit scores for all possible pairs of people. Then places
    people in pairs by finding the pair of people with the maximum fit score
    and removing them from the pool of potential matches. We then
    repeat this until all people have been matched. If a single person is left
    over, they are placed in their own group.

    Args:
        people_info (dict): Contains attribute info for each person,
            structure is {name: {attribute: val, }, }
        config (dict): Contains fit criteria,
            structure is {attribute: (direction, weight), }

    Returns:
        dict: Contains group information,
            structure is {group_num: {'people': set([person1, person2]),
                                      'fit': fit_score }, }
    """
    sorted_fits = {}    # key: name1, value: list of (name2, fit) tuples sorted (desc) by `fit`
    max_fit = {}        # key: name1, value: (name2, fit) tuple, where `fit` is name1's highest fit score among all unmatched people
    people = set(people_info.keys())

    # calculate fit scores for every possible pair of people
    for person in people_info:
        fits = {}
        for other_person in people.difference([person]):
            fits[other_person] = compute_fit(people_info[person],
                                             people_info[other_person], config)

        # sort (descending) by fit score
        sorted_fits[person] = sorted(fits.items(),
                                     key=lambda x: x[1], reverse=True)
        max_fit[person] = sorted_fits[person].pop(0)
        max_fit_person, max_fit_score = max_fit[person]

    unmatched_people = set(people_info.keys())
    groups = {}
    cur_group = 0
    while unmatched_people:
        # get (alphabetically first) pair with highest fit score
        max_fit_score = max([fit_score for _, fit_score in max_fit.values()])
        max_fit_people = [person for person, (_, fit)
                          in max_fit.items() if fit == max_fit_score]
        person1 = min(max_fit_people)   # get person whose name is alphabetically first
        person2 = max_fit[person1][0]   # get match for `person1`
        groups[cur_group] = {}
        groups[cur_group]['people'] = set([person1, person2])
        groups[cur_group]['fit'] = max_fit_score
        cur_group += 1

        # `person1` and `person2` can no longer be matched
        unmatched_people.remove(person1)
        unmatched_people.remove(person2)
        del max_fit[person1]
        del max_fit[person2]
        del sorted_fits[person1]
        del sorted_fits[person2]

        if len(unmatched_people) > 1:
            # prepare for next iteration
            # find next highest fit score for each person whose max fit person was `person1` or `person2`
            for person in unmatched_people:
                max_fit_person, max_fit_score = max_fit[person]
                if max_fit_person == person1 or max_fit_person == person2:
                    while max_fit_person not in unmatched_people:
                        # while loop in case this person's top two matches were `person1` and `person2`
                        max_fit_person, max_fit_score = sorted_fits[person].pop(0)
                    max_fit[person] = max_fit_person, max_fit_score
        elif len(unmatched_people) == 1:
            # odd number of people => place remaining person in his/her own group
            groups[cur_group] = {}
            groups[cur_group]['people'] = set([unmatched_people.pop()])
            groups[cur_group]['fit'] = 0

    return groups
