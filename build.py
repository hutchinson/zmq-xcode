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

# Poor man's dependency tracking...
static_lib = os.path.join(BUILD_DIR, "lib", "libzmq.a")
header_c_zmq = os.path.join(BUILD_DIR, "include", "zmq.h")
header_cpp_zmq = os.path.join(BUILD_DIR, "include", "zmq.hpp")

if os.path.exists(static_lib) and os.path.exists(header_c_zmq) and os.path.exists(header_cpp_zmq):
  exit(0)

if not os.path.exists(BUILD_DIR):
  os.mkdir(BUILD_DIR)

ORIGINAL_DIR = os.getcwd()
os.chdir(BUILD_DIR)

# configure && make && install...
call(["../zeromq-4.0.4/configure", "--prefix=%s" % BUILD_DIR])
call(["make", "-j4"])
call(["make", "install"])

# Copy the C++ bindings over.
shutil.copyfile("../zeromq-4.0.4/include/zmq.hpp", "include/zmq.hpp")

os.chdir(ORIGINAL_DIR)