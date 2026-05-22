from src.core import get_regulator_type, build_regulon
from src.filter import filter_by_min_genes, filter_by_type, filter_interactions_by_regulon  

def test_filter_by_min_genes_keep_only_regulators_with_enough_genes():
    # Esta prueba verifica que solo permanezan los reguladores que tiene
    # al menos el numero minimo de genes que se indican
     interactions = [
        ("CRP", "lacZ", "+"),
        ("CRP", "araB", "+"),
        ("FNR", "narG", "-"),
    ]
     regulon = {
        "CRP": {
            "genes": ["lacZ", "araB"],
            "activados": 2,
            "reprimidos": 0,
        },
        "FNR": {
            "genes": ["narG"],
            "activados": 0,
            "reprimidos": 1,
        }
    }
     filtered_regulon = filter_by_min_genes(
        regulon,
        min_genes=2
    )
     assert "CRP" in filtered_regulon
     assert "FNR" not in filtered_regulon
     assert len(filtered_regulon) == 1
     filtered_interactions = filter_interactions_by_regulon(
        interactions,
        filtered_regulon
    )
     expected = [
        ("CRP", "lacZ", "+"),
        ("CRP", "araB", "+"),
    ]
     assert filtered_interactions == expected

def test_filter_by_type_activador():
    # Esta prueba verifica que solo permanezcan los reguladores que son
    # activadores
   interactions = [
        ("CRP", "lacZ", "+"),
        ("CRP", "araB", "+"),
        ("RpsD", "rplQ", "-"),
        ("CsrA", "ytiC", "+"),
        ("CsrA", "ymdA", "-"),
    ]
   regulon = {
        "CRP": {
            "genes": ["lacZ", "araB"],
            "activados": 2,
            "reprimidos": 0,
        },
        "RpsD": {
            "genes": ["rplQ"],
            "activados": 0,
            "reprimidos": 1,
        },
        "CsrA": {
            "genes": ["ytiC", "ymdA"],
            "activados": 1,
            "reprimidos": 1,
        }
    }
   filtered_regulon = filter_by_type(regulon, "activador")
   assert "CRP" in filtered_regulon
   assert "RpsD" not in filtered_regulon
   assert "CsrA" not in filtered_regulon
   filtered_interactions = filter_interactions_by_regulon(
        interactions,
        filtered_regulon
    )
   expected = [
        ("CRP", "lacZ", "+"),
        ("CRP", "araB", "+"),
    ]
   assert filtered_interactions == expected

def test_filter_by_type_represor():
    # Esta prueba verifica que solo permanezcan los reguladores que son
    # represores
    interactions = [
        ("CRP", "lacZ", "+"),
        ("RpsD", "rplQ", "-"),
        ("CsrA", "ytiC", "+"),
    ]

    regulon = {
        "CRP": {
            "genes": ["lacZ"],
            "activados": 1,
            "reprimidos": 0,
        },
        "RpsD": {
            "genes": ["rplQ"],
            "activados": 0,
            "reprimidos": 1,
        },
        "CsrA": {
            "genes": ["ytiC"],
            "activados": 1,
            "reprimidos": 1,
        }
    }

    filtered_regulon = filter_by_type(regulon, "represor")

    assert "CRP" not in filtered_regulon
    assert "RpsD" in filtered_regulon
    assert "CsrA" not in filtered_regulon

    filtered_interactions = filter_interactions_by_regulon(
        interactions,
        filtered_regulon
    )

    expected = [
        ("RpsD", "rplQ", "-"),
    ]

    assert filtered_interactions == expected

def test_filter_by_type_dual():
    # Esta prueba verifica que solo permanezcan los reguladores que son duales
    interactions = [
        ("CRP", "lacZ", "+"),
        ("RpsD", "rplQ", "-"),
        ("CsrA", "ytiC", "+"),
        ("CsrA", "ymdA", "-"),
    ]

    regulon = {
        "CRP": {
            "genes": ["lacZ"],
            "activados": 1,
            "reprimidos": 0,
        },
        "RpsD": {
            "genes": ["rplQ"],
            "activados": 0,
            "reprimidos": 1,
        },
        "CsrA": {
            "genes": ["ytiC", "ymdA"],
            "activados": 1,
            "reprimidos": 1,
        }
    }

    filtered_regulon = filter_by_type(regulon, "dual")

    assert "CRP" not in filtered_regulon
    assert "RpsD" not in filtered_regulon
    assert "CsrA" in filtered_regulon

    filtered_interactions = filter_interactions_by_regulon(
        interactions,
        filtered_regulon
    )

    expected = [
        ("CsrA", "ytiC", "+"),
        ("CsrA", "ymdA", "-"),
    ]

    assert filtered_interactions == expected

def test_filter_by_type_none():
    # Esta prueba verifica que si se indica None como tipo, no se filtre nada 
    # pero se mantenga la misma estructura de datos
    regulon = {
        "CRP": {
            "genes": ["lacZ", "araB"],
            "activados": 2,
            "reprimidos": 0,
        },
        "RpsD": {
            "genes": ["rplQ"],
            "activados": 0,
            "reprimidos": 1,
        },
        "CsrA": {
            "genes": ["ytiC", "ymdA"],
            "activados": 1,
            "reprimidos": 1,
        }
    }
    filtered = filter_by_type(regulon, None)
    assert "CRP" in filtered
    assert "RpsD" in filtered
    assert "CsrA" in filtered
    assert len(filtered) == 3


def test_filter_interactions_by_regulon_keeps_only_filtered_tfs():
    #Verifica que solo se mantengan interacciones cuyos TFs estén presentes 
    #en el regulon filtrado.
    interactions = [
        ("CRP", "lacZ", "+"),
        ("CRP", "araB", "+"),
        ("RpsD", "rplQ", "-"),
        ("CsrA", "ytiC", "+"),
    ]
    filtered_regulon = {
        "CRP": {
            "genes": ["lacZ", "araB"],
            "activados": 2,
            "reprimidos": 0,
        },
        "CsrA": {
            "genes": ["ytiC"],
            "activados": 1,
            "reprimidos": 0,
        }
    }
    filtered = filter_interactions_by_regulon(interactions,filtered_regulon)
    expected = [
        ("CRP", "lacZ", "+"),
        ("CRP", "araB", "+"),
        ("CsrA", "ytiC", "+"),
    ]

    assert filtered == expected
    assert ("RpsD", "rplQ", "-") not in filtered
    assert len(filtered) == 3