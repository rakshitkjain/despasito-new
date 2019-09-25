from .main import run
import sys
import os
import argparse
import logging
import logging.handlers

## Define parser functions and arguements
parser = argparse.ArgumentParser(description="DESPASITO: Determining Equilibrium State and Parametrization: Application for SAFT, Intended for Thermodynamic Output.  This is an open-source application for thermodynamic calculations and parameter fitting for the Statistical Associating Fluid Theory (SAFT) EOS and SAFT-𝛾-Mie coarse-grained simulations.")
parser.add_argument("-i", "--input", dest="input", help="Input .json file with calculation instructions and path(s) to equation of state parameters. See documentation for explicit explanation. Compile docs or visit https://despasito.readthedocs.io")
parser.add_argument("-q", "--quiet", action="store_true", dest="quiet", help="Removes printing to console")
parser.add_argument("-v", "--verbose", action="count", default=0, help="Verbose level, repeat up to two times.")
parser.add_argument("--log", nargs='?', dest="logFile", default="despasito.log", help="Output a log file. The default name is despasito.log.")
parser.add_argument("-t", "--threads", dest="threads", type=int, help="Set the number of theads used. This hasn't been implemented yet.",default=1)
parser.add_argument("-p", "--path", default=".", help="Set the location of the data/library files (e.g. SAFTcross, etc.) for despasito to look for")
parser.add_argument("--jit", action='store_true', default=0, help="turn on Numba's JIT compilation for accelerated computation")

## Extract arguements
args = parser.parse_args()
if args.verbose:
    if args.verbose < 3:
        args.verbose = (3 - args.verbose) * 10
    else:
        args.verbose = 10

## Handle arguements

# Logging

## Set up logging (refined after argparse)
logger = logging.getLogger()
logger.setLevel(args.verbose)

# Set up rotating log files
log_file_handler = logging.handlers.RotatingFileHandler(args.logFile)
log_file_handler.setFormatter( logging.Formatter('%(asctime)s [%(levelname)s](%(name)s:%(funcName)s:%(lineno)d): %(message)s') )
log_file_handler.setLevel(args.verbose)
logger.addHandler(log_file_handler)

if not args.quiet:
    # Set up logging to console
    console_handler = logging.StreamHandler() # sys.stderr
    console_handler.setFormatter( logging.Formatter('[%(levelname)s](%(name)s): %(message)s') )
    console_handler.setLevel(args.verbose)
    logger.addHandler(console_handler)

logging.info("Input args: {}".format(args))
logging.info("JIT compilation: {}".format(args.jit))

# Threads
# if args.threads != None:
#     threadcount = args.threads
# else:
#     threadcount = 1

# Run program
if args.input:
    kwargs = {"filename":args.input}
else:
    kwargs = {}

kwargs["threads"] = args.threads
kwargs["path"] = args.path
kwargs["jit" ] = args.jit

run(**kwargs)

