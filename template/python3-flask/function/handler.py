from PyPDF2 import PdfFileMerger, PdfFileReader
from flask import send_file
import tempfile

def handle(req):
    """handle a request to the function
    Args:
        req (request): flask request
    """
    files = req.files
    file_storages = files.getlist("files")
    print(file_storages)

    merger = PdfFileMerger()

    for file_storage in file_storages:
        pdfFileReader = PdfFileReader(file_storage)
        merger.append(pdfFileReader)

    # with open('D:/result.pdf', 'wb') as fout:   # write binary
    fout = tempfile.TemporaryFile()
    merger.write(fout)

    for file_storage in file_storages:
        file_storage.close()

    fout.seek(0)
    return send_file(fout, 'application/pdf')
