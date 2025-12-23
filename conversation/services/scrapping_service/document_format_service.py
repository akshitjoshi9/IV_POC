
class DocumentFormatting:

    def format_docs_with_metadata(self, documents):
        for document in documents:
            source = document.metadata.get("source", "Unknown source")
            document.page_content = f"Source: {source}\n\n{document.page_content}"
        return documents