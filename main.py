from dataclasses import dataclass, field
from src.scores import Match, Record, Team, TeamMatchGoals, Tournament


def main():
    mat = Match.fromString("onion 3, carrot 7")
    city = Team("manchester city", Record(6, 2, 1))
    chelsea = Team("chelsea fc", Record(7, 1, 1))
    arsenal = Team("arsenal", Record(4, 2, 3))

    path = "data/sample-input.txt"
    epl = Tournament(path)
    print(epl)

    manutd = TeamMatchGoals('manutd', 3)
    lpool = TeamMatchGoals('lpool', 3)
    print(manutd <= lpool)


if __name__ == "__main__":
    main()
