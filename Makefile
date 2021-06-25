# Remember: order of arguments to g++ is important, the `root-config` must follow the rest of the arguments

vpath %.a lib
vpath %.so lib
vpath %.o obj
vpath %.cc src
vpath %.h include
vpath % bin

.PHONY: all
all: processDeltaRHistograms

processDeltaRHistograms: processDeltaRHistograms.o
	g++ -o bin/processDeltaRHistograms obj/processDeltaRHistograms.o -L$(TMCPPUTILS)/generalUtils/lib -ltmGeneralUtils -L$(TMCPPUTILS)/ROOTUtils/lib -ltmROOTUtils `root-config --ldflags --glibs` -lTreePlayer -lRooFit -lRooFitCore -lMinuit -lMathCore -lMathMore

processDeltaRHistograms.o: processDeltaRHistograms.cc processDeltaRHistograms.h
	g++ -g -c -std=c++11 -Wall -Wextra -Werror -pedantic-errors -fPIC -O3 -o obj/processDeltaRHistograms.o src/processDeltaRHistograms.cc -I$(TMCPPUTILS)/generalUtils/include -I$(TMCPPUTILS)/ROOTUtils/include `root-config --cflags`

clean:
	rm -rf bin/*
	rm -rf obj/*

.DEFAULT_GOAL := all
