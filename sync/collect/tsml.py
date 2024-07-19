'''
Collect meeting data from TSML
'''
import hashlib
import json
import logging
import os
import re
import requests

import sync.collect
import sync.db

# Pattern to identify TSML-UI source data
TSML_RE = (
        r'<div id="tsml-ui"\s+'
        r'data-src="([^"]+\.json)[0-9?]*"\s+'
        r'data-timezone="([^"]+)"')

DAYS_OF_WEEK = {
        0: 'Sunday',
        1: 'Monday',
        2: 'Tuesday',
        3: 'Wednesday',
        4: 'Thursday',
        5: 'Friday',
        6: 'Saturday',
        7: 'Sunday'}


def refresh(subdomain, source_url):
    '''
    Refresh collected data from a remote Twelve-Step-Meeting-List (TSML) source
    '''
    # Fetch current meeting (tsml-ui) page
    response = requests.get(source_url)
    if response.status_code != 200:
        raise sync.collect.CollectionException(
                f'Unexpected response [{response.status_code}]')

    # Identify current source data url
    match = re.search(TSML_RE, response.text)
    if not match:
        raise sync.collect.CollectionException('No TSML source data found')
    data_src = match.group(1)
    data_timezone = match.group(2)
    source_json = f'{os.path.dirname(source_url)}{data_src}'

    # Calculate checksum-based cache name from full url
    url_checksum = hashlib.sha256(source_json.encode('utf-8')).hexdigest()
    cache_json = f'tsml_{url_checksum}.json'
    # cache_tz = f'tsml_{url_checksum}.tz'

    # Check if this json file has already been cached
    if sync.db.exists(cache_json):
        logging.info(f'{source_json} exists in cache; using local copy')
        source_data = json.loads(sync.db.get(cache_json))
    else:
        # Download TSML data
        response = requests.get(source_json)
        if response.status_code != 200:
            raise sync.collect.CollectionException(
                    f'Unexpected response [{response.status_code}]')
        # sync.db.set(cache_tz, data_timezone)  # always fresh from tsml-ui
        sync.db.set(cache_json, response.content)
        source_data = response.json()
        logging.info(f'Collected meeting data from {source_json}')

    # Normalize TSML source data
    collected = {}
    for meeting in source_data:
        # Check for required fields
        missed_fields = []
        for required in ['day', 'types']:
            if meeting.get(required) is None:
                missed_fields.append(required)
        if missed_fields:
            logging.warning(f'Skip {meeting["name"]}; missing {missed_fields}')
            logging.debug(f'Skipped Meeting: {meeting}')
            continue

        if meeting['slug'] not in collected:
            # Populate with initial data
            collected[meeting['slug']] = {
                    'name': meeting['name'],
                    'time': {},
                    # 'place': meeting[''],
                    'tz': meeting.get('timezone', data_timezone),
                    'address': meeting['formatted_address'],
                    'longitude': meeting['longitude'],
                    'latitude': meeting['latitude'],
                    'types': meeting['types'],
                    }

            # Optional values
            if meeting.get('notes'):
                collected[meeting['slug']]['note'] = meeting['notes']
            if meeting.get('location') or meeting.get('region'):
                collected[meeting['slug']]['keywords'] = '{} {}'.format(
                        meeting.get('location', ''),
                        meeting.get('region', ''))

        # Add meeting time to existing entry
        cm = collected[meeting['slug']]
        day = DAYS_OF_WEEK[meeting['day']]
        if day not in cm['time']:
            cm['time'][day] = [meeting['time']]
        else:
            cm['time'][day].append(meeting['time'])

    # Store collected data
    for slug, meeting in collected.items():
        geostore = json.dumps(sync.collect.validate(shortname=slug, **meeting))
        sync.db.geo_set(
                key=f'{subdomain}_{slug}',
                lon=meeting['longitude'],
                lat=meeting['latitude'],
                value=geostore)
