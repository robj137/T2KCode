#!/usr/local/python-2.6.2-X86_64/bin/python

import os
import sys
import string
import random

# system-dependent (filepath) stuff:
genieSetupPath = '/nfs/hepcode/t2k/GENIE/setup.sh'
passThruDir ='/nfs/dcache102/t2k/GNprod5/production005/A/mcp/genie/2010-11-'

class MCRunInfoClass:
  def __init__(self):
    self.setDefaults()
    self.setDetails()
    self.MissingConfigs = []
  def loadCard(self, cardname):
    input = open(cardname,'r')
    lines = []
    for line in input:
      lines.append(line)
    self.production = int(lines[0].split()[0])
    self.step = lines[6].split()[0]
    self.big = False
    if len(lines[6].split())>1:
      self.big = True
    self.nd280Version = lines[8].split()[0]
  def setDetails(self):
    pwd = os.environ['PWD']
    self.prodDir = pwd[0:pwd.find('production')+13]
    self.loadCard('runInfo.card')
    if 'beam' in pwd:
      self.beam = 'beam'
    if 'beama' in pwd:
      self.beam = 'beama'
    if 'beamb' in pwd:
      self.beam = 'beamb'
    if 'beamc' in pwd:
      self.beam = 'beamc'
    if 'ccpiplus' in pwd:
      self.beam = 'ccpiplus'
      self.nMesons = 0
      self.nLeptons = 1
      self.nMuMinus = 1
      self.nPiZero = 0
      self.nPiPlus = 1
    if 'ccpizero' in pwd:
      self.beam = 'ccpizero'
      self.nMesons = 0
      self.nLeptons = 1
      self.nMuMinus = 1
      self.nPiZero = 1
      self.nPiPlus = 0
    if 'ncpiplus' in pwd:
      self.beam = 'ncpiplus'
      self.nMesons = 0
      self.nLeptons = 0
      self.nMuMinus = 0
      self.nPiZero = 0
      self.nPiPlus = 1
    if 'ncpizero' in pwd:
      self.beam = 'ncpizero'
      self.nMesons = 0
      self.nLeptons = 0
      self.nMuMinus = 0
      self.nPiZero = 1
      self.nPiPlus = 0
    if 'verify' in pwd:
      self.verify = True
    if 'genie' in pwd:
      self.mc = 'Genie'
      self.runprefix += 1000000
    self.respin = pwd[pwd.find(self.prodDir)+len(self.prodDir)+1:][0]
    if self.respin not in string.uppercase:
      print 'Respin', self.respin, 'doesn\'t appear to be an UPPER CASE LETTER'
    if '2010-11' in pwd:
      self.runN = 2
      self.baseline = '2010-11'
      self.runprefix += 100000
    if 'water' in pwd:
      self.fill = 'water'
      self.p0dwater = 1
      self.runprefix += 10000
    if 'basket' in pwd:
      self.fluxVolume = 'basket'
      self.fluxMasterVolume = 'basket'
      self.fluxName = 'basket'
      self.runprefix += 1000
      if 'nue' in pwd:
        self.fluxName = 'basket'
        self.runprefix += 1000
      if 'ncpizero' in pwd:
        self.fluxName = 'NC1pi0'
        self.runprefix += 2000
      if 'ccpizero' in pwd:
        self.fluxName = 'CC1pi0'
        self.runprefix += 3000
      if 'ncpiplus' in pwd:
        self.fluxName = 'NC1pi+'
        self.runprefix += 4000
      if 'ccpiplus' in pwd:
        self.fluxName = 'CC1pi+'
        self.runprefix += 5000
      if 'ncpizerofgd' in pwd:
        self.fluxName = 'NCpi0FGD'
        self.fluxMasterVolume = 'FGD1'
        self.runprefix += 6000
      if 'ccpicoh' in pwd:
        self.fluxName = 'CCpicoh'
        self.fluxMasterVolume = 'FGD1'
        self.runprefix += 7000
    self.setFluxInfo()
  
  def setDefaults(self):
    self.beam = 'beam'
    self.fill = 'air'
    self.p0dwater = 0
    self.production = 5
    self.respin = 'A'
    self.baseline = '2010-02'
    self.runN = 1
    self.fluxVolume = 'magnet'
    self.fluxMasterVolume = 'magnet'
    self.fluxName = 'magnet'
    self.mc = 'neut'
    self.runprefix = 90100000
    self.verify = False
    self.setCherryPickingDefaults()

  def setCherryPickingDefaults(self):
    self.inputFileList = []
    self.nMesons = 0
    self.nLeptons = 0
    self.nMuMinus = 0
    self.nPiZero = 0
    self.nPiPlus = 0
  
  def setFluxInfo(self):
    self.fluxTree = 'h3002'
    self.fluxFile = 'nu.nd6_flukain.0-249.root' 
    self.fluxPOT = '5e17'
    self.XSFile = 'genie_nd280_xsec_v10r3.xml'
    self.fluxProbs = 'nu.nd6_flukain.0-249_genie_evtrate_'
    self.fluxProbs += self.baseline+'-'+self.fill+'.root'
    self.fluxFilePOT = '250e21'
    self.randomStart = 1
    if self.fluxVolume == 'basket':
      self.fluxPOT = '1e18'
      if self.big:
        self.fluxPOT = '2e19'
      self.fluxFile = 'nu.nd5_flukain.0-499.root' 
      self.fluxFilePOT = '500e21'
      self.fluxProbs = 'nu.nd5_flukain.0-499_genie_evtrate_'
      self.fluxProbs += self.baseline+'-'+self.fill+'.root'
    
  def getNeededFiles(self):
    files = ['genie_nd280_xsec_v10r3.xml']
    baseline = self.baseline
    fill = self.fill
    if self.fluxVolume.title() == 'Magnet':
      base = 'nu.nd6_flukain.0-249'
    else:
      base = 'nu.nd5_flukain.0-499'
    files.append(base+'.root')
    files.append(base+'_genie_evtrate_'+baseline+'-'+fill+'.root')
    return files
   
  def getND280CfgPath(self, run, subrun):
    path = os.environ['PWD'] + '/cfg/nd280_'+self.beam+'_'+self.fluxMasterVolume+'_'
    path += self.baseline + '-'+self.fill + '_'
    path += str(run+self.runprefix)+'-'+str(subrun)+'.cfg'
    return path
  def getJobName(self, run, subrun):
    handle = 'R'+str(self.runN)+self.fluxMasterVolume[0]+self.fill[0]
    handle += '_'+str(run)+'_'+str(subrun)
    return handle
  def setND280Version(self, ver):
    self.nd280Version = ver

