try:
  import time
except ImportError:
  print "Requirement: 'time' module not found."

try:
  import MySQLdb
except ImportError:
  print "Requirement: 'os' module not found."

try:
  import os
except ImportError:
  print "Requirement: 'os' module not found."


default_settings = {
  'connection': {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'db': 'mysql'
  },
  'limit': []
}

def status(settings = None):

  if not settings:
    settings = default_settings

  data_rows = []
  db = MySQLdb.connect(host=settings['connection']['host'],
                       user=settings['connection']['user'],
                       passwd=settings['connection']['password'],
                       db=settings['connection']['db'])
  cur = db.cursor()
  cur.execute("SHOW STATUS")

  for row in cur.fetchall():
    if settings['limit']:
      if row[0] in settings['limit']:
        data = {
          'host': os.uname()[1],
          'service': row[0],
          'metric': row[1],
          'state': 'ok',
          'time': int(time.time()),
          'tags': [__name__],
        }
        data_rows.append(data)
    else:
      data = {
        'host': os.uname()[1],
        'service': row[0],
        'metric': row[1],
        'state': 'ok',
        'time': int(time.time()),
        'tags': [__name__],
      }
      data_rows.append(data)

  return data_rows