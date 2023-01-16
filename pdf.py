import fitz
from fitz import Matrix
from PyQt6.QtGui import QImage, QPixmap
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

        imgs = []
        mode = 'RGB'
        matrix = Matrix(fitz.Identity)
        if scale_factor:
            matrix = Matrix(scale_factor, scale_factor)
        for page in self.doc:
            pix = page.get_pixmap(matrix=matrix)
            bs = pix.tobytes("ppm")
            img = QImage.fromData(bs, "PPM")
            #fmt = QImage.Format.Format_RGBA8888 if pix.alpha else QImage.Format.Format_RGB888
            #img = QImage(pix.samples, pix.width, pix.height, fmt)
            print(f"w {pix.width} h {pix.height}")
            imgs.append(img)
        return imgs

