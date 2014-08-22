# Example Use
For starters your should auth yourself with https://api.vps.net

    import vps.net
    vpsnet.init('your@email.me','your_auth_key')

After it you may do API calls:

    from vpsnet import cloudserver as cs
    sc.reboot('cloudserver_id')


##Get a list fo CloudServers  

[`cs.get_cloudservers()`](https://control.vps.net/api/#vm_list)

##Edit CloudServer 
    
[`cs.edit(cloudserver_id,data)`](https://control.vps.net/api/#vm_edit)


# TODO
Document each api call and add Nodes, IPs, Backups operation and etc. check https://control.vps.net/api/
