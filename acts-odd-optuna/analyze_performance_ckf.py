import ROOT

def get_efficiency_png(tefficiency, name):
    tcanvas = ROOT.TCanvas()
    tefficiency.Draw()
    tcanvas.Print(name + '.png')

def get_plots(root_filename):
    tfile = ROOT.TFile.Open(root_filename)
    
    efficiency_keys = ["trackeff_vs_pT", "trackeff_vs_phi", "trackeff_vs_eta", "fakerate_vs_pT", "fakerate_vs_eta", "fakerate_vs_phi", "duplicationRate_vs_pT", "duplicationRate_vs_eta", "duplicationRate_vs_phi"]

    for key in efficiency_keys:
        tefficiency = tfile.Get(key)
        get_efficiency_png(tefficiency, key)


