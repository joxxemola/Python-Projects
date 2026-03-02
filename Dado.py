# Implementación de librerías
import random
import matplotlib.pyplot as plt
import csv

def simular_y_graficar():
    # -----------------------------
    # Configuración general
    # -----------------------------
    n_dados = 1000
    n_intentos = 10000

    # -----------------------------3
    
    
    # ENTRADA DEL USUARIO
    # -----------------------------
    cara_favorita = int(input("Elige la cara del dado (1-6): "))
    porcentaje = float(input("Porcentaje de probabilidad para esa cara (0-100): "))

    prob_favorita = porcentaje / 100

    if cara_favorita < 1 or cara_favorita > 6:
        print("❌ La cara debe estar entre 1 y 6")
        return

    if prob_favorita < 0 or prob_favorita > 1:
        print("❌ El porcentaje debe estar entre 0 y 100")
        return

    # -----------------------------
    # Probabilidades del dado
    # -----------------------------
    caras = [1, 2, 3, 4, 5, 6]
    prob_restante = (1 - prob_favorita) / 5

    probabilidades = [
        prob_favorita if cara == cara_favorita else prob_restante
        for cara in caras
    ]
    # -----------------------------
    # Estado inicial 
    # -----------------------------
    dados = [6] * n_dados
    suma_actual = sum(dados)
    historial_sumas = [suma_actual]

    # -----------------------------
    # Simulación
    # -----------------------------
    for _ in range(n_intentos):
        indice = random.randint(0, n_dados - 1)

        nuevo_valor = random.choices(
            population=caras,
            weights=probabilidades,
            k=1
        )[0]

        suma_actual = suma_actual - dados[indice] + nuevo_valor
        dados[indice] = nuevo_valor
        historial_sumas.append(suma_actual)

    # -----------------------------
    # Guardar CSV
    # -----------------------------
    with open("historial_sumas.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["suma_total"])
        for valor in historial_sumas:
            writer.writerow([valor])

    # -----------------------------
    # Gráfica
    # -----------------------------
    plt.figure(figsize=(10, 6))
    plt.plot(historial_sumas, linewidth=1)

    promedio_teorico = n_dados * (
        cara_favorita * prob_favorita +
        sum(c for c in caras if c != cara_favorita) * prob_restante
    )

    plt.axhline(
        y=promedio_teorico,
        linestyle='--',
        label=f'Promedio teórico ≈ {promedio_teorico:.0f}'
    )

    plt.title('Evolución de la Suma de 1000 Dados (Interactivo)')
    plt.xlabel('Número de Intentos')
    plt.ylabel('Suma Total')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()

simular_y_graficar()
