import argparse   # Para leer argumentos desde la línea de comandos
import pandas as pd # Para trabajar con archivos CSV fácilmente
import os   # Para comprobar si existe un archivo
import sys  # Para salir del programa si hay errores
import matplotlib.pyplot as plt # Para graficar los datos

def analizar_keywords(df):
    resultados = {}  # Diccionario para guardar los resultados por palabra clave
    for col in df.columns[1:]:  # Recorre todas las columnas excepto la primera (que es 'Date')
        datos = df[col] 
        promedio = datos.mean()   # Promedio del interés
        max_fecha = df.loc[datos.idxmax(), 'Date']  # Fecha de mayor interés
        min_fecha = df.loc[datos.idxmin(), 'Date']  # Fecha de menor interés
        desviacion = datos.std()   # Volatilidad (desviación estándar)


        resultados[col] = {
            'promedio': promedio,
            'fecha_max': max_fecha,
            'fecha_min': min_fecha,
            'desviacion': desviacion
        }

    return resultados  # Devuelve el diccionario de resultados

def comparar_keywords(resultados, lista_keywords): #Aqui es para mostrar los datos de cada palabra clave
    print("\n📊 Comparación de palabras clave:")
    for kw in lista_keywords:
        if kw not in resultados:
            print(f"❗ '{kw}' no encontrado en el CSV.")
            continue

        info = resultados[kw]
        print(f"\n🔍 {kw}")
        print(f"Promedio: {info['promedio']:.2f}")
        print(f"Máximo interés: {info['fecha_max']}")
        print(f"Mínimo interés: {info['fecha_min']}")
        print(f"Volatilidad: {info['desviacion']:.2f}")

def graficar_keywords(df, lista_keyword):
    plt.figure(figsize=(10, 5)) # Crea un lienzo de 10x5 pulgadas
    
    for kw in lista_keyword:
        if kw in df.columns:
            plt.plot(df['Date'], df[kw], label=kw)  # Dibuja la curva de esa palabra clave
        else:
            print(f"'{kw}' no está en el archivo CSV y no se graficará.")

    plt.xlabel("Fecha")
    plt.ylabel("Interés de búsqueda")
    plt.title("Tendencias de palabras clave")
    plt.xticks(rotation=45)  # Gira las fechas para que se vean bien
    plt.legend()
    plt.tight_layout()
    plt.show()  # Muestra la gráfica



def exportar_a_txt(resultados, nombre_archivo="resumen.txt"):
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            for kw, datos in resultados.items():
                f.write(f"🔍 {kw}\n")
                f.write(f"Promedio: {datos['promedio']:.2f}\n")
                f.write(f"Máximo interés: {datos['fecha_max']}\n")
                f.write(f"Mínimo interés: {datos['fecha_min']}\n")
                f.write(f"Volatilidad: {datos['desviacion']:.2f}\n")
                f.write("\n")
        print(f"\n✅ Resultados exportados a {nombre_archivo}")
    except Exception as e:
        print(f"❌ Error al exportar a .txt: {e}")



def main():
     # Define los argumentos desde terminal
    parser = argparse.ArgumentParser(description="Analizador de tendencias de Google")
    parser.add_argument('--file', type=str, required=True, help='Ruta del archivo CSV')
    parser.add_argument('--compare', type=str, help='Palabras clave a comparar, separadas por comas (ej: Python,Java)')
    args = parser.parse_args()

       # Verifica que el archivo exista
    if not os.path.exists(args.file):
        print(f"Error: No se encontró el archivo '{args.file}'")
        sys.exit(1)

    try:
        df = pd.read_csv(args.file)
        if 'Date' not in df.columns:
            print("Error: El archivo debe tener una columna 'Date'")
            sys.exit(1)
        resultados=analizar_keywords(df)
        exportar_a_txt(resultados)
  # Si se pasan palabras clave para comparar
        if args.compare:
            lista_keywords = [kw.strip() for kw in args.compare.split(",")]
            comparar_keywords(resultados, lista_keywords)
            graficar_keywords(df, lista_keywords)
        # Si no se pasan, se analiza todo individualmente
        else:
            print("\n📈 Análisis individual:")
            comparar_keywords(resultados, list(df.columns[1:]))
    except Exception as e:
        print(f"Error al procesar el archivo CSV: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
