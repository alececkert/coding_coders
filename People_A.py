
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
    
]

non_ivy_league_alumni = []

letter=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
filtered_almaMater = []
ivy_league_alumni = []

for file_name in letter:
    with open(f'People/{file_name}_people.json', 'r') as file:
        data = json.load(file)

    #print(filtered_almaMater)

    # select data with name, almaMater, and networth all together
    # Name_Uni_Networth = [
    #     {
    #         "name": label.get("http://www.w3.org/2000/01/rdf-schema#label"),
    #         "almaMater": label.get("ontology/almaMater_label"),
    #         "networth": label.get("ontology/networth")
    #     }
    #     for label in data
    # ]

    # create a list with name, uni, and networth
    filtered_data = []
    for person in data:
        if "http://www.w3.org/2000/01/rdf-schema#label" in person and \
           ("ontology/almaMater_label" in person or "ontology/education_label" in person) and \
           "ontology/networth" in person:
            education = []
            if "ontology/almaMater_label" in person:
                if isinstance(person["ontology/almaMater_label"], list):
                    education.extend(person["ontology/almaMater_label"])
                else:
                    education.append(person["ontology/almaMater_label"])
            
            if "ontology/education_label" in person:
                if isinstance(person["ontology/education_label"], list):
                    education.extend(person["ontology/education_label"])
                else:
                    education.append(person["ontology/education_label"])

            filtered_data.append({
                "name": person.get("http://www.w3.org/2000/01/rdf-schema#label"),
                "education": education,
                "networth": person.get("ontology/networth")
            })

    #for entry in filtered_data:
     #  print (f"Name: {entry['name']}, University: {entry['almaMater']} , networth: {entry['networth']}")

    # filter for only people that went to an ivy league uni
    for alumnus in filtered_data:
        education = alumnus["education"]
        
        if any(ivy_uni in alma for alma in education for ivy_uni in ivy_league_universities):
            ivy_league_alumni.append(alumnus)
        else:
            non_ivy_league_alumni.append(alumnus)       
            

        


for entry in ivy_league_alumni:
   entry['ivy_league'] = True
   print(f"Name: {entry['name']}, University: {entry['education']}, Networth: {entry['networth']}")

for entry in non_ivy_league_alumni:
    entry['ivy_league'] = False
    print(f"Name: {entry['name']}, University: {entry['education']}, Networth: {entry['networth']}")

with open("ivy_league.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, ["name", "ivy_league", "education", "networth"])
    writer.writeheader()
    writer.writerows(ivy_league_alumni)

with open("non_ivy_league.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, ["name", "ivy_league", "education", "networth"])
    writer.writeheader()
    writer.writerows(non_ivy_league_alumni)

with open("combined.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, ["name", "ivy_league", "education", "networth"])
    writer.writeheader()
    writer.writerows(ivy_league_alumni)
    writer.writerows(non_ivy_league_alumni)