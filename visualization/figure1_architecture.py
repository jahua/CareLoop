from pathlib import Path
import subprocess


def render_graphviz(dot_path: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    png_path = output_dir / "figure1_system_architecture.png"
    svg_path = output_dir / "figure1_system_architecture.svg"

    subprocess.run(
        ["dot", "-Tpng", str(dot_path), "-o", str(png_path)],
        check=True,
    )
    subprocess.run(
        ["dot", "-Tsvg", str(dot_path), "-o", str(svg_path)],
        check=True,
    )

    print(f"Saved: {png_path}")
    print(f"Saved: {svg_path}")


if __name__ == "__main__":
    base_dir = Path(__file__).parent
    render_graphviz(
        dot_path=base_dir / "figure1_architecture.dot",
        output_dir=base_dir / "figures",
    )
