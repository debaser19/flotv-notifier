import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

import config


class Player:
    def __init__(self, name, race, mmr=0):
        self.name = name
        self.race = race
        self.mmr = mmr

class Game:
    def __init__(self, id, players, map, server, start_time, game_url):
        self.id = id
        self.players = players
        self.map = map
        self.server = server
        self.start_time = start_time
        self.game_url = game_url


def parse_race(race):
    races = ['RANDOM', 'HUMAN', 'ORC', 'NIGHT_ELF', 'UNDEAD']
    if race in races:
        match race:
            case 'RANDOM':
                return 0
            case 'HUMAN':
                return 1
            case 'ORC':
                return 2
            case 'NIGHT_ELF':
                return 4
            case 'UNDEAD':
                return 8
    else:
        return 0


def get_flo_games(flo_url):
    driver_path = config.DRIVER_PATH
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get(flo_url)
    time.sleep(3)

    flo_table = driver.find_element(by=By.TAG_NAME, value="tbody")
    flo_rows = flo_table.find_elements(by=By.TAG_NAME, value="tr")

    game_list = []
    limit = 0
    for row in flo_rows:
        limit += 1
        if limit >= 11:
            break
        players = []
        elements = row.find_elements(by=By.TAG_NAME, value="td")
        game_url = row.find_element(by=By.TAG_NAME, value="a").get_attribute("href")
        p0 = elements[1].text.split("\n")[0]
        p1 = elements[1].text.split("\n")[1]
        p0_race = p0.split("[")[1].split("]")[0]
        p1_race = p1.split("[")[1].split("]")[0]
        players.append(
            Player(
                p0.split(" ")[2],
                p0_race,
                0
            )
        )
        players.append(
            Player(
                p1.split(" ")[2],
                p1_race,
                0
            )
        )
        game_list.append(
            Game(
                elements[0].text,
                players,
                elements[2].text,
                elements[3].text,
                elements[4].text,
                game_url
            )
        )
    
    for game in game_list:
        for player in game.players:
            print(f"Fetching mmr for player {player.name}")
            player.mmr = get_mmr(player.name, parse_race(player.race))
    
    return game_list


def get_mmr(user, race):
    season = 11
    while season > 0:
        res = requests.get(config.W3C_URL + user.replace("#", "%23") + f'/game-mode-stats?gateWay=20&season={season}')
        for item in res.json():
            if item['gameMode'] == 1 and item['race'] == int(race):
                return int(item["mmr"])
        season -= 1
    return None


# def main():
#     games = get_flo_games(config.FLO_URL)
#     for game in games:
#         print(f"{game.id} - {game.map} - {game.start_time} - {game.game_url}")
#         for player in game.players:
#             print(f"[{player.race}] {player.name} - {player.mmr}")


# if __name__ == "__main__":
#     main()