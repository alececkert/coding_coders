
import json
import csv

# insert ivy league universities
ivy_league_universities = [
    "Harvard University",
    "Yale University",
    "Princeton University",
    "Columbia University",
    "University of Pennsylvania",
    "Dartmouth College",
    "Brown University",
    "Cornell University"
]

university_keys = [
    "ontology/almaMater_label",
    "ontology/education",
    "ontology/education_label",
    "ontology/university_label",
    "ontology/almaMater"
]

non_ivy_league_alumni = []

letter=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
filtered_almaMater = []
ivy_league_alumni = []

for file_name in letter:
    with open(f'People/{file_name}_people.json', 'r') as file:
        data = json.load(file)

    # create a list with all univeristies
    Universities = []
    for label in data:
        for university_key in university_keys:
            university = label.get(university_key)
            if university is not None:
                Universities.append(university)
        # universities = [
            #label.get("ontology/almaMater_label"),
            #label.get("ontology/education"),
            #label.get("ontology/education_label"),
            #label.get("ontology/university_label")
        #]

    # for university in Universities:
    #     if university is not None:
    #         Universities.append(university)

    print(filtered_almaMater)

    # select data with name, almaMater, and networth all together
    Name_Uni_Networth = [
        {
            "name": label.get("http://www.w3.org/2000/01/rdf-schema#label"),
            "almaMater": label.get(university_keys[0]),
            "networth": label.get("ontology/networth")
        }
        for label in data
    ]

    # create a list with name, uni, and networth
    filtered_data = []
    for data in Name_Uni_Networth:
        if data["name"] and data["almaMater"] and data["networth"]:
            filtered_data.append(data)

    for entry in filtered_data:
       print (f"Name: {entry['name']}, University: {entry['almaMater']} , networth: {entry['networth']}")

    # filter for only people that went to an ivy league uni
    for alumnus in filtered_data:
        if alumnus["almaMater"] in ivy_league_universities:
            ivy_league_alumni.append(alumnus)
        else:
            non_ivy_league_alumni.append(alumnus)


for entry in ivy_league_alumni:
   print(f"Name: {entry['name']}, University: {entry['almaMater']}, Networth: {entry['networth']}")

with open("results.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, ["name", "almaMater", "networth"])
    writer.writeheader()
    writer.writerows(ivy_league_alumni)

with open("non_ivy_league_results.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, ["name", "almaMater", "networth"])
    writer.writeheader()
    writer.writerows(non_ivy_league_alumni)