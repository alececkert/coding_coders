
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

letter=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

for file_name in letter:
    with open(f'People/{file_name}_people.json', 'r') as file:
        data = json.load(file)


    almaMaterlabels = [record.get("ontology/almaMater_label", None) for record in data]

    # Filter out None values
    almaMaterlabels = [label for label in almaMaterlabels if label is not None]


    #print(almaMaterlabels)

    Name_Uni_Networth = [
        {
            "name": record.get("http://www.w3.org/2000/01/rdf-schema#label", None),
            "almaMater": record.get("ontology/almaMater_label", None),
            "networth": record.get("ontology/networth", None)
        }
        for record in data
    ]

    filtered_Unis = [entry for entry in Name_Uni_Networth if entry["name"] and entry["almaMater"] and entry ["networth"]]


    #for entry in filtered_Unis:
    #   print (f"Name: {entry['name']}, University: {entry['almaMater']} , networth: {entry['networth']}")

    ivy_league_alumni = [entry for entry in filtered_Unis if entry["almaMater"] in ivy_league_universities]


for entry in ivy_league_alumni:
    print(f"Name: {entry['name']}, University: {entry['almaMater']}, networth: {entry['networth']}")