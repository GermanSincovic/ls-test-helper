import os

MAINTENANCE = False

BASE_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MAIN_REPOSITORY_PATH = os.path.join(BASE_FOLDER, "files")

RESULTS_DIR = os.path.join(MAIN_REPOSITORY_PATH, "results")

ARCHIVE_DIR = os.path.join(MAIN_REPOSITORY_PATH, "archive")

UPLOAD_DIR = os.path.join(MAIN_REPOSITORY_PATH, 'uploaded')

MODULES_DIR = os.path.join(BASE_FOLDER, "modules")

UI_DIR = os.path.join(BASE_FOLDER, 'ui')

LOGS_DIR = os.path.join(BASE_FOLDER, 'logs')

FEATURE_NAMES = {"1": "venue",
                 "2": "goal scorers",
                 "3": "goal assists",
                 "4": "cards",
                 "5": "head to head",
                 "6": "spectators",
                 "7": "incidents",
                 "8": "line-ups",
                 "9": "commentaries",
                 "10": "referee",
                 "11": "league table",
                 "12": "stats",
                 "13": "odds",
                 "14": "live tracker",
                 "16": "basic info",
                 "17": "team bage"}

SPORT_NAMES = {"1": "soccer",
               "5": 'hockey',
               "23": 'basketball',
               "2": 'tennis',
               "73": 'cricket',
               "31": 'horses'}

PROVIDER_NAMES = {"8": 'LiveScore',
                  "1": 'Enet',
                  "6": 'SportRadar',
                  "11": 'Opta',
                  "12": 'SportsBook',
                  "14": 'BetMakers',
                  "15": 'StreamAMG',
                  "3": 'Testing'}

