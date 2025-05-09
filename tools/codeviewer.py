from rich.console import Console
from rich.text import Text
import re

console = Console()

def view_pdf_code(pdf_path, lines=500):
    """
    Displays colorized raw PDF code (up to `lines` lines).
    Highlights common PDF keys, paths, and values.
    """
    try:
        with open(pdf_path, "rb") as f:
            content = f.read().decode("latin1", errors="ignore")
            all_lines = content.splitlines()

            for i, line in enumerate(all_lines[:lines], 1):
                t = Text(f"{i:04}: ")

                # PDF objects like "12 0 obj"
                obj_match = re.search(r"\d+\s+\d+\s+obj", line)
                if obj_match:
                    t.append(obj_match.group(), style="bold magenta")
                    line = line.replace(obj_match.group(), "")

                # Paths like /Type /JS /Pages etc.
                for part in re.findall(r"/[A-Za-z0-9#]+", line):
                    line = line.replace(part, f"[cyan]{part}[/cyan]")

                # Strings in parentheses
                line = re.sub(r"\((.*?)\)", r"[green](\1)[/green]", line)

                # Stream keywords
           
                line = line.replace("endstream", "[yellow]endstream[/yellow]")

                t.append(Text.from_markup(line))
                console.print(t)

            if len(all_lines) > lines:
                console.print(f"\n[dim]... (truncated at {lines} lines)[/dim]")

    except Exception as e:
        console.print(f"[bold red][Error][/bold red] Failed to read PDF content: {str(e)}")
