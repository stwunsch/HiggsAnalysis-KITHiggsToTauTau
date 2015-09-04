# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re


class DatacardConfigs(object):
	def __init__(self):
		super(DatacardConfigs, self).__init__()
		
		self._mapping_process2sample = {
			"data_obs" : "data",
			"ZTT" : "ztt",
			"TTJ" : "ttj",
			"VV" : "vv",
			"WJ" : "wj",
			"QCD" : "qcd",
			"ggH" : "ggh",
			"qqH" : "qqh",
			"VH" : "vh",
		}
		
		self._mapping_category2binid = {
			"mt" : {
				"inclusive" : 0,
				"zerojet" : 1,
				"onejet" : 2,
				"twojet" : 3,
			},
			"et" : {
				"inclusive" : 0,
				"zerojet" : 1,
				"onejet" : 2,
				"twojet" : 3,
			},
			"em" : {
				"inclusive" : 0,
				"zerojet" : 1,
				"onejet" : 2,
				"twojet" : 3,
			},
			"tt" : {
				"inclusive" : 0,
				"zerojet" : 1,
				"onejet" : 2,
				"twojet" : 3,
			},
		}
	
	def process2sample(self, process):
		tmp_process = re.match("(?P<process>[^0-9]*).*", process).groupdict().get("process", "")
		return process.replace(tmp_process, self._mapping_process2sample.get(tmp_process, tmp_process))
	
	def sample2process(self, sample):
		tmp_sample = re.match("(?P<sample>[^0-9]*).*", sample).groupdict().get("sample", "")
		return sample.replace(tmp_sample, dict([reversed(item) for item in self._mapping_process2sample.iteritems()]).get(tmp_sample, tmp_sample))
	
	def category2binid(self, category, channel="default"):
		return self._mapping_category2binid.get(channel, {}).get(category, 0)
	
	def binid2category(self, binid, channel="default"):
		return dict([reversed(item) for item in self._mapping_category2binid.get(channel, {}).iteritems()]).get(binid, "inclusive")
