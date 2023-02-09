import ROOT
import pathlib

def get_efficiency_png(tefficiency, name):
    tcanvas = ROOT.TCanvas()
    tefficiency.Draw()
    tcanvas.Print(name + '.png')

def get_efficiency_pngs_separate(root_filename):
    tfile = ROOT.TFile.Open(root_filename)

    efficiency_keys = ["trackeff_vs_pT", "trackeff_vs_phi", "trackeff_vs_eta", "fakerate_vs_pT", "fakerate_vs_eta", "fakerate_vs_phi", "duplicationRate_vs_pT", "duplicationRate_vs_eta", "duplicationRate_vs_phi"]
    
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

def get_efficiency_keys():
    return ["trackeff_vs_pT", "trackeff_vs_phi", "trackeff_vs_eta", "fakerate_vs_pT", "fakerate_vs_eta", "fakerate_vs_phi", "duplicationRate_vs_pT", "duplicationRate_vs_eta", "duplicationRate_vs_phi"]

# Get the legend for these histograms with these labels. For some
# reason, the legend has to be drawn in the same code scope as the
# tcanvas. So return the tlegend and then have the caller draw it. Do
# not mess with the color of the tefficiency, assume it is already
# set.
def get_legend(labels, thisograms):
    x1 = 0.8;
    y1 = 0.8;
    width = 0.15;
    height = 0.15;
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

# Given the list of paths, get the efficiency histograms and overlay
# them.  Also, plot the filenames
def get_total_pngs_multiple(paths, labels):
    efficiency_keys = get_efficiency_keys()
    tfiles = []
    for p in paths:
        tfiles.append(ROOT.TFile.Open(p))

    for key in efficiency_keys:
        tcanvas = ROOT.TCanvas()
        totalhistograms = []
        
        for i, t in enumerate(tfiles):
            tefficiency = t.Get(key)
            totalhistogram = tefficiency.GetTotalHistogram()
            # Set the title, because its more descriptive.
            totalhistogram.SetTitle('Distribution')
            # Set to false, because it doesnt stack.
            totalhistogram.SetStats(False)
            totalhistogram.SetLineColor(i + 1)
            totalhistograms.append(totalhistogram)
            
            if i == 0:
                totalhistogram.Draw()
            else:
                totalhistogram.Draw('same')
                
        legend = get_legend(labels, totalhistograms)
        legend.Draw()
        tcanvas.Print(key + '.png')

# not used
def get_total_pngs_single(path):
    # Given the one .root file, get the efficiency histograms and overlay them.
    tfile = ROOT.TFile.Open(path)

    efficiency_keys = ["trackeff_vs_pT", "trackeff_vs_phi", "trackeff_vs_eta", "fakerate_vs_pT", "fakerate_vs_eta", "fakerate_vs_phi", "duplicationRate_vs_pT", "duplicationRate_vs_eta", "duplicationRate_vs_phi"]

    for key in efficiency_keys:
        tefficiency = tfile.Get(key)
        totalhistogram = tefficiency.GetTotalHistogram()
        tcanvas = ROOT.TCanvas()
        tcanvas.SetCanvasSize(2000, 500)
        ttext = ROOT.TText()
        totalhistogram.Draw()
        ttext.DrawTextNDC(0.05, 0, path)
        tcanvas.Print(key + '.png')
