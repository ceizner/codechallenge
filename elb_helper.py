# Import the SDK
import boto3
import uuid
import sys
import getopt

elbclient = boto3.client('elb')
InstanceID=[ {'InstanceId': 'i-89ffec3b' } ]

def usage ():
   print "elb_helper.py -l <LB name> -i <instance> <-d[eregister]|-r[egister]|-s[status]>"
	

try:
    opts, args = getopt.getopt(sys.argv[1:], 'l:i:c', ['loadbalancer=', 'instance=', 'help', 'r|d|s'])
except getopt.GetoptError:
    usage()
    sys.exit(2)
print type(opts)
for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit(2)
    elif opt in ('-l', '--loadbalancer'):
        LB = arg
    elif opt in ('-i', '--instance'):
        InstanceID=[ {'InstanceId': arg } ] 
    else:
        usage()
        sys.exit(2)

#Let's print our instances 
def printinstances( str ):
  list_elb_resp = elbclient.describe_load_balancers(LoadBalancerNames=[str])
  print 'Load Balancer {0} has the following instances'.format(LB)
  for instance in (list_elb_resp['LoadBalancerDescriptions'][0]['Instances' ]):
       print '{0}'.format(instance['InstanceId'])
  return;

printinstances(LB)

response = elbclient.deregister_instances_from_load_balancer(
    LoadBalancerName=LB,
    Instances= InstanceID
)

response = elbclient.register_instances_with_load_balancer(
    LoadBalancerName=LB,
    Instances= InstanceID
)

printinstances(LB)

#try:
#    input = raw_input
#except NameError:
#    pass
#input("\nPress enter to continue...")

