from PyPDF2 import PdfReader, PdfWriter, PageObject, Transformation
import os


def resize_pdf(
    input_pdf_path, output_pdf_path=None, target_width_mm=850, target_height_mm=2000
):
    """
    Resize a PDF to specific dimensions in millimeters.

    Args:
        input_pdf_path (str): Path to the input PDF file
        output_pdf_path (str, optional): Path to save the output PDF. If None, will append '_resized' to input filename
        target_width_mm (float): Target width in millimeters
        target_height_mm (float): Target height in millimeters
    """
    if output_pdf_path is None:
        base, ext = os.path.splitext(input_pdf_path)
        output_pdf_path = f"{base}_850x2000mm{ext}"

    # Convert mm to points (1 mm = 2.83465 points)
    target_width_pts = target_width_mm * 2.83465
    target_height_pts = target_height_mm * 2.83465

    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        # Create a new blank page with the target size
        new_page = PageObject.create_blank_page(
            width=target_width_pts, height=target_height_pts
        )

        # Calculate scaling factors
        original_width = float(page.mediabox.width)
        original_height = float(page.mediabox.height)
        scale_x = target_width_pts / original_width
        scale_y = target_height_pts / original_height

        # Create transformation matrix for scaling
        transform = Transformation().scale(scale_x, scale_y)

        # Apply transformation to the page
        page.scale(scale_x, scale_y)

        # Merge the scaled page onto the new blank page
        new_page.merge_page(page)
        writer.add_page(new_page)

    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)

    print(f"Resized PDF saved to: {output_pdf_path}")

    # Verify the new dimensions
    reader = PdfReader(output_pdf_path)
    page = reader.pages[0]
    width_pts = float(page.mediabox.width)
    height_pts = float(page.mediabox.height)
    width_mm = width_pts / 2.83465
    height_mm = height_pts / 2.83465
    print(f"\nNew dimensions:")
    print(f"Width: {width_mm:.1f}mm")
    print(f"Height: {height_mm:.1f}mm")


if __name__ == "__main__":
    input_pdf = "/Users/kendavidn/Dropbox/Mac (2)/Documents/graph-courses-42.5-by-100-cm-2025-05-13.pdf"
    resize_pdf(input_pdf)
