import json
from indexer import save4aria, print_info, save_links

with open('db.json', 'r') as jsondb:
    db = json.load(jsondb)

save4aria(db)
save_links(db)
print_info(db)