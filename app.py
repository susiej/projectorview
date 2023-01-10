#!/usr/bin/env python3
# :vim:ts=2:tw=2:et:sts=2:
import sys, fitz, tkinter as tk, functools
from PIL import Image, ImageTk, ImageOps
from screeninfo import get_monitors
from datetime import datetime
from configparser import ConfigParser




#page = doc[0]
#pix = page.get_pixmap()
# set the mode depending on alpha
#label = tk.Label(image = tkimg)
#label.pack()
#frame = tk.Frame(window)
#canvas = tk.Canvas(frame, bd=0)
#canvas.create_image(0, 0, image=tkimg, anchor="nw")
#canvas.pack()
#frame.pack()

#window.mainloop()


class ProjectorView(tk.Frame):
  def __init__(self, parent=None):
    #for m in get_monitors():
    tk.Frame.__init__(self, parent)
    self.master.title("ProjectorView")
    self.readConfig()
    print(get_monitors())
    #print(config.get('main', 'key1'))
    self.pack(expand=tk.YES, fill=tk.BOTH)
    self.canvas = tk.Canvas(self, relief=tk.SUNKEN)
    self.canvas.config(width=400, height=200)
    self.canvas.config(highlightthickness=0)

    sbarV = tk.Scrollbar(self, orient=tk.VERTICAL)
    sbarH = tk.Scrollbar(self, orient=tk.HORIZONTAL)

    sbarV.config(command=self.canvas.yview)
    sbarH.config(command=self.canvas.xview)

    self.canvas.config(yscrollcommand=sbarV.set)
    self.canvas.config(xscrollcommand=sbarH.set)

    sbarV.pack(side=tk.RIGHT, fill=tk.Y)
    sbarH.pack(side=tk.BOTTOM, fill=tk.X)

    self.canvas.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
    self.bind('<Enter>', self._bound_to_mousewheel)
    self.bind('<Leave>', self._unbound_to_mousewheel)

    self.layer_window = tk.Toplevel(self)
    self.config_window = tk.Toplevel(self)
    self.pdfPath = ""
    self.doc = None
    self.configWindow()

  def configWindow(self):
    def updateBorder(v):
      self.config.set('main', 'outer_border', str(v))
      self.addOuterBorder()

    w = tk.Scale(self.config_window, from_=0, to=2000, orient=tk.HORIZONTAL, command=updateBorder, label="Outer border")
    w.set(self.config.getint('main', 'outer_border'))
    w.pack()

    b = tk.Button(self.config_window, text="Save config", command=self.writeConfig)
    b.pack()
    

  def readConfig(self):
    self.config = ConfigParser()
    self.config.read('config.ini')
    self.checkConfig()
  
  def writeConfig(self):
    with open('config.ini', 'w') as f:
      self.config.write(f)
    self.config.read('config.ini')

  def checkConfig(self):
    added = False
    if not self.config.has_section('main'):
      self.config.add_section('main')
      added = True
    if not self.config.has_option('main', 'outer_border'):
      self.config.set('main', 'outer_border', '100')
      added = True
    if added:
      self.writeConfig()


  def _bound_to_mousewheel(self, event):
    # with Windows OS
    self.bind_all("<MouseWheel>", self._on_mousewheel)
    # with Linux
    self.bind_all("<Button-4>", self._on_mousewheel)
    self.bind_all("<Button-5>", self._on_mousewheel)

  def _unbound_to_mousewheel(self, event):
    self.unbind_all("<MouseWheel>")
    self.unbind_all("<Button-4>")
    self.unbind_all("<Button-5>")

  def _on_mousewheel(self, event):
    if sys.platform == 'darwin':
      delta = int(event.delta)
      state = event.state
    elif event.num == 4:
        delta = 1
        state = False
    elif event.num == 5:
        delta = -1
        state = False
    else:
      delta = int(event.delta) / 120
      state = event.state
    if state:
      self.canvas.xview_scroll(int(-1*(delta)), "units")
    else:
      self.canvas.yview_scroll((-1*(delta)), "units")

  def layerModal(self):
    layers = self.doc.layer_ui_configs()
    def update_pdf_layer(a,b):
      on = 2 if b.get() == 0 else 0 # pymupdf uses 2 as setting off, 0 as on and 1 as toggle... dumb
      self.doc.set_layer_ui_config(a, on)
      self.redrawPDF()
      return
        
    for i,l in enumerate(layers):
      v = tk.IntVar()
      v.set(l['on'])
      c = tk.Checkbutton(self.layer_window, text=l['text'], variable=v, onvalue=1, offvalue=0, command=functools.partial(update_pdf_layer, l['number'], v))
      c.pack()

  
  def setPDF(self, path):
    self.pdfPath = path
    self.doc = fitz.open(self.pdfPath)
    self.layerModal()
    self.redrawPDF()

  def redrawPDF(self):
    layers = self.doc.layer_ui_configs() 

    self.canvas.delete('all')
    if not self.pdfPath:
        return
    if not self.doc:
        return
    imgs = []
    width = 0
    height = 0
    mode = 'RGB'
    for page in self.doc:
      pix = page.get_pixmap()
      mode = "RGBA" if pix.alpha else "RGB"
      img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
      img = ImageOps.expand(img, border=5, fill="black")
      imgs.append(img)
      w,h = img.size
      width = max(width, w) 
      height = height + h
    self.image = Image.new(mode, (width, height))
    h = 0
    for img in imgs:
        self.image.paste(img, (0, h))
        w2,h2 = img.size
        h = h + h2

    self.non_bordered_image = self.image
    self.addOuterBorder()

  def addOuterBorder(self):
    self.image = ImageOps.expand(self.non_bordered_image, border=self.config.getint('main','outer_border'), fill='black')
    width,height = self.image.size
    self.tkimg = ImageTk.PhotoImage(self.image)
    self.canvas.config(scrollregion=(0,0,width,height))
    self.imgtag=self.canvas.create_image(0,0,anchor="nw",image=self.tkimg)

sp = ProjectorView()
sp.setPDF('./Itch-to-Stitch-Angelia-Shorts-PDF-Sewing-Pattern-Large-Format-V3.pdf')
sp.mainloop()
#doc = fitz.open('/Users/susie/sewing/Patterns/Patterns/Itch to Stitch/Angelia Shorts/Itch-to-Stitch-Angelia-Shorts-PDF-Sewing-Pattern-Large-Format-V3.pdf')
