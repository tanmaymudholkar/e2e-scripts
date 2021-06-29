#include <cstdlib>
#include <cmath>
#include <iostream>
#include <vector>
#include <map>
#include <cassert>

#include "TROOT.h"
#include "Rtypes.h"
#include "TStyle.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TH1.h"
#include "TH1D.h"
#include "TLine.h"
#include "TText.h"

#include "tmArgumentParser.h"
#include "tmProgressBar.h"

struct optionsStruct {
  std::string outputFolder, outputFileName;
  std::vector<std::string> inputFilePaths;

  friend std::ostream& operator<< (std::ostream& out, const optionsStruct& options) {
    out << "inputFilePaths: {";
    for (const std::string & inputFilePath : (options.inputFilePaths)) {
      out << inputFilePath << "; ";
    }
    out << "}" << std::endl
        << "outputFolder: " << options.outputFolder << std::endl
        << "outputFileName: " << options.outputFileName << std::endl;
    return out;
  }
};

optionsStruct getOptionsFromParser(tmArgumentParser& argumentParser) {
  optionsStruct options = optionsStruct();
  std::string inputFilePathsRaw = argumentParser.getArgumentString("inputFilePaths");
  std::ifstream inputFilePathsRawHandle(inputFilePathsRaw.c_str());
  assert(inputFilePathsRawHandle.is_open());
  while (!inputFilePathsRawHandle.eof()) {
    std::string inputFilePath;
    inputFilePathsRawHandle >> inputFilePath;
    if (!(inputFilePath.empty())) (options.inputFilePaths).push_back(inputFilePath);
  }
  inputFilePathsRawHandle.close();
  assert((options.inputFilePaths).size() >= 1);
  options.outputFolder = argumentParser.getArgumentString("outputFolder");
  options.outputFileName = argumentParser.getArgumentString("outputFileName");
  return options;
}
