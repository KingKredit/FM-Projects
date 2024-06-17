import openai
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from matplotlib.widgets import Slider, Button

# Initialize OpenAI API
class Particle:
    def __init__(self, x, y, velocity, mass, radius, theta):
        self.x = x  # Position on the x-axis
        self.y = y  # Position on the y-axis
        self.vx = velocity * math.cos(math.radians(theta))  # Velocity along the x-axis
        self.vy = velocity * math.sin(math.radians(theta))  # Velocity along the y-axis
        self.mass = mass  # Mass of the particle
        self.radius = radius  # Radius of the particle for wall collision
        self.theta = theta  # Launch angle in degrees
        
        # Additional attributes
        self.x0 = x  # Initial position on the x-axis
        self.y0 = y  # Initial position on the y-axis
        self.g = 9.8  # Acceleration due to gravity (m/s^2)
        self.t = 0  # Initial time

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt - 0.5 * self.g * dt ** 2
        self.vy += -self.g * dt

    def max_height(self):
        # Time to reach maximum height (when vy = 0)
        t_max_height = self.vy / self.g
        # Maximum height using the formula: h = y0 + vy * t - 0.5 * g * t^2
        max_height = self.y0 + self.vy * t_max_height - 0.5 * self.g * t_max_height ** 2
        return max_height
    
# Initialize variables
initial_angle = 45
initial_velocity = 50
initial_mass = 1
dt = 0.1

# Create the figure and axis
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.35)
ax.set_xlim(0, 500)
ax.set_ylim(0, 100)

particle, = ax.plot([], [], 'bo', markersize=5)
velocity_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
time_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)
x_distance = ax.text(0.02, 0.85, '', transform=ax.transAxes)
max_height_text = ax.text(0.02, 0.80, '', transform=ax.transAxes)

# Create sliders
ax_angle = plt.axes([0.1, 0.2, 0.65, 0.03], facecolor='lightgoldenrodyellow')
ax_velocity = plt.axes([0.1, 0.25, 0.65, 0.03], facecolor='lightgoldenrodyellow')
s_angle = Slider(ax_angle, 'Angle (degrees)', 0, 90, valinit=initial_angle)
s_velocity = Slider(ax_velocity, 'Velocity (m/s)', 0, 100, valinit=initial_velocity)

# Create buttons
ax_start = plt.axes([0.8, 0.2, 0.1, 0.04])
ax_stop = plt.axes([0.8, 0.25, 0.1, 0.04])
ax_reset = plt.axes([0.8, 0.3, 0.1, 0.04])
b_start = Button(ax_start, 'Start')
b_stop = Button(ax_stop, 'Stop')
b_reset = Button(ax_reset, 'Reset')

# Initialize particle
p = Particle(0, 0, initial_velocity, initial_mass, 0.1, initial_angle)
anim = None

def init():
    particle.set_data([], [])
    velocity_text.set_text('')
    x_distance.set_text('')
    max_height_text.set_text('')
    return particle, velocity_text, time_text, x_distance, max_height_text

def animate(frame):
    global p
    p.move(dt)
    if p.y >= 0:
        particle.set_data(p.x, p.y)
        velocity_text.set_text(f'Vx: {p.vx:.2f}, Vy: {p.vy:.2f}')
        time_text.set_text(f'Time: {frame*dt:.2f}s')
        x_distance.set_text(f'X-Distance: {p.x:.2f}')
        max_height_text.set_text(f'Max Height: {p.max_height():.2f}')
    return particle, velocity_text, time_text, x_distance, max_height_text


def start(event):
    global anim
    if anim:
        anim.event_source.start()
    else:
        anim = FuncAnimation(fig, animate, init_func=init, frames=np.arange(0, 100, dt), interval=10, blit=True)
        plt.draw()

def stop(event):
    global anim
    if anim:
        anim.event_source.stop()

def reset(event):
    global p, anim
    p = Particle(0, 0, s_velocity.val, 1, 0.1, s_angle.val)
    particle.set_data([], [])
    velocity_text.set_text('')
    if anim:
        anim.event_source.stop()
        anim = None
    plt.draw()

b_start.on_clicked(start)
b_stop.on_clicked(stop)
b_reset.on_clicked(reset)

# Button to set parameters from a question
ax_set_params = plt.axes([0.8, 0.15, 0.1, 0.04])
b_set_params = Button(ax_set_params, 'Set Params')

# Initialize the plot
init()
plt.show()
