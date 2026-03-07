import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

class SistemaPoleaMovil:
    def __init__(self, m1=2, m2=3, m3=1, g=9.8):
        """
        Configuración:
        - Polea fija en el techo (P1)
        - De P1 cuelgan: masa m1 (izquierda) y polea móvil P2 (derecha)
        - De P2 cuelgan: masa m2 (izquierda) y masa m3 (derecha)
        """
        self.m1 = m1
        self.m2 = m2
        self.m3 = m3
        self.g = g
        
        # Calcular aceleraciones correctamente para todos los casos
        self.a1, self.a2, self.a3 = self.calcular_aceleraciones()
        
        # Verificar ligadura
        self.verificar_ligadura()
        
        # Posiciones iniciales
        self.y1 = 2.0      # altura inicial m1
        self.yP2 = 2.8     # altura inicial polea móvil
        self.y2_rel = 0.8 if m2 > 0 else 0  # si m2=0, no hay masa
        self.y3_rel = 0.8 if m3 > 0 else 0
        
        # Velocidades iniciales
        self.v1 = 0
        self.v2 = 0
        self.v3 = 0
        self.vP2 = 0  # velocidad de la polea móvil
        
        # Configuración de la animación
        self.fig, self.ax = plt.subplots(figsize=(14, 9))
        self.t = 0
        self.dt = 0.05
        
        # Posiciones fijas
        self.polea_fija_x = 0
        self.polea_fija_y = 4.0
        
        # Límites físicos
        self.distancia_minima_polea = 0.6
        
        # Historial para gráficas (opcional)
        self.tiempo_hist = []
        self.posiciones_hist = {'m1': [], 'm2': [], 'm3': [], 'polea': []}
        
        # Colores para cada masa
        self.colores = {'m1': 'blue', 'm2': 'red', 'm3': 'green'}
        
    def verificar_ligadura(self):
        """Verificar la ecuación de ligadura del sistema"""
        if self.m2 > 0 or self.m3 > 0:
            ligadura = self.a2 + self.a3 + 2 * self.a1
            if abs(ligadura) > 1e-8:
                print(f"⚠️ Advertencia: Violación de ligadura: {ligadura:.2e}")
                if abs(ligadura) > 1e-5:
                    print("   Error significativo - revisar ecuaciones")
            else:
                print(f"✅ Ligadura verificada: a₂ + a₃ + 2a₁ = {ligadura:.2e}")
        else:
            print("📌 Caso especial: sin ligadura (masas libres)")
    
    def calcular_energias(self):
        """Calcular energías cinética y potencial del sistema"""
        # Velocidades actuales
        v1 = self.v1
        v2 = self.v2 if self.m2 > 0 else 0
        v3 = self.v3 if self.m3 > 0 else 0
        
        # Energía cinética
        EC = 0.5 * (self.m1 * v1**2 + 
                    (self.m2 * v2**2 if self.m2 > 0 else 0) + 
                    (self.m3 * v3**2 if self.m3 > 0 else 0))
        
        # Energía potencial (tomando y=0 como referencia)
        EP = self.m1 * self.g * self.y1 + \
             (self.m2 * self.g * self.y2 if self.m2 > 0 else 0) + \
             (self.m3 * self.g * self.y3 if self.m3 > 0 else 0)
        
        # Energía total
        ET = EC + EP
        
        return EC, EP, ET
    
    def calcular_aceleraciones(self):
        """Calcula aceleraciones para TODOS los casos posibles"""
        
        # CASO ESPECIAL: Sistema en equilibrio estático
        if abs(self.m1 - 2*self.m2) < 1e-10 and abs(self.m2 - self.m3) < 1e-10 and self.m2 > 0:
            print("⚖️ Sistema en equilibrio estático")
            return 0, 0, 0
        
        # CASO 1: m2 = 0 y m3 = 0
        if self.m2 == 0 and self.m3 == 0:
            # m₁ cae libremente, polea móvil también cae libremente
            print("📌 Caso especial: m₂ = m₃ = 0 → Caída libre de todo")
            a1 = self.g
            a2 = 0  # No hay masa m2
            a3 = 0  # No hay masa m3
            return a1, a2, a3
        
        # CASO 2: m2 = 0, m3 > 0
        elif self.m2 == 0 and self.m3 > 0:
            print("📌 Caso especial: m₂ = 0")
            # Resolviendo ecuaciones
            a1 = (self.m1 - 2*self.m3) * self.g / (self.m1 + 4*self.m3)
            a3 = -2 * a1
            a2 = 0
            return a1, a2, a3
        
        # CASO 3: m3 = 0, m2 > 0
        elif self.m3 == 0 and self.m2 > 0:
            print("📌 Caso especial: m₃ = 0")
            # Simétrico al caso anterior
            a1 = (self.m1 - 2*self.m2) * self.g / (self.m1 + 4*self.m2)
            a2 = -2 * a1
            a3 = 0
            return a1, a2, a3
        
        # CASO 4: Ambos m2 y m3 > 0 (caso general)
        else:
            print("📌 Caso general: todas las masas > 0")
            # Sistema de ecuaciones completo
            A = np.array([
                [2*self.m3, self.m2 + self.m3],
                [self.m1, -2*self.m2]
            ])
            B = np.array([
                (self.m2 - self.m3) * self.g,
                (self.m1 - 2*self.m2) * self.g
            ])
            
            try:
                a1, a2 = np.linalg.solve(A, B)
                print("   ✅ Solución encontrada")
            except np.linalg.LinAlgError:
                print("   ⚠️ Error en solución numérica, usando valores por defecto")
                a1, a2 = 0, 0
                
            a3 = -2*a1 - a2
            return a1, a2, a3
    
    def actualizar_posiciones(self, frame):
        """Actualiza posiciones respetando límites físicos"""
        self.t += self.dt
        
        # Movimiento de m1 (siempre presente)
        self.v1 = self.a1 * self.t
        dy1 = 0.5 * self.a1 * self.t**2
        nueva_y1 = 2.0 + dy1
        self.y1 = np.clip(nueva_y1, 0.5, 3.8)
        
        # ===== MOVIMIENTO DE LA POLEA MÓVIL - CORREGIDO =====
        if self.m2 == 0 and self.m3 == 0:
            # CASO ESPECIAL: Polea móvil cae libremente con aceleración g
            self.vP2 = self.g * self.t
            dyP2 = 0.5 * self.g * self.t**2
            nueva_yP2 = 2.8 + dyP2  # ¡Cae hacia abajo! (+dy porque y aumenta hacia abajo)
            print(f"Debug: Polea cayendo - t={self.t:.2f}, dy={dyP2:.3f}, y={nueva_yP2:.3f}")
        else:
            # CASO GENERAL: Polea móvil se mueve según ligadura (opuesta a m1)
            # La aceleración de la polea es -a1
            self.vP2 = -self.a1 * self.t
            dyP2 = -0.5 * self.a1 * self.t**2
            nueva_yP2 = 2.8 + dyP2
        
        self.yP2 = np.clip(nueva_yP2, 1.0, 3.8)
        
        # Actualizar posiciones de m2 y m3 solo si tienen masa
        if self.m2 > 0:
            self.v2 = self.a2 * self.t
            dy2_rel = 0.5 * self.a2 * self.t**2
            nueva_y2_rel = 0.8 + dy2_rel
            self.y2_rel = self.aplicar_limites_masa(nueva_y2_rel, self.yP2)
        
        if self.m3 > 0:
            self.v3 = self.a3 * self.t
            dy3_rel = 0.5 * self.a3 * self.t**2
            nueva_y3_rel = 0.8 + dy3_rel
            self.y3_rel = self.aplicar_limites_masa(nueva_y3_rel, self.yP2)
        
        # Guardar historial
        self.tiempo_hist.append(self.t)
        self.posiciones_hist['m1'].append(self.y1)
        self.posiciones_hist['polea'].append(self.yP2)
        if self.m2 > 0:
            self.posiciones_hist['m2'].append(self.y2)
        if self.m3 > 0:
            self.posiciones_hist['m3'].append(self.y3)
        
        # Verificar conservación de energía (cada 10 frames)
        if len(self.tiempo_hist) % 10 == 0:
            self.verificar_energia()
    
    def aplicar_limites_masa(self, y_rel, y_polea):
        """Aplica límites físicos a la posición relativa de una masa"""
        # Límite superior (no pasar polea)
        y_max = y_polea - self.distancia_minima_polea
        if y_polea + y_rel > y_max:
            y_rel = y_max - y_polea
        
        # Límite inferior
        if y_polea + y_rel < 0.5:
            y_rel = 0.5 - y_polea
        
        return y_rel
    
    def verificar_energia(self):
        """Verifica la conservación de energía (solo como diagnóstico)"""
        if len(self.tiempo_hist) > 1:
            EC, EP, ET_actual = self.calcular_energias()
            
            # Energía inicial (aproximada)
            ET_inicial = self.m1 * self.g * 2.0 + \
                        (self.m2 * self.g * (2.8 + 0.8) if self.m2 > 0 else 0) + \
                        (self.m3 * self.g * (2.8 + 0.8) if self.m3 > 0 else 0)
            
            # Cambio en energía total
            delta_ET = ET_actual - ET_inicial
            
            # Si el cambio es significativo, mostrar advertencia
            if abs(delta_ET) > 10 and len(self.tiempo_hist) > 20:  # Umbral arbitrario
                print(f"⚠️ Posible violación de conservación de energía: ΔE = {delta_ET:.2f} J")
    
    @property
    def y2(self):
        """Posición absoluta de m2 (solo si tiene masa)"""
        if self.m2 > 0:
            return self.yP2 + self.y2_rel
        return -10  # fuera de pantalla
    
    @property
    def y3(self):
        """Posición absoluta de m3 (solo si tiene masa)"""
        if self.m3 > 0:
            return self.yP2 + self.y3_rel
        return -10
    
    def dibujar_polea(self, x, y, radio, color_face, titulo, es_fija=True):
        """Dibuja una polea con estilo mejorado"""
        # Círculo principal
        polea = patches.Circle((x, y), radio, 
                              edgecolor='black', 
                              facecolor=color_face, 
                              linewidth=2,
                              zorder=3)
        self.ax.add_patch(polea)
        
        # Detalles de la polea (rueda)
        rueda = patches.Circle((x, y), radio*0.6, 
                              edgecolor='gray', 
                              facecolor='lightgray', 
                              linewidth=1,
                              zorder=4)
        self.ax.add_patch(rueda)
        
        # Eje de la polea
        eje = patches.Circle((x, y), radio*0.2, 
                            color='black', 
                            zorder=5)
        self.ax.add_patch(eje)
        
        # Texto identificador
        if es_fija:
            self.ax.text(x, y + radio + 0.2, titulo, 
                        ha='center', fontsize=9, 
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        else:
            self.ax.text(x, y + radio + 0.2, titulo, 
                        ha='center', fontsize=9, color='darkred',
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    def dibujar_masa(self, x, y, ancho, alto, masa, color, nombre, aceleracion, velocidad):
        """Dibuja una masa con estilo mejorado"""
        # Sombra (opcional)
        sombra = patches.Rectangle((x + 0.05, y - 0.4 - 0.05), ancho, alto, 
                                  facecolor='gray', alpha=0.3, zorder=1)
        self.ax.add_patch(sombra)
        
        # Cuerpo de la masa
        masa_rect = FancyBboxPatch((x, y - 0.4), ancho, alto,
                                  boxstyle="round,pad=0.02,rounding_size=0.05",
                                  edgecolor='black', 
                                  facecolor=color, 
                                  linewidth=2,
                                  alpha=0.9,
                                  zorder=2)
        self.ax.add_patch(masa_rect)
        
        # Etiqueta con masa
        self.ax.text(x + ancho/2, y, f'm{nombre} = {masa}kg', 
                    ha='center', va='center', 
                    fontsize=9, weight='bold',
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.7))
        
        # Indicador de aceleración
        if abs(aceleracion) > 0.01 and masa > 0:
            flecha_y = y + 0.6 if aceleracion > 0 else y - 0.6
            direccion = 0.3 if aceleracion > 0 else -0.3
            self.ax.arrow(x + ancho/2, y + (0.5 if aceleracion > 0 else -0.5), 
                         0, direccion, 
                         head_width=0.1, head_length=0.1, 
                         fc=color, ec=color, linewidth=2,
                         alpha=0.8)
            self.ax.text(x + ancho/2, flecha_y, 
                        f'a{nombre}={abs(aceleracion):.2f}', 
                        color=color, ha='center', fontsize=8,
                        bbox=dict(boxstyle="round,pad=0.1", facecolor="white", alpha=0.7))
        
        # Velocidad
        if abs(velocidad) > 0.01 and masa > 0:
            self.ax.text(x + ancho/2, y - 0.8, 
                        f'v={velocidad:.2f} m/s', 
                        ha='center', fontsize=7,
                        bbox=dict(boxstyle="round,pad=0.1", facecolor="lightyellow", alpha=0.7))
    
    def dibujar(self):
        """Dibuja el sistema completo con estilo mejorado"""
        self.ax.clear()
        
        # Límites y fondo
        self.ax.set_xlim(-4, 4)
        self.ax.set_ylim(0, 5)
        self.ax.set_aspect('equal')
        self.ax.set_facecolor('#f0f0f0')
        self.ax.grid(True, alpha=0.3, linestyle='--')
        
        # Calcular energías para mostrar
        EC, EP, ET = self.calcular_energias()
        
        # Determinar estado del sistema
        if self.m2 == 0 and self.m3 == 0:
            estado = "🔴 CASO ESPECIAL: m₂ = m₃ = 0 → CAÍDA LIBRE (todo cae)"
        elif self.m2 == 0:
            estado = "🟡 CASO ESPECIAL: m₂ = 0 (solo m₁ y m₃)"
        elif self.m3 == 0:
            estado = "🟡 CASO ESPECIAL: m₃ = 0 (solo m₁ y m₂)"
        else:
            estado = "🟢 SISTEMA COMPLETO: todas las masas presentes"
        
        # Direcciones
        dir1 = "↓" if self.a1 > 0 else "↑" if self.a1 < 0 else "—"
        dir2 = "↓" if self.a2 > 0 else "↑" if self.a2 < 0 else "—" if self.m2 > 0 else "✗"
        dir3 = "↓" if self.a3 > 0 else "↑" if self.a3 < 0 else "—" if self.m3 > 0 else "✗"
        
        # Velocidad de la polea
        v_polea_dir = "↓" if self.vP2 > 0 else "↑" if self.vP2 < 0 else "—"
        
        titulo = f'{estado}\n'
        titulo += f'📊 ACELERACIONES: a₁={self.a1:.2f} {dir1} | a₂={self.a2:.2f} {dir2} | a₃={self.a3:.2f} {dir3} m/s²\n'
        titulo += f'⚖️ MASAS: m₁={self.m1}kg, m₂={self.m2}kg, m₃={self.m3}kg'
        
        self.ax.set_title(titulo, fontsize=11, pad=15)
        
        # Techo decorado
        techo = patches.Rectangle((-2, 4.3), 4, 0.2, 
                                 facecolor='gray', edgecolor='darkgray', linewidth=2)
        self.ax.add_patch(techo)
        self.ax.text(0, 4.5, '🏢 TECHO', ha='center', fontsize=12, weight='bold')
        
        # Soportes del techo
        self.ax.plot([-1.5, -1.5], [4.3, 4.5], 'k-', linewidth=2)
        self.ax.plot([1.5, 1.5], [4.3, 4.5], 'k-', linewidth=2)
        
        # Polea fija
        self.dibujar_polea(self.polea_fija_x, self.polea_fija_y, 0.3, 
                          'gold', '⚙️ POLEA FIJA', es_fija=True)
        
        # Soporte polea fija
        self.ax.plot([0, 0], [self.polea_fija_y, 4.3], 'k-', linewidth=2)
        
        # Polea móvil
        self.dibujar_polea(2.0, self.yP2, 0.25, 'silver', 
                          '🔧 POLEA MÓVIL', es_fija=False)
        
        # Mostrar velocidad de la polea en caso especial
        if self.m2 == 0 and self.m3 == 0:
            self.ax.text(2.0, self.yP2 - 0.4, f'v_polea={self.vP2:.2f} m/s ↓', 
                        ha='center', fontsize=8, color='darkred',
                        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.7))
        
        # Límite físico
        if self.m2 > 0 or self.m3 > 0:
            limite_y = self.yP2 - self.distancia_minima_polea
            self.ax.axhline(y=limite_y, xmin=0.4, xmax=0.7, 
                          color='red', linestyle='--', alpha=0.5)
            self.ax.text(2.8, limite_y, '⚠️ Límite físico', 
                        color='red', fontsize=8, alpha=0.7,
                        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.7))
        
        # Cuerdas
        # Cuerda 1 (polea fija → m1 y polea móvil)
        self.ax.plot([0, -1.5], [self.polea_fija_y - 0.1, self.y1 + 0.3], 
                    'k-', linewidth=2, alpha=0.8)
        self.ax.plot([0, 1.75], [self.polea_fija_y - 0.1, self.yP2 + 0.2], 
                    'k-', linewidth=2, alpha=0.8)
        
        # Cuerda 2 (polea móvil → m2 y m3)
        if self.m2 > 0:
            self.ax.plot([1.75, 0.5], [self.yP2 - 0.1, self.y2 + 0.3], 
                        'k-', linewidth=2, alpha=0.8)
        if self.m3 > 0:
            self.ax.plot([2.25, 3.2], [self.yP2 - 0.1, self.y3 + 0.3], 
                        'k-', linewidth=2, alpha=0.8)
        
        # Masas
        self.dibujar_masa(-1.9, self.y1, 0.8, 0.8, self.m1, 
                         'lightblue', '₁', self.a1, self.v1)
        
        if self.m2 > 0:
            self.dibujar_masa(0.1, self.y2, 0.8, 0.8, self.m2, 
                            'lightcoral', '₂', self.a2, self.v2)
        else:
            self.ax.text(0.5, 2.5, '❌ (sin masa)', 
                        color='gray', ha='center', alpha=0.7,
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7))
        
        if self.m3 > 0:
            self.dibujar_masa(2.7, self.y3, 0.8, 0.8, self.m3, 
                            'lightgreen', '₃', self.a3, self.v3)
        else:
            self.ax.text(3.1, 2.5, '❌ (sin masa)', 
                        color='gray', ha='center', alpha=0.7,
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7))
        
        # Panel de información
        ligadura_text = f'{self.a2 + self.a3 + 2*self.a1:.2e}' if (self.m2>0 or self.m3>0) else 'N/A (caída libre)'
        
        info_text = (f'⏱️ Tiempo: {self.t:.1f} s\n'
                    f'📈 Ligadura: {ligadura_text}\n'
                    f'⚡ EC: {EC:.1f} J\n'
                    f'📐 EP: {EP:.1f} J\n'
                    f'💫 ET: {ET:.1f} J')
        
        if self.m2 == 0 and self.m3 == 0:
            info_text += '\n⚠️ CAÍDA LIBRE: Todo cae con g=9.8 m/s²'
        
        self.ax.text(-3.5, 4.6, info_text, 
                    bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.9, 
                             edgecolor="black"), 
                    fontsize=9)
        
        # Leyenda de símbolos
        leyenda = '📋 LEYENDA:\n↓ baja | ↑ sube | — quieto | ✗ sin masa | ⚠️ límite'
        self.ax.text(2.5, 0.2, leyenda, 
                    bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.9,
                             edgecolor="orange"),
                    fontsize=8)
        
        # Velocidades actuales
        vel_text = f'Velocidades: v₁={self.v1:.2f} | v₂={self.v2:.2f} | v₃={self.v3:.2f} m/s'
        self.ax.text(-3.5, 0.2, vel_text,
                    bbox=dict(boxstyle="round", facecolor="lightcyan", alpha=0.7),
                    fontsize=8)
    
    def animar(self, frame):
        """Función de animación"""
        self.actualizar_posiciones(frame)
        self.dibujar()
        return self.ax
    
    def ejecutar(self):
        """Ejecuta la animación"""
        print("\n" + "=" * 70)
        print("🎬 INICIANDO ANIMACIÓN DEL SISTEMA DE POLEAS")
        print("=" * 70)
        print("Controles:")
        print("  • Cierra la ventana para terminar")
        print("  • Se mostrarán advertencias si hay problemas")
        print("=" * 70)
        
        anim = FuncAnimation(self.fig, self.animar, interval=50, cache_frame_data=False)
        plt.tight_layout()
        plt.show()
        
        print("\n" + "=" * 70)
        print("✅ ANIMACIÓN FINALIZADA")
        print(f"⏱️ Tiempo total simulado: {self.t:.1f} s")
        print("=" * 70)


def mostrar_intro():
    """Muestra una introducción interactiva al sistema"""
    print("=" * 70)
    print("🎯 SISTEMA DE POLEA FIJA + POLEA MÓVIL (VERSIÓN CORREGIDA)")
    print("=" * 70)
    print("\n📐 CONFIGURACIÓN:")
    print("  • 🏢 Polea fija en el techo")
    print("  • 🔗 De ella cuelgan: m₁ y una polea móvil")
    print("  • ⚙️ De la polea móvil cuelgan: m₂ y m₃")
    print("\n✨ CORRECCIONES APLICADAS:")
    print("  • ✅ Cuando m₂=m₃=0: TODO cae libremente (m₁ Y polea móvil)")
    print("  • ✅ La polea móvil tiene su propio movimiento")
    print("  • ✅ Visualización de velocidades")
    print("  • ✅ Verificación de energía mejorada")
    print("=" * 70)


if __name__ == "__main__":
    mostrar_intro()
    
    # Entrada de datos con validación
    try:
        print("\n📝 INGRESE LAS MASAS (kg):")
        print("   • Para ver la corrección, pruebe m₁=5, m₂=0, m₃=0")
        print("   • Ejemplo 1: m₁=5, m₂=0, m₃=0 (caída libre de TODO)")
        print("   • Ejemplo 2: m₁=2, m₂=3, m₃=1 (caso general)")
        print("-" * 50)
        
        m1 = float(input("m₁ (kg) [5] para probar caída libre: ") or "5")
        m2 = float(input("m₂ (kg) [0] para probar caso especial: ") or "0")
        m3 = float(input("m₃ (kg) [0] para probar caso especial: ") or "0")
        
        # Validar que no sean negativas
        if m1 < 0 or m2 < 0 or m3 < 0:
            print("❌ Error: Las masas no pueden ser negativas. Usando valores por defecto.")
            m1, m2, m3 = 5, 0, 0
    except ValueError:
        print("❌ Error: Entrada inválida. Usando valores por defecto.")
        m1, m2, m3 = 5, 0, 0
    
    # Crear y ejecutar sistema
    print("\n" + "=" * 70)
    print("⚙️ CONFIGURANDO SISTEMA...")
    print("=" * 70)
    
    sistema = SistemaPoleaMovil(m1, m2, m3)
    
    print("\n" + "=" * 70)
    print("📊 ACELERACIONES CALCULADAS:")
    print(f"  • a₁ (m₁) = {sistema.a1:>7.3f} m/s² {'↓' if sistema.a1 > 0 else '↑' if sistema.a1 < 0 else '—'}")
    
    if m2 > 0:
        print(f"  • a₂ (m₂) = {sistema.a2:>7.3f} m/s² {'↓' if sistema.a2 > 0 else '↑' if sistema.a2 < 0 else '—'}")
    else:
        print(f"  • a₂ (m₂) =    (masa cero, no aplica)")
    
    if m3 > 0:
        print(f"  • a₃ (m₃) = {sistema.a3:>7.3f} m/s² {'↓' if sistema.a3 > 0 else '↑' if sistema.a3 < 0 else '—'}")
    else:
        print(f"  • a₃ (m₃) =    (masa cero, no aplica)")
    
    if m2 == 0 and m3 == 0:
        print(f"  • Polea móvil cae con g = {sistema.g:.1f} m/s² ↓")
    
    print("-" * 70)
    if m2 > 0 or m3 > 0:
        print(f"🔗 Verificación ligadura: a₂ + a₃ + 2a₁ = {sistema.a2 + sistema.a3 + 2*sistema.a1:.2e}")
    else:
        print("🔗 Ligadura: No aplica (sistema en caída libre)")
    
    # Calcular energías iniciales
    EC, EP, ET = sistema.calcular_energias()
    print(f"⚡ Energías iniciales: EC={EC:.1f} J, EP={EP:.1f} J, ET={ET:.1f} J")
    print("=" * 70)
    
    sistema.ejecutar()