#!/usr/bin/env python

from __future__ import print_function
import shutil,os,sys,subprocess,webbrowser,time
from os.path import expanduser
HOME=expanduser("~")
PIP_PACKAGES=sorted(['bs4','xopen','bleach','ujson','unicodecsv','mpi4py','numpy','pandas','scipy','paramiko']) #,'scikit-learn']
#BREW_CASK_CMD='ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" < /dev/null 2> /dev/null ; brew install caskroom/cask/brew-cask 2> /dev/null'



GITHUB_USERNAME='quadrismegistus'
GITHUB_EMAIL='heuser@stanford.edu'

NAP=5


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

def hidden_exec(cmd):
	output=''
	try:
		#output=subprocess.check_output(cmd.split())
		result = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
		output = result.stdout
	except subprocess.CalledProcessError as e:
		print(e.output)
	return str(output)

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


## GIT

def check_ssh():
	import paramiko
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	try:
		#ssh.connect('github.com', username='git', key_filename=key_file)
		ssh.connect('github.com', username='git')
		print('>> Successfully connected to Github\'s SSH server!')
		return True
	except (BadHostKeyException, AuthenticationException, SSHException, socket.error) as e:
		print(e)
		#sleep(interval)
		return False

def get_git_user_info():
	global GITHUB_USERNAME,GITHUB_EMAIL

	if not GITHUB_USERNAME: GITHUB_USERNAME = input('\n>> What is your github username? (If you do not have one, please register now @ https://github.com)\n')
	if not GITHUB_EMAIL: GITHUB_EMAIL = input('\n>> What is your github email address?\n')

def ssh_key_exists(path_id_rsa):
	path_id_rsa = os.path.join(HOME,'id_rsa') if not path_id_rsa else path_id_rsa
	path_id_rsa_pub = path_id_rsa+'.pub'
	return os.path.exists(path_id_rsa) and os.path.exists(path_id_rsa_pub)

def git_gen_ssh_key(path_id_rsa):
	global GITHUB_USERNAME,GITHUB_EMAIL

	if ssh_key_exists(path_id_rsa) and False:
		print('>> SSH keys already exist')
	else:
		print('>> No SSH keys exist already')

		get_git_user_info()

		if not GITHUB_EMAIL or not GITHUB_USERNAME:
			print('>> Please re-run this installer once you have a github account')
			exit()

		cmd='ssh-keygen -q -N "" -f {path} -t rsa -b 4096 -C "{email}"'.format(path=path_id_rsa, email=GITHUB_EMAIL)
		exec(cmd)

		if not ssh_key_exists(path_id_rsa):
		#if True:
			url='https://help.github.com/en/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent'
			print('>> SSH Keygen creation failed. Please follow these instructions manually:',url)
			time.sleep(2)
			webbrowser.open_new(url)
			exit()

def git_add_ssh_key_to_agent(path_id_rsa):
	# start up agent
	exec('eval "$(ssh-agent -s)"')

	# add opt to ssh config
	ssh_config_path=os.path.join(HOME,'.ssh','config')
	with open(ssh_config_path,'a+') as of:
		of.write('Host *\n\tAddKeysToAgent yes\n\tUseKeychain yes\n\tIdentityFile {path}\n\n'.format(path=path_id_rsa))

	exec('ssh-add -K '+path_id_rsa)

def git_add_ssh_key_to_github(path_id_rsa):
	exec('pbcopy < '+path_id_rsa+'.pub')

	url='https://github.com/settings/ssh/new'

	print('\n#### MANUAL STEP NECESSARY ####')
	print('>> Your SSH Key has been copied to your clipboard.')
	print(' - Please paste it in the "Key" box on this page: '+url)
	print(' - Any Title is fine. The name of your computer is your recommended')
	print(' - Loading the above URL automatically in %s seconds...' % NAP)
	print(' - Once you\'re done, press any key to continue')
	time.sleep(NAP)
	webbrowser.open_new(url)
	x=input()
	print ('>> Continuing...')


def check_git():
	global GITHUB_USERNAME,GITHUB_EMAIL

	print('>> Checking whether git is set up to connect to GitHub using SSH...')
	ssh_ok = check_ssh()
	if ssh_ok: return True

	# Step 1. Make Key
	path_id_rsa = os.path.join(HOME,'id_rsa')
	git_gen_ssh_key(path_id_rsa)

	# Step 2. Add key to key list
	git_add_ssh_key_to_agent(path_id_rsa)

	# Step 3.
	git_add_ssh_key_to_github(path_id_rsa)

	# Test whether ok
	ssh_ok = check_ssh()
	if not ssh_ok:
		url='https://help.github.com/en/articles/connecting-to-github-with-ssh'
		print('\n>> Still cannot connect to Github SSH. Please follow these instructions manually:\n'+url)
		time.sleep(NAP)
		webbrowser.open_new(url)
		exit()









## MAIN

def run_all():
	# What are the steps
	#steps = [check_anaconda, check_packages]
	steps = [check_brew, check_anaconda, check_packages, check_apps, check_git]
	num_steps = len(steps)

	for i,step in enumerate(steps):
		print('\n>> Step #%s of %s' % (i+1, num_steps))
		res=step()
		if res is not True:
			exit()
		else:
			print('>> Success!')

if __name__=='__main__':
	print('>> Welcome to the Literary Lab Starter Pack Installer!')

	run_all()

	print('\nAll set up! Happy hacking...')
