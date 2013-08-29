#!/usr/bin/python

import os
import sys


def usage():
  print ' '
  print 'Usage:', sys.argv[0], 'run subrun1 subrun2 ...\n'
  print 'This script only allows purging within one run at a time, but'
  print 'you can purge as many subruns within that run as you wish'
  print ' '

if len(sys.argv) < 3:
  usage()
  sys.exit()

pwd = os.environ['PWD']
print pwd



if pwd[-7:] != 'staging':
  print 'You really should be running this from the \'staging\' directory'
  sys.exit()

run = int(sys.argv[1])
subruns = []
for arg in sys.argv[2:]:
  subruns.append(int(arg))


dirs = ['anal', 'cali', 'elmc', 'g4mc', 'reco']

toPurge = []

for subrun in subruns:
  runHandle = '%(run)03i-%(subrun)04i'%{"run":run, "subrun":subrun}
  print runHandle
  for dir in dirs:
    for path, derps, files in os.walk('../'+dir+'/'):
      for file in files:
        if runHandle in file:
          toPurge.append('../'+dir+'/'+file)

print 'These are the files that will be deleted!'
for file in toPurge:
  print file

doIt = raw_input('Do you want to purge the above files??? [y/n]')
if doIt == 'y' or doIt == 'Y':
  for file in toPurge:
    cmd = 'rm '+file
    print cmd
    os.system(cmd)


