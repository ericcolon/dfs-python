import sys
sys.path.append('..')

from datetime import date
import sqlite3
import unittest
import BBRTestUtility
import projections

class TestProjections(unittest.TestCase):
	def setUp(self):
		self.testUtil = BBRTestUtility.BBRTestUtility()
		self.projections = projections.Projections(self.testUtil.conn)
		self.testUtil.runSQL()
		
		# Initialize the player info map.
		self.player_info = {
			"id": "",
			"name": "Test",
			"position": "G",
			"height": 0,
			"weight": 0,
			"url": "something"
		}
		
		# Initialize the player game totals map.
		self.game_totals_basic_info = {
			"player_id": "test",
			"season": date.today().year,
			"game_number": 0,
			"date": date.today(),
			"age": 0,
			"team": "BOS",
			"home": True,
			"opponent": "BOS",
			"result": "",
			"games_started": 0,
			"minutes_played": 0,
			"field_goals": 0,
			"field_goal_attempts": 0,
			"field_goal_pct": 0,
			"three_point_field_goals": 0,
			"three_point_field_goal_attempts": 0,
			"three_point_field_goal_pct": 0,
			"free_throws": 0,
			"free_throw_attempts": 0,
			"free_throw_pct": 0,
			"offensive_rebounds": 0,
			"defensive_rebounds": 0,
			"total_rebounds": 0,
			"assists": 0,
			"steals": 0,
			"blocks": 0,
			"turnovers": 0,
			"personal_fouls": 0,
			"points": 0,
			"game_score": 0,
			"plus_minus": 0
		}
		
		self.game_totals_advanced_info = {
			"player_id": "",
			"game_number": 0,
			"season": date.today().year,
			"date": date.today(),
			"age": 0,
			"team": "BOS",
			"home": True,
			"opponent": "NYK",
			"result": "",
			"games_started": 0,
			"minutes_played": 0,
			"true_shooting_pct": 0,
			"effective_field_goal_pct": 0,
			"offensive_rebound_pct": 0,
			"defensive_rebound_pct": 0,
			"total_rebound_pct": 0,
			"assist_pct": 0,
			"steal_pct": 0,
			"block_pct": 0,
			"turnover_pct": 0,
			"usage_pct": 0,
			"offensive_rating": 0,
			"defensive_rating": 0,
			"game_score": 0
		}
		
		# Initialize the team game totals map.
		self.team_game_totals_info = {
			"team": "",
			"season": date.today().year,
			"game": 0,
			"date": date.today(),
			"home": True,
			"opponent": "",
			"result": "",
			"minutes_played": 240,
			"field_goals": 0,
			"field_goal_attempts": 0,
			"three_point_field_goals": 0,
			"three_point_field_goal_attempts": 0,
			"free_throws": 0,
			"free_throw_attempts": 0,
			"offensive_rebounds": 0,
			"total_rebounds": 0,
			"assists": 0,
			"steals": 0,
			"blocks": 0,
			"turnovers": 0,
			"personal_fouls": 0,
			"points": 0,
			"opp_field_goals": 0,
			"opp_field_goal_attempts": 0,
			"opp_three_point_field_goals": 0,
			"opp_three_point_field_goal_attempts": 0,
			"opp_free_throws": 0,
			"opp_free_throw_attempts": 0,
			"opp_offensive_rebounds": 0,
			"opp_total_rebounds": 0,
			"opp_assists": 0,
			"opp_steals": 0,
			"opp_blocks": 0,
			"opp_turnovers": 0,
			"opp_personal_fouls": 0,
			"opp_points": 0
		}
	
	def tearDown(self):
		self.testUtil.conn.close()
		
		self.player_info = {}
	
	####################################################################################
	# Tests retrieval of player information from the players table, given a player_id.
	####################################################################################
	def test_get_player_info(self):
		self.player_info["id"] = "macleda01"
		self.player_info["name"] = "Dan"
		self.player_info["position"] = "G"
		self.player_info["height"] = 69
		self.player_info["weight"] = 175
		self.player_info["url"] = "something"
				
		self.testUtil.insert_into_players(self.player_info)
		info = self.projections.get_player_info("macleda01")
		
		self.assertTrue(len(info) > 0)
		self.assertTrue(info["id"] == self.player_info["id"])
	
	###############################################################################
	# Test the retrieval of the team that a player is on as of a particular date.
	###############################################################################
	def test_get_team(self):
		# Player is on Miami for game 1 of 2012
		self.game_totals_basic_info["player_id"] = "macleda01"
		self.game_totals_basic_info["season"] = 2012
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["team"] = "MIA"
		self.game_totals_basic_info["date"] = date(2012,11,1)
		
		# Player is on Philly for game 1 of 2013
		self.game_totals_basic_info["player_id"] = "macleda01"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["team"] = "PHI"
		self.game_totals_basic_info["date"] = date(2013,11,1)
		
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		self.assertTrue(self.projections.get_team("macleda01", 2013, date(2013,11,1)) == "PHI")
		
		# Player is on Boston for game 2 of 2013
		self.game_totals_basic_info["game_number"] = 2
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["date"] = date(2013,11,2)
				
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		self.assertTrue(self.projections.get_team("macleda01", 2013, date(2013,11,1)) == "PHI")
		self.assertTrue(self.projections.get_team("macleda01", 2013, date(2013,11,2)) == "BOS")

	###################################################################################
	# Tests the computation of the stats compiled against a team by its opponents
	#  at a position, starting from the beginning of the season to a particular date.
	###################################################################################
	def test_calculate_defense_vs_position(self):
		positions = ["G","F","C"]
		
		for p in positions:
			# Set up two guards that played against a team on separate days
			self.player_info["id"] = p + "1"
			self.player_info["name"] = p + " 1"
			self.player_info["position"] = p
			self.testUtil.insert_into_players(self.player_info)
		
			self.player_info["id"] = p + "2"
			self.player_info["name"] = p +" 2"
			self.testUtil.insert_into_players(self.player_info)
		
			self.game_totals_basic_info["player_id"] = p+"1"
			self.game_totals_basic_info["season"] = 2013
			self.game_totals_basic_info["game_number"] = 1
			self.game_totals_basic_info["team"] = "PHI"
			self.game_totals_basic_info["opponent"] = "BOS"
			self.game_totals_basic_info["date"] = date(2013,11,1)
			self.game_totals_basic_info["points"] = 20
			self.game_totals_basic_info["offensive_rebounds"] = 5
			self.game_totals_basic_info["defensive_rebounds"] = 10
			self.game_totals_basic_info["assists"] = 4
			self.game_totals_basic_info["steals"] = 3
			self.game_totals_basic_info["blocks"] = 2
			self.game_totals_basic_info["turnovers"] = 5
			self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
			self.game_totals_basic_info["player_id"] = p+"2"
			self.game_totals_basic_info["season"] = 2013
			self.game_totals_basic_info["game_number"] = 2
			self.game_totals_basic_info["team"] = "PHI"
			self.game_totals_basic_info["opponent"] = "BOS"
			self.game_totals_basic_info["date"] = date(2013,11,2)
			self.game_totals_basic_info["points"] = 10
			self.game_totals_basic_info["offensive_rebounds"] = 7
			self.game_totals_basic_info["defensive_rebounds"] = 12
			self.game_totals_basic_info["assists"] = 8
			self.game_totals_basic_info["steals"] = 1
			self.game_totals_basic_info["blocks"] = 0
			self.game_totals_basic_info["turnovers"] = 3
			self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
			# Set up team game total for 2nd game.
			self.team_game_totals_info["team"] = "BOS"
			self.team_game_totals_info["season"] = 2013
			self.team_game_totals_info["game"] = 2
			self.team_game_totals_info["date"] = date(2013,11,2)
			self.team_game_totals_info["opponent"] = "PHI"
			self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)
		
			points_vs_position = self.projections.calculate_defense_vs_position("points", p, "BOS", 2013, date(2013,11,2))
			offensive_rebs_vs_position = self.projections.calculate_defense_vs_position("offensive_rebounds", p, "BOS", 2013, date(2013,11,2))
			defensive_rebs_vs_position = self.projections.calculate_defense_vs_position("defensive_rebounds", p, "BOS", 2013, date(2013,11,2))
			assists_vs_position = self.projections.calculate_defense_vs_position("assists", p, "BOS", 2013, date(2013,11,2))
			steals_vs_position = self.projections.calculate_defense_vs_position("steals", p, "BOS", 2013, date(2013,11,2))
			blocks_vs_position = self.projections.calculate_defense_vs_position("blocks", p, "BOS", 2013, date(2013,11,2))
			turnovers_vs_position = self.projections.calculate_defense_vs_position("turnovers", p, "BOS", 2013, date(2013,11,2))

			self.assertTrue(points_vs_position == 15)
			self.assertTrue(offensive_rebs_vs_position == 6)
			self.assertTrue(defensive_rebs_vs_position == 11)
			self.assertTrue(assists_vs_position == 6)
			self.assertTrue(steals_vs_position == 2)
			self.assertTrue(blocks_vs_position == 1)
			self.assertTrue(turnovers_vs_position == 4)
	
	####################################################################################
	# Same test as above, except we specify a date that would exclude the second game.
	# This date should eliminate the second player's stats from the computation.
	####################################################################################
	def test_calculate_defense_vs_position_date_subset(self):
		positions = ["G","F","C"]
		
		for p in positions:
			# Set up two guards that played against a team on separate days
			self.player_info["id"] = p + "1"
			self.player_info["name"] = p + " 1"
			self.player_info["position"] = p
			self.testUtil.insert_into_players(self.player_info)
		
			self.player_info["id"] = p + "2"
			self.player_info["name"] = p +" 2"
			self.testUtil.insert_into_players(self.player_info)
		
			self.game_totals_basic_info["player_id"] = p+"1"
			self.game_totals_basic_info["season"] = 2013
			self.game_totals_basic_info["game_number"] = 1
			self.game_totals_basic_info["team"] = "PHI"
			self.game_totals_basic_info["opponent"] = "BOS"
			self.game_totals_basic_info["date"] = date(2013,11,1)
			self.game_totals_basic_info["points"] = 20
			self.game_totals_basic_info["offensive_rebounds"] = 5
			self.game_totals_basic_info["defensive_rebounds"] = 10
			self.game_totals_basic_info["assists"] = 4
			self.game_totals_basic_info["steals"] = 3
			self.game_totals_basic_info["blocks"] = 2
			self.game_totals_basic_info["turnovers"] = 5
			self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
			self.game_totals_basic_info["player_id"] = p+"2"
			self.game_totals_basic_info["season"] = 2013
			self.game_totals_basic_info["game_number"] = 2
			self.game_totals_basic_info["team"] = "PHI"
			self.game_totals_basic_info["opponent"] = "BOS"
			self.game_totals_basic_info["date"] = date(2013,11,4)
			self.game_totals_basic_info["points"] = 10
			self.game_totals_basic_info["offensive_rebounds"] = 7
			self.game_totals_basic_info["defensive_rebounds"] = 12
			self.game_totals_basic_info["assists"] = 8
			self.game_totals_basic_info["steals"] = 1
			self.game_totals_basic_info["blocks"] = 0
			self.game_totals_basic_info["turnovers"] = 3
			self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
			# Set up team game total for 2nd game.
			self.team_game_totals_info["team"] = "BOS"
			self.team_game_totals_info["season"] = 2013
			self.team_game_totals_info["game"] = 1
			self.team_game_totals_info["date"] = date(2013,11,1)
			self.team_game_totals_info["opponent"] = "PHI"
			self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)
			
			self.team_game_totals_info["team"] = "BOS"
			self.team_game_totals_info["season"] = 2013
			self.team_game_totals_info["game"] = 2
			self.team_game_totals_info["date"] = date(2013,11,4)
			self.team_game_totals_info["opponent"] = "PHI"
			self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)
		
			points_vs_position = self.projections.calculate_defense_vs_position("points", p, "BOS", 2013, date(2013,11,2))
			offensive_rebs_vs_position = self.projections.calculate_defense_vs_position("offensive_rebounds", p, "BOS", 2013, date(2013,11,2))
			defensive_rebs_vs_position = self.projections.calculate_defense_vs_position("defensive_rebounds", p, "BOS", 2013, date(2013,11,2))
			assists_vs_position = self.projections.calculate_defense_vs_position("assists", p, "BOS", 2013, date(2013,11,2))
			steals_vs_position = self.projections.calculate_defense_vs_position("steals", p, "BOS", 2013, date(2013,11,2))
			blocks_vs_position = self.projections.calculate_defense_vs_position("blocks", p, "BOS", 2013, date(2013,11,2))
			turnovers_vs_position = self.projections.calculate_defense_vs_position("turnovers", p, "BOS", 2013, date(2013,11,2))

			self.assertTrue(points_vs_position == 20)
			self.assertTrue(offensive_rebs_vs_position == 5)
			self.assertTrue(defensive_rebs_vs_position == 10)
			self.assertTrue(assists_vs_position == 4)
			self.assertTrue(steals_vs_position == 3)
			self.assertTrue(blocks_vs_position == 2)
			self.assertTrue(turnovers_vs_position == 5)

	def test_calculate_league_avg(self):
		positions = ["G","F","C"]
		
		for p in positions:
			# Set up three players that played against a team on separate days
			self.player_info["id"] = p + "1"
			self.player_info["name"] = p + " 1"
			self.player_info["position"] = p
			self.testUtil.insert_into_players(self.player_info)
		
			self.player_info["id"] = p + "2"
			self.player_info["name"] = p +" 2"
			self.testUtil.insert_into_players(self.player_info)
			
			self.player_info["id"] = p + "3"
			self.player_info["name"] = p +" 3"
			self.testUtil.insert_into_players(self.player_info)
		
			self.game_totals_basic_info["player_id"] = p+"1"
			self.game_totals_basic_info["season"] = 2013
			self.game_totals_basic_info["game_number"] = 1
			self.game_totals_basic_info["team"] = "PHI"
			self.game_totals_basic_info["opponent"] = "BOS"
			self.game_totals_basic_info["date"] = date(2013,11,1)
			self.game_totals_basic_info["points"] = 20
			self.game_totals_basic_info["offensive_rebounds"] = 5
			self.game_totals_basic_info["defensive_rebounds"] = 10
			self.game_totals_basic_info["assists"] = 4
			self.game_totals_basic_info["steals"] = 3
			self.game_totals_basic_info["blocks"] = 2
			self.game_totals_basic_info["turnovers"] = 5
			self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
			self.game_totals_basic_info["player_id"] = p+"2"
			self.game_totals_basic_info["season"] = 2013
			self.game_totals_basic_info["game_number"] = 2
			self.game_totals_basic_info["team"] = "LAL"
			self.game_totals_basic_info["opponent"] = "ATL"
			self.game_totals_basic_info["date"] = date(2013,11,4)
			self.game_totals_basic_info["points"] = 10
			self.game_totals_basic_info["offensive_rebounds"] = 7
			self.game_totals_basic_info["defensive_rebounds"] = 12
			self.game_totals_basic_info["assists"] = 8
			self.game_totals_basic_info["steals"] = 1
			self.game_totals_basic_info["blocks"] = 0
			self.game_totals_basic_info["turnovers"] = 3
			self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
			
			self.game_totals_basic_info["player_id"] = p+"3"
			self.game_totals_basic_info["season"] = 2013
			self.game_totals_basic_info["game_number"] = 3
			self.game_totals_basic_info["team"] = "DET"
			self.game_totals_basic_info["opponent"] = "BOS"
			self.game_totals_basic_info["date"] = date(2013,11,5)
			self.game_totals_basic_info["points"] = 30
			self.game_totals_basic_info["offensive_rebounds"] = 7
			self.game_totals_basic_info["defensive_rebounds"] = 12
			self.game_totals_basic_info["assists"] = 8
			self.game_totals_basic_info["steals"] = 1
			self.game_totals_basic_info["blocks"] = 0
			self.game_totals_basic_info["turnovers"] = 3
			self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
			# Team game totals for ATL and BOS
			self.team_game_totals_info["team"] = "BOS"
			self.team_game_totals_info["season"] = 2013
			self.team_game_totals_info["game"] = 1
			self.team_game_totals_info["date"] = date(2013,11,1)
			self.team_game_totals_info["opponent"] = "PHI"
			self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)
			
			self.team_game_totals_info["team"] = "BOS"
			self.team_game_totals_info["season"] = 2013
			self.team_game_totals_info["game"] = 2
			self.team_game_totals_info["date"] = date(2013,11,5)
			self.team_game_totals_info["opponent"] = "DET"
			self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)
			
			self.team_game_totals_info["team"] = "ATL"
			self.team_game_totals_info["season"] = 2013
			self.team_game_totals_info["game"] = 3
			self.team_game_totals_info["date"] = date(2013,11,4)
			self.team_game_totals_info["opponent"] = "LAL"
			self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)
			
			# BOS had 50 pts scored against them over 2 games = 25/ppg
			# ATL had 10 pts scored against them over 3 games = 3.3/ppg
			#
			# 2 teams, yielding 25+3.3 ppg = 28.3/2 = ~14
			points = self.projections.calculate_league_avg("points", p, 2013)
			self.assertTrue(points == 14)
	
	def test_calculate_league_avg_with_date(self):
		positions = ["G","F","C"]
		
		for p in positions:
			# Set up three players that played against a team on separate days
			self.player_info["id"] = p + "1"
			self.player_info["name"] = p + " 1"
			self.player_info["position"] = p
			self.testUtil.insert_into_players(self.player_info)
		
			self.player_info["id"] = p + "2"
			self.player_info["name"] = p +" 2"
			self.testUtil.insert_into_players(self.player_info)
			
			self.player_info["id"] = p + "3"
			self.player_info["name"] = p +" 3"
			self.testUtil.insert_into_players(self.player_info)
		
			self.game_totals_basic_info["player_id"] = p+"1"
			self.game_totals_basic_info["season"] = 2013
			self.game_totals_basic_info["game_number"] = 1
			self.game_totals_basic_info["team"] = "PHI"
			self.game_totals_basic_info["opponent"] = "BOS"
			self.game_totals_basic_info["date"] = date(2013,11,1)
			self.game_totals_basic_info["points"] = 20
			self.game_totals_basic_info["offensive_rebounds"] = 5
			self.game_totals_basic_info["defensive_rebounds"] = 10
			self.game_totals_basic_info["assists"] = 4
			self.game_totals_basic_info["steals"] = 3
			self.game_totals_basic_info["blocks"] = 2
			self.game_totals_basic_info["turnovers"] = 5
			self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
			self.game_totals_basic_info["player_id"] = p+"2"
			self.game_totals_basic_info["season"] = 2013
			self.game_totals_basic_info["game_number"] = 2
			self.game_totals_basic_info["team"] = "LAL"
			self.game_totals_basic_info["opponent"] = "ATL"
			self.game_totals_basic_info["date"] = date(2013,11,4)
			self.game_totals_basic_info["points"] = 10
			self.game_totals_basic_info["offensive_rebounds"] = 7
			self.game_totals_basic_info["defensive_rebounds"] = 12
			self.game_totals_basic_info["assists"] = 8
			self.game_totals_basic_info["steals"] = 1
			self.game_totals_basic_info["blocks"] = 0
			self.game_totals_basic_info["turnovers"] = 3
			self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
			
			self.game_totals_basic_info["player_id"] = p+"3"
			self.game_totals_basic_info["season"] = 2013
			self.game_totals_basic_info["game_number"] = 3
			self.game_totals_basic_info["team"] = "DET"
			self.game_totals_basic_info["opponent"] = "BOS"
			self.game_totals_basic_info["date"] = date(2013,11,5)
			self.game_totals_basic_info["points"] = 30
			self.game_totals_basic_info["offensive_rebounds"] = 7
			self.game_totals_basic_info["defensive_rebounds"] = 12
			self.game_totals_basic_info["assists"] = 8
			self.game_totals_basic_info["steals"] = 1
			self.game_totals_basic_info["blocks"] = 0
			self.game_totals_basic_info["turnovers"] = 3
			self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
			# Team game totals for ATL and BOS
			self.team_game_totals_info["team"] = "BOS"
			self.team_game_totals_info["season"] = 2013
			self.team_game_totals_info["game"] = 1
			self.team_game_totals_info["date"] = date(2013,11,1)
			self.team_game_totals_info["opponent"] = "PHI"
			self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)
			
			self.team_game_totals_info["team"] = "BOS"
			self.team_game_totals_info["season"] = 2013
			self.team_game_totals_info["game"] = 2
			self.team_game_totals_info["date"] = date(2013,11,5)
			self.team_game_totals_info["opponent"] = "DET"
			self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)
			
			self.team_game_totals_info["team"] = "ATL"
			self.team_game_totals_info["season"] = 2013
			self.team_game_totals_info["game"] = 3
			self.team_game_totals_info["date"] = date(2013,11,4)
			self.team_game_totals_info["opponent"] = "LAL"
			self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)
			
			# BOS had 20 pts scored against them over 1 game on or before 11/4 = 20/ppg
			# ATL had 10 pts scored against them over 3 games on or before 11/4 = 3.3/ppg
			#
			# 2 teams, yielding 25+3.3 ppg = 23.3/2 = ~11
			points = self.projections.calculate_league_avg("points", p, 2013, date(2013,11,4))
			self.assertTrue(points == 11)
		
	def test_get_baseline(self):
		# Write basic game totals for player
		self.game_totals_basic_info["player_id"] = "macleda01"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["team"] = "LAL"
		self.game_totals_basic_info["opponent"] = "ATL"
		self.game_totals_basic_info["date"] = date(2013,11,4)
		self.game_totals_basic_info["points"] = 10
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		self.game_totals_basic_info["game_number"] = 2
		self.game_totals_basic_info["date"] = date(2013,11,5)
		self.game_totals_basic_info["points"] = 20
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		# Write advanced game totals for player
		self.game_totals_advanced_info["player_id"] = "macleda01"
		self.game_totals_advanced_info["date"] = date(2013,11,4)
		self.game_totals_advanced_info["usage_pct"] = 10.6
		self.game_totals_advanced_info["offensive_rating"] = 100
		self.game_totals_advanced_info["defensive_rating"] = 101
		self.testUtil.insert_into_game_totals_advanced(self.game_totals_advanced_info)
		
		self.game_totals_advanced_info["date"] = date(2013,11,5)
		self.game_totals_advanced_info["usage_pct"] = 12.6
		self.game_totals_advanced_info["offensive_rating"] = 104
		self.game_totals_advanced_info["defensive_rating"] = 103
		self.testUtil.insert_into_game_totals_advanced(self.game_totals_advanced_info)
		
		baseline = self.projections.get_baseline("macleda01", 2013, "points")
		self.assertTrue(baseline[0] == 15)	# avg points
		self.assertTrue(baseline[1] == 11.6)	# usage
		self.assertTrue(baseline[2] == 102)	# off rating
		self.assertTrue(baseline[3] == 102)	# def rating
	
	def test_get_baseline_with_date(self):
		# Write basic game totals for player
		self.game_totals_basic_info["player_id"] = "macleda01"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["team"] = "LAL"
		self.game_totals_basic_info["opponent"] = "ATL"
		self.game_totals_basic_info["date"] = date(2013,11,4)
		self.game_totals_basic_info["points"] = 10
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		self.game_totals_basic_info["game_number"] = 2
		self.game_totals_basic_info["date"] = date(2013,11,5)
		self.game_totals_basic_info["points"] = 20
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		# Write advanced game totals for player
		self.game_totals_advanced_info["player_id"] = "macleda01"
		self.game_totals_advanced_info["date"] = date(2013,11,4)
		self.game_totals_advanced_info["usage_pct"] = 10.6
		self.game_totals_advanced_info["offensive_rating"] = 100
		self.game_totals_advanced_info["defensive_rating"] = 101
		self.testUtil.insert_into_game_totals_advanced(self.game_totals_advanced_info)
		
		self.game_totals_advanced_info["date"] = date(2013,11,5)
		self.game_totals_advanced_info["usage_pct"] = 12.6
		self.game_totals_advanced_info["offensive_rating"] = 104
		self.game_totals_advanced_info["defensive_rating"] = 103
		self.testUtil.insert_into_game_totals_advanced(self.game_totals_advanced_info)
		
		baseline = self.projections.get_baseline("macleda01", 2013, "points", date(2013,11,4))
		self.assertTrue(baseline[0] == 10)	# avg points
		self.assertTrue(baseline[1] == 10.6)	# usage
		self.assertTrue(baseline[2] == 100)	# off rating
		self.assertTrue(baseline[3] == 101)	# def rating
		
if __name__ == '__main__':
	unittest.main()