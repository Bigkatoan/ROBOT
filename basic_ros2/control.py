import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import numpy
import cv2

class control(Node):
    def __init__(self):
        super().__init__('control')
        self.publisher_ = self.create_publisher(
            Float32MultiArray, '/robot_control', 10)

        self.action = numpy.zeros(7)
        while True:
            canvas = numpy.zeros((256, 256))
            cv2.imshow('control_pad', canvas)
            key = cv2.waitKey(1)
            if key == ord('t'):
                self.action[0] = min(self.action[0] + 0.1, 1)
            if key == ord('y'):
                self.action[0] = max(self.action[0] - 0.1, -1)
            msg = Float32MultiArray()
            msg.data = self.action.tolist()
            self.publisher_.publish(msg)

def main(arg=None):
    rclpy.init()
    node = control()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
