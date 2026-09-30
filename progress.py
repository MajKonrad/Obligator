import json

FILE_NAME = "completed.json"

def load_completed():
    with open(FILE_NAME) as file:
        return json.load(file)


def mark_completed(assignment_id):
    completed = load_completed()

    if assignment_id not in completed:
        completed.append(assignment_id)

    with open(FILE_NAME, "w") as file:
        json.dump(completed, file)

def is_completed(assignment_id):
    completed = load_completed()
    return assignment_id in completed

def mark_undone(assignment_id):
    completed = load_completed()
    if assignment_id in completed:
        completed.remove(assignment_id)

    with open(FILE_NAME, "w") as file:
        json.dump(completed, file)

