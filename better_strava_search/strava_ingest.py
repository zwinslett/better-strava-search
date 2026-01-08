from typing import Any
import login as login
import requests
import sqlite3


def get_token() -> dict[str, str]:
    payload = {
        'client_id': f'{login.client_id}',
        'client_secret': f'{login.client_secret}',
        'refresh_token': f'{login.refresh_token}',
        'grant_type': 'refresh_token',
        'f': 'json'
    }

    print('Requesting Token...\n')
    token_object = requests.post('https://www.strava.com/oauth/token', data=payload, verify=False)
    access_token = token_object.json()['access_token']

    header = {'Authorization': 'Bearer ' + access_token}
    return header


def get_activities(header: dict[str, str], before: int, after: int, page: int) -> list[dict[str, Any]]:
    # start at page ...
    page = page
    # set new_results to True initially
    new_results = True
    # create an empty array to store our combined pages of data in
    data = []
    while new_results:
        # request a page + 200 results
        get_strava = requests.get('https://www.strava.com/api/v3/activities', headers=header, params={'per_page': 200,
                                                                                                      'page': f'{page}',
                                                                                                      'before': before,
                                                                                                      'after': after}).json()
        # save the response to new_results to check if its empty or not and close the loop
        new_results = get_strava

        if not get_strava:
            break
        else:
            # add our responses to the data array
            data.extend(get_strava)
            # Give some feedback
            print(f'You are requesting page {page} of your activities data ...')
            # increment the page
            page += 1
    # return the combine results of our get requests
    return data


def sync_strava_activities(activities: list[dict[str, Any]], header: dict[str, str]) -> None:
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    for activity in activities:
        if activity['type'] == 'Run':
            detailed_activity = requests.get(f"https://www.strava.com/api/v3/activities/{activity['id']}",
                                             headers=header).json()
            cur.execute("INSERT OR REPLACE INTO activities(id, start_date, elapsed_time, type, average_speed,"
                        "max_speed, average_cadence, average_heartrate, max_heartrate, suffer_score, calories, "
                        "gear_name, "
                        "description, distance, name) "
                        "VALUES(?,?, ?, ?, ?, "
                        "?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        [activity['id'], detailed_activity['start_date'], detailed_activity['elapsed_time'],
                         detailed_activity['type'], detailed_activity['average_speed'] * 2.237, detailed_activity['max_speed'] * 2.237,
                         detailed_activity['average_cadence'], detailed_activity['average_heartrate'],
                         detailed_activity['max_heartrate'], detailed_activity['suffer_score'], detailed_activity['calories'], detailed_activity['gear']['name'], detailed_activity['description'], detailed_activity['distance'] / 1609, detailed_activity['name']])
    conn.commit()


token = get_token()
data = get_activities(token, 1761797242, 1759291642, 1)
sync_strava_activities(data, token)
