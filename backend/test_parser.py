from app.file_parser.service import FileParser

parser = FileParser()

text = parser.parse("test_resume.pdf")

print(text)