
class DocumentFormatting:
    def format_docs_with_metadata(self, documents):
        for doc in documents:
            source = doc.metadata.get("source", "unknown")
            doc.metadata["source"] = source
        return documents
