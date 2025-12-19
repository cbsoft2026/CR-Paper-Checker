from pypdf import PdfReader

def visitor_font_info(text, cm, tm, font_dict, font_size):
    """
    A visitor function that captures font information for each text fragment.
    """
    if font_dict:
        # Extract the BaseFont name from the font dictionary if available
        font_name = font_dict.get('/BaseFont', 'Unknown')
        print(f"Text: '{text.strip()}', Size: {font_size}, Font: {font_name}")


def main():

    reader = PdfReader("/data/sbes24.pdf")
    number_of_pages = len(reader.pages)
    # page = reader.pages[6]
    # text = page.extract_text()
    print("PDF has", number_of_pages, "pages") ## Check page limits?

    print("PDF Outline:\n", reader.outline)
    print("-"*72)
    print(reader.metadata) ## Check if used acmart
    ## Check if title matches first page title?

    #for page in reader.pages:
        # Pass the visitor function to extract_text
    reader.pages[0].extract_text(visitor_text=visitor_font_info)

if __name__ == "__main__":
    main()