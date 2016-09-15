import feedparser as fp
from datetime import datetime
import time
import pytz

ALERTS_URL = 'http://www.metroalerts.info/rss.aspx?rs'
LINES = ['BLUE', 'GREEN', 'ORANGE', 'RED', 'SILVER', 'YELLOW']

# DATA_TIMEZONE = pytz.timezone('GMT')
DATA_TIMEZONE = pytz.timezone('UTC')
LOCAL_TIMEZONE = pytz.timezone('US/Eastern')


def shorten_summary(summary):
    return summary[summary.find(': ') + 2:]


def entry_list_to_md(entries):
    if not entries:
        return '*No alerts.*'

    return '\n'.join('- ' + summary for summary, _ in sorted(entries, key=lambda x: x[1]))


header_str = 'Here are the current WMATA metrorail alerts:'

footer_str = '*Last updated {}*'.format(
    datetime.ctime(datetime.now())
)

d = fp.parse(ALERTS_URL)

lines = {line: [] for line in LINES}

for entry in d['entries']:
    parsed = entry['published_parsed']
    t = time.mktime(parsed)
    dt = datetime.fromtimestamp(
            t
        )
    raw_time = DATA_TIMEZONE.localize(
        dt
    )

    # print(entry['published'])
    # print(entry['published_parsed'])
    # print(raw_time)

    local_time = raw_time.astimezone(LOCAL_TIMEZONE)

    # print(local_time)
    # print(local_time.ctime())
    # print('\n')

    # summary = '{} ({})'.format(shorten_summary(entry['summary']), local_time.ctime())
    summary = shorten_summary(entry['summary'])
    lines[entry['title']].append((summary, local_time))

elements = []

for line in LINES:
    entries = lines[line]
    elements.append('__{}__'.format(line))
    elements.append(entry_list_to_md(entries))

body_str = '\n\n'.join(elements)

with open('post.md', 'w') as f:
    f.write('\n\n'.join([header_str, body_str, footer_str]))
