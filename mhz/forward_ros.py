from message import Message
from transceiver import Transceiver
import roslibpy
import time
import calendar


def multijoyCallback(message):
    if(time.time() - (message['header']['stamp']['secs'] + message['header']['stamp']['nsecs']/1000000000) < 0.01):
        x_axis = int(message['joys'][0]['axes'][2] * 80)
        y_axis = int(message['joys'][0]['axes'][3] * 80)

        print([x_axis, y_axis])

        multijoy_message = Message(op_code=0, data=[x_axis, y_axis])
        transceiver.write(multijoy_message)
    else:
        pass


# Initialize 433
transceiver = Transceiver('/dev/ttyUSB0', 19200)

# Initialize Ros-bridge
client = roslibpy.Ros(host='192.168.1.100', port=9090)
client.run()

print('Is ROS connected?', client.is_connected)

# https://roslibpy.readthedocs.io/en/latest/reference/#main-ros-concepts
# http://digital.csic.es/bitstream/10261/133333/1/ROS-systems.pdf
# http://wiki.ros.org/master_discovery_fkie#Services
service = roslibpy.Service(
    client, '/master_discovery/list_masters', 'multimaster_msgs_fkie/DiscoverMasters')
request = roslibpy.ServiceRequest()

print('Calling service...')
while(True):
    result = service.call(request)
    print('Service response: {}'.format(len(result['masters'])))


# Start listening for multijoy
listener = roslibpy.Topic(client, '/multijoy', 'multijoy/Multi')
listener.subscribe(multijoyCallback)

# Terminate on ctrl-z
try:
    while True:
        pass
except KeyboardInterrupt:
    client.terminate()
