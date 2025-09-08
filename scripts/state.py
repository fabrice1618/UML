import xml.etree.ElementTree as ET
from datetime import datetime

def mxcell(parent, id_, value="", style="", vertex=False, edge=False, parent_id="1", x=None, y=None, w=None, h=None, source=None, target=None):
    cell = ET.SubElement(parent, "mxCell", id=id_)
    if value:
        cell.set("value", value)
    if style:
        cell.set("style", style)
    if vertex:
        cell.set("vertex", "1")
    if edge:
        cell.set("edge", "1")
    if parent_id:
        cell.set("parent", parent_id)
    if source:
        cell.set("source", source)
    if target:
        cell.set("target", target)
    geom = ET.SubElement(cell, "mxGeometry", as_="geometry")
    if edge:
        geom.set("relative", "1")
    if x is not None:
        geom.set("x", str(x))
    if y is not None:
        geom.set("y", str(y))
    if w is not None:
        geom.set("width", str(w))
    if h is not None:
        geom.set("height", str(h))
    return cell

def build_drawio():
    # Root mxfile
    mxfile = ET.Element(
        "mxfile",
        host="app.diagrams.net",
        modified=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        agent="python-xml",
        version="20.8.16",
        type="device",
    )
    diagram = ET.SubElement(mxfile, "diagram", id="atm-state-1", name="ATM - États (exemple)")
    model = ET.SubElement(
        diagram,
        "mxGraphModel",
        dx="1280",
        dy="720",
        grid="1",
        gridSize="10",
        guides="1",
        tooltips="1",
        connect="1",
        arrows="1",
        fold="1",
        page="1",
        pageScale="1",
        pageWidth="1600",
        pageHeight="1000",
        math="0",
        shadow="0",
    )
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")

    # Common styles
    state_style = "rounded=1;whiteSpace=wrap;html=1;labelPosition=center;verticalLabelPosition=middle;align=center;verticalAlign=middle;strokeColor=#1a1a1a;fillColor=#ffffff;spacing=4;"
    composite_style = state_style + "container=1;recursiveResize=0;"
    edge_style = "endArrow=block;endFill=1;html=1;rounded=1;strokeColor=#1a1a1a;labelBackgroundColor=#ffffff;"
    initial_style = "shape=ellipse;perimeter=ellipsePerimeter;html=1;fillColor=#000000;strokeColor=#000000;"
    final_style = "shape=doubleEllipse;perimeter=ellipsePerimeter;html=1;fillColor=#ffffff;strokeColor=#000000;"

    # Initial [*]
    ini = mxcell(root, "ini", style=initial_style, vertex=True, x=60, y=60, w=18, h=18)

    # States (top-level)
    attente_carte = mxcell(root, "AttenteCarte", value="AttenteCarte", style=state_style, vertex=True, x=120, y=50, w=140, h=60)
    lecture_carte = mxcell(root, "LectureCarte", value="LectureCarte", style=state_style, vertex=True, x=340, y=50, w=160, h=60)
    fin_session = mxcell(root, "FinSession", value="", style=final_style, vertex=True, x=1180, y=420, w=26, h=26)

    # Composite: AttentePIN
    attente_pin = mxcell(root, "AttentePIN", value="AttentePIN", style=composite_style, vertex=True, x=560, y=30, w=340, h=200)

    # Inside AttentePIN
    pin_init = mxcell(root, "PIN_init", style=initial_style, vertex=True, parent_id="AttentePIN", x=15, y=18, w=14, h=14)
    pin_saisie = mxcell(root, "Saisie", value="Saisie", style=state_style, vertex=True, parent_id="AttentePIN", x=50, y=10, w=120, h=50)
    pin_auth = mxcell(root, "Authentifie", value="Authentifié", style=state_style, vertex=True, parent_id="AttentePIN", x=220, y=10, w=110, h=50)
    pin_ret = mxcell(root, "RetenirCarte", value="RetenirCarte", style=state_style, vertex=True, parent_id="AttentePIN", x=180, y=90, w=150, h=50)

    # Other top-level states
    authentifie = mxcell(root, "AuthTop", value="Authentifié", style=state_style, vertex=True, x=940, y=40, w=130, h=60)
    selection_op = mxcell(root, "SelectionOp", value="SélectionOp", style=state_style, vertex=True, x=1120, y=40, w=140, h=60)

    # Composite: RetraitEnCours
    retrait = mxcell(root, "RetraitEnCours", value="RetraitEnCours", style=composite_style, vertex=True, x=1120, y=140, w=260, h=160)
    ret_init = mxcell(root, "Ret_init", style=initial_style, vertex=True, parent_id="RetraitEnCours", x=16, y=22, w=14, h=14)
    ret_prelever = mxcell(root, "Prelever", value="Prélever", style=state_style, vertex=True, parent_id="RetraitEnCours", x=50, y=10, w=100, h=50)
    ret_final = mxcell(root, "Ret_final", value="", style=final_style, vertex=True, parent_id="RetraitEnCours", x=180, y=16, w=20, h=20)

    # Composite: Transaction (orthogonalité simulée)
    transaction = mxcell(root, "Transaction", value="Transaction", style=composite_style, vertex=True, x=720, y=270, w=350, h=200)
    trans_prep = mxcell(root, "TransPrep", value="Préparation", style=state_style, vertex=True, parent_id="Transaction", x=20, y=20, w=130, h=50)
    trans_impr = mxcell(root, "TransImpr", value="Impression", style=state_style, vertex=True, parent_id="Transaction", x=200, y=20, w=130, h=50)
    trans_note = mxcell(
        root,
        "TransNote",
        value="Préparation et Impression en parallèle (conceptuel)",
        style="shape=note;whiteSpace=wrap;html=1;size=14;fillColor=#fff2a8;strokeColor=#b09500;",
        vertex=True,
        parent_id="Transaction",
        x=20, y=90, w=310, h=70
    )

    # Edges (top-level flow)
    mxcell(root, "e_ini_att", value="", style=edge_style, edge=True, source="ini", target="AttenteCarte", parent_id="1")
    mxcell(root, "e_att_lc", value="carteInsérée / lirePiste()", style=edge_style, edge=True, source="AttenteCarte", target="LectureCarte", parent_id="1")
    mxcell(root, "e_lc_pin", value="carteValide / afficherÉcranPIN()", style=edge_style, edge=True, source="LectureCarte", target="AttentePIN", parent_id="1")
    mxcell(root, "e_lc_fin", value="carteInvalide / éjecterCarte()", style=edge_style, edge=True, source="LectureCarte", target="FinSession", parent_id="1")

    # Edges inside AttentePIN
    mxcell(root, "e_pin_init_saisie", value="", style=edge_style, edge=True, source="PIN_init", target="Saisie", parent_id="AttentePIN")
    mxcell(root, "e_saisie_self", value="pinInvalide / incTentatives()", style=edge_style, edge=True, source="Saisie", target="Saisie", parent_id="AttentePIN")
    mxcell(root, "e_saisie_auth", value="pinValide / resetTentatives()", style=edge_style, edge=True, source="Saisie", target="Authentifie", parent_id="AttentePIN")
    mxcell(root, "e_saisie_ret", value="tentatives&gt;3 / aspirerCarte()", style=edge_style, edge=True, source="Saisie", target="RetenirCarte", parent_id="AttentePIN")

    # Exit from AttentePIN
    mxcell(root, "e_pin_timeout_fin", value="after(30s) / éjecterCarte()", style=edge_style, edge=True, source="AttentePIN", target="FinSession", parent_id="1")

    # From nested Authentifié (inside AttentePIN) to top-level Authentifié (for clarity)
    mxcell(root, "e_authpin_to_auth", value="", style=edge_style, edge=True, source="Authentifie", target="AuthTop", parent_id="1")

    # Authentifié -> SélectionOp
    mxcell(root, "e_auth_sel", value="afficherMenu()", style=edge_style, edge=True, source="AuthTop", target="SelectionOp", parent_id="1")
    # SélectionOp -> RetraitEnCours
    mxcell(root, "e_sel_retrait", value="choisirRetrait(montant)", style=edge_style, edge=True, source="SelectionOp", target="RetraitEnCours", parent_id="1")
    # SélectionOp -> FinSession (annuler)
    mxcell(root, "e_sel_fin", value="annuler / éjecterCarte()", style=edge_style, edge=True, source="SelectionOp", target="FinSession", parent_id="1")

    # Inside RetraitEnCours
    mxcell(root, "e_ret_init_prelever", value="", style=edge_style, edge=True, source="Ret_init", target="Prelever", parent_id="RetraitEnCours")
    mxcell(root, "e_prelever_final", value="aprèsDébit", style=edge_style, edge=True, source="Prelever", target="Ret_final", parent_id="RetraitEnCours")

    # RetraitEnCours -> FinSession
    mxcell(root, "e_retrait_fin", value="billetsRemis / remercierClient()", style=edge_style, edge=True, source="RetraitEnCours", target="FinSession", parent_id="1")

    # Cosmetic separators for readability
    title = mxcell(root, "Title", value="ATM - Diagramme d'États (exemple draw.io)", style="text;whiteSpace=wrap;html=1;align=left;verticalAlign=top;fontSize=18;fontStyle=1;", vertex=True, x=40, y=10, w=520, h=30)

    # Serialize with correct attribute names (mxGeometry needs as="geometry")
    def fix_as_attributes(elem):
        for e in elem.iter():
            if "as_" in e.attrib:
                e.set("as", e.attrib["as_"])
                del e.attrib["as_"]
        return elem

    mxfile = fix_as_attributes(mxfile)
    return mxfile

def save_drawio(filename="atm_state_example.drawio"):
    mxfile = build_drawio()
    ET.indent(mxfile, space="  ", level=0)
    tree = ET.ElementTree(mxfile)
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    return filename

if __name__ == "__main__":
    out = save_drawio()
    print(f"Fichier généré: {out}")
