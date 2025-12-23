import os
from reportlab.lib.pagesizes import A4
import markdown2
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from io import BytesIO
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
import urllib.parse
from common.services import convert_to_user_timezone

from weasyprint import HTML, CSS
import re


app = FastAPI()

static_path = Path(__file__).resolve().parent.parent / "static"
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Project root path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Setup template environment
template_env = Environment(
    loader=FileSystemLoader(PROJECT_ROOT/"conversation"/"templates")
)

# Validate the template is found (debugging step)
template_file = PROJECT_ROOT/"conversation"/"templates"/"pdf_header.html"

# Define PDFChatExporter
class PDFChatExporter:
    """Utility class for creating styled PDFs from chat messages using WeasyPrint."""
    base_dir = Path(__file__).resolve().parent.parent.parent

    template_env = Environment(
        loader=FileSystemLoader(base_dir/"conversation"/"templates")
    )

    @staticmethod
    def encode_url(url: str) -> str:
        """Properly encode URL to handle special characters in PDF links."""
        return urllib.parse.quote(url, safe='/:?&=#%')

    @staticmethod
    def _get_logo_path(filename: str = "Intuvigilancelogo.png") -> str:
        """Return absolute file path to the logo in the static directory."""
        return str(PDFChatExporter.base_dir/"conversation"/"static"/filename)

    @staticmethod
    def make_clickable_links(text: str) -> str:
        """Convert URLs and email addresses in text into clickable HTML links."""

        def replace_raw_url(match):
            """ Prevent processing labeled Markdown links by ignoring lines with [label](url) """

            url = match.group(1)
            return f'<a href="{url}" style="color:blue; text-decoration:underline;" target="_blank">{url}</a>'

        # Convert raw HTTP/HTTPS URLs
        text = re.sub(
            r'(?<!\]\()'
            r'(https?://[^\s<]+)',
            replace_raw_url,
            text
        )

        # Convert www. links
        text = re.sub(
            r'(?<!\]\()'
            r'\b(www\.[^\s<]+)',
            lambda m: f'<a href="http://{m.group(1)}" style="color:blue; text-decoration:underline;" target="_blank">{m.group(1)}</a>',
            text
        )

        # Convert email addresses
        text = re.sub(
            r'(?<!\]\()'
            r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)',
            lambda m: f'<a href="mailto:{m.group(1)}" style="color:blue; text-decoration:underline;" target="_blank">{m.group(1)}</a>',
            text
        )
        return text

    @staticmethod
    def create_pdf_from_messages(messages, thread_id, metadata: dict, tz, file_name: str = "IntuVigilanceAI_Report.pdf") -> BytesIO:
        """Generate a styled PDF report from chat messages with header, metadata, and pagination."""

        html_parts = []
        logo_path = PDFChatExporter._get_logo_path()

        if not messages:
            buffer = BytesIO()
            HTML(string="<body></body>").write_pdf(target=buffer)
            buffer.seek(0)
            return buffer

        q_counter = 1
        for msg in messages:
            role = msg.role.value if hasattr(msg.role, "value") else str(msg.role)
            created_at_str = "N/A"
            if hasattr(msg, "created_at"):
                created_at = convert_to_user_timezone(msg.created_at, tz.zone)
                created_at_str = created_at.strftime("%Y-%m-%d %I:%M %p")

            display_role = f"Q{q_counter}" if role.lower() == "user" else "Response" if role.lower() == "assistant" else role.capitalize()
            if role.lower() == "user":
                q_counter += 1

            html_parts.append(f'<div class="question-block">{display_role} [{created_at_str}]</div>')

            raw_content = msg.content or ""
            content_with_links = PDFChatExporter.make_clickable_links(raw_content)
            content_html = markdown2.markdown(content_with_links, extras=["fenced-code-blocks"])

            if role.lower() == "assistant":
                sources_html = ""
                if getattr(msg, "sources", None):
                    sources_html += "<div class='sources'><b>Sources:</b><ul>"
                    for link in msg.sources:
                        sources_html += f'<li><a href="{link}" target="_blank">{link}</a></li>'
                    sources_html += "</ul></div>"

                html_parts.append(f"""
                    <div class="assistant-block">
                        {content_html}
                        {sources_html}
                    </div>
                """)
            else:
                html_parts.append(f"<div class='user-block'>{content_html}</div>")

        logo_path = PDFChatExporter._get_logo_path()

        # Same logic for content generation...
        header_template = PDFChatExporter.template_env.get_template("pdf_header.html")
        header_html = header_template.render(
            logo_path=logo_path,
            last_updated=metadata.get("last_updated", ""),
            country=metadata.get("country", ""),
            category=metadata.get("category", ""),
            subcategory=metadata.get("subcategory", ""),
            user_name=metadata.get("user_name", "")
        )

        body_html = f"""
            <body>
                {header_html}
                {''.join(html_parts)}
            </body>
        """

        buffer = BytesIO()
        css_path = PDFChatExporter.base_dir/"conversation"/"static"/"export_pdf_style.css"

        try:
            HTML(string=body_html).write_pdf(
                target=buffer,
                stylesheets=[CSS(filename=str(css_path))]
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"PDF generation failed: {e}")

        buffer.seek(0)
        return buffer
