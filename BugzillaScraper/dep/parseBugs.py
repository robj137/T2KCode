#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

#wget --no-check-certificate --load-cookies cookies.txt -O test.txt 'https://bugzilla.nd280.org/show_bug.cgi?id=234'
import os
#curl -k --cookie cookies.txt 'https://bugzilla.nd280.org/show_bug.cgi?id=67' | grep bz_component

y = open('nd280reconbugs.txt')

bugs = {}
for line in y:
  bugN = int(line.split(',')[0])
  package = line.split(',')[1].strip().rstrip()
  summary = line.split(',')[2].strip().rstrip()
  bugs[bugN] = (package, summary)

openBugs = {}
z = open('currentBugs.txt')
for line in z:
  if len(line)>0:
    openBugs[int(line.split()[0])] =  line.split()[1]

print len(openBugs)
output = []
keys = bugs.keys()
keys.sort()
cats = {}
cats['enh'] = 'Enhancement'
cats['min'] = 'Minor'
cats['maj'] = 'Major'
cats['cri'] = 'Critical'
for bug in keys:
  if bug in openBugs.keys():
    package, summary = bugs[bug]
    cat = cats[openBugs[bug]]
    tableLine = '<tr><td>'+str(bug)+'</td><td>'+cat+'</td><td>'+package+'</td><td>'+summary+'</td></tr>'
    output.append(tableLine)


for line in output:
  print line
