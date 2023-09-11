from espn_api.football import League
from pprint import pprint
import json
from constant import PRO_TEAM_MAP

league_id = 55432112
year = 2022
# https://cran.r-project.org/web/packages/ffscrapr/vignettes/espn_authentication.html
espn_s2 = "AECMk6QMKaUhotkRDG6z%2Fhgk91pIa42kCh0o64d9xYY0AhXZ3GYiPbYK0UN9l2z3e0yceHQR3wqDILFGSdDlNMsxg7qmJ%2F1l0fRwSwNpz%2FF3rb0zSOioo%2BHKQ%2FRtBJc%2BRLTWjnIMH3vmDFfyvkjyDSs5pAD%2FvpqAf0dOApdcEq3WkHqXqMeRxaD%2Bde%2F4l%2ByfP45wYk5M6R4HlBkMiMlu2%2Fn%2BL17k%2F13X0ly2FTi1kVWBfxal%2B8Mjsfq0jMSdKkOFp2yn%2BJceb9QD9VkIU2aSqgrAQB8aBW%2B1aBjRd8pFnd4zvO0%2BNUeA31E3PPBSsZYUr7U%3D"
swid = "{EE8E2DD1-59A7-4AB4-B36B-7A57A97AF541}"
debug = False

league = League(
    league_id=league_id, year=year, espn_s2=espn_s2, swid=swid, debug=debug
)

for i, opponent in enumerate(league.teams[0].schedule):
    print(f"Week {i+1}: {opponent.team_name}")
