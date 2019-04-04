from PyPDF2 import PdfFileMerger, PdfFileReader
from flask import send_file
import tempfile


def handle(req):
    """handle a request to the function
    Args:
        req (request): flask request
    """
    files = req.files   # multipart files http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
    file_storages = files.getlist("files")

    if len(file_storages) == 0:
        raise ValueError("no files given. Ensure the multipart boundaries match the one in content-type, "
                         "and the content-disposition of each file part contains both the name 'files' "
                         "as well as a 'filename' attribute")

    # https://pythonhosted.org/PyPDF2/index.html
    merger = PdfFileMerger()

    for file_storage in file_storages:
        pdf_file_reader = PdfFileReader(file_storage)
        merger.append(pdf_file_reader)

    fout = tempfile.TemporaryFile()
    merger.write(fout)

    for file_storage in file_storages:
        file_storage.close()

    fout.seek(0)
    return send_file(fout, 'application/pdf')