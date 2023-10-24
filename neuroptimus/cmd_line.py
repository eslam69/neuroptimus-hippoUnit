import matplotlib
matplotlib.use('Agg')
import sys
import os
import Core
import json
matplotlib.interactive(False)
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
    print("json data attributes: ", json_data.keys())
    # core.Print()
    kwargs = {"file" : core.option_handler.GetFileOption(),
            "input": core.option_handler.GetInputOptions()}
    print("kwargs1: ", kwargs)
    core.FirstStep(kwargs)
    kwargs = {"simulator": core.option_handler.GetSimParam()[0],
            "model" : core.option_handler.GetModelOptions(),
            "sim_command":core.option_handler.GetSimParam()[1]}
    print("kwargs2: ", kwargs)
    core.LoadModel(kwargs)

    kwargs = {"stim" : core.option_handler.GetModelStim(), "stimparam" : core.option_handler.GetModelStimParam()}
    print("kwargs3: ", kwargs)
    core.SecondStep(kwargs)
    kwargs = None
    core.ThirdStep(kwargs)

    core.FourthStep()
    print("resulting parameters: ", core.optimal_params)

    ## Saving the results
    fig = figure(figsize=(7, 6))
    axes = fig.add_subplot(111)
    exp_data = []
    model_data = []
    if core.option_handler.type[-1] != 'hippounit':
        if core.option_handler.type[-1] != 'features':
            for n in range(core.data_handler.number_of_traces()):
                exp_data.extend(core.data_handler.data.GetTrace(n))
                model_data.extend(core.final_result[n])
            no_traces = core.data_handler.number_of_traces()
        else:
            for n in range(len(core.data_handler.features_data["stim_amp"])):
                model_data.extend(core.final_result[n])
            no_traces = len(core.data_handler.features_data["stim_amp"])
        if core.option_handler.type[-1]  != 'features' and core.option_handler.type[-1] != 'hippounit':
            t = int(ceil(core.option_handler.input_length))
        else:
            t = int(ceil(core.option_handler.run_controll_tstop))
        step = core.option_handler.run_controll_dt
        axes.set_xticks([n for n in range(0, int((t * no_traces) / (step)), int((t * no_traces) / (step) / 5.0)) ])
        axes.set_xticklabels([str(n) for n in range(0, int(t * no_traces), int((t * no_traces) / 5))])


        axes.set_xlabel("time [ms]")
        if core.option_handler.type[-1]!= 'features' and core.option_handler.type[-1] != 'hippounit':
            _type = core.data_handler.data.type
        else:
            _type = "Voltage" if core.option_handler.run_controll_record =="v" else "Current" if core.option_handler.run_controll_record == "c" else ""
        axes.set_ylabel(_type + " [" + core.option_handler.input_scale + "]")
        if core.option_handler.type[-1]!= 'features' and core.option_handler.type[-1] != 'hippounit':
            axes.plot(list(range(0, len(exp_data))), exp_data)
            axes.plot(list(range(0, len(model_data))), model_data, 'r')
            axes.legend(["target", "model"])
        else:
            axes.plot(list(range(0, len(model_data))), model_data, 'r')
            axes.legend(["model"])
        fig.savefig("result_trace.png", dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1)
        fig.savefig("result_trace.eps", dpi=None, facecolor='w', edgecolor='w')
        fig.savefig("result_trace.svg", dpi=None, facecolor='w', edgecolor='w')


