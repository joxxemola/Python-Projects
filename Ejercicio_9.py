import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# =========================
# PARÁMETROS DEL PROBLEMA
# =========================
g = 9.8
D = 10
h = 4
theta = np.radians(40)
v0 = 16.17

vx0 = v0 * np.cos(theta)
vy0 = v0 * np.sin(theta)

t1 = D / vx0

a = 0.5 * g
b = -vy0
c = h
disc = b**2 - 4*a*c
t_total = (-b + np.sqrt(disc)) / (2*a)

# =========================
# ESTILO GENERAL
# =========================
plt.style.use("dark_background")

fig, ax = plt.subplots(figsize=(8,5))
ax.set_xlim(-1, D + 2)
ax.set_ylim(0, 12)

ax.set_title("Trayectoria del balón", fontsize=14, pad=10)
ax.set_xlabel("Distancia (m)")
ax.set_ylabel("Altura (m)")

# Rejilla suave
ax.grid(alpha=0.2)

# =========================
# ESCENARIO
# =========================
# Suelo
ax.plot([-1, D+2], [0, 0], color="white", linewidth=2)

# Paredes
ax.plot([0, 0], [0, 12], color="gray", linewidth=3)
ax.plot([D, D], [0, 12], color="gray", linewidth=3)

# Canasta
ax.plot([0.0, 1.5], [h, h], color="orange", linewidth=4)

# =========================
# PELOTA Y TRAYECTORIA
# =========================
ball, = ax.plot([], [], 'o',
                color="orange",
                markersize=10,
                markeredgecolor="white")

trail, = ax.plot([], [], '--',
                 color="cyan",
                 linewidth=2,
                 alpha=0.8)

xdata, ydata = [], []

# =========================
# ACTUALIZACIÓN
# =========================
def update(t):

    if t <= t1:
        x = vx0 * t
    else:
        x = D - vx0 * (t - t1)

    y = vy0 * t - 0.5 * g * t**2

    xdata.append(x)
    ydata.append(y)

    ball.set_data([x], [y])
    trail.set_data(xdata, ydata)

    return ball, trail

ani = FuncAnimation(
    fig,
    update,
    frames=np.linspace(0, t_total, 250),
    interval=30
)

plt.show()
