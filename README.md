# Example Use
For starters your should auth yourself with https://api.vps.net

    from vpsnet import cloudserver
    cloudserver.vpsnetAuth('username','authkey')

After it you may do API calls:

    a=cloudserver.Operation()
    a.reboot('cloudserver_id')
    

