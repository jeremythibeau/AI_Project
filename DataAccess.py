import csv


def overwrite_data(filepath):
    fieldnames = ['id', 'name', 'player_score', 'comp_score', 'computerHasAce', 'decision']

    with open(filepath, "w+", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

def create_score():
    fieldnames = ['name', 'win', 'loss', 'draw']
    with open('scoreboard.csv', "w+", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

def add_score(name, win, loss, draw):
    fieldnames = ['name', 'win', 'loss', 'draw']
    with open('scoreboard.csv', "a", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({
            "name": name,
            "win": int(win),
            "loss": int(loss),
            "draw": int(draw)
        })

def read_data(filepath):
    with open(filepath, "r", newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(row)

def get_length(filepath):
    with open("data.csv", "r", newline='') as csvfile:
        reader = csv.reader(csvfile)
        reader_list = list(reader)
    return len(reader_list)


def append_data(data):
    fieldnames = ['id', 'name', 'player_score', 'comp_score', 'computerHasAce', 'decision']
    next_id = get_length(data)

    with open(data[0], "a", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({
            "id": int(next_id),
            "name": data[1],
            "player_score": int(data[2]),
            "comp_score": int(data[3]),
            "computerHasAce": int(data[4]),
            "decision": data[5],
        })


'''overwrite_data("data.csv")
append_data("data.csv", "johnny", 21, 19, 1, 0)
append_data("data.csv", "mary", 20, 21, 0, 0)
append_data("data.csv", "mar", 20, 22, 0, 0)
append_data("data.csv", "may", 20, 23, 0, 0)
append_data("data.csv", "mry", 20, 24, 0, 0)
append_data("data.csv", "ary", 20, 25, 0, 0)
append_data("data.csv", "ma", 20, 26, 0, 0)
read_data("data.csv")'''



