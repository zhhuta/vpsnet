# DevOps approache with vps.net public clouds
## Proof of Concept
### Intro

 "My God, it's full of stars!"
 
Yes, internet is full of articles how to deploy environment with
Amazon EC2, RackSpace, DigitalOcean and etc.  In this article you will
find how to deploy environment with [VPS.NET](https://vps.net
"vps.net").

The most obvious method to create bunch of servers that suppose to
have different roles is WEB-GUI.  You chose number of nodes(decide how
mach cpu, ram and storage will have each server), location where this
server will be built, template(Operation System: generally Linux). What
if you would like to do this with on click(one command), without
WEB-GUI? You should look [here](https://control.vps.net/api/ "VPS.NET
RESTful API")

Another question how, as [here](https://control.vps.net/api/ "VPS.NET
RESTful API") contains description of api calls that should be send to
https://api.vps.net.
For this purpouse article has been written.

## Python and vps.net API

We going to use Python as language for our scripts. We should also
install some frameworks(Python Libs)

	$sudo pip install configobj requests sqlalchemy json

We use:

* `configobj` for operating with config file
* `requests` to communicate with https://api.vps.net
* `sqlalchemy` to store some data into SQLite DB
* `json` to operate with data in json format

Lest start from small example. Hope you already have had account on
vps.net. we going to write small python-scrips to check your profile
on vps.net:

	#!/usr/bin/env python
	import requests
	import json
	import sys, getpass

	def main():
		exmail = raw_input("Enter your email that you use with vps.net:")
		api_key = getpass.getpass("Enter your api key:") ### key you may find on control.vps.net "profile"
		request = requests.get('https://api.vps.net/profile.api10json',\
		                       auth=(email,api_key),\
							   headers={"Accept": "application/json", "Content-type": "application/json"},\
							   verify=False)
		if ( request.status_code == requests.codes.ok):
			print json.dumps(request.json(),sort_keys=True, indent=2)
		else:
			request.raise_for_status()
			
	if __name__ == '__main__':
		main()

The rusult of running this program should be next:

	
	{
	  "user": {
	  	"address": "164 n springcreek parkway",
	    "city": "Providence",
		"company": "",
		"country": "US",
		"created_at": "2010-07-19T05:34:37-04:00",
		"email_address": "john.galt@johngalt.tld",
		"first_name": "John",
		"id": ****,
		"last_name": "Galt",
		"payment_type": "Credit Card",
		"paypal_address": null,
		"per_node_price": 20,
		"phone_code": ***,
		"phone_number": "***********",
		"pin_security_enabled": false,
		"reseller": false,
		"state": "UT",
		"time_zone": "Eastern Time (US & Canada)",
		"updated_at": "2014-06-10T03:20:16-04:00",
		"zip_code": "000000"
		}
	}

I have specially changed my own information to John Galt :)

If credentials are not valid and server won't replie with HTTP 200 we get exception

	requests.exceptions.HTTPError: 404 Client Error: Not Found

Hope we entered correct credentials

Let's figure out what do this program step by spep

1. First we expect that you enter you email and api_key

	`raw_input()` & `getpass.getpass()`
	
2. Next we build HTTP GET request to api.vps.net

    `r = requests.get(url,auth,headers,varify)`

Where:

 * `url='https://api.vps.net/profile.api10json'`
 * `auth = (email,api_key)`
 * `headers= {"Accept": "application/json", "Content-type": "application/json"}`
 * `varify=False`

After we get replie form `api.vps.net` we check if `r.status_code`
equal to `requests.codes.ok`, if not we riese exception

As soon as we go forward we going to modify our script and add more
functions to it. Now lets store our credentials in config file for
future use.
## Storing Credentials
First we should add global variale `cred_file = 'credentilas.cfg'` and
write new function `store_credentials`

	def store_credentials(email,api_key):
	        config_cred = ConfigObj()
			config_cred.filename = cred_file
			config_cred['CREDENTAILS'] = {}
			config_cred['CREDENTAILS']['url'] = 'https://api.vps.net'
			config_cred['CREDENTAILS']['email'] =  email
			config_cred['CREDENTAILS']['api_auth'] = api_key
			config_cred.write()
			print "[+] Config file %s created." % cred_file
			return config_cred


Also add this function into our main function

	cred = store_credentials(email,api_key)

in our IF statetment, we want store credentials only if they are valid.

Now we should switch to more complicated task: build infrastructure on
one of vps.net public cloud. For stater, we should decide how our
infra should look.
## Infrastructure
Lets imagine that we have to deploy some application that's need Web
server, DB server also we need some SVN sever and monitoring.  In real
world we need servers for Continues Integration(Jenkins), test
environment and etc.

So we going to build:

* web server: Tomcat 2 Nodes
* db server: MySQL 2 Nodes
* svn server: git 1 Node
* CI server: jenkins 2 Node

In total it is 4 servers with different configuration. As a best
pracitse we should use the same OS for all this servers, let's say:
Centos 6.4 x64

## Storing infra config

Now we going to write function add will create `infra.cfg` file and base on thie file we will build Virtual Servers.


Add global variable `infr_file = 'infra.cfg'` and write next function `create_infr`

	def create_infr():
		""" Funciton that create infra.cfg file """
		config_infr =ConfigObj()
		config_infr.filename = infr_file
		print "\t[+]Please Enter name of server groups. CTRL+D end list."
		a= []
		while True:
		try:
			a.append(raw_input("[-] Name of server groups:"))
		except EOFError:
			print
			break
			print
		print "[+]Eenter params for each server"
		for i in a:
			config_infr[i] = {}
			print "[-] for %s" % i
			config_infr[i]['label'] = raw_input("\t[-] Label:")
			config_infr[i]['fqdn'] = raw_input("\t[-] fqdn:")
			config_infr[i]['nodes'] = raw_input("\t[-] Nodes:")
			config_infr[i]['quantity'] = raw_input("\t[-] quantity of such server :")
		config_infr.write()
		print "[+] Config file %s written" % infr_file
		return config_infr


Call this function at the end of main function:
	cred = create_infr()

If we ran the script we get two files `credentials.cfg` and `infra.cfg`. Config for infra would looks next:

	...
	[app]
	label = web
	fqdn = zhhuta.tld
	nodes = 2
	quantity = 2
	...

Explanation:

We have group called `[app]` where will be 2 servers with labels `web01`
and `web02`, each server will be build with 2 Nodes and have hostname
`web01.zhhuta.tld` and `web02.zhhuta.tld`

It's not enough to build our ifra, we have to decide on witch cloud we goig to build and chose base tamplate.
## Geting Clouds from api.vps.net
Next step we going to retrieve the list of vps.net clouds and check on what cloud we can build infra.

	def get_clouds(config_cred):
		""" Fucntion get full list of clouds and retunr dict of cloud namd and id """
		print "[+] checking available clouds ..."
		request = requests.get(config_cred['CREDENTAILS']['url'] + "/available_clous.api10json",\
			auth=(config_cred['CREDENTAILS']['email'],config_cred['CREDENTAILS']['api_auth']),\
			headers=headers_post,\
			verify=False)
		clouds = {}
		r = request.json()
		for i in r:
			if i['cloud']['available'] == 'true':
				print i['cloud']['label']
				clouds.update({i['cloud']['id']: i['cloud']['label']})
		print "[+ Done]"
		return clouds

and add `get_cloud` into `main`

	clouds = get_couds(cred)

## Getting templates
Now we need tamlates ids on vps.net cloud.

	def get_templates(config_cred,clouds):
		""" Function that get a list of all existing templates on each cloud
		retunr cloud id and templated id that take from keybaord
		Future todo: .... """
		print "[+] checking available templates ..."
		request = requests.get(config_cred['CREDENTAILS']['url'] + '/available_templates.api10json',\
			auth=(config_cred['CREDENTAILS']['email'],config_cred['CREDENTAILS']['api_auth']),\
			headers=headers_post,\
			verify=False)
		r = request.json()
		rexp = raw_input("Enter a Name of OS:")
		c_rexp = re.compile(rexp, re.IGNORECASE)
		for i in r["template_groups"]:
			for j in i["templates"]:
				for k in j["clouds"]:
					if re.match(c_rexp,j["name"]) and clouds.get(int(k['id'])):
						print j["name"],clouds.get(int(k['id'])),"Cloud id:",k['id'],"Templat id:",k['system_template_id']
		cloud = raw_input("Enter Cloud id:")
		template = raw_input("Enter Template id:")
		print "[+] Done"
		return cloud, template


This function will parse dict of templates and print cloud and template id on that cloud. This params we will user for building VMs on specified clouds. Lets attache this prarams to our `infra.cfg`

	def modify_infra_cfg(config_infr,cloud,template):
		"""Function that first modifi config_infr and add cloud id and template id to each server groups"""
		print "[+]Modifing infra.cfg...."
		for i in config_infr:
			config_infr[i]['cloud'] = cloud
			config_infr[i]['template'] = template
		config_infr.write()
		return config_infr

`infra.cfg` should looks next:
	...
	[app]
	label = web
	fqdn = zhhuta.tld
	nodes = 2
	quantity = 2
	cloud = 55
	template = 4302
	...

We are almost ready to build infra we have all variable to do it, but we need to store IP address of newly created VMs and their passwords. For this we going to create sqlite db.

## Sqlite Inint

	def init_db():
		"""Creating DB """
		db = create_engine('sqlite:///'+db_file)
		metadata = MetaData(db)
		vms = Table('vms', metadata,
				Column('id',Integer, primary_key=True),
				Column('vm_id',Integer),
				Column('label',String(40)),
				Column('ip_address',String(40)),
				Column('password',String(40)),
			)
		vms.create()
		return vms

add to main

	vms_db = init_db()

##Time to build VMs

	def buil_vm(config_cred,label,fqdn,template,cloud,nodes,vms_db):
		""" Build VM """
		post_json = {
				"virtual_machine":
				{
					"label": label,
					"fqdn": fqdn,
					"system_template_id": template,
					"cloud_id":cloud,
					"backups_enabled": 'false',
					"rsync_backups_enabled": 'false',
					"slices_required": nodes
				}
			}
		print "[+]Sending request to", config_cred['CREDENTAILS']['url']
		request = requests.post(config_cred['CREDENTAILS']['url']+'/virtual_machines.api10json',\
				auth=(config_cred['CREDENTAILS']['email'],config_cred['CREDENTAILS']['api_auth']),\
				data=json.dumps(post_json),\
				headers=headers_post,\
				verify=False)
		print "[+] Request status code",request.status_code
		vm = request.json()
		print "[+] Add Vm to db..."
		ins = vms_db.insert()
		ins.execute(vm_id = vm['virtual_machine']['id'],
				label = vm['virtual_machine']['label'],
				ip_address = vm['virtual_machine']['primary_ip_address']['ip_address']['ip_address'],
				assword = vm['virtual_machine']['password'])
		print "[+] VM", vm['virtual_machine']['label'], "hass been add into DB"
		return vm['virtual_machine']['label'], vm['virtual_machine']['primary_ip_address']['ip_address']['ip_address']


##Now infra time

	def build_infra(config_cred,config_infr,vms_db):
		"""Parse configs and build vms """
		infra = []
		hosts = open("hosts",'a')
		servers = open("servers.txt",'a')
		for i in config_infr:
			infra.append(i)
		infra.append('all')
		print "[+]Chose what to build",infra, ".. to build everythin type all"
		answ = raw_input("?")
		if answ == 'all':
			for i in config_infr:
				hosts.writelines("#"+i + "\n")
				servers.writelines(i + "\n")
				for j in range(int(config_infr[i]['quantity'])):
					h, ip = build_vm(config_cred,config_infr[i]['label']+str(j),\
						config_infr[i]['label']+str(j)+"."+config_infr[i]['fqdn' ],\
						config_infr[i]['template'],\
						config_infr[i]['cloud'],\
						config_infr[i]['nodes'],
						vms_db)
					hosts.writelines(ip + '\t' + h +'\n')
					servers.writelines(h+'\n')
		else:
			hosts.writelines("#"+answ + "\n")
			servers.writelines(answ + "\n")
			for j in range(int(config_infr[answ]['quantity'])):
				h, ip = build_vm(config_cred,config_infr[answ]['label']+str(j),\
					config_infr[answ]['label']+str(j)+"."+config_infr[answ]['fqdn' ],\
					config_infr[answ]['template'],\
					config_infr[answ]['cloud'],\
					config_infr[answ]['nodes'],
					vms_db)
				hosts.writelines(ip + '\t' + h +'\n')
				servers.writelines(h+'\n')
			hosts.close()
			servers.close()
		print "[+] Infra has been built"

add to main

	build_infra(cred,infr,vms_db)

After all our main function should looks next

## Main

	def main():
		email = raw_input("Enter your email that you use with vps.net:")
		api_key = getpass.getpass("Enter your api key:") ### key you may find on control.vps.net "profile"
		r = requests.get('https://api.vps.net/profile.api10json',\
				auth=(email,api_key),\
				headers={"Accept": "application/json", "Content-type": "application/json"},\
				verify=False)
		if (r.status_code == requests.codes.ok):
			print json.dumps(r.json(),sort_keys=True, indent=2)
			cred = store_credentials(email,api_key)
		else:
	 		print r.raise_for_status()
		infr = create_infr()
		vps_clouds = get_couds(cred)
		cloud, templ = get_templates(cred,vps_clouds)
		infr = modify_infra_cfg(infr, cloud,templ)
		vms_db = init_db()
		build_infra(cred,infr,vms_db)

Script will create next files:

 * `credentilas.cfg` contain credentails to api.vps.net
 * `infra.cfg` contain informaont aobut infrastructure
 * `infra.db` containe dst id, ip address, password of vms
 * `hosts` containe IP_ADDRESS HOSTNAME record of out infra servers
 * `servers.txt` containe sorted infromatin about servers and groups, servers belongs.

As last step we should distribute our ssh public keys over servers. We going to automate this task too.




+++++++++++++++++++++


