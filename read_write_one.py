# init OSC send
from pythonosc.udp_client import SimpleUDPClient
ip = "127.0.0.1"
port = 9000
client = SimpleUDPClient(ip, port)
# init arguments parser
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('-p','--pos', default='200')
parser.add_argument('-v','--vit', default='100')
parser.add_argument('-a','--acc', default='2')
parser.add_argument('-t','--tre', default='10')
parser.add_argument('-i','--ind', default='1')
args = parser.parse_args()
pos = args.pos
vit = args.vit
acc = args.acc
tre = args.tre
ind = args.ind
pos = int(pos)
vit = int(vit)
acc = int(acc)
tre = int(tre)
ind = int(ind)

from dynamixel_sdk import *                    # Uses Dynamixel SDK library

# Control table address; do not change without knowing!
ADDR_PRO_TORQUE_ENABLE      = 64               # Control table address is different in Dynamixel model
ADDR_PRO_GOAL_POSITION      = 116
ADDR_PRO_PRESENT_POSITION   = 132
ADDR_PRO_GOAL_VELOCITY      = 104
ADDR_PRO_OPERATING_MODE     = 11
ADDR_PRO_POS_TRAJ           = 112
ADDR_PRO_VEL_TRAJ           = 108
ADDR_RETURN_DELAY_TIME      = 9

# Protocol version
PROTOCOL_VERSION            = 2.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID                      = ind                # Dynamixel ID : 1
BAUDRATE                    = 1000000             # Dynamixel default baudrate : 57600
DEVICENAME                  = 'COM6'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"
RETURN_DELAY_TIME           = 10        # answering delay (between 0 and 256)
OPERATING_MODE              = 4         # 4 is for extended position (-100000 to 100000)
TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0 
POS_TRAJ                    = vit       # velocity
VEL_TRAJ                    = acc       # acceleration  
# Value for disabling the torque

DXL_MAXIMUM_POSITION_VALUE  = pos           # goal position
DXL_MOVING_STATUS_THRESHOLD = tre              # Dynamixel moving status threshold

dxl_goal_velocity = 100
dxl_goal_position = DXL_MAXIMUM_POSITION_VALUE        # Goal position
# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
portHandler.openPort()
  
portHandler.setBaudRate(BAUDRATE)
   
# Enable Dynamixel Torque and set the movement
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_OPERATING_MODE, OPERATING_MODE)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_RETURN_DELAY_TIME, RETURN_DELAY_TIME)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_PRO_POS_TRAJ, POS_TRAJ)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_PRO_VEL_TRAJ, VEL_TRAJ)  
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_PRO_GOAL_VELOCITY, dxl_goal_velocity)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_PRO_GOAL_POSITION, dxl_goal_position)

# send OSC movement on
mov = 1
client.send_message("/mov",mov) 

while 1:
    # Read present position
    dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_PRO_PRESENT_POSITION)
    # Send to OSC
    client.send_message("/position",dxl_present_position)
    # Print in Terminal
    print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID, dxl_goal_position, dxl_present_position))
    # Stop the processus reaching goal position
    if not abs(dxl_goal_position - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD:
            break

# Disable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
mov = 0
# Send OSC end
client.send_message("/mov",mov)

# Close port
portHandler.closePort()