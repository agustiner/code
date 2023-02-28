import ROOT
    
def get_n_keys():
    return ['nMeasurements_vs_eta', 'nMeasurements_vs_pT']

# Get plot of total number of events as function of eta, phi, pt
def get_n_png(root_path):
    tfile = ROOT.TFile.Open(str(root_path))

    for key in get_n_keys():
        tprofile = tfile.Get(key)
        tcanvas = ROOT.TCanvas()
        tprofile.Draw()
        tcanvas.Print(str(root_path.parent / (key + '.png')))
