from collections import defaultdict

from tinydb import TinyDB
import pandas

def rangeQuery(range):
    matches_db = TinyDB('matches_db.json')
    all_records = matches_db.all()

    records_by_image = defaultdict(list)
    for record in all_records:
        records_by_image[record['image1_name']].append(record)

    high_score_records_by_image = {}
    for image, records in records_by_image.items():
        high_score_records = [record for record in records if int(record['score']) >= range]
        high_score_records_by_image[image] = high_score_records

    return high_score_records_by_image

def knnQuery(knn):
    matches_db = TinyDB('matches_db.json')
    all_records = matches_db.all()
    records_by_image = defaultdict(list)
    for record in all_records:
        records_by_image[record['image1_name']].append(record)

    top_two_records_by_image = {}
    for image, records in records_by_image.items():
        top_two_records = sorted(records, key=lambda record: record['score'], reverse=True)[:knn]
        top_two_records_by_image[image] = top_two_records

    return top_two_records_by_image

def json_to_df(data):
    dfs = []
    for key, values in data.items():
        df = pandas.DataFrame(values)
        try:  
            df['image1_name'] = df['image1_name'].apply(lambda x: x if isinstance(x, str) else x['path'])
            df['image2_name'] = df['image2_name'].apply(lambda x: x if isinstance(x, str) else x['path'])
            df['image'] = key
            dfs.append(df)
        except Exception as e:
            continue
    if dfs:
        return pandas.concat(dfs, ignore_index=True)
    return pandas.DataFrame()