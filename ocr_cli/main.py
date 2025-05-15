import typer
import questionary
from rich import print
from PIL import Image
import pytesseract
from pathlib import Path

app = typer.Typer()


def extract_text(image_path: str, lang: str = "eng") -> str:
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang=lang)
        return text
    except Exception as e:
        return f"[red]Error:[/red] {e}"


@app.command()
def main():
    print("[bold cyan]🧠 OCR CLI Tool[/bold cyan]\n")
    print("[bold yellow]Default OCR language is set to English.[/bold yellow]\n")

    action = questionary.select(
        "What do you want to do?",
        choices=[
            "📄 Extract text and display",
            "💾 Extract text and save to .txt file",
            "❌ Exit"
        ]
    ).ask()

    if action == "❌ Exit":
        print("[bold red]Goodbye![/bold red]")
        raise typer.Exit()

    image_path = questionary.path("Enter the image path:").ask()
    image_path = image_path.strip('"') 
    if not image_path or not Path(image_path).is_file():
        print(f"[red]❗ File not found:[/red] {image_path}")
        raise typer.Exit()

    text = extract_text(image_path)

    if action.startswith("📄"):
        print("\n[bold green]✅ Extracted Text:[/bold green]\n")
        print(text)

    elif action.startswith("💾"):
        output_file = Path(image_path).with_suffix('.txt')
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"\n[green]✅ Text saved to:[/green] {output_file}")


if __name__ == "__main__":
    try:
        app()    
    except KeyboardInterrupt:
        print("\n[bold red]❌ Interrupted by user. Exiting...[/bold red]")

