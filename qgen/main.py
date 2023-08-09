#!/usr/bin/env python
# coding: utf-8
import argparse
import sys,os
import itertools
import logging
from qgen.generator.run import gene_run
from qgen import info
from qgen.collect.init_c import gene_c
from qgen.collect.init_conf import init_conf
__author__ = "Lv Xinmao"
__copyright__ = "Copyright 2022, @TCCL"
__maintainer__ = "Lv Xinmao"
__email__ = ""

def main():
	info()

	print("Description\n-------")
	parser = argparse.ArgumentParser(description="""
	Inspired by DPgen,Qgen is an iterative workflow used with VaspSOL and JDFTX 
	to solve the number of electrons carried in the system of 
	different materials under the condition of constant potential.
	Enter "qgen-h" for more information.""")

	subparsers = parser.add_subparsers()

	# run 
	parser_run = subparsers.add_parser(
		"run",
		help="At the set voltage, the number of electrons in the system is solved iteratively")
	parser_run.add_argument('PARAM', type=str,
						help="json format file which should contains all the para that the iteration needs.")
	parser_run.set_defaults(func=gene_run)

	# init_c
	parser_initc = subparsers.add_parser(
		"init_c",
		help="calculate the capacitance value of this material-UNDER BUILDING")
	parser_initc.add_argument('PARAM', type=str,
						help="UNDER BUILDING")
	parser_initc.set_defaults(func=gene_c)


	#init_conf
	parser_initconf = subparsers.add_parser(
		"init_conf",
		help="using idpp algorithm to generate the intermediate structure of TI. ")
	parser_initconf.add_argument('-i', '--images', nargs='+',
				   type=str, help='Images defining path from initial to final state.')
	parser_initconf.add_argument('-n', '--nimage', type=int, default=7,
				   help='Number of images in a band. Default: 6')
	# 是否写入XDATCAR。
	parser_initconf.add_argument('-o', '--output', action='store_true',
				   help='Whether or not write XDATCAR.')
	# 插点方法，可选线性插点或idpp，默认用idpp。
	parser_initconf.add_argument('--method', type=str, choices=['linear', 'idpp'], default='idpp',
				   help='Interpolate method to initial guess. Default: linear')
	# idpp插点最大迭代步数，默认是100。
	parser_initconf.add_argument('--nstep', type=int, default=100,
				   help='Max number of iteration steps. Default: 100')
	# 弹簧常数，默认按照ase.neb.NEB的0.1。
	parser_initconf.add_argument('--spring', type=float, default=0.1,
				   help='Fraction of spring force. Default: 0.1')
	# idpp插点迭代的力收敛域值，默认按照ase.neb.NEB的0.1。
	parser_initconf.add_argument('--fmax', type=float, default=0.1,
				   help='Maximum force of converge thershould. Default: 0.1')
	# idpp插点迭代所使用的优化算法，默认为ase.optimize.MDMin。
	parser_initconf.add_argument('--optimizer', type=str, choices=['MDMin', 'BFGS', 'LBFGS', 'FIRE'],
				   default='MDMin', help='Optimizer using in IDPP iteration. Default: MDMin')

	parser_initconf.set_defaults(func=init_conf)

	try:
		import argcomplete
		argcomplete.autocomplete(parser)
	except ImportError:
		# argcomplete not present.
		pass

	args = parser.parse_args()

	try:
		getattr(args, "func")
	except AttributeError:
		parser.print_help()
		sys.exit(0)
	args.func(args)


if __name__ == "__main__":
	main()

