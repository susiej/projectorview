import fitz
from fitz import Matrix
from PyQt6.QtGui import QImage, QPixmap
class PDF:
    def __init__(self, app):
        self.app = app
        self.doc = None
        self.pdfPath = None
        self.trims = {"left": 0, "right": 0, "top": 0, "bottom": 0}
        self.trim_units = "pixels"
        self.cropboxes = []

    def setPDF(self, pdfPath):
        self.pdfPath = pdfPath
        self.cropboxes = []
        if self.pdfPath == None:
            self.doc = None
        else:
            self.doc = fitz.open(self.pdfPath)
            for page in self.doc:
                self.cropboxes.append(page.cropbox)
                


    def setTrimUnits(self, u):
        self.trim_units = u

    def setTrimLeft(self, t):
        self.trims["left"] = t

    def setTrimRight(self, t):
        self.trims["right"] = t

    def setTrimTop(self, t):
        self.trims["top"] = t

    def setTrimBottom(self, t):
        self.trims["bottom"] = t

    def calcBox(self, page, i):
        def convert(v):
            match self.trim_units:
                case "pixels":
                    return v
                case "cm":
                    return v * 72 / 2.53
                case "inches":
                    return v * 72

        #cb = page.cropbox
        cb = self.cropboxes[i]
        x0 = cb.x0 + convert(self.trims["left"])
        y0 = cb.y0 + convert(self.trims["top"])
        x1 = cb.x1 - convert(self.trims["right"])
        y1 = cb.y1 - convert(self.trims["bottom"])
        r = fitz.Rect(x0, y0, x1, y1)
        if cb.contains(r):
            page.set_cropbox(r)

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
            self.calcBox(page, i)
            page.set_rotation(0)
            pix = page.get_pixmap(matrix=matrix)
            bs = pix.tobytes("ppm")
            img = QImage.fromData(bs, "PPM")
            #fmt = QImage.Format.Format_RGBA8888 if pix.alpha else QImage.Format.Format_RGB888
            #img = QImage(pix.samples, pix.width, pix.height, fmt)
            #print(f"w {pix.width} h {pix.height}")
            imgs.append(img)
        return imgs

