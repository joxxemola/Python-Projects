import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, TextBox
import numpy as np

plt.style.use("seaborn-v0_8-whitegrid")

# ===============================
# FIGURA Y EJE PRINCIPAL
# ===============================
fig, ax = plt.subplots(figsize=(12, 4))
plt.subplots_adjust(right=0.75)

ax.set_xlim(-30, 140)
ax.set_ylim(0, 12)
ax.set_yticks([])
ax.set_xlabel("Distancia (km)")
ax.set_title("Acertijo de los trenes y la mosca", fontsize=14, weight="bold")

# ===============================
# PANEL DE INFORMACIÓN
# ===============================
info_ax = fig.add_axes([0.78, 0.35, 0.2, 0.55])
info_ax.axis("off")
info_text = info_ax.text(0.05, 0.9, "", fontsize=11, va="top")

# ===============================
# GRÁFICO DE REBOTES (ABAJO DE LOS DATOS)
# ===============================
rebotes_ax = fig.add_axes([0.78, 0.05, 0.2, 0.25])
rebotes_ax.set_xlim(0, 10)
rebotes_ax.set_ylim(0, 20)
rebotes_ax.set_xlabel("Tiempo (h)")
rebotes_ax.set_ylabel("Rebotes")
rebotes_line, = rebotes_ax.plot([], [], "-o", color="orange")
rebotes_time = []
rebotes_count = []

# ===============================
# PARÁMETROS
# ===============================
DISTANCIA = 100
RECT_LENGTH = 40
RECT_HEIGHT = 2
TRAIN_SPEED = 10
FLY_SPEED = 50
FPS = 50
DT = 1 / FPS
BALL_RADIUS = 0.1
TRAIL_LENGTH = 20

# ===============================
# ESTADO INICIAL
# ===============================
def reset_state():
    global left_train_x, right_train_x, fly_x, direction
    global time_h, rebotes, fly_distance, running, finished
    global fly_trail_x, fly_trail_y, fly_y
    global rebotes_time, rebotes_count

    left_train_x = -RECT_LENGTH
    right_train_x = DISTANCIA

    fly_x = left_train_x + RECT_LENGTH + BALL_RADIUS
    fly_y = 6
    direction = 1

    time_h = 0.0
    rebotes = 0
    fly_distance = 0.0

    running = False
    finished = False

    fly_trail_x = [fly_x]
    fly_trail_y = [fly_y]

    # Datos para gráfico de rebotes
    rebotes_time = [0]
    rebotes_count = [0]

reset_state()

# ===============================
# ELEMENTOS GRÁFICOS
# ===============================
left_train = patches.Rectangle((left_train_x, 5), RECT_LENGTH, RECT_HEIGHT,
                               color="#4C72B0", ec="black")
right_train = patches.Rectangle((right_train_x, 5), RECT_LENGTH, RECT_HEIGHT,
                                color="#55A868", ec="black")
left_shadow = patches.Rectangle((left_train_x + 2, 5 - 0.5), RECT_LENGTH, RECT_HEIGHT,
                                color="#2A4C72", alpha=0.3)
right_shadow = patches.Rectangle((right_train_x + 2, 5 - 0.5), RECT_LENGTH, RECT_HEIGHT,
                                 color="#2A8650", alpha=0.3)

ax.add_patch(left_shadow)
ax.add_patch(left_train)
ax.add_patch(right_shadow)
ax.add_patch(right_train)

fly, = ax.plot([fly_x], [6], "o", color="#C44E52", markersize=8)
fly_trail_lines = []
for i in range(TRAIL_LENGTH):
    line, = ax.plot([], [], "-", color="#C44E52", alpha=i / TRAIL_LENGTH)
    fly_trail_lines.append(line)

# ===============================
# UPDATE
# ===============================
def update(frame):
    global left_train_x, right_train_x, fly_x
    global direction, time_h, rebotes, fly_distance, finished
    global fly_trail_x, fly_trail_y
    global rebotes_time, rebotes_count

    gap = right_train_x - (left_train_x + RECT_LENGTH)

    if running and not finished:
        time_h += DT
        fly_distance += FLY_SPEED * DT

        left_train_x += TRAIN_SPEED * DT
        right_train_x -= TRAIN_SPEED * DT

        gap = right_train_x - (left_train_x + RECT_LENGTH)

        if gap <= 2 * BALL_RADIUS:
            fly_x = left_train_x + RECT_LENGTH + gap / 2
            finished = True
        else:
            fly_x += direction * FLY_SPEED * DT
            if fly_x >= right_train_x - BALL_RADIUS:
                fly_x = right_train_x - BALL_RADIUS
                direction = -1
                rebotes += 1
            if fly_x <= left_train_x + RECT_LENGTH + BALL_RADIUS:
                fly_x = left_train_x + RECT_LENGTH + BALL_RADIUS
                direction = 1
                rebotes += 1

        # Actualizar trenes
        left_train.set_x(left_train_x)
        left_shadow.set_x(left_train_x + 2)
        right_train.set_x(right_train_x)
        right_shadow.set_x(right_train_x + 2)

        # Actualizar mosca
        fly.set_data([fly_x], [6])
        fly_trail_x.append(fly_x)
        fly_trail_y.append(6)
        if len(fly_trail_x) > TRAIL_LENGTH:
            fly_trail_x.pop(0)
            fly_trail_y.pop(0)
        for i, line in enumerate(fly_trail_lines):
            if i < len(fly_trail_x):
                line.set_data(fly_trail_x[i:], fly_trail_y[i:])
                line.set_alpha(i / TRAIL_LENGTH)

        # Actualizar gráfico de rebotes
        rebotes_time.append(time_h)
        rebotes_count.append(rebotes)
        rebotes_line.set_data(rebotes_time, rebotes_count)
        rebotes_ax.set_xlim(0, max(10, time_h + 1))
        rebotes_ax.set_ylim(0, max(5, max(rebotes_count) + 1))

    # Actualizar panel de información
    info_text.set_text(
        f"DATOS DE LA SIMULACIÓN\n"
        f"────────────────────────\n"
        f"Tiempo transcurrido: {time_h:.2f} h\n"
        f"Rebotes de la mosca: {rebotes}\n"
        f"Distancia recorrida: {fly_distance:.1f} km\n"
        f"Distancia entre trenes: {gap:.1f} km\n"
        + ("\nSIMULACIÓN FINALIZADA" if finished else "")
    )

    return [left_train, left_shadow, right_train, right_shadow, fly] + fly_trail_lines + [info_text, rebotes_line]

# ===============================
# INICIO AUTOMÁTICO
# ===============================
def start_animation():
    global running
    running = True

timer = fig.canvas.new_timer(interval=2000)
timer.add_callback(start_animation)
timer.start()

# ===============================
# ANIMACIÓN
# ===============================
anim = FuncAnimation(
    fig,
    update,
    interval=1000 / FPS,
    blit=False,
    cache_frame_data=False
)

plt.show()
