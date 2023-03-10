import pdfreader
from pdfreader import PDFDocument, SimplePDFViewer

file_name = "2023+Domestic+Technical+Handbook.pdf"
fd = open(file_name, "rb")
doc = PDFDocument(fd)

print("version: %s" % doc.header.version )
print("doc.root.Type: %s" % doc.root.Type )
print("doc.root.Metadata.Subtype: %s" % doc.root.Metadata.Subtype )

# 
# 

viewer = SimplePDFViewer(fd)

for canvas in viewer:
     current_page_number = viewer.current_page_number
     if current_page_number > 10:
       continue
       
     page_images = canvas.images
     page_forms = canvas.forms
     page_text = canvas.text_content
     page_inline_images = canvas.inline_images
     page_strings = canvas.strings

     print("#########################################################")
     print("viewer.current_page_number: %s" % current_page_number)
     print("canvas.text_content: %s" % ''.join(canvas.strings))
