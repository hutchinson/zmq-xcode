#!/usr/bin/env python

import os
import sys
import shutil
from subprocess import call

BUILD_SCRIPT_PATH = os.path.realpath(__file__)
ZMQ_ROOT_PATH = os.path.dirname(BUILD_SCRIPT_PATH)
BUILD_DIR = os.path.join(ZMQ_ROOT_PATH, "build")

print("Root path %s" % ZMQ_ROOT_PATH)

if len(sys.argv) > 1 and sys.argv[1] == "clean":
  shutil.rmtree(BUILD_DIR, ignore_errors=True)
  exit(0)

if not os.path.exists(BUILD_DIR):
  os.mkdir(BUILD_DIR)

ORIGINAL_DIR = os.getcwd()
os.chdir(BUILD_DIR)

# configure
call(["../zeromq-4.0.4/configure", "--prefix=%s" % BUILD_DIR])
call(["make", "-j4"])
call(["make", "install"])

os.chdir(ORIGINAL_DIR)