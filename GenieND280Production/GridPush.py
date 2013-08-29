#!/usr/bin/python

import os
import sys
from subprocess import Popen, PIPE, STDOUT
#cg-cp -v -n 5 production005/A/mcp/genie/2010-11-water/magnet/beamb/numc/oa_gn_beam_91210001-0044_5edpxrhgo26n_numc_000_prod005magnet201011waterb.root srm://t2ksrm.nd280.org/nd280data/production005/A/mcp/genie/2010-11-water/magnet/beamb/numc/oa_gn_beam_91210001-0044_5edpxrhgo26n_numc_000_prod005magnet201011waterb.root

fileList = sys.argv[1:]
pwd = os.getenv('PWD')+'/'
ocmd = 'lcg-cr -v -n 6 '
seprefix = ' -d srm://t2ksrm.nd280.org/nd280data/'
for file in fileList:
  cmd = ocmd + seprefix+file + ' -l lfn:/grid/t2k.org/nd280/'+file + ' file:'+pwd+file
  pushFile =  Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE,
                    stderr=STDOUT).communicate()[0]
  print pushFile
  print cmd
  outlines = pushFile.split('\n')
  for line in outlines:
    print line
