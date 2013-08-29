#!/usr/bin/python
#
#############################################################################
#
# Title: ND280 MCP directory structure initialization script
#
# Usage: This script should be called from the base production directory, i.e.
#        /nfs/wafflesciences/t2k/production005/
#
#        Ensure you have the desired generators, baselines, volumes and 
#        MC types set in the cardname. The cardname should have the following
#        format:
'''
production:     5
respin:         E
nuMCType:       genie
verify:         True
version:        v10r11p9
'''
#        the whole directory structure as defined here:
#        http://www.t2k.org/nd280/datacomp/howtoaccessdata/directorystructure 
#        and here:
#        http://www.t2k.org/nd280/datacomp/mcproductionruns/production004.
#        Note, the actual sample configurations are generated using 
#        conditionals within the loop below.
#
#        Finally, this script will link the configuration file creation scripts
#        and the job submission scripts into each sample directory, and you
#        should call them from there
#
#        This script was lovingly stolen and modified from Patrick DePerio's 
#        mk_dir.sh SciNet script
#############################################################################

import os
import sys

def fillFromCard(cardname):
  input = open(cardname, 'r')
  lines = []
  dirDict = {}
  for line in input:
    dirDict[line.split(':')[0]] = line.split(':')[1].strip()
  
  keyCheck = ['production', 'respin', 'nuMCType', 'verify', 'version']
  dirKeys = dirDict.keys()
  for key in keyCheck:
    if key not in dirKeys:
      print 'Check', cardname, 'for proper format, could not find \'%s\' key'%key
      sys.exit()
  return dirDict

def checkCombination(baseline, vol, beamType):
  if vol == 'magnet':
    if 'beam' not in beamType or beamType == 'beam':
      return False # only beama or beamb for magnet
    if baseline == '2010-02-water':
      if beamType != 'beama':
        return False # only beama for 2010-02-water
      return True # 2010-02-water beama magnet
    if '2010-11' in baseline:
      if (beamType != 'beamb') and (beamType != 'beamc'):
        return False # beamb for Run2, beamc for Run3
      return True # 2010-11-water/air beamb/c magnet
  if vol == 'basket':
    if '2010-11' not in baseline:
      return False # only 2010-11 for basket
    if 'beam' in beamType and len(beamType) > 4:
      return False #no full spill
    return True # 2010-11 water/air basket {beam, nue, pistuff)

def makePath(aList):
  path = ''
  for item in aList:
    path += str(item)+'/'
  path = path[0:-1] # strip out the last /
  return path

def main():
  createDirs = False
  if len(sys.argv) == 2:
    cardName = sys.argv[1]
  else:
    print 'Need to provide the cardname'
    sys.exit()
  inp = raw_input('Create Directories for real?:')
  if inp.title() == 'Y':
    createDirs = True
  else:
    createDirs = False
  
  dirDict = fillFromCard(cardName)
  #god help you if you don't run this not from the  production directory
  prodDir = os.environ['PWD'] 
  print 'Production Directory is', prodDir
  
  linkedFiles = ['MCJobClass.py','CreateCfgFile.py','SubmitJob.py','Purge.py']
  linkedFiles.append('CountDirMissing.py')
  copiedFiles = ['runInfo.card']
  respin = dirDict['respin']
  simName = dirDict['nuMCType']
  version = dirDict['version']
  
  baselines = ['2010-02-water', '2010-11-water', '2010-11-air']
  volumes = ['magnet', 'basket']
  beamTypes = ['beam','beama','beamb','beamc','ccpiplus','ccpizero','ncpiplus','ncpizero','nue']
  
  if dirDict['verify'] == 'True':
    simName = 'verify/'+version+'/'+simName
    volumes = ['magnet']
    beamTypes = ['beam', 'beama', 'beamb', 'beamc']

  for baseline in baselines:
    for volume in volumes:
      for beamType in beamTypes:
        if checkCombination(baseline, volume, beamType):
          print '\nCreating file for:\n', respin, simName, baseline, volume,
          print beamType
          # a good combination, so let's make a directory!
          subdirs=['anal','cali','dats','elmc','g4mc','gnmc','numc','nucp','reco','staging','logf']
          dirs = [makePath([prodDir,respin])]
          for subdir in subdirs:
            dirs.append(makePath([prodDir, respin, 'mcp', simName, baseline,
                        volume, beamType, subdir]))
          for step in ['nd280', 'nucp', 'numc']:
            for substep in ['logs', 'cfg', 'scripts']:
              subdir = step+'/'+substep
              path = makePath([prodDir,respin,'mcp',simName,baseline,volume, 
                              beamType, 'staging', subdir])
              dirs.append(path)
          for dir in dirs:
            cmd = 'mkdir -m 775 -p '+dir
            print cmd
            if createDirs:
              os.system(cmd)
            if dir[-7:] == 'staging':
              cmds = []
              for file in linkedFiles:
                cmds.append('ln -sf '+prodDir+'/'+file+' '+dir)
              for file in copiedFiles:
                cmds.append('cp '+prodDir+'/'+file+' '+dir)
              for cmd in cmds:
                print cmd
                if createDirs:  
                  os.system(cmd)

if __name__ == '__main__':
  main()
