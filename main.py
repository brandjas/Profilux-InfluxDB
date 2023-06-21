from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import argparse


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--profilux-url', type=str, default='http://localhost/sensordata.json')
    parser.add_argument('--influxdb-url', type=str, default='http://localhost:8086')
    parser.add_argument('--db', type=str, default='profilux', help='InfluxDB database name')
    parser.add_argument('--bucket', type=str, default='profilux', help='InfluxDB bucket name')
    parser.add_argument('--measurement', type=str, default='profilux', help='InfluxDB measurement name')

    parser.add_argument('--token', type=str, help='InfluxDB token')
    parser.add_argument('--org', type=str, help='InfluxDB organization')

    parser.add_argument('--username', type=str, help='InfluxDB username')
    parser.add_argument('--password', type=str, help='InfluxDB password')

    args = parser.parse_args()

    # Check if we have either only a token or only a username/password
    if (args.token is None and (args.username is None or args.password is None)) or \
            (args.token is not None and (args.username is not None or args.password is not None)):
        parser.error('You must provide either a token or a username/password combination')

    client = InfluxDBClient(url=args.influxdb_url, token=args.token, org=args.org,
                            username=args.username, password=args.password)

    write_api = client.write_api(write_options=SYNCHRONOUS)


if __name__ == '__main__':
    main()
