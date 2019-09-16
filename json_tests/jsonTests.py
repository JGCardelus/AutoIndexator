import json
import os

raw_file = open('json_tests\\test.txt', 'r')
table = json.load(raw_file)

for person in table["people"]:
    print(person["firstName"])
    for child in person["children"]:
        child["hobbies"] = ["a", "b", "c"]

with open('json_tests\\test.txt', 'w') as out_file:
    json.dump(table, out_file)

