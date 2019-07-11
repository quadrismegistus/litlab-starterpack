#!/usr/bin/env python

from __future__ import print_function
import shutil,os,sys
from os.path import expanduser
HOME=expanduser("~")
PIP_PACKAGES=['bs4','xopen','bleach','ujson','unicodecsv','mpi4py','numpy','pandas','scipy'] #,'scikit-learn']
#BREW_CASK_CMD='ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" < /dev/null 2> /dev/null ; brew install caskroom/cask/brew-cask 2> /dev/null'



"""
BREW_INSTALL_CMDS = [
	#BREW_CASK_CMD,
	'brew install wget',
	'brew cask install iterm2',
	'brew cask install textmate'
]
"""

def exec(cmd):
	print('>> executing:',cmd)
	os.system(cmd)

def test_if_exec_exists(exec_name):
	return bool(shutil.which(exec_name))


## STEP 1. Check Brew


def check_brew():
	cmd_install_brew='/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"'

	print('>> Checking whether HomeBrew is installed...')
	brew_path = shutil.which('brew')
	if not brew_path:
		print('\n!! Homebrew not installed!')
		answer = input('\n?? Would you like to install homebrew? [Y/n]\n')
		if answer.strip().lower()!='n':
			exec(cmd_install_brew)
			return check_brew()
		else:
			print('>> Please install Homebrew on your own: https://brew.sh/')
			return False

	return True






## Step 2. Check Anaconda



def check_anaconda():
	print('>> Checking whether Anaconda (for Python 3.x) is installed...')
	anaconda_path = shutil.which('conda')
	pip_path = shutil.which('pip')
	python_path = shutil.which('python')
	if not anaconda_path or not 'anaconda3' in anaconda_path or not 'anaconda3' in pip_path:
		print('\n!! Anaconda3 not installed!')
		answer = input('\n?? Would you like to install Anaconda3? [Y/n]\n')
		if answer.strip().lower()!='n':
			exec('brew cask install anaconda')
			return check_anaconda()
		else:
			print('>> Please install Anaconda for Python 3.x on your own: https://www.anaconda.com/distribution/')
			return False

	else:
		return True

def add_anaconda_to_path():
	anaconda_path = shutil.which('conda')
	anaconda_bin_path = os.path.split(anaconda_path)[0]

	ofn=os.path.join(HOME,'.bash_profile')
	with open(ofn,'a+') as of:
		print('\n\nexport PATH=%s:$PATH' % anaconda_bin_path)





## Step 3. Check pip packages


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





def check_apps():
	print('>> Checking whether basic Mac apps are installed...')
	#for cmd in BREW_INSTALL_CMDS:
	#	exec(cmd)

	if not os.path.exists('/Applications/TextMate.app'):
		print('>> Installing TextMate, a good and open-source text editor for Mac...')
		exec('brew cask install textmate')

	if not os.path.exists('/Applications/iTerm.app'):
		print('>> Installing iTerm2, a good and open-source terminal for Mac...')
		exec('brew cask install iterm2')

	if not test_if_exec_exists('wget'):
		print('>> Installing wget, which lets us download things from the Terminal...')
		exec('brew install wget')

	if not test_if_exec_exists('git'):
		print('>> Installing git, which lets us use github to download/upload code collaboratively...')
		exec('brew install git')

	return True



## MAIN

def run_all():
	# What are the steps
	#steps = [check_anaconda, check_packages]
	steps = [check_brew, check_anaconda, check_packages, check_apps]
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
