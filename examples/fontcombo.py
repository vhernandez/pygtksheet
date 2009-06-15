import gtk
from gtk import gdk
import gobject

class FontFamilyCombo(gtk.ComboBox):
    __gtype_name__ = "FontFamilyCombo"

    __gproperties__ = {\
        'use_font': (gobject.TYPE_BOOLEAN,
                      'Reder entries using corresponding font families',
                      'If true, entries will be rendered using their'\
                      'correspoding font family names.',
                      False,                                        
                      gobject.PARAM_READWRITE)             
        }

    __gsignals__ = {\
        'family_set' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                       (gobject.TYPE_STRING,))
        }

    def __init__(self, use_font=False):
        gtk.ComboBox.__init__(self)
        model = gtk.ListStore(gobject.TYPE_STRING)        
        context = self.create_pango_context()
        for family in context.list_families():
            name = family.get_name()
            if name:
                model.append([name])        
        self._model = model

        sort_model = gtk.TreeModelSort(model)
        sort_model.set_sort_column_id(0, gtk.SORT_ASCENDING)
        self._sort_model = sort_model
    
        self.set_model(sort_model)

        cell = gtk.CellRendererText()
        self.pack_start(cell, True)
        self.add_attribute(cell, "text", 0)
        if use_font:
            self.add_attribute(cell, "family", 0)
        self._cell = cell

        self._use_font = use_font
    
        self.connect("changed", self._changed_cb)

    def do_get_properties(self, prop):
        if prop.name == 'use-font':
            return self._use_font
        else:
            raise AttributeError, 'unknown property %s' % prop.name

    def do_set_properties(self, prop, value):
        if prop.name == 'use-font':
            self.set_use_font(value)
        else:
            raise AttributeError, 'unknown property %s' % prop.name

    def _changed_cb(self, widget):
        family = self.get_font_family()
        if family:
            self.emit("family-set", family)

    def set_use_font(self, use_font):
        if use_font != self._use_font:
            if use_font:
                self.add_attribute(self._cell, "family",0)
            else:
                self.clear_attributes(self._cell)
                self.add_attribute(self._cell, "text", 0)
            self._use_font = use_font

    def get_font_family(self):
        model = self.props.model
        _iter = self.get_active_iter()
        if _iter:
            family = model.get(_iter, 0)
            return family[0]
        else:
            return None

    def set_font_family(self, family):
        """
        Sets 'family' as the selected font family in the combo box.
        Returns True if success.
        """
        model = self.props.model
        _iter = model.get_iter_first()
        while _iter is not None:
            our_fam = model.get(_iter, 0)[0]
            if our_fam == family:
                self.set_active_iter(_iter)
                return True
            _iter = model.iter_next(_iter)
        return False

if __name__ == "__main__":
    def _family_set_cb(widget, family):
        print "Family set to:", family
    w = gtk.Window()    
    f = FontFamilyCombo(use_font=True)
    f.set_font_family("Sans")
    f.connect("family-set", _family_set_cb)
    b = gtk.ToggleButton("Use font")
    b.props.active = True
    b.connect("toggled",
              lambda widget: f.set_use_font(widget.props.active))
    h = gtk.HBox()
    h.pack_start(b, False, False, 0)
    h.pack_start(f, True, True, 0)
    w.add(h)
    w.show_all()
    w.connect("delete_event", lambda x,y: gtk.main_quit())
    gtk.main()
        

