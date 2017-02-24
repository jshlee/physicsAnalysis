import ROOT

#open your root file
rtfile = ROOT.TFile("test.root")

#open ttree using exact tree name (you can ckeck using TBrowser or source code)
tree = rtfile.Get("t1")

#this will print particular value for each event, also you need exact value name
tree.Scan("nmuons")

#open new canvas
canv = ROOT.TCanvas()
#draw distribution of particlar value on the canvas
tree.Draw("nmuons")
#save the canvas as image file
canv.Print("test.png") #this will make image file, you can open it with image file opener such as 'display', 'eog', etc.

canv2 = ROOT.TCanvas()
tree.Draw("nmuons", "mu_pt>5") #you can set cut for plot
canv2.Print("test2.png")
