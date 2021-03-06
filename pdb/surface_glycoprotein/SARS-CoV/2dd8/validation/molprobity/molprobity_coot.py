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
data['rama'] = [('H', '   3 ', 'GLN', 0.027812000633922373, (59.03799999999999, -20.626, 36.758)), ('L', '  11 ', 'VAL', 0.08294233543784496, (50.371000000000016, -42.855, 15.777000000000001)), ('L', ' 152 ', 'ASP', 0.027688590561892136, (7.7920000000000025, -38.3, 34.271)), ('S', ' 370 ', 'SER', 0.02290358434183345, (74.71000000000002, -25.16, -6.76)), ('S', ' 507 ', 'PRO', 0.03551655974723188, (91.897, -18.736, -17.702))]
data['omega'] = [('H', ' 147 ', 'PRO', None, (33.623, -14.731999999999996, 28.302)), ('H', ' 149 ', 'PRO', None, (38.052000000000014, -18.335, 30.331)), ('L', ' 142 ', 'PRO', None, (35.82700000000001, -46.677000000000014, 27.005)), ('S', ' 470 ', 'PRO', None, (79.89399999999998, 15.172, 24.093))]
data['rota'] = [('H', '  35 ', 'SER', 0.038234357584048764, (59.901000000000025, -16.133, 23.753)), ('H', '  56 ', 'ILE', 0.0, (66.355, -5.909000000000002, 21.846)), ('H', '  96 ', 'THR', 0.07697488112976009, (67.03, -22.926, 25.334)), ('H', '  97 ', 'VAL', 0.012832687002440628, (70.635, -22.258, 24.37)), ('H', ' 100A', 'MET', 0.1130177275641385, (62.161, -23.453, 24.596)), ('H', ' 112 ', 'SER', 0.21579370137939832, (34.988000000000014, -11.31, 19.756)), ('H', ' 124 ', 'LEU', 0.0004723435739584672, (24.759, -28.138, 44.439)), ('H', ' 138 ', 'LEU', 0.0014488058697806586, (28.312000000000005, -31.433, 46.711)), ('H', ' 141 ', 'LEU', 0.0017382279611616912, (26.926, -24.573, 39.244)), ('H', ' 150 ', 'VAL', 0.18282995480014266, (36.839, -19.831999999999994, 34.804)), ('H', ' 160 ', 'THR', 0.09643958769729669, (42.016, -30.48, 47.078)), ('H', ' 178 ', 'LEU', 0.1314343415721962, (30.388000000000005, -25.676999999999992, 34.121)), ('H', ' 189 ', 'LEU', 0.018913579907862056, (29.210000000000015, -32.449, 56.384)), ('L', '  18 ', 'THR', 0.17155219502026509, (57.40900000000001, -48.433, 21.816)), ('L', '  26 ', 'ASN', 0.16035736212341595, (65.461, -30.408, 4.796)), ('L', '  95 ', 'SER', 0.0872265001505859, (62.219, -18.705, 9.58)), ('L', ' 127 ', 'GLN', 0.16549479460214134, (14.827000000000004, -16.512, 41.815)), ('S', ' 323 ', 'CYS', 0.07044317753318921, (93.73500000000003, -23.685000000000002, -1.379)), ('S', ' 337 ', 'VAL', 0.003150532575091347, (80.778, -6.933, 9.962)), ('S', ' 345 ', 'ILE', 0.17901404542917582, (92.062, -17.264, -3.437)), ('S', ' 356 ', 'TYR', 0.0008115630863952718, (79.932, -29.123, 1.371)), ('S', ' 431 ', 'THR', 0.05872186230579542, (80.966, -14.864000000000003, 27.13)), ('S', ' 463 ', 'ASP', 0.25094233157833207, (72.39, 16.958999999999993, 8.955)), ('S', ' 475 ', 'TYR', 0.001952711600082653, (75.896, 9.846, 18.04))]
data['cbeta'] = []
data['probe'] = [(' H  96  THR HG22', ' H 100  GLY  H  ', -0.977, (67.116, -23.655, 21.981)), (' H   2  VAL  O  ', ' H  25  SER  HB3', -0.903, (60.17, -18.65, 38.101)), (' H  96  THR HG23', ' H  98  MET  H  ', -0.883, (69.402, -24.596, 23.013)), (' H  11  VAL HG11', ' H 116  THR HG21', -0.872, (35.655, -9.841, 27.655)), (' S 329  PHE  HB2', ' S1330  NAG  H82', -0.798, (87.203, -23.569, 6.725)), (' S 406  ALA  O  ', ' S 411  LYS  HE3', -0.773, (73.891, -3.661, 2.117)), (' S 469  PRO  HA ', ' S 471  ALA  N  ', -0.75, (78.439, 16.018, 21.751)), (' H  75  THR  O  ', ' H  75  THR HG22', -0.734, (65.014, -8.039, 32.853)), (' H  71  THR  CG2', ' H  75  THR  HA ', -0.718, (63.047, -5.314, 31.318)), (' S 431  THR HG22', ' S 434  GLY  H  ', -0.713, (80.506, -12.481, 28.457)), (' H  96  THR HG22', ' H 100  GLY  N  ', -0.711, (66.242, -23.864, 21.772)), (' S 352  TYR  CD2', ' S 374  LEU  HB3', -0.704, (82.792, -26.3, -5.817)), (' H  96  THR HG23', ' H  98  MET  N  ', -0.701, (69.296, -24.583, 22.78)), (' L 131  ALA  HB3', ' L 182  LEU HD12', -0.692, (14.113, -25.793, 35.612)), (' H  36  TRP  CE2', ' H  80  MET  HB2', -0.68, (54.334, -11.493, 24.826)), (' S 469  PRO  HA ', ' S 471  ALA  H  ', -0.677, (78.691, 16.089, 21.754)), (' S 342  ARG  HD3', ' S 383  TYR  HD2', -0.674, (88.196, -10.287, -3.183)), (' H  40  ALA  HB3', ' H  43  GLN  HG3', -0.67, (44.182, -21.78, 16.063)), (' S 378  CYS  HB3', ' S 508  ALA  CB ', -0.652, (89.116, -22.256, -14.694)), (' S 426  ARG  O  ', ' S 430  ALA  HB3', -0.652, (79.201, -17.777, 23.062)), (' L  10  SER  O  ', ' L  11  VAL HG23', -0.646, (51.757, -41.314, 14.214)), (' H   5  GLN  NE2', ' H  25  SER  HA ', -0.644, (58.169, -15.674, 39.467)), (' L 121  PRO  HG3', ' L 133  LEU HD12', -0.642, (16.463, -28.738, 37.216)), (' S 390  LYS  HB2', ' S 481  TYR  CE1', -0.631, (74.195, -9.102, 15.348)), (' S 356  TYR  HA ', ' S 364  PHE  HE2', -0.618, (79.506, -27.084, 1.599)), (' S 439  LYS  HG2', ' S 480  ASP  OD1', -0.613, (80.694, -1.903, 19.104)), (' S 356  TYR  HD1', ' S 357  ASN HD22', -0.607, (81.097, -32.877, 0.889)), (' H 169  VAL  HA ', ' H 563  HOH  O  ', -0.606, (29.964, -27.387, 26.223)), (' H 123  PRO  HD3', ' H 209  LYS  HE2', -0.601, (24.582, -20.531, 45.626)), (' H  11  VAL HG21', ' H 116  THR HG22', -0.594, (34.169, -10.478, 26.359)), (' L 151  ALA  C  ', ' L 153  GLY  H  ', -0.592, (9.243, -38.595, 32.054)), (' H  85  GLU  CD ', ' H  85  GLU  H  ', -0.589, (40.556, -13.963, 12.786)), (' S 355  LEU HD12', ' S 356  TYR  N  ', -0.585, (81.454, -27.538, 1.127)), (' H 178  LEU  C  ', ' H 178  LEU HD12', -0.584, (31.23, -25.062, 36.096)), (' H  71  THR HG21', ' H  75  THR  HA ', -0.581, (63.113, -6.006, 31.495)), (' S 351  ASP  OD2', ' S 354  VAL HG23', -0.579, (87.955, -31.46, -0.16)), (' S 352  TYR  HD2', ' S 374  LEU  HB3', -0.576, (83.276, -26.585, -5.314)), (' S 356  TYR  HE2', ' S 372  THR HG22', -0.576, (76.329, -31.757, -3.074)), (' H  96  THR HG21', ' L  34  HIS  NE2', -0.574, (66.731, -25.685, 22.435)), (' H 100  GLY  HA3', ' L  34  HIS  CD2', -0.57, (64.821, -26.383, 21.679)), (' H  71  THR HG22', ' H  75  THR  HA ', -0.566, (62.687, -4.945, 31.541)), (' S 367  TYR  O  ', ' S 369  VAL HG23', -0.561, (75.799, -19.061, -7.841)), (' S 356  TYR  HA ', ' S 364  PHE  CE2', -0.557, (78.983, -27.16, 1.341)), (' H  58  ASN  HB3', ' L 284  HOH  O  ', -0.551, (63.248, -11.787, 15.384)), (' H 162  GLY  O  ', ' H 182  VAL  HA ', -0.55, (35.047, -33.575, 44.787)), (' S 329  PHE  HB2', ' S1330  NAG  C8 ', -0.547, (87.783, -23.824, 6.493)), (' S 323  CYS  SG ', ' S 345  ILE HG23', -0.546, (92.144, -20.517, -4.267)), (' H 186  SER  O  ', ' H 189  LEU  HB2', -0.544, (28.336, -34.939, 55.99)), (' H  63  PHE  HB3', ' H  67  VAL HG23', -0.544, (52.479, -9.832, 15.884)), (' L 209  ALA  O  ', ' L 212  GLU  HB3', -0.543, (12.825, -34.64, 44.113)), (' L 131  ALA  HB3', ' L 182  LEU  CD1', -0.54, (13.848, -26.136, 35.974)), (' L  55  PRO  HG2', ' L  58  ILE HG12', -0.539, (62.39, -33.835, 30.68)), (' H  35  SER  HB2', ' H  95  ASP  OD1', -0.539, (61.622, -18.167, 23.501)), (' H 127  SER  HB2', ' H 129  LYS  HG3', -0.538, (20.368, -37.035, 48.411)), (' L 159  GLY  O  ', ' L 180  LEU HD12', -0.528, (17.597, -28.964, 28.572)), (' H 199  ASN  ND2', ' H 527  HOH  O  ', -0.525, (38.555, -13.408, 38.223)), (' H  47  TRP  CZ2', ' H  49  GLY  HA2', -0.525, (59.662, -14.23, 17.987)), (' S 337  VAL HG22', ' S 388  VAL  O  ', -0.521, (79.052, -8.794, 11.813)), (' L 167  LYS  HG2', ' L 174  TYR  CZ ', -0.513, (40.156, -38.988, 26.575)), (' S 353  SER  O  ', ' S 357  ASN  ND2', -0.513, (82.45, -32.701, 1.716)), (' L 151  ALA  O  ', ' L 153  GLY  N  ', -0.511, (8.497, -38.837, 31.779)), (' H  27  GLY  O  ', ' H  76  SER  HB2', -0.507, (61.879, -8.945, 37.625)), (' S 342  ARG  HD3', ' S 383  TYR  CD2', -0.505, (88.117, -10.074, -3.301)), (' L  17  LYS  O  ', ' L  78  VAL HG23', -0.493, (55.602, -47.977, 23.753)), (' H  75  THR  CG2', ' H  75  THR  O  ', -0.493, (64.731, -7.291, 32.695)), (' S 332  THR HG22', ' S 333  LYS  HG3', -0.492, (91.936, -15.301, 16.582)), (' S 378  CYS  HB3', ' S 508  ALA  HB2', -0.488, (88.855, -21.95, -14.447)), (' L 170  ASN  O  ', ' L 172  ASN  HB2', -0.485, (43.587, -42.846, 33.077)), (' S 475  TYR  CD1', ' S 475  TYR  N  ', -0.484, (74.751, 11.016, 17.023)), (' L  39  LYS  HE3', ' L  81  GLY  O  ', -0.483, (50.298, -38.571, 29.294)), (' H  47  TRP  CH2', ' H  49  GLY  HA2', -0.481, (60.031, -14.066, 17.184)), (' S 326  GLY  HA2', ' S1330  NAG  C8 ', -0.48, (89.364, -24.837, 6.298)), (' L  18  THR HG22', ' L 287  HOH  O  ', -0.478, (58.914, -50.559, 24.072)), (' S 448  LEU  HA ', ' S 452  GLU  OE1', -0.478, (78.088, 1.803, -0.148)), (' L 121  PRO  HG3', ' L 133  LEU  CD1', -0.477, (16.275, -28.939, 37.335)), (' S 353  SER  HA ', ' S 356  TYR  HB3', -0.476, (81.556, -30.238, -0.604)), (' H   5  GLN HE21', ' H  25  SER  HA ', -0.473, (57.603, -16.004, 39.415)), (' L 168  GLN  OE1', ' L 175  ALA  HB2', -0.473, (36.173, -37.472, 34.321)), (' H  71  THR HG22', ' H  72  ASP  N  ', -0.47, (61.249, -4.67, 31.092)), (' H   3  GLN  HA ', ' H 621  HOH  O  ', -0.469, (57.848, -21.51, 35.3)), (' L 133  LEU  N  ', ' L 133  LEU HD12', -0.468, (17.55, -29.051, 36.247)), (' L 125  GLU  HG2', ' L 130  LYS  O  ', -0.468, (16.521, -21.369, 37.952)), (' H  52  THR HG22', ' H  53  ILE HG22', -0.463, (69.885, -9.789, 27.117)), (' S 354  VAL  O  ', ' S 354  VAL HG12', -0.463, (86.155, -29.007, 4.284)), (' S 463  ASP  O  ', ' S 465  LYS  HG2', -0.461, (74.572, 19.148, 9.117)), (' L  32  SER  OG ', ' L  50  ASP  HA ', -0.461, (69.471, -29.613, 19.524)), (' L  55  PRO  HG2', ' L  58  ILE  CG1', -0.459, (62.465, -33.357, 30.386)), (' S 397  ILE  O  ', ' S 397  ILE HG22', -0.458, (74.961, -13.52, 2.911)), (' L   2  SER  HA ', ' L 218  HOH  O  ', -0.458, (59.827, -19.085, 6.417)), (' S 381  ASN  HB2', ' S 502  GLU  OE1', -0.457, (89.083, -13.195, -9.318)), (' L 212  GLU  O  ', ' L 213  CYS  HB3', -0.457, (13.799, -33.994, 49.46)), (' S 418  GLY  HA2', ' S 501  PHE  CD2', -0.454, (79.965, -18.414, -5.542)), (' H 127  SER  C  ', ' H 129  LYS  H  ', -0.452, (20.96, -36.894, 50.568)), (' L  83  GLU  O  ', ' L  84  ALA  HB2', -0.452, (49.347, -37.033, 26.331)), (' S 469  PRO  CA ', ' S 471  ALA  H  ', -0.452, (79.303, 15.536, 22.012)), (' S 337  VAL HG13', ' S 387  PHE  CD1', -0.45, (79.532, -9.831, 8.82)), (' H 150  VAL HG22', ' H 178  LEU HD21', -0.448, (34.887, -22.547, 34.906)), (' H 144  ASP  HB3', ' H 175  LEU HD13', -0.448, (24.568, -16.816, 30.103)), (' L 151  ALA  C  ', ' L 153  GLY  N  ', -0.447, (8.866, -38.683, 32.546)), (' S 431  THR HG22', ' S 434  GLY  N  ', -0.441, (80.081, -12.05, 29.16)), (' H  63  PHE  HB3', ' H  67  VAL  CG2', -0.441, (52.929, -9.947, 16.05)), (' S 348  CYS  O  ', ' S 510  VAL  HA ', -0.439, (92.829, -23.556, -8.187)), (' S 326  GLY  O  ', ' S 330  ASN  HB2', -0.438, (91.076, -22.891, 9.124)), (' S 441  ARG  HD2', ' S 444  ARG  HD2', -0.438, (77.88, 3.117, 7.172)), (' H  11  VAL HG11', ' H 116  THR  CG2', -0.437, (34.835, -10.106, 28.076)), (' H  52A PRO  HB3', ' H  75  THR HG23', -0.436, (65.166, -7.329, 30.962)), (' L 167  LYS  HG2', ' L 174  TYR  CE2', -0.435, (39.875, -38.628, 26.824)), (' L 145  VAL HG23', ' L 198  THR  O  ', -0.434, (27.019, -43.482, 27.024)), (' L  64  GLY  HA2', ' L  72  THR  O  ', -0.434, (64.141, -39.373, 18.67)), (' H  18  VAL  O  ', ' H  81  GLU  HA ', -0.431, (49.711, -6.556, 23.392)), (' H  85  GLU  CD ', ' H  85  GLU  N  ', -0.428, (40.679, -14.464, 13.324)), (' S 436  TYR  HA ', ' S 481  TYR  O  ', -0.428, (79.112, -6.928, 22.314)), (' L  15  PRO  HD3', ' L 107  LEU  O  ', -0.427, (46.824, -50.177, 24.633)), (' L  37  GLN  HB2', ' L  47  VAL HG11', -0.426, (56.51, -34.921, 25.908)), (' S 404  VAL HG23', ' S 405  ILE  N  ', -0.425, (71.919, -4.288, 9.855)), (' H  56  ILE HG12', ' S 491  TYR  HE2', -0.424, (67.237, -8.81, 20.674)), (' S 418  GLY  HA2', ' S 501  PHE  HD2', -0.423, (80.224, -18.376, -6.043)), (' H  41  PRO  O  ', ' H  43  GLN  HG2', -0.423, (42.872, -24.322, 16.799)), (' H  11  VAL  CG1', ' H 116  THR HG21', -0.423, (35.77, -9.338, 27.677)), (' S 489  ILE  HA ', ' S 492  GLN  NE2', -0.42, (71.838, -19.13, 20.842)), (' S 363  THR  HB ', ' S 422  ALA  HB3', -0.418, (75.073, -19.779, 7.674)), (' S 270  HOH  O  ', ' S 375  ASN  HB2', -0.418, (84.622, -31.096, -5.037)), (' H  74  SER  O  ', ' H  75  THR  HB ', -0.418, (65.504, -5.125, 34.592)), (' L  12  SER  HB3', ' L 107  LEU HD11', -0.416, (46.969, -47.901, 17.718)), (' S 390  LYS  HG2', ' S 490  GLY  O  ', -0.415, (70.93, -12.844, 16.872)), (' S 383  TYR  HE1', ' S 502  GLU  OE1', -0.413, (88.435, -12.432, -8.185)), (' H 150  VAL  CG2', ' H 178  LEU HD21', -0.412, (34.636, -22.518, 35.162)), (' L 182  LEU HD11', ' L 187  TRP  HB2', -0.412, (13.075, -27.408, 36.429)), (' H 150  VAL HG12', ' H 200  HIS  CD2', -0.411, (34.789, -17.138, 33.598)), (' S 456  SER  O  ', ' S 457  ASN  HB3', -0.41, (86.144, 5.931, 11.87)), (' L 182  LEU  CD1', ' L 187  TRP  HB2', -0.409, (12.62, -27.534, 36.556)), (' L 258  HOH  O  ', ' S 365  LYS  HE3', -0.409, (69.978, -20.884, 5.49)), (' L 159  GLY  O  ', ' L 180  LEU  HA ', -0.407, (18.746, -29.126, 29.56)), (' L 152  ASP  OD1', ' L 191  ARG  N  ', -0.407, (6.923, -35.841, 37.261)), (' H  56  ILE HD11', ' S 390  LYS  NZ ', -0.406, (68.779, -8.358, 17.716)), (' S 242  HOH  O  ', ' S 459  PRO  HG2', -0.405, (81.9, 13.921, 13.574)), (' L  28  ILE HG23', ' L  66  ASN  OD1', -0.402, (67.297, -34.382, 11.748)), (' L 212  GLU  HG2', ' L 212  GLU  O  ', -0.402, (14.508, -35.715, 47.504)), (' H  35  SER  CB ', ' H 100A MET  HE2', -0.401, (60.232, -18.588, 22.458))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
