from __future__ import annotations

import re
from pathlib import Path

def extract_figure_pages(pdf_path: Path, patterns: dict[str, str]) -> dict[str, int | None]:
    """
    Return a mapping "Figure 9.x" -> page index (0-based) where the label is found,
    or None if not found. Uses PyMuPDF (fitz) if available.
    """
    try:
        import fitz  # PyMuPDF
    except Exception as e:
        print("PyMuPDF (fitz) is required to extract images. Install it if available in this environment.")
        return {k: None for k in patterns.keys()}

    pages = {}
    with fitz.open(pdf_path) as doc:
        for fig_key, regex in patterns.items():
            pages[fig_key] = None
            pat = re.compile(regex, flags=re.IGNORECASE)
            for page_index in range(len(doc)):
                text = doc[page_index].get_text("text")
                if pat.search(text):
                    pages[fig_key] = page_index
                    break
    return pages

def render_pages_as_images(pdf_path: Path, page_map: dict[str, int | None], out_dir: Path, dpi: int = 144) -> dict[str, Path | None]:
    """
    Render each located page to a PNG and return mapping "Figure 9.x" -> image path.
    If a page is None, returns None for that figure. Uses PyMuPDF (fitz).
    """
    try:
        import fitz  # PyMuPDF
    except Exception:
        return {k: None for k in page_map.keys()}

    out_dir.mkdir(parents=True, exist_ok=True)
    images: dict[str, Path | None] = {}
    with fitz.open(pdf_path) as doc:
        # Zoom factor from dpi (default display matrix ~72 dpi)
        zoom = dpi / 72.0
        mat = fitz.Matrix(zoom, zoom)
        for fig_key, page_index in page_map.items():
            if page_index is None or page_index < 0 or page_index >= len(doc):
                images[fig_key] = None
                continue
            page = doc[page_index]
            pix = page.get_pixmap(matrix=mat, alpha=False)
            safe_name = fig_key.lower().replace(" ", "_").replace(".", "_")
            out_path = out_dir / f"{safe_name}.png"
            pix.save(out_path.as_posix())
            images[fig_key] = out_path
    return images

def build_markdown(md_path: Path, figure_images: dict[str, Path | None]) -> None:
    """
    Write the markdown file with a concise introduction to UML based on the supplied PDF excerpts.
    Link the exported images when available.
    """
    sections = [
        {
            "fig": "Figure 9.1",
            "title": "De l’expression des besoins au code",
            "summary": (
                "UML est un langage de modélisation, pas une méthode. Une démarche outillée par UML doit être "
                "pilotée par les cas d’utilisation et centrée sur l’architecture, tout en restant légère. "
                "L’objectif: produire un logiciel utile, de qualité, dans des délais et coûts maîtrisés."
            ),
        },
        {
            "fig": "Figure 9.2",
            "title": "Identification des besoins — Diagrammes de cas d’utilisation",
            "summary": (
                "On délimite le système, on identifie acteurs et cas d’utilisation, puis on priorise selon importance et risque. "
                "Les cas d’utilisation décrivent les besoins des utilisateurs sans considération technique."
            ),
        },
        {
            "fig": "Figure 9.3",
            "title": "Diagrammes de séquence système",
            "summary": (
                "Ils illustrent la description textuelle des cas d’utilisation en montrant les échanges entre acteurs et le système (vu comme une boîte noire). "
                "On modélise au minimum le scénario nominal et, si nécessaire, les variantes majeures."
            ),
        },
        {
            "fig": "Figure 9.4",
            "title": "Maquette de l’IHM",
            "summary": (
                "Une maquette rapide et jetable facilite le dialogue avec les utilisateurs. "
                "Elle peut évoluer pour simuler navigation et enchaînements d’écrans, même si les fonctions sont fictives."
            ),
        },
        {
            "fig": "Figure 9.6",
            "title": "Diagramme de classes participantes",
            "summary": (
                "Pont entre besoins et conception. Il distingue Dialogues (IHM), Contrôles (logique d’application) et Entités (domaine), "
                "et organise leurs relations pour préserver l’indépendance du domaine vis-à-vis de l’interface."
            ),
        },
        {
            "fig": "Figure 9.7",
            "title": "Diagrammes d’activités de navigation",
            "summary": (
                "Ils représentent la navigation IHM (fenêtres, menus, dialogues…). "
                "La modélisation est souvent structurée par acteur et reliée aux classes de dialogue."
            ),
        },
        {
            "fig": "Figure 9.8",
            "title": "Diagrammes d’interaction (conception)",
            "summary": (
                "On alloue précisément les responsabilités aux classes d’analyse via des séquences/communications. "
                "Ces diagrammes matérialisent qui fait quoi dans un scénario et préparent la conception détaillée."
            ),
        },
        {
            "fig": "Figure 9.9",
            "title": "De la boîte noire aux objets en collaboration",
            "summary": (
                "Le ‘système’ des séquences système est remplacé par un ensemble d’objets (Dialogues, Contrôles, Entités) qui collaborent. "
                "Les interactions doivent respecter les associations et leur navigabilité."
            ),
        },
        {
            "fig": "Figure 9.10",
            "title": "Diagramme de classes de conception",
            "summary": (
                "Vue statique destinée à l’implémentation: on complète opérations, visibilités et détails internes des classes. "
                "La première ébauche se raffine en parallèle des diagrammes d’interaction, indépendamment des choix techniques."
            ),
        },
    ]

    lines = []
    lines.append("# Démarche UML — Introduction pratique\n")
    lines.append("_Synthèse libre inspirée du support « UML 2 » de Laurent Audibert (extraits pages 124–134)._")
    lines.append("")
    lines.append("## Pourquoi une démarche avec UML ?")
    lines.append(
        "- UML fournit un langage pour décrire besoins et solutions, mais ne dicte pas la démarche.\n"
        "- Une méthode outillée par UML est typiquement:\n"
        "  - pilotée par les cas d’utilisation (utilité pour l’utilisateur en premier),\n"
        "  - centrée sur l’architecture (satisfaction des besoins, évolutivité, contraintes),\n"
        "  - pragmatique (se concentrer sur le sous-ensemble UML réellement utile)."
    )
    lines.append("")

    for sec in sections:
        lines.append(f"## {sec['title']}")
        img_path = figure_images.get(sec["fig"])
        if img_path is not None:
            rel = img_path.as_posix()
            lines.append(f"![{sec['fig']}]({rel})")
        else:
            lines.append(f"> Illustration: {sec['fig']} (non extraite).")
        lines.append("")
        lines.append(sec["summary"])
        lines.append("")

    lines.append("## Chaîne d’ensemble (récapitulatif)")
    lines.append(
        "1) Cas d’utilisation → 2) Séquences système → 3) Maquette IHM → 4) Modèle du domaine → "
        "5) Classes participantes (Dialogues/Contrôles/Entités) → 6) Interactions (séquences) → "
        "7) Classes de conception (prêtes pour l’implémentation)."
    )
    lines.append("")
    lines.append("## Conseils pratiques")
    lines.append(
        "- Modélisez juste ce qu’il faut: privilégiez la clarté et la traçabilité des décisions.\n"
        "- Tissez les liens entre artefacts (un cas d’utilisation doit se retrouver en séquences, puis en classes participantes, etc.).\n"
        "- Impliquez les utilisateurs tôt via la maquette et itérez selon importance/risque."
    )
    lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")

def main():
    pdf_filename = "uml2-apprentissage-pratique-124-134.pdf"
    pdf_path = Path(pdf_filename)
    if not pdf_path.exists():
        print(f"Fichier PDF introuvable: {pdf_path}. Placez '{pdf_filename}' dans le répertoire courant.")
        # On génère malgré tout un markdown squelette.
        figure_images = {k: None for k in ["Figure 9.1","Figure 9.2","Figure 9.3","Figure 9.4","Figure 9.6","Figure 9.7","Figure 9.8","Figure 9.9","Figure 9.10"]}
        build_markdown(Path("demarche_uml.md"), figure_images)
        return

    # Regex robustes pour repérer les légendes de figures dans le texte extrait
    patterns = {
        "Figure 9.1": r"Figure\s*9\.?1",
        "Figure 9.2": r"Figure\s*9\.?2",
        "Figure 9.3": r"Figure\s*9\.?3",
        "Figure 9.4": r"Figure\s*9\.?4",
        "Figure 9.6": r"Figure\s*9\.?6",
        "Figure 9.7": r"Figure\s*9\.?7",
        "Figure 9.8": r"Figure\s*9\.?8",
        "Figure 9.9": r"Figure\s*9\.?9",
        "Figure 9.10": r"Figure\s*9\.?10",
    }

    page_map = extract_figure_pages(pdf_path, patterns)
    figures_dir = Path("figures")
    figure_images = render_pages_as_images(pdf_path, page_map, figures_dir, dpi=144)
    build_markdown(Path("demarche_uml.md"), figure_images)

if __name__ == "__main__":
    main()
