# -*- coding: utf-8 -*-
import itertools
import pprint
import numpy
import copy
import json

class CategoriesDict(object):
	def __init__(self):
		super(CategoriesDict, self).__init__()
		boosted_higgs_string = "(H_pt>100)"
		boosted_higgs_medium_string = "(H_pt>50)"
		boosted_higgs_low_string = "(H_pt>30)"
		vbf_medium_string = "(mjj>500&&jdeta>3.5)"
		vbf_loose_string = "(mjj>200&&jdeta>2)"
		jet2_string = "(njetspt30>1)"
		jet2x_string = "(njetspt30==2)"
		jet1_string = "(njetspt30==1)"
		jet0_string = "(njetspt30==0)"
		pt2_tight_string = "(pt_2>=45)"
		pt2_medium_string = "(pt_2>=35)"
		pt2_loose_string = "(pt_2>=25)"
		eta_hard_string = "jdeta>4.0"
		auto_rebin_binning = " ".join([str(float(f)) for f in range(0,251,10)])
		self.pp = pprint.PrettyPrinter(indent=4)
		self.categoriesDict = {}

                # Load config # FIXME: Hacky!
                # NOTE: WTF, Combine does not take unicode strings...
                config = json.load(open('/portal/ekpbms2/home/wunsch/UncEst/framework/config_stat.json'))

                hist_variables_unicode = config['variables']
                hist_variables = []
                for var in hist_variables_unicode:
                    hist_variables.append(var.encode('ascii'))

                hist_bins = config['bins']
                hist_ranges = {}
                for key in hist_bins:
                    hist_ranges[key] = [str(float(f)) for f in eval(hist_bins[key])]

                hist_categories_unicode = config['categories']
                hist_categories = {}
                for key in hist_categories_unicode:
                    hist_categories[key.encode('ascii')] = hist_categories_unicode[key].encode('ascii')

                for category in hist_categories:
                    for i_var1, var1 in enumerate(hist_variables):
                        # Add categories for single variables
                        global_expression = "({})".format(hist_categories[category])
                        self.categoriesDict["{analysis}{channel}%s_%s{discriminator}"%(category, var1)] = {
                                        "channel": [
                                                    "mt_",
                                                    ],
                                        "expressions":{
                                                    "global": global_expression,
                                                    "analysis": [
                                                                "catHtt13TeV_",
                                                                ],
                                                    },
                                        "binnings":{
                                                    "analysis": [
                                                                "binningHtt13TeV_",
                                                                ],
                                                    "global":{
                                                            "_{}".format(var1):" ".join(hist_ranges[var1]),
                                                            }
                                                    }
                                            }

                        # Add categories for variable pairs
                        for i_var2, var2 in enumerate(hist_variables):
                            # Ensure that every pair appears only once
                            if i_var1 >= i_var2:
                                continue

                            # Set up category for this slice
                            for i_slice in range(len(hist_ranges[var2])-1):
                                global_expression = "({}) && ({}>{}) && ({}<{})".format(
                                                            hist_categories[category],
                                                            var2, hist_ranges[var2][i_slice],
                                                            var2, hist_ranges[var2][i_slice+1])
                                self.categoriesDict["{analysis}{channel}%s_%s_%s_%s{discriminator}"%(category, var1, var2, str(i_slice))] = {
                                                "channel": [
                                                        "mt_",
                                                        ],
                                                "expressions":{
                                                        "global": global_expression,
                                                        "analysis": [
                                                                "catHtt13TeV_",
                                                                ],
                                                        },
                                                "binnings":{
                                                        "analysis": [
                                                                "binningHtt13TeV_",
                                                                ],
                                                        "global":{
                                                                "_{}".format(var1):" ".join(hist_ranges[var1]),
                                                                }
                                                        }
                                                }
		for class_ in ['PyKeras']:
                    for iClass in [0, 1, 2, 3]:
                        self.categoriesDict["{analysis}{channel}%sClass_%i{discriminator}"%(class_, iClass)] = {
                                        "channel": [
                                                "mt_",
                                                ],
                                        "expressions":{
                                                "global":"class{}=={}".format(class_, iClass),
                                                "analysis": [
                                                        "catHtt13TeV_",
                                                        ],
                                                },
                                        "binnings":{
                                                "analysis": [
                                                        "binningHtt13TeV_",
                                                        ],
                                                "global":{
                                                        "_m_sv":" ".join([str(float(f)) for f in numpy.linspace(50,200,20)]),
                                                        }
                                                }
                                        }
                    for iClass in [4]:
                        self.categoriesDict["{analysis}{channel}%sClass_%i{discriminator}"%(class_, iClass)] = {
                                        "channel": [
                                                "mt_",
                                                ],
                                        "expressions":{
                                                "global":"class{}=={}".format(class_, iClass),
                                                "analysis": [
                                                        "catHtt13TeV_",
                                                        ],
                                                },
                                        "binnings":{
                                                "analysis": [
                                                        "binningHtt13TeV_",
                                                        ],
                                                "global":{
                                                        "_m_sv":" ".join([str(float(f)) for f in numpy.linspace(50,200,8)]),
                                                        }
                                                }
                                        }
                    for iClass in [5]:
                        self.categoriesDict["{analysis}{channel}%sClass_%i{discriminator}"%(class_, iClass)] = {
                                        "channel": [
                                                "mt_",
                                                ],
                                        "expressions":{
                                                "global":"class{}=={}".format(class_, iClass),
                                                "analysis": [
                                                        "catHtt13TeV_",
                                                        ],
                                                },
                                        "binnings":{
                                                "analysis": [
                                                        "binningHtt13TeV_",
                                                        ],
                                                "global":{
                                                        "_m_sv":" ".join([str(float(f)) for f in numpy.linspace(50,200,8)]),
                                                        }
                                                }
                                        }
		#print self.categoriesDict
		self.calculateBinnings()
		self.calculateExpressions()
		self.calculateDataCards()
	def calculateBinnings(self):
		self.binnings = {}
		for name, info in self.categoriesDict.iteritems():
			#print name
			channels = info["channel"]
			analysis = info["binnings"]["analysis"]
			global_keys = info["binnings"].get("global", {}).keys()
			for (channel,ana) in itertools.product(channels, analysis):
				#print channel, ana
				discriminators = global_keys
				if channel in info["binnings"].keys():
					discriminators += [x for x in info["binnings"][channel].keys() if not x in global_keys]
				for discriminator in discriminators:
					binning_string = info["binnings"].get(channel, info["binnings"]["global"]).get(discriminator, info["binnings"]["global"][discriminator])
					self.binnings[name.format(analysis=ana, channel=channel, discriminator=discriminator)]=binning_string

	def calculateDataCards(self):
		pass

	def calculateExpressions(self):
		self.expressions = {}
		for name, info in self.categoriesDict.iteritems():
			#print name
			channels = info["channel"]
			analysis = info["expressions"]["analysis"]
			global_expression = info["expressions"].get("global", "")
			for (channel,ana) in itertools.product(channels, analysis):
				expression = global_expression
				if channel in info["expressions"].keys():
					expression = self.combine([expression, info["expressions"][channel]])
				self.expressions[name.format(analysis=ana, channel=channel, discriminator="")]=expression
		#self.pp.pprint(self.expressions)

	def getExpressionsDict(self):
		return self.expressions

	def getBinningsDict(self):
		return self.binnings

	def getCategories(self, channels, prefix = True):
		Categories = {}
		placeholder=0
		for chan in channels:
			Categories[chan] = []
		for name, info in self.categoriesDict.iteritems():
			for chan in channels:
				if chan+"_" in info["channel"]:
					Categories[chan].append(name.format(analysis="", channel=(chan+"_") if prefix else "", discriminator=""))
				else:
					Categories[chan].append("placeholder{ph}".format(ph=placeholder))
					placeholder += 1
		return Categories

	def invert(self, expression):
		tmp_expression = "(" + expression + ")"
		return "(" + tmp_expression + "==0)"

	def combine(self, strings_to_combine):
		return "(" + "*".join(strings_to_combine) + ")"
