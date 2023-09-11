from espn_api.football import League
from pprint import pprint
import json
from constant import PRO_TEAM_MAP
import datetime
from utils import get_match_id

# import espn_api.football as ff

league_id = 55432112
# https://cran.r-project.org/web/packages/ffscrapr/vignettes/espn_authentication.html
espn_s2 = "AECMk6QMKaUhotkRDG6z%2Fhgk91pIa42kCh0o64d9xYY0AhXZ3GYiPbYK0UN9l2z3e0yceHQR3wqDILFGSdDlNMsxg7qmJ%2F1l0fRwSwNpz%2FF3rb0zSOioo%2BHKQ%2FRtBJc%2BRLTWjnIMH3vmDFfyvkjyDSs5pAD%2FvpqAf0dOApdcEq3WkHqXqMeRxaD%2Bde%2F4l%2ByfP45wYk5M6R4HlBkMiMlu2%2Fn%2BL17k%2F13X0ly2FTi1kVWBfxal%2B8Mjsfq0jMSdKkOFp2yn%2BJceb9QD9VkIU2aSqgrAQB8aBW%2B1aBjRd8pFnd4zvO0%2BNUeA31E3PPBSsZYUr7U%3D"
swid = "{EE8E2DD1-59A7-4AB4-B36B-7A57A97AF541}"
debug = False

curr_year = datetime.datetime.now().year
all_years = []
# Iterate current year down to 2000
for year in range(curr_year, 1999, -1):
    try:
        league = League(
            league_id=league_id,
            year=year,
            espn_s2=espn_s2,
            swid=swid,
            debug=debug,
        )
        all_years.append(year)
    except:
        continue

print(all_years)

leagues = {}

res = {
    "league_id": league_id,
    "years": all_years,
    "commissioner": None,
}

for year in all_years:
    league = League(
        league_id=league_id,
        year=year,
        espn_s2=espn_s2,
        swid=swid,
        debug=debug,
    )

    # Get Teams
    teams = [team.team_id for team in league.teams]
    res[year] = {}
    res[year]["teams"] = teams

    # Get Draft
    draft = league.draft
    draft_picks = [
        {
            "team_id": pick.team.team_id,
            "player_id": pick.playerId,
            "player_name": pick.playerName,
            "round_num": pick.round_num,
            "round_pick": pick.round_pick,
        }
        for pick in draft
    ]
    res[year]["draft"] = draft_picks

    # Get Standings
    standings = [team.team_id for team in league.standings()]
    res[year]["standings"] = standings

    # Get season length
    schedule_lens = [len(team.schedule) for team in league.teams]
    reg_season_len = max(schedule_lens)
    res[year]["reg_season_num_weeks"] = reg_season_len

    # No need to store schedule
    # Get from matches with league_id, year, then build and display

document_id = f"{league_id}"
leagues[document_id] = res

# Print json to leagues.json
with open("leagues.json", "w") as f:
    json.dump(leagues, f, indent=4)
