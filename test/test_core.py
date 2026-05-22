from src.core import get_regulator_type, build_regulon


def test_get_regulator_type_returns_activador():

    #ESta prueba verifica que un regulador con genes activados y sin genes reprimidos 
    # se clasifique como "activador"
    data = {"genes": ["lacZ", "araB"], "activados": 2, "reprimidos":0}
    result = get_regulator_type(data)
    assert result == "activador"

def test_get_regulator_type_returns_represor():
    #Esta prueba verifica que un regulador sin genes activados y con genes reprimidos
    #sea clasificado como "represor"
    data = {"genes": ["trpA"], "activados": 0, "reprimidos":1}
    result = get_regulator_type(data)
    assert result == "represor"

def test_get_regulator_type_returns_dual():
    #Esta prueba verifica que un regulador con genes activados y genes reprimidos 
    #sea clasificado como "dual"
    data = {"genes": ["lacZ", "galE"], "activados": 1, "reprimidos":1}
    result = get_regulator_type(data)
    assert result == "dual"

def test_obtener_el_mismo_gen_para_el_mismo_regulador():
    #Esta prueba verifica si un mismo gen aparece 2 o mas veces para el mismo regulador,
    # y se cuente una sola vez en la lista de genes pero que el conteo se haga correctamente

    data = {"genes": ["galE", "galE", "lacZ"], 
            "activados": 2,
            "reprimidos": 2}
    result = get_regulator_type(data)
    assert result == "dual"

def test_build_regulon_ignorando_genes_repetidos():
    #Esta prueba verifica que build_regulon contruya el regulon correctamente 
    # aunque haya interacciones repetidas para el mismo gen y regulador

    interactions = [
        ("LacI", "lacZ", "+"),
        ("LacI", "lacZ", "+"), #Este es el repetido
        ("LacI", "lacY", "-"),
        ("FNR", "narG", "-"),
        ("FNR", "narG", "-") #Este es el repetido
    ]
    regulon = build_regulon(interactions)
    assert set(regulon["LacI"]["genes"]) == {"lacZ", "lacY"}
    assert regulon["LacI"]["activados"] == 2
    assert regulon["LacI"]["reprimidos"] == 1

    assert set(regulon["FNR"]["genes"]) == {"narG"}
    assert regulon["FNR"]["activados"] == 0
    assert regulon["FNR"]["reprimidos"] == 2


##ojo aqui
def test_build_regulon_con_genes_activados_y_reprimidos():
    #Esta prueba verifica que la función build_regulon construya correctamente la estructura de datos
    # para un regulador con genes activados y reprimidos
    interactions = [
        ("LacI", "lacZ", "+"),
        ("LacI", "lacY", "+"),
        ("LacI", "lacA", "-"),
        ("LacI", "galE", "+-")
    ]
    regulon = build_regulon(interactions)
    
    assert "LacI" in regulon
    assert len(regulon["LacI"]["genes"]) == 4
    assert regulon["LacI"]["activados"] == 3
    assert regulon["LacI"]["reprimidos"] == 2

def test_build_regulon_varios_reguladores_un_mismo_gen():
    # Esta prueba verifica que la funcion build_regulon construya correctamente
    # la estructura de datos para varios reguladores que regulan el mismo gen

    interactions = [
        ("LacI", "lacZ", "+"),
        ("FNR", "lacZ", "-"),
        ("CRP", "lacZ", "+")
    ]
    regulon = build_regulon(interactions)

    assert set(regulon["LacI"]["genes"]) == {"lacZ"}
    assert regulon["LacI"]["activados"] == 1
    assert regulon["LacI"]["reprimidos"] == 0

    assert set(regulon["FNR"]["genes"]) == {"lacZ"}
    assert regulon["FNR"]["activados"] == 0
    assert regulon["FNR"]["reprimidos"] == 1

    assert set(regulon["CRP"]["genes"]) == {"lacZ"}
    assert regulon["CRP"]["activados"] == 1
    assert regulon["CRP"]["reprimidos"] == 0
    