#!/usr/bin/python

# Standardised method of managing SSH access to our servers. This script hopefully can be used
# to wrap SSH key management and can log and expire SSH keys configured within the authorized_keys file.

import sys, re, os, getopt, time

USAGE = """Usage: manage.py [command] (options)

Note: all commands expect list write to a file: newauth which you can update authorized_keys with afterwards.

Commands and options:
  list - show list of keys, their id, enabled/disabled and expiry.
  export - print how authorized_keys should appear considering expiry and enabled/disabled.
  delete [id] - delete a key by id.
    e.g. manage.py delete bakersl
  add [id, public key, expiry (yyyy-MM-dd)] - Add a key with an id and expiry.
    e.g. manage.py add bakersl "AAAAB3NzaC1yc2EA...vIuuRniQ==" 2020-01-01
  enable [id] - enable a key by id.
    e.g. manage.py enable bakersl
  disable [id] - disable a key by id.
    e.g. manage.py disable bakersl
"""

# used for highlighting expiries in summaries
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
# end ansi flag for colours
ENDC = '\033[0m'
    
class Entry:
  def __init__(self, id, key, enabled, expiry):
    self.id = id
    self.key = key
    self.enabled = enabled
    self.expiry = expiry
    
  def expired(self):
    now = time.strftime("%Y-%m-%d")
    return now > self.expiry
    
  def printSummary(self):
    keyslice = "%s...%s" % (entry.key[0:10], self.key[-10:])
    colour = GREEN
    if self.expired():
      colour = RED
    if not self.enabled:
      colour = YELLOW
    
    summary = ("%s: %s. Enabled: %s. Expires: %s." % (self.id, keyslice, self.enabled, self.expiry))
    print(colour + summary + ENDC)
    
  def printKeyEntry(self, file):
    prefix = ""
    if self.expired() or not self.enabled:
      prefix = "#"
    file.write("%sssh-rsa %s %s:%s\n" % (prefix, self.key, self.id, self.expiry))

    
def write(current):
  f = open('newauth', 'w')
  f.write("#### KEY MANAGEMENT EXPORT AS AT %s ####\n" % (time.strftime("%Y-%m-%d %H:%M:%S")))
  [ entry.printKeyEntry(f) for entry in current ]
  f.close()
  

def list(authKeys):
  entries = []
  f = open(authKeys, 'r')
  for line in f:
    match = re.search("^(#*)ssh-rsa (.+) (.+):([0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9])$", line)
    if match:
      entries.append(Entry(match.group(3), match.group(2), (match.group(1) != "#"), match.group(4)))
  return entries
    

def findAuthorizedKeys():
  possiblities = [ "/.ssh/authorized_keys", "/.ssh/authorized_keys2", "/../.ssh/authorized_keys", "/../.ssh/authorized_keys2" ]
  for possibility in possiblities:
    keyFile = ("%s" + possibility) % os.environ['HOME']
    if os.path.isfile(keyFile):
      return keyFile
  
  print("Could not find authorized_keys")
  sys.exit(1)
    
    
def findById(list, id, exitIfNotFound):
  for found in list:
    if found.id == id:
      return found
  
  if exitIfNotFound:
    print("Could not find by id: %s" % id)
    sys.exit(1)
  
    
if len(sys.argv) < 2:
  print(USAGE)
  sys.exit(1)

authKeys = findAuthorizedKeys()
current = list(authKeys)
option = sys.argv[1]
if option == "list":
  [ entry.printSummary() for entry in current ]
  sys.exit(0)
  
if option == "export":
  write(current)
  sys.exit(0)
 
if option == "enable" and len(sys.argv) == 3:
  id = sys.argv[2]
  update = findById(current, id, True)
  update.enabled = True
  write(current)
  sys.exit(0)

if option == "disable" and len(sys.argv) == 3:
  id = sys.argv[2]
  update = findById(current, id, True)
  update.enabled = False
  write(current)
  sys.exit(0)
  
if option == "delete" and len(sys.argv) == 3:
  id = sys.argv[2]
  updated = []
  remove = findById(current, id, True)
  for entry in current:
    if entry.id != remove.id:
      updated.append(entry)
   
  write(updated)
  sys.exit(0)
 
if option == "add" and len(sys.argv) == 5:
  id = sys.argv[2]
  key = sys.argv[3]
  expiry = sys.argv[4]
  exists = findById(current, id, False)
  if findById(current, id, False):
    print("%s already exists" % id)
    sys.exit(1)

  current.append(Entry(id, key, True, expiry))
  write(current)
  sys.exit(0)
 
print(USAGE)
sys.exit(1)