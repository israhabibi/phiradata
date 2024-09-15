import argparse
from datetime import datetime, timedelta

today = datetime.now().strftime('%Y-%m-%d')
yestday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

parser = argparse.ArgumentParser()
parser.add_argument('-s', action='store', dest='start_date', default=today, nargs='?')
parser.add_argument('-e', action='store', dest='end_date', default=yestday, nargs='?')

args = parser.parse_args()

if args.start_date == today:
    h = today
    h_1 = yestday
    print(h, h_1)
else:
    h = args.start_date
    h_1 = args.end_date
    print(h, h_1)