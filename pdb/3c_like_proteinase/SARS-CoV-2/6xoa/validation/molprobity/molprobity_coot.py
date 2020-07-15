# script auto-generated by phenix.molprobity


from __future__ import absolute_import, division, print_function
from six.moves import cPickle as pickle
from six.moves import range
try :
  import gobject
except ImportError :
  gobject = None
import sys

class coot_extension_gui(object):
  def __init__(self, title):
    import gtk
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    scrolled_win = gtk.ScrolledWindow()
    self.outside_vbox = gtk.VBox(False, 2)
    self.inside_vbox = gtk.VBox(False, 0)
    self.window.set_title(title)
    self.inside_vbox.set_border_width(0)
    self.window.add(self.outside_vbox)
    self.outside_vbox.pack_start(scrolled_win, True, True, 0)
    scrolled_win.add_with_viewport(self.inside_vbox)
    scrolled_win.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

  def finish_window(self):
    import gtk
    self.outside_vbox.set_border_width(2)
    ok_button = gtk.Button("  Close  ")
    self.outside_vbox.pack_end(ok_button, False, False, 0)
    ok_button.connect("clicked", lambda b: self.destroy_window())
    self.window.connect("delete_event", lambda a, b: self.destroy_window())
    self.window.show_all()

  def destroy_window(self, *args):
    self.window.destroy()
    self.window = None

  def confirm_data(self, data):
    for data_key in self.data_keys :
      outlier_list = data.get(data_key)
      if outlier_list is not None and len(outlier_list) > 0 :
        return True
    return False

  def create_property_lists(self, data):
    import gtk
    for data_key in self.data_keys :
      outlier_list = data[data_key]
      if outlier_list is None or len(outlier_list) == 0 :
        continue
      else :
        frame = gtk.Frame(self.data_titles[data_key])
        vbox = gtk.VBox(False, 2)
        frame.set_border_width(6)
        frame.add(vbox)
        self.add_top_widgets(data_key, vbox)
        self.inside_vbox.pack_start(frame, False, False, 5)
        list_obj = residue_properties_list(
          columns=self.data_names[data_key],
          column_types=self.data_types[data_key],
          rows=outlier_list,
          box=vbox)

# Molprobity result viewer
class coot_molprobity_todo_list_gui(coot_extension_gui):
  data_keys = [ "rama", "rota", "cbeta", "probe" ]
  data_titles = { "rama"  : "Ramachandran outliers",
                  "rota"  : "Rotamer outliers",
                  "cbeta" : "C-beta outliers",
                  "probe" : "Severe clashes" }
  data_names = { "rama"  : ["Chain", "Residue", "Name", "Score"],
                 "rota"  : ["Chain", "Residue", "Name", "Score"],
                 "cbeta" : ["Chain", "Residue", "Name", "Conf.", "Deviation"],
                 "probe" : ["Atom 1", "Atom 2", "Overlap"] }
  if (gobject is not None):
    data_types = { "rama" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "rota" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "cbeta" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT],
                   "probe" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT] }
  else :
    data_types = dict([ (s, []) for s in ["rama","rota","cbeta","probe"] ])

  def __init__(self, data_file=None, data=None):
    assert ([data, data_file].count(None) == 1)
    if (data is None):
      data = load_pkl(data_file)
    if not self.confirm_data(data):
      return
    coot_extension_gui.__init__(self, "MolProbity to-do list")
    self.dots_btn = None
    self.dots2_btn = None
    self._overlaps_only = True
    self.window.set_default_size(420, 600)
    self.create_property_lists(data)
    self.finish_window()

  def add_top_widgets(self, data_key, box):
    import gtk
    if data_key == "probe" :
      hbox = gtk.HBox(False, 2)
      self.dots_btn = gtk.CheckButton("Show Probe dots")
      hbox.pack_start(self.dots_btn, False, False, 5)
      self.dots_btn.connect("toggled", self.toggle_probe_dots)
      self.dots2_btn = gtk.CheckButton("Overlaps only")
      hbox.pack_start(self.dots2_btn, False, False, 5)
      self.dots2_btn.connect("toggled", self.toggle_all_probe_dots)
      self.dots2_btn.set_active(True)
      self.toggle_probe_dots()
      box.pack_start(hbox, False, False, 0)

  def toggle_probe_dots(self, *args):
    if self.dots_btn is not None :
      show_dots = self.dots_btn.get_active()
      overlaps_only = self.dots2_btn.get_active()
      if show_dots :
        self.dots2_btn.set_sensitive(True)
      else :
        self.dots2_btn.set_sensitive(False)
      show_probe_dots(show_dots, overlaps_only)

  def toggle_all_probe_dots(self, *args):
    if self.dots2_btn is not None :
      self._overlaps_only = self.dots2_btn.get_active()
      self.toggle_probe_dots()

class rsc_todo_list_gui(coot_extension_gui):
  data_keys = ["by_res", "by_atom"]
  data_titles = ["Real-space correlation by residue",
                 "Real-space correlation by atom"]
  data_names = {}
  data_types = {}

class residue_properties_list(object):
  def __init__(self, columns, column_types, rows, box,
      default_size=(380,200)):
    assert len(columns) == (len(column_types) - 1)
    if (len(rows) > 0) and (len(rows[0]) != len(column_types)):
      raise RuntimeError("Wrong number of rows:\n%s" % str(rows[0]))
    import gtk
    self.liststore = gtk.ListStore(*column_types)
    self.listmodel = gtk.TreeModelSort(self.liststore)
    self.listctrl = gtk.TreeView(self.listmodel)
    self.listctrl.column = [None]*len(columns)
    self.listctrl.cell = [None]*len(columns)
    for i, column_label in enumerate(columns):
      cell = gtk.CellRendererText()
      column = gtk.TreeViewColumn(column_label)
      self.listctrl.append_column(column)
      column.set_sort_column_id(i)
      column.pack_start(cell, True)
      column.set_attributes(cell, text=i)
    self.listctrl.get_selection().set_mode(gtk.SELECTION_SINGLE)
    for row in rows :
      self.listmodel.get_model().append(row)
    self.listctrl.connect("cursor-changed", self.OnChange)
    sw = gtk.ScrolledWindow()
    w, h = default_size
    if len(rows) > 10 :
      sw.set_size_request(w, h)
    else :
      sw.set_size_request(w, 30 + (20 * len(rows)))
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    box.pack_start(sw, False, False, 5)
    inside_vbox = gtk.VBox(False, 0)
    sw.add(self.listctrl)

  def OnChange(self, treeview):
    import coot # import dependency
    selection = self.listctrl.get_selection()
    (model, tree_iter) = selection.get_selected()
    if tree_iter is not None :
      row = model[tree_iter]
      xyz = row[-1]
      if isinstance(xyz, tuple) and len(xyz) == 3 :
        set_rotation_centre(*xyz)
        set_zoom(30)
        graphics_draw()

def show_probe_dots(show_dots, overlaps_only):
  import coot # import dependency
  n_objects = number_of_generic_objects()
  sys.stdout.flush()
  if show_dots :
    for object_number in range(n_objects):
      obj_name = generic_object_name(object_number)
      if overlaps_only and not obj_name in ["small overlap", "bad overlap"] :
        sys.stdout.flush()
        set_display_generic_object(object_number, 0)
      else :
        set_display_generic_object(object_number, 1)
  else :
    sys.stdout.flush()
    for object_number in range(n_objects):
      set_display_generic_object(object_number, 0)

def load_pkl(file_name):
  pkl = open(file_name, "rb")
  data = pickle.load(pkl)
  pkl.close()
  return data

data = {}
data['rama'] = [('A', ' 154 ', 'TYR', 0.03396580210594782, (5.254999999999999, -5.756000000000002, -17.056)), ('B', ' 154 ', 'TYR', 0.024617497625975027, (26.397999999999993, -4.356, 4.519)), ('D', ' 154 ', 'TYR', 0.03198182487175621, (-29.597000000000005, -20.045, -34.232))]
data['omega'] = []
data['rota'] = [('A', '  27 ', 'LEU', 0.2244848081883783, (12.718000000000007, 12.121, 5.071)), ('A', ' 152 ', 'ILE', 0.2507287004435478, (4.536999999999996, -3.483000000000001, -11.562)), ('A', ' 169 ', 'THR', 0.06575076573765876, (-3.1289999999999982, 2.235, 17.18)), ('A', ' 240 ', 'GLU', 0.24777720439789896, (-16.593999999999994, -7.42, 4.782)), ('A', ' 286 ', 'LEU', 0.2974608077867348, (-5.403000000000001, -17.803, 11.24)), ('B', '  18 ', 'VAL', 0.018414118843153214, (19.465000000000003, -13.495000000000001, -17.64)), ('B', '  76 ', 'ARG', 0.08102947251897828, (27.810000000000002, -14.329, -27.06)), ('B', ' 222 ', 'ARG', 0.010170796931930546, (8.655, -16.064, 36.435)), ('B', ' 256 ', 'GLN', 0.24484567056474557, (18.525999999999986, -4.664, 24.929)), ('B', ' 286 ', 'LEU', 0.27504050163939475, (1.8339999999999956, -19.92, 15.884)), ('C', '  49 ', 'MET', 0.0, (-3.72, -33.782, -16.389)), ('C', '  55 ', 'GLU', 0.23058328123454233, (-0.2020000000000099, -44.086, -24.457)), ('C', '  60 ', 'ARG', 0.0, (-7.597000000000013, -48.88300000000002, -22.126)), ('C', '  87 ', 'LEU', 0.1373936883916286, (-6.628000000000004, -38.221, -31.691)), ('C', '  90 ', 'LYS', 0.2328200090770454, (-12.114, -43.64400000000001, -37.525)), ('C', ' 238 ', 'ASN', 0.05119545683297683, (11.327000000000004, -5.341, -29.619)), ('D', '  46 ', 'SER', 0.04200607543550623, (-21.205, 3.4049999999999976, -67.478)), ('D', '  72 ', 'ASN', 0.26203743227407805, (-21.545, -21.848, -62.841)), ('D', '  76 ', 'ARG', 0.0032093831274109543, (-33.379, -18.993000000000006, -65.923)), ('D', ' 130 ', 'MET', 0.0890535095085662, (-23.967, 1.0399999999999991, -38.997)), ('D', ' 137 ', 'LYS', 0.0, (-16.463, 1.3740000000000006, -42.747)), ('D', ' 165 ', 'MET', 0.0008382461561084437, (-21.734, 2.037000000000001, -53.881)), ('D', ' 169 ', 'THR', 0.1576785574394322, (-14.552999999999997, 9.676000000000005, -48.519)), ('D', ' 222 ', 'ARG', 0.0008745803696337331, (-14.866, 4.821, -6.971)), ('D', ' 226 ', 'THR', 0.053037411998957396, (-26.200999999999993, 9.849, -12.943)), ('D', ' 232 ', 'LEU', 0.08304340383823268, (-23.735999999999997, 16.306000000000004, -20.333999999999996)), ('D', ' 306 ', 'GLN', 0.10183164311107379, (-26.809, -24.44900000000001, -35.842))]
data['cbeta'] = []
data['probe'] = [(' B  22  CYS  SG ', ' B  61  LYS  NZ ', -0.771, (21.666, -27.419, -25.51)), (' D 126  TYR  HA ', ' D 401  EDO  H22', -0.634, (-14.539, -10.027, -40.078)), (' C   4  ARG HH12', ' D 128  CYS  HB3', -0.596, (-16.911, -3.614, -40.967)), (' D  49  MET  HB3', ' D 189  GLN  HG3', -0.592, (-23.062, 5.865, -61.923)), (' C  49  MET  HB3', ' C 189  GLN  HB2', -0.591, (-3.326, -30.668, -16.206)), (' B 109  GLY  HA2', ' B 200  ILE HD13', -0.581, (16.641, -21.856, 9.975)), (' D 109  GLY  HA2', ' D 200  ILE HD13', -0.575, (-23.261, 2.066, -33.813)), (' D  30  LEU HD22', ' D 148  VAL HG11', -0.569, (-28.473, -10.403, -49.754)), (' A 285  ALA  HB3', ' B 285  ALA  HB3', -0.561, (-2.615, -19.015, 14.074)), (' B  40  ARG  HA ', ' B  87  LEU  HG ', -0.554, (24.37, -27.121, -16.635)), (' C  12  LYS  HE3', ' C 155  ASP  HA ', -0.54, (-13.693, -23.354, -51.67)), (' C   4  ARG  O  ', ' C 299  GLN  NE2', -0.539, (-8.924, -7.044, -44.548)), (' C  44  CYS  HB3', ' C  48  ASP  HB2', -0.535, (-6.335, -37.215, -18.216)), (' D 186  VAL HG11', ' D 188  ARG HH21', -0.526, (-31.613, 10.267, -55.291)), (' C  21  THR  HB ', ' C  67  LEU  HB2', -0.525, (-19.661, -38.547, -27.015)), (' C 115  LEU HD11', ' C 122  PRO  HB3', -0.521, (-18.566, -21.922, -37.21)), (' A 109  GLY  HA2', ' A 200  ILE HD13', -0.517, (-8.696, -5.7, 0.832)), (' C 166  GLU  OE2', ' D   1  SER  N  ', -0.514, (-9.788, -17.844, -22.625)), (' D  27  LEU HD21', ' D  42  VAL  HB ', -0.51, (-26.234, -4.65, -60.637)), (' D  58  LEU HD22', ' D  82  MET  HE3', -0.509, (-36.825, -1.574, -62.192)), (' D  72  ASN  ND2', ' D  72  ASN  O  ', -0.506, (-21.877, -22.384, -65.575)), (' C  86  VAL HG13', ' C 179  GLY  HA2', -0.505, (-2.425, -33.11, -33.024)), (' B 111  THR HG22', ' B 129  ALA  HB2', -0.504, (14.83, -18.353, 7.083)), (' B  44  CYS  HB3', ' B  48  ASP  HB2', -0.499, (18.065, -34.354, -20.037)), (' A 140  PHE  O  ', ' B   1  SER  N  ', -0.499, (6.908, 2.075, 13.145)), (' D  54  TYR  HB3', ' D  82  MET  HE1', -0.497, (-34.872, 0.497, -62.051)), (' C 109  GLY  HA2', ' C 200  ILE HD13', -0.485, (3.927, -12.82, -37.735)), (' B 102  LYS  HG3', ' B 156  CYS  SG ', -0.481, (30.504, -10.384, -1.474)), (' C  58  LEU HD22', ' C  82  MET  HB2', -0.48, (-3.509, -42.476, -29.41)), (' A 169  THR HG22', ' A 171  VAL HG22', -0.477, (-3.843, 2.026, 13.858)), (' B 102  LYS  HB2', ' B 102  LYS  HE3', -0.471, (29.132, -13.031, -0.215)), (' D 211  ALA  HB1', ' D 216  ASP  HB3', -0.468, (-10.343, -4.474, -20.411)), (' B  49  MET  HA ', ' B  49  MET  HE2', -0.459, (17.519, -35.017, -16.241)), (' B  44  CYS  HB2', ' B  49  MET  HE3', -0.456, (18.047, -33.108, -17.688)), (' D 111  THR HG22', ' D 129  ALA  HB2', -0.455, (-20.996, -2.343, -35.536)), (' C  55  GLU  H  ', ' C  55  GLU  HG3', -0.449, (1.498, -42.198, -23.672)), (' D  10  SER  O  ', ' D  14  GLU  HG3', -0.449, (-21.326, -18.227, -46.291)), (' A 249  ILE HD11', ' D 217  ARG  CZ ', -0.445, (-12.879, -7.236, -11.216)), (' C 285  ALA  HB3', ' D 285  ALA  HB3', -0.443, (-4.234, 3.738, -30.493)), (' D  95  ASN  HB3', ' D  98  THR  OG1', -0.435, (-33.202, -20.978, -51.427)), (' A 102  LYS  HE3', ' D 279  ARG  HG2', -0.435, (-0.485, 2.803, -18.472)), (' A 305  PHE  HE2', ' C  49  MET  HE2', -0.434, (-4.397, -32.045, -20.45)), (' D  41  HIS  HA ', ' D  54  TYR  HE1', -0.433, (-29.643, 1.015, -61.579)), (' C 111  THR HG22', ' C 129  ALA  HB2', -0.433, (-1.543, -12.728, -38.408)), (' D 169  THR HG23', ' D 171  VAL HG22', -0.43, (-17.241, 8.018, -47.075)), (' A  39  PRO  HB3', ' A 164  HIS  CD2', -0.428, (3.708, 13.462, 3.746)), (' A 305  PHE  CE2', ' C  49  MET  HG3', -0.427, (-4.691, -31.345, -18.978)), (' C 210  ALA  HB2', ' C 296  VAL HG13', -0.425, (-1.799, -3.712, -47.742)), (' B   5  LYS  HD2', ' B 291  PHE  CZ ', -0.423, (8.899, -12.562, 9.113)), (' D 226  THR  OG1', ' D 227  LEU  N  ', -0.422, (-27.738, 10.407, -14.317)), (' A   8  PHE  HB3', ' A 152  ILE HD13', -0.419, (7.206, -4.409, -8.721)), (' A 175  THR HG22', ' A 181  PHE  HA ', -0.411, (-3.357, 11.101, 1.526)), (' D 245  ASP  O  ', ' D 249  ILE HG13', -0.409, (-31.288, -0.673, -23.255)), (' A 140  PHE  HB2', ' A 172  HIS  NE2', -0.409, (4.751, 2.554, 10.183)), (' A 207  TRP  HZ3', ' A 287  LEU HD23', -0.408, (-7.984, -19.038, 6.648)), (' D  59  ILE  HA ', ' D  59  ILE HD12', -0.406, (-40.602, -2.549, -68.875)), (' A 297  VAL HG13', ' A 301  SER  HB3', -0.405, (-3.505, -17.75, -12.472)), (' B 111  THR  OG1', ' B 295  ASP  OD2', -0.404, (17.155, -13.874, 7.917)), (' B  27  LEU  HB2', ' B 145  SER  O  ', -0.403, (16.162, -21.719, -14.617)), (' C 118  TYR  CE1', ' C 144  SER  HB3', -0.401, (-14.531, -22.451, -27.087)), (' D   3  PHE  HB2', ' D 214  ASN  ND2', -0.4, (-11.896, -9.794, -24.204)), (' C   5  LYS  HB3', ' C 401  EDO  H22', -0.4, (-10.625, -6.507, -38.142))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
