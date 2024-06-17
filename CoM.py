import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Physical constants
g = 9.81  # acceleration due to gravity (m/s^2)
L = 1.0   # length of the pendulum (m)
theta0 = np.pi / 2  # initial angle (45 degrees)
omega0 = 0  # initial angular velocity (rad/s)
dt = 0.01  # time step (s)
T = 10  # total simulation time (s)

# Time array
time = np.arange(0, T, dt)

# Initialize arrays for angle, angular velocity, kinetic energy, potential energy
theta = np.zeros(len(time))
omega = np.zeros(len(time))
KE = np.zeros(len(time))
PE = np.zeros(len(time))
TE = np.zeros(len(time))

# Initial conditions
theta[0] = theta0
omega[0] = omega0

# Functions for the Runge-Kutta method
def f(theta, omega):
    return - (g / L) * np.sin(theta)

def runge_kutta_step(theta, omega, dt):
    k1_theta = omega
    k1_omega = f(theta, omega)
    
    k2_theta = omega + 0.5 * dt * k1_omega
    k2_omega = f(theta + 0.5 * dt * k1_theta, omega + 0.5 * dt * k1_omega)
    
    k3_theta = omega + 0.5 * dt * k2_omega
    k3_omega = f(theta + 0.5 * dt * k2_theta, omega + 0.5 * dt * k2_omega)
    
    k4_theta = omega + dt * k3_omega
    k4_omega = f(theta + dt * k3_theta, omega + dt * k3_omega)
    
    theta_new = theta + (dt / 6) * (k1_theta + 2*k2_theta + 2*k3_theta + k4_theta)
    omega_new = omega + (dt / 6) * (k1_omega + 2*k2_omega + 2*k3_omega + k4_omega)
    
    return theta_new, omega_new

# Simulation using the Runge-Kutta method
for i in range(1, len(time)):
    theta[i], omega[i] = runge_kutta_step(theta[i-1], omega[i-1], dt)
    KE[i] = 0.5 * (L**2) * (omega[i]**2)
    PE[i] = g * L * (1 - np.cos(theta[i]))
    TE[i] = KE[i] + PE[i]

# Create the figure and axes
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

# Pendulum plot
ax1.set_xlim(-L-0.1, L+0.1)
ax1.set_ylim(-L-0.1, L+0.1)
ax1.set_aspect('equal')
ax1.grid()
pendulum_line, = ax1.plot([], [], 'o-', lw=2)
time_template = 'Time = %.1fs'
time_text = ax1.text(0.05, 0.9, '', transform=ax1.transAxes)

# Energy plot
ax2.set_xlim(0, T)
ax2.set_ylim(0, max(KE+PE) * 1.1)
ax2.grid()
ke_line, = ax2.plot([], [], 'r-', label='Kinetic Energy')
pe_line, = ax2.plot([], [], 'b-', label='Potential Energy')
te_line, = ax2.plot([], [], 'g-', label='Total Energy')
ax2.legend()

# Initialize function for animation
def init():
    pendulum_line.set_data([], [])
    ke_line.set_data([], [])
    pe_line.set_data([], [])
    te_line.set_data([], [])
    time_text.set_text('')
    return pendulum_line, ke_line, pe_line, te_line, time_text

# Animation function
def animate(i):
    x = [0, L * np.sin(theta[i])]
    y = [0, -L * np.cos(theta[i])]
    pendulum_line.set_data(x, y)
    time_text.set_text(time_template % (i*dt))

    ke_line.set_data(time[:i], KE[:i])
    pe_line.set_data(time[:i], PE[:i])
    te_line.set_data(time[:i], TE[:i])
    
    return pendulum_line, ke_line, pe_line, te_line, time_text

# Create the animation
ani = animation.FuncAnimation(fig, animate, frames=len(time), init_func=init,
                              interval=dt*1000, blit=True)

plt.show()
