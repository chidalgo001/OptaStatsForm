import sys, os, clr, gc
clr.AddReference("IronPython.Wpf")
clr.AddReference("Xceed.Wpf.Toolkit")
clr.AddReference("System")
import System
import io

from System.IO import File, Directory, Path, StreamWriter

from System.Windows.Controls import *
from System.Collections.ObjectModel import ObservableCollection
import wpf

def Execute(): 
	Project.ScriptingObjects["GraphicsLocation"] = Project.ProjectSettings["GraphicsLocation"]
	Globals["PlayerSelectedStat"] = []
	Globals["TeamSelectedStat"] = []
	Globals["PressedButtons"] = []
	Project.EventsManager.SubscribeEvent("GameOpened", Script.Id, "OnGameOpened", True)
	Project.EventsManager.SubscribeEvent("Game.SelectedTeamChanged", Script.Id, "OnGame_SelectedTeamChanged", True)
	Project.EventsManager.SubscribeEvent("Game.SelectedPlayerChanged", Script.Id, "OnGame_SelectedPlayerChanged", True)
	Project.EventsManager.SubscribeEvent("Game.SelectedStatsChanged", Script.Id, "OnGame_SelectedStatsChanged", True)
	Project.EventsManager.SubscribeEvent("GameClosed", Script.Id, "OnGameClosed", True)
	Project.EventsManager.SubscribeEvent("GameOnline.UpdateTrigger", Script.Id, "OnGameOnline_UpdateTrigger", True)
	
def OnGameClosed(sender, args):
	Project.EventsManager.UnsubscribeEvent("GameOpened", Script.Id)
	Project.EventsManager.UnsubscribeEvent("GameClosed", Script.Id)
	
def OnGameOpened(sender, args):
	Globals["PlayerSelectedStat"] = []
	Globals["TeamSelectedStat"] = []
	Globals["RefereesSorted"] = sorted(Game.Referees, key=lambda x: x.Function, reverse=False)
	RefreshTeamStats()

def OnGame_SelectedTeamChanged(sender, args):
	RefreshTeamStats()

def OnGame_SelectedStatsChanged(sender, args):
	RefreshTeamStats()
	RefreshPlayerStats()

def OnGame_SelectedPlayerChanged(sender, args):
	Globals["RefereesSorted"] = sorted(Game.Referees, key=lambda x: x.Function, reverse=False)
	RefreshPlayerStats()
	RefreshTeamStats()
	temp = []
	for item in Globals["PlayerSelectedStat"]:

		stat = item["Stat"]
		
		value = Globals["OptaStatsForm"].GetPlayerStat([stat], Game.SelectedPlayer)	
	
		temp.append({"Stat":stat,"Value":value} )

	Globals["PlayerSelectedStat"] = temp

		

def btnReset(sender, args):
	Globals["PlayerSelectedStat"] = []
	Globals["TeamSelectedStat"] = []
	for btn in Globals["PressedButtons"]:
		btn.IsChecked = False
	

def btnPlayerStatChecked(sender, args):
	
	stat = sender.Name
	
	value = Globals["OptaStatsForm"].GetPlayerStat([stat], Game.SelectedPlayer)	

	found = False	
	
	if len(Globals["PlayerSelectedStat"]) == 0:
		Globals["PlayerSelectedStat"].append({"Stat":stat,"Value":value} )
		if not sender in Globals["PressedButtons"]:
			Globals["PressedButtons"].append(sender)		
	
	else:
		for entry in Globals["PlayerSelectedStat"]:
			if entry["Stat"] == stat:
				found = True
				break
	
		if found:
			Globals["PlayerSelectedStat"].remove(entry)
			if sender in Globals["PressedButtons"]:
				Globals["PressedButtons"].remove(sender)	
		else:
			Globals["PlayerSelectedStat"].append({"Stat":stat,"Value":value})
			if not sender in Globals["PressedButtons"]:
				Globals["PressedButtons"].append(sender)		

	
def btnTeamStatChecked(sender, args):
	team = Game.SelectedTeam
	stat = sender.Name[1:]
	hvalue = Globals["OptaStatsForm"].GetTeamStat([stat], Game.HomeTeam)	
	avalue = Globals["OptaStatsForm"].GetTeamStat([stat], Game.AwayTeam)
	found = False	
	
	if len(Globals["TeamSelectedStat"]) == 0:
		Globals["TeamSelectedStat"].append({"Stat":stat,"HomeValue":hvalue , "AwayValue":avalue} )
		if not sender in Globals["PressedButtons"]:
			Globals["PressedButtons"].append(sender)
	else:
		
		for entry in Globals["TeamSelectedStat"]:
			if entry["Stat"] == stat:
				found = True
				break;
				
		if found:
			Globals["TeamSelectedStat"].remove(entry)
			if sender in Globals["PressedButtons"]:
				Globals["PressedButtons"].remove(sender)	
		else:
			Globals["TeamSelectedStat"].append({"Stat":stat,"HomeValue":hvalue , "AwayValue":avalue} )
			if not sender in Globals["PressedButtons"]:
				Globals["PressedButtons"].append(sender)			
				

def btnRefreshStats(sender , args):
	RefreshPlayerStats()
	RefreshTeamStats()
	print "Refreshed"
	

def RefreshPlayerStats():
	
	player = Game.SelectedPlayer
	
	value = ""
	
	try:
		Globals["OptaStatsForm"].Goals = player.Stats.GetValue("Goals")
	except:
		pass
	
		

	try:
		value = player.Stats.ExtraStats.saves
	except:
		value = "0"
	Globals["OptaStatsForm"].Saves = value	
	
	try:
		value= player.Stats.ExtraStats.goalsconceded
	except:	
		value = "0"
	Globals["OptaStatsForm"].GoalsConceded = value	
	
	try:
		value = player.Stats.ExtraStats.punches
	except:	
		value = "0"
	Globals["OptaStatsForm"].Punches = value
	
	try:
		value = player.Stats.ExtraStats.wasfouled
	except:
		value = "0"
	Globals["OptaStatsForm"].WasFouled = value
		
	try:
		value = player.Stats.ExtraStats.fouls
	except:
		value = "0"
	Globals["OptaStatsForm"].Fouls = value
	
	try:
		value = player.Stats.ExtraStats.totalpass
	except:
		value = "0"
	Globals["OptaStatsForm"].TotalPass = value
	
	try:
		value = round((float(player.Stats.ExtraStats.accuratepass) * 100 / float(player.Stats.ExtraStats.totalpass)),1)
	except:			
		value = "0"
	Globals["OptaStatsForm"].PassAcc = value
	
	try:
		value =  player.Stats.ExtraStats.totalcross
	except:
		value = "0"
	Globals["OptaStatsForm"].TotalCross = value
	
	try:
		value = player.Stats.ExtraStats.totalscoringatt
	except:
		value = "0"
	Globals["OptaStatsForm"].TotalScoreAtt = value
	
	try:
		value = player.Stats.ExtraStats.ontargetscoringatt
	except:
		value = "0"
	Globals["OptaStatsForm"].OnTargetScoreAtt = value
	
	try:
		value = player.Stats.ExtraStats.totalattassist
	except:
		value = "0"
	Globals["OptaStatsForm"].TotalAttAssist = value
	
	try:
		value = player.Stats.ExtraStats.totaloffside
	except:
		value = "0"
	Globals["OptaStatsForm"].TotalOffside = value
		
	try:
		value = player.Stats.ExtraStats.touches
	except:
		value = "0"
	Globals["OptaStatsForm"].Touches = value
	
	try:
		value = player.Stats.ExtraStats.duelwon
	except:
		value = "0"
	Globals["OptaStatsForm"].DuelWon = value	
	
	try:
		value = player.Stats.ExtraStats.duellost
	except:
		value = "0"
	Globals["OptaStatsForm"].DuelLost = value
	
	try:
		value = player.Stats.ExtraStats.totaltackle
	except:
		value = "0"		
	Globals["OptaStatsForm"].TotalTackle = value	
	
	try:
		value = player.Stats.ExtraStats.totalclearance
	except:
		value = "0"	
	Globals["OptaStatsForm"].TotalClearance = value
	
	try:
		value = player.Stats.ExtraStats.ballrecovery
	except:
		value= "0"	
	Globals["OptaStatsForm"].BallRecovery = value
	
	try:
		value = player.Stats.ExtraStats.posslostall
	except:
		value = "0"	
	Globals["OptaStatsForm"].PossLostAll = value
	
	"""try:
		value = player.Stats.ExtraStats.goals
	except:
		value = "0"		
	Globals["OptaStatsForm"].Goals = value
	"""
	try:
		value = player.Stats.ExtraStats.yellowcard
	except:
		value = "0"	
	Globals["OptaStatsForm"].YellowCard = value
	
	try:
		value = player.Stats.ExtraStats.redcard
	except:
		value = "0"	
	Globals["OptaStatsForm"].RedCard = value

	try:
		value = player.Stats.ExtraStats.minsplayed
	except:
		value = "0"	
	Globals["OptaStatsForm"].MinsPlayed = value	
	
	try:
		value = player.CompetitionStats.YellowCards
	except:
		value = "0"	
	Globals["OptaStatsForm"].SsnYellow = value		

def RefreshTeamStats():
	hTeam = Game.HomeTeam
	aTeam = Game.AwayTeam
	
	try:
		Globals["OptaStatsForm"].HomeGoals = hTeam.Stats.GetValue("Goals")
	except:
		pass
	try:
		Globals["OptaStatsForm"].AwayGoals = aTeam.Stats.GetValue("Goals")
	except:
		pass
		

		
	try:
		value = hTeam.Stats.ExtraStats.totalscoringatt
	except:
		value = "0"			
	Globals["OptaStatsForm"].HomeScoreAtt = value

	try:
		value = aTeam.Stats.ExtraStats.totalscoringatt
	except:
		value = "0"			
	Globals["OptaStatsForm"].AwayScoreAtt = value

	#-----
	try:
		value = hTeam.Stats.ExtraStats.possessionpercentage
	except:
		value = "0"			
	
	Globals["OptaStatsForm"].HomePoss = value

	try:
		value = aTeam.Stats.ExtraStats.possessionpercentage
	except:
		value = "0"		
	
	Globals["OptaStatsForm"].AwayPoss = value
	
	#-----
	try:
		value = hTeam.Stats.ExtraStats.ontargetscoringatt
	except:
		value = "0"			
	Globals["OptaStatsForm"].HomeOnTargetScoringAtt = value

	try:
		value = aTeam.Stats.ExtraStats.ontargetscoringatt
	except:
		value = "0"			
	Globals["OptaStatsForm"].AwayOnTargetScoringAtt = value
	
	#-----
	try:
		value = hTeam.Stats.ExtraStats.totalpass
	except:
		value = "0"			
	Globals["OptaStatsForm"].HomeTotalPass = value

	try:
		value = aTeam.Stats.ExtraStats.totalpass
	except:
		value = "0"			
	Globals["OptaStatsForm"].AwayTotalPass = value
	
	#-----
	try:
		value = str(round((float(Game.HomeTeam.Stats.ExtraStats.accuratepass) * 100 / float(Game.HomeTeam.Stats.ExtraStats.totalpass)) ,1))
		
	except:
		value = "0"			
	Globals["OptaStatsForm"].HomePassAcc = value
	Globals["HomePassPerc"] = value
	
	try:
		value = str(round((float(Game.AwayTeam.Stats.ExtraStats.accuratepass)* 100  / float(Game.AwayTeam.Stats.ExtraStats.totalpass)) ,1))

	except:
		value = "0"			
	Globals["OptaStatsForm"].AwayPassAcc = value
	Globals["AwayPassPerc"] = value
	#-----
	try:
		value = hTeam.Stats.ExtraStats.totaloffside
	except:
		value = "0"			
	Globals["OptaStatsForm"].HomeOffside = value

	try:
		value = aTeam.Stats.ExtraStats.totaloffside
	except:
		value = "0"			
	Globals["OptaStatsForm"].AwayOffside = value
	
	#-----
	try:
		value = hTeam.Stats.ExtraStats.fkfoullost
	except:
		value = "0"			
	Globals["OptaStatsForm"].HomeFkFoulLost = value

	try:
		value = aTeam.Stats.ExtraStats.fkfoullost
	except:
		value = "0"			
	Globals["OptaStatsForm"].AwayFkFoulLost = value

	#-----
	try:
		value = hTeam.Stats.ExtraStats.totalyellowcard
	except:
		value = "0"			
	Globals["OptaStatsForm"].HomeTotalYellow = value

	try:
		value = aTeam.Stats.ExtraStats.totalyellowcard
	except:
		value = "0"			
	Globals["OptaStatsForm"].AwayTotalYellow = value
	
	#-----
	try:
		value = hTeam.Stats.ExtraStats.totalredcard
	except:
		value = "0"			
	Globals["OptaStatsForm"].HomeTotalRed = value

	try:
		value = aTeam.Stats.ExtraStats.totalredcard
	except:
		value = "0"			
	Globals["OptaStatsForm"].AwayTotalRed = value	
	
	#-----
	try:
		value = hTeam.Stats.ExtraStats.woncorners
	except:
		value = "0"			
	Globals["OptaStatsForm"].HomeCorners = value

	try:
		value = aTeam.Stats.ExtraStats.woncorners
	except:
		value = "0"			
	Globals["OptaStatsForm"].AwayCorners = value	

	"""
	try:
		value = hTeam.Stats.ExtraStats.goals
	except:
		value = "0"			
	Globals["OptaStatsForm"].HomeGoals = value

	try:
		value = aTeam.Stats.ExtraStats.goals
	except:
		value = "0"			
	Globals["OptaStatsForm"].AwayGoals = value	
	"""
	try:
		value = hTeam.Stats.ExtraStats.atthdtotal
	except:
		value = "0"			
	Globals["OptaStatsForm"].HomeHeader = value

	try:
		value = aTeam.Stats.ExtraStats.atthdtotal
	except:
		value = "0"			
	Globals["OptaStatsForm"].AwayHeader = value	
		
	#-----
	try:
		value = hTeam.Stats.ExtraStats.duelwon
	except:
		value = "0"			
	Globals["OptaStatsForm"].HomeDuels = value

	try:
		value = aTeam.Stats.ExtraStats.duelwon
	except:
		value = "0"			
	Globals["OptaStatsForm"].AwayDuels = value	

	#-----
	try:
		value = str(round((float(Game.HomeTeam.Stats.ExtraStats.duelwon) * 100) / (float(Game.HomeTeam.Stats.ExtraStats.duelwon) + float(Game.HomeTeam.Stats.ExtraStats.duellost)) , 1))
		
	except:
		value = "0"			
	Globals["OptaStatsForm"].HomeDuelsPerc = value

	try:
		value = str(round((float(Game.AwayTeam.Stats.ExtraStats.duelwon) * 100) / (float(Game.AwayTeam.Stats.ExtraStats.duelwon) + float(Game.AwayTeam.Stats.ExtraStats.duellost)) , 1))
	
	except:
		value = "0"			
	Globals["OptaStatsForm"].AwayDuelsPerc = value	
	
	#-----
	try:
		value = hTeam.Stats.ExtraStats.attemptsobox
	except:
		value = "0"			
	Globals["OptaStatsForm"].HomeAttOBox = value

	try:
		value = aTeam.Stats.ExtraStats.attemptsobox
	except:
		value = "0"			
	Globals["OptaStatsForm"].AwayAttOBox = value	
	#-----
	try:
		value = hTeam.Stats.ExtraStats.posslostall
	except:
		value = "0"			
	Globals["OptaStatsForm"].HomePossLoss = value

	try:
		value = aTeam.Stats.ExtraStats.posslostall
	except:
		value = "0"			
	Globals["OptaStatsForm"].AwayPossLoss = value
	#-----
	try:
		value = hTeam.CompetitionStats.YellowCards
	except:
		value = "0"			
	Globals["OptaStatsForm"].HomeSsnYellow = value

	try:
		value = aTeam.CompetitionStats.YellowCards
	except:
		value = "0"			
	Globals["OptaStatsForm"].AwaySsnYellow = value
