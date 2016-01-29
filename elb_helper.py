#!/usr/bin/env python 
# Import the SDK
import boto3
import uuid
import sys
import getopt

elbclient = boto3.client('elb')

def usage ():
   print "elb_helper.py -l <LB name> -i <instance> <-d[eregister]|-r[egister]|-s[status]>"
	
if(len(sys.argv) < 6):
   usage()
   sys.exit(2)

#Let's print the status of our instances 
def printinstances( loadblancer, instance ):
  try:
     list_elb_resp = elbclient.describe_load_balancers(LoadBalancerNames=[loadblancer])
     for list_instance in (list_elb_resp['LoadBalancerDescriptions'][0]['Instances' ]):
               if (instance[0]['InstanceId']==list_instance['InstanceId']):
                 print ('Instance {1} registered with load balancer {0}'.format(loadblancer,list_instance['InstanceId']))
                 return;
     print ('Instance {1} IS NOT registered with load balancer {0}'.format(loadblancer,list_instance['InstanceId']))
     return;
  except Exception as e: 
      print e
      

try:
    opts, args = getopt.getopt(sys.argv[1:], 'l:i:rds', ['loadbalancer=', 'instance=', 'help', 'r|d|s'])
except getopt.GetoptError:
    usage()
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit(2)
    elif opt in ('-l', '--loadbalancer'):
        LB = arg
    elif opt in ('-i', '--instance'):
        InstanceID=[ {'InstanceId': arg } ] 
    elif opt in ('-r', '--redister'):
	response = elbclient.register_instances_with_load_balancer(
        LoadBalancerName=LB,
    	Instances= InstanceID
	)
    elif opt in ('-d', '--deregister'):
	 response = elbclient.deregister_instances_from_load_balancer(
         LoadBalancerName=LB,
         Instances= InstanceID
         )
    elif opt in ('-s', '--status'):
         printinstances(LB,InstanceID)
    else:
        usage()
        sys.exit(2)

