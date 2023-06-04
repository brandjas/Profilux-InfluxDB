from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import argparse


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--profilux-url', type=str, default='http://localhost/sensordata.html')
    parser.add_argument('--influxdb-url', type=str, default='http://localhost:8086')
    parser.add_argument('--db', type=str, default='profilux', help='InfluxDB database name')
    parser.add_argument('--bucket', type=str, default='profilux', help='InfluxDB bucket name')
    parser.add_argument('--measurement', type=str, default='profilux', help='InfluxDB measurement name')
    parser.add_argument('--token', type=str, required=True, help='InfluxDB token')
    parser.add_argument('--org', type=str, required=True, help='InfluxDB organization')

    args = parser.parse_args()

    client = InfluxDBClient(url=args.influxdb_url, token=args.token, org=args.org)
    write_api = client.write_api(write_options=SYNCHRONOUS)


if __name__ == '__main__':
    main()
