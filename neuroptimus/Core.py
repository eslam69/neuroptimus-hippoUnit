from matplotlib import pyplot as plt
from traceHandler import *
from modelHandler import *
from optimizerHandler import *
from optionHandler import optionHandler
import time
from datetime import datetime
import numpy
import json
import os
import matplotlib
# matplotlib.use("Qt5Agg")
matplotlib.use("Agg")
matplotlib.interactive(False)


class my_candidate():
    """
    Mimics the behavior of ``candidate`` from the ``inspyred`` package to allow the uniform
    handling of the results produced by the different algorithms.

    :param vals: the result of the optimization
    :param fitn: the fitness of the result

    """

    def __init__(self, vals, fitn=-1):
        self.candidate = vals
        self.fitness = fitn


class coreModul():
    """
    This class is responsible to carry out the main steps of the optimization process by
    interacting with the other modules. The main attributes are the following:

    :attr: data_handler:

            performs input operations and handles input data

    :attr: option_handler:

            stores the settings

    :attr: model_handler:

            handles the model and runs the simulations and carries out other model related tasks

    :attr: optimizer:

            carries out the optimization process

    :attr: optimal_params:

            contains the resulting parameters

    :attr: ffun_calc_list:

            contains the list of available fitness functions in a dictionary

    """

    def __init__(self):
        self.data_handler = DATA()
        self.option_handler = optionHandler()
        self.model_handler = None
        self.optimizer = None
        self.optimal_params = None
        self.solutions = []
        self.wfits = []
        self.wfits2 = []
        self.cands = []
        self.fits = []
        f_m = {"MSE": "calc_ase",
               "Spike count": "calc_spike",
               "MSE (excl. spikes)": "calc_spike_ase",
               "Spike count (stim.)": "spike_rate",
               "ISI differences": "isi_differ",
               "Latency to 1st spike": "first_spike",
               "AP amplitude": "AP_overshoot",
               "AHP depth": "AHP_depth",
               "AP width": "AP_width",
               "Derivative difference": "calc_grad_dif"}
        self.ffun_mapper = dict((v, k) for k, v in list(f_m.items()))
        self.ffun_calc_list = ["MSE",
                               "MSE (excl. spikes)",
                               "Spike count",
                               "Spike count (stim.)",
                               "ISI differences",
                               "Latency to 1st spike",
                               "AP amplitude",
                               "AHP depth",
                               "AP width",
                               "Derivative difference"]
        self.hippounit_tests_names = ["SomaticFeaturesTest", "PSPAttenuationTest", "BackpropagatingAPTest",
                                      "PathwayInteraction", "DepolarizationBlockTest", "ObliqueIntegrationTest",]
        self.grid_result = None

    def htmlStrBold(self, inp):
        return "<b>"+str(inp)+"</b>"

    def htmlStr(self, inp):
        return "<p>"+str(inp)+"</p>"

    def htmlUnderline(self):
        return "text-decoration:underline"

    def htmlResize(self, size):
        return "font-size:"+str(int(size))+"%"

    def htmlAlign(self, align_to):
        if align_to not in ["left", "right", "center"]:
            raise ValueError
        return "text-align:"+align_to

    def htmlStyle(self, inp, *args):
        tmp_str = "<span style=\""
        for n in args:
            tmp_str += n+";"
        tmp_str += "\">"+str(inp)+"</span>"
        return tmp_str

    def htmlTable(self, header_list, data):
        tmp_str = "<table border=\"1\" align=\"center\">"
        for h in header_list:
            tmp_str += "\n<th>"+str(h)+"</th>"

        for r in data:
            tmp_str += "\n<tr>"
            for c in r:
                tmp_str += "\n<td>"+str(c)+"</td>"
            tmp_str += "\n</tr>"

        tmp_str += "\n</table>"
        return tmp_str

    def htmlPciture(self, inp):
        return "<p align=\"center\"><img style=\"border:none;\" src=\""+inp+"\" ></p>"

    def htmlPdf(self, inp):
        # return "<p align=\"center\"><embed src = \""+inp+"#toolbar=0&navpanes=0&scrollbar=0\" width = \"800px\" height = \"630px\" /></p>"
        return "<p align=\"center\"><embed src = \" "+inp+" \" width = \"800px\" height = \"630px\" /></p>"

    def Print(self):
        print([self.option_handler.GetFileOption(),
               self.option_handler.GetInputOptions(),
               self.option_handler.GetModelOptions(),
               self.option_handler.GetModelStim(),
               self.option_handler.GetModelStimParam(),
               self.option_handler.GetObjTOOpt(),
               self.option_handler.GetOptParam(),
               self.option_handler.GetFitnessParam(),
               self.option_handler.GetOptimizerOptions()])
        print("\n")

    def FirstStep(self, args):
        """
        Stores the location of the input, and the base directory in the ``option_handler`` object
        and reads the data from the file into the ``data_handler`` object.

        :param args: dictionary with keys "file" and "input"

        """
        # print("args inside first step: ")
        # print(args)
        self.option_handler.SetFileOptions(args.get("file"))
        self.option_handler.SetInputOptions(args.get("input"))

        stim_type = self.option_handler.type[-1]
        if stim_type.lower() == "hippounit":
            self.option_handler.SetSimParam(["hippounit", []])
        else:
            self.data_handler.Read([self.option_handler.input_dir], self.option_handler.input_size,
                                   self.option_handler.input_scale, self.option_handler.input_length, self.option_handler.input_freq, stim_type)
            if stim_type == "features":
                self.option_handler.input_size = len(
                    self.data_handler.features_data['stim_amp'])

    def LoadModel(self, args):
        """
        Stores the type of the simulator as well as the optional parameters passed to it.
        Creates the ``model_handler`` objects which can be either ``modelHandlerNeuron`` or ``externalHandler``.
        If the ``externalHandler`` is selected then the number of parameters subject to optimization is also set.

        :param args: dictionary with keys "simulator" and "sim_command"

        """
        self.model_handler = None
        # print("args inside load model: ")
        # print(args)
        self.option_handler.SetSimParam(
            [args.get("simulator", "Neuron"), args.get("sim_command"), None])
        if self.option_handler.GetSimParam()[0] == "Neuron":
            self.option_handler.SetModelOptions(args.get("model"))
            self.model_handler = modelHandlerNeuron(
                self.option_handler.model_path, self.option_handler.model_spec_dir, self.option_handler.base_dir)
        elif self.option_handler.GetSimParam()[0] == "hippounit":
            self.option_handler.SetModelOptions(args.get("model"))
            return
        else:
            self.model_handler = externalHandler(
                self.option_handler.GetSimParam()[1])
            self.model_handler.SetNParams(self.option_handler)
            if self.option_handler.type[-1] != 'features':
                k_range = self.data_handler.number_of_traces()
            else:
                k_range = len(self.data_handler.features_data["stim_amp"])
            self.option_handler.SetModelStimParam([[0]*k_range, 0, 0])

    def ReturnSections(self):
        """

        :return: the sections found in the model including "None" in a ``string`` ``list``.

        """
        temp = self.model_handler.GetParameters()
        sections = []
        for n in temp:
            sections.append(n[0])
        sections = list(set(sections))
        sections.append("None")
        return sections

    def ReturnMorphology(self):
        """

        :return: the morphological parameters found in the model including "None" in a ``string`` ``list``.

        """
        temp = self.model_handler.GetParameters()
        morphs = (str.split(temp[0][1], ", "))
        morphs = list(set(morphs))
        morphs.append("None")
        return morphs

    def ReturnChannels(self, section):
        """
        Collects the channels from the given section.

        :param section: the name of the section

        :return: the channels in the given section including "None" in a ``string`` ``list``.

        """
        temp = self.model_handler.GetParameters()
        channels = []
        for n in temp:
            if n[0] == section:
                for k in str.split(n[2], " "):
                    if k != "":
                        for s in str.split(n[3], " "):
                            if str.count(k, s) == 1 and s != "":
                                channels.append(s)

        channels = list(set(channels))
        channels.append("None")
        return channels

    def ReturnChParams(self, channel):
        """
        Collects channel parameters from the given channel

        :param channel: the name of the channel mechanism
        :return: the channel parameters in the given channel including "None" in a ``string`` ``list``.

        .. note::
                This function returns everything from the channel object not only the parameters.

        """
        temp = self.model_handler.GetParameters()
        ch_param = []
        for n in temp:
            if str.find(n[3], channel) != -1:
                for p in n[2].split():
                    if str.find(p, channel) != -1:
                        ch_param.append(p)
        ch_param = list(set(ch_param))
        ch_param.append("None")

        return ch_param

    # not in use
    def SetModel(self, args):

        if args.get("channel") != "None":
            self.model_handler.SetChannelParameters(args.get("section"), args.get(
                "segment"), args.get("channel"), args.get("params"), args.get("values"))
        else:
            self.model_handler.SetMorphParameters(
                args.get("section"), args.get("morph"), args.get("values"))

    def SetModel2(self, args):
        """
        Stores the selected parameter as subject to optimization in the ``option_handler`` object.
        For future use it offers a way to store initial value (not in use at the moment).

        :param args: must be a string-string dictionary containing the following keys:

                        * section
                        * channel
                        * params
                        * value

                or:

                        * section
                        * morph
                        * values

        """
        if args.get("channel") != "None":
            self.option_handler.SetObjTOOpt(args.get(
                "section")+" "+args.get("segment")+" "+args.get("channel")+" "+args.get("params"))
            self.option_handler.SetOptParam(args.get("values"))
        else:
            self.option_handler.SetObjTOOpt(
                args.get("section")+" "+args.get("morph"))
            self.option_handler.SetOptParam(args.get("values"))

    def SecondStep(self, args):
        """
        Stores the stimulation settings in the option object.

        :param args: must be a dictionary with the following keys:

                * stim
                        must hold a ``list`` as value, which contains:
                           * stimulus type as ``string``, must be either "IClamp" or "VClamp"
                           * position of stimulus inside the section as of real value (0-1)
                           * name of stimulated section as ``string``
                * stimparam
                        must hold a ``list`` as value which contains:
                           * stimulus amplitudes as a ``list`` of real values
                           * delay of stimulus as real value
                           * duration of stimulus as real value

        """
        self.option_handler.SetModelStim(args.get("stim"))
        self.option_handler.SetModelStimParam(args.get("stimparam"))

    def ThirdStep(self, args):
        """
        Stores the parameters in the ``option_handler`` object regarding the optimization process.
        If the sampling rate of the simulation is higher than the sampling rate of the input trace,
        then it re-samples the input using linear interpolation to create more points.
        Currently running a simulation with lower sampling rate than the input trace is not supported!
        After storing the necessary settings the ``optimizer`` object is initialized and the optimization is performed.
        The raw results are stored in the ``solutions`` variable in the ``optimizer`` object.

        :param args: a dictionary containing the following keys:

                * runparam
                        must be a list containing the following values:
                                * length of simulation as real value
                                * integration step as real value
                                * parameter to record as ``string``
                                * name of the section where the recording takes place as ``string``
                                * position inside the section as real value (0-1)
                                * initial voltage as a real value
                * feat
                        must be a ``list`` with the names of the selected fitness functions
                * weights
                        must be a list of real values
                * algo_options
                        must be a dictionary containing options related to the optimization algorithm

                        mandatory parameters:
                                * seed
                                * current_algorithm
                                * pop_size
                                * num_params
                                * boundaries
                        optional parameter shared by every algorithm
                                * starting_points
        """
        self.grid_result = None
        # print("args inside third step: ")
        # print(args)
        if args != None:
            # print("args inside third step: ")
            # print(args)
            self.option_handler.SetModelRun(args.get("runparam"))
            fit_par = []
            fit_par.append(args.get("feat", []))
            fit_par.append(args.get("weights", []))
            self.option_handler.SetFitnesParam(fit_par)
            tmp = args.get("algo_options")
            """
			if self.option_handler.type[-1]=='features':
				tmp.update({"num_params" : len(self.data_handler.features_data['stim_amp'])})
			"""
            if len(tmp.get("boundaries")[0]) < 1:
                raise sizeError("No boundaries were given!")
            # tmp.append(args.get("starting_points"))
            self.option_handler.SetOptimizerOptions(tmp)

        if self.option_handler.type[-1] != 'features' and self.option_handler.type[-1] != 'hippounit':
            if self.option_handler.run_controll_dt < self.data_handler.data.step:
                print("re-sampling because integration step is smaller then data step")
                print((self.option_handler.run_controll_dt,
                      self.data_handler.data.step))
                # we have to resample the input trace so it would match the model output
                # will use lin interpolation
                x = numpy.linspace(0, self.option_handler.run_controll_tstop, int(
                    # x axis of data points
                    self.option_handler.run_controll_tstop*(1/self.data_handler.data.step)))

                tmp = []
                for i in range(self.data_handler.number_of_traces()):
                    # y axis, the values from the input traces, corresponding to x
                    y = self.data_handler.data.GetTrace(i)

                    # we have the continuous trace, we could re-sample it now
                    new_x = numpy.linspace(0, self.option_handler.run_controll_tstop, int(
                        self.option_handler.run_controll_tstop/self.option_handler.run_controll_dt))
                    # self.trace_reader.SetColumn(i,f(new_x)) the resampled vector replaces the original in the trace reader object
                    tmp.append(numpy.interp(new_x, x, y))
                self.data_handler.data.t_length = len(tmp[0])
                self.data_handler.data.freq = self.option_handler.run_controll_tstop / \
                    self.option_handler.run_controll_dt
                self.data_handler.data.step = self.option_handler.run_controll_dt
                transp = list(map(list, list(zip(*tmp))))
                self.data_handler.data.data = []
                for n in transp:
                    self.data_handler.data.SetTrace(n)
            # running simulation with smaller resolution is not supported
            if self.option_handler.run_controll_dt > self.data_handler.data.step:
                self.option_handler.run_controll_dt = self.data_handler.data.step

        exec("self.optimizer="+self.option_handler.algorithm_name +
             "(self.data_handler,self.option_handler)")
        # self.optimizer=RANDOM_SEARCH(self.data_handler,self.option_handler)
        if self.option_handler.type[-1] == 'hippounit':
            self.option_handler.feat_str = ""  # TODO
        elif self.option_handler.type[-1] != 'features':
            self.option_handler.feat_str = ", ".join(
                [self.ffun_mapper[x.__name__] for x in self.option_handler.feats])
        else:
            self.option_handler.feat_str = ", ".join(self.option_handler.feats)

        if self.option_handler.algorithm_name != "SINGLERUN":
            with open(self.option_handler.GetFileOption()+"/"+self.option_handler.GetFileOption().split("/")[-1]+"_settings.json", 'w+') as outfile:
                json.dump(self.option_handler.CreateDictForJson(
                    self.ffun_mapper), outfile, sort_keys=True, indent=4)

            try:
                if (self.option_handler.simulator == 'Neuron'):
                    del self.model_handler
            except:
                "no model yet"

            start_time = time.time()
            self.optimizer.Optimize()
            stop_time = time.time()

            with open("eval.txt", "r") as ind_file:
                for line in ind_file:
                    solution = json.loads(line)
                    candidate = solution[1]
                    fitness = solution[0]
                    self.solutions.append(my_candidate(
                        candidate[:self.option_handler.num_params], fitness))

            """if self.option_handler.algorithm_name.split("_")[1] == "SCIPY":
				ordered_solutions = []
				for i in range(self.optimizer.size_of_population):
					for x in range(0,self.optimizer.number_of_generations*self.optimizer.size_of_population,self.optimizer.number_of_generations):
						ordered_solutions.append(self.solutions[x+i])
				self.solutions = ordered_solutions"""

            print(self.solutions[0].fitness)
            if isinstance(self.solutions[0].fitness, list):
                for solution in self.solutions:
                    wsum = sum([w*f for f, w in zip(solution.fitness,
                               self.option_handler.weights*self.data_handler.number_of_traces())])
                    solution.fitness = wsum
            self.solutions_by_generations = []
            try:
                os.remove(self.optimizer.directory + '/stat_file.txt')
                os.remove(self.optimizer.directory + '/ind_file.txt')
            except OSError:
                pass
            current_population = []
            for idx, solution in enumerate(self.solutions):
                current_population.append(solution)
                if not (idx+1) % self.optimizer.size_of_population:
                    self.solutions_by_generations.append(current_population)
                    current_population = []
            self.option_handler.WriteIndFile(self.solutions_by_generations)
            self.option_handler.WriteStatFile(self.solutions_by_generations)

            self.cands = [x.candidate for x in self.solutions]
            self.fits = [x.fitness for x in self.solutions]

            min_sol = min(self.solutions, key=lambda x: x.fitness)
            self.best_fit = min_sol.fitness
            self.best_cand = min_sol.candidate
            min_ind = self.fits.index(self.best_fit)+1
            print((self.best_cand, "Best Candidate (Normalized)"))
            print((self.best_fit, "Best Fitness"))
            print((min_ind, "Index of best individual"))
            print((len(self.solutions), "Number of Evaluations"))
            print(("Optimization lasted for ", stop_time-start_time, " s"))
            self.optimal_params = self.optimizer.fit_obj.ReNormalize(
                self.best_cand)

    def FourthStep(self, args={}):
        """
        Renormalizes the output of the ``optimizer`` (see optimizerHandler module for more), and runs
        a simulation with the optimal parameters to receive an optimal trace.
        The components of the fitness value is calculated on this optimal trace.
        Settings of the entire work flow are saved into a configuration file named "model name"_settings.xml.
        A report of the results is generated in the form of a html document.
        :param args: currently not in use
        """
        if self.option_handler.type[-1] == 'hippounit':
            self.optimizer.fit_obj.is_figures_saved = True

        self.best_fit = self.optimizer.fit_obj.single_objective_fitness(
            self.optimizer.fit_obj.normalize(self.optimal_params), delete_model=False)

        self.final_result = []
        self.error_comps = []

        if self.option_handler.type[-1] == 'hippounit':
            k_range = 1
            self.error_comps.append(
                self.optimizer.fit_obj.getTestErrorComponents())
        else:
            if self.option_handler.type[-1] != 'features':
                k_range = self.data_handler.number_of_traces()
            else:
                k_range = len(self.data_handler.features_data["stim_amp"])

            for k in range(k_range):
                self.error_comps.append(self.optimizer.fit_obj.getErrorComponents(
                    k, self.optimizer.fit_obj.model_trace[k]))
                trace_handler = open("result_trace"+str(k)+".txt", "w+")
                for l in self.optimizer.fit_obj.model_trace[k]:
                    trace_handler.write(str(l))
                    trace_handler.write("\n")
                trace_handler.close()
                self.final_result.append(self.optimizer.fit_obj.model_trace[k])

        if isinstance(self.optimizer.fit_obj.model, externalHandler):
            self.optimizer.fit_obj.model.record[0] = []

        # ---------------------------------------------------------------------------- #
        # TODO : result trace fig May not work with hippoUnit, Comment it then
        if self.option_handler.type[-1] != 'hippounit':
            fig, axes = plt.subplots(1, figsize=(7, 6))
            fig.clf()
            axes = fig.add_subplot(111)
            exp_data = []
            model_data = []
            if self.option_handler.type[-1] != 'features':
                for n in range(k_range):
                    exp_data.extend(self.data_handler.data.GetTrace(n))
                    model_data.extend(self.final_result[n])
            else:
                for n in range(k_range):
                    model_data.extend(self.final_result[n])
            if self.option_handler.type[-1] != 'features':
                t = int(self.option_handler.input_length)
            else:
                t = int(self.option_handler.run_controll_tstop)
            step = self.option_handler.run_controll_dt
            axes.set_xticks([n for n in range(
                0, int((t * k_range) / (step)), int((t * k_range) / (step) / 5.0))])
            axes.set_xticklabels([str(n) for n in range(
                0, int(t * k_range), int((t * k_range) / 5))])

            axes.set_xlabel("time [ms]")
            if self.option_handler.type[-1] != 'features':
                _type = self.data_handler.data.type
            else:
                _type = "Voltage" if self.option_handler.run_controll_record == "v" else "Current" if self.option_handler.run_controll_record == "c" else ""
            axes.set_ylabel(
                _type + " [" + self.option_handler.input_scale + "]")
            if self.option_handler.type[-1] != 'features':
                axes.plot(list(range(0, len(exp_data))), exp_data)
                axes.plot(list(range(0, len(model_data))), model_data, 'r')
                axes.legend(["target", "model"])
            else:
                axes.plot(list(range(0, len(model_data))), model_data, 'r')
                axes.legend(["model"])
            fig.savefig("result_trace.png", dpi=None, facecolor='w', edgecolor='w',
                        orientation='portrait', format=None, bbox_inches=None, pad_inches=0.1)
            # fig.savefig("result_trace.eps", dpi=None, facecolor='w', edgecolor='w')
            fig.savefig("result_trace.svg", dpi=None,
                        facecolor='w', edgecolor='w')
        # ---------------------------------------------------------------------------- #

        self.name = self.option_handler.model_path.split("/")[-1].split(".")[0]
        f_handler = open(self.name+"_results.html", "w+")
        tmp_str = "<!DOCTYPE html>\n<html>\n<body>\n"
        tmp_str += self.htmlStr(str(time.asctime(time.localtime(time.time()))))+"\n"
        if not self.option_handler.type[-1] == 'hippounit':
            tmp_str += "<p>"+self.htmlStyle("Optimization of <b>"+self.name+".hoc</b> based on: " +
                                            self.option_handler.input_dir, self.htmlAlign("center"))+"</p>\n"
        else:  # TODO: Add more infromative text for hippounit
            tmp_str += "<p>" + \
                self.htmlStyle("Optimization of <b>"+self.name +
                               ".hoc</b>  ", self.htmlAlign("center"))+"</p>\n"
        tmp_list = []
        tmp_fit = self.optimal_params
        for name, mmin, mmax, f in zip(self.option_handler.GetObjTOOpt(), self.option_handler.boundaries[0], self.option_handler.boundaries[1], tmp_fit):
            tmp_list.append([str(name), str(mmin), str(mmax), str(f)])
        param_list = tmp_list
        tmp_str += "<center><p>" + \
            self.htmlStyle("Results", self.htmlUnderline(),
                           self.htmlResize(200))+"</p></center>\n"
        tmp_str += self.htmlTable(["Parameter Name",
                                  "Minimum", "Maximum", "Optimum"], tmp_list)+"\n"
        tmp_str += "<center><p>"+self.htmlStrBold("Fitness: ")
        tmp_str += self.htmlStrBold(str(self.best_fit))+"</p></center>\n"

        # TODO: what to plot in the html in the case of hippounit for each test type?
        if self.option_handler.type[-1] == "hippounit":
            hippounit_settings = self.optimizer.fit_obj.model.settings
            model_name = hippounit_settings["model"]["name"]
            # test_name = 'somaticfeat'
            test_name = ""
            tests = hippounit_settings["model"]["tests"]
            for test in tests:  # filling test_name
                test_name += test + "_"
            test_name = test_name[:-1]
            dataset_name = hippounit_settings["model"]["dataset"]
            pdf_path = "output/figs/{}_{}/{}/traces.pdf".format(
                test_name, dataset_name, model_name)
            tmp_str += self.htmlPdf(pdf_path)+"\n"
        else:
            tmp_str += self.htmlPciture("result_trace.png")+"\n"

        for k in list(self.option_handler.GetOptimizerOptions().keys()):
            tmp_str += "<p><b>"+k+" =</b> " + \
                str(self.option_handler.GetOptimizerOptions()[k])+"</p>\n"
        tmp_str += "<p><b>feats =</b> "+self.option_handler.feat_str + "</p>\n"
        tmp_str += "<p><b>weights =</b> " + \
            str(self.option_handler.weights)+"</p>\n"
        tmp_str += "<p><b>user function =</b></p>\n"
        for l in (self.option_handler.u_fun_string.split("\n")[4:-1]):
            tmp_str += "<p>"+l+"</p>"
        tmp_str += "</body>\n</html>\n"
        tmp_str += "<p><b>Fitness Components:</b></p>\n"
        tmp_w_sum = 0
        tmp_list = []
        for t in self.error_comps:
            for c in t:
                if self.option_handler.type[-1] != 'features' and self.option_handler.type[-1] != 'hippounit':
                    # tmp_str.append( "*".join([str(c[0]),c[1].__name__]))
                    tmp_list.append([self.ffun_mapper[c[1].__name__],
                                     str(c[2]),
                                     str(c[0]),
                                     str(c[0]*c[2]), ""])
                    tmp_w_sum += c[0]*c[2]
                else:
                    tmp_list.append([c[1],
                                     str(c[2]),
                                     str(c[0]),
                                     str(c[0]*c[2]), ""])
                    tmp_w_sum += c[0]*c[2]
            tmp_list.append(["", "", "", "", tmp_w_sum])
            tmp_w_sum = 0
        error_comps_list = tmp_list
        tmp_str += self.htmlTable(["Name", "Value", "Weight",
                                  "Weighted Value", "Weighted Sum"], tmp_list)+"\n"
        tmp_list = []
        for c in zip(*self.error_comps):
            tmp = [0]*4
            for t_idx in range(len(c)):
                tmp[1] += c[t_idx][2]
                tmp[2] = c[t_idx][0]
                tmp[3] += c[t_idx][2]*c[t_idx][0]
            if self.option_handler.type[-1] != 'features' and self.option_handler.type[-1] != 'hippounit':
                tmp[0] = self.ffun_mapper[c[t_idx][1].__name__]
            else:
                tmp[0] = (c[t_idx][1])
            tmp = list(map(str, tmp))
            tmp_list.append(tmp)

        tmp_str += self.htmlTable(["Name", "Value",
                                  "Weight", "Weighted Value"], tmp_list)+"\n"
        f_handler.write(tmp_str)
        f_handler.close()

        if self.option_handler.algorithm_name != "SINGLERUN":
            param_dict = [{"name": value[0], "min_boundary": value[1],
                           "max_boundary": value[2], "optimum": value[3]} for value in param_list]
            error_dict = [{"name": value[0], "value": value[1], "weight": value[2],
                           "weighted_value": value[3]} for value in tmp_list]
            algo_name = self.option_handler.algorithm_name.split("_")
            algorithm_parameters = [{"parameter_name": p_name, "parameter_value": str(
                p_value)} for p_name, p_value in self.option_handler.algorithm_parameters.items()]
            alg_dict = {
                "algorithm_name": algo_name[0], "algorithm_package": algo_name[1], "algorithm_parameters": algorithm_parameters}
            target_dict = {"data_type": self.option_handler.type[-1], "file_name": self.option_handler.input_dir.split('/')[-1], "number_of_traces": k_range, "stim_delay": self.option_handler.stim_del,
                           "stim_duration": self.option_handler.stim_dur}
            json_var = {"opt_name": self.name+"_"+self.option_handler.algorithm_name+str(datetime.utcnow().strftime("_%d_%b_%Y_%H:%M:%S:%f")), "seed": self.option_handler.seed, "final_fitness": self.best_fit, "number_of_evaluations": len(self.solutions),
                        "models": {"model_name": self.name, "model_author": os.uname()[1]}, "parameters": param_dict, "error_function": error_dict, "algorithm": [alg_dict], "target_data": target_dict, "created_at": datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%S.%fZ")}

            if self.option_handler.type[-1] == 'hippounit':
                with open('metadata.json', 'w+') as outfile:
                    json.dump(json_var, outfile, indent=4)
            elif self.option_handler.type[-1] == 'features':
                with open(self.option_handler.input_dir, 'r') as outfile:
                    input_features = json.load(outfile)
                    amp_list = []
                    for x, y in input_features["features"].items():
                        for t, p in y.items():
                            if ('stimAmp') in t:
                                feats = p
                                feats["name"] = x
                                amp_list.append({"stim_amplitude": float(t.replace('stimAmp_', '')), "features": [
                                                {k.lower(): v for k, v in feats.items()}]})
                    json_var["target_data"].update(
                        {"stim_amp": sorted(amp_list, key=lambda d: d["stim_amplitude"])})
            else:
                json_var["target_data"].update({"length_ms": self.data_handler.data.t_length, "sampling_frequency": self.data_handler.data.freq, "stim_amp": [
                                               {"stim_amplitude": stim} for stim in self.option_handler.stim_amp]})
            json_var["target_data"] = [json_var["target_data"]]
            json_stat = []
            for idx, current_generation in enumerate(self.solutions_by_generations):
                generation_fitness = [x.fitness for x in current_generation]
                json_stat.append({"generation": idx, "population": len(current_generation),
                                  "maximum": np.max(generation_fitness), "minimum": np.min(generation_fitness),
                                  "median": np.median(generation_fitness), "mean": np.mean(generation_fitness), "std": np.std(generation_fitness)})
            json_var["statistics"] = json_stat
            with open('metadata.json', 'w+') as outfile:
                json.dump(json_var, outfile, indent=4)

    def callGrid(self, resolution):
        """
        Calculates fitness values on a defined grid (see optimizerHandler module for more).
        This tool is purely for analyzing results, and we do not recommend to use it to obtain parameter values.
        """
        import copy
        self.prev_result = copy.copy(self.solutions)
        self.optimizer = grid(
            self.data_handler, self.optimizer.fit_obj.model, self.option_handler, resolution)
        self.optimizer.Optimize(self.optimal_params)
        self.grid_result = copy.copy(self.solutions)
        self.solutions = self.prev_result
