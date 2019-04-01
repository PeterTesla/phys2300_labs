from vpython import *
from math import sin, cos
import argparse
import numpy as np
import matplotlib.pyplot as plt

def set_scene(data):
    """
    Set Vpython Scene
    """
    scene.title = "Assignment 5: Projectile motion"
    scene.width = 1200
    scene.heigth = 1200
    scene.caption = """Right button drag or Ctrl-drag to rotate "camera" to view scene.
    To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
    On a two-button mouse, middle is left + right.
    Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""
    scene.forward = vector(0, -.3, -1)
    scene.x = -1
    # Set background: floor, table, etc
    scene.autoscale = False 
    box(pos=vector(450,-data['ball_radius']-1,0), size=vector(1000,1,10))


def motion_no_drag(data):
    """
    Create animation for projectile motion with no dragging force
    """
    ball = sphere(pos=vector(-25, data['ball_radius'], 0),
                        radius=1, color=color.cyan, make_trail=True)
    # Follow the movement of the ball
    scene.camera.follow(ball)
    # Set initial velocity & position
    ball.velocity = vector(data['init_velocity']* np.cos( np.radians(data['theta']) ), data['init_velocity'] * np.sin( np.radians(data['theta'])) , 0)
    # Animate
    t = 0

    while t < 1000:
        rate(100)
        ball.velocity = ball.velocity + vector(0,data['gravity'],0)*data['deltat']
        ball.pos = ball.pos + ball.velocity*data['deltat']
        t = t + data['deltat']
        data['pos_nodrag_x'].append(ball.pos.x)
        data['pos_nodrag_y'].append(ball.pos.y)
        if ball.pos.y < -1:
            break


def motion_drag(data):
    """
    Create animation for projectile motion with no dragging force
    """
    ball = sphere(pos=vector(-25, data['ball_radius'], 0),
                        radius=1, color=color.blue, make_trail=True)
    # Follow the movement of the ball
    scene.camera.follow(ball)
    # Set initial velocity & position
    ball.velocity = vector(data['init_velocity']* np.cos( np.radians(data['theta']) ), data['init_velocity'] * np.sin( np.radians(data['theta'])) , 0)
    # Animate
    t = 0

    while t < 1000:
        rate(100)
        ball.velocity = ball.velocity + vector(0,data['gravity'],0)*data['deltat'] - (ball.velocity)*data['beta']*data['deltat']
        ball.pos = ball.pos + ball.velocity*data['deltat']
        t = t + data['deltat']
        data['pos_drag_x'].append(ball.pos.x)
        data['pos_drag_y'].append(ball.pos.y)
        if ball.pos.y < -1:
            break

def plot_data(data):
    plt.figure()
    plt.title('X and Y Positions of Projectile with and without Air Resistance')
    plt.ylabel('Y position (m) ')
    plt.xlabel('X position (m) ')
    plt.plot(data['pos_nodrag_x'], data['pos_nodrag_y'], color='c', label='Without Air Resistance')
    plt.plot(data['pos_drag_x'], data['pos_drag_y'], color='b', label='With Air Resistance')
    plt.legend()
    plt.show()


def main():
    """
    """

    # 1) Parse the arguments
    parser = argparse.ArgumentParser(description='Given starting conditions calculate and animate projectile motion')

    parser.add_argument('--velocity', metavar='V', help='Input the initial speed of the projectile in meters per second',action='store', type=int, required=True)
    parser.add_argument('--angle', metavar='theta', help ='Launch angle for projectile in degress', action='store', type=int, required=True)
    parser.add_argument('--height', type=float, help ='Optional initial projectile height')

    args = parser.parse_args()

    # Set Variables
    data = {}       # empty dictionary for all data and variables
    if args.height == None:
        data['init_height'] = 0
    else:
        data['init_height'] = args.height   # y-axis

    data['init_velocity'] = args.velocity  # m/s
    data['theta'] = args.angle       # degrees
    # Constants
    data['rho'] = 1.225  # kg/m^3
    data['Cd'] = 0.5    # coefficient friction
    data['deltat'] = 0.005
    data['gravity'] = -9.8  # m/s^2
    data['pos_nodrag_x'], data['pos_nodrag_y'] = [], []
    data['pos_drag_x'], data['pos_drag_y'] = [], []
    data['ball_mass'] = 0.145  # kg
    data['ball_radius'] = 0.075  # meters
    data['ball_area'] = np.pi * data['ball_radius']**2
    data['alpha'] = data['rho'] * data['Cd'] * data['ball_area'] / 2.0
    data['beta'] = data['alpha'] / data['ball_mass']

    # Set Scene
    set_scene(data)
    # 2) No Drag Animation
    motion_no_drag(data)
    # 3) Drag Animation
    motion_drag(data)
    # 4) Plot Information: extra credit
    plot_data(data)


if __name__ == "__main__":
    main()
    exit(0)
