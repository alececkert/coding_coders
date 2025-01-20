
import json

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

#ivy_league_universities = [uni.lower() for uni in ivy_league_universities]

with open("People/A_people.json", "r") as file:
    data_A = json.load(file)

almaMaterlabels = [record.get("ontology/almaMater_label", None) for record in data_A]

# Filter out None values
almaMaterlabels = [label for label in almaMaterlabels if label is not None]


#print(almaMaterlabels)

Name_and_Uni = [
    {
        "name": record.get("http://www.w3.org/2000/01/rdf-schema#label", None),
        "almaMater": record.get("ontology/almaMater_label", None),
    }
    for record in data_A
]

filtered_Unis = [entry for entry in Name_and_Uni if entry["name"] and entry["almaMater"]]


#for entry in filtered_Unis:
    #print(f"Name: {entry['name']}, University: {entry['almaMater']}")
ivy_league_alumni = [entry for entry in filtered_Unis if entry["almaMater"] in ivy_league_universities]


for entry in ivy_league_alumni:
    print(f"Name: {entry['name']}, University: {entry['almaMater']}")