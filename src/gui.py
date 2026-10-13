"""Temperature converter browser page (US-5). Spec: specs/temperature-converter/"""
import html
import math
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import List, Optional
from urllib.parse import parse_qs, urlsplit

import converter

TITLE = "Temperature Converter"


def conversion_lines(value_text: str, from_unit: str) -> List[str]:
    """Convert value_text from from_unit to every other unit, formatted for display."""
    try:
        value = float(value_text)
    except ValueError:
        raise ValueError("Enter a number") from None
    if not math.isfinite(value):  # float() accepts "nan" and "inf"
        raise ValueError("Enter a number")
    source = from_unit.upper()
    return [  # AC-14, AC-15; units come from the table (AC-17)
        converter.format_result(converter.convert(value, source, unit), unit)
        for unit in converter.UNITS
        if unit != source
    ]


def render_page(value_text: Optional[str], unit: str) -> str:
    """Build the page. value_text is None on first load, before anything is submitted."""
    options = "\n".join(  # AC-13, AC-17
        f'<option value="{u}"{" selected" if u == unit.upper() else ""}>{u}</option>'
        for u in converter.UNITS
    )
    if value_text is None:
        output = ""
    else:
        try:
            lines = conversion_lines(value_text, unit)
            output = "\n".join(f"<p>{html.escape(line)}</p>" for line in lines)
        except ValueError as e:  # AC-16
            output = f"<p>Error: {html.escape(str(e))}</p>"
    value_attr = html.escape(value_text or "", quote=True)  # never echo raw input
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>{TITLE}</title></head>
<body>
<h1>{TITLE}</h1>
<form method="get" action="/">
<label>Value <input name="value" value="{value_attr}" autofocus></label>
<label>Unit <select name="unit">
{options}
</select></label>
<button type="submit">Convert</button>
</form>
{output}
</body>
</html>
"""


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlsplit(self.path)
        if url.path != "/":
            self.send_error(404)
            return
        # keep_blank_values: an empty field must show an error, not the first-load page
        query = parse_qs(url.query, keep_blank_values=True)
        value_text = query["value"][0] if "value" in query else None
        unit = query.get("unit", [next(iter(converter.UNITS))])[0]
        body = render_page(value_text, unit).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass  # keep the terminal quiet


def make_server(port: int = 0) -> HTTPServer:
    """Create the server on 127.0.0.1 only; port 0 lets the OS pick a free port (AC-18)."""
    return HTTPServer(("127.0.0.1", port), _Handler)


def main() -> int:
    server = make_server()
    url = f"http://127.0.0.1:{server.server_address[1]}/"
    # flush: show the address right away even when output is not a terminal
    print(f"{TITLE} running at {url}  (press Ctrl+C to stop)", flush=True)
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    print("Stopped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
