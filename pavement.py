from paver.easy import *
import os
import glob

@task
def test():
  #sh('nosetests code/test/*.py --with-coverage')
  sh('nosetests code/test/*.py --with-coverage --cover-html')
  pass

@task
def clean():
  for pycfile in glob.glob("*/*/*.pyc"): os.remove(pycfile)
  pass

@task
@needs(['test'])
def default():
  pass
