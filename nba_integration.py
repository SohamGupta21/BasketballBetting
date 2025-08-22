"""
NBA API Integration for Basketball Simulation
Uses the official nba_api package for reliable data access
"""

import time
from typing import Dict, List, Optional, Tuple
import player
import team

# NBA API imports - install with: pip install nba_api
try:
    from nba_api.stats.endpoints import (
        commonteamroster,
        playerdashboardbyyearoveryear,
    )
    from nba_api.stats.static import teams
    NBA_API_AVAILABLE = True
    print("✅ NBA API available!")
except ImportError:
    NBA_API_AVAILABLE = False
    print("⚠️  NBA API not installed. Run: pip install nba_api")


class NBADataManager:
    """
    NBA data manager using the official nba_api package.
    Handles fetching real NBA team rosters and player statistics.
    """
    
    def __init__(self):
        if not NBA_API_AVAILABLE:
            raise ImportError("nba_api package is required. Install with: pip install nba_api")
        
        # Cache for reducing API calls
        self._team_cache = {}
        self._player_cache = {}
        self._roster_cache = {}
        print("🏀 NBA Data Manager initialized!")
    
    def get_all_teams(self) -> List[Dict]:
        """Get all NBA teams using nba_api static data"""
        try:
            print("📋 Fetching all NBA teams...")
            all_teams = teams.get_teams()
            team_list = [
                {
                    'id': team['id'],
                    'name': team['full_name'], 
                    'abbreviation': team['abbreviation'],
                    'city': team['city'],
                    'nickname': team['nickname']
                }
                for team in all_teams
            ]
            print(f"✅ Found {len(team_list)} NBA teams")
            return team_list
        except Exception as e:
            print(f"❌ Error fetching teams: {e}")
            return []
    
    def get_popular_teams(self) -> List[Tuple[str, int]]:
        """Get popular NBA teams for easy selection"""
        print("🌟 Loading popular teams...")
        popular_team_names = [
            'Los Angeles Lakers', 'Golden State Warriors', 'Boston Celtics',
            'Miami Heat', 'Chicago Bulls', 'New York Knicks', 'Brooklyn Nets',
            'Philadelphia 76ers', 'Milwaukee Bucks', 'Denver Nuggets',
            'Phoenix Suns', 'Dallas Mavericks', 'Toronto Raptors',
            'Los Angeles Clippers', 'Memphis Grizzlies', 'Atlanta Hawks'
        ]
        
        all_teams = self.get_all_teams()
        popular_teams = []
        
        for team_name in popular_team_names:
            for team in all_teams:
                if team['name'] == team_name:
                    popular_teams.append((team['name'], team['id']))
                    break
        
        print(f"✅ Loaded {len(popular_teams)} popular teams")
        return popular_teams
    
    def get_team_roster(self, team_id: int, season: str = '2024-25') -> List[Dict]:
        """Get team roster using nba_api"""
        cache_key = f"{team_id}_{season}"
        if cache_key in self._roster_cache:
            print(f"📋 Using cached roster for team {team_id}")
            return self._roster_cache[cache_key]
        
        try:
            print(f"🔄 Fetching roster for team ID {team_id} (Season: {season})...")
            time.sleep(0.5)  # Rate limiting
            roster_data = commonteamroster.CommonTeamRoster(team_id=team_id, season=season)
            roster_df = roster_data.get_data_frames()[0]
            
            roster = []
            for _, row in roster_df.iterrows():
                roster.append({
                    'id': row['PLAYER_ID'],
                    'name': row['PLAYER'],
                    'position': row['POSITION'],
                    'height': row['HEIGHT'],
                    'weight': row['WEIGHT'],
                    'age': row['AGE'] if row['AGE'] else 25,
                    'experience': row['EXP'],
                    'jersey_number': row['NUM']
                })
            
            self._roster_cache[cache_key] = roster
            print(f"✅ Found {len(roster)} players on roster")
            return roster
            
        except Exception as e:
            print(f"❌ Error fetching roster for team {team_id}: {e}")
            return []
    
    def get_player_season_stats(self, player_id: int, season: str = '2024-25') -> Optional[Dict]:
        """Get player season statistics - this is where we get the shooting percentages!"""
        cache_key = f"{player_id}_{season}"
        if cache_key in self._player_cache:
            return self._player_cache[cache_key]
        
        try:
            print(f"📊 Fetching stats for player ID {player_id} (Season: {season})...")
            time.sleep(0.5)  # Rate limiting - NBA API doesn't like rapid requests
            
            # This is the key endpoint for getting player percentages and stats
            dashboard = playerdashboardbyyearoveryear.PlayerDashboardByYearOverYear(
                player_id=player_id, 
                season=season
            )
            
            # Get the season totals dataframe - this has all the shooting percentages
            season_totals_df = dashboard.get_data_frames()[1]  # SeasonTotalsRegularSeason
            
            if season_totals_df.empty:
                print(f"⚠️  No stats found for player {player_id}")
                return None
            
            # Get the most recent season data
            latest_season = season_totals_df.iloc[0]
            
            # Extract all the key stats we need for simulation
            games_played = max(latest_season.get('GP', 1), 1)  # Prevent division by zero
            
            stats = {
                'games_played': latest_season.get('GP', 0),
                'minutes_per_game': latest_season.get('MIN', 0) / games_played,
                'points_per_game': latest_season.get('PTS', 0) / games_played,
                'assists_per_game': latest_season.get('AST', 0) / games_played,
                'rebounds_per_game': latest_season.get('REB', 0) / games_played,
                'steals_per_game': latest_season.get('STL', 0) / games_played,
                'blocks_per_game': latest_season.get('BLK', 0) / games_played,
                'turnovers_per_game': latest_season.get('TOV', 0) / games_played,
                # These are the key shooting percentages we convert to simulation attributes
                'fg_percentage': latest_season.get('FG_PCT', 0.45),      # Field Goal %
                'fg3_percentage': latest_season.get('FG3_PCT', 0.35),    # 3-Point %
                'ft_percentage': latest_season.get('FT_PCT', 0.75),      # Free Throw %
                'fg_attempts_per_game': latest_season.get('FGA', 0) / games_played,
                'fg3_attempts_per_game': latest_season.get('FG3A', 0) / games_played,
                # Raw totals for reference
                'total_minutes': latest_season.get('MIN', 0),
                'total_points': latest_season.get('PTS', 0),
                'total_assists': latest_season.get('AST', 0),
                'total_rebounds': latest_season.get('REB', 0)
            }
            
            print(f"✅ Got stats: {stats['points_per_game']:.1f} PPG, {stats['fg_percentage']:.1%} FG%, {stats['fg3_percentage']:.1%} 3P%")
            
            self._player_cache[cache_key] = stats
            return stats
            
        except Exception as e:
            print(f"❌ Error fetching stats for player {player_id}: {e}")
            return None
    
    def convert_position_to_number(self, position_str: str) -> int:
        """Convert NBA position string to our 1-5 simulation position number"""
        print(f"🔄 Converting position '{position_str}' to number...")
        position_mapping = {
            'PG': 1, 'Point Guard': 1,
            'SG': 2, 'Shooting Guard': 2, 'Guard': 2,
            'SF': 3, 'Small Forward': 3, 'Forward': 3,
            'PF': 4, 'Power Forward': 4,
            'C': 5, 'Center': 5,
            'G': 2,  'F': 3, 'F-C': 4, 'C-F': 4, 'G-F': 2
        }
        
        # Handle multi-position players (e.g., "PG-SG")
        if '-' in position_str:
            primary_pos = position_str.split('-')[0]
            result = position_mapping.get(primary_pos, 3)
        else:
            result = position_mapping.get(position_str, 3)
        
        print(f"✅ '{position_str}' → {result} ({player.POSITIONS[result]})")
        return result
    
    def convert_stats_to_simulation_attributes(self, stats: Dict, position: int) -> Dict:
        """
        This is the magic function! Convert NBA shooting percentages and stats 
        to our simulation's 0-100 attribute system
        """
        if not stats:
            print("⚠️  No stats available, using position defaults")
            return self._get_position_defaults(position)
        
        print(f"🔧 Converting NBA stats to simulation attributes for position {position}...")
        
        # Extract stats with safe defaults
        ppg = max(0, stats.get('points_per_game', 10))
        apg = max(0, stats.get('assists_per_game', 2))
        rpg = max(0, stats.get('rebounds_per_game', 4))
        spg = max(0, stats.get('steals_per_game', 1))
        bpg = max(0, stats.get('blocks_per_game', 0.5))
        mpg = max(10, min(40, stats.get('minutes_per_game', 20)))
        
        # These are the key conversions - NBA percentages to 0-100 scale
        fg_pct = max(0.3, min(0.7, stats.get('fg_percentage', 0.45)))      # Clamp realistic range
        fg3_pct = max(0.2, min(0.5, stats.get('fg3_percentage', 0.35)))    # 20% to 50% is realistic
        ft_pct = max(0.5, min(0.95, stats.get('ft_percentage', 0.75)))     # 50% to 95%
        
        print(f"📊 Raw shooting: {fg_pct:.1%} FG, {fg3_pct:.1%} 3P, {ft_pct:.1%} FT")
        
        # Convert shooting percentages to simulation scale (roughly 30-100)
        shooting_base = int(fg_pct * 150)  # 0.45 FG% → 67.5 → 67
        three_point_skill = int(fg3_pct * 200)  # 0.35 3P% → 70
        ft_skill = int(ft_pct * 120)  # 0.75 FT% → 90
        
        # Scoring volume affects close/mid range (good scorers get boost)
        scoring_factor = min(2.0, ppg / 15.0)  # Players scoring 15+ PPG get boost
        close_range = min(100, max(40, int(shooting_base * 1.2 * scoring_factor)))
        mid_range = min(100, max(40, int(shooting_base * scoring_factor)))
        
        print(f"🎯 Shooting skills: Close={close_range}, Mid={mid_range}, Long={three_point_skill}, FT={ft_skill}")
        
        # Position-specific modifiers
        position_mods = self._get_position_modifiers(position)
        
        # Passing skill based on assists (PGs get bigger multiplier)
        base_passing = int(apg * position_mods['passing_multiplier'])
        passing_skill = min(100, max(position_mods['min_passing'], base_passing))
        
        # Speed and dribbling based on position and performance
        speed = min(100, max(position_mods['min_speed'], 
                           position_mods['base_speed'] + int((apg + spg) * 3)))
        dribbling = min(100, max(position_mods['min_dribbling'],
                               position_mods['base_dribbling'] + int(apg * 4)))
        
        # Defensive stats from counting stats
        steal_skill = min(100, max(30, int(spg * 50)))
        block_skill = min(100, max(20, int(bpg * 60)))
        rebound_skill = min(100, max(30, int(rpg * position_mods['rebound_multiplier'])))
        defense_skill = min(100, max(40, 50 + int((spg + bpg) * 15)))
        
        # Stamina based on minutes played
        stamina = min(100, max(50, int(mpg * 2.5)))
        
        # Driving abilities based on position and scoring
        layup_base = position_mods['layup_base']
        dunk_base = position_mods['dunk_base']
        
        layup_skill = min(100, max(layup_base, layup_base + int(scoring_factor * 20)))
        dunk_skill = min(100, max(dunk_base, dunk_base + int(scoring_factor * 15)))
        
        attributes = {
            'shooting': {
                'close': close_range,
                'mid': mid_range,
                'long': three_point_skill,
                'ft': ft_skill
            },
            'driving': {
                'layups': layup_skill,
                'dunking': dunk_skill
            },
            'skills': {
                'speed': speed,
                'dribbling': dribbling,
                'passing': passing_skill,
                'stamina': stamina
            },
            'defense': {
                'rebounding': rebound_skill,
                'defense': defense_skill,
                'blocking': block_skill,
                'stealing': steal_skill
            }
        }
        
        print(f"✅ Converted to simulation attributes!")
        print(f"   Shooting: {attributes['shooting']}")
        print(f"   Skills: {attributes['skills']}")
        
        return attributes
    
    def _get_position_modifiers(self, position: int) -> Dict:
        """Get position-specific modifiers for attribute calculation"""
        modifiers = {
            1: {  # PG - Point Guards are the best passers and fastest
                'passing_multiplier': 15, 'min_passing': 60,
                'base_speed': 70, 'min_speed': 60,
                'base_dribbling': 65, 'min_dribbling': 55,
                'rebound_multiplier': 8, 'layup_base': 50, 'dunk_base': 30
            },
            2: {  # SG - Shooting Guards are great shooters, good athletes
                'passing_multiplier': 12, 'min_passing': 45,
                'base_speed': 65, 'min_speed': 55,
                'base_dribbling': 60, 'min_dribbling': 50,
                'rebound_multiplier': 10, 'layup_base': 55, 'dunk_base': 40
            },
            3: {  # SF - Small Forwards are versatile
                'passing_multiplier': 10, 'min_passing': 50,
                'base_speed': 60, 'min_speed': 50,
                'base_dribbling': 55, 'min_dribbling': 45,
                'rebound_multiplier': 12, 'layup_base': 60, 'dunk_base': 45
            },
            4: {  # PF - Power Forwards are strong rebounders and scorers inside
                'passing_multiplier': 8, 'min_passing': 40,
                'base_speed': 50, 'min_speed': 40,
                'base_dribbling': 45, 'min_dribbling': 35,
                'rebound_multiplier': 15, 'layup_base': 65, 'dunk_base': 55
            },
            5: {  # C - Centers dominate inside, rebound, block shots
                'passing_multiplier': 6, 'min_passing': 35,
                'base_speed': 45, 'min_speed': 35,
                'base_dribbling': 40, 'min_dribbling': 30,
                'rebound_multiplier': 18, 'layup_base': 70, 'dunk_base': 60
            }
        }
        return modifiers.get(position, modifiers[3])
    
    def _get_position_defaults(self, position: int) -> Dict:
        """Get default attributes when no NBA stats available"""
        defaults = {
            1: {  # PG
                'shooting': {'close': 65, 'mid': 70, 'long': 75, 'ft': 80},
                'driving': {'layups': 70, 'dunking': 50},
                'skills': {'speed': 85, 'dribbling': 80, 'passing': 85, 'stamina': 75},
                'defense': {'rebounding': 45, 'defense': 65, 'blocking': 30, 'stealing': 70}
            },
            2: {  # SG
                'shooting': {'close': 70, 'mid': 75, 'long': 80, 'ft': 82},
                'driving': {'layups': 75, 'dunking': 60},
                'skills': {'speed': 80, 'dribbling': 75, 'passing': 65, 'stamina': 75},
                'defense': {'rebounding': 50, 'defense': 70, 'blocking': 35, 'stealing': 65}
            },
            3: {  # SF
                'shooting': {'close': 72, 'mid': 70, 'long': 75, 'ft': 78},
                'driving': {'layups': 75, 'dunking': 65},
                'skills': {'speed': 75, 'dribbling': 70, 'passing': 70, 'stamina': 80},
                'defense': {'rebounding': 65, 'defense': 72, 'blocking': 45, 'stealing': 60}
            },
            4: {  # PF
                'shooting': {'close': 75, 'mid': 65, 'long': 60, 'ft': 75},
                'driving': {'layups': 80, 'dunking': 75},
                'skills': {'speed': 65, 'dribbling': 60, 'passing': 55, 'stamina': 80},
                'defense': {'rebounding': 80, 'defense': 75, 'blocking': 65, 'stealing': 50}
            },
            5: {  # C
                'shooting': {'close': 80, 'mid': 55, 'long': 45, 'ft': 70},
                'driving': {'layups': 85, 'dunking': 80},
                'skills': {'speed': 55, 'dribbling': 50, 'passing': 45, 'stamina': 75},
                'defense': {'rebounding': 85, 'defense': 80, 'blocking': 80, 'stealing': 45}
            }
        }
        return defaults.get(position, defaults[3])
    
    def create_nba_player(self, player_data: Dict) -> Optional[player.Player]:
        """Create a Player object from NBA data - this brings it all together!"""
        try:
            print(f"🏀 Creating player: {player_data['name']}")
            
            # Step 1: Get player stats (shooting percentages, etc.)
            stats = self.get_player_season_stats(player_data['id'])
            
            # Step 2: Convert position
            position = self.convert_position_to_number(player_data['position'])
            
            # Step 3: Create basic player object (this uses your existing Player class)
            p = player.Player(player_data['name'], position)
            
            # Step 4: Convert NBA stats to simulation attributes
            attributes = self.convert_stats_to_simulation_attributes(stats, position)
            
            # Step 5: Override the randomly generated attributes with NBA-based ones
            p.shooting = attributes['shooting']
            p.driving = attributes['driving'] 
            p.skills = attributes['skills']
            p.defense = attributes['defense']
            
            # Step 6: Recalculate derived stats (from your existing Player class)
            p.complete_pass = p.skills['passing'] / 100.0
            p.protect_drive = (0.60 * p.skills['dribbling'] + 0.40 * p.skills['speed']) / 100.0
            p.steal_drive = (0.40 * p.defense['defense'] + 0.30 * p.skills['speed'] + 0.30 * p.defense['stealing']) / 100.0
            p.steal_pass = (0.25 * p.defense['defense'] + 0.35 * p.skills['speed'] + 0.40 * p.defense['stealing']) / 100.0
            p.block_chance = (0.80 * p.defense['blocking'] + 0.40 * p.defense['defense']) / 750.0
            
            print(f"✅ Created {p.name} ({p.position_string})")
            return p
            
        except Exception as e:
            print(f"❌ Error creating player {player_data.get('name', 'Unknown')}: {e}")
            return None
    
    def create_nba_team(self, team_name: str, team_id: int) -> Optional[team.Team]:
        """Create a Team object with real NBA players"""
        print(f"🏀 Creating NBA team: {team_name}")
        print("=" * 50)
        
        # Step 1: Get roster
        roster_data = self.get_team_roster(team_id)
        if not roster_data:
            print(f"❌ Could not fetch roster for {team_name}")
            return None
        
        print(f"📋 Processing {len(roster_data)} players...")
        players_created = []
        
        # Step 2: Process each player (limit to 12 for performance)
        for i, player_data in enumerate(roster_data):
            if len(players_created) >= 12:  # Limit roster size
                break
                
            print(f"\n🔄 Processing {i+1}/{min(12, len(roster_data))}: {player_data['name']}")
            nba_player = self.create_nba_player(player_data)
            
            if nba_player:
                players_created.append(nba_player)
            
            # Small delay to be nice to the API
            time.sleep(0.1)
        
        if len(players_created) < 8:
            print(f"⚠️  Warning: Only created {len(players_created)} players for {team_name}")
            return None
        
        # Step 3: Ensure positional balance
        players_created = self._balance_roster(players_created)
        
        # Step 4: Create team using your existing Team class
        nba_team = team.Team(team_name, players_created)
        
        print(f"✅ Successfully created {team_name} with {len(players_created)} players!")
        return nba_team
    
    def _balance_roster(self, players: List[player.Player]) -> List[player.Player]:
        """Ensure roster has reasonable positional balance"""
        print("⚖️  Balancing roster positions...")
        
        # Sort by position
        players.sort(key=lambda x: x.position)
        
        # Count positions
        position_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for p in players:
            position_counts[p.position] += 1
        
        print(f"📊 Position counts: {position_counts}")
        
        # Ensure at least one player per position
        for pos in range(1, 6):
            if position_counts[pos] == 0 and len(players) > 0:
                print(f"⚠️  Missing position {pos} ({player.POSITIONS[pos]}), converting closest player...")
                
                # Find closest position player to convert
                best_candidate = None
                min_distance = float('inf')
                
                for p in players:
                    distance = abs(p.position - pos)
                    if distance < min_distance:
                        min_distance = distance
                        best_candidate = p
                
                if best_candidate:
                    old_pos = best_candidate.position_string
                    best_candidate.position = pos
                    best_candidate.position_string = player.POSITIONS[pos]
                    position_counts[pos] += 1
                    print(f"✅ Converted {best_candidate.name} from {old_pos} to {best_candidate.position_string}")
        
        return players


# Convenience function for easy team creation
def create_nba_teams(team1_name: str, team1_id: int, team2_name: str, team2_id: int):
    """Create two NBA teams for simulation"""
    if not NBA_API_AVAILABLE:
        print("❌ NBA API not available. Please install: pip install nba_api")
        return None, None
    
    manager = NBADataManager()
    
    print("🏀 Creating NBA teams for simulation...")
    print("=" * 60)
    
    team1 = manager.create_nba_team(team1_name, team1_id)
    team2 = manager.create_nba_team(team2_name, team2_id)
    
    if team1 and team2:
        print(f"\n🎉 Successfully created both teams!")
        print(f"✅ {team1.name} ({len(team1.players)} players)")
        print(f"✅ {team2.name} ({len(team2.players)} players)")
        return team1, team2
    else:
        print("❌ Failed to create one or both teams")
        return None, None


if __name__ == "__main__":
    # Test the NBA integration
    print("🧪 Testing NBA integration...")
    
    if NBA_API_AVAILABLE:
        manager = NBADataManager()
        
        teams_list = manager.get_popular_teams()
        print(f"📋 Found {len(teams_list)} popular teams")
        
        # Test creating Lakers (should be first in popular teams)
        if teams_list:
            lakers_name, lakers_id = teams_list[0]
            print(f"\n🧪 Testing with {lakers_name}...")
            test_team = manager.create_nba_team(lakers_name, lakers_id)
            
            if test_team:
                print(f"\n🎉 Test successful! Created {test_team.name}")
                print("👥 Sample players:")
                for p in test_team.players[:5]:
                    overall = (p.shooting['close'] + p.shooting['mid'] + p.shooting['long'] + 
                              p.skills['passing'] + p.defense['rebounding']) // 5
                    print(f"   {p.name} ({p.position_string}) - Overall: {overall}")
            else:
                print("❌ Test failed - could not create team")
    else:
        print("❌ NBA API not available - install nba_api package")
