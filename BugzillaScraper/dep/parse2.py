#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import os
import subprocess
import pickle

def getBugPackageInfo(bugID):
  url = "https://bugzilla.nd280.org/show_bug.cgi?id="+str(bugID)
  href = '<a href="'+url+'" target = "_blank">'+str(bugID)+'</a>'
  cmd = "curl -k --cookie cookies.txt '"+url+"' |grep bz_component"
  #cmd = "curl -k --cookie cookies.txt 'https://bugzilla.nd281.org/show_bug.cgi?id="+str(bugID)+"' | grep bz_component"
  d = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate()[0]
  if 'bz_component' in d and 'bz_bug' in d:
    m1 = d.find('bz_component_')+13
    m2 = d.find('bz_bug_')-1
    return d[m1:m2], href
  return 'G4+1', None

def getBugNumberSeveritySummary(bugBlock):
  lines = bugBlock.split('\n')
  if 'bz' in lines[1]:
    bug = -1
    summary = 'Blah'
    severity = 'Lame'
    lBug = lines[4]
    lSummary = lines[21]
    lSeverity = lines[9]
    #m1 = lBug.find('"')+2
    #m2 = lBug.rfind('"')
    #bug = int(lBug[m1:m2])
    bug = int(lBug[lBug.find('"')+2:lBug.rfind('"')])
    summary = lSummary[lSummary.find('>')+1:]
    severity = lSeverity[lSeverity.rfind('>')+1:]
    return bug, severity, summary
  return 0, 0, 0
  #if '<a name="' in line:
  #return 1

cmd = "curl -k --cookie cookies.txt 'https://bugzilla.nd280.org/buglist.cgi?query_format=advanced&short_desc_type=allwordssubstr&short_desc=&long_desc_type=substring&long_desc=&bug_file_loc_type=allwordssubstr&bug_file_loc=&deadlinefrom=&deadlineto=&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&emailassigned_to1=1&emailtype1=substring&email1=&emailassigned_to2=1&emailreporter2=1&emailcc2=1&emailtype2=substring&email2=&bugidtype=include&bug_id=&chfieldfrom=&chfieldto=Now&chfieldvalue=&cmdtype=doit&order=Reuse+same+sort+as+last+time&field0-0-0=component&type0-0-0=substring&value0-0-0=recon&field0-0-1=component&type0-0-1=substring&value0-0-1=recpack'"

d = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate()[0]
bugblocks = d.split('bz_bugitem')

bugs = {}
for bug in bugblocks:
  bug, severity, summary = getBugNumberSeveritySummary(bug)
  if bug:
    bugs[bug] = (severity, summary)



output = []
keys = bugs.keys()
keys.sort()
cats = {}
cats['enh'] = 'Enhancement'
cats['min'] = 'Minor'
cats['maj'] = 'Major'
cats['cri'] = 'Critical'
for bug in keys:
  package, href = getBugPackageInfo(bug)
  severity, summary = bugs[bug]
  cat = cats[severity]
  tableLine = '<tr><td>'+href+'</td><td>'+cat+'</td><td>'+package+'</td><td>'+summary+'</td></tr>'
  output.append(tableLine)

outFile = open('currentBugzilla.pkl', 'w')
pickle.dump(output, outFile)
outFile.close()
for line in output:
  print line
