
import json

with open("People/A_people.json", "r") as file:
    data_A = json.load(file)
<<<<<<< HEAD
    
=======

>>>>>>> refs/remotes/origin/main
almaMaterlabels = [record.get("ontology/almaMater_label", None) for record in data_A]

# Filter out None values if needed
almaMaterlabels = [label for label in almaMaterlabels if label is not None]

# Print the results
print(almaMaterlabels)

