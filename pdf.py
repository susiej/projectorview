import fitz
from fitz import Matrix
class PDF:
    def __init__(self, parent):
        self.parent = parent

    def setPDF(self, pdfPath):
        self.pdfPath = pdfPath
        if self.pdfPath == None:
            self.doc = None
        else:
            self.doc = fitz.open(self.pdfPath)

    def createImages(self, scale_factor = 1):
        layers = self.doc.layer_ui_configs()

        if not self.pdfPath:
            return
        if not self.doc:
            return

        pixs = []
        mode = 'RGB'
        matrix = Matrix(fitz.Identity)
        if scale_factor:
            matrix = Matrix(scale_factor, scale_factor)
        for page in self.doc:
            pix = page.get_pixmap(matrix=matrix)
            pixs.append(pix)
        return pixs

