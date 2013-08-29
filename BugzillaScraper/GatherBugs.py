#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import subprocess
import pickle

def getBugPackageInfo(bugID):
  url = "https://bugzilla.nd280.org/show_bug.cgi?id="+str(bugID)
  href = '<a href="'+url+'" target = "_blank">'+str(bugID)+'</a>'
  cmd = 'curl -k --cookie cookies.txt '+url
  #cmd = "curl -k --cookie cookies.txt 'https://bugzilla.nd281.org/show_bug.cgi?id="+str(bugID)+"' | grep bz_component"
  component = 'G4+1'
  d = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate()[0]
  reported = 'Never'
  modified = 'Never'
  lines = d.split('\n')
  for n, line in enumerate(lines):
    if 'bz_component' in line and 'bz_bug' in line:
      m1 = line.find('bz_component_')+13
      m2 = line.find('bz_bug_')-1
      component = line[m1:m2]
    if 'Last modified' in line:
      modified = line[line.find('modified:')+10:line.rfind('</p>')]
    if 'Reported' in line:
      rep = lines[n+2]
      reported = rep[rep.find('<td>')+4:rep.find('by')]
  return component, reported, modified, href

def getBugNumberSeveritySummary(bugBlock):
  lines = bugBlock.split('\n')
  if 'bz' in lines[1]:
    stuff = lines[1].split('bz_')
    severity = stuff[1].rstrip()
    status = stuff[3].rstrip()
    bug = -1
    summary = 'Blah'
    lBug = lines[4]
    lSummary = lines[21]
    bug = int(lBug[lBug.find('"')+2:lBug.rfind('"')])
    summary = lSummary[lSummary.find('>')+1:]
    return bug, severity, summary, status
  return 0, 0, 0, 0
  #if '<a name="' in line:
  #return 1

def main():
  #cmd = "curl -k --cookie cookies.txt 'https://bugzilla.nd280.org/buglist.cgi?query_format=advanced&short_desc_type=allwordssubstr&short_desc=&long_desc_type=substring&long_desc=&bug_file_loc_type=allwordssubstr&bug_file_loc=&deadlinefrom=&deadlineto=&emailassigned_to1=1&emailtype1=substring&email1=&emailassigned_to2=1&emailreporter2=1&emailcc2=1&emailtype2=substring&email2=&bugidtype=include&bug_id=&chfieldfrom=&chfieldto=Now&chfieldvalue=&cmdtype=doit&order=Reuse+same+sort+as+last+time&field0-0-0=component&type0-0-0=substring&value0-0-0=recon&field0-0-1=component&type0-0-1=substring&value0-0-1=recpack'"
  cmd = "curl -L -k --cookie cookies.txt 'http://bit.ly/RUXELu'"

  d = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate()[0]
  bugblocks = d.split('bz_bugitem')

  bugs = {}
  for bug in bugblocks:
    bug, severity, summary, status = getBugNumberSeveritySummary(bug)
    if bug:
      bugs[bug] = [severity, summary, status]

  output = []
  keys = bugs.keys()
  keys.sort()
  for bug in keys:
    package, reported, modified, href = getBugPackageInfo(bug)
    bugs[bug].extend([package, reported, modified])
    print bugs[bug]
    #severity, summary, status = bugs[bug]
    #cat = severity 
    #tableLine = '<tr><td>'+href+'</td><td>'+cat+'</td><td>'+package+'</td><td>'+summary+'</td></tr>'
    #output.append(tableLine)

  outFile = open('currentBugzilla.pkl', 'w')
  pickle.dump(bugs, outFile)
  outFile.close()


if __name__ == '__main__':
  main()
