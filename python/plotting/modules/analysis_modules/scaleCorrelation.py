# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import hashlib

import Artus.HarryPlotter.analysisbase as analysisbase
import Artus.HarryPlotter.utility.roottools as roottools
import Artus.HarryPlotter.analysis_modules.scaleerrors as scaleerrors


class ScaleCorrelation(analysisbase.AnalysisBase):
	"""Reweight MC to fit Data correlation"""

	def modify_argument_parser(self, parser, args):
		super(ScaleCorrelation, self).modify_argument_parser(parser, args)

		self.scaleCorrelation_options = parser.add_argument_group("{} options".format(self.name()))
		self.scaleCorrelation_options.add_argument(
				"--scale-correlation-datanick",
				help="Nick names for the numerators of the ratio. Multiple nicks (whitespace separated) will be summed up before calculating the ratio."
		)
		self.scaleCorrelation_options.add_argument(
				"--scale-correlation-mc-nicks", default=[False],
				help="Remove errors of numerator histograms before calculating the ratio. [Default: %(default)s]"
		)
		self.scaleCorrelation_options.add_argument(
				"--scale-correlation-nicks", default=[False],
				help="Remove errors of numerator histograms before calculating the ratio. [Default: %(default)s]"
		)

	def prepare_args(self, parser, plotData):
		super(ScaleCorrelation, self).prepare_args(parser, plotData)
		self.prepare_list_args(plotData, ["scale_correlation_datanick", "scale_correlation_mc_nicks", "scale_correlation_nicks"])

	def run(self, plotData=None):
		super(ScaleCorrelation, self).run(plotData)
		weight_data = plotData.plotdict["root_objects"][plotData.plotdict["scale_correlation_datanick"][0]].Project3D("zy")
		weight_mc = roottools.RootTools.add_root_histograms(*[plotData.plotdict["root_objects"][nick] for nick in plotData.plotdict["scale_correlation_mc_nicks"][0].split(" ")]).Project3D("zy")
		log.warning(plotData.plotdict["root_objects"][plotData.plotdict["scale_correlation_datanick"][0]].GetYaxis().GetBinCenter(1))
		log.warning(weight_data.GetXaxis().GetBinCenter(1))
		reweight_list = []
		for x in range(1, weight_data.GetNbinsX()+1):
			for y in range(1, weight_data.GetNbinsY()+1):
				try:
					weight = weight_data.GetBinContent(x,y)/weight_mc.GetBinContent(x,y)
					weight_mc.SetBinContent(x,y, weight_mc.GetBinContent(x,y)*weight)
					if weight > 0:
						reweight_list.append((x,y,weight))
				except ZeroDivisionError:
					continue
		print weight_mc.GetCorrelationFactor(), weight_data.GetCorrelationFactor()
		#print reweight_list, len(reweight_list)
		for mc_nick in plotData.plotdict["scale_correlation_nicks"][0].split(" "):
			for x in range(1,plotData.plotdict["root_objects"][mc_nick].GetNbinsX()+1):
				pass
				for reweight in reweight_list:
					plotData.plotdict["root_objects"][mc_nick].SetBinContent(x, reweight[0], reweight[1], plotData.plotdict["root_objects"][mc_nick].GetBinContent(x, reweight[0], reweight[1])*reweight[2])
			plotData.plotdict["root_objects"][mc_nick] = plotData.plotdict["root_objects"][mc_nick].Project3D("x")
		plotData.plotdict["root_objects"]["data"] = plotData.plotdict["root_objects"]["data"].Project3D("x")

