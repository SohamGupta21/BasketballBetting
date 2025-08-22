"""
Enhanced NBA Basketball Simulation
Uses real NBA data with your existing simulation engine
"""

import player
import team
import game
import random

# Try to import NBA integration
try:
    import nba_integration
    NBA_AVAILABLE = True
    print("🏀 NBA integration loaded successfully!")
except ImportError:
    NBA_AVAILABLE = False
    print("⚠️  NBA integration not available. Install: pip install nba_api")


def main():
    print("\n" + "="*60)
    print("🏀 ENHANCED NBA BASKETBALL SIMULATION")
    print("="*60)
    
    if NBA_AVAILABLE:
        print("Choose your simulation type:")
        print("1. 🏆 Real NBA Teams (Lakers, Warriors, etc.)")
        print("2. 🎮 Original Simulation (Your hardcoded players)")  
        print("3. 🔀 Mixed: NBA Team vs Simulated Team")
        print("4. ⚡ Quick Demo: Lakers vs Warriors")
        choice = input("\nSelect option (1-4): ").strip()
    else:
        print("NBA API not available - running original simulation")
        choice = "2"
    
    print("\n" + "-"*60)
    
    if choice == "1":
        run_full_nba_simulation()
    elif choice == "2":
        run_original_simulation()
    elif choice == "3":
        run_mixed_simulation()
    elif choice == "4":
        run_quick_demo()
    else:
        print("Invalid choice, running original simulation...")
        run_original_simulation()


def run_full_nba_simulation():
    """Full NBA teams simulation with team selection"""
    print("🏀 REAL NBA TEAMS SIMULATION")
    print("="*40)
    
    if not NBA_AVAILABLE:
        print("❌ NBA integration not available!")
        return
    
    try:
        # Create the NBA data manager
        manager = nba_integration.NBADataManager()
        
        # Get available teams
        print("📋 Loading NBA teams...")
        teams_list = manager.get_popular_teams()
        
        print("\n🏀 Available NBA Teams:")
        print("-" * 30)
        for i, (name, team_id) in enumerate(teams_list, 1):
            print(f"{i:2d}. {name}")
        
        # Get team selections from user
        print(f"\nSelect two teams to compete:")
        team1_choice = int(input(f"Team 1 (1-{len(teams_list)}): ")) - 1
        team2_choice = int(input(f"Team 2 (1-{len(teams_list)}): ")) - 1
        
        if not (0 <= team1_choice < len(teams_list) and 0 <= team2_choice < len(teams_list)):
            print("❌ Invalid team selection!")
            return
        
        team1_name, team1_id = teams_list[team1_choice]
        team2_name, team2_id = teams_list[team2_choice]
        
        print(f"\n🆚 MATCHUP: {team1_name} vs {team2_name}")
        print("⏳ Creating teams with real NBA data...")
        print("   (This may take 30-60 seconds due to API calls)")
        
        # Create teams with real NBA data - this is where the magic happens!
        team1, team2 = nba_integration.create_nba_teams(team1_name, team1_id, team2_name, team2_id)
        
        if team1 and team2:
            print("\n🎉 Teams created successfully!")
            show_team_rosters(team1, team2)
            run_simulation_menu(team1, team2)
        else:
            print("❌ Failed to create teams. Please try again.")
            
    except ValueError:
        print("❌ Invalid input! Please enter numbers only.")
    except KeyboardInterrupt:
        print("\n⏹️ Simulation cancelled.")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Try the quick demo or original simulation if NBA API is having issues.")


def run_quick_demo():
    """Quick demo with Lakers vs Warriors"""
    print("⚡ QUICK DEMO: Lakers vs Warriors")
    print("="*40)
    
    if not NBA_AVAILABLE:
        print("❌ NBA integration not available!")
        return
    
    print("🚀 Loading Lakers and Warriors with real NBA data...")
    print("⏳ This will take about 30 seconds...")
    
    try:
        # Lakers ID: 1610612747, Warriors ID: 1610612744 (these are the official NBA team IDs)
        team1, team2 = nba_integration.create_nba_teams(
            "Los Angeles Lakers", 1610612747,
            "Golden State Warriors", 1610612744
        )
        
        if team1 and team2:
            print(f"\n🎉 Demo teams ready!")
            print(f"🏀 {team1.name} roster loaded with real stats")
            print(f"🏀 {team2.name} roster loaded with real stats")
            
            # Show a few key players
            print(f"\n⭐ {team1.name} stars:")
            for p in team1.players[:3]:
                overall = get_player_overall_rating(p)
                print(f"   {p.name} ({p.position_string}) - Overall: {overall}")
            
            print(f"\n⭐ {team2.name} stars:")
            for p in team2.players[:3]:
                overall = get_player_overall_rating(p)
                print(f"   {p.name} ({p.position_string}) - Overall: {overall}")
            
            print(f"\n🎮 Running quick simulation...")
            sim_single_game(team1, team2, pbp=False)
        else:
            print("❌ Failed to create demo teams")
            
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("💡 Try the original simulation if NBA API is having issues.")


def run_mixed_simulation():
    """NBA team vs simulated team"""
    print("🔀 MIXED SIMULATION: NBA vs Simulated")
    print("="*40)
    
    if not NBA_AVAILABLE:
        print("❌ NBA integration not available!")
        return
    
    try:
        manager = nba_integration.NBADataManager()
        
        print("📋 Select an NBA team to face the Simulation All-Stars:")
        teams_list = manager.get_popular_teams()
        
        for i, (name, team_id) in enumerate(teams_list, 1):
            print(f"{i:2d}. {name}")
        
        team_choice = int(input(f"\nSelect NBA team (1-{len(teams_list)}): ")) - 1
        
        if not (0 <= team_choice < len(teams_list)):
            print("❌ Invalid selection!")
            return
        
        team_name, team_id = teams_list[team_choice]
        
        print(f"⏳ Creating {team_name} with real NBA data...")
        nba_team = nba_integration.NBADataManager().create_nba_team(team_name, team_id)
        
        if nba_team:
            # Create a strong simulated team to compete
            print("🎮 Creating Simulation All-Stars...")
            sim_team = create_simulation_team()
            
            print(f"\n🆚 MATCHUP: {nba_team.name} vs {sim_team.name}")
            show_team_rosters(nba_team, sim_team)
            run_simulation_menu(nba_team, sim_team)
        else:
            print("❌ Failed to create NBA team")
            
    except ValueError:
        print("❌ Invalid input!")
    except Exception as e:
        print(f"❌ Error: {e}")


def create_simulation_team() -> team.Team:
    """Create a strong simulated team to compete with NBA teams"""
    sim_names = [
        'Alex "The Shooter" Johnson', 'Mike "Lightning" Davis', 'Chris "The Wall" Wilson', 
        'David "Hammer" Brown', 'Robert "The Tower" Taylor', 'James "Flash" Anderson', 
        'Michael "Sniper" Miller', 'William "The Rock" Moore', 'Richard "Speed" Jackson', 
        'Joseph "Giant" White', 'Daniel "Clutch" Harris', 'Matthew "The Force" Martin'
    ]
    
    sim_players = []
    for i, name in enumerate(sim_names):
        pos = (i % 5) + 1  # Cycle through positions 1-5
        # Create strong players (75-95 range) to compete with NBA stars
        sim_players.append(player.Player(name, pos, floor=75, ceiling=95))
    
    return team.Team("Simulation All-Stars", sim_players)


def run_original_simulation():
    """Run the original hardcoded simulation"""
    print("🎮 ORIGINAL BASKETBALL SIMULATION")
    print("="*40)
    print("Using your original hardcoded players...")
    
    # Your original players from main.py
    raptors_players = [
        player.Player('Kyle Lowry', 1, floor=70, ceiling=80),
        player.Player('DeMar DeRozan', 2, floor=70, ceiling=80),
        player.Player('James Johnson', 3, floor=70, ceiling=80),
        player.Player('Amir Johnson', 4, floor=70, ceiling=80),
        player.Player('Jonas Valanciunas', 5, floor=70, ceiling=80),
        player.Player('Lou Williams', 1, floor=70, ceiling=80),
        player.Player('Terrence Ross', 2, floor=70, ceiling=80),
        player.Player('Bruno Caboclo', 3, floor=70, ceiling=80),
        player.Player('Patrick Patterson', 4, floor=70, ceiling=80),
        player.Player('Chuck Hayes', 5, floor=70, ceiling=80)
    ]
    
    sabres_players = [
        player.Player('Sam Baskerville', 1, floor=70, ceiling=80),
        player.Player('Brendan Tracey', 2, floor=70, ceiling=80),
        player.Player('Connor Petterson', 3, floor=70, ceiling=80),
        player.Player('Dan Fettes', 4, floor=90, ceiling=100),  # Your star player!
        player.Player('Rick Nydam', 5, floor=70, ceiling=80),
        player.Player('James Tran', 1, floor=70, ceiling=80),
        player.Player('Brett Mitchell', 2, floor=70, ceiling=80),
        player.Player('David Teichrobe', 3, floor=70, ceiling=80),
        player.Player('Mike North', 4, floor=70, ceiling=80),
        player.Player('Logan Earnst', 5, floor=70, ceiling=80)
    ]

    team1 = team.Team('Toronto Raptors', raptors_players)
    team2 = team.Team('Simcoe Sabres', sabres_players)
    
    print(f"\n🆚 MATCHUP: {team1.name} vs {team2.name}")
    run_simulation_menu(team1, team2)


def show_team_rosters(team1: team.Team, team2: team.Team):
    """Display team rosters with overall ratings"""
    print(f"\n📋 TEAM ROSTERS")
    print("="*50)
    
    print(f"\n🏀 {team1.name}:")
    for i, p in enumerate(team1.players[:10], 1):  # Show top 10 players
        rating = get_player_overall_rating(p)
        # Show key attributes to see the NBA data conversion
        print(f"  {i:2d}. {p.name:<25} ({p.position_string}) - OVR:{rating:2d} "
              f"| Shoot:{p.shooting['close']:2d}/{p.shooting['long']:2d} "
              f"| Pass:{p.skills['passing']:2d} | Reb:{p.defense['rebounding']:2d}")
    
    print(f"\n🏀 {team2.name}:")
    for i, p in enumerate(team2.players[:10], 1):
        rating = get_player_overall_rating(p)
        print(f"  {i:2d}. {p.name:<25} ({p.position_string}) - OVR:{rating:2d} "
              f"| Shoot:{p.shooting['close']:2d}/{p.shooting['long']:2d} "
              f"| Pass:{p.skills['passing']:2d} | Reb:{p.defense['rebounding']:2d}")


def get_player_overall_rating(p: player.Player) -> int:
    """Calculate a simple overall rating (0-100) for a player"""
    shooting_avg = (p.shooting['close'] + p.shooting['mid'] + p.shooting['long'] + p.shooting['ft']) / 4
    driving_avg = (p.driving['layups'] + p.driving['dunking']) / 2
    skills_avg = (p.skills['speed'] + p.skills['dribbling'] + p.skills['passing'] + p.skills['stamina']) / 4
    defense_avg = (p.defense['rebounding'] + p.defense['defense'] + p.defense['blocking'] + p.defense['stealing']) / 4
    
    overall = (shooting_avg + driving_avg + skills_avg + defense_avg) / 4
    return int(overall)


def run_simulation_menu(team1: team.Team, team2: team.Team):
    """Show simulation options menu"""
    print(f"\n🎮 SIMULATION OPTIONS")
    print("="*30)
    print("1. 📺 Single Game with Play-by-Play Commentary")
    print("2. 📊 Single Game (Box Score Only)")
    print("3. 🏆 Season Simulation (Multiple Games)")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        print("\n📺 Starting game with full commentary...")
        sim_single_game(team1, team2, pbp=True)
    elif choice == "2":
        print("\n📊 Running quick simulation...")
        sim_single_game(team1, team2, pbp=False)
    elif choice == "3":
        games = input("Number of games to simulate (1-82, default 10): ").strip()
        try:
            games = int(games) if games else 10
            games = max(1, min(82, games))
            print(f"\n🏆 Simulating {games} game season...")
            sim_season(team1, team2, games)
        except ValueError:
            print("Invalid input, simulating 10 games...")
            sim_season(team1, team2, 10)
    else:
        print("Invalid choice, running single game...")
        sim_single_game(team1, team2, pbp=False)


def sim_single_game(team1: team.Team, team2: team.Team, pbp: bool = False):
    """Simulate a single game using your existing game engine"""
    print(f"\n🏀 {'LIVE GAME SIMULATION' if pbp else 'GAME SIMULATION'}")
    print("="*60)
    
    # This uses your existing game.py simulation engine!
    quarters_played = game.game(team1, team2, pbp)
    
    # Display results
    print_game_results(team1, team2, quarters_played)


def sim_season(team1: team.Team, team2: team.Team, games: int = 10):
    """Simulate multiple games"""
    print(f"\n🏆 SEASON SIMULATION ({games} games)")
    print("="*60)
    
    # Reset season stats
    for t in [team1, team2]:
        t.wins = 0
        t.losses = 0
        t.season_points = 0
        for p in t.players:
            reset_player_stats(p)
    
    # Simulate games
    print("⏳ Simulating games", end="")
    for i in range(games):
        if i % 5 == 0:
            print(".", end="", flush=True)
        
        # Reset game-specific stats
        for t in [team1, team2]:
            for p in t.players:
                reset_game_stats(p)
        
        # Use your existing game engine
        game.game(team1, team2, pbp=False)
        
        # Update games played
        for t in [team1, team2]:
            for p in t.players:
                p.games += 1
    
    print(" Done!")
    print_season_results(team1, team2, games)


def reset_player_stats(p: player.Player):
    """Reset all player statistics for season simulation"""
    p.games = 0
    p.fga = p.fg2a = p.fg3a = p.fta = 0
    p.fgm = p.fg2m = p.fg3m = p.ftm = 0
    p.points = p.assists = p.rebounds = 0
    p.def_rebounds = p.off_rebounds = 0
    p.turnovers = p.steals = p.blocks = p.passes = 0
    p.time_played = player.timedelta(0)


def reset_game_stats(p: player.Player):
    """Reset game-specific stats while keeping season totals"""
    # The game simulation automatically handles this
    pass


def print_game_results(team1: team.Team, team2: team.Team, quarters_played: int):
    """Print game results and box scores"""
    print(f"\n📊 GAME RESULTS")
    print("="*80)
    
    # Team box scores
    for team in [team1, team2]:
        print(f'\n🏀 {team.name}')
        print('|        Name        |Pts|  FG  | 3PT | AST | TO  | STL | BLK | REB |OREB| MINS |')
        print('-'*86)
        
        for p in team.players:
            if p.time_played.total_seconds() > 0:  # Only show players who played
                p.fga = p.fg2a + p.fg3a
                p.fgm = p.fg2m + p.fg3m
                fg_string = f'{p.fgm}/{p.fga}'
                fg3_string = f'{p.fg3m}/{p.fg3a}'
                time_str = str(p.time_played).split('.')[0]
                
                print(f'|{p.name:<20}|{p.points:3d}|{fg_string:6}|{fg3_string:5}|{p.assists:5}|'
                      f'{p.turnovers:5}|{p.steals:5}|{p.blocks:5}|{p.rebounds:5}|{p.off_rebounds:4}|{time_str:6}|')

    # Final score
    print(f'\n🏆 FINAL SCORE {"" if quarters_played == 4 else f"({quarters_played-4}OT)"}')
    print("="*30)
    print(f'🏀 {team1.name}: {team1.points}')
    print(f'🏀 {team2.name}: {team2.points}')
    
    # Winner
    winner = team1 if team1.points > team2.points else team2
    margin = abs(team1.points - team2.points)
    print(f'🎉 WINNER: {winner.name} by {margin} points!')


def print_season_results(team1: team.Team, team2: team.Team, games: int):
    """Print season statistics"""
    print(f'\n📈 SEASON STATISTICS ({games} games)')
    print('='*90)
    
    for team in [team1, team2]:
        print(f'\n🏀 {team.name}')
        print('|        Name        | PPG | APG | RPG | FG% |3PT%| SPG | BPG | MPG  |')
        print('-'*70)
        
        for p in team.players:
            if p.games > 0:
                p.fga = p.fg2a + p.fg3a
                p.fgm = p.fg2m + p.fg3m
                
                ppg = p.points / p.games
                apg = p.assists / p.games
                rpg = p.rebounds / p.games
                fg_pct = (p.fgm / p.fga * 100) if p.fga > 0 else 0
                fg3_pct = (p.fg3m / p.fg3a * 100) if p.fg3a > 0 else 0
                spg = p.steals / p.games
                bpg = p.blocks / p.games
                
                avg_seconds = p.time_played.total_seconds() / p.games
                minutes = int(avg_seconds // 60)
                seconds = int(avg_seconds % 60)
                mpg = f"{minutes}:{seconds:02d}"
                
                print(f'|{p.name:<20}|{ppg:5.1f}|{apg:5.1f}|{rpg:5.1f}|{fg_pct:4.1f}|'
                      f'{fg3_pct:4.1f}|{spg:5.1f}|{bpg:5.1f}|{mpg:6}|')
    
    # Team records
    print(f'\n🏆 FINAL STANDINGS')
    print("="*40)
    t1_ppg = team1.season_points / games
    t2_ppg = team2.season_points / games
    
    # Determine season winner
    if team1.wins > team2.wins:
        print(f'🥇 {team1.name}: {team1.wins}-{team1.losses} ({t1_ppg:.1f} PPG) - SEASON CHAMPION!')
        print(f'🥈 {team2.name}: {team2.wins}-{team2.losses} ({t2_ppg:.1f} PPG)')
    elif team2.wins > team1.wins:
        print(f'🥇 {team2.name}: {team2.wins}-{team2.losses} ({t2_ppg:.1f} PPG) - SEASON CHAMPION!')
        print(f'🥈 {team1.name}: {team1.wins}-{team1.losses} ({t1_ppg:.1f} PPG)')
    else:
        print(f'🤝 TIE! Both teams: {team1.wins}-{team1.losses}')
        print(f'   {team1.name}: {t1_ppg:.1f} PPG')
        print(f'   {team2.name}: {t2_ppg:.1f} PPG')


if __name__ == '__main__':
    main()
