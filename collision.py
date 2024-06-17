import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, Slider, TextBox

# Define the Particle class
class Particle:
    def __init__(self, x, vx, mass, radius=0.01):
        self.x = x  # Position on the x-axis
        self.vx = vx  # Velocity along the x-axis
        self.mass = mass  # Mass of the particle
        self.radius = radius  # Radius of the particle for wall collision

    def move(self, dt):
        """Move the particle based on its velocity and time step dt."""
        self.x += self.vx * dt

    def collide_with_particle(self, other, restitution):
        """Handle collision with another particle."""
        if abs(self.x - other.x) < (self.radius + other.radius):  # Check if the particles are colliding
            # Relative velocity
            v1 = self.vx
            v2 = other.vx
            m1 = self.mass
            m2 = other.mass

            # New velocities after collision
            self.vx = (v1 * (m1 - restitution * m2) + (1 + restitution) * m2 * v2) / (m1 + m2)
            other.vx = (v2 * (m2 - restitution * m1) + (1 + restitution) * m1 * v1) / (m1 + m2)
            
            # Separate the particles slightly
            overlap = (self.radius + other.radius) - abs(self.x - other.x)
            separation = overlap / 2
            if self.x < other.x:
                self.x -= separation
                other.x += separation
            else:
                self.x += separation
                other.x -= separation

    def collide_with_walls(self, width):
        """Handle collision with the walls."""
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx = -self.vx
        if self.x + self.radius > width:
            self.x = width - self.radius
            self.vx = -self.vx

# Simulation parameters
initial_restitution = 0.9  # Initial coefficient of restitution
time_step = 0.01  # Smaller time step for smoother motion
width = 1.0  # Width of the plot

# Initialize the particle sliders as an empty list
velocity_sliders = []

# Function to initialize particles
def initialize_particles():
    global particles, restitution, velocity_sliders
    restitution = restitution_slider.val
    num_particles = int(particle_slider.val)
    particles = []
    for i in range(num_particles):
        x = np.random.rand() * (width - 0.1) + 0.05
        vx = velocity_sliders[i].val
        particles.append(Particle(x=x, vx=vx, mass=1))

# Set up the plot
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.5)  # Adjust subplot to make room for widgets
ax.set_xlim(0, width)
ax.set_ylim(-0.1, 0.1)
scat = ax.scatter([], [], s=100)  # Initialize empty scatter plot

# Create text annotations for velocities
velocity_texts = []

def update(frame):
    for p in particles:
        p.move(time_step)
        p.collide_with_walls(width)
    
    # Check for collisions between particles
    for i in range(len(particles)):
        for j in range(i + 1, len(particles)):
            particles[i].collide_with_particle(particles[j], restitution)
    
    # Update scatter plot positions
    scat.set_offsets([[p.x, 0] for p in particles])
    
    # Update velocity text annotations
    for i, p in enumerate(particles):
        if i < len(velocity_texts):
            velocity_texts[i].set_text(f'Particle {i+1} velocity: {p.vx:.2f}')
        else:
            velocity_texts.append(ax.text(0.02, 0.9 - 0.05 * i, f'Particle {i+1} velocity: {p.vx:.2f}', transform=ax.transAxes))
    
    return scat, *velocity_texts

# Create sliders for restitution
ax_restitution = plt.axes([0.2, 0.25, 0.65, 0.03])
restitution_slider = Slider(ax_restitution, 'Restitution', 0.0, 1.0, valinit=initial_restitution)

# Create a slider for the number of particles
ax_particles = plt.axes([0.2, 0.30, 0.65, 0.03])
particle_slider = Slider(ax_particles, 'Number of Particles', 1, 10, valinit=3, valstep=1)

# Create start button
ax_start = plt.axes([0.65, 0.025, 0.1, 0.04])
button_start = Button(ax_start, 'Start')

# Create stop button
ax_stop = plt.axes([0.75, 0.025, 0.1, 0.04])
button_stop = Button(ax_stop, 'Stop')

# Create a reset button
ax_reset = plt.axes([0.8, 0.025, 0.1, 0.04])
button_reset = Button(ax_reset, 'Reset')

ani = None  # Global variable to control animation instance

def start(event):
    global ani
    if ani is None:
        initialize_particles()
        ani = FuncAnimation(fig, update, frames=1000, interval=10, blit=True)
    plt.draw()  # Redraw the plot to update with the animation

button_start.on_clicked(start)

def stop(event):
    global ani
    if ani is not None:
        ani.event_source.stop()
        ani = None

button_stop.on_clicked(stop)

def reset(event):
    global ani, velocity_texts
    if ani is not None:
        ani.event_source.stop()
        ani = None
    velocity_texts = []
    initialize_particles()
    scat.set_offsets([[p.x, 0] for p in particles])  # Reset scatter plot positions
    for i, p in enumerate(particles):
        if i < len(velocity_texts):
            velocity_texts[i].set_text(f'Particle {i+1} velocity: {p.vx:.2f}')
        else:
            velocity_texts.append(ax.text(0.02, 0.9 - 0.05 * i, f'Particle {i+1} velocity: {p.vx:.2f}', transform=ax.transAxes))
    plt.draw()  # Redraw the plot to update positions and annotations

button_reset.on_clicked(reset)

# Function to dynamically update velocity sliders
def update_velocity_sliders(val):
    global velocity_sliders
    # Remove old sliders
    for slider in velocity_sliders:
        slider.ax.clear()
        slider.ax.remove()
    velocity_sliders = []

    # Create new sliders for each particle
    num_particles = int(particle_slider.val)
    for i in range(num_particles):
        ax_slider = plt.axes([0.2, 0.20 - 0.05 * i, 0.65, 0.03])
        velocity_slider = Slider(ax_slider, f'Velocity {i+1}', -2.0, 2.0, valinit=0.0)
        velocity_sliders.append(velocity_slider)
    plt.draw()  # Redraw the plot to update sliders

particle_slider.on_changed(update_velocity_sliders)

# Initialize the sliders based on the initial number of particles
update_velocity_sliders(particle_slider.val)

# Update the restitution value when the slider is changed
def update_restitution(val):
    global restitution
    restitution = restitution_slider.val

restitution_slider.on_changed(update_restitution)

plt.show()
