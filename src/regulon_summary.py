import os
import argparse


# =========================================
# Responsabilidad: Leer el archivo de interacciones y construir una estructura de datos que contenga la información relevante para cada TF.
# Entrada: Archivo TSV con interacciones entre reguladores y genes.
# Salida: lista de interacciones (TF, gen, efecto).
# =========================================
def load_interactions(filename):
    """
    Carga las interacciones desde un archivo TSV.

    Args:
        filename (str): Ruta del archivo de interacciones.

    Returns:
        list[tuple[str, str, str]]: Lista de interacciones (TF, gen, efecto).
    """
    interactions = []

    if not filename:
        raise ValueError("filename vacío")

    with open(filename) as f:
        for line in f:

            line = line.strip()

            # Ignorar líneas vacías
            if not line:
                continue

            # Ignorar comentarios
            if line.startswith("#"):
                continue

            # Ignorar encabezado
            if line.startswith("1)regulatorId"):
                continue

            fields = line.split("\t")

            # Validar número mínimo de columnas
            if len(fields) <= 6:
                continue

            TF = fields[1]
            gene = fields[4]
            effect = fields[5]

            # Validar effect
            if effect not in ["+", "-", "+-"]:
                continue

            interactions.append((TF, gene, effect))

    return interactions


# =========================================
# Responsabilidad: Construir una estructura de datos que resuma la información de cada TF, incluyendo el número total de genes regulados únicos, genes activados únicos, genes reprimidos únicos y la lista de genes regulados.
# Entrada: lista de interacciones (TF, gen, efecto).
# Salida: diccionario con clave TF y valores
# =========================================
def build_regulon(interactions):
    """Construye una estructura de datos que resume la información de cada TF.

    Args:
        interactions (list[tuple[str, str, str]]): Lista de interacciones (TF, gen, efecto).

    Returns:
        dict: Diccionario con clave TF y valores que contienen conjuntos de genes únicos,
            genes activados únicos y genes reprimidos únicos.
    """
    regulon = {}

    for TF, gene, effect in interactions:

        # Inicializar estructura si el TF no existe
        if TF not in regulon:
            regulon[TF] = {"genes": [], "activados": 0, "reprimidos": 0}

        # Agregar gen a los conjuntos para evitar duplicados
        regulon[TF]["genes"].append(gene)

        # Contar tipo de regulación
        if effect == "+":
            regulon[TF]["activados"] += 1
        elif effect == "-":
            regulon[TF]["reprimidos"] += 1
        elif effect == "+-":
            regulon[TF]["activados"] += 1
            regulon[TF]["reprimidos"] += 1

    return regulon


# =========================================
# Responsabilidad: Generar un archivo de salida que resuma la información de cada TF, incluyendo el número total de genes regulados únicos, el número de genes activados únicos, el número de genes reprimidos únicos, el tipo de regulación (activador, represor o dual) y la lista de genes regulados.
# Entrada: diccionario con clave TF y valores
# Salida: archivo TSV con resumen de reguladores
# =========================================
def write_summary(regulon, output_file):
    """Escribe el resumen del regulon a un archivo TSV.

    Args:
        regulon (dict): Diccionario con información del regulon.
        output_file (str): Ruta del archivo de salida.

    Notes:
        Calcula los totales de activados y reprimidos a partir de conjuntos de genes únicos.
    """

    if not output_file:
        raise ValueError("output_file vacío")

    if regulon is None:
        raise ValueError("regulon no puede ser None")

    dirpath = os.path.dirname(output_file)

    if dirpath:
        os.makedirs(dirpath, exist_ok=True)

    with open(output_file, "w") as out:
        out.write("TF\tTotal genes\tActivados\tReprimidos\tTipo\tLista de genes\n")

        for TF in sorted(regulon):

            # Obtener datos
            genes = sorted(regulon[TF]["genes"])
            total = len(genes)
            activados = regulon[TF]["activados"]
            reprimidos = regulon[TF]["reprimidos"]

            # Determinar tipo de regulación
            if activados > 0 and reprimidos > 0:
                tipo = "dual"
            elif activados > 0:
                tipo = "activador"
            else:
                tipo = "represor"

            lista_genes = ", ".join(genes)
            out.write(
                f"{TF}\t{total}\t{activados}\t{reprimidos}\t{tipo}\t{lista_genes}\n"
            )


# =========================================
# Lectura de argumentos
# =========================================
def parse_arguments():
    """Define y lee los argumentos de línea de comandos."""

    parser = argparse.ArgumentParser(
        description="Genera un resumen de regulones a partir de un archivo TSV"
    )

    # Argumentos obligatorios (posicionales)
    parser.add_argument("input_file", help="Archivo de entrada con interacciones")

    parser.add_argument("output_file", help="Archivo de salida para el resumen")

    # Argumento opcional
    parser.add_argument(
        "--min_genes",
        type=int,
        default=0,
        help="Filtrar TFs con al menos este número de genes",
    )

    return parser.parse_args()


# =========================================
# Main
# =========================================
def main():
    """Función principal del programa."""

    # =========================================
    # 1. Lectura de argumentos
    # =========================================
    args = parse_arguments()

    input_file = args.input_file
    output_file = args.output_file
    min_genes = args.min_genes

    # =========================================
    # 2. Validación de argumentos (errores predecibles)
    # =========================================
    if min_genes < 0:
        print("Error: min_genes debe ser mayor o igual a 0.")
        exit(1)

    # =========================================
    # 3. Lectura de datos (puede fallar → try/except)
    # =========================================
    try:
        interactions = load_interactions(input_file)

    except FileNotFoundError:
        print(f"Error: no existe el archivo de entrada -> {input_file}")
        exit(1)

    except PermissionError:
        print(f"Error: no hay permisos para leer el archivo -> {input_file}")
        exit(1)

    except OSError as e:
        print(f"Error al leer el archivo ({input_file}): {e}")
        exit(1)

    # =========================================
    # 4. Validación de contenido (no error crítico)
    # =========================================
    if not interactions:
        print("Advertencia: no se encontraron interacciones válidas.")

    # =========================================
    # 5. Construcción del regulon
    # =========================================
    regulon = build_regulon(interactions)

    # =========================================
    # 6. Filtrado por número de genes
    # =========================================
    nuevo_regulon = {}

    for TF, data in regulon.items():
        num_genes = len(data["genes"])

        if num_genes >= min_genes:
            nuevo_regulon[TF] = data

    regulon = nuevo_regulon

    # =========================================
    # 7. Resultado vacío (caso válido)
    # =========================================
    if not regulon:
        print("Advertencia: no hay reguladores que cumplan el filtro.")

    # =========================================
    # 8. Escritura de resultados (puede fallar)
    # =========================================
    try:
        write_summary(regulon, output_file)

    except PermissionError:
        print(f"Error: no hay permisos para escribir -> {output_file}")
        exit(1)

    except IsADirectoryError:
        print(f"Error: la ruta de salida es un directorio -> {output_file}")
        exit(1)

    except OSError as e:
        print(f"Error al escribir el archivo ({output_file}): {e}")
        exit(1)


if __name__ == "__main__":
    main()
