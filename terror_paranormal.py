import os
import struct

TXT_FILE = "paranormal.txt"
BIN_FILE = "paranormal_stats.bin"

def crear_archivos():
    if not os.path.exists(TXT_FILE):
        with open(TXT_FILE, "w", encoding="utf-8") as f:
            f.write("COLECCIÓN DE CASOS PARANORMALES\n")

    if not os.path.exists(BIN_FILE):
        with open(BIN_FILE, "wb") as f:
            pass

def agregar_caso():
    try:
        nombre = input("Nombre del caso paranormal: ").strip()
        if nombre == "":
            raise ValueError("El nombre no puede estar vacío.")

        tipo = input("Tipo (aparición, poltergeist, objeto poseído, entidad, maldición): ").strip()
        lugar = input("Lugar del suceso: ").strip()
        año = input("Año aproximado: ").strip()

        with open(TXT_FILE, "a", encoding="utf-8") as f:
            f.write(f"{nombre}|{tipo}|{lugar}|{año}\n")

        actividad = input("Nivel de actividad paranormal (1-100): ")

        try:
            actividad = int(actividad)
            if not (1 <= actividad <= 100):
                raise ValueError("El nivel de actividad debe estar entre 1 y 100.")
        except ValueError as e:
            print("Error:", e)
            return

        with open(BIN_FILE, "ab") as bf:
            nombre_bytes = nombre.encode("utf-8")
            bf.write(struct.pack("I", len(nombre_bytes)))
            bf.write(nombre_bytes)
            bf.write(struct.pack("I", actividad))

        print("\nCaso paranormal agregado.\n")

    except Exception as e:
        print("Ocurrió un error al agregar el caso:", e)

def mostrar_casos():
    try:
        with open(TXT_FILE, "r", encoding="utf-8") as f:
            print("\nCASOS PARANORMALES REGISTRADOS\n")
            print(f.read())
    except FileNotFoundError:
        print("ERROR: No existe el archivo de casos.")

def buscar_caso():
    nombre = input("Ingresa el nombre del caso paranormal: ").strip().lower()

    try:
        encontrado = False
        with open(TXT_FILE, "r", encoding="utf-8") as f:
            for linea in f:
                if linea.lower().startswith(nombre):
                    print("\nCaso encontrado:")
                    print(linea)
                    encontrado = True
                    break

        if not encontrado:
            print("No se encontró ningún caso paranormal con ese nombre.")

    except FileNotFoundError:
        print("ERROR: No existe el archivo de casos.")

def mostrar_actividad():
    try:
        with open(BIN_FILE, "rb") as bf:
            print("\nINTENSIDAD DE ACTIVIDAD PARANORMAL\n")
            while True:
                long_bytes = bf.read(4)
                if not long_bytes:
                    break

                longitud = struct.unpack("I", long_bytes)[0]
                nombre = bf.read(longitud).decode("utf-8")
                actividad = struct.unpack("I", bf.read(4))[0]

                print(f"{nombre}: Actividad paranormal {actividad}/100")

    except FileNotFoundError:
        print("ERROR: archivo binario no encontrado.")
    except Exception as e:
        print("Error al leer el archivo binario:", e)
    finally:
        print("\nFin del análisis paranormal.\n")

def menu():
    crear_archivos()

    while True:
        print("\nCOLECCIÓN PARANORMAL")
        print("1. Registrar nuevo caso paranormal")
        print("2. Mostrar todos los casos")
        print("3. Buscar caso por nombre")
        print("4. Mostrar actividad paranormal")
        print("5. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            agregar_caso()
        elif opcion == "2":
            mostrar_casos()
        elif opcion == "3":
            buscar_caso()
        elif opcion == "4":
            mostrar_actividad()
        elif opcion == "5":
            print("\nFin del programa. No mires detrás de ti.")
            break
        else:
            print("Opción inválida. Intenta nuevamente.")

if __name__ == "__main__":
    menu()
