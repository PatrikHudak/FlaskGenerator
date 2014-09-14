#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
################################################
# Simple Flask App generator
# by Patrik Hudak in 2014

import functools
import inspect
import os
import subprocess
import sys

VIRTUALENV = {
  "name": "virtenv",
  "used": False
}

BASEDIR = os.path.abspath(".")
PYTHON = 'python'
PIP = 'pip'

#if len(sys.argv) > 1:
#  BASEDIR = os.path.abspath(sys.argv[1])

# Helpers
def touch(filename, flush=''):
  if filename.endswith(".py"):
    flush  = "#!/usr/bin/env python\n"
    flush += "# -*- coding: utf-8 -*-\n"
  elif filename.endswith(".sh"):
    flush = "#!/bin/bash\n"
  open(os.path.join(BASEDIR, filename), 'w').write(flush)

def mkdir(dirname):
  dirname = os.path.join(BASEDIR, dirname)
  if not os.path.exists(dirname):
    os.mkdir(dirname)

# Decorators
def prompt_action(f):
    __prompt__ = "{} (y/N): ".format(f.__doc__.strip())

    @functools.wraps(f)
    def decorated():
      result = None
      while(result not in ['y', 'n', '']):
        result = raw_input(__prompt__).lower()
      if result == 'y':
        f()

    return decorated

def action(f):
  @functools.wraps(f)
  def decorated():
    __message__ = f.__doc__
    if __message__:
      print "{}...\t".format(__message__.strip()),
    try:
      f()
    except Exception as e:
      if __message__: print "[FAIL]"
      print e
      print "Exiting now..."
      sys.exit(1)
    else:
      if __message__: print "[OK]"
  return decorated


# Actions
def virtualenv():
  # Master action (priority)
  global PYTHON, PIP, VIRTUALENV
  VIRTUALENV["used"] = True
  PYTHON = os.path.join(BASEDIR, VIRTUALENV["name"], "bin/python")
  PIP = os.path.join(BASEDIR, VIRTUALENV["name"], "bin/pip")
  subprocess.call(['virtualenv', VIRTUALENV["name"], '--no-site-packages'])
  subprocess.call([PIP, 'install', 'Flask'])

@action
def fs_structure():
  """Generating folder structure"""
  mkdir("app")
  mkdir("app/static")
  mkdir("app/static/css")
  mkdir("app/static/js")
  mkdir("app/static/js/vendor")
  mkdir("app/static/images")
  mkdir("app/templates")
  touch("app/__init__.py", "#!/bin/bash\n")
  touch("build.sh")
  touch("config.py")
  touch("LICENCE")
  touch("README.md")
  touch("requirements.txt")

@action
def extensions():
  extensions = raw_input("Flask Extensions to install (use <space> as separator): ")
  if not extensions:
    return
  # Double checking separator :)
  extensions = extensions.replace(",", " ").replace("  ", " ").lower()
  extensions = extensions.split()
  subprocess.call([PIP, 'install'] + extensions)

  if 'flask-script' in extensions:
    touch("manage.py")

# Prompted actions
@prompt_action
def fabric():
  """ Use fabric? """
  touch("fabfile.py")
  subprocess.call([PIP, 'install', 'fabric'])

@prompt_action
def docker():
  """ Use docker? """
  touch("Dockerfile")

@prompt_action
def git():
  """ Use git? """
  subprocess.call(['git', 'init', BASEDIR])
  touch(".gitignore", "*.pyc\n")

# setup & teardown
def setup():
  virtualenv()

def teardown():
  requirements = open(os.path.join(BASEDIR, "requirements.txt"), 'w')
  subprocess.call([PIP, 'freeze'], stdout=requirements)
  requirements.close()

if __name__ == '__main__':
  setup()

  functions = {
    "actions": [],
    "prompted": []
  }

  for i in globals().values():
    if inspect.isfunction(i) and i.__closure__:
      if len(i.__closure__) == 1:
        functions["actions"].append(i)
      else:
        functions["prompted"].append(i)

  for action in functions["actions"]:
    action.__call__()

  for p_action in functions["prompted"]:
    p_action.__call__()

  teardown()

  print "=" * 20
  print "Done! Enjoy :)"
