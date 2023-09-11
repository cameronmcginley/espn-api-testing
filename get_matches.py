from espn_api.football import League
from pprint import pprint
import json
from constant import PRO_TEAM_MAP
from utils import get_match_id

# import espn_api.football as ff

league_id = 55432112
year = 2020
# https://cran.r-project.org/web/packages/ffscrapr/vignettes/espn_authentication.html
espn_s2 = "AECMk6QMKaUhotkRDG6z%2Fhgk91pIa42kCh0o64d9xYY0AhXZ3GYiPbYK0UN9l2z3e0yceHQR3wqDILFGSdDlNMsxg7qmJ%2F1l0fRwSwNpz%2FF3rb0zSOioo%2BHKQ%2FRtBJc%2BRLTWjnIMH3vmDFfyvkjyDSs5pAD%2FvpqAf0dOApdcEq3WkHqXqMeRxaD%2Bde%2F4l%2ByfP45wYk5M6R4HlBkMiMlu2%2Fn%2BL17k%2F13X0ly2FTi1kVWBfxal%2B8Mjsfq0jMSdKkOFp2yn%2BJceb9QD9VkIU2aSqgrAQB8aBW%2B1aBjRd8pFnd4zvO0%2BNUeA31E3PPBSsZYUr7U%3D"
swid = "{EE8E2DD1-59A7-4AB4-B36B-7A57A97AF541}"
debug = False

league = League(
    league_id=league_id, year=year, espn_s2=espn_s2, swid=swid, debug=debug
)

matches = {}
reg_curr_week = 1
playoff_curr_week = 1

# Get length of season
schedule_lens = [len(team.schedule) for team in league.teams]
season_len = max(schedule_lens)

# https://github.com/cwendt94/espn-api/wiki/Box-Score-Class
for sched_idx in range(0, season_len):
    week_pro_schedule = league._get_pro_schedule(sched_idx)

    # Check if this is a playoff week, arbitrary match
    playoff_week = league.box_scores(week=sched_idx)[0].is_playoff

    # Track week, ignore playoffs
    # It appears champ game is always at index 0
    # Then rest of playoffs are at end of schedule
    # So give the champ games a high num for sorting
    if playoff_week and sched_idx == 0:
        week = 100
    elif playoff_week:
        week = playoff_curr_week
        playoff_curr_week += 1
    else:
        week = reg_curr_week
        reg_curr_week += 1

    for match in league.box_scores(week=sched_idx):
        # Create unique match id
        # match_id = f"{year}-{week:02d}_{match.home_team.team_id}-{match.away_team.team_id}"\
        match_id = get_match_id(
            year, week, match.home_team.team_id, match.away_team.team_id
        )

        # For playoffs, week could make non unique
        if playoff_week:
            match_id += "_playoff"

        # Get winner
        winner = None
        if match.home_score > match.away_score:
            winner = match.home_team.team_id
        else:
            winner = match.away_team.team_id

        home_lineup = []
        away_lineup = []

        for res, data in [
            (home_lineup, match.home_lineup),
            (away_lineup, match.away_lineup),
        ]:
            for player in data:
                stats = {}
                try:
                    stats = player.stats[sched_idx]["breakdown"]
                except KeyError:
                    # print(f"No stats for {player.name}")
                    pass

                if stats != {}:
                    # Remove keys if they eval to int
                    for key in list(stats.keys()):
                        if key.isnumeric():
                            del stats[key]

                # Team player is on is not tracked in Box Player, only
                # their current team in Player. Instead fetch it
                # Get their opponent team's ID
                opp_team_abbrev = player.pro_opponent
                opp_team_id = [
                    id
                    for id in PRO_TEAM_MAP
                    if PRO_TEAM_MAP[id] == opp_team_abbrev
                ][0]
                # Use opp id to get for team's ID
                try:
                    for_team_id = week_pro_schedule[opp_team_id][0]
                    for_team_abbrev = PRO_TEAM_MAP[for_team_id]
                except KeyError:
                    for_team_id = 0
                    for_team_abbrev = ""

                res.append(
                    {
                        # From Player and Box Player class
                        "name": player.name,
                        "player_id": player.playerId,
                        "position": player.position,
                        "slot_position": player.slot_position,
                        "for_team_id": for_team_id,
                        "for_team_abbrev": for_team_abbrev,
                        # Stats
                        "points": player.points,
                        "projected_points": player.projected_points,
                        "stats": stats,
                        "pro_opponent_id": opp_team_id,
                        "pro_opponent_abbrev": player.pro_opponent,
                        "pro_pos_rank": player.pro_pos_rank,
                        "game_played": player.game_played,
                        "on_bye_week": player.on_bye_week,
                    }
                )

        document_id = f"{league_id}-{match_id}"
        matches[document_id] = {
            "league_id": league_id,
            "year": year,
            "week": week,
            "match_id": match_id,
            "winning_team_id": winner,
            "home_team_id": match.home_team.team_id,
            "home_score": match.home_score,
            "home_projected": match.home_projected,
            "away_team_id": match.away_team.team_id,
            "away_score": match.away_score,
            "away_projected": match.away_projected,
            "home_lineup": home_lineup,
            "away_lineup": away_lineup,
            "is_playoff": match.is_playoff,
            "matchup_type": match.matchup_type,
        }

with open("matches.json", "w") as f:
    f.write(json.dumps(matches, indent=2))
