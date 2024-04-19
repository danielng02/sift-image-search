from collections import defaultdict

from tinydb import TinyDB

def rangeQuery(range):
    matches_db = TinyDB('matches_db.json')
    all_records = matches_db.all()

    all_records_dict = defaultdict(list)
    for record in all_records:
        all_records_dict[record['image1_name']].append(record)

    passing_matches = {}
    for image, records in all_records_dict.items():
        high_score_records = [record for record in records if int(record['score']) >= range]
        passing_matches[image] = high_score_records

    return passing_matches

def knnQuery(knn):
    matches_db = TinyDB('matches_db.json')
    all_records = matches_db.all()
    
    all_records_dict = defaultdict(list)
    for record in all_records:
        all_records_dict[record['image1_name']].append(record)

    passing_matches = {}
    for image, records in all_records_dict.items():
        top_k_records = sorted(records, key=lambda record: record['score'], reverse=True)[:knn]
        passing_matches[image] = top_k_records

    return passing_matches