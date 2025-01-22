
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
            
            
            birth_year = person.get("ontology/birthYear", "Unknown")

            filtered_data.append({
                "name": person.get("http://www.w3.org/2000/01/rdf-schema#label"),
                "education": education,
                "networth": person.get("ontology/networth"),
                "birthYear": birth_year
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

headers = ["name", "ivy_league", "education", "networth", "birthYear"]
headers_without_birth_year = ["name", "ivy_league", "education", "networth"]

def filter_fields(data, fields):
    return [{key: item.get(key, "") for key in fields} for item in data]

with open("ivy_league.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, headers_without_birth_year)
    writer.writeheader()
    writer.writerows (filter_fields(ivy_league_alumni, headers_without_birth_year))

with open("non_ivy_league.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, headers_without_birth_year)
    writer.writeheader()
    writer.writerows (filter_fields(non_ivy_league_alumni, headers_without_birth_year))

with open("combined.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, headers_without_birth_year)
    writer.writeheader()
    writer.writerows(filter_fields(ivy_league_alumni, headers_without_birth_year))
    writer.writerows(filter_fields(non_ivy_league_alumni, headers_without_birth_year))

with open("with birth year.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, headers)
    writer.writeheader()
    writer.writerows(ivy_league_alumni)  
    writer.writerows(non_ivy_league_alumni)