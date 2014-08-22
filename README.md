# Example Use
For starters your should auth yourself with https://api.vps.net

    import vps.net
    vpsnet.init('your@email.me','your_auth_key')

After it you may do API calls:

    from vpsnet import cloudserver as cs
    sc.reboot('cloudserver_id')


Get a list fo CloudServers [get_list](https://control.vps.net/api/#vm_list)  

`cs.get_cloudservers`

Edit CloudServer [edit](https://control.vps.net/api/#vm_edit)
    
`cs.edit(cloudserver_id,data)`


# TODO
Document each api call and add Nodes, IPs, Backups operation and etc. check https://control.vps.net/api/
