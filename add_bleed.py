import os
import copy
from PyPDF2 import PdfReader, PdfWriter, PageObject, Transformation


def add_bleed(input_pdf_path, output_pdf_path=None, bleed_mm=3):
    """
    Add standard bleed to a PDF file by increasing the page size and centering the original content.

    Args:
        input_pdf_path (str): Path to the input PDF file
        output_pdf_path (str, optional): Path to save the output PDF. If None, will append '_with_bleed' to input filename
        bleed_mm (float): Bleed amount in millimeters (default: 3mm)
    """
    if output_pdf_path is None:
        base, ext = os.path.splitext(input_pdf_path)
        output_pdf_path = f"{base}_with_bleed{ext}"

    # Convert mm to points (1 mm = 2.83465 points)
    bleed_pts = bleed_mm * 2.83465

    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        original_width = float(page.mediabox.width)
        original_height = float(page.mediabox.height)
        new_width = original_width + 2 * bleed_pts
        new_height = original_height + 2 * bleed_pts

        # Create a new blank page with the new size
        new_page = PageObject.create_blank_page(width=new_width, height=new_height)
        # Deep copy the original page so we don't modify the input
        page_copy = copy.deepcopy(page)
        # Apply translation to the copy
        page_copy.add_transformation(Transformation().translate(bleed_pts, bleed_pts))
        # Merge the translated page onto the new blank page
        new_page.merge_page(page_copy)
        writer.add_page(new_page)

    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)

    print(f"PDF with bleed saved to: {output_pdf_path}")


if __name__ == "__main__":
    input_pdf = (
        "/Users/kendavidn/Dropbox/Mac (2)/Downloads/Bootcamp-Fliers-RBB-PBB-AIW (1).pdf"
    )
    add_bleed(input_pdf)
