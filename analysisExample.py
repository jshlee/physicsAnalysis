# import ROOT in batch mode
import sys,ROOT,numpy
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
ROOT.gROOT.SetBatch(True)
sys.argv = oldargv

# making new ttree
tfile = ROOT.TFile( 'test.root', 'recreate' )
ttree = ROOT.TTree( 't1', 'tree' )

from array import array
# adding variables to ttree
maxMuons = 15
nmuons = array("i", [0])
ttree.Branch("nmuons", nmuons,"nmuons/I")
mu_isTightMuon = array("i", maxMuons*[0])
ttree.Branch("mu_isTightMuon", mu_isTightMuon,"mu_isTightMuon[nmuons]/I")
mu_pt = array("d", maxMuons*[0.0])
ttree.Branch("mu_pt", mu_pt,"mu_pt[nmuons]/D")

# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events

#https://github.com/vallot/CATTools/tree/cat80x/DataFormats/interface
muons, muonLabel = Handle("std::vector<cat::Muon>"), "catMuons"
elecs, elecLabel = Handle("std::vector<cat::Electron>"), "catElectrons"
jets, jetLabel = Handle("std::vector<cat::Jet>"), "catJets"

# open file
events = Events("/home/CAT/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/v8-0-3_RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext1-v1/161219_090504/0000/catTuple_1.root")

for iev,event in enumerate(events):
    print "\nEvent %d: run %6d, lumi %4d, event %12d" % (iev,event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())
    #https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/DataFormats/PatCandidates/interface/Jet.h
    event.getByLabel(jetLabel, jets)
    for i,jet in enumerate(jets.product()):
        print "jet %3d: pt %5.1f, eta %+4.2f, mass %5.1f, partonFlavour %3d" % (
            i, jet.pt(), jet.eta(), jet.mass(), jet.partonFlavour())

    event.getByLabel(muonLabel, muons)
    nmu =0
    for j,muon in enumerate(muons.product()):
        if not muon.isTightMuon():
            continue
        print "muon %3d: pt %5.1f, eta %+4.2f, phi %+4.2f, mass %5.1f, isTightMuon %5.1f" % (
            j, muon.pt(), muon.eta(), muon.phi(), muon.mass(), muon.isTightMuon())
        mutlv=ROOT.TLorentzVector()
        mutlv.SetPtEtaPhiM(muon.pt(), muon.eta(), muon.phi(), muon.mass())

        mu_pt[nmu] = mutlv.Pt()
        mu_isTightMuon[nmu] = muon.isTightMuon()
        nmu = nmu+1
    nmuons[0] = nmu

    event.getByLabel(elecLabel, elecs)
    for k,elec in enumerate(elecs.product()):
        print "elec %3d: pt %5.1f, eta %+4.2f, phi %+4.2f, mass %5.1f, electronID %5.1f" % (
            k, elec.pt(), elec.eta(), elec.phi(), elec.mass(), elec.electronID('cutBasedElectronID-Summer16-80X-V1-medium'))



    ttree.Fill()

tfile.Write()
tfile.Close()
    
