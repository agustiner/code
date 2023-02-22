import ROOT

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

# Given the list of paths, get the efficiency histograms and overlay
# them.  Also, plot the filenames
def get_numerator_pngs_multiple(paths, labels):
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

def get_numerator_pngs_single(path):
    tfile = ROOT.TFile.Open(path)
    efficiency_keys = get_efficiency_keys()

    for key in efficiency_keys:
        tefficiency = tfile.Get(key)
        totalhistogram = tefficiency.GetTotalHistogram()
        tcanvas = ROOT.TCanvas()
        tcanvas.SetCanvasSize(2000, 500)
        ttext = ROOT.TText()
        totalhistogram.Draw()
        ttext.DrawTextNDC(0.05, 0, path)
        tcanvas.Print(key + '.png')
