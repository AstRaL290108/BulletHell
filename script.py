import sys

def StartLvL(m):
	m[0].lost = 0
	m[0].now_scen = f"Level{m[1]}"

def GameClose(n):
	sys.exit()

def ReStartLvL(scen):
	scen.lost = 0
	scen.now_scen = scen.memorize[0]

def ToMenu(scen):
	scen.lost = 0
	scen.now_scen = "main-menu"

def AllLvL(scen):
	scen.lost = 0
	scen.now_scen = "AllLevel"