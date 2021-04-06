from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO

resume_file = 'pdfs/xuhaoyu_380313_4284914_hx2258_resume.pdf'
resource_mgr = PDFResourceManager()
retstr = BytesIO()
codec = 'utf-8'
laparams = LAParams()
device = TextConverter(resource_mgr, retstr, laparams=laparams)
fp = open(resume_file, 'rb')
interpreter = PDFPageInterpreter(resource_mgr, device)
maxpages = 0
caching = True
pagenos = set()

# loops over PDFs with multiple pages
for page in PDFPage.get_pages(fp, pagenos,
                              maxpages=maxpages,
                              caching=caching,
                              check_extractable=True):
    interpreter.process_page(page)

print(retstr.getvalue())
type(retstr.getvalue())

fp.close()
device.close()
retstr.close()
