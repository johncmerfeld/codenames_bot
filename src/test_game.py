#! /usr/bin/env python3

import unittest

from game import Game


class TestGame(unittest.TestCase):
    def setUp(self):
        self.client = "test_client"
        self.database = "test_db"
        self.collection = "test_collection"
        self.words_by_team = {
            "red": ["Fair", "Fish", "Dinosaur"],
            "blue": ["Drill", "Hollywood", "Chocolate", "King"],
            "nuetral": ["Ivory", "Shop"],
            "assassin": ["Turkey"],
        }
        self.test_game = Game(
            self.client, self.database, self.collection, self.words_by_team
        )

    def test_get_valid_teams(self):
        self.assertEqual(
            self.test_game.get_valid_teams(), ["red", "blue", "nuetral", "assassin"]
        )

    def test_validate_team(self):
        self.assertTrue(self.test_game.validate_team("red"))

    def test_validate_team_negative(self):
        self.assertRaises(Exception, self.test_game.validate_team, "yellow")


if __name__ == "__main__":
    unittest.main()
