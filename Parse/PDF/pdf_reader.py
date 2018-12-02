import PyPDF2

with open('Skyteam_Timetable.pdf', 'rb') as pdfFileObj:
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    with open('text_pdf.txt', 'w') as f:
        for i in range(4,27508):
            page = ''
            page = pdfReader.getPage(i).extractText()
            f.write(page + '\n')
            status = '{} from 27507'.format(i-3)
            print(status)
