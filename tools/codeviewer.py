from rich.console import Console
from rich.text import Text
import re

console = Console()

def view_pdf_code(pdf_path, lines=500, search_term=None):
    """
    Displays colorized raw PDF code (up to `lines` lines).
    Optionally highlights matching `search_term` entries.
    """
    try:
        with open(pdf_path, "rb") as f:
            content = f.read().decode("latin1", errors="ignore")
            all_lines = content.splitlines()

            for i, line in enumerate(all_lines[:lines], 1):
                t = Text(f"{i:04}: ")

                # Highlight object definitions
                obj_match = re.search(r"\d+\s+\d+\s+obj", line)
                if obj_match:
                    t.append(obj_match.group(), style="bold magenta")
                    line = line.replace(obj_match.group(), "")

                # Highlight /Paths
                for part in re.findall(r"/[A-Za-z0-9#]+", line):
                    line = line.replace(part, f"[cyan]{part}[/cyan]")

                # Highlight strings
                line = re.sub(r"\((.*?)\)", r"[green](\1)[/green]", line)

                # Highlight stream keywords
                line = line.replace("endstream", "[yellow]endstream[/yellow]")

                # Highlight search term if provided
                if search_term:
                    pattern = re.escape(search_term)
                    line = re.sub(f"({pattern})", r"[bold red]\1[/bold red]", line, flags=re.IGNORECASE)

                t.append(Text.from_markup(line))
                console.print(t)


    except Exception as e:
        console.print(f"[bold red][Error][/bold red] Failed to read PDF content: {str(e)}")
