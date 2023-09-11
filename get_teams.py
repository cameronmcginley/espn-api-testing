from espn_api.football import League
from pprint import pprint
import json
from constant import PRO_TEAM_MAP
from utils import get_match_id
import datetime

# import espn_api.football as ff

imported = [{}, {}]

league_id = 55432112
# https://cran.r-project.org/web/packages/ffscrapr/vignettes/espn_authentication.html
espn_s2 = "AECMk6QMKaUhotkRDG6z%2Fhgk91pIa42kCh0o64d9xYY0AhXZ3GYiPbYK0UN9l2z3e0yceHQR3wqDILFGSdDlNMsxg7qmJ%2F1l0fRwSwNpz%2FF3rb0zSOioo%2BHKQ%2FRtBJc%2BRLTWjnIMH3vmDFfyvkjyDSs5pAD%2FvpqAf0dOApdcEq3WkHqXqMeRxaD%2Bde%2F4l%2ByfP45wYk5M6R4HlBkMiMlu2%2Fn%2BL17k%2F13X0ly2FTi1kVWBfxal%2B8Mjsfq0jMSdKkOFp2yn%2BJceb9QD9VkIU2aSqgrAQB8aBW%2B1aBjRd8pFnd4zvO0%2BNUeA31E3PPBSsZYUr7U%3D"
swid = "{EE8E2DD1-59A7-4AB4-B36B-7A57A97AF541}"
debug = False

curr_year = datetime.datetime.now().year
all_years = []
# Iterate up from 2000 to current year (so we overwrite with new)
for year in range(2000, curr_year + 1):
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

res = {}
for year in all_years:
    league = League(
        league_id=league_id,
        year=year,
        espn_s2=espn_s2,
        swid=swid,
        debug=debug,
    )

    for team in league.teams:
        document_id = f"{league_id}-{team.team_id}"

        team_data = {
            "league_id": league_id,
            "team_id": team.team_id,
            "team_name": team.team_name,
            "team_abbrev": team.team_abbrev,
            "owner": team.owner,
            "years": {},
        }

        roster = [
            {
                "player_id": player.playerId,
                "name": player.name,
                "position": player.position,
                "posRank": player.posRank,
                "proTeam": player.proTeam,
            }
            for player in team.roster
        ]
        year_data = {
            "wins": team.wins,
            "losses": team.losses,
            "ties": team.ties,
            "points_for": round(team.points_for, 2),
            "points_against": round(team.points_against, 2),
            "acquisitions": team.acquisitions,
            "trades": team.trades,
            "drops": team.drops,
            "standing": team.standing,
            "draft_projected_rank": team.draft_projected_rank,
            "playoff_pct": round(team.playoff_pct, 2),
            "roster": roster,
        }

        if document_id not in res:
            res[document_id] = team_data
        res[document_id]["years"][str(year)] = year_data


with open("teams.json", "w") as f:
    f.write(json.dumps(res, indent=2))

import firebase_admin
from firebase_admin import firestore

# Application Default credentials are automatically created.
# app = firebase_admin.initialize_app()
# db = firestore.client()

app_options = {"projectId": "mcginley-football-league"}
default_app = firebase_admin.initialize_app(options=app_options)
db = firestore.client()

for document_id in res:
    db.collection("teams").document(document_id).set(res[document_id])
