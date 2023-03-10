import ROOT
import pathlib

def get_efficiency_keys():
    return ["trackeff_vs_pT", "trackeff_vs_phi", "trackeff_vs_eta", "fakerate_vs_pT", "fakerate_vs_eta", "fakerate_vs_phi", "duplicationRate_vs_pT", "duplicationRate_vs_eta", "duplicationRate_vs_phi"]

def get_efficiency_titles():
    return ['Track Efficiency', 'Track Efficiency', 'Track Efficiency', 'Track Fake Rate', 'Track Fake Rate', 'Track Fake Rate', 'Track Duplicate Rate', 'Track Duplicate Rate', 'Track Duplicate Rate']

def get_efficiency_png(tefficiency, title, filename, dirpath):
    tcanvas = ROOT.TCanvas()
    tefficiency.Draw()
    tefficiency.SetTitle(title)
    tcanvas.Print(str(dirpath / (filename + '.png')))

def get_efficiency_pngs(root_path):
    efficiency_keys = get_efficiency_keys()
    efficiency_titles = get_efficiency_titles()
    tfile = ROOT.TFile.Open(str(root_path))
    
    for i, key in enumerate(efficiency_keys):
        tefficiency = tfile.Get(key)
        title = efficiency_titles[i]
        get_efficiency_png(tefficiency, title, key, root_path.parent)

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
def get_efficiency_pngs_combined(dirpaths, labels):
    rootpaths = [d / 'performance_ckf.root' for d in dirpaths]
    tfiles = [ROOT.TFile.Open(str(r)) for r in rootpaths]
    efficiency_keys = get_efficiency_keys()
    efficiency_titles = get_efficiency_titles()
    for i, key in enumerate(efficiency_keys):
        tcanvas = ROOT.TCanvas()
        tefficiencies = []
        for t in tfiles:
            tefficiencies.append(t.Get(key))

        for j, tefficiency in enumerate(tefficiencies):
            tefficiency.SetLineColor(j + 1)
            if (j == 0):
                tefficiency.Draw()
            else:
                tefficiency.Draw('same')

            tefficiency.SetTitle(efficiency_titles[i])
            ROOT.gPad.Update()
            graph = tefficiency.GetPaintedGraph()
            graph.SetMinimum(0)
            graph.SetMaximum(1)

        legend = get_legend(labels, tefficiencies)
        legend.Draw()
        tcanvas.Print(key + '.png')

