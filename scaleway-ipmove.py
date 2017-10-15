#!/usr/bin/python

import requests
import subprocess
import json
import sys

# get a server id based on its name
def get_server_id(servername, token, url):
  servers=requests.get(url, headers=token)
  print servers.status_code, servers.reason
  for server in json.loads(servers.content)['servers']:
    server_name=server['name']
    if server_name == servername:
      server_id=server['id']
      print servername+"="+server_id
      return server_id

# get an ip id
def get_ip_id(ip, token,url):
  ips=requests.get(url, headers=token)
  print ips.status_code, ips.reason
  for ip_addr in json.loads(ips.content)['ips']:
    ip_address=ip_addr['address']
    if ip_address == ip:
      ip_id=ip_addr['id']
      server_id=ip_addr['server']['id']
      print ip+"="+ip_id+" is attached to server "+server_id
      return ip_id, server_id

# this assume you have only have one organization
def get_organization_id(token,url):
  orgas=requests.get(url, headers=token)
  print orgas.status_code, orgas.reason
  print json.loads(orgas.content)['organizations'][0]['id']
  return json.loads(orgas.content)['organizations'][0]['id']

# this swap the ip addr
def swap_ip(attached_server, server_id1, server_id2, ip_id, ip, reverse, orga_id, url):
  body = {
    "address": ip,
    "id": ip_id,
    "organization": orga_id,
    "server": "",
    "reverse": reverse
  }
  if attached_server == server_id1:
    print "IP is attached to "+server_id1+" swapping to "+server_id2
    body['server']=server_id2
  elif attached_server == server_id2:
    print "IP is attached to "+server_id2+" swapping to "+server_id1
    body['server']=server_id1

  print body

  scw_meta = subprocess.check_output(['/usr/local/bin/scw-metadata-json'])

  json_scw_meta=json.loads(scw_meta)

  print json_scw_meta

  current_server=json_scw_meta['name']
  print current_server

  server_id=get_server_id(current_server, token, 'https://cp-par1.scaleway.com/servers')

  print server_id
  body['server']=server_id

  token['Content-Type']='application/json'
  swap=requests.put(url, data=json.dumps(body), headers=token)
  print swap.status_code, swap.reason
  print swap.text


if __name__ == '__main__':
  token_arg=sys.argv[1]
  server1_arg=sys.argv[2]
  server2_arg=sys.argv[3]
  ip_arg=sys.argv[4]
  reverse_arg=sys.argv[5]
  orga_arg=sys.argv[6]

  print token_arg, server1_arg, server2_arg, ip_arg, reverse_arg

  token={'X-Auth-Token': token_arg}

  #orga=get_organization_id(token, 'https://account.scaleway.com/organizations' )
  orga=orga_arg
  server_id1=get_server_id(server1_arg, token, 'https://cp-par1.scaleway.com/servers')
  server_id2=get_server_id(server2_arg, token, 'https://cp-par1.scaleway.com/servers')
  ip_id, attached_server=get_ip_id(ip_arg, token, 'https://cp-par1.scaleway.com/ips')
  swap_ip(attached_server, server_id1, server_id2, ip_id, ip_arg, reverse_arg, orga, "https://cp-par1.scaleway.com/ips/"+ip_id)
