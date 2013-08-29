#!/usr/local/python-2.6.2-X86_64/bin/python

import os
import sys
import string
import random
import MCRunInfoClass

# system-dependent (filepath) stuff:
genieSetupPath = '/nfs/hepcode/t2k/GENIE/setup.sh'
passThruDir ='/nfs/dcache102/t2k/GNprod5/production005/A/mcp/genie/2010-11-'

#------------------------------------------------------------------------------ 
# MCConfigClass
#------------------------------------------------------------------------------ 

class MCConfigClass:
  def __init__(self,runInfo = 0):
    if runInfo == 0:
      print 'Please provide a valid RunInfo class'
    self.runInfo = runInfo
    self.cfgDict = {}
    self.setRunInfo()
    self.setBasePath()
    self.setPassThruDir()
    self.setSoftwareFields()
    self.setConfigFields()
    self.setFileNamingFields()
    self.setGeometryFields()
    self.setND280Fields()
    self.setCherryPickingFields()
    if runInfo.output == 'numc':
      #FIXME
      self.setNeutrinoFields()
    if runInfo.output == 'nd280':
      self.setSoftwareFields()
      self.setElectronicsCfgFields()
      self.setAnalysisFields()
      self.throwAgain()
    if runInfo.output == 'nucp':
      self.cfgDict['module_list'] = 'oaCherryPicker'
      self.cfgDict['num_events'] =  100000000
      self.throwAgain()
  
  def throwAgain(self):
    self.cfgDict['mc_seed'] = random.randint(0,9e8)
    self.cfgDict['elec_seed'] = random.randint(0,9e8)
    self.mcSeed = random.randint(0,9e8)
    self.elecSeed = random.randint(0,9e8)
    

    
#------------------------------------------------------------------------------ 
# Initial Setters
#------------------------------------------------------------------------------ 

  def setRunInfo(self):
    self.cfgDict['p0d_water_fill'] = 1
    self.mcPosition = 'free'
    if self.runInfo.fill == 'air':
      self.cfgDict['p0d_water_fill'] = 0
    self.cfgDict['mc_type'] = self.runInfo.mc
    if self.runInfo.fluxVolume == 'basket':
      self.nBunches = 1
      self.potPerSpill = 7.98913e13
      self.bunchDuration = 0
      self.timeOffset = 0
      self.countType = 'FIXED'
      self.interactionsPerSpill = 1
      #self.potPerSpill = 0
      self.mcFullSpill = 0
    
    if self.runInfo.fluxVolume == 'magnet':
      self.timeOffset = 50
      self.countType = 'MEAN'
      self.mcFullSpill = 1
      if self.runInfo.runN == 1:
        self.nBunches = 6
        self.potPerSpill = 3.66e13
        self.bunchDuration = 17
        self.interactionsPerSpill = 3.6210409
      if self.runInfo.runN == 2:
        self.nBunches = 8
        self.potPerSpill = 7.99e13
        self.bunchDuration = 19
        if self.runInfo.fill == 'water':
          self.interactionsPerSpill = 8.3507203
        if self.runInfo.fill == 'air':
          self.interactionsPerSpill = 8.3285105
      if self.runInfo.runN == 3:
        self.nBunches = 8
        self.potPerSpill = 9.462526e13
        self.interactionsPerSpill = 9.864719
        self.bunchDuration = 19

  def setBasePath(self):
    basePath = os.environ['PWD']
    basePath = basePath[0:basePath.rfind('staging')-1]
    self.basePath = basePath
  
  def setPassThruDir(self):
    if self.runInfo.respin == 'A':
      dir = self.basePath+'/numc'
    else:
      ptdir = self.basePath+'/numc'
      # just swap the respin in the path
      ndex = ptdir.find('/mcp')-1
      dir = ptdir[0:ndex]+'A'+ptdir[ndex+1:]
    if self.runInfo.usingNUCP:
      dir = self.basePath+'/nucp'
    if self.runInfo.output == 'nucp':
      dir = passThruDir
      dir += self.runInfo.fill+'/basket/beam/numc'
    if 'verify' in dir:
      version = self.runInfo.nd280Version
      start = dir[0:dir.find('verify')]
      end = dir[dir.find(version)+len(version)+1:]
      dir = start+end
    self.PassThruDir = dir
#------------------------------------------------------------------------------ 
# Set the nd280Control fields
#------------------------------------------------------------------------------ 

  #-----------------
  # [software]
  #-----------------
  def setSoftwareFields(self):
    self.cfgDict['[software]'] = []
    self.cfgDict['[software]'].append(('cmtpath', 'environment'))
    self.cfgDict['[software]'].append(('cmtroot', 'environment'))
    self.cfgDict['[software]'].append(('nd280ver', self.runInfo.nd280Version))
    if self.runInfo.output == 'numc':
      self.cfgDict['[software]'].append(('genie_setup_script', genieSetupPath))

  #-----------------
  # [configuration]
  #-----------------
  def setConfigFields(self):
    self.inputFile = None
    self.cfgDict['[configuration]'] = []
    modList = ''
    if self.runInfo.output == 'numc':
      modList = 'genieMC genieConvert'
    if self.runInfo.output == 'nd280':
      modList = 'nd280MC elecSim oaCalibMC oaRecon oaAnalysis'
    if self.runInfo.output == 'nucp':
      modList = 'oaCherryPicker'
    self.cfgDict['[configuration]'].append(('module_list', modList))

  #-----------------
  # [filenaming]
  #-----------------
  def setFileNamingFields(self):
    self.cfgDict['[filenaming]'] = []
    self.cfgDict['[filenaming]'].append(('run_number', None))
    self.cfgDict['[filenaming]'].append(('subrun', None))
    self.setComment()
    self.cfgDict['[filenaming]'].append(('comment', self.runInfo.Comment))

  #-----------------
  # [neutrino]
  #-----------------
  def setNeutrinoFields(self):
    self.NeutrinoCfg = True
    self.cfgDict['[neutrino]'] = []
    nuType = None
    fluxVolume = self.runInfo.fluxVolume
    fluxMasterVolume = self.runInfo.fluxMasterVolume
    if 'beam' in self.runInfo.beam:
      nuType = 'beam'
    else:
      nuType = self.runInfo.beam
    self.cfgDict['[neutrino]'].append(('neutrino_type',nuType))
    self.cfgDict['[neutrino]'].append(('master_volume', fluxMasterVolume.title()))
    self.cfgDict['[neutrino]'].append(('flux_region', fluxVolume))
    self.cfgDict['[neutrino]'].append(('flux_file', self.runInfo.fluxFile))
    self.cfgDict['[neutrino]'].append(('flux_tree', self.runInfo.fluxTree))
    self.cfgDict['[neutrino]'].append(('flux_file_pot',
                                         self.runInfo.fluxFilePOT))
    self.cfgDict['[neutrino]'].append(('pot', self.runInfo.fluxPOT))
    self.cfgDict['[neutrino]'].append(('genie_xs_table', self.runInfo.XSFile))
    self.cfgDict['[neutrino]'].append(('random_start', self.runInfo.randomStart))
    self.cfgDict['[neutrino]'].append(('genie_flux_probs_file_name',
                                         self.runInfo.fluxProbs))
  #-----------------
  # [analysis]
  #-----------------
  def setAnalysisFields(self):
    self.cfgDict['[analysis]'] = []
    self.cfgDict['[analysis]'].append(('pass_through_dir', self.PassThruDir))
    #self.cfgDict['NeutrinoCfg'].append(('random_seed', 

  #-----------------
  # [geometry]
  #-----------------
  def setGeometryFields(self):
    self.cfgDict['[geometry]'] = []
    self.cfgDict['[geometry]'].append(('baseline', self.runInfo.baseline))
    self.cfgDict['[geometry]'].append(('p0d_water_fill', self.runInfo.p0dwater))

  #-----------------
  # [electronics]
  #-----------------
  def setElectronicsCfgFields(self):
    self.cfgDict['[electronics]'] = []

  #-----------------
  # [nd280mc]
  #-----------------
  def setND280Fields(self):
    self.cfgDict['[nd280mc]'] = []
    self.cfgDict['[nd280mc]'].append(('mc_type', 'Genie'))
    if self.runInfo.output in ['nd280','nucp']:
      self.cfgDict['[nd280mc]'].append(('num_events', '100000000'))
      self.cfgDict['[nd280mc]'].append(('mc_full_spill', self.mcFullSpill))
      self.cfgDict['[nd280mc]'].append(('interactions_per_spill', 
                                        self.interactionsPerSpill))
      self.cfgDict['[nd280mc]'].append(('time_offset', self.timeOffset))
      self.cfgDict['[nd280mc]'].append(('count_type', self.countType))
      self.cfgDict['[nd280mc]'].append(('mc_position', self.mcPosition))
      
    if self.runInfo.output == 'nd280':  
      self.cfgDict['[nd280mc]'].append(('nbunches', self.nBunches))
      self.cfgDict['[nd280mc]'].append(('pot_per_spill', self.potPerSpill))
      self.cfgDict['[nd280mc]'].append(('bunch_duration', self.bunchDuration))


  #-----------------
  # [cherry_picker]
  #-----------------
  def setCherryPickingFields(self):
    self.cfgDict['[cherry_picker]'] = []
    if self.runInfo.output == 'nucp':
      self.cfgDict['[cherry_picker]'].append(('num_mesons', self.runInfo.nMesons))
      self.cfgDict['[cherry_picker]'].append(('num_leptons', self.runInfo.nLeptons))
      self.cfgDict['[cherry_picker]'].append(('num_mu_minus', self.runInfo.nMuMinus))
      self.cfgDict['[cherry_picker]'].append(('num_pizero', self.runInfo.nPiZero))
      self.cfgDict['[cherry_picker]'].append(('num_piplus', self.runInfo.nPiPlus))


#------------------------------------------------------------------------------ 
# Functions that are run for each file
#------------------------------------------------------------------------------ 
  
  def getCfgFileName(self, run, subrun):
    if self.runInfo.output == 'nd280':
      return self.basePath+'/staging/nd280/cfg/nd280-{0}-{1}.cfg'.format(run,subrun)
    if self.runInfo.output == 'numc':
      return self.basePath+'/staging/numc/cfg/numc-{0}-{1}.cfg'.format(run,subrun)
    if self.runInfo.output == 'nucp':
      return self.basePath+'/staging/nucp/cfg/nucp-{0}-{1}.cfg'.format(run,subrun)
  
  def setInputFileList(self):
    self.inputFileList = []
    run = self.runInfo.RunNumber
    subrun = self.runInfo.SubRunNumber
    for a, b, files in os.walk(self.PassThruDir):
      for aFile in files:
        if '.root' in aFile:
          if '%(run)03i-%(subrun)04i'%{'run':run%1000, 'subrun':subrun} in aFile:  
            self.inputFile = aFile
            self.inputFileList.append(os.path.join(a,aFile))
    if len(self.inputFileList) == 0:
      print 'Could not find inputfiles', run, subrun
      self.runInfo.MissingConfigs.append((run,subrun))

  def GetShortPathFileList(self):
    string = ' '
    for file in self.inputFileList:
      sFile = file[1+file.rfind('/'):]
      string += ' '+sFile
    return string

  def GetFullPathFileList(self):
    string = ' '
    for file in self.inputFileList:
      string += ' '+file
    return string

  def setInputFile(self):
    self.inputFile = None
    run = self.runInfo.RunNumber
    subrun = self.runInfo.SubRunNumber
    for a, b, files in os.walk(self.PassThruDir):
      for aFile in files:
        if '_{0}-{1:04}_'.format(run,subrun) in aFile:
          if '.root' in aFile:
            self.inputFile = aFile
    if self.inputFile == None:
      print 'Couldn\'t find inputfile!', run, subrun
  
  def ResetRun(self):
    if '[configuration]' in self.cfgDict.keys():
      cfgList = self.cfgDict['[configuration]']
      for item in cfgList:
        if 'inputfile' in item:
          cfgList.pop(cfgList.index(item))
    if '[filenaming]' in self.cfgDict.keys():
      fnList = self.cfgDict['[filenaming]']
      for item in fnList:
        if 'subrun' in item:
          fnList.pop(fnList.index(item))
      for item in fnList:
        if 'run_number' in item:
          fnList.pop(fnList.index(item))
    if '[neutrino]' in self.cfgDict.keys():
      nuList = self.cfgDict['[neutrino]']
      for item in nuList:
        if 'random_seed' in item:
          nuList.pop(nuList.index(item))
    if '[electronics]' in self.cfgDict.keys():
      elList = self.cfgDict['[electronics]']
      for item in elList:
        if 'random_seed' in item:
          elList.pop(elList.index(item))
    if '[nd280mc]' in self.cfgDict.keys():
      ndList = self.cfgDict['[nd280mc]']
      for item in ndList:
        if 'random_seed' in item:
          ndList.pop(ndList.index(item))
    if '[cherry_picker]' in self.cfgDict.keys():
      cpList = self.cfgDict['[cherry_picker]']
      for item in cpList:
        if 'inputfile_list' in item:
          cpList.pop(cpList.index(item))

  def setRunNumbersAndReset(self, run, subrun):
    self.ResetRun()
    run += self.runInfo.runprefix
    self.runInfo.RunNumber = run
    self.runInfo.SubRunNumber = subrun
    self.throwAgain()
    self.cfgDict['[filenaming]'].insert(0,('subrun', self.runInfo.SubRunNumber))
    self.cfgDict['[filenaming]'].insert(0,('run_number', self.runInfo.RunNumber))
    if self.runInfo.output == 'nd280':
      self.setInputFile()
      self.cfgDict['[configuration]'].append(('inputfile', self.inputFile))
      self.cfgDict['[electronics]'].insert(0,('random_seed',random.randint(0,9e8)))
      self.cfgDict['[nd280mc]'].insert(0,('random_seed',random.randint(0,9e8)))
    if self.runInfo.output == 'numc':
      self.cfgDict['[neutrino]'].insert(0,('random_seed',random.randint(0,9e8)))
    if self.runInfo.output == 'nucp':
      self.setInputFileList()
      self.cfgDict['[nd280mc]'].insert(0,('random_seed',random.randint(0,9e8)))
      self.cfgDict['[cherry_picker]'].insert(0,('inputfile_list',self.GetShortPathFileList()))
      
  def setComment(self):
  #ver, vol, base, mcType):
    ver = int(self.runInfo.production)
    vol = self.runInfo.fluxMasterVolume
    base = self.runInfo.baseline
    beam = self.runInfo.beam
    fill = self.runInfo.fill
    comment = 'prod{0:03}{1}{2}{3}{4}'.format(ver, vol, base[0:4], base[5:7],fill)
    if vol == 'magnet':
      if 'beam' in beam and len(beam) == 5:
        comment += beam[4] #i.e. 'a' or 'b'
      else:
        print 'Baseline, fluxVolume, mcType configuration not compatible'
        print vol, base, mcType
        return 'NOTVALID'
    else:
      #fluxVolume is basket
      if 'beam' not in beam and 'nu' not in beam:
        comment += beam
    self.runInfo.Comment = comment
#------------------------------------------------------------------------------ 
# Construction of the config file
#------------------------------------------------------------------------------ 

  def getSubLines(self, sub):
    lines = []
    if sub in self.cfgDict.keys():
      list = self.cfgDict[sub]
      for key, val in list:
        lines.append(key+' = '+str(val))
    return lines

  def constructCfgFile(self):
    lines = []
    subs = ['[software]','[configuration]','[filenaming]','[analysis]']
    subs.extend(['[geometry]','[neutrino]','[nd280mc]', '[electronics]'])
    subs.append('[cherry_picker]')

    for sub in subs:
      block = self.getSubLines(sub)
      if len(block) > 0:
        lines.append(sub)
        lines.extend(block)
        lines.append('')
    
    return lines

  def writeCfgFile(self, run, subrun):
    print self.getCfgFileName(run,subrun)
    outFile = open(self.getCfgFileName(run,subrun), 'w')
    self.setRunNumbersAndReset(run, subrun)
    lines = self.constructCfgFile()
    for line in lines:
      outFile.write(line+'\n')
    outFile.close()

  def parseRunSubrunArgs(self,arg):
    runs = []
    if '-' in arg:
      try:
        aSplit = [int(k) for k in arg.split('-')]
        runs = range(aSplit[0], aSplit[1]+1)
      except:
        print 'faulty argument:', arg
        sys.exit()
    else:
      runs = [int(k) for k in arg.split(',')]
    return runs

  def submitJob(self,run, subrun):
    output = self.runInfo.output
    script = self.createScript(int(run), int(subrun))
    print 'Created script', script
    handle = self.runInfo.getJobName(run,subrun)
    cmd = 'Qsub -e -l lnxfarm -N '
    subcmd = cmd + handle + ' -o '+output+'/logs/'+handle+'.out '+script
    print subcmd
    os.system(subcmd)
  
  def Usage(self):
    print 'Usage:'
    print 'to specify run/subrun number(s) (two arguments):'
    print '  ', 'an individual run'
    print '       ', sys.argv[0], 'runN subrunN'
    print '  ', 'a range:'
    print '       ', sys.argv[0], 'runM-runN subrunN'
    print '       ', sys.argv[0], 'runN subruM-subrunN'
    print '       ', sys.argv[0], 'runM-runN subruM-subrunN'
    print 'a pickled set (perhaps of missing runs) (one argument):'
    print '       ', sys.argv[0], 'Missing.pkl'
    print 'use the specified ranges as coded within this file (one argument):'
    print '       ', sys.argv[0], 'hardcoded'
    print 'display this usage'
    print '       ', sys.argv[0], 'help'

  def createScript(self, run, subrun):
    output = self.runInfo.output
    self.setRunNumbersAndReset(run,subrun)
    output = self.runInfo.output # i.e. 'nucp, nd280'
    outFileName = output+'.'+self.runInfo.baseline+'.'+str(run)+'.'+str(subrun)+'.sh'
    outFileName = './'+output+'/scripts/'+outFileName
    outputFile = open(outFileName, 'w')
    HERE = os.environ['PWD']
    out = []
    out.append('#!/bin/bash\n\n')
    out.append('source /nfs/hepcode/t2k/NDSW/setup_t2knd280.sh')
    out.append('\n')
    out.append('export HERE='+HERE)
    out.append('cd ${TMPDIR}')
    out.append('echo "Copying file"')
    
    if self.runInfo.output == 'nd280':
      out.append('cp '+self.PassThruDir+'/'+self.inputFile +' .')
    elif self.runInfo.output == 'numc':
      needFiles = self.runInfo.getNeededFiles()
      out.append('mkdir -p /sge-batch/GNfiles\n')
      for file in needFiles:
        out.append('if [ ! -e /sge-batch/GNfiles/'+file+' ]; then')
        out.append('  cp /nfs/data42/t2k/GNProd/files/'+file+' /sge-batch/GNfiles/ &')
        out.append('fi')
      out.append('wait\n')
      for file in needFiles:
        out.append('ln -sf /sge-batch/GNfiles/'+file+' . &')
      out.append('wait\n')
    elif self.runInfo.output == 'nucp':
      out.append('cp '+self.GetFullPathFileList() + ' .')
    
    out.append('\n')
    out.append('echo "Running ND280"')
    out.append('runND280 -t ${TMPDIR} -c '+self.getCfgFileName(run,subrun))
    out.append('\n')
    
    if self.runInfo.output == 'nd280':
      out.append('/usr/local/adm/bin/CUStageOut oa_gn*cali* $HERE/../cali')
      out.append('/usr/local/adm/bin/CUStageOut oa_gn*elmc* $HERE/../elmc')
      out.append('/usr/local/adm/bin/CUStageOut oa_gn*reco* $HERE/../reco')
      out.append('/usr/local/adm/bin/CUStageOut oa_gn*anal* $HERE/../anal')
      out.append('/usr/local/adm/bin/CUStageOut oa_gn*g4mc* $HERE/../g4mc')
      out.append('/usr/local/adm/bin/CUStageOut oa_gn*log $HERE/../logf')
      out.append('/usr/local/adm/bin/CUStageOut *dat $HERE/../dats')
    elif self.runInfo.output == 'numc':
      out.append('/usr/local/adm/bin/CUStageOut oa_gn*gnmc* $HERE/../gnmc/')
      out.append('/usr/local/adm/bin/CUStageOut oa_gn*numc* $HERE/../numc/')
      out.append('/usr/local/adm/bin/CUStageOut oa_gn*log* $HERE/numc/logs/')
      out.append('/usr/local/adm/bin/CUStageOut oa_gn*dat* $HERE/numc/dats/\n')
    elif self.runInfo.output == 'nucp':
      out.append('rm oa_gn_*nucp*geo.root')
      out.append('/usr/local/adm/bin/CUStageOut oa_gn_*nucp* $HERE/../nucp')
      out.append('/usr/local/adm/bin/CUStageOut oa_gn_*log $HERE/../logf')
      
    for line in out:
      outputFile.write(line+'\n')
    outputFile.close()
    os.system('chmod 744 '+outFileName)
    return outFileName
