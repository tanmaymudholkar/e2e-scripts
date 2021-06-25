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
  std::string inputFilePath, outputFolder, outputFileName;

  friend std::ostream& operator<< (std::ostream& out, const optionsStruct& options) {
    out << "inputFilePath: " << options.inputFilePath << std::endl
        << "outputFolder: " << options.outputFolder << std::endl
        << "outputFileName: " << options.outputFileName << std::endl;
    return out;
  }
};

optionsStruct getOptionsFromParser(tmArgumentParser& argumentParser) {
  optionsStruct options = optionsStruct();
  options.inputFilePath = argumentParser.getArgumentString("inputFilePath");
  options.outputFolder = argumentParser.getArgumentString("outputFolder");
  options.outputFileName = argumentParser.getArgumentString("outputFileName");
  return options;
}
