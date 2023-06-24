# Profilux-InfluxDB
A simple script to put data from a Profilux aquarium controller in InfluxDB.

## Installing prerequisites

You can either use [Docker](https://www.docker.com/) or install the dependencies in a virtual environment.

### Docker

Make sure Docker is installed and running on your system. Then, run the
following command to build the Docker image:

```
docker build -t profilux-influxdb .
```

Verify that the image was built successfully by running:

```
docker run --rm -it profilux-influxdb -h
```

Note that you need to build the image again to reflect any changes to the
source code.

### Virtual environment

Install Python 3.10 or higher. Run `python3 -m venv venv` to create a virtual
in a new directory called `venv`. Then, activate the virtual environment with
`source venv/bin/activate` on Linux/macOS or `venv\Scripts\activate.bat` on
Windows. Finally, install the dependencies with `pip install -r requirements.txt`.

Verify that the installation was successful by running:

```
python3 main.py -h
```

## Usage

If you've followed the above instructions, you should now see the usage information. It should look something like this:
```
usage: main.py [-h] [--profilux-url PROFILUX_URL] [--influxdb-url INFLUXDB_URL] [--db DB] [--bucket BUCKET] [--measurement MEASUREMENT] [--token TOKEN] [--org ORG] [--username USERNAME] [--password PASSWORD] [--basic-auth] [--interval INTERVAL]

options:
  -h, --help            show this help message and exit
  --profilux-url PROFILUX_URL
  --influxdb-url INFLUXDB_URL
  --db DB               InfluxDB database name
  --bucket BUCKET       InfluxDB bucket name
  --measurement MEASUREMENT
                        InfluxDB measurement name
  --token TOKEN         InfluxDB token
  --org ORG             InfluxDB organization
  --username USERNAME   InfluxDB username
  --password PASSWORD   InfluxDB password
  --basic-auth          Use basic authentication instead of token
  --interval INTERVAL   Interval in seconds to query Profilux and write to InfluxDB (0 to run only once)
```

### Example

Here's an example:
```
docker run --rm -dt profilux-influxdb \
    --profilux-url http://<Profilux IP>/sensordata.json \
    --influxdb-url http://localhost:8086 \
    --org my-org \
    --bucket profilux \
    --measurement sensors \
    --token very-secret-token \
    --interval 60
```

This will query `http://<Profilux IP>/sensordata.json` every 60 seconds and write
the sensor data to InfluxDB. The token is used for authentication with InfluxDB.
Since we're passing the `-d` flag to `docker run`, the container will run in the
background.

If you're not using docker, simply replace `docker run --rm -dt profilux-influxdb`
with `python3 main.py`. Don't forget to activate the virtual environment before
running the command.

## Setting up Profilux

Use GHL Command Center or an FTP client to upload `sensordata.json` to Profilux.
Verify that it works as expected by visiting `http://<profilux-ip>/sensordata.json`
in your browser.

It should look something like this:
```json
{
    "sensors": [
        {
            "name": "pH-value 1",
            "short_name": "pH ",
            "operation_state": "+ ",
            "description": "Ph",
            "type": "2",
            "value": "   6.87pH"
        }, {
            "name": "Temperature 1",
            "short_name": "Temp ",
            "operation_state": "* ",
            "description": "Temp",
            "type": "1",
            "value": "    24.5C"
        }, {
            "name": "Conduct.(F) 1",
            "short_name": "Co.F ",
            "operation_state": "  ",
            "description": "",
            "type": "4",
            "value": "      ---"
        }, {
            "name": "Redox 1",
            "short_name": "Redx ",
            "operation_state": "  ",
            "description": "",
            "type": "3",
            "value": "      ---"
        }
    ]
}
```
