
import json
import csv

# insert ivy league universities
ivy_league_universities = [
    "Harvard",  
    "Princeton",
    "Columbia",
    "Pennsylvania",
    "Dartmouth",
    "Brown",
    "Cornell",
    "Yale"
]

university_keys = [
    "ontology/almaMater_label",
    "ontology/education_label",
    "ontology/university_label"
    
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
                if isinstance(university, str) and university.startswith('[') and university.endswith(']'):
                    university = json.loads(university)
                if isinstance(university, list):
                    Universities.extend(university)
        

    #print(filtered_almaMater)

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

    #for entry in filtered_data:
     #  print (f"Name: {entry['name']}, University: {entry['almaMater']} , networth: {entry['networth']}")

    # filter for only people that went to an ivy league uni
    for alumnus in filtered_data:
        Education = alumnus["almaMater"]
        
        
        if isinstance(Education, list):
          
            if any(ivy_uni in alma for alma in Education for ivy_uni in ivy_league_universities):
                ivy_league_alumni.append(alumnus)
            else:
                non_ivy_league_alumni.append(alumnus)
        elif any(ivy_uni in Education for ivy_uni in ivy_league_universities):
                ivy_league_alumni.append(alumnus)
        else:
                non_ivy_league_alumni.append(alumnus)          
            

        


for entry in ivy_league_alumni:
   print(f"Name: {entry['name']}, University: {entry['almaMater']}, Networth: {entry['networth']}")

for entry in non_ivy_league_alumni:
    print(f"Name: {entry['name']}, University: {entry['almaMater']}, Networth: {entry['networth']}")

with open("ivy_league.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, ["name", "almaMater", "networth"])
    writer.writeheader()
    writer.writerows(ivy_league_alumni)

with open("non_ivy_league.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, ["name", "almaMater", "networth"])
    writer.writeheader()
    writer.writerows(non_ivy_league_alumni)