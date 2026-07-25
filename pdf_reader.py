from pypdf import PdfReader


def read_pdf(pdf_path, file_name):
    reader = PdfReader(pdf_path)

    pages = []


    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()

        if page_text:
            pages.append({
                "text": page_text,
                "page": page_number,
                "file_name": file_name
            })

    return pages