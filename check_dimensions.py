from PyPDF2 import PdfReader


def check_pdf_dimensions(pdf_path):
    reader = PdfReader(pdf_path)
    page = reader.pages[0]

    # Get dimensions in points
    width_pts = float(page.mediabox.width)
    height_pts = float(page.mediabox.height)

    # Convert to millimeters (1 point = 0.352778 mm)
    width_mm = width_pts * 0.352778
    height_mm = height_pts * 0.352778

    print(f"PDF Dimensions:")
    print(f"Width: {width_mm:.1f}mm")
    print(f"Height: {height_mm:.1f}mm")

    # Check against required dimensions
    required_width = 850
    required_height = 2000

    if width_mm == required_width and height_mm == required_height:
        print("\n✅ The PDF dimensions are correct!")
    else:
        print("\n❌ The PDF dimensions are incorrect!")
        print(f"Required dimensions: {required_width}x{required_height}mm")


if __name__ == "__main__":
    pdf_path = "/Users/kendavidn/Dropbox/Mac (2)/Documents/graph-courses-42.5-by-100-cm-2025-05-13.pdf"
    check_pdf_dimensions(pdf_path)
