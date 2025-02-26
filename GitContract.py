import os
from PyPDF2 import PdfReader, PdfWriter
#trying git
def split_pdf(input_file):
    """Splits a PDF file into individual pages and names them according to specific names.

    Args:
        input_file (str): Path to the input PDF file.
        output_dir (str): Path to the output directory.
    """
    #strip the quotation marks that are added when you copy to path
    input_file = input_file.strip('"')
    #output should be in the same directory as the input file
    output_dir = os.path.dirname(input_file)
    #standard page names
    page_names = ["Contract", "Med Auth SHC", "Med Auth Defense", "POA to Endorse", "Employment Auth", "Certificate"]
    pdf_writer = PdfWriter()

    with open(input_file, 'rb') as file:
        pdf_reader = PdfReader(file)
        num_pages = len(pdf_reader.pages)
        #standard case, pandadoc package has 6 pages
        if num_pages == 6:

            for page_num in range(num_pages):
                pdf_writer = PdfWriter()
                #extracts the current page
                pdf_writer.add_page(pdf_reader.pages[page_num])
                #creates variable containing file name
                output_filename = os.path.join(output_dir, f"{page_names[page_num]}.pdf")
                #outputs new file
                with open(output_filename, 'wb') as output_file:
                    pdf_writer.write(output_file)
        #if there are an unusual amount of pages, usually if signed up in person
        elif (num_pages - 1) % 5 != 0:
            for page_num in range(num_pages):
                pdf_writer = PdfWriter()
                pdf_writer.add_page(pdf_reader.pages[page_num])
                #outputs as just a page number
                output_filename = os.path.join(output_dir, f"{[page_num]}.pdf")
                with open(output_filename, 'wb') as output_file:
                    pdf_writer.write(output_file)

        #used if multiple clients are included in a sign up packet
        else:
            num_core_pages = len(page_names)

            client_index = 0

            for i in range(num_pages):
                pdf_writer = PdfWriter()
                pdf_writer.add_page(pdf_reader.pages[i])

                page_index = i % num_core_pages
                #if it is not the last page in the packet
                if i + 1 < num_pages:
                    output_filename = os.path.join(output_dir, f"{page_names[page_index]} {client_index + 1}.pdf")
                else:
                    output_filename = os.path.join(output_dir, f"Certificate.pdf")

                with open(output_filename, 'wb') as output_file:
                    pdf_writer.write(output_file)
            
                if page_index == num_core_pages - 1:
                    client_index += 1
                
                    
if __name__ == "__main__":
    
    input_file = input("Enter the full path to the input PDF file: ")

    print(input_file)

    split_pdf(input_file)