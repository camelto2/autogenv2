from __future__ import print_function
import os
import numpy as np
import subprocess as sub
import shutil
from submitter import LocalSubmitter
from pyscf.pbc import lib as pbclib
from pyscf import lib
import pyscf2qwalk

####################################################

class PySCF2QWalk:
  """ Converts from a PySCF run to a QWalk input file"""
  _name_='LocalPySCF2QMCRunner'
  def __init__(self,options):
    self.basename='qw'
    self.chkfile='pyscf_driver.py.chkfile'
    self.method='scf'
    self.tol=0.01
    self.files={}
    self.completed=False

    self.set_options(options)

  #-------------------------------------------------
  def set_options(self,d):
    selfdict=self.__dict__

    # Check important keys are set. 
    for k in d.keys():
      if not k in selfdict.keys():
        print("Error:",k,"not a keyword for PySCFWriter")
        raise AssertionError
      selfdict[k]=d[k]

  #-------------------------------------------------
  def is_consistent(self,other):
    skipkeys = ['completed','files']
    for otherkey in other.__dict__.keys():
      if otherkey not in self.__dict__.keys():
        print('other is missing a key.')
        return False
    for selfkey in self.__dict__.keys():
      if selfkey not in other.__dict__.keys():
        print('self is missing a key.')
        return False
    for key in self.__dict__.keys():
      if self.__dict__[key]!=other.__dict__[key] and key not in skipkeys:
        print("Different keys [{}] = \n{}\n or \n {}"\
            .format(key,self.__dict__[key],other.__dict__[key]))
        return False
    return True
    
  #-------------------------------------------------      
  def check_status(self):
    if self.completed:
      return 'ok'
    else:
      return 'not_started'

  #-------------------------------------------------      
  def run(self):
    mol=lib.chkfile.load_mol(self.chkfile)
    results=lib.chkfile.load(self.chkfile,self.method)

    self.files=pyscf2qwalk.print_qwalk(
        mol,results,self.method,self.tol,self.basename)
    self.completed=True
