import gtk
from gtk import gdk
import pango
import gtksheet
from bordercombo import BorderCombo


DEFAULT_PRECISION = 3
DEFAULT_SPACE = 8

# XPM
bullet_xpm = [\
"16 16 26 1",
" 	c #None",
".	c #000000000000",
"X	c #0000E38D0000",
"o	c #0000EBAD0000",
"O	c #0000F7DE0000",
"+	c #0000FFFF0000",
"@	c #0000CF3C0000",
"#	c #0000D75C0000",
"$	c #0000B6DA0000",
"%	c #0000C30B0000",
"&	c #0000A2890000",
"*	c #00009A690000",
"=	c #0000AEBA0000",
"-	c #00008E380000",
";	c #000086170000",
":	c #000079E70000",
">	c #000071C60000",
",	c #000065950000",
"<	c #000059650000",
"1	c #000051440000",
"2	c #000045140000",
"3	c #00003CF30000",
"4	c #000030C20000",
"5	c #000028A20000",
"6	c #00001C710000",
"7	c #000014510000",
"     ......     ",
"    .XooO++.    ",
"  ..@@@#XoO+..  ",
" .$$$$$%@#XO++. ",
" .&&*&&=$%@XO+. ",
".*-;;;-*&=%@XO+.",
".;:>>>:;-&=%#o+.",
".>,<<<,>:-&$@XO.",
".<12321<>;*=%#o.",
".1345431,:-&$@o.",
".2467642<>;&$@X.",
" .57.753<>;*$@. ",
" .467642<>;&$@. ",
"  ..5431,:-&..  ",
"    .21<>;*.    ",
"     ......     "]

# XPM 
smile_xpm = [\
"16 16 3 1",
" 	c #None",
".	c #000000000000",
"X	c #FFFFFFFF0000",
"     ......     ",
"    .XXXXXX.    ",
"  ..XXXXXXXX..  ",
" .XXXXXXXXXXXX. ",
" .XXX..XX..XXX. ",
".XXXX..XX..XXXX.",
".XXXX..XX..XXXX.",
".XXXXXXXXXXXXXX.",
".XX..XXXXXX..XX.",
".XX..XXXXXX..XX.",
".XXX.XXXXXX.XXX.",
" .XXX.XXXX.XXX. ",
" .XXXX....XXXX. ",
"  ..XXXXXXXX..  ",
"    .XXXXXX.    ",
"     ......     "]

class Sheet1(gtksheet.Sheet):
    def __init__(self):
        gtksheet.Sheet.__init__(self, 1000, 26)
        self.set_background(gdk.color_parse("light yellow"))
        self.set_grid(gdk.color_parse("light blue"))

        for column in xrange(self.get_columns_count()):
            name = chr(ord("A") + column)
            self.column_button_add_label(column, name)
            self.set_column_title(column, name)

        self.row_button_add_label(0, "This is\na multiline\nlabel")
        self.row_button_add_label(1, "This is long label")
        self.row_button_justify(0, gtk.JUSTIFY_RIGHT)

        range = gtksheet.SheetRange(1,1,2,3)
        self.clip_range(range)
        self.range_set_font(range, pango.FontDescription("Arial 28"))
        self.range_set_foreground(range, gdk.color_parse("red"))

        self.set_cell(1,2, gtk.JUSTIFY_CENTER, "Welcome to")
        
        range.row0 = 2
        self.range_set_font(range, pango.FontDescription("Arial 36"))
        self.range_set_foreground(range, gdk.color_parse("blue"))
        self.set_cell(2,2, gtk.JUSTIFY_CENTER, "python-gtksheet")


        range = gtksheet.SheetRange(3,0,3,4)
        self.range_set_background(range, gdk.color_parse("dark gray"))
        self.range_set_foreground(range, gdk.color_parse("green"))

        self.set_cell(3, 2, gtk.JUSTIFY_CENTER, "a Matrix widget for Gtk+")
        
        texts =["GtkSheet is a matrix where you can allocate cells of text.",
                "Cell contents can be edited interactively with an specially designed entry",
                "You can change colors, borders, and many other attributes",
                "Drag & drop or resize the selection clicking the corner or border",
                "Store the selection on the clipboard pressing Ctrl-C",
                "You can add buttons, charts, pixmaps, and other widgets"]
        for i in xrange(len(texts)):
            self.set_cell(i+4, 1, gtk.JUSTIFY_LEFT, texts[i])
        
        colormap = gdk.colormap_get_system()
        pixmap, mask = gdk.pixmap_colormap_create_from_xpm_d(None, colormap, 
                                                             None, bullet_xpm)
        for i in xrange(6):
            image = gtk.image_new_from_pixmap(pixmap, mask)
            image.show()
            self.attach( image,
                         4+i, 0, gtk.EXPAND, gtk.EXPAND, 0, 0)

        pixmap, mask = gdk.pixmap_colormap_create_from_xpm_d(None, colormap, 
                                                             None, smile_xpm)
        self.button_attach( gtk.image_new_from_pixmap(pixmap, mask), -1, 5)

        self.curve = gtk.Curve()
        self.curve.show()
        self.curve.set_range(0, 200, 0, 200)
        
        show_button = gtk.Button("Show me a plot")
        show_button.show()
        show_button.set_size_request(100, 60)
        self.attach(show_button, 12, 2, gtk.FILL, gtk.FILL, 5, 5)

        show_button.connect("clicked", self._show_child_cb)

        self.connect("key_press_event", self._key_press_cb)

    def _show_child_cb(self, widget):
        if not self.curve.flags() & gtk.MAPPED:
            self.attach_floating(self.curve, 2, 7)
            
    def _key_press_cb(self, widget, event):
        copy = False
        kname = gdk.keyval_name(event.keyval)
        if event.state & gdk.CONTROL_MASK or kname in ("Control_L", "Control_R"):
            if kname in ('c', 'C') and self.props.state != gtksheet.SHEET_NORMAL:
                if self.in_clip():
                    self.unclip_range()
                #/*gtk_sheet_unselect_range(sheet);*/
                copy = True
            if kname in ('x', 'X') and self.state != gtksheet.SHEET_NORMAL:
                if self.in_clip():
                    self.unclip_range()
                copy = True
        if copy:
            return self._copy_to_clipboard()
        return False

    def _copy_to_clipboard(self):
        range = self.props.selected_range
        colspan = range.coli - range.col0;
        rowspan = range.rowi - range.row0;

        if ((colspan < 0 or rowspan < 0) or (colspan == 0 and rowspan == 0)):
            return False

        buf = ""
        for row in xrange(range.row0, range.rowi+1):
            for col in xrange(range.col0, range.coli+1):
                text = self.cell_get_text(row, col)
                if text:
                    if col == range.coli:
                        buf += "%s\n" % text
                    else:
                        buf += "%s\t" % text
                else:
                    if col == range.coli:
                        buf += "\n"
                    else:
                        buf += "\t"
        clipboard = gtk.clipboard_get(gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(buf)

        return True

class Sheet2(gtksheet.Sheet):
    def __init__(self):
        gtksheet.Sheet.__init__(self, 1000, 26)
        self.props.autoscroll = True
        range = gtksheet.SheetRange(0,0, 2, self.props.n_columns-1)
        self.range_set_editable(range, False)
        self.range_set_background(range, gdk.color_parse("light gray"))
        self.range_set_foreground(range, gdk.color_parse("blue"))
        range.row0 = 1
        self.range_set_foreground(range, gdk.color_parse("red"))
        range.row0 = 2
        self.range_set_foreground(range, gdk.color_parse("black"))
        self.connect("button_press_event", self._do_popup)
        self.connect("set_cell", self._parse_numbers)
        self.set_row_height(12, 60)
        b = gtk.Button("gtk.FILL")        
        self.attach(b, 12, 2, gtk.FILL, gtk.FILL, 5, 5)        
        b = gtk.Button("gtk.EXPAND")        
        self.attach(b, 12, 3, gtk.EXPAND, gtk.EXPAND, 5, 5)
        b = gtk.Button("gtk.SHRINK")        
        self.attach(b, 12, 4, gtk.SHRINK, gtk.SHRINK, 5, 5)

    def _popup_activated_cb(self, widget, title):
        if title == "Append Column":
            self.add_column(1)
        elif title == "Append Row":
            self.add_row(1)
        elif title == "Insert Row":
            if self.props.state == gtksheet.SHEET_ROW_SELECTED:
                self.insert_rows(self.props.selected_range.row0,                       
                                 self.props.selected_range.rowi - self.props.selected_range.row0+1)
        elif title == "Insert Column":
           if self.props.state == gtksheet.SHEET_COLUMN_SELECTED:
                self.insert_columns(self.props.selected_range.col0,                       
                                    self.props.selected_range.coli - self.props.selected_range.col0+1)
        elif title == "Delete Row":
            if self.props.state == gtksheet.SHEET_ROW_SELECTED:
                self.delete_rows(self.props.selected_range.row0,
                                 self.props.selected_range.rowi - self.props.selected_range.row0+1)
        elif title == "Delete Column":
            if self.props.state == gtksheet.SHEET_COLUMN_SELECTED:
                self.delete_columns(self.props.selected_range.col0,
                                         self.props.selected_range.coli - self.props.selected_range.col0+1) 
        elif title == "Clear Cells":
            if self.props.state != gtksheet.SHEET_NORMAL:
                self.range_clear(sheet, self.props.selected_range)
        self._popup.destroy()
        return True


    def _build_menu(self):
        items = ["Append Column",
                 "Append Row",
                 "Insert Row",
                 "Insert Column",
                 "Delete Row",
                 "Delete Column",
                 "Clear Cells"]
        menu = gtk.Menu()
        for i in xrange(len(items)):
            item = gtk.MenuItem(items[i])
            item.connect("activate", self._popup_activated_cb, items[i])
            item.set_flags(gtk.SENSITIVE | gtk.CAN_FOCUS)
            if i in (2,4):
                if self.props.state != gtksheet.SHEET_ROW_SELECTED:
                    item.unset_flags(gtk.SENSITIVE | gtk.CAN_FOCUS)
            elif i in (3,5):
                if self.props.state != gtksheet.SHEET_COLUMN_SELECTED:
                    item.unset_flags(gtk.SENSITIVE | gtk.CAN_FOCUS)
            item.show()
            menu.append(item)
        self._popup = menu

    def _do_popup(self, widget, event):
        x,y,mask = self.window.get_pointer()
        if mask & gdk.BUTTON3_MASK:
            self._build_menu()
            self._popup.popup(None, None, None, event.button, event.time)
            return True

        return False

    def _parse_numbers(self, sheet, row, column):
        attr = self.get_attributes(*self.props.active_cell)
        justification = attr.justification
        label, justification = self._format_text(self.get_entry().get_text(), justification)
        self.set_cell(self.props.active_cell[0], self.props.active_cell[1], justification, label)

    def _format_text(self, text, justification):
        digspace = 0
        val = 0.0
        nonzero = False
        label = ""

        context = self.get_pango_context()
        metrics = context.get_metrics(self.style.font_desc, context.get_language())
        char_width = metrics.get_approximate_char_width()
        cell_width = self.get_column_width(self.props.active_cell[1])
        space = float(cell_width) / char_width

        intspace = int(min(space, DEFAULT_SPACE))
        format = "empty"
        l = len(text)
        if l:
            for nchar in text:
                if nchar in ('.', ' ', ',', '-', '+', 'd', 'D', 'E', 'e', '1', '2',
                            '3', '4', '5', '6', '7', '8', '9'):
                    nonzero = True
                elif nchar == '0':
                    pass
                else:
                    format = "text"
                if format != "empty":
                    break
        try:
            val = float(text)
        except ValueError:
            val = 0.0
        else:
            pass

        if format != "empty" or (val == 0. and nonzero):
            format = "text"
        else:
            format = "numeric"

        if format in ("text", "empty"):
            label = text
            return label, justification
        
        val = float(text)
        justification = gtk.JUSTIFY_RIGHT

        auxval = -val if val < 0 else val
        while auxval < 1 and auxval != 0.:
            auxval = auxval * 10.
            digspace += 1
        if digspace + DEFAULT_PRECISION+1 > intspace or digspace > DEFAULT_PRECISION:
            label = "%*.*E" % (intspace, DEFAULT_PRECISION, val)
        else:
            intspace = min(intspace, len(text)-digspace-1)
            label = "%*.*f" % (intspace, DEFAULT_PRECISION, val)
            if len(label) > space:
                label = "%*.*E" % (intspace, DEFAULT_PRECISION, val)
        return label, justification


class Sheet3(gtksheet.Sheet):
    def __init__(self):
        gtksheet.Sheet.__init__(self, 1000, 26)
        self.show_grid(False)
        range = gtksheet.SheetRange(0,0,10,6)
        self.range_set_background(range, gdk.color_parse("orange"))
        self.range_set_foreground(range, gdk.color_parse("violet"))
        range.row0 = 1
        self.range_set_background(range, gdk.color_parse("blue"))
        range.coli = 0
        self.range_set_background(range, gdk.color_parse("dark green"))
        range.row0 = 0
        color = gdk.color_parse("dark blue")
        self.range_set_background(range, color)
        self.range_set_border_color(range, color)
        self.range_set_border(range, gtksheet.SHEET_RIGHT_BORDER, 4, 1)
        range.coli = 0
        range.col0 = 0
        range.rowi = 0
        self.range_set_background(range, gdk.color_parse("red"))
        self.range_set_border(range, gtksheet.SHEET_RIGHT_BORDER | gtksheet.SHEET_BOTTOM_BORDER, 4, 0)
        range.rowi = 0
        range.col0 = 1
        range.coli = 6
        self.range_set_border_color(range, gdk.color_parse("dark blue"))
        self.range_set_border(range, gtksheet.SHEET_BOTTOM_BORDER, 4, 1)
        self.props.autoresize = True
        self.change_entry(gtk.Combo)
        self.connect("traverse", self._change_entry)
        self.current_index = 0
        self.types = [gtk.Combo, gtk.Entry, gtk.SpinButton, gtksheet.ItemEntry]

    def _change_entry(self, sheet, row, col, new_row, new_col):
        if self.props.state == gtksheet.SHEET_NORMAL:
            self.current_index = (self.current_index + 1) % len(self.types)
            self.change_entry(self.types[self.current_index])
        return True
              
class TestMainWindow(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        self.set_title("python-gtksheet demo")
        self.set_size_request(500, 500)
        self.connect("delete_event", lambda x,y: gtk.main_quit())

        # Create the show/hide row and column titles buttons
        hrt = gtk.Button("Hide Row Titles")
        hct = gtk.Button("Hide Column Titles")
        srt = gtk.Button("Show Row Titles")
        sct = gtk.Button("Show Column Titles")

        shb = gtk.HBox(False, 1)
        shb.pack_start(hrt, True, True, 0)
        shb.pack_start(hct, True, True, 0)
        shb.pack_start(srt, True, True, 0)
        shb.pack_start(sct, True, True, 0)

        hrt.connect("clicked", self._hide_row_titles)
        hct.connect("clicked", self._hide_column_titles)
        srt.connect("clicked", self._show_row_titles)
        sct.connect("clicked", self._show_column_titles)

        #Create the sheets
        self.notebook = gtk.Notebook()
        self.notebook.set_tab_pos(gtk.POS_BOTTOM)

        self.sheets = [Sheet1(), Sheet2(), Sheet3(), ]
        for sheet, i in zip(self.sheets, xrange(len(self.sheets))):
            sheet.show()
            sheet.connect("activate", self._activate_sheet_cell_cb)
            sheet.connect("changed", self._show_entry_cb)
            scrwin = gtk.ScrolledWindow()
            label = gtk.Label("Example %d" % (i+1))
            scrwin.add(sheet)
            self.notebook.append_page(scrwin, label)
                
        # Create the toolbar
        self._create_toolbar()

        # Create the spreadsheet entry */

        status_box = gtk.HBox(False, 1)
        status_box.set_border_width(0)
        
        self.location = gtk.Label("")
        req_width, req_height = self.location.size_request()
        self.location.set_size_request(160, req_height)
        status_box.pack_start(self.location, False, True, 0)

        self.entry  = gtk.Entry() 
        status_box.pack_start(self.entry, True, True, 0)

        self.entry.connect("activate", self._activate_entry_cb)

        # Pack widgets
        main_vbox = gtk.VBox(False, 1)
        main_vbox.pack_start(shb, False, False, 0)
        main_vbox.pack_start(self.toolbar, False, False, 0)
        main_vbox.pack_start(status_box, False, True, 0)
        main_vbox.pack_start(self.notebook, True, True, 0)

        self.add(main_vbox)
        self.show_all()

    def _create_toolbar(self):
        def _add_widget_to_toolbar(widget, separator, tooltip):
            ti = gtk.ToolItem()
            ti.add(widget)
            if tooltip:
                ti.set_tooltip_text(tooltip)
            self.toolbar.insert(ti, -1)
            if separator:
                self.toolbar.insert(gtk.SeparatorToolItem(), -1)

        self.toolbar = gtk.Toolbar()
        self.tooltips = gtk.Tooltips()

        #font button
        self.font_button = gtk.FontButton()
        self.font_button.connect("font-set", self._font_changed_cb)
        _add_widget_to_toolbar(self.font_button, True, 
                               "Change the font of the selected cells")

        # text justification buttons
        self.justify_left = gtk.Action("justleft", None,
                                        "Justify selected cells to the left",
                                        gtk.STOCK_JUSTIFY_LEFT)
        self.justify_left.connect("activate", self._justify_cb, gtk.JUSTIFY_LEFT)
        self.toolbar.insert(self.justify_left.create_tool_item(), -1)

        self.justify_center = gtk.Action("justcenter",  None,
                                         "Justify selected cells to the center",
                                         gtk.STOCK_JUSTIFY_CENTER)
        self.justify_center.connect("activate", self._justify_cb, gtk.JUSTIFY_CENTER)
        self.toolbar.insert(self.justify_center.create_tool_item(), -1)
        

        self.justify_right = gtk.Action("justright",  None,
                                        "Justify selected cells to the right",
                                        gtk.STOCK_JUSTIFY_RIGHT)
        self.justify_right.connect("activate", self._justify_cb, gtk.JUSTIFY_RIGHT)
        self.toolbar.insert(self.justify_right.create_tool_item(), -1)
        self.toolbar.insert(gtk.SeparatorToolItem(), -1)

        # background/foreground color buttons
        self.fg_color_button = gtk.ColorButton()
        self.fg_color_button.connect("color-set", self._color_changed_cb)
        _add_widget_to_toolbar(self.fg_color_button, False, 
                            "Change the foreground color of the selected cells")

        self.bg_color_button = gtk.ColorButton()
        self.bg_color_button.connect("color-set", self._color_changed_cb)
        _add_widget_to_toolbar(self.bg_color_button, True, 
                            "Change the background color of the selected cells")

        # Create the combo box */
        self.border_combo = BorderCombo()
        self.border_combo.connect("changed", self._border_changed_cb)
        _add_widget_to_toolbar(self.border_combo, False,
                              tooltip="Change the border of the selected cells")

    def get_current_sheet(self):
        page = self.notebook.get_current_page()
        if page < 0 or page >= len(self.sheets):
            return None
        else:
            return self.sheets[page]

    def _hide_row_titles(self, widget):
        sheet = self.get_current_sheet()
        if sheet:
            self.sheet.hide_row_titles()

    def _hide_column_titles(self, widget):
        sheet = self.get_current_sheet()
        if sheet:
            self.sheet.hide_column_titles()

    def _show_row_titles(self, widget):
        sheet = self.get_current_sheet()
        if sheet:
            self.sheet.show_row_titles()

    def _show_column_titles(self, widget):
        sheet = self.get_current_sheet()
        if sheet:
            self.sheet.show_column_titles()

    def _activate_sheet_cell_cb(self, widget, row, col):
        sheet = self.get_current_sheet()
        if sheet is None:
            return
        
        coltitle = sheet.get_column_title(col)
        rowtitle = sheet.get_column_title(row)
        if coltitle and rowtitle:
            cell = "   %s:%s   " % (coltitle, rowtitle)
        elif coltitle:
            cell = "   %s:%d   " % (coltitle, row)
        elif rowtitle:
            cell = "   %d:%s   " % (col, rowtitle)
        else:
            cell = "   %d:%d   " % (col, row)
        self.location.set_text(cell)
        
        text = sheet.cell_get_text(row, col)
        if text:
            self.entry.set_text(text)
        else:
            self.entry.set_text("")
        
        attrs = sheet.get_attributes(row, col)
        self.entry.set_editable(attrs.is_editable)
        
        font_desc = widget.style.font_desc if not attrs.font_desc else attrs.font_desc
        font_name = font_desc.to_string()
        self.font_button.set_font_name(font_name)
        
        self.bg_color_button.set_color(attrs.background)
        self.fg_color_button.set_color(attrs.foreground)

        return True

    def _show_entry_cb(self, widget, row, col):
        if not widget.flags() & gtk.HAS_FOCUS:
            return
        sheet = self.get_current_sheet()
        if sheet is None:
            return

        sheet_entry = sheet.get_entry()
    
        text = sheet_entry.get_text()
        self.entry.set_text(text)

    def _activate_entry_cb(self, widget):
        sheet = self.get_current_sheet()
        if sheet is None:
            return
        sheet_entry = sheet.get_entry()
        row, col = sheet.props.active_cell
        if isinstance (sheet_entry, gtksheet.ItemEntry):
            justification = sheet_entry.props.justification

        sheet.set_cell(row, col, justification, sheet_entry.get_text())
        
    def _font_changed_cb(self, widget):
        sheet = self.get_current_sheet()
        if sheet is None:
            return  
        r = sheet.props.selected_range
        fd = pango.FontDescription(widget.get_font_name())
        sheet.range_set_font(r, fd)

    def _justify_cb(self, widget, data=None):
        if data is None:
            return
        sheet = self.get_current_sheet()
        if sheet is None:
            return    
        sheet.range_set_justification(sheet.props.selected_range, data)

    def _color_changed_cb(self, widget):
        sheet = self.get_current_sheet()
        if sheet is None:
            return
        color = widget.get_color()
        if widget == self.bg_color_button:
            sheet.range_set_background(sheet.props.selected_range, color)
        elif widget == self.fg_color_button:
            sheet.range_set_foreground(sheet.props.selected_range, color)

    def _border_changed_cb(self, widget):
        sheet = self.get_current_sheet()
        if sheet is None:
            return
        border = widget.get_active()
        range = sheet.props.selected_range
        border_width = 3
        sheet.range_set_border(range, 0, 0)
        if border == 1:
            border_mask = gtksheet.SHEET_TOP_BORDER
            range.rowi = range.row0
            sheet.range_set_border(range, border_mask, border_width)
        elif border == 2:
            border_mask = gtksheet.SHEET_BOTTOM_BORDER
            range.row0 = range.rowi
            sheet.range_set_border(range, border_mask, border_width)
        elif border == 3:
            border_mask = gtksheet.SHEET_RIGHT_BORDER
            range.col0 = range.coli
            sheet.range_set_border(range, border_mask, border_width)
        elif border == 4:
            border_mask = gtksheet.SHEET_LEFT_BORDER
            range.coli = range.col0
            sheet.range_set_border(range, border_mask, border_width)
        elif border == 5:
            if range.col0 == range.coli:
                border_mask = gtksheet.SHEET_LEFT_BORDER | gtksheet.SHEET_RIGHT_BORDER
                sheet.range_set_border(range, border_mask, border_width)
            else:
                border_mask = gtksheet.SHEET_LEFT_BORDER
                auxcol = range.coli
                range.coli = range.col0
                sheet.range_set_border(range, border_mask, border_width)
                border_mask = gtksheet.SHEET_RIGHT_BORDER
                range.col0 = range.coli = auxcol
                sheet.range_set_border(range, border_mask, border_width)
        elif border == 6:
            if range.row0 == range.rowi:
                border_mask = gtksheet.SHEET_TOP_BORDER | gtksheet.SHEET_BOTTOM_BORDER
                sheet.range_set_border(range, border_mask, border_width)
            else:
                border_mask = gtksheet.SHEET_TOP_BORDER
                auxrow = range.rowi
                range.rowi = range.row0
                sheet.range_set_border(range, border_mask, border_width)
                border_mask = gtksheet.SHEET_BOTTOM_BORDER
                range.row0 = range.rowi = auxrow
                sheet.range_set_border(range, border_mask, border_width)
        elif border == 7:
            border_mask = gtksheet.SHEET_RIGHT_BORDER | gtksheet.SHEET_LEFT_BORDER
            sheet.range_set_border(range, border_mask, border_width)
        elif border == 8:
            border_mask = gtksheet.SHEET_BOTTOM_BORDER | gtksheet.SHEET_TOP_BORDER
            sheet.range_set_border(range, border_mask, border_width)
        elif border == 9:
            sheet.range_set_border(range, 15, border_width)
            for i in xrange(range.row0, range.rowi + 1):
                for j in xrange(range.col0, range.coli + 1):
                    border_mask = 15
                    auxrange = sheet.SheetRange(i, j, i, j)
                    if i == range.rowi:
                        border_mask = border_mask ^ gtksheet.SHEET_BOTTOM_BORDER
                    if i == range.row0:
                        border_mask = border_mask ^ gtksheet.SHEET_TOP_BORDER
                    if j == range.coli:
                        border_mask = border_mask ^ gtksheet.SHEET_RIGHT_BORDER
                    if j == range.col0:
                        border_mask = border_mask ^ gtksheet.SHEET_LEFT_BORDER
                    if border_mask != 15:
                        sheet.range_set_border(auxrange, border_mask,
                                               border_width)
        elif border == 10:
            for i in xrange(range.row0, range.rowi + 1):
                for j in xrange(range.col0, range.coli + 1):
                    border_mask = 0
                    auxrange = gtksheet.SheetRange(i, j, i, j)
                    if i == range.rowi:
                        border_mask = border_mask | gtksheet.SHEET_BOTTOM_BORDER
                    if i == range.row0:
                        border_mask = border_mask | gtksheet.SHEET_TOP_BORDER
                    if j == range.coli:
                        border_mask = border_mask | gtksheet.SHEET_RIGHT_BORDER
                    if j == range.col0:
                        border_mask = border_mask | gtksheet.SHEET_LEFT_BORDER
                    if border_mask != 0:
                        sheet.range_set_border(auxrange, border_mask,
                                               border_width)
        elif border == 11:
            border_mask = 15
            sheet.range_set_border(range, border_mask, border_width)

if __name__=="__main__":
    w = TestMainWindow()
    gtk.main()
