"""Python program to fetch HIRLAM FMI surface temperature data from AWS.
   - Use the current date/time to fetch the most recent data
   - Download the temperature only (not modular/flexible code)
   - store the results in numerical-hirlam74-forecast-Temperature.grb2

"""

from datetime import datetime, timedelta
import s3fs

def get_lastfile(fs, output_prefix):
    # datetime object containing current date and time
    current_date = datetime.now()
    print("Current date and time =", current_date)
    s3path = 's3://fmi-opendata-rcrhirlam-surface-grib/' + current_date.strftime("%Y") + '/' + \
              current_date.strftime("%m") + '/' + current_date.strftime("%d") + '/*/' + \
              output_prefix + '-*.grb2'
    remote_files = fs.glob(s3path)
    if len(remote_files) <= 0:
        previous_date = current_date - timedelta(days=1)
        s3path = 's3://fmi-opendata-rcrhirlam-surface-grib/' + previous_date.strftime("%Y") + '/' + \
                  previous_date.strftime("%m") + '/' + previous_date.strftime("%d") + '/*/' + \
                  output_prefix + '-*.grb2'
        remote_files = fs.glob(s3path)
    if len(remote_files) <= 0:
        latest_file = ""
    else:
        latest_file = remote_files[-1]
    return latest_file

def main():

    fs = s3fs.S3FileSystem(  
            anon=True,
            client_kwargs={"endpoint_url": "http://s3-eu-west-1.amazonaws.com" },
        )

    output_prefix = 'numerical-hirlam74-forecast-Temperature'
    latest_file = get_lastfile(fs, output_prefix)
    if latest_file != "":
        fs.download('s3://' + latest_file, output_prefix + '.grb2')

if __name__ == "__main__":
    main()
