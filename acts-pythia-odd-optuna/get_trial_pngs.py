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

def get_total_pngs_multiple(paths, labels):
    # Given the list of paths, get the efficiency histograms and overlay them.
    # Also, plot the filenames

    efficiency_keys = ["trackeff_vs_pT", "trackeff_vs_phi", "trackeff_vs_eta", "fakerate_vs_pT", "fakerate_vs_eta", "fakerate_vs_phi", "duplicationRate_vs_pT", "duplicationRate_vs_eta", "duplicationRate_vs_phi"]

    tfiles = []
    for p in paths:
        tfiles.append(ROOT.TFile.Open(p))

    color = 1
    offset = 0
    canvas_offset = 100
    canvas_offset_margin = 0.06
    text_offset = 0.04

    for key in efficiency_keys:
        tcanvas = ROOT.TCanvas()
        # tcanvas.SetCanvasSize(1000, 500 + canvas_offset * len(paths))
        x1 = 0.85;
        y1 = 0.6;
        width = 0.1;
        height = 0.3;
        x2 = x1 + width;
        y2 = y1 + width;        
        legend = ROOT.TLegend(x1, y1, x2, y2)
        
        for i, tfile in enumerate(tfiles):
            tefficiency = tfile.Get(key)
            totalhistogram = tefficiency.GetTotalHistogram()
            totalhistogram.SetLineColor(i + 1)
            totalhistogram.Draw('same')
            legend.AddEntry(totalhistogram, labels[i], 'f')

        ROOT.gPad.SetBottomMargin(canvas_offset_margin * len(paths))
        for i, tfile in enumerate(tfiles):
            ttext = ROOT.TText()
            ttext.SetTextSize(0.03)
            path = pathlib.Path(paths[i])
            important_parts_of_path = str('/'.join(path.parts[-3:]))
            ttext.DrawTextNDC(0, 0.01 + i * text_offset, labels[i] + ' ' + important_parts_of_path)
            ttext.Draw()
            
        legend.Draw()
        tcanvas.Print(key + '.png')
