import os
import argparse

from filter import filter_by_min_genes, filter_by_type, filter_interactions_by_regulon
from core import build_regulon
from exporters import write_summary, write_sif
from io_utils import load_interactions
from cli import parse_arguments

# =========================================
# Responsabilidad: Leer el archivo de interacciones y construir una estructura de datos que contenga la información relevante para cada TF.
# Entrada: Archivo TSV con interacciones entre reguladores y genes.
# Salida: lista de interacciones (TF, gen, efecto).
# =========================================
# =========================================
# Responsabilidad: Construir una estructura de datos que resuma la información de cada TF.
# Entrada: lista de interacciones (TF, gen, efecto).
# Salida: diccionario con clave TF y valores que contienen genes únicos y conteos de activación/represión.
# =========================================


def main():
    """Función principal del programa."""

    args = parse_arguments()
    input_file = args.input_file
    output_file = args.output_file
    min_genes = args.min_genes
    regulator_type = args.type
    output_format = args.format

    if min_genes < 0:
        print("Error: min_genes debe ser mayor o igual a 0.")
        exit(1)

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

    if not interactions:
        print("Advertencia: no se encontraron interacciones válidas.")

    regulon = build_regulon(interactions)
    regulon = filter_by_min_genes(regulon, min_genes)
    regulon = filter_by_type(regulon, regulator_type)

    if not regulon:
        print("Advertencia: no hay reguladores que cumplan el filtro.")

    try:
        if output_format == "summary":
            write_summary(regulon, output_file)
        else:
            filtered_interactions = filter_interactions_by_regulon(
                interactions, regulon
            )
            write_sif(filtered_interactions, output_file)
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
