"""
Handles the primary functions

In any directory with the appropriate .json input files, run DESPASITO with ``python -m despasito input.json``

"""

import logging
from .input_output import readwrite_input
from .equations_of_state import eos as eos_mod
from .thermodynamics import thermo
from .fit_parameters import fit

def run(filename="input.json"):

    """ Main function for running despasito calculations. All inputs and settings should be in the supplied JSON file(s).
    """

    eos_obj_name = "saft.gamma_mie"
    
    logger = logging.getLogger(__name__)
    
    #read input file (need to add command line specification)
    logger.info("Begin processing input file: %s" % filename)
    eos_dict, thermo_dict = readwrite_input.extract_calc_data(filename)
    logger.debug("EOS dict:",eos_dict)
    logger.debug("Thermo dict:",thermo_dict)
    logger.info("Finish processing input file: %s" % filename)
    
    logger.info("Creating eos object: %s" % (eos_obj_name))
    try:
        eos = eos_mod(eos_obj_name, **eos_dict)
    except:
        raise
    logger.info("Created %s eos object" % (eos_obj_name))
    
    # Run either parametrization or thermodynamic calculation
    if "opt_params" in list(thermo_dict.keys()):
        logger.info("Intializing parametrization procedure")
        output = fit(eos, thermo_dict)
        logger.info("Finished parametrization")
        # readwrite_input.writeout_dict(output_dict)
    else:
        logger.info("Intializing thermodynamic calculation")
        output_dict = thermo(eos, thermo_dict)
        logger.info("Finished thermodynamic calculation")
        # readwrite_input.writeout_dict(output_dict)
    