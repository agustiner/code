void plotefficiency(TEfficiency* teff, TString name) {
  TCanvas *c1 = new TCanvas();
  teff->Draw();
  TString filename = name + ".png";
  c1->Print(filename);
}

void root_ls(TString root_filename) {
  std::unique_ptr<TFile> myFile(TFile::Open(root_filename));
  myFile->ls();
}

void get_performance_plots(TString root_filename) {
  std::unique_ptr<TFile> myFile(TFile::Open(root_filename));
  TEfficiency* teffeta = (TEfficiency*)myFile->Get("trackeff_vs_eta");
  plotefficiency(teffeta, "trackeff_vs_eta");

  std::vector<TString> names = {"trackeff_vs_pT", "trackeff_vs_phi", "trackeff_vs_eta", "fakerate_vs_pT", "fakerate_vs_eta", "fakerate_vs_phi", "duplicationRate_vs_pT", "duplicationRate_vs_eta", "duplicationRate_vs_phi"};

  for (auto it = begin (names); it != end (names); ++it) {
    TEfficiency* tefficiency = (TEfficiency*)myFile->Get(*it);
    plotefficiency(tefficiency, *it);
  }
}

int get_plots() {
  get_performance_plots("./2023-01-17-16-59-04/trial_0/performance_ckf.root");
  return 0;
}
