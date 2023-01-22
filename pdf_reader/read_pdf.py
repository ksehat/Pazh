# importing the required modules
import PyPDF2


def PDFread(origFileName, newFileName):
    # creating a pdf File object of original pdf
    pdfFileObj = open(origFileName, 'rb')

    # creating a pdf Reader object
    pdfReader = PyPDF2.PdfReader(pdfFileObj)

    # creating a pdf writer object for new pdf
    pdfWriter = PyPDF2.PdfWriter()

    for page in range(len(pdfReader.pages)):
        page_obj = pdfReader.pages[page]
        # contents = page.get_contents().get_data()
        # contents = contents.replace()
        # page.get_contents().set_data(contents)
        # pdfWriter.addPage(page)
        page_obj.update({'/T': '/Yes'})
        pdfWriter.add_page(page_obj)
    # for page in range(len(pdfReader.pages)):
    #     pdfReader.get_pa





    # new pdf file object
    newFile = open(newFileName, 'wb')

    # writing rotated pages to new file
    pdfWriter.write(newFile)

    # closing the original pdf file object
    pdfFileObj.close()

    # closing the new pdf file object
    newFile.close()


def main():
    # original pdf file name
    origFileName = '1.pdf'

    # new pdf file name
    newFileName = 'new.pdf'

    # calling the PDFrotate function
    PDFread(origFileName, newFileName)


if __name__ == "__main__":
    # calling the main function
    main()