from pypdf import PdfReader


def extract_pages(pdf_path):

    reader = PdfReader(
        pdf_path
    )

    pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        text = page.extract_text() or ""

        text = text.strip()

        if text:

            pages.append({
                "page": page_number,
                "text": text
            })

    return pages