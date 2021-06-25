#include "../include/processDeltaRHistograms.h"

double get_resolution_in_dR(const double & transverse_size, const double & longitudinal_distance) {
  return (transverse_size/longitudinal_distance);
}

void draw_vertical_line(double xAxis_position, EColor color, std::string text) {
  TLine lineObj = TLine();
  lineObj.SetLineColor(color);
  lineObj.DrawLine(xAxis_position, gPad->GetUymin(), xAxis_position, gPad->GetUymax());
  TText textObj = TText();
  textObj.SetTextAlign(23);
  textObj.SetTextSize(0.02);
  textObj.SetTextColor(color);
  textObj.SetTextAngle(90);
  textObj.DrawText(xAxis_position, 0.5*(gPad->GetUymin() + gPad->GetUymax()), text.c_str());
}

int main(int argc, char* argv[]) {
  gROOT->SetBatch();
  TH1::AddDirectory(kFALSE);

  tmArgumentParser argumentParser = tmArgumentParser("Process deltaR histograms.");
  argumentParser.addArgument("inputFilePath", "", true, "Path to file with deltaR histograms.");
  argumentParser.addArgument("outputFolder", "plots", false, "Output folder.");
  argumentParser.addArgument("outputFileName", "", true, "Name of output file.");
  argumentParser.setPassedStringValues(argc, argv);
  optionsStruct options = getOptionsFromParser(argumentParser);
  std::cout << "Options passed:" << std::endl << options << std::endl;

  int mkdir_return_status = system(("set -x && mkdir -p " + options.outputFolder + " && set +x").c_str());
  if (mkdir_return_status != 0) {
    std::cout << "ERROR in creating output folder with path: " << options.outputFolder << std::endl;
    std::exit(EXIT_FAILURE);
  }

  double resolution_EE = get_resolution_in_dR(29., 3170.);
  double resolution_ES = get_resolution_in_dR(2., 3045.);

  TFile *inputFileHandle = TFile::Open(options.inputFilePath.c_str(), "READ");
  if ((inputFileHandle->IsZombie()) || (!(inputFileHandle->IsOpen()))) {
    std::cout << "ERROR: Unable to open file: " << options.inputFilePath << std::endl;
    std::exit(EXIT_FAILURE);
  }

  TH1D *inputHistogram;
  inputFileHandle->GetObject("genLevelMinimalAnalyzer/deltaR", inputHistogram);
  assert (inputHistogram != nullptr);
  TCanvas outputCanvas("deltaR", "deltaR", 1600, 900);
  gStyle->SetOptStat(110010);
  inputHistogram->Draw();
  outputCanvas.Update();
  draw_vertical_line(resolution_ES, static_cast<EColor>(kRed+2), "ES granularity");
  draw_vertical_line(resolution_EE, static_cast<EColor>(kGreen+3), "EE granularity");
  outputCanvas.Update();
  outputCanvas.SaveAs((options.outputFolder + "/" + options.outputFileName).c_str());
  inputFileHandle->Close();

  std::cout << "All done!" << std::endl;
  return EXIT_SUCCESS;
}
