import pytest
from src.io_utils import load_interactions

def test_load_interactions_ignores_invalid_lines(tmp_path):
    # Esta prueba verifica que se load_interactions solo conserve 
    # interacciones validas desde un archivo TSV temporal 

    input_file = tmp_path / "interactions.tsv"
    input_file.write_text(
         "# comentario\n"
         "1)regulatorId\tregulatorName\tX\tX\tgeneName\teffect\tX\n"
         "id1\tCRP\tX\tX\tlacZ\t+\tX\n"
         "id2\tFNR\tX\tX\tnarG\t-\tX\n"
         "id3\tBAD\tX\tX\tgeneX\t?\tX\n"
    )
    interactions = load_interactions(input_file)
    assert interactions == [
        ("CRP", "lacZ", "+"),
        ("FNR", "narG", "-"),
    ]

def test_load_interactions_ignores_empty_lines(tmp_path):
    """
    Verifica que las líneas vacías sean ignoradas.
    """

    input_file = tmp_path / "interactions.tsv"

    input_file.write_text(
        "\n"
        "# comentario\n"
        "\n"
        "id1\tCRP\tX\tX\tlacZ\t+\tX\n"
        "\n"
    )

    interactions = load_interactions(input_file)

    assert interactions == [
        ("CRP", "lacZ", "+")
    ]

def test_load_interactions_keeps_dual_effect(tmp_path):
    # Verifica que las interacciones con efecto '-+'
    # sean conservadas.

    input_file = tmp_path / "interactions.tsv"

    input_file.write_text(
        "id1\tArcA\tX\tX\taraB\t-+\tX\n"
    )

    interactions = load_interactions(input_file)

    assert ("ArcA", "araB", "-+") in interactions

def test_load_interactions_ignores_short_lines(tmp_path):
    """
    Verifica que líneas con pocas columnas sean ignoradas.
    """

    input_file = tmp_path / "interactions.tsv"

    input_file.write_text(
        "id1\tCRP\tX\n"
        "id2\tFNR\tX\tX\tnarG\t-\tX\n"
    )

    interactions = load_interactions(input_file)

    assert interactions == [
        ("FNR", "narG", "-")
    ]
