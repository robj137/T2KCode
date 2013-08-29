#!/usr/local/python-2.6.2-X86_64/bin/python

import os
import sys
import string
import MCJobClass
import MCConfigClass
import pickle



def parseMissingFileList(aFile):
  y = open(aFile)
  missingDict = pickle.load(y)
  y.close()
  return missingDict
 
def main(): 
  runInfo = MCJobClass.MCRunInfoClass()
  runCfgInfo = MCConfigClass.MCConfigClass(runInfo)
  if len(sys.argv) == 1:
    runCfgInfo.Usage()
    sys.exit()
  if len(sys.argv) == 2:
    arg = sys.argv[1]
    if arg.title() == 'Help':
      Usage()
      sys.exit()
    if arg.title() == 'hardcoded':
      for run in range(0,8):
        for subrun in range(0, 100):
          runCfgInfo.submitJob(run, subrun)
    if '.pkl' in sys.argv[1]:
      missingDict = parseMissingFileList(sys.argv[1])
      for run in missingDict.keys():
        for subrun in missingDict[run]:
          runCfgInfo.submitJob(run%1000,subrun)
  if len(sys.argv) == 3:
    runs = runCfgInfo.parseRunSubrunArgs(sys.argv[1])
    subs = runCfgInfo.parseRunSubrunArgs(sys.argv[2])
    for runN in runs:
      for subN in subs:
        runCfgInfo.submitJob(runN, subN)

  

if __name__ == '__main__':
  main()
