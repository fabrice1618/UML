import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path

class DrawIOBuilder:
    def __init__(self):
        self.mxfile = ET.Element("mxfile", attrib={"host": "app.diagrams.net"})
        self.id_counter = 2  # 0=root, 1=layer reserved
        self.page_index = 0

    def _next_id(self) -> str:
        self.id_counter += 1
        return str(self.id_counter)

    def _pretty_xml(self, elem: ET.Element) -> str:
        rough = ET.tostring(elem, encoding="utf-8")
        return minidom.parseString(rough).toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")

    def add_page(self, name: str):
        self.page_index += 1
        diagram = ET.SubElement(self.mxfile, "diagram", attrib={"name": f"{self.page_index:02d} - {name}"})
        model = ET.SubElement(diagram, "mxGraphModel", attrib={
            "dx": "1600", "dy": "900", "grid": "1", "gridSize": "10",
            "page": "1", "pageWidth": "1600", "pageHeight": "900", "math": "0", "background": "#ffffff"
        })
        root = ET.SubElement(model, "root")
        # Root + Layer
        ET.SubElement(root, "mxCell", attrib={"id": "0"})
        ET.SubElement(root, "mxCell", attrib={"id": "1", "parent": "0"})
        return root

    def add_vertex(self, root, x, y, w, h, label, style):
        vid = self._next_id()
        cell = ET.SubElement(root, "mxCell", attrib={
            "id": vid, "value": label, "style": style, "vertex": "1", "parent": "1"
        })
        geo = ET.SubElement(cell, "mxGeometry", attrib={"x": str(x), "y": str(y), "width": str(w), "height": str(h)})
        geo.set("as", "geometry")
        return vid

    def add_edge(self, root, source_id, target_id, label="", style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=block;endFill=1;"):
        eid = self._next_id()
        cell = ET.SubElement(root, "mxCell", attrib={
            "id": eid, "value": label, "style": style, "edge": "1", "parent": "1", "source": source_id, "target": target_id
        })
        geo = ET.SubElement(cell, "mxGeometry", attrib={"relative": "1"})
        geo.set("as", "geometry")
        return eid

    def save(self, path: str):
        xml = self._pretty_xml(self.mxfile)
        Path(path).write_text(xml, encoding="utf-8")
        return path

def build_pages():
    d = DrawIOBuilder()

    # Common styles
    style_action = "shape=rect;rounded=1;whiteSpace=wrap;html=1;fillColor=#e3f2fd;strokeColor=#1565c0;"
    style_object = "shape=rect;rounded=1;whiteSpace=wrap;html=1;fillColor=#fffde7;strokeColor=#f9a825;"
    style_start = "shape=ellipse;whiteSpace=wrap;html=1;fillColor=#111111;strokeColor=#111111;"
    style_flow_final = "shape=ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#c62828;strokeWidth=2;"
    style_final_inner = "shape=ellipse;whiteSpace=wrap;html=1;fillColor=#c62828;strokeColor=#c62828;"
    style_decision = "shape=rhombus;whiteSpace=wrap;html=1;fillColor=#f3e5f5;strokeColor=#6a1b9a;"
    style_merge = "shape=rhombus;whiteSpace=wrap;html=1;fillColor=#ede7f6;strokeColor=#4527a0;dashed=1;"
    style_bar = "shape=rect;rounded=0;whiteSpace=wrap;html=1;fillColor=#212121;strokeColor=#212121;"
    style_swimlane = "swimlane;strokeColor=#616161;fontStyle=1;align=center;horizontal=1;startSize=26;"
    style_interruptible = "shape=rect;rounded=1;dashed=1;dashPattern=8 4;strokeColor=#ef6c00;fillColor=#fff3e0;"
    style_signal = "shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;fillColor=#e8f5e9;strokeColor=#2e7d32;"
    style_note = "shape=note;whiteSpace=wrap;html=1;fillColor=#fffde7;strokeColor=#f9a825;"

    # 01 - Éléments de base (Start, Action, Activity Final, Flow Final, Control Flow, Decision, Merge, Garde)
    root = d.add_page("Éléments de base — DAB Retrait")
    start = d.add_vertex(root, 80, 120, 30, 30, "", style_start)

    a_insert = d.add_vertex(root, 150, 110, 180, 50, "Insérer la carte", style_action)
    a_pin = d.add_vertex(root, 380, 110, 200, 50, "Saisir le code PIN", style_action)
    dec_pin = d.add_vertex(root, 620, 110, 120, 60, "PIN valide ?", style_decision)
    a_menu = d.add_vertex(root, 800, 110, 220, 50, "Afficher le menu", style_action)
    act_final = d.add_vertex(root, 1080, 110, 36, 36, "", style_flow_final)
    # Activity Final (bullseye) = outer ellipse + inner filled
    act_final_inner = d.add_vertex(root, 1088, 118, 20, 20, "", style_final_inner)

    # Flow Final (cercle avec croix)
    flow_final = d.add_vertex(root, 680, 260, 36, 36, "", "shape=ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#1565c0;strokeWidth=2;")
    # Add cross for Flow Final via two thin rectangles
    ff_bar1 = d.add_vertex(root, 696, 260+18-2, 24, 4, "", "shape=line;strokeWidth=3;strokeColor=#1565c0;")
    ff_bar2 = d.add_vertex(root, 696, 260+18-2, 24, 4, "", "shape=line;strokeWidth=3;strokeColor=#1565c0;rotation=90;")

    # Decision alternate path and Merge
    a_retry = d.add_vertex(root, 500, 260, 200, 50, "Afficher erreur PIN", style_action)
    merge = d.add_vertex(root, 950, 190, 120, 60, "Continuer", style_merge)

    # Edges and guards
    d.add_edge(root, start, a_insert, "")
    d.add_edge(root, a_insert, a_pin, "")
    d.add_edge(root, a_pin, dec_pin, "")
    e_ok = d.add_edge(root, dec_pin, a_menu, "[valide]")
    e_bad = d.add_edge(root, dec_pin, a_retry, "[invalide]")
    # from retry to Flow Final (ends only that flow)
    d.add_edge(root, a_retry, flow_final, "", "endArrow=oval;endFill=0;strokeColor=#1565c0;")
    # Merge: menu -> merge -> Activity Final
    d.add_edge(root, a_menu, merge, "")
    d.add_edge(root, merge, act_final, "")

    # helpful note
    d.add_vertex(root, 70, 50, 360, 40, "Exemple: transitions avec gardes [valide]/[invalide]", style_note)

    # 02 - Parallélisme — Fork & Join
    root = d.add_page("Parallélisme — Comptes et Journal")
    start2 = d.add_vertex(root, 80, 120, 30, 30, "", style_start)
    a_sel = d.add_vertex(root, 140, 105, 240, 50, "Choisir ‘Retrait’", style_action)
    fork = d.add_vertex(root, 410, 120, 160, 8, "", style_bar)  # 1→n
    a_verif = d.add_vertex(root, 620, 60, 260, 50, "Vérifier solde (banque)", style_action)
    a_journal = d.add_vertex(root, 620, 160, 260, 50, "Écrire entrée journal", style_action)
    join = d.add_vertex(root, 920, 120, 160, 8, "", style_bar)  # n→1
    a_disp = d.add_vertex(root, 1110, 105, 260, 50, "Afficher confirmation", style_action)
    final2 = d.add_vertex(root, 1410, 110, 36, 36, "", style_flow_final)
    final2_inner = d.add_vertex(root, 1418, 118, 20, 20, "", style_final_inner)

    d.add_edge(root, start2, a_sel)
    d.add_edge(root, a_sel, fork)
    d.add_edge(root, fork, a_verif)
    d.add_edge(root, fork, a_journal)
    d.add_edge(root, a_verif, join)
    d.add_edge(root, a_journal, join)
    d.add_edge(root, join, a_disp)
    d.add_edge(root, a_disp, final2)

    # 03 - Flux d’objet — Objet billet et reçu
    root = d.add_page("Flux d’objet — Billets & Reçu")
    start3 = d.add_vertex(root, 80, 140, 30, 30, "", style_start)
    a_calc = d.add_vertex(root, 140, 125, 260, 50, "Calculer la répartition des billets", style_action)
    obj_billets = d.add_vertex(root, 450, 100, 200, 60, "Obj: LotBillets", style_object)
    a_dispense = d.add_vertex(root, 700, 125, 260, 50, "Distribuer les billets", style_action)
    obj_recu = d.add_vertex(root, 700, 230, 220, 50, "Obj: ReçuPDF", style_object)
    a_impr = d.add_vertex(root, 980, 225, 240, 50, "Imprimer le reçu", style_action)
    final3 = d.add_vertex(root, 1260, 130, 36, 36, "", style_flow_final)
    final3_inner = d.add_vertex(root, 1268, 138, 20, 20, "", style_final_inner)

    d.add_edge(root, start3, a_calc)
    # Object Flow (blue dashed with stereotype label)
    d.add_edge(root, a_calc, obj_billets, "«objectFlow»", "dashed=1;strokeColor=#1e88e5;endArrow=block;endFill=1;")
    d.add_edge(root, obj_billets, a_dispense, "«objectFlow»", "dashed=1;strokeColor=#1e88e5;endArrow=block;endFill=1;")
    d.add_edge(root, a_dispense, final3)
    d.add_edge(root, a_dispense, obj_recu, "«objectFlow»", "dashed=1;strokeColor=#1e88e5;endArrow=block;endFill=1;")
    d.add_edge(root, obj_recu, a_impr, "«objectFlow»", "dashed=1;strokeColor=#1e88e5;endArrow=block;endFill=1;")

    # 04 - Partitions (Swimlanes) — Client / DAB / Banque
    root = d.add_page("Partitions — Client / DAB / Banque")
    lane_client = d.add_vertex(root, 40, 60, 450, 700, "Client", style_swimlane)
    lane_dab = d.add_vertex(root, 520, 60, 500, 700, "DAB", style_swimlane)
    lane_banque = d.add_vertex(root, 1040, 60, 500, 700, "Banque", style_swimlane)

    # Elements in lanes (parent set to layer; swimlanes are just background shapes)
    s4 = d.add_vertex(root, 80, 140, 30, 30, "", style_start)
    a_cli = d.add_vertex(root, 120, 125, 360, 50, "Composer le PIN", style_action)
    a_dab = d.add_vertex(root, 560, 125, 420, 50, "Vérifier PIN", style_action)
    a_bnk = d.add_vertex(root, 1080, 125, 420, 50, "Autoriser l’opération", style_action)
    f4 = d.add_vertex(root, 1530, 130, 36, 36, "", style_flow_final)
    f4i = d.add_vertex(root, 1538, 138, 20, 20, "", style_final_inner)

    d.add_edge(root, s4, a_cli)
    d.add_edge(root, a_cli, a_dab, "")
    d.add_edge(root, a_dab, a_bnk, "")
    d.add_edge(root, a_bnk, f4, "")

    # 05 - Interruption/Exception — Carte avalée
    root = d.add_page("Interruption — Carte avalée")
    region = d.add_vertex(root, 120, 80, 1000, 420, "Région interruptible", style_interruptible)
    s5 = d.add_vertex(root, 160, 140, 30, 30, "", style_start)
    a_lire = d.add_vertex(root, 210, 125, 260, 50, "Lire la carte", style_action)
    a_sess = d.add_vertex(root, 500, 125, 260, 50, "Démarrer session", style_action)
    a_attente = d.add_vertex(root, 800, 125, 260, 50, "Attendre saisie PIN", style_action)
    exc = d.add_vertex(root, 520, 280, 260, 50, "«exception» Carte retenue", style_action)
    final5 = d.add_vertex(root, 900, 280, 36, 36, "", style_flow_final)
    final5i = d.add_vertex(root, 908, 288, 20, 20, "", style_final_inner)

    d.add_edge(root, s5, a_lire)
    d.add_edge(root, a_lire, a_sess)
    d.add_edge(root, a_sess, a_attente)
    # Exception flow (red with open arrow)
    d.add_edge(root, a_attente, exc, "", "strokeColor=#d32f2f;endArrow=block;endFill=0;dashed=1;")
    d.add_edge(root, exc, final5, "", "strokeColor=#d32f2f;endArrow=block;endFill=1;")

    # 06 - Signal/Événement — Maintenance à distance
    root = d.add_page("Signal/Événement — Maintenance")
    s6 = d.add_vertex(root, 80, 140, 30, 30, "", style_start)
    a_idle = d.add_vertex(root, 140, 125, 260, 50, "Attendre client", style_action)
    sig_recv = d.add_vertex(root, 470, 80, 220, 50, "«receiveSignal»\nSignal: ModeMaintenance", style_signal)
    sig_send = d.add_vertex(root, 470, 220, 220, 50, "«sendSignal»\nSignal: AlerteGuichet", style_signal)
    a_switch = d.add_vertex(root, 740, 125, 280, 50, "Basculer en mode maintenance", style_action)
    fin6 = d.add_vertex(root, 1060, 130, 36, 36, "", style_flow_final)
    fin6i = d.add_vertex(root, 1068, 138, 20, 20, "", style_final_inner)

    d.add_edge(root, s6, a_idle)
    d.add_edge(root, a_idle, sig_recv, "", "strokeColor=#2e7d32;endArrow=block;endFill=1;dashed=1;")
    d.add_edge(root, sig_recv, a_switch, "", "strokeColor=#2e7d32;endArrow=block;endFill=1;")
    d.add_edge(root, a_switch, fin6, "")
    # optional outgoing signal
    d.add_edge(root, a_idle, sig_send, "", "strokeColor=#2e7d32;endArrow=block;endFill=1;dashed=1;")

    # 07 - Sous-activité (Call Behavior Action) — Vérifier identité
    root = d.add_page("Sous-activité — Appel d’activité")
    s7 = d.add_vertex(root, 80, 140, 30, 30, "", style_start)
    a_main = d.add_vertex(root, 140, 125, 300, 60, "Vérifier identité\n«callBehavior»", style_action + "strokeWidth=2;")
    # Visual cue: small triangle marker (simulate with tiny rotated rectangle)
    marker = d.add_vertex(root, 410, 150, 14, 14, "", "shape=triangle;direction=east;fillColor=#1565c0;strokeColor=#1565c0;")
    a_sub = d.add_vertex(root, 500, 120, 320, 60, "Activité appelée: Vérification KYC", style_action)
    fin7 = d.add_vertex(root, 860, 130, 36, 36, "", style_flow_final)
    fin7i = d.add_vertex(root, 868, 138, 20, 20, "", style_final_inner)

    d.add_edge(root, s7, a_main)
    d.add_edge(root, a_main, a_sub)
    d.add_edge(root, a_sub, fin7)

    out_path = "atm_activity_examples.drawio"
    d.save(out_path)
    return out_path

if __name__ == "__main__":
    path = build_pages()
    print(f"Fichier .drawio généré: {path}")

