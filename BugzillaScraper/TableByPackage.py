#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import pickle


y = open('currentBugzilla.pkl')
bugDict = pickle.load(y)
packages = ['oaRecon', 'oaRecPack', 'fgdRecon', 'tpcRecon', 'ecalRecon']
packages.extend(['smrdRecon','p0dRecon','trackerRecon','RECPACK','p0decalRecon'])
packages.sort()
packDict = {}
for package in packages:
  packDict[package] = []
keys = bugDict.keys()
keys.sort()
other = []
enhancements = []
major = []
minor = []
critical = []
for key in keys:
  if 'RESOLVED' not in bugDict[key][2]:
    packDict[bugDict[key][3]].append((key, bugDict[key]))
    if 'critical' in bugDict[key][0]:
      critical.append((key,bugDict[key]))
    if 'minor' in bugDict[key][0]:
      minor.append((key,bugDict[key]))
    if 'major' in bugDict[key][0]:
      major.append((key,bugDict[key]))
    elif 'enhancement' in bugDict[key][0]:
      enhancements.append((key,bugDict[key]))
    else:
      other.append((key, bugDict[key]))
print '<table class="vertical listing">'
print '<thead>'
print '<tr><th colspan="4">Critical and Major Bugs, sorted by Package</th></tr>'
print '<tr><th>Bug ID</th><th>Severity</th><th>Package</th><th>Summary</th></tr></thead>'
theKeys = packDict.keys()
theKeys.sort()
packageBlock = []
for package in theKeys:
  badBugs = 0
  del packageBlock[:]
  packageBlock.append('<tr><th colspan="4">'+package+'</th></tr>')
  packageBlock.append('<tbody>')
  for bug, bugInfo in packDict[package]:
    if 'critical' in bugInfo[0]  or 'major' in bugInfo[0]:
      badBugs += 1
      bugline = '<tr><td><a href="https://bugzilla.nd280.org/show_bug.cgi?id='+str(bug)
      bugline +='" target="_blank">'+str(bug)+'</a></td>'
      bugline +='<td>'+str(bugInfo[0])+'</td>'
      bugline +='<td>'+str(bugInfo[3])+'</td>'
      bugline +='<td>'+str(bugInfo[1])+'</td></tr>'
      packageBlock.append(bugline)
  packageBlock.append('</tbody>')
  if badBugs > 0:
    for line in packageBlock:
      print line
print '</table>'
