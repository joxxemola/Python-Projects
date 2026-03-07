import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from matplotlib.patches import Circle

# -----------------------------
# DATOS DEL PROBLEMA
# -----------------------------
v_tierra = 6.0
v_agua = 2.5

horizontal_total = 500.0
profundidad = 150.0

# -----------------------------
# FUNCION DE TIEMPO TOTAL
# -----------------------------
def tiempo_total(x):
    tiempo_tierra = np.sqrt(x**2 + profundidad**2) / v_tierra
    distancia_agua = np.sqrt((horizontal_total - x)**2 + profundidad**2)
    tiempo_agua = distancia_agua / v_agua
    return tiempo_tierra + tiempo_agua

x_vals = np.linspace(0, horizontal_total, 2000)
x_opt = x_vals[np.argmin(tiempo_total(x_vals))]

# -----------------------------
# PUNTOS
# -----------------------------
A = np.array([0, -150])
entrada = np.array([x_opt, 0])
B = np.array([horizontal_total, 150])

dist_tierra_total = np.linalg.norm(entrada - A)
dist_agua_total = np.linalg.norm(B - entrada)

tiempo_tierra = dist_tierra_total / v_tierra
tiempo_agua = dist_agua_total / v_agua
tiempo_total_mov = tiempo_tierra + tiempo_agua

print(f"Tiempo total: {tiempo_total_mov/60:.2f} minutos")

# -----------------------------
# FIGURA
# -----------------------------
fig, ax = plt.subplots(figsize=(10,5))
plt.subplots_adjust(left=0.08, right=0.98, top=0.90, bottom=0.28)

ax.set_xlim(-50, horizontal_total + 50)
ax.set_ylim(-200, 200)
ax.set_aspect('equal')
ax.set_facecolor('#eaf2f8')

# -----------------------------
# TIERRA
# -----------------------------
ax.fill_between([0, horizontal_total], -200, 0,
                color='#d2b48c', alpha=0.85)

# -----------------------------
# AGUA CON DEGRADADO
# -----------------------------
gradiente = np.linspace(0.3, 1, 400)
gradiente = np.vstack((gradiente, gradiente))

ax.imshow(gradiente.T,
          extent=[0, horizontal_total, 0, 200],
          origin='lower',
          cmap='Blues',
          alpha=0.9,
          aspect='auto')

ax.plot([0, horizontal_total], [0, 0], color='black', linewidth=2)

# Trayectoria guía
ax.plot([A[0], entrada[0]], [A[1], entrada[1]],
        '--', color='gray')
ax.plot([entrada[0], B[0]], [entrada[1], B[1]],
        '--', color='gray')

# Puntos
ax.scatter(*A, color='red', zorder=3)
ax.scatter(*entrada, color='black', zorder=3)
ax.scatter(*B, color='green', zorder=3)

ax.text(A[0], A[1]-15, 'Inicio')
ax.text(entrada[0], entrada[1]+10, 'Entrada óptima')
ax.text(B[0], B[1]+10, 'Meta')

# -----------------------------
# ATLETA
# -----------------------------
atleta, = ax.plot([], [], 'o', markeredgecolor='black')

cronometro = ax.text(10, 170, '', fontsize=12,
                     bbox=dict(facecolor='white', alpha=0.8))

velocidad_texto = ax.text(10, 150, '', fontsize=11,
                          bbox=dict(facecolor='white', alpha=0.8))

distancia_texto = ax.text(10, 130, '', fontsize=11,
                          bbox=dict(facecolor='white', alpha=0.8))

# -----------------------------
# ONDAS
# -----------------------------
ondas = []
onda_activa = False

# -----------------------------
# POSICION
# -----------------------------
def posicion(t):
    if t <= tiempo_tierra:
        frac = t / tiempo_tierra
        return A + frac * (entrada - A), False
    else:
        frac = (t - tiempo_tierra) / tiempo_agua
        return entrada + frac * (B - entrada), True

# -----------------------------
# ANIMACION
# -----------------------------
fps = 60
dt = tiempo_total_mov / (fps * 3)
t_actual = 0
anim_running = False

def update(frame):
    global t_actual, onda_activa

    if not anim_running:
        return []

    t_actual += dt
    if t_actual > tiempo_total_mov:
        return []

    pos, en_agua = posicion(t_actual)

    # Atleta
    atleta.set_data([pos[0]], [pos[1]])

    if en_agua:
        atleta.set_color('blue')
        atleta.set_markersize(8)
        velocidad_texto.set_text(f'Velocidad: {v_agua:.1f} m/s (agua)')
    else:
        atleta.set_color('red')
        atleta.set_markersize(11)
        velocidad_texto.set_text(f'Velocidad: {v_tierra:.1f} m/s (tierra)')

    cronometro.set_text(f'Tiempo: {t_actual:0.2f} s')

    # -----------------------------
    # DISTANCIA RECORRIDA
    # -----------------------------
    if t_actual <= tiempo_tierra:
        distancia_recorrida = (t_actual / tiempo_tierra) * dist_tierra_total
    else:
        distancia_recorrida = (
            dist_tierra_total +
            ((t_actual - tiempo_tierra) / tiempo_agua) * dist_agua_total
        )

    distancia_texto.set_text(
        f'Distancia recorrida: {distancia_recorrida:0.1f} m'
    )

    # -----------------------------
    # ONDAS AL ENTRAR AL AGUA
    # -----------------------------
    if en_agua and not onda_activa:
        onda_activa = True
        for r in [5, 10, 15]:
            onda = Circle((entrada[0], 0), r,
                          fill=False,
                          linewidth=1.5,
                          edgecolor='white',
                          alpha=0.8)
            ax.add_patch(onda)
            ondas.append(onda)

    for onda in ondas:
        onda.set_radius(onda.radius + 0.6)
        onda.set_alpha(max(onda.get_alpha() - 0.01, 0))

    return [atleta, cronometro,
            velocidad_texto, distancia_texto] + ondas

anim = FuncAnimation(fig, update,
                     interval=1000/fps,
                     blit=False)

# -----------------------------
# BOTONES
# -----------------------------
ax_start = plt.axes([0.20, 0.08, 0.18, 0.08])
ax_pause = plt.axes([0.41, 0.08, 0.18, 0.08])
ax_reset = plt.axes([0.62, 0.08, 0.18, 0.08])

btn_start = Button(ax_start, 'Iniciar')
btn_pause = Button(ax_pause, 'Pausar')
btn_reset = Button(ax_reset, 'Reiniciar')

def start(event):
    global anim_running
    anim_running = True

def pause(event):
    global anim_running
    anim_running = False

def reset(event):
    global t_actual, anim_running, onda_activa
    t_actual = 0
    anim_running = False
    onda_activa = False
    atleta.set_data([], [])
    for o in ondas:
        o.remove()
    ondas.clear()

btn_start.on_clicked(start)
btn_pause.on_clicked(pause)
btn_reset.on_clicked(reset)

# -----------------------------
# TITULOS
# -----------------------------
ax.set_title('Movimiento del atleta (trayectoria de tiempo mínimo)', pad=15)
ax.set_xlabel('Distancia horizontal (m)', labelpad=15)
ax.set_ylabel('Posición vertical (m)')

plt.show()