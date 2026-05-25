import matplotlib.pyplot as plt
import os

def leer_ventas(ruta_archivo):
    """
    Lee el archivo CSV manualmente.
    Retorna una lista de tuplas (fecha, monto).
    """
    datos = []
    # Verifico existencia del archivo
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(
            f"No se encuentra el archivo: {ruta_archivo}"
        )
    with open(ruta_archivo, "r") as f:
        lineas = f.readlines()
    
    # Salteo la primera linea
    for linea in lineas[1:]:
        linea = linea.strip()
        if not linea:
            continue
        partes = linea.split(",")
        if len(partes) >= 3:
            fecha = partes[1]       # columna 2: fecha (YYYY-MM-DD)
            monto = float(partes[2]) # columna 3: monto
            datos.append((fecha, monto))
    return datos

def obtener_mes(fecha_str):
    """Obtengo el mes en formato 'YYYY-MM' desde 'YYYY-MM-DD'."""
    return fecha_str[:7]

def main():
    # Defino las rutas relativas
    ruta_datos = os.path.join("datos", "ventas.csv")
    ruta_grafico = os.path.join("resultados", "ventas_mensuales.png")
    ruta_resumen = os.path.join("resultados", "resumen_ventas.txt")
    
    # Leo los datos
    datos = leer_ventas(ruta_datos)
    if not datos:
        print("No se encontraron datos.")
        return
    
    # Consigo las listas
    fechas = [f for f, _ in datos]
    montos = [m for _, m in datos]
    
    # 1. Ventas totales y promedio diario
    total_ventas = sum(montos)
    promedio_diario = total_ventas / len(montos)
    
    # 2. Dia con mayor venta
    max_monto = max(montos)
    idx_max = montos.index(max_monto)
    dia_max = fechas[idx_max]
    
    # 3. Ventas por mes
    ventas_por_mes = {}
    for fecha, monto in datos:
        mes = obtener_mes(fecha)
        ventas_por_mes[mes] = ventas_por_mes.get(mes, 0) + monto
    
    # 4. Uso un grafico de barras con ventas por mes
    meses_ordenados = sorted(ventas_por_mes.keys())
    valores = [ventas_por_mes[mes] for mes in meses_ordenados]

    if total_ventas <= 0:
        print("Advertencia: total de ventas igual o menor a 0")

    if len(ventas_por_mes) == 0:
        print("No hay ventas agrupadas por mes")

    if len(meses_ordenados) != len(valores):
        print("Error de consistencia entre meses y valores")

    # Le doy estilo
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(meses_ordenados, valores, color='#2E86AB', edgecolor='white', linewidth=1.2)
    
    # Pinto la barra mas alta (mes con mas ventas)
    max_val = max(valores)
    max_idx = valores.index(max_val)
    bars[max_idx].set_color('#D62828')
    
    # Pongo valores arriba de las barras
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'${height:,.0f}',
                    xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 5), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # Titulo y ejes
    ax.set_title('Ventas mensuales - Año 2024', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Mes', fontsize=12, labelpad=10)
    ax.set_ylabel('Total de ventas ($)', fontsize=12, labelpad=10)
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.set_axisbelow(True)
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(ruta_grafico, dpi=150, bbox_inches='tight')
    plt.close()
    
    # 5. Guardo el resumen en un archivo de texto
    with open(ruta_resumen, "w", encoding="utf-8") as f:
        f.write("RESUMEN DE ANÁLISIS DE VENTAS\n")
        f.write(f"Ventas totales: ${total_ventas:,.2f}\n")
        f.write(f"Promedio diario: ${promedio_diario:,.2f}\n")
        f.write(f"Dia con mayor venta: {dia_max} -> ${max_monto:,.2f}\n")
        f.write("\nVentas por mes:\n")
        for mes in meses_ordenados:
            f.write(f"  {mes}: ${ventas_por_mes[mes]:,.2f}\n")
    
    print(f"   - Gráfico guardado en: {ruta_grafico}")
    print(f"   - Resumen guardado en: {ruta_resumen}")

if __name__ == "__main__":
    main()