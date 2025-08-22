# 🏀 Enhanced NBA Basketball Simulation

Your basketball simulation now supports **real NBA data**! This integration fetches current NBA team rosters, player statistics, and converts real shooting percentages into your simulation attributes.

## 🚀 Quick Start

1. **Install NBA API and dependencies:**
   ```bash
   python setup_nba.py
   ```

2. **Run the enhanced simulation:**
   ```bash
   python main_nba.py
   ```

3. **Choose your simulation type:**
   - 🏆 **Real NBA Teams** - Lakers vs Warriors with real stats
   - 🎮 **Original Simulation** - Your hardcoded players
   - 🔀 **Mixed** - NBA team vs simulated team
   - ⚡ **Quick Demo** - Instant Lakers vs Warriors

## 🔧 How It Works

### NBA Data → Simulation Conversion

**Real NBA Stats** → **Your Simulation Attributes**

```python
# Example: Stephen Curry's real stats
NBA Stats:
- FG%: 40.7%     → Close/Mid Shooting: 82/85
- 3P%: 40.3%     → Long Range: 81  
- FT%: 91.5%     → Free Throws: 100
- APG: 5.1       → Passing: 77
- PPG: 26.4      → Scoring boost applied

# Example: Giannis Antetokounmpo's real stats  
NBA Stats:
- FG%: 61.1%     → Close/Mid Shooting: 100/91
- 3P%: 27.4%     → Long Range: 55
- RPG: 11.5      → Rebounding: 100
- BPG: 1.1       → Blocking: 66
```

### 📊 API Endpoints Used

1. **`teams.get_teams()`** - Get all NBA teams
2. **`commonteamroster`** - Get team rosters (who's on each team)
3. **`playerdashboardbyyearoveryear`** - **KEY ENDPOINT** for player stats:
   - Shooting percentages (FG%, 3P%, FT%)
   - Points, assists, rebounds per game
   - Steals, blocks, turnovers
   - Minutes played

### 🎯 Position-Based Scaling

Different positions get different attribute scaling:

- **Point Guards (PG)**: Passing multiplier x15, speed boost
- **Centers (C)**: Rebounding multiplier x18, blocking boost  
- **Shooting Guards (SG)**: Shooting focus, athleticism
- **Forwards (SF/PF)**: Balanced with size advantages

## 🏀 Available Teams

Popular teams you can select:
- Los Angeles Lakers
- Golden State Warriors  
- Boston Celtics
- Miami Heat
- Chicago Bulls
- New York Knicks
- And 10+ more!

## 🎮 Game Features

Everything from your original simulation works:
- ✅ **Detailed play-by-play** - "LeBron James made inside shot"
- ✅ **Realistic game flow** - Quarters, overtime, substitutions
- ✅ **Player fatigue** - Starters get tired, bench players rest
- ✅ **Season simulation** - Multiple games with stats tracking
- ✅ **Box scores** - Points, rebounds, assists, shooting percentages

**NEW:** Now with real NBA player abilities!

## 📁 Files Created

- `nba_integration.py` - Core NBA API integration
- `main_nba.py` - Enhanced main program with NBA options
- `setup_nba.py` - Installation and testing script
- `requirements.txt` - Python package dependencies

## 🔍 Example Output

```
🏀 Creating player: LeBron James
📊 Got stats: 25.7 PPG, 54.0% FG%, 41.0% 3P%
🎯 Shooting skills: Close=100, Mid=91, Long=82, FT=75
✅ Created LeBron James (SF)

🆚 MATCHUP: Los Angeles Lakers vs Golden State Warriors
Lakers: LeBron James (SF) - OVR:94 | Shoot:100/82 | Pass:89 | Reb:88
Lakers: Anthony Davis (PF) - OVR:91 | Shoot:89/45 | Pass:52 | Reb:95
Warriors: Stephen Curry (PG) - OVR:89 | Shoot:82/81 | Pass:77 | Reb:35
```

## 🛠️ Troubleshooting

**"NBA API not available"**
- Run: `pip install nba_api pandas requests`
- Check internet connection
- Try the Quick Demo first

**"Could not fetch roster"**  
- NBA API can be slow or rate-limited
- Wait a minute and try again
- Use original simulation as backup

**Slow performance**
- Initial team creation takes 30-60 seconds (fetching 24+ players)
- After creation, games run at normal speed
- Consider using cached teams for repeated runs

## 🎯 What Makes This Special

1. **Real Data**: Actual NBA shooting percentages, not random numbers
2. **Smart Conversion**: A 45% NBA shooter becomes appropriately skilled in your sim
3. **Position Awareness**: Point guards get passing boosts, centers get rebounding boosts
4. **Performance Scaling**: High scorers get attribute bonuses
5. **Fallback System**: If API fails, uses intelligent position-based defaults

Your simulation engine is unchanged - it just now gets fed real NBA player abilities instead of random ones!

## 🏆 Try It Out

```bash
# Install everything
python setup_nba.py

# Run simulation  
python main_nba.py

# Quick test
# Select "4" for Lakers vs Warriors demo
```

Enjoy your enhanced NBA simulation! 🏀
