import csv


def overwrite_data(filepath):
    fieldnames = ['id', 'name', 'player_score', 'comp_score', 'computerHasAce', 'decision']

    with open(filepath, "w+", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


def get_length(filepath):
    with open("data.csv", "r", newline='') as csvfile:
        reader = csv.reader(csvfile)
        reader_list = list(reader)
        print(reader_list)
    return len(reader_list)


def append_data(filepath, name, player_score, comp_score, comp_has_ace, decision):
    fieldnames = ['id', 'name', 'player_score', 'comp_score', 'computerHasAce', 'decision']
    next_id = get_length(filepath)

    with open(filepath, "a", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({
            "id": int(next_id),
            "name": name,
            "player_score": int(player_score),
            "comp_score": int(comp_score),
            "computerHasAce": bool(comp_has_ace),
            "decision": bool(decision),
        })


overwrite_data("data.csv")
append_data("data.csv", "johnny", 21, 19, 1, 0)
append_data("data.csv", "mary", 20, 21, 0, 0)
append_data("data.csv", "mary", 20, 21, 0, 0)
append_data("data.csv", "mary", 20, 21, 0, 0)
append_data("data.csv", "mary", 20, 21, 0, 0)
append_data("data.csv", "mary", 20, 21, 0, 0)
append_data("data.csv", "mary", 20, 21, 0, 0)



