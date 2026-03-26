from pathlib import Path
import subprocess


def render_graphviz(dot_path: Path, output_dir: Path) -> None:
    """Render Graphviz to PNG (300 DPI, journal quality), SVG, and PDF (vector)."""
    output_dir.mkdir(parents=True, exist_ok=True)
    png_path = output_dir / "figure1_system_architecture.png"
    svg_path = output_dir / "figure1_system_architecture.svg"
    pdf_path = output_dir / "figure1_system_architecture.pdf"

    # 300 DPI for A4 print / journal standard (min 300 for raster)
    subprocess.run(
        ["dot", "-Gdpi=300", "-Tpng", str(dot_path), "-o", str(png_path)],
        check=True,
    )
    subprocess.run(
        ["dot", "-Tsvg", str(dot_path), "-o", str(svg_path)],
        check=True,
    )
    subprocess.run(
        ["dot", "-Tpdf", str(dot_path), "-o", str(pdf_path)],
        check=True,
    )

    print(f"Saved: {png_path} (300 DPI)")
    print(f"Saved: {svg_path}")
    print(f"Saved: {pdf_path} (vector, for print)")


if __name__ == "__main__":
    base_dir = Path(__file__).parent
    render_graphviz(
        dot_path=base_dir / "figure1_architecture.dot",
        output_dir=base_dir / "figures",
    )
