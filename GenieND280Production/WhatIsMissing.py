#!/usr/bin/python

import sys
import pickle
import subprocess
import math

#oa_gn_beam_91200002-0090_xphtzo4a6xha_anal_000_prod005magnet201011airb-bsdv01.root
#or
#oa_gn_xxx_91203000-0000_6vgsiuvte6e4_anal_000_prod005basket201011airncpizero-bsdv01.root

def getRunAndSubrun(filename):
  handle = filename
  dash = handle.find('-')
  run = handle[dash-8:dash]
  subrun = handle[dash+1:dash+5]
  return int(run), int(subrun)

filedir = sys.argv[1]
outfilename = 'Missing.pkl'
print len(sys.argv)
if len(sys.argv) > 2:
  outfilename = sys.argv[2]
dir = filedir[:filedir.rfind('/')]

runs = {}
duplicates = []
missing = {}
anoms = []
fileSizes  = []
checkSizes = True
print dir
lsStr = subprocess.Popen('ls -l '+dir, shell=True,
                         stdout=subprocess.PIPE).communicate()[0]

lsFileList = lsStr.split('\n')


for fileLine in lsFileList:
  if len(fileLine)>0 and '.root' in fileLine.split()[-1]:
    info = fileLine.split()
    size = int(info[4])
    file = info[8]
    file = file[file.rfind('/')+1:]
    fileSizes.append((size, file))
    if 'root' not in file:
      print 'wtf?', file
      sys.exit()
    run, subrun = getRunAndSubrun(file)
    #run = int(file[11:19])
    #subrun = int(file[20:24])
    if run not in runs.keys():
      runs[run] = []
    if subrun in runs[run]:
      duplicates.append((run,subrun))
    runs[run].append(subrun)


nExpected = 0
nMissing = 0
nSubRuns = 100
for run in runs.keys():
  thisRun = runs[run]
  thisRun.sort()
  if len(thisRun) != nSubRuns:
    print len(thisRun), run
  if thisRun != range(0,nSubRuns):
    print '--------------------------------------------------------'
    print 'something is amiss with this run', run
    print 'Number of elements', len(thisRun)
    for i in range(len(thisRun)-1):
      if thisRun[i] == thisRun[i+1]:
        print 'Something wrong with', i, '?'
      if thisRun[i+1] - thisRun[i] > 1:
        print 'Something wrong with', i+1, '?'
    print thisRun
    print '--------------------------------------------------------'
  nExpected += max(thisRun)+1
  for i in range(min(thisRun), max(thisRun)+1):
    if i not in thisRun:
      if run not in missing.keys():
        missing[run] = []
      missing[run].append(i)
      nMissing += 1
  
print '%(miss)i missing out of %(exp)i expected, or %(div).2f%% completion' %\
        {"miss":nMissing, "exp":nExpected, "div":100-100*float(nMissing)/nExpected}
for run in missing.keys():
  print run, missing[run]

if len(duplicates) > 0:
  print 'Found Duplicates:'
  for dupe in duplicates:
    print dupe

outFile = open(outfilename, 'w')
pickle.dump(missing, outFile)
sizes, files = zip(*fileSizes)
avgSize = sum(sizes)/len(sizes)
cutoff = 0.15
for size, file in fileSizes:
  if math.fabs(size-avgSize)/float(avgSize) > cutoff: 
    anoms.append((file, size))
    print '  Size of file', file, 'is >',float(100*cutoff),'% different from avg file size!' 
    print '    Avg:', avgSize, 'this file size:', size
pickle.dump(anoms, outFile)
outFile.close()

