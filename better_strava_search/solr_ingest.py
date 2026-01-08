import sqlite3
import json
import requests


def sql_to_solr(db: str) -> None:
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute('SELECT id, start_date, elapsed_time, type, average_speed, max_speed, average_cadence, '
                   'average_heartrate, max_heartrate, suffer_score, calories, gear_name, description, distance, '
                   'name FROM activities')
    rows = cursor.fetchall()
    solr_url = 'http://localhost:8983/solr/activities/update?commit=true'
    headers = {'Content-Type': 'application/json'}
    solr_docs = []

    for row in rows:
        solr_docs.append({
            'id': row[0],
            'start_date_dt': row[1],
            'elapsed_time_i': row[2],
            'type_s': row[3],
            'average_speed_f': row[4],
            'max_speed_f': row[5],
            'average_cadence_f': row[6],
            'average_heartrate_i': row[7],
            'max_heartrate_i': row[8],
            'suffer_score_i': row[9],
            'calories_i': row[10],
            'gear_name_s': row[11],
            'description_t': row[12],
            'distance_f': row[13],
            'name_t': row[14]
        })
    post_to_solr = requests.post(solr_url, data=json.dumps(solr_docs), headers=headers)
    print(solr_docs)
    print(post_to_solr.status_code)
    print(post_to_solr.text)
    connection.close()


sql_to_solr('db.sqlite3')
