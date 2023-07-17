import os
import os.path
import sys
import shutil
import pkg_resources
import datetime
import docworker
import uuid

def note_user_access(db, name):
  """
  Update last access time for the user.
  """
  now = datetime.datetime.now()
  
  db.execute("UPDATE user SET last_access = ? WHERE username = ?",
               (now.timestamp(), name))
  db.commit()

def get_user_by_key(db, key):
  """
  Lookup user for key and return user name
  """
  result = db.execute(
    "SELECT username FROM user WHERE access_key = ?",
    (key,)).fetchone()
  if result is not None:
    return result[0]
  return None

def get_user_key(db, name):
  """
  Lookup a user by name and return the access key
  Return None if doesn't exist
  """
  result = db.execute(
    "SELECT access_key FROM user WHERE username = ?",
    (name,)).fetchone()
  if result is not None:
    return result[0]
  return None

  
def token_count(db, name):
  """
  Return number of tokens available.
  """
  (consumed, limit) = db.execute(
    "SELECT consumed_tokens, limit_tokens FROM user WHERE username = ?",
    (name,)).fetchone()
  return limit - consumed
  
  
def increment_tokens(db, name, count):
  """
  Update the token count.
  """
  (tokens,) = db.execute("SELECT consumed_tokens FROM user WHERE username = ?",
                     (name,)).fetchone()
  tokens += count
  db.execute("UPDATE user SET consumed_tokens = ? WHERE username = ?",
               (tokens, name))
  db.commit()

def check_available_tokens(db, name):
  """
  Check if the consumed_tokens are less than the limit tokens
  """
  (consumed, limit) = db.execute(
    "SELECT consumed_tokens, limit_tokens FROM user WHERE username = ?",
    (name,)).fetchone()
  
  return consumed < limit
  
  
def add_or_update_user(db, user_dir, name, limit):
  """
  Add a user if it doesn't exist. Otherwise update the limit.
  """
  (count,) = db.execute("SELECT COUNT(*) FROM user WHERE username = ?",
                     (name,)).fetchone()
  if count == 0:
    print("add user")
    db.execute("INSERT INTO user (username, access_key, limit_tokens) VALUES (?,?,?)",
               (name, uuid.uuid4().hex, limit))
    populate_samples(user_dir)
  else:
    print("update user")
    db.execute("UPDATE user SET limit_tokens = ? WHERE username = ?",
               (limit,name))
  db.commit()


def populate_samples(user_dir):
  """
  Copy sample docs into user dir.
  """
  print("user dir = %s" % user_dir)
  samples_dir = pkg_resources.resource_filename('docworker', 'samples')
  print("samples dir = %s" % samples_dir)  
  if not os.path.exists(samples_dir):
    print("%s not found" % samples_dir)

  if not os.path.exists(user_dir):    
    os.makedirs(user_dir)
  for filename in os.listdir(samples_dir):
    if filename.endswith(".daf"):
      shutil.copyfile(os.path.join(samples_dir, filename),
                      os.path.join(user_dir, filename))
  print("done")
  

def list_users(db):
  q = db.execute("SELECT id, username, access_key, consumed_tokens, limit_tokens, last_access FROM user")
  for (id, user, access_key, consumed, limit, last_access) in q.fetchall():
    dt = datetime.datetime.fromtimestamp(last_access)
    print("user: [%d] %s (%s), limit: %d, consumed %d, last access: %s" %
          (id, user, access_key, limit, consumed, dt.isoformat(sep=' ')))


def get_or_create_user(name):
  """
  If user exists, return the access key.
  If user does not exist, create the account and return the access key.
  """
  return 'xxxx'
