from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import argparse
import json
import re
import requests


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--profilux-url', type=str, default='http://localhost/sensordata.json')
    parser.add_argument('--influxdb-url', type=str, default='http://localhost:8086')
    parser.add_argument('--db', type=str, default='profilux', help='InfluxDB database name')
    parser.add_argument('--bucket', type=str, default='profilux', help='InfluxDB bucket name')
    parser.add_argument('--measurement', type=str, default='profilux', help='InfluxDB measurement name')

    parser.add_argument('--token', type=str, help='InfluxDB token')
    parser.add_argument('--org', type=str, default='profilux', help='InfluxDB organization')

    parser.add_argument('--username', type=str, help='InfluxDB username')
    parser.add_argument('--password', type=str, help='InfluxDB password')

    parser.add_argument('--basic-auth', action='store_true', help='Use basic authentication instead of token')

    args = parser.parse_args()

    # Check if we have either only a token or only a username/password
    if (args.token is None and (args.username is None or args.password is None)) or \
            (args.token is not None and (args.username is not None or args.password is not None)):
        parser.error('You must provide either a token or a username/password combination')

    client = InfluxDBClient(url=args.influxdb_url, token=args.token, org=args.org,
                            username=args.username, password=args.password, auth_basic=args.basic_auth)

    write_api = client.write_api(write_options=SYNCHRONOUS)

    response = requests.get(args.profilux_url)
    response_json = json.loads(response.text)

    # Write all sensor values to InfluxDB
    for sensor in response_json['sensors']:
        value = sensor['value'].strip()  # Remove leading and trailing whitespace
        if all(c == '-' for c in value):
            # Skip sensors with all dashes
            continue

        # Split value into number and unit
        split = re.split('([0-9.]+)', value)
        value, unit = float(split[1].strip()), split[2].strip()
        name = sensor['name'].strip()

        # Write sensor value to InfluxDB
        point = Point(args.measurement).tag('name', name).tag('unit', unit).field('value', value)
        write_api.write(bucket=args.bucket, record=point)


if __name__ == '__main__':
    main()
