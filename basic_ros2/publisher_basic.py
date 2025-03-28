import rclpy
from rclpy.node import Node
import gymnasium as gym
from std_msgs.msg import Float32MultiArray
import numpy


class robot_bringup(Node):
    def __init__(self):
        super().__init__('robot_bringup')
        self.env = gym.make("Pusher-v5", render_mode='human')
        self.observation, _ = self.env.reset()
        self.action = numpy.zeros(self.env.action_space.shape)
        self.state_publisher_ = self.create_publisher(
            Float32MultiArray, 
            '/robot_state', 
            10
        )
        self.action_sub = self.create_subscription(
            Float32MultiArray,
            '/robot_control',
            self.get_action, 
            10
        )
        self.timer_ = self.create_timer(1/60, self.step)

    def step(self):
        s = self.observation
        self.state_publish(s)
        a = self.action
        self.observation, r, t, _, _ = self.env.step(a)

    def get_action(self, msg):
        self.action = numpy.array(msg.data)

    def state_publish(self, s):
        msg = Float32MultiArray()
        msg.data = s.tolist()
        self.state_publisher_.publish(msg)


def main(arg=None):
    rclpy.init()
    node = robot_bringup()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
