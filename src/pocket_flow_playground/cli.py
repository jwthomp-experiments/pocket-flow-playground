from typing import Optional
from streamlit.web import cli as stcli
import sys
import typer

app = typer.Typer()


@app.command()
def server() -> None:
    import uvicorn

    uvicorn.run(
        "pocket_flow_playground.server_openai:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )


@app.command()
def web_ui() -> None:
    sys.argv = ["streamlit", "run", "src/pocket_flow_playground/web_ui.py"]
    sys.exit(stcli.main())


@app.command()
def cli() -> None:
    pass


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
) -> None:
    return
