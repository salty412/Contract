import os
import sys
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_file):
    """Splits a PDF file into individual pages and names them according to specific names.
    Args:
        input_file (str): Path to the input PDF file.
        output_dir (str): Path to the output directory.
    """
    input_file = input_file.strip('"')
    output_dir = os.path.dirname(input_file)

    with open(input_file, 'rb') as file:
        pdf_reader = PdfReader(file)
        num_pages = len(pdf_reader.pages)
        
        #standard packet is 6 pages
        if num_pages == 6:
          
            page_names = ["Contract", "Med Auth SHC", "Med Auth Defense", "POA to Endorse", "Employment Auth", "Certificate"]

            for page_num in range(num_pages):
                pdf_writer = PdfWriter()
                pdf_writer.add_page(pdf_reader.pages[page_num])

                output_filename = os.path.join(output_dir, f"{page_names[page_num]}.pdf")
                with open(output_filename, 'wb') as output_file:
                    pdf_writer.write(output_file)

        elif (num_pages - 1) % 5 != 0:
            for page_num in range(num_pages):
                pdf_writer = PdfWriter()
                pdf_writer.add_page(pdf_reader.pages[page_num])

                output_filename = os.path.join(output_dir, f"{[page_num]}.pdf")
                with open(output_filename, 'wb') as output_file:
                    pdf_writer.write(output_file)

        #if not 6 pages, it's likely multiple clients in a single pdf. needs to iterate for each client, but there's only one certificate page
        else:
            page_names = ["Contract", "Med Auth SHC", "Med Auth Defense", "POA to Endorse", "Employment Auth"]
            num_core_pages = len(page_names)

            client_index = 0

            for i in range(num_pages):
                pdf_writer = PdfWriter()
                pdf_writer.add_page(pdf_reader.pages[i])

                page_index = i % num_core_pages

                if i + 1 < num_pages:
                    output_filename = os.path.join(output_dir, f"{page_names[page_index]} {client_index + 1}.pdf")
                else:
                    output_filename = os.path.join(output_dir, f"Certificate.pdf")

                with open(output_filename, 'wb') as output_file:
                    pdf_writer.write(output_file)
            
                if page_index == num_core_pages - 1:
                    client_index += 1
                
                    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file_received = sys.argv[1]
        #print(f"Python script received: '{input_file_received}'")
        split_pdf(input_file_received)
    else:
        input_file = input("Enter the full path to the input PDF file: ")
        print(input_file)
        split_pdf(input_file)

        #hiiiiiii