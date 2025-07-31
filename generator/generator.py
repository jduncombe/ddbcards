from .services.card_service import process_json
from .utils.helpers import generate_pdf

def save_pdf_to_file(html_content, output_path):
    """Save the generated HTML content to a file."""
    try:
        with open(output_path, 'wb') as file:
            file.write(html_content)
        print(f"HTML successfully saved to {output_path}")
    except Exception as e:
        print(f"Error saving HTML to file: {e}")

def generate(charname, input_json, out_dir):
    cards = process_json(input_json)  

    # Generate HTML content
    html_content = generate_pdf(cards)

    # Save the generated PDF to the output file
    save_pdf_to_file(html_content, f'{out_dir}/{charname}.pdf')