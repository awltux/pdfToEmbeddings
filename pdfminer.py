from pdfminer.high_level import extract_text

text  = extract_text('./data/obama-worlds-matter.pdf', 'rb')
print(text)