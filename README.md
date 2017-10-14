scaleway_ipmove
===============

This quick code is used to swap a scaleway ip between two servers.
I'm using it mixed with _keepalived_ and _kubernetes_ to have an HA ingress-controller
Change the keepalive _notify_ script and add a call to this python script in it

usage
=====

```
scaleway-ipmove.py token servername1 servername2 ipaddr reverse_ipaddr
```
