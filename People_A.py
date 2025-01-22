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

# identify unis in the original data
university_keys = [
    "ontology/almaMater_label",
    "ontology/education_label"   
]

# list all files with each letter of the alphabet
letter=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# create empty list to store the data in
non_ivy_league_alumni = []
ivy_league_alumni = []

# loop through all files
# load the json data 
for file_name in letter:
    with open(f'People/{file_name}_people.json', 'r') as file:
        data = json.load(file)

    # create a list with name, uni, and networth
    filtered_data = []
    # check if person has: name, uni, AND networth
    for person in data:
        if "http://www.w3.org/2000/01/rdf-schema#label" in person and \
           ("ontology/almaMater_label" in person or "ontology/education_label" in person) and \
           "ontology/networth" in person:

            # collect all education entries - from almaMater and education_label
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
            
            
            birth_year = person.get("ontology/birthYear","N/A")

            # add person's details to the filtered data
            filtered_data.append({
                "name": person.get("http://www.w3.org/2000/01/rdf-schema#label"),
                "education": education,
                "networth": person.get("ontology/networth"),
                "birthYear": birth_year
            })

    # filter for people that went to an ivy league uni and for people that didn't
    for alumnus in filtered_data:
        education = alumnus["education"]
        
        if any(ivy_uni in alma for alma in education for ivy_uni in ivy_league_universities):
            ivy_league_alumni.append(alumnus)
        else:
            non_ivy_league_alumni.append(alumnus)       
            
# add TRUE to the people that went to an ivy league uni
for entry in ivy_league_alumni:
   entry['ivy_league'] = True
   print(f"Name: {entry['name']}, University: {entry['education']}, Networth: {entry['networth']}")

# add FALSE to the people that didn't go to an ivy league uni
for entry in non_ivy_league_alumni:
    entry['ivy_league'] = False
    print(f"Name: {entry['name']}, University: {entry['education']}, Networth: {entry['networth']}")

headers = ["name", "ivy_league", "education", "networth", "birthYear"]
headers_without_birth_year = ["name", "ivy_league", "education", "networth"]

def filter_fields(data, fields):
    return [{key: item.get(key, "") for key in fields} for item in data]

def remove_NA(data):
    return [person for person in data if person.get("birthYear") not in ["", "N/A"]]

def born_after_1920(data):
    return [
        person for person in data
        if isinstance(person.get("birthYear"), (str, int))
        and str(person.get("birthYear")).isdigit()  #ensures birthYear is numeric characters. NO LETTERSSS
        and 1920 < int(person["birthYear"]) < 1991
    ]
    

ivy_league_alumni_filtered = remove_NA(ivy_league_alumni)
non_ivy_league_alumni_filtered = remove_NA(non_ivy_league_alumni)

ivy_after_1920 = born_after_1920(ivy_league_alumni_filtered)
non_ivy_after_1920 = born_after_1920(non_ivy_league_alumni_filtered) 

#make a csv with ppl that went to an ivy. 
with open("ivy_league.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, headers_without_birth_year)
    writer.writeheader()
    writer.writerows (filter_fields(ivy_league_alumni, headers_without_birth_year))

#make a csv with ppl ppl that went to a non ivy 
with open("non_ivy_league.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, headers_without_birth_year)
    writer.writeheader()
    writer.writerows (filter_fields(non_ivy_league_alumni, headers_without_birth_year))

#make a csv with both ivy and non-ivy.
with open("combined.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, headers_without_birth_year)
    writer.writeheader()
    writer.writerows(filter_fields(ivy_league_alumni, headers_without_birth_year))
    writer.writerows(filter_fields(non_ivy_league_alumni, headers_without_birth_year))

#make a csv with both ppl that attended ivy and non-ivy AND their birth year
with open("with_birth_year_after_2019.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, headers)
    writer.writeheader()
    writer.writerows(ivy_after_1920)  
    writer.writerows(non_ivy_after_1920)
