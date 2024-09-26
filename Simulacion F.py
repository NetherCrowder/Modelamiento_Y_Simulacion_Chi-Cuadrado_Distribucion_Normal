import numpy as np
from scipy.stats import chi2, norm
import matplotlib.pyplot as plt

# Parámetros de la simulación
minerales_por_minuto = {
    'hierro': {
        'impuro': 30,
        'normal': 60,
        'puro': 120
    },
    'cobre': {
        'impuro': 30,
        'normal': 60,
        'puro': 120
    }
}
max_entrada_minutos = 30
max_salida_minutos = 30
max_cinta_minutos = 60  # Límite máximo de la cinta transportadora

# Función para simular la extracción de minerales
def simular_extraccion(estado_mena, mineral, tiempo_simulacion_minutos):
    minerales_por_minuto_estado = minerales_por_minuto.get(mineral, {}).get(estado_mena, 0)
    if minerales_por_minuto_estado == 0:
        return "Estado de mena o mineral no válido"

    extraccion = np.random.normal(minerales_por_minuto_estado, minerales_por_minuto_estado * 0.1,
                                  tiempo_simulacion_minutos)

    return extraccion


# Función para simular la entrada de minerales al horno
def simular_entrada_al_horno(entrada_cinta, num_hornos, tiempo_simulacion_minutos):
    entrada = np.minimum(entrada_cinta, max_entrada_minutos * num_hornos)
    return entrada


# Función para simular la salida de lingotes del horno
def simular_salida_de_lingotes(entrada_minutos, num_hornos):
    salida = np.minimum(entrada_minutos, max_salida_minutos * num_hornos)
    return salida


# Función para simular la conversión de lingotes de hierro en barras de hierro en constructores
def simular_construccion_barras_de_hierro(entrada_lingotes, tiempo_simulacion_minutos):
    conversion_rate = 15  # 15 lingotes por minuto se convierten en 15 barras de hierro por minuto
    salida_barras_de_hierro = np.minimum(entrada_lingotes, conversion_rate * tiempo_simulacion_minutos)
    return salida_barras_de_hierro


# Función para simular la conversión de lingotes de cobre en alambres en constructores
def simular_construccion_alambres(entrada_lingotes, tiempo_simulacion_minutos):
    conversion_rate = 15  # Cada 15 lingotes de cobre se convierten en 30 alambres
    salida_alambres = np.floor(
        entrada_lingotes / 15) * 30  # Usamos np.floor para asegurarnos de no producir más alambres de los esperados
    return salida_alambres


# Función para simular el movimiento de minerales en la cinta transportadora
def simular_cinta_transportadora(entrada_extraccion, num_cintas, tiempo_simulacion_minutos):
    cinta = np.minimum(entrada_extraccion, max_cinta_minutos * num_cintas)
    return cinta


# Función para calcular el total de minerales transportados por cada cinta
def calcular_totales_cintas(resultados_cinta, num_cintas, tiempo_simulacion_minutos):
    totales_cintas = [np.sum(resultados_cinta[i::num_cintas]) for i in range(num_cintas)]
    return totales_cintas


# Simulación de extracción de minerales durante 60 minutos en estado impuro
estado_mena_hierro = 'impuro'
estado_mena_cobre = 'normal'  # Cambiar a 'impuro' o 'puro' según se necesite
tiempo_simulacion_minutos = 5

# Crear vectores para almacenar los resultados de extracción
resultados_extraccion_hierro = np.zeros(tiempo_simulacion_minutos)
resultados_extraccion_cobre = np.zeros(tiempo_simulacion_minutos)

# Determinar el número de cintas y hornos según el nivel de pureza
if estado_mena_hierro == 'impuro':
    num_cintas_hierro = 1
    num_hornos_hierro = 1
elif estado_mena_hierro == 'normal':
    num_cintas_hierro = 2
    num_hornos_hierro = 2
elif estado_mena_hierro == 'puro':
    num_cintas_hierro = 4
    num_hornos_hierro = 4

if estado_mena_cobre == 'impuro':
    num_cintas_cobre = 1
    num_hornos_cobre = 1
elif estado_mena_cobre == 'normal':
    num_cintas_cobre = 2
    num_hornos_cobre = 2
elif estado_mena_cobre == 'puro':
    num_cintas_cobre = 4
    num_hornos_cobre = 4

# Simulación de extracción de hierro y cobre
for minuto in range(tiempo_simulacion_minutos):
    resultados_extraccion_hierro[minuto] = simular_extraccion(estado_mena_hierro, 'hierro', 1)
    resultados_extraccion_cobre[minuto] = simular_extraccion(estado_mena_cobre, 'cobre', 1)

resultados_cinta_hierro = simular_cinta_transportadora(resultados_extraccion_hierro, num_cintas_hierro,
                                                       tiempo_simulacion_minutos)
resultados_cinta_cobre = simular_cinta_transportadora(resultados_extraccion_cobre, num_cintas_cobre,
                                                      tiempo_simulacion_minutos)

resultados_entrada_horno_hierro = simular_entrada_al_horno(resultados_cinta_hierro, num_hornos_hierro,
                                                           tiempo_simulacion_minutos)
resultados_entrada_horno_cobre = simular_entrada_al_horno(resultados_cinta_cobre, num_hornos_cobre,
                                                          tiempo_simulacion_minutos)

resultados_salida_lingotes_hierro = simular_salida_de_lingotes(resultados_entrada_horno_hierro, num_hornos_hierro)
resultados_salida_lingotes_cobre = simular_salida_de_lingotes(resultados_entrada_horno_cobre, num_hornos_cobre)

# Simulación de conversión de lingotes de hierro en barras de hierro en constructores
resultados_construccion_barras_de_hierro_hierro = simular_construccion_barras_de_hierro(
    resultados_salida_lingotes_hierro, tiempo_simulacion_minutos)

# Simulación de conversión de lingotes de cobre en alambres en constructores
resultados_construccion_alambres_cobre = simular_construccion_alambres(resultados_salida_lingotes_cobre,
                                                                       tiempo_simulacion_minutos)

# Calcular el total de minerales transportados por cada cinta
totales_cintas_hierro = calcular_totales_cintas(resultados_cinta_hierro, num_cintas_hierro, tiempo_simulacion_minutos)
totales_cintas_cobre = calcular_totales_cintas(resultados_cinta_cobre, num_cintas_cobre, tiempo_simulacion_minutos)

# Calcular el total de minerales que entraron en cada horno
totales_entrada_horno_hierro = [np.sum(resultados_entrada_horno_hierro[i::num_hornos_hierro]) for i in
                                range(num_hornos_hierro)]
totales_entrada_horno_cobre = [np.sum(resultados_entrada_horno_cobre[i::num_hornos_cobre]) for i in
                               range(num_hornos_cobre)]

# Calcular el total de lingotes que salieron en total
total_salida_lingotes_hierro = np.sum(resultados_salida_lingotes_hierro)
total_salida_lingotes_cobre = np.sum(resultados_salida_lingotes_cobre)

# Calcular el total de barras de hierro producidas
total_barras_de_hierro_hierro = np.sum(resultados_construccion_barras_de_hierro_hierro)

# Calcular el total de alambres producidos
total_alambres_cobre = np.sum(resultados_construccion_alambres_cobre)

# Imprimir resultados
print(
    f"Simulación de extracción de hierro en estado {estado_mena_hierro} y cobre en estado {estado_mena_cobre} durante {tiempo_simulacion_minutos} minutos:")
for i, (extraccion_hierro, cinta_hierro, entrada_horno_hierro, salida_lingotes_hierro, extraccion_cobre, cinta_cobre,
        entrada_horno_cobre, salida_lingotes_cobre) in enumerate(
        zip(resultados_extraccion_hierro, resultados_cinta_hierro, resultados_entrada_horno_hierro,
            resultados_salida_lingotes_hierro, resultados_extraccion_cobre, resultados_cinta_cobre,
            resultados_entrada_horno_cobre, resultados_salida_lingotes_cobre), 1):
    print(
        f"Minuto {i}: Extracción Hierro: {extraccion_hierro:.2f} minerales, Cinta Hierro: {cinta_hierro}, Entrada al horno Hierro: {entrada_horno_hierro}, Salida de lingotes Hierro: {salida_lingotes_hierro}, Extracción Cobre: {extraccion_cobre:.2f} minerales, Cinta Cobre: {cinta_cobre}, Entrada al horno Cobre: {entrada_horno_cobre}, Salida de lingotes Cobre: {salida_lingotes_cobre}")

for i, total_cinta_hierro in enumerate(totales_cintas_hierro):
    print(f"Total transportado por cinta Hierro {i + 1}: {total_cinta_hierro}")

for i, total_cinta_cobre in enumerate(totales_cintas_cobre):
    print(f"Total transportado por cinta Cobre {i + 1}: {total_cinta_cobre}")

for i, total_entrada_horno_hierro in enumerate(totales_entrada_horno_hierro):
    print(f"Total de minerales entrados al horno Hierro {i + 1}: {total_entrada_horno_hierro}")

for i, total_entrada_horno_cobre in enumerate(totales_entrada_horno_cobre):
    print(f"Total de minerales entrados al horno Cobre {i + 1}: {total_entrada_horno_cobre}")

print(f"Total de lingotes salidos en total (Hierro): {total_salida_lingotes_hierro}")
print(f"Total de lingotes salidos en total (Cobre): {total_salida_lingotes_cobre}")
print(f"Total de barras de hierro producidas (Hierro): {total_barras_de_hierro_hierro}")
print(f"Total de alambres producidos (Cobre): {total_alambres_cobre}")

# Mostrar los arreglos de resultados de extracción de hierro y cobre
print("Resultados de extracción de hierro (por minuto):")
print(resultados_extraccion_hierro)
print("Resultados de extracción de cobre (por minuto):")
print(resultados_extraccion_cobre)


# Función para realizar la prueba de bondad de ajuste chi-cuadrada
def prueba_chi_cuadrada(resultados):
    # Calcular la media y la desviación estándar de los resultados
    media = np.mean(resultados)
    desviacion_estandar = np.std(resultados, ddof=1)  # Usamos ddof=1 para calcular la desviación estándar muestral

    # Generar valores esperados basados en una distribución normal
    valores_esperados = np.random.normal(media, desviacion_estandar, len(resultados))

    # Redondear los valores
    resultados_redondeados = np.round(resultados)
    valores_esperados_redondeados = np.round(valores_esperados)

    # Calcular el estadístico de prueba chi-cuadrada
    chi_cuadrada = np.sum((resultados_redondeados - valores_esperados_redondeados) ** 2 / valores_esperados_redondeados)

    return chi_cuadrada


# Realizar la prueba de bondad de ajuste chi-cuadrada para hierro y cobre
chi_cuadrada_hierro = prueba_chi_cuadrada(resultados_extraccion_hierro)
chi_cuadrada_cobre = prueba_chi_cuadrada(resultados_extraccion_cobre)

# Establecer un nivel de significancia
nivel_de_significancia = 0.05

# Comparar los valores de chi-cuadrada con el valor crítico
grados_de_libertad = len(resultados_extraccion_hierro) - 1  # Se calcula como n - 1
valor_critico = chi2.ppf(1 - nivel_de_significancia, grados_de_libertad)

# Imprimir los resultados de la prueba
print(f"Prueba chi-cuadrada para hierro:")
print(f"Valor de chi-cuadrada: {chi_cuadrada_hierro}")
print(f"Valor crítico: {valor_critico}")

if chi_cuadrada_hierro > valor_critico:
    print("Los resultados de extracción de hierro no siguen una distribución normal (se rechaza la hipótesis nula).")
else:
    print("Los resultados de extracción de hierro siguen una distribución normal (no se rechaza la hipótesis nula).")

print("Prueba chi-cuadrada para cobre:")
print(f"Valor de chi-cuadrada: {chi_cuadrada_cobre}")
print(f"Valor crítico: {valor_critico}")

if chi_cuadrada_cobre > valor_critico:
    print("Los resultados de extracción de cobre no siguen una distribución normal (se rechaza la hipótesis nula).")
else:
    print("Los resultados de extracción de cobre siguen una distribución normal (no se rechaza la hipótesis nula).")

# Crear una figura con dos subtramas (una para hierro y otra para cobre)
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Simulación de valores de una distribución normal para hierro
mu_hierro = np.mean(resultados_extraccion_hierro)
sigma_hierro = np.std(resultados_extraccion_hierro,
                      ddof=1)  # Usamos ddof=1 para calcular la desviación estándar muestral
valores_simulados_hierro = np.random.normal(mu_hierro, sigma_hierro, tiempo_simulacion_minutos)

# Simulación de valores de una distribución normal para cobre
mu_cobre = np.mean(resultados_extraccion_cobre)
sigma_cobre = np.std(resultados_extraccion_cobre, ddof=1)
valores_simulados_cobre = np.random.normal(mu_cobre, sigma_cobre, tiempo_simulacion_minutos)

# Crear histogramas y curvas de densidad de probabilidad
axes[0].hist(resultados_extraccion_hierro, bins=10, density=True, alpha=1, color='b', label='Datos reales (Hierro)')
axes[0].plot(np.linspace(mu_hierro - 3 * sigma_hierro, mu_hierro + 3 * sigma_hierro, 100),
             norm.pdf(np.linspace(mu_hierro - 3 * sigma_hierro, mu_hierro + 3 * sigma_hierro, 100), mu_hierro,
                      sigma_hierro), 'r-', lw=2, label='Distribución Normal')
axes[0].set_title('Extracción de Hierro')
axes[0].legend()

axes[1].hist(resultados_extraccion_cobre, bins=10, density=True, alpha=1, color='g', label='Datos reales (Cobre)')
axes[1].plot(np.linspace(mu_cobre - 3 * sigma_cobre, mu_cobre + 3 * sigma_cobre, 100),
             norm.pdf(np.linspace(mu_cobre - 3 * sigma_cobre, mu_cobre + 3 * sigma_cobre, 100), mu_cobre, sigma_cobre),
             'r-', lw=2, label='Distribución Normal')
axes[1].set_title('Extracción de Cobre')
axes[1].legend()

plt.tight_layout()
plt.show()