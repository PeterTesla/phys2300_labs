import numpy as np
from matplotlib import pyplot as plt
from vpython import *

g = 9.81    # m/s**2
l = 0.1     # meters
W = 0.002   # arm radius
R = 0.01     # ball radius
c = 6
framerate = 100
steps_per_frame = 1

class pendulum:

        def __init__(self, Theta, Omega, Color):
                self.theta = Theta
                self.omega = Omega

                self.theta_points = []
                self.omega_points = []

                self.string = cylinder(pos = vector(0,0,0), axis = vector(l*np.sin(self.theta), -l*np.cos(self.theta), 0), radius = W)
                self.ball = sphere(pos = vector(l*np.sin(self.theta),-l*np.cos(self.theta),0), radius = R, make_trail = True, color = Color)

        def UpdatePos(self):
                self.string.axis = vector(l*np.sin(self.theta), -l*np.cos(self.theta), 0)
                self.ball.pos = vector(l*np.sin(self.theta),-l*np.cos(self.theta),0)

        def CalculatePos(self, t, dt):
                
                for n in range(steps_per_frame):
                        k1 = dt*domega(self.theta,self.omega, t)
                        k2 = dt*domega(self.theta + 0.5*k1,self.omega, t + 0.5*dt)
                        k3 = dt*domega(self.theta + 0.5*k2,self.omega, t + 0.5*dt)
                        k4 = dt*domega(self.theta+k3,self.omega, t+dt)
                        self.omega += (k1 + 2*k2 + 2*k3 + k4)/6

                        k1 = dt*dtheta(self.omega, t)
                        k2 = dt*dtheta(self.omega + 0.5*k1, t + 0.5*dt)
                        k3 = dt*dtheta(self.omega + 0.5*k2, t + 0.5*dt)
                        k4 = dt*dtheta(self.omega+k3, t+dt)
                        self.theta += (k1 + 2*k2 + 2*k3 + k4)/6


                self.omega_points.append(self.omega)
                self.theta_points.append(self.theta)

                return self.theta, self.omega




def Set_Scene(theta):
    scene.title = "Assignment 6: Pendulum"
    scene.width = 1200
    scene.heigth = 1200
    scene.autoscale = True


def domega(theta, omega, t):
        return -(g/l)*np.sin(theta) -c*omega


def dtheta(omega, t):
        return omega 

def main():
    """
    """
    #Initial Positions
    theta = np.radians(179)
    omega = 0

    t = 0
    dt = 0.005

    Set_Scene(theta)

    pendulum_1 = pendulum(theta, omega, color.cyan)
    pendulum_2 = pendulum(theta - np.pi, 25, color.orange)

    t_points = []
    while t < 10:

        rate(framerate)
        
        pendulum_1.CalculatePos(t,dt)
        pendulum_1.UpdatePos()

        pendulum_2.CalculatePos(t,dt)
        pendulum_2.UpdatePos()

        t_points.append(t)
        t = t + dt


    # Plot Values
    plt.plot(t_points, pendulum_1.theta_points)
    plt.plot(t_points, pendulum_2.theta_points)
    plt.xlabel("time (s) ")
    plt.ylabel("theta (rad) ")
    plt.show()
 
    

if __name__ == "__main__":
    main()
    exit(0)
