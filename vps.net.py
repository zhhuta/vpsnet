#!/usr/bin/env python
# Written by Vitaliy Zhhuta
# 24 June 2014
import json
import getpass
import re

from configobj import ConfigObj
from sqlalchemy import *
import vpsnet
from vpsnet import cloudserver
from vpsnet import clouds
from vpsnet import profile
from vpsnet import templates


cred_file = 'credentilas.cfg'
infr_file = 'infra.cfg'
db_file = 'infra.db'


def store_credentials(email, api_key):
    """Function that create credentials.cfg file """
    config_cred = ConfigObj()
    config_cred.filename = cred_file
    config_cred['CREDENTAILS'] = {}
    config_cred['CREDENTAILS']['url'] = 'https://api.vps.net'
    config_cred['CREDENTAILS']['email'] = email
    config_cred['CREDENTAILS']['api_auth'] = api_key
    config_cred.write()
    print "[+] Config file %s created." % cred_file
    return config_cred


def create_infr():
    """ Funciton that create infra.cfg file """
    config_infr = ConfigObj()
    config_infr.filename = infr_file
    print "\t[+]Please Enter name of server groups. CTRL+D end list."
    a = []
    while True:
        try:
            a.append(raw_input("[-] Name of server groups:"))
        except EOFError:
            print
            break
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


def get_clouds():
    """ Fucntion get full list of clouds and retunr dict of cloud namd and id """
    print "[+] checking available clouds ..."
    r = clouds.get_list()
    cloud = {}
    for i in r:
        if i['cloud']['available'] is True:
            print i['cloud']['label'], "\t", i['cloud']['id'], "\t", i['cloud']['available']
            cloud.update({i['cloud']['id']: i['cloud']['label']})
        else:
            print i['cloud']['label'], "\t Disabled"
    return cloud


def get_templates(cloud):
    """ Function that get a list of all existing
    templates on each cloud retunr cloud id and
    templated id that take from keybaord Future todo: .... """
    print "[+] checking available templates ..."
    r = templates.get_list()
    rexp = raw_input("Enter a Name of OS:")
    c_rexp = re.compile(rexp, re.IGNORECASE)
    for i in r["template_groups"]:
        for j in i["templates"]:
            for k in j["clouds"]:
                if re.match(c_rexp, j["name"]) and cloud.get(int(k['id'])):
                    print j["name"], cloud.get(int(k['id'])), "Cloud id:", k['id'], "Templat id:", k[
                        'system_template_id']
    cloud = raw_input("Enter Cloud id:")
    template = raw_input("Enter Template id:")
    print "[+] Done"
    return cloud, template


def modify_infra_cfg(config_infr, cloud, template):
    """Function that first modifi config_infr and add cloud id and template id to each server groups"""
    print "[+]Modifing infra.cfg...."
    for i in config_infr:
        config_infr[i]['cloud'] = cloud
        config_infr[i]['template'] = template
    config_infr.write()
    return config_infr


def init_db():
    """Creating DB """
    db = create_engine('sqlite:///' + db_file)
    metadata = MetaData(db)
    vms = Table('vms', metadata,
                Column('id', Integer, primary_key=True),
                Column('vm_id', Integer),
                Column('label', String(40)),
                Column('ip_address', String(40)),
                Column('password', String(40)),
                )
    vms.create()
    return vms


def build_vm(config_cred, label, fqdn, template, cloud, nodes, vms_db):
    """ Build VM """
    vm_params = {"virtual_machine": {
        "label": label,
        "fqdn": fqdn,
        "system_template_id": template,
        "cloud_id": cloud,
        "backups_enabled": 'false',
        "rsync_backups_enabled": 'false',
        "slices_required": nodes
    }
    }
    print "[+]Sending request to", config_cred['CREDENTAILS']['url']
    vm = cloudserver.create(vm_params)
    print "[+] Add Vm to db..."
    ins = vms_db.insert()
    ins.execute(vm_id=vm['virtual_machine']['id'],
                label=vm['virtual_machine']['label'],
                ip_address=vm['virtual_machine']['primary_ip_address']['ip_address']['ip_address'],
                password=vm['virtual_machine']['password'])
    print "[+] VM", vm['virtual_machine']['label'] + "." + fqdn, \
        vm['virtual_machine']['primary_ip_address']['ip_address']['ip_address'], "hass been add into DB"
    return vm['virtual_machine']['label'], vm['virtual_machine']['primary_ip_address']['ip_address']['ip_address']


def build_infra(config_cred, config_infr, vms_db):
    """Parse configs and build vms """
    infra = []
    hosts = open("hosts", 'a')
    servers = open("servers.txt", 'a')
    for i in config_infr:
        infra.append(i)
    infra.append('all')
    print "[+]Chose what to build", infra, ".. to build everythin type all"
    answ = raw_input("?")
    if answ == 'all':
        for i in config_infr:
            hosts.writelines("#" + i + "\n")
            servers.writelines(i + "\n")
            for j in range(int(config_infr[i]['quantity'])):
                h, ip = build_vm(config_cred, config_infr[i]['label'] + str(j),
                                 config_infr[i]['label'] + str(j) + "." + config_infr[i]['fqdn'],
                                 config_infr[i]['template'],
                                 config_infr[i]['cloud'],
                                 config_infr[i]['nodes'],
                                 vms_db)
                hosts.writelines(ip + '\t' + h + '\n')
                servers.writelines(h + '\n')
    else:
        hosts.writelines("#" + answ + "\n")
        servers.writelines(answ + "\n")
        for j in range(int(config_infr[answ]['quantity'])):
            h, ip = build_vm(config_cred, config_infr[answ]['label'] + str(j),
                             config_infr[answ]['label'] + str(j) + "." + config_infr[answ]['fqdn'],
                             config_infr[answ]['template'],
                             config_infr[answ]['cloud'],
                             config_infr[answ]['nodes'],
                             vms_db)
            hosts.writelines(ip + '\t' + h + '\n')
            servers.writelines(h + '\n')
    hosts.close()
    servers.close()
    print "[+] Infra has been built"


def main():
    email = raw_input("Enter your email that you use with vps.net:")
    api_key = getpass.getpass("Enter your api key:")  # ## key you may find on control.vps.net "profile"
    vpsnet.init(email, api_key)
    cred = store_credentials(email, api_key)
    prof = profile.get()
    print json.dumps(prof, sort_keys=True, indent=2)
    infr = create_infr()
    vps_clouds = get_clouds()
    # noinspection PyArgumentList
    cloud, templ = get_templates( vps_clouds)
    infr = modify_infra_cfg(infr, cloud, templ)
    vms_db = init_db()
    build_infra(cred, infr, vms_db)


if __name__ == '__main__':
    main()
