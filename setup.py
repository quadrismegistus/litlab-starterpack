#!/usr/bin/env python

from __future__ import print_function
import shutil,os,sys
from os.path import expanduser
HOME=expanduser("~")

PIP_PACKAGES=['bs4','xopen','bleach','ujson','unicodecsv','mpi4py','numpy','pandas','scipy','scikit-learn']

## CHECKING ANACONDA
def check_anaconda():
	print('>> Checking whether Anaconda (for Python 3.x) is installed...')
	anaconda_path = shutil.which('conda')
	pip_path = shutil.which('pip')
	python_path = shutil.which('python')
	if not anaconda_path:
		print('\n!! Looks like Anaconda is not installed. Please download it (for Python 3.x) and install it here: https://www.anaconda.com/distribution/')
		return False
	elif 'anaconda2' in anaconda_path or not 'anaconda3' in anaconda_path:
		print('\n!! Looks like you have Anaconda installed for Python 2, not 3. Please install it for Python 3.x by downloading it here: https://www.anaconda.com/distribution/')
		return False

	elif not 'anaconda3' in pip_path:
		print('\n!! Anaconda is installed, but the default "pip" command is not pointing to Anaconda3.')
		answer = input('\n?? Would you like to add anaconda3 to your $PATH to solve this problem? [Y/n]\n')
		if answer.strip().lower()!='n':
			add_anaconda_to_path()
			print('\n>> Success! Now please re-run the setup.')

	else:
		return True

def add_anaconda_to_path():
	anaconda_path = shutil.which('conda')
	anaconda_bin_path = os.path.split(anaconda_path)[0]

	ofn=os.path.join(HOME,'.bash_profile')
	with open(ofn,'a+') as of:
		print('\n\nexport PATH=%s:$PATH' % anaconda_bin_path)






## PIP
def check_packages():
	import importlib.util

	print('>> Installing common Python packages...')
	print()

	for pkg in PIP_PACKAGES:
		spec = importlib.util.find_spec(pkg)
		if spec is None:
			print('>>',pkg +" is not installed...")
			cmd='pip install %s' % pkg
			print('>> executing:',cmd)
			os.system(cmd)

	return True






## MAIN

def run_all():
	# What are the steps
	steps = [check_anaconda, check_packages]
	num_steps = len(steps)

	for i,step in enumerate(steps):
		print('\n>> Step #%s of %s' % (i+1, num_steps))
		res=step()
		if res is not True:
			exit()
		else:
			print('>> Success!')

if __name__=='__main__':
	print('Welcome to the Literary Lab Starter Pack Installer!')

	run_all()
