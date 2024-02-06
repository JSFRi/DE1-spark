# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time, os, sys,  random
import inspect
from os import environ as env

from  novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session

flavor = "ssc.xlarge.highcpu" 
private_net = "UPPMAX 2024/1-1 Internal IPv4 Network"
floating_ip_pool_name = None
floating_ip = None
image_name = "31dbaaf8-2200-44bc-b4f2-44ab4be099ca"

identifier = random.randint(1000,9999)

loader = loading.get_plugin_loader('password')

auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                project_domain_id=env['OS_PROJECT_DOMAIN_ID'],
                                #project_id=env['OS_PROJECT_ID'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
print ("user authorization completed.")

image = nova.glance.find_image(image_name)

flavor = nova.flavors.find(name=flavor)

if private_net != None:
    net = nova.neutron.find_network(private_net)
    nics = [{'net-id': net.id, 'v4-fixed-ip': '192.168.2.251'}]
else:
    sys.exit("private-net not defined.")

#print("Path at terminal when executing this file")
#print(os.getcwd() + "\n")
cfg_file_path =  os.getcwd()+'/cloud-cfg.txt'
if os.path.isfile(cfg_file_path):
    userdata = open(cfg_file_path)
else:
    sys.exit("cloud-cfg.txt is not in current working directory")

secgroups = ['default','Spark']

print ("Creating instance ... ")
instance = nova.servers.create(name="Spark_worker1", image=image, flavor=flavor, key_name='TZLDSA', userdata=userdata, nics=nics, security_groups=secgroups)

# incase you want to login to the production server 
#instance = nova.servers.create(name="prod_server_without_docker", image=image, flavor=flavor, key_name='access-key-name',userdata=userdata, nics=nics,security_groups=secgroups)
inst_status = instance.status
print ("waiting for 10 seconds.. ")
time.sleep(10)

while inst_status == 'BUILD':
    print ("Instance: "+instance.name+" is in "+inst_status+" state, sleeping for 5 seconds more...")
    time.sleep(5)
    instance = nova.servers.get(instance.id)
    inst_status = instance.status

print ("Instance: "+ instance.name +" is in " + inst_status + "state")
