from PyPDF2 import PdfFileMerger, PdfFileReader
import tempfile


def handle(event, context):
    json = event.json

    if json:
        return { "body": json }

    form = event.form
    files = event.files  # multipart files http://flask.pocoo.org/docs/1.0/patterns/fileuploads/

    if len(files) == 0:
        return { "body": form.getlist('foo') }

    original_files = form.getlist("originalFiles")

    file_storages = files.getlist("files")

    if len(file_storages) == 0:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/problem+json"
            },
            "body": {
                "title": "No files given",
                "type": "https://example.com/probs/no-files",
                "detail": "Ensure that the multipart boundaries match the one in content-type, "
                                "and the content-disposition of each file part contains both the name 'files' "
                                "as well as a 'filename' attribute"
            }
        }

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

    # TODO implement
    return {
        'statusCode': 200,
        "headers": {
            "Content-Disposition": "attachment; filename=result.pdf"
            # 'Content-Type': 'application/pdf'
        },
        'file': fout
    }
