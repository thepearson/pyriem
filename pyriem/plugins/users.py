try:
  import psutil
except ImportError:
  print "Module 'psutil' required"


def logged_in():
  values = []
  users = psutil.get_users()
  for user in users:
    values.append(
      {
        'name': user.name,
        'terminal': user.terminal,
        'host': user.host,
        'started': user.started,
      }
    )
  return values
