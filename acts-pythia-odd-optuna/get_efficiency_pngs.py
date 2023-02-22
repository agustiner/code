import ROOT
import pathlib

def get_efficiency_keys():
    return ["trackeff_vs_pT", "trackeff_vs_phi", "trackeff_vs_eta", "fakerate_vs_pT", "fakerate_vs_eta", "fakerate_vs_phi", "duplicationRate_vs_pT", "duplicationRate_vs_eta", "duplicationRate_vs_phi"]

def get_efficiency_png(tefficiency, name):
    tcanvas = ROOT.TCanvas()
    tefficiency.Draw()
    tcanvas.Print(name + '.png')

def get_efficiency_pngs(root_filename):
    efficiency_keys = get_efficiency_keys()
    tfile = ROOT.TFile.Open(root_filename)
    
    for key in efficiency_keys:
        tefficiency = tfile.Get(key)
        get_efficiency_png(tefficiency, key)

# Given root_files, labels, and a current canvas, add text to the
# bottom stating the files and labels
def set_debug_text(root_files, labels, tcanvas):
    canvas_offset = 100
    canvas_offset_margin = 0.06
    text_offset = 0.04
    
    tcanvas.SetCanvasSize(2000, 500 + canvas_offset * len(root_files))
    ROOT.gPad.SetBottomMargin(canvas_offset_margin * len(root_files))
    for i, root_file in enumerate(root_files):
        ttext = ROOT.TText()
        ttext.SetTextSize(0.03)
        path = pathlib.Path(root_file)
        important_parts_of_path = str('/'.join(path.parts[-3:]))
        ttext.DrawTextNDC(0, 0.01 + i * text_offset, labels[i] + ' ' + important_parts_of_path)
        ttext.Draw()

# Get the legend for these histograms with these labels. For some
# reason, the legend has to be drawn in the same code scope as the
# tcanvas. So return the tlegend and then have the caller draw it. Do
# not mess with the color of the tefficiency, assume it is already
# set.
def get_legend(labels, thisograms):
    x1 = 0.85;
    y1 = 0.85;
    width = 0.1;
    height = 0.1;
    x2 = x1 + width;
    y2 = y1 + width;        
    legend = ROOT.TLegend(x1, y1, x2, y2)

    for i, thistogram in enumerate(thisograms):
        legend.AddEntry(thistogram, labels[i], 'f')

    return legend

    
# Make all efficiency plots from the root files, combining the ones of
# the same type.
def get_efficiency_pngs_combined(root_files, labels):
    tfiles = []
    for f in root_files:
        tfiles.append(ROOT.TFile.Open(f))

    efficiency_keys = get_efficiency_keys()

    for key in efficiency_keys:
        tcanvas = ROOT.TCanvas()
        
        tefficiencies = []
        for t in tfiles:
            tefficiencies.append(t.Get(key))

        for i, tefficiency in enumerate(tefficiencies):
            tefficiency.SetLineColor(i + 1)
            if (i == 0):
                tefficiency.Draw()
            else:
                tefficiency.Draw('same')
                
        legend = get_legend(labels, tefficiencies)
        legend.Draw()
        tcanvas.Print(key + '.png')
        tefficiencies = []

