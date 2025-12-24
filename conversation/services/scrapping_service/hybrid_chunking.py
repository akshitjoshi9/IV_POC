import re
from typing import List
from langchain.schema import Document


class HybridChunker:
    """
    Hybrid Chunking Strategy
    ------------------------
    1. Section-aware hierarchical splitting
    2. Paragraph-level semantic chunking
    3. Boilerplate removal
    4. Size-safe merging
    5. Context-preserving metadata enrichment
    """

    MIN_CHARS = 80
    MAX_CHARS = 1200
    SECTION_PREVIEW_CHARS = 200

    SECTION_PATTERNS = [
        r"\nNews story\n",
        r"\nPress release\n",
        r"\nNotes to Editors:\n",
        r"\nPublished .*?\n",
        r"\nDr .*? said:\n",
    ]

    BOILERPLATE_PATTERNS = [
        "share this page",
        "share on facebook",
        "share on twitter",
        "the following links open",
        "updates to this page",
        "media enquiries",
        "email ",
        "telephone ",
    ]

    def __init__(
        self,
        min_chars: int | None = None,
        max_chars: int | None = None,
    ):
        self.min_chars = min_chars or self.MIN_CHARS
        self.max_chars = max_chars or self.MAX_CHARS

        self._section_regex = re.compile(
            "(" + "|".join(self.SECTION_PATTERNS) + ")",
            flags=re.IGNORECASE,
        )

    def _split_by_sections(self, text: str) -> List[str]:
        parts = self._section_regex.split(text)

        sections = []
        buffer = ""

        for part in parts:
            if self._section_regex.match(part):
                if buffer.strip():
                    sections.append(buffer.strip())
                buffer = part
            else:
                buffer += part

        if buffer.strip():
            sections.append(buffer.strip())

        return sections

    def _split_by_paragraphs(self, section: str) -> List[str]:
        return [p.strip() for p in section.split("\n\n") if p.strip()]

    def _is_boilerplate(self, text: str) -> bool:
        text_lower = text.lower()
        return any(bp in text_lower for bp in self.BOILERPLATE_PATTERNS)

    def _merge_chunks(self, chunks: List[str]) -> List[str]:
        merged = []
        buffer = ""

        for chunk in chunks:
            if not buffer:
                buffer = chunk
                continue

            if len(buffer) + len(chunk) <= self.max_chars:
                buffer += " " + chunk
            else:
                merged.append(buffer.strip())
                buffer = chunk

        if buffer.strip():
            merged.append(buffer.strip())

        return merged

    def chunk(self, documents: List[Document]) -> List[Document]:
        """
        Main entrypoint used by embedding pipeline
        """
        final_chunks: List[Document] = []

        for doc in documents:
            source = doc.metadata.get("source", "unknown")
            text = doc.page_content

            sections = self._split_by_sections(text)

            for section in sections:
                section_preview = section[: self.SECTION_PREVIEW_CHARS]

                paragraphs = self._split_by_paragraphs(section)

                clean_paragraphs = [
                    p for p in paragraphs
                    if len(p) >= self.min_chars and not self._is_boilerplate(p)
                ]

                merged_chunks = self._merge_chunks(clean_paragraphs)

                for chunk in merged_chunks:
                    final_chunks.append(
                        Document(
                            page_content=chunk,
                            metadata={
                                "source": source,
                                "chunking": "hybrid",
                                "section_preview": section_preview,
                            },
                        )
                    )

        return final_chunks
