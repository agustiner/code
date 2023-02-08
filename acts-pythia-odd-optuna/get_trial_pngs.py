import ROOT

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

def get_efficiency_pngs_combined(root_filenames, labels):
    tfiles = []

    for f in root_filenames:
        tfiles.append(ROOT.TFile.Open(f))

    efficiency_keys = ["trackeff_vs_pT", "trackeff_vs_phi", "trackeff_vs_eta", "fakerate_vs_pT", "fakerate_vs_eta", "fakerate_vs_phi", "duplicationRate_vs_pT", "duplicationRate_vs_eta", "duplicationRate_vs_phi"]

    tefficiencies = []
    
    for key in efficiency_keys:
        tcanvas = ROOT.TCanvas()
        x1 = 0.8;
        y1 = 0.8;
        width = 0.1;
        height = 0.3;
        x2 = x1 + width;
        y2 = y1 + width;        
        legend = ROOT.TLegend(x1, y1, x2, y2)
        
        tefficiency = tfiles[0].Get(key)
        tefficiency.Draw()
        legend.AddEntry(tefficiency, labels[0], 'f')

        tefficiency = tfiles[1].Get(key)
        tefficiency.SetLineColor(2)
        tefficiency.Draw('same')
        legend.AddEntry(tefficiency, labels[1], 'f')

        tefficiency = tfiles[2].Get(key)
        tefficiency.SetLineColor(3)
        tefficiency.Draw('same')
        legend.AddEntry(tefficiency, labels[2], 'f')
        
        # The legend must be after histograms.
        legend.Draw()
        tcanvas.Print(key + '.png')
        tefficiencies = []

    
