import sys
import os
import Core
import json
from pylab import *
ioff()



def main(fname, param=None):
    """
    The main function of the command line version.
    Reads the content of the .json file into the option object,
    and creates the core object which runs the optimization process based on the .json file.

    :param fname: the configuration file which contains the settings (should be in json format)
    :param param: controls the level of output, 0 means minimal, 1 means maximal (the Default is None which is interpreted as 1)

    """
    try:
        with open(fname, "r") as f:
            json_data = json.load(f)
    except IOError as ioe:
        print(ioe)
        sys.exit("File not found!\n")
    
    core = Core.coreModul()
    if param != None:
        core.option_handler.output_level = param.lstrip("-v_level=")
    core.option_handler.ReadJson(json_data['attributes'])
    core.Print()
    kwargs = {"file" : core.option_handler.GetFileOption(),
            "input": core.option_handler.GetInputOptions()}
    core.FirstStep(kwargs)
    kwargs = {"simulator": core.option_handler.GetSimParam()[0],
            "model" : core.option_handler.GetModelOptions(),
            "sim_command":core.option_handler.GetSimParam()[1]}
    core.LoadModel(kwargs)

    kwargs = {"stim" : core.option_handler.GetModelStim(), "stimparam" : core.option_handler.GetModelStimParam()}
    core.SecondStep(kwargs)
    kwargs = None
    core.ThirdStep(kwargs)
    core.FourthStep()
    print("resulting parameters: ", core.optimal_params)
    


