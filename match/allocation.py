import random

# TODO
# Must clear existing match for all users (not just the ones who voted), then
# create an allocation for every user who did vote

def serial_dictatorship(users):
    random.shuffle(users)

    for u in users:
        u.match = None

        for o in u.rank_order:
            if not o.match:
                u.match = o
                break


def probabilistic_serial(users):
    # AKA "simultaneous eating"
    total_bites = 10
    options = set(sum([u.rank_order for u in users], []))
    bites_taken = {u: [] for u in users}
    bites_remaining = {o: total_bites for o in options}

    random.shuffle(users)

    # Unmatch all users first (in case a user doesn't rank all options and
    # ultimately ends up without a match)
    for u in users:
        u.match = None

    # One at a time, each user assigns a bite to the highest preference option
    # that isn't entirely "eaten"; once all users have taken enough bites to
    # fully "eat" one option, options are assigned to each user
    # probabilistically based on the number of bites they have taken of it
    for i in range(total_bites):
        for u in users:
            for o in u.rank_order:
                if bites_remaining[o]:
                    bites_taken[u].append(o)
                    bites_remaining[o] -= 1
                    break

    print(bites_taken)

    for u in users:
        if not bites_taken[u]:
            continue

        # Make the match
        u.match = random.choice(bites_taken[u])

        # Remove this option from all other users' bites_taken
        for i in users:
            bites_taken[i] = [q for q in bites_taken[i] if q is not u.match]

