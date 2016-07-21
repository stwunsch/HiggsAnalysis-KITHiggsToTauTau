#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os
import sys
import ROOT
from scipy import stats
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True



def get_tex_mask(samples, dim=2, form=""):
	tex_string = r"{channel} & {category}"
	for sample in samples:
		tex_string += r" & ${%s:.%i%s}$"%(sample, dim, form)
	tex_string += r" \\"+"\n"
	return tex_string

def get_upper_limit(chi2_val, number):
	nums = number*1.0
	last_nums = number*0.9
	stat = 0
	last_stat = 0
	if number < 1:
		return 3.7
	while True:
		stat = stats.chi2.cdf(nums, 2 * (number+1))
		if abs(stat - chi2_val) < 0.0001:
			break
		if stat > chi2_val and last_stat < chi2_val:
			keep = nums
			nums = last_nums + 0.5*(nums-last_nums)
			last_nums = keep
			last_stat = stat
		elif stat < chi2_val and last_stat > chi2_val:
			keep = nums
			nums = nums + 0.5*(last_nums-nums)
			last_nums = keep
			last_stat = stat
		elif stat > chi2_val and last_stat > chi2_val:
			keep = nums
			nums = nums * 0.5
			last_nums = keep
			last_stat = stat
		elif stat < chi2_val and last_stat < chi2_val:
			keep = nums
			nums = nums * 2.
			last_nums = keep
			last_stat = stat
	return nums/2.
















if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Write Table from root files: integral for each sample, (calculate upper poisson limit)",
									 parents=[logger.loggingParser])
	parser.add_argument("-i", "--input-dir", required=True,
						help="Input directory. Use directory of output from makePlots_controlPlots.py")
	parser.add_argument("-c", "--channels", nargs="*",
						default=["tt", "mt", "et", "em", "mm", "ee"],
						help="Channels. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="+", default=["inclusive"],
	                    help="Categories. [Default: %(default)s]")
	parser.add_argument("--higgs-mass", default="125",
						help="Higgs mass. [Default: %(default)s]")
	parser.add_argument("-o", "--output-file",
							default="XS-Table.tex",
							help="Output dir. [Default: %(default)s]")
	parser.add_argument("-n", "--norm",
							default=False,
							help="norm all XS to this samples XS. [Default: %(default)s]")
	parser.add_argument("-s", "--samples", nargs="+",
						default=["ggh", "qqh", "ztt", "zll", "ttj", "vv", "wj"],
						choices=["ggh", "qqh", "ztt", "zll", "ttj", "vv", "wj", "vv_ngm", "vv_gm",],
						help="Samples for correlation calculation and scatter plots. [Default: %(default)s]")
	parser.add_argument("--plot-vars", nargs="+", default=["all"],
						help = "plot correlation for those variables. [Default: %(default)s]")
	parser.add_argument("--lumi", type = int, default = 2305,
						help="lumi in inverse pb. [Default: %(default)s]")
	args = parser.parse_args()
	logger.initLogger(args)
	base_path = args.input_dir
	info_vector = {}
	for channel in args.channels:
		info_vector[channel] = {}
		for category in args.categories:
			info_vector[channel][category] = {}
			infile = ROOT.TFile(os.path.join(base_path, channel, category, "integral.root"), "READ")
			for sample in args.samples:
				sample_name = sample if sample not in ["ggh", "qqh"] else sample+args.higgs_mass
				thist = infile.Get(sample_name)
				number = thist.GetBinContent(1)
				print sample, number
				if sample == "ztt":
					number = get_upper_limit(0.025, number)
				else:
					number = get_upper_limit(0.975, number)
				number = number / args.lumi * 1000
				info_vector[channel][category][sample]=number

	if args.norm:
		for channel in args.channels:
			for category in args.categories:
				norm_val = info_vector[channel][category][args.norm]
				for sample in args.samples:
					info_vector[channel][category][sample]/=norm_val

	with open(args.output_file, "w") as out_file:
		out_file.write(r"\begin{center}"+"\n"+r"\begin{tabular}{%s}"%("l"*(len(args.samples)+2))+"\n")
		tex_mask = get_tex_mask(args.samples, 10)
		print tex_mask
		out_file.write(tex_mask.format(channel=" ", category="Jets", **dict(zip(args.samples, args.samples))))
		tex_mask = get_tex_mask(args.samples, 3, "G")
		print tex_mask
		for channel in args.channels:
			for category in args.categories:
				cat_string = category.replace("Jet30", "")
				out_file.write(tex_mask.format(channel="\\"+channel+"c", category=cat_string, **info_vector[channel][category]).replace("E+0",r"\cdot10^"))
		out_file.write(r"\end{tabular}"+"\n"+r"\end{center}"+"\n")