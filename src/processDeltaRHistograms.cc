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
  argumentParser.addArgument("inputFilePaths", "", true, "Path to file with deltaR histograms.");
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

  std::cout << "Adding histogram from file: " << (options.inputFilePaths).at(0) << std::endl;
  TFile *inputFileHandle_first_file = TFile::Open(((options.inputFilePaths).at(0)).c_str(), "READ");
  assert((!(inputFileHandle_first_file->IsZombie())) && (inputFileHandle_first_file->IsOpen()));
  TH1D *deltaRHistogram_first_file;
  inputFileHandle_first_file->GetObject("genLevelMinimalAnalyzer/deltaR", deltaRHistogram_first_file);
  assert (deltaRHistogram_first_file != nullptr);
  TH1D *deltaRHistogram = (TH1D*)(deltaRHistogram_first_file->Clone());
  inputFileHandle_first_file->Close();
  for (unsigned int inputFilePathsCounter = 1; inputFilePathsCounter < (options.inputFilePaths).size(); ++inputFilePathsCounter) {
    std::cout << "Adding histogram from file: " << (options.inputFilePaths).at(inputFilePathsCounter) << std::endl;
    TFile *inputFileHandle_new = TFile::Open(((options.inputFilePaths).at(inputFilePathsCounter)).c_str(), "READ");
    assert((!(inputFileHandle_new->IsZombie())) && (inputFileHandle_new->IsOpen()));
    TH1D *deltaRHistogram_new;
    inputFileHandle_new->GetObject("genLevelMinimalAnalyzer/deltaR", deltaRHistogram_new);
    assert (deltaRHistogram_new != nullptr);
    deltaRHistogram->Add(deltaRHistogram_new);
    inputFileHandle_new->Close();
  }

  TCanvas outputCanvas("deltaR", "deltaR", 1600, 900);
  gStyle->SetOptStat(110010);
  deltaRHistogram->Draw();
  outputCanvas.Update();
  draw_vertical_line(resolution_ES, static_cast<EColor>(kRed+2), "ES granularity");
  draw_vertical_line(resolution_EE, static_cast<EColor>(kGreen+3), "EE granularity");
  outputCanvas.Update();
  outputCanvas.SaveAs((options.outputFolder + "/" + options.outputFileName).c_str());

  std::cout << "All done!" << std::endl;
  return EXIT_SUCCESS;
}
