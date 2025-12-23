from enum import Enum


class PromptConstant(Enum):
    """All useful prompts will be stored here."""

    MARKDOWN_CONVERTER = """
    Convert the following text into proper Markdown format using appropriate syntax for
    headings, emphasis, lists, code blocks, and any other necessary formatting.
    Do not include any explanations or comments. Do not wrap the output in triple
    backticks or any other code formatting.
    Only return the converted Markdown as plain text.


    Text:
    \"\"\"{input_text}\"\"\"
    """

    PROMPT_TEMPLATE ="""
                 You are an AI assistant specialized in answering questions based on regulatory documents including:
                - Human Medicines Regulations
                - Medicines & Healthcare products Regulatory Agency (MHRA) guidance
                - Guidance on pharmacovigilance procedures
                - Pharmacovigilance requirements

                The information provided is specific to the country: {country}
                
                Use the following context to answer the question:

                {context}

                Question: {question}
                Answer:
            """

