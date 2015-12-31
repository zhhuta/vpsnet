# DevOps approach with vps.net public clouds
## Proof of Concept
### Intro

 "The possibilities are endless"
 
As we all know there are many different IaaS providers out there, and there are many different ways to deploy your infrastructure with them. In this article we will explain one way to deploy your infrastructure with [VPS.NET](https://vps.net
"vps.net").

Let's say your ready to deploy your environment, you need multiple servers with different Operating Systems in different geographic locations. The most obvious method to accomplish this task is simply logging into the VPS.NET control panel and deploying your servers. But what if you are like me and want to accomplish this with a single click? Perhaps you want to integrate this rollout in your own scripts? Good news, you can!  Check out the VPS.NET API[here](https://control.vps.net/api/ "VPS.NET
RESTful API")

Okay, now you know where to look, it's time to talk about how.  For a description of the available API calls check this out [here](https://control.vps.net/api/ "VPS.NET
RESTful API"). 

To help clarify things a little more - our amazing DevOps team has created there own script to help point you in the right direction.

## Python and vps.net API

We are going to use Python as language for our scripts. First thing we need to do is install the required frameworks (Python Libs)

	$sudo pip install configobj requests sqlalchemy json

We use:

* `configobj` for operating with config file
* `requests` to communicate with https://api.vps.net
* `sqlalchemy` to store some data into SQLite DB
* `json` to operate with data in json format

Lest start with a small example. Please be aware, we are assuming you already have had account on
vps.net. 

Let's write a small python script to check out your profile.

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


Below is the results you should get when running this script:
	
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


If credentials are invalid we'll get the following exception.

	requests.exceptions.HTTPError: 404 Client Error: Not Found

If you see this - check your credentials! :) 


Okay - let's go through this script, step by step:

1. First you will enter you email and api_key

	`raw_input()` & `getpass.getpass()`
	
2. Next we build the HTTP GET request to api.vps.net

    `r = requests.get(url,auth,headers,varify)`

Where:

 * `url='https://api.vps.net/profile.api10json'`
 * `auth = (email,api_key)`
 * `headers= {"Accept": "application/json", "Content-type": "application/json"}`
 * `varify=False`

After we get a reply from `api.vps.net` we check if `r.status_code` is equal to `requests.codes.ok`, if not we raise an exception

Going forward we are going to add more functionality to our script.  To make our life easy let's store our credentials in a config file for future use. 

First we should add global variable `cred_file = 'credentilas.cfg'` and write a new function `store_credentials`

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


Also add this into our main function

	cred = store_credentials(email,api_key)

In our IF statement, we'll want store credentials only if they are valid.

Now, let's get into a bit more complicated of a task. Let's look at how to build some infrastructure servers on
one of vps.net public clouds. First things first, let's decide what our infrastructure should look like. 

Okay, let's say we need to deploy an application, this application needs a web server, a database server, an SVN server and a monitoring server.  
Lets imagine that we have to deploy some application that's need Web
server, DB server also we need some SVN sever and a to make things nice and tidy we want a continuous integration server (Jenkins).

So to accomplish this we are going to build:

* 2 x Web Server: Tomcat 2 Nodes
* 1 x DB Server: MySQL 2 Nodes
* 1 x SVN Server: git 1 Node
* 1 x CI Server: jenkins 2 Node

So we're going to create 4 servers, all with different configurations.  But to keep things a little organized we're going to use the same OS - in this example we'll use CentOS 6.4 x64.

Okay, first step is writing function to create a `infra.cfg` file this file will describe the infrastructure we want to build. 


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

If we ran the script we get two files `credentials.cfg` and `infra.cfg`. The infra.cfg file would look something like:

	...
	[app]
	label = web
	fqdn = zhhuta.tld
	nodes = 2
	quantity = 2
	...

Okay - let's explain the above config file 'snippet':

We have group called `[app]` with 2 servers `[quantity = 2]` with labels `web01` and `web02`, each of these servers will be build with 2 Nodes `[nodes=2]` and have hostname
`web01.zhhuta.tld` and `web02.zhhuta.tld` `fqdn = zhhuta.tld`.

Okay - we have a decription of what we're going to build, now let's work out the 'where' and 'how' we are going to accomplish these builds.

Next step we going to retrieve the list of vps.net clouds and check which clouds we can build our infrastructure on.

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

Okay - now we need to get all the available templates on each of those clouds.

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


This function will parse a description of each template and print out the cloud and template ids. We will then use that info for building our VMs. Lets add this info to our `infra.cfg` file:

	def modify_infra_cfg(config_infr,cloud,template):
		"""Function that first modifi config_infr and add cloud id and template id to each server groups"""
		print "[+]Modifing infra.cfg...."
		for i in config_infr:
			config_infr[i]['cloud'] = cloud
			config_infr[i]['template'] = template
		config_infr.write()
		return config_infr

`infra.cfg` should now look like:
	...
	[app]
	label = web
	fqdn = zhhuta.tld
	nodes = 2
	quantity = 2
	cloud = 55
	template = 4302
	...

Okay - we're almost ready! We have all our variables but we need to think about storing details of each VM after it's creation. To help accomplish this we going to create an sqlite db.


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

Okay - it's time to build our VMs!

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


Infrastructue creation time!

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

After all of this our main function should looks like:

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

So our script will create the following files:

 * `credentilas.cfg` This contains credentails to api.vps.net
 * `infra.cfg` This contains information about our infrastructure
 * `infra.db` This contains the dst id, ip address, password of vms
 * `hosts` This contains the IP_ADDRESS HOSTNAME record of our infra servers
 * `servers.txt` This contains sorted information about our servers.


One last step - you probably want to distribute your public SSH keys across your infrastructure.


Now check new version of vps.net.py where we use vpsnet python module.

+++++++++++++++++++++


