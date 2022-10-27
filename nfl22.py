from pathlib import Path 
from graph import Graph
from pprint import pprint as pp 
from time import time


files = [f for f in Path('./matchups/NFL22').glob("*")]


def load_file(filepath):
    with open(filepath, 'r') as fp:
        lines = fp.readlines()

    body = lines[1:]

    results = []
    for l in body:
        away, home, winner = l.strip("\n").split(",")
        if winner == '-':
            continue
        if winner == home:
            results.append((winner, away))
        else:
            results.append((winner, home))
    return results 


def get_all_teams(results):
    all_teams = set()
    for week in results:
        for game in week:
            all_teams.update(game)
    return all_teams

if __name__ == '__main__':
    results = [load_file(f) for f in files]

    start = time()

    g = Graph(directed=True)
    for res in results:
        g.add_connections(res)
    longest = g.find_longest_cycle()
    print(len(longest), longest)

    for team in get_all_teams(results):
        if team != "Eagles":

            g = Graph(directed=True)
            for res in results:
                g.add_connections(res)
            g.add(team, "Eagles")
            cycle = g.find_longest_cycle()

            result = len(cycle) == 32

            print("{}: {}".format(team, result))

    print("Time elapsed: {}".format(time()-start))