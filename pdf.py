import fitz
from fitz import Matrix
from PyQt6.QtGui import QImage, QPixmap
class PDF:
    def __init__(self, app):
        self.app = app
        self.doc = None
        self.pdfPath = None

    def setPDF(self, pdfPath):
        self.pdfPath = pdfPath
        if self.pdfPath == None:
            self.doc = None
        else:
            self.doc = fitz.open(self.pdfPath)

    def createImages(self, scale_factor = 1, min_line_width = 0):

        if not self.pdfPath:
            return []
        if not self.doc:
            return []
        layers = self.doc.layer_ui_configs()

        fitz.TOOLS.set_graphics_min_line_width(min_line_width)
        imgs = []
        mode = 'RGB'
        matrix = Matrix(fitz.Identity)
        if scale_factor:
            matrix = Matrix(scale_factor, scale_factor)
        for i, page in enumerate(self.doc):
            pix = page.get_pixmap(matrix=matrix)
            bs = pix.tobytes("ppm")
            img = QImage.fromData(bs, "PPM")
            #fmt = QImage.Format.Format_RGBA8888 if pix.alpha else QImage.Format.Format_RGB888
            #img = QImage(pix.samples, pix.width, pix.height, fmt)
            #print(f"w {pix.width} h {pix.height}")
            imgs.append(img)
        return imgs

