
import json

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

with open("People/A_people.json", "r") as file:
    data_A = json.load(file)

# create a list with all univeristies
almaMaterlabels = []
for label in data_A:
    almaMaterlabels.append(label.get("ontology/almaMater_label", None))

# filter out none values
filtered_almaMater = []
for university in almaMaterlabels:
    if university is not None:
        filtered_almaMater.append(university)

#print(filtered_almaMater)

# select data with name, almaMater, and networth all together
Name_Uni_Networth = [
    {
        "name": label.get("http://www.w3.org/2000/01/rdf-schema#label", None),
        "almaMater": label.get("ontology/almaMater_label", None),
        "networth": label.get("ontology/networth", None)
    }
    for label in data_A
]

# create a list with name, uni, and networth
filtered_data = []
for data in Name_Uni_Networth:
    if data["name"] and data["almaMater"] and data["networth"]:
        filtered_data.append(data)

#for entry in filtered_data:
 #   print (f"Name: {entry['name']}, University: {entry['almaMater']} , networth: {entry['networth']}")

# filter for only people that went to an ivy league uni
ivy_league_alumni = []
for alumnus in filtered_data:
    if alumnus["almaMater"] in ivy_league_universities:
        ivy_league_alumni.append(alumnus)


for entry in ivy_league_alumni:
    print(f"Name: {entry['name']}, University: {entry['almaMater']}, Networth: {entry['networth']}")