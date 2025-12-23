from uuid import UUID
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from io import BytesIO
from typing import Optional
from datetime import datetime, timezone
import pytz

from core.models import (
    Message, CategoryMaster, CountryMaster, SubCategoryMaster, User, Thread
    )
from .create_pdf_service import PDFChatExporter


class ChatExportService:
    """Service class for exporting chat messages to PDF."""

    def __init__(self, db: Session, user_timezone: str = "UTC"):
        self.db = db
        try:
            self.tz = pytz.timezone(user_timezone)
        except pytz.UnknownTimeZoneError:
            self.tz = pytz.UTC

    def generate_chat_pdf(
        self, thread_id: UUID, message_id: Optional[UUID] = None
    ) -> Optional[BytesIO]:
        """Generate chat PDF for either full thread OR a specific Q–A."""

        thread_details = self.db.exec(
            select(
                CountryMaster.name.label("country_name"),
                CategoryMaster.name.label("category_name"),
                SubCategoryMaster.name.label("subcategory_name"),
                User.first_name,
                User.last_name,
            )
            .select_from(Thread)
            .join(User, Thread.user_id == User.id)
            .join(SubCategoryMaster, Thread.subcategory_id == SubCategoryMaster.id)
            .join(CategoryMaster, SubCategoryMaster.category_id == CategoryMaster.id)
            .join(CountryMaster, Thread.country_id == CountryMaster.id)
            .where(Thread.id == thread_id)
        ).first()

        # Convert last_updated into user tz
        utc_now = datetime.now(timezone.utc)
        metadata = {
            "last_updated": utc_now.astimezone(self.tz).strftime("%b %d, %Y, %I:%M %p"),
            "country": thread_details.country_name if thread_details else "",
            "category": thread_details.category_name if thread_details else "",
            "subcategory": thread_details.subcategory_name if thread_details else "",
            "user_name": f"{thread_details.first_name} {thread_details.last_name}" if thread_details else "",
        }

        if message_id:
            answer = self.db.get(Message, message_id)
            if not answer or answer.thread_id != thread_id:
                return None

            messages = [msg for msg in (self.db.get(Message, answer.parent_id), answer) if msg]
            file_name = f"IntuVigilanceAI_{metadata.get("country")}_{metadata.get("category")}_{metadata.get("subcategory")}_Reporting.pdf"
        else:
            messages = self.db.exec(
                select(Message)
                .where(Message.thread_id == thread_id)
                .options(selectinload(Message.feedback))
                .order_by(Message.created_at)
            ).all()
            file_name = f"IntuVigilanceAI_{metadata.get("country")}_SessionHistory_Reporting.pdf"

        # return PDFChatExporter.create_pdf_from_messages(messages, thread_id) if messages else None
        pdf_stream = PDFChatExporter.create_pdf_from_messages(
            messages,
            thread_id,
            metadata=metadata,
            tz=self.tz,
            file_name=file_name
        )

        return pdf_stream, file_name
