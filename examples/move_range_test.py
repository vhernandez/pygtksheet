import gtk
import pango
import gtksheet

class MainWin(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)

        self.sheet = gtksheet.Sheet(columns=20, rows=20)

        scrwin = gtk.ScrolledWindow()
        scrwin.add(self.sheet)

        self.add(scrwin)
        self.show_all()
        self.set_size_request(700,480)
        self.count = 0
        for i in xrange(20):
            for j in xrange(20):                
                self.sheet.set_cell_text(i, j, "Row %d Col: %d" % (i,j)) 
        self.sheet.insert_rows(0,1)
        self.sheet.range_set_font(gtksheet.SheetRange(0,0,0,0),
                                  pango.FontDescription("sans bold 9"))
        self.sheet.set_cell_text(0,0, "Select some cells, click the border of the selection and drag it to a new location")
        self.sheet.set_active_cell(1,0)
        self.connect("delete-event", lambda x,y: gtk.main_quit())
        self.sheet.connect("move-range", self._move_range_cb)
        self.set_title("Moving cell contents around")

    def _move_range_cb(self, sheet, range1, range2):
        print "Moving", range1, "to", range2
        assert range1.rowi - range1.row0 == range2.rowi - range2.row0
        assert range1.coli - range1.col0 == range2.coli - range2.col0

        #first copy the text, in case range1 and range2 overlap
        ops = []
        for i1, i2 in zip(xrange(range1.row0, range1.rowi+1), xrange(range2.row0, range2.rowi+1)):
            for j1, j2 in zip(xrange(range1.col0, range1.coli+1), xrange(range2.col0, range2.coli+1)):
                ops.append( (i2,j2, sheet.cell_get_text(i1, j1)))
        #then move the text
        for i,j,text in ops:
            sheet.set_cell_text(i,j,text)
                
        
if __name__ == '__main__':
  MainWin()
  gtk.main()
