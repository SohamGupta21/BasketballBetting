#!/usr/bin/env python3
"""
Setup script for NBA Basketball Simulation
Installs dependencies and tests the NBA API integration
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("🔧 Installing NBA API and dependencies...")
    print("   This may take a minute...")
    
    packages = ['nba_api>=1.1.11', 'requests>=2.31.0', 'pandas>=1.5.0']
    
    for package in packages:
        try:
            package_name = package.split('>=')[0]  # Get just the package name
            print(f"   📦 Installing {package_name}...")
            
            result = subprocess.run([sys.executable, "-m", "pip", "install", package], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"   ✅ {package_name} installed successfully")
            else:
                print(f"   ❌ Failed to install {package_name}")
                print(f"   Error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"   ❌ Exception installing {package}: {e}")
            return False
    
    return True

def test_nba_api():
    """Test NBA API connection and functionality"""
    print("\n🏀 Testing NBA API connection...")
    
    try:
        # Test basic imports
        print("   📚 Testing imports...")
        from nba_api.stats.static import teams
        from nba_api.stats.endpoints import commonteamroster
        print("   ✅ NBA API imports successful")
        
        # Test getting teams
        print("   🏀 Testing team data...")
        all_teams = teams.get_teams()
        
        if all_teams and len(all_teams) > 0:
            print(f"   ✅ Found {len(all_teams)} NBA teams")
            
            # Test getting Lakers roster (team ID 1610612747)
            print("   📋 Testing roster fetch...")
            import time
            time.sleep(1)  # Rate limiting
            
            lakers_roster = commonteamroster.CommonTeamRoster(team_id=1610612747, season='2023-24')
            roster_df = lakers_roster.get_data_frames()[0]
            
            if not roster_df.empty:
                print(f"   ✅ Roster fetch successful! Found {len(roster_df)} Lakers players")
                print(f"   📝 Sample: {roster_df.iloc[0]['PLAYER']}")
                return True
            else:
                print("   ⚠️  Roster fetch returned no data")
                return False
        else:
            print("   ❌ No teams found")
            return False
            
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        print("   💡 Try running: pip install nba_api")
        return False
    except Exception as e:
        print(f"   ❌ API test failed: {e}")
        print("   ℹ️  This might be temporary - the NBA API can be slow or rate-limited")
        print("   ℹ️  You can still try running the simulation")
        return False

def test_simulation_files():
    """Test that simulation files exist and can be imported"""
    print("\n📁 Testing simulation files...")
    
    required_files = ['player.py', 'team.py', 'game.py', 'main.py']
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing required files: {', '.join(missing_files)}")
        print("Please ensure you're running this from the basketball-sim directory")
        return False
    
    # Test importing the modules
    try:
        print("   🔄 Testing imports...")
        import player
        import team
        import game
        print("   ✅ All simulation modules import successfully")
        
        # Test creating a simple player
        test_player = player.Player("Test Player", 1)
        print(f"   ✅ Player creation works: {test_player.name}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        return False

def test_integration():
    """Test the NBA integration module"""
    print("\n🔗 Testing NBA integration...")
    
    try:
        import nba_integration
        print("   ✅ NBA integration module loads")
        
        # Test creating the manager (without API calls)
        if nba_integration.NBA_API_AVAILABLE:
            print("   ✅ NBA API available for integration")
            return True
        else:
            print("   ⚠️  NBA API not available - integration will use fallbacks")
            return False
            
    except Exception as e:
        print(f"   ❌ Integration test failed: {e}")
        return False

def main():
    print("🏀 NBA BASKETBALL SIMULATION SETUP")
    print("="*50)
    print("This script will:")
    print("1. Install required Python packages (nba_api, pandas, requests)")
    print("2. Test NBA API connectivity") 
    print("3. Verify your simulation files")
    print("4. Test the integration")
    print()
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
        print("❌ Python 3.7+ required. You have Python {}.{}".format(python_version.major, python_version.minor))
        return
    else:
        print(f"✅ Python {python_version.major}.{python_version.minor} detected")
    
    # Test simulation files first
    if not test_simulation_files():
        print("\n❌ Setup failed - simulation files missing or broken")
        return
    
    # Install packages
    print(f"\n{'='*50}")
    if not install_requirements():
        print("\n❌ Package installation failed!")
        print("💡 Try manually: pip install nba_api pandas requests")
        return
    
    # Test NBA API
    print(f"\n{'='*50}")
    api_works = test_nba_api()
    
    # Test integration
    print(f"\n{'='*50}")
    integration_works = test_integration()
    
    # Final results
    print(f"\n{'='*50}")
    print("🏁 SETUP COMPLETE!")
    print("="*50)
    
    if api_works and integration_works:
        print("🎉 Everything working perfectly!")
        print("\n🚀 Ready to run:")
        print("   python main_nba.py")
        print("\n💫 Features available:")
        print("   ✅ Real NBA teams and players")
        print("   ✅ Current season statistics (2023-24)")
        print("   ✅ Live shooting percentages converted to simulation")
        print("   ✅ Detailed game simulation with real player abilities")
        print("   ✅ Season simulation")
        print("   ✅ Mixed NBA vs simulated teams")
        
    elif integration_works:
        print("⚠️  Setup completed with warnings!")
        print("NBA API had issues but integration is ready")
        print("\n🚀 You can try running:")
        print("   python main_nba.py")
        print("   python main.py  (original simulation)")
        print("\n💡 NBA API issues are often temporary - try again later")
        
    else:
        print("⚠️  Basic setup completed!")
        print("NBA integration had issues")
        print("\n🚀 You can still run:")
        print("   python main.py  (original simulation)")
        print("\n🔧 To fix NBA integration:")
        print("   1. Check internet connection")
        print("   2. Try: pip install --upgrade nba_api")
        print("   3. Run this setup again")
    
    print(f"\n💡 If you have issues:")
    print("   - NBA API can be slow or rate-limited")
    print("   - Try the 'Quick Demo' option first")
    print("   - Original simulation always works as backup")

if __name__ == "__main__":
    main()
