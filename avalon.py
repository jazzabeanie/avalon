import logging
import random
import os

logger = logging.getLogger('avalon')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('avalon.log')
file_handler.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.debug("======")

def clear_console():
    os.system('clear')

class Session:
    def __init__(self):
        logger.info("Welcome to Avalon.")
        self.players = self._get_player_names()
        self.confirm_players()
        self.characters = self._get_characters()
        self.confirm_special_characters()
        self.roles = self.assign_characters()
        logger.info("You are now ready to be assigned characters")
        input("Press enter to continue")
        clear_console()
        self.communicate_characters()
        logger.info(f"You are now ready to play.")
        self.determine_who_starts()

    def _get_characters(self):
        if self.number_of_players == 5:
            return ['good', 'good', 'good', 'evil', 'evil']
        if self.number_of_players == 6:
            return ['good', 'good', 'good', 'good', 'evil', 'evil']
        if self.number_of_players == 7:
            return ['good', 'good', 'good', 'good', 'evil', 'evil', 'evil']
        if self.number_of_players == 8:
            return ['good', 'good', 'good', 'good', 'good', 'evil', 'evil', 'evil']
        if self.number_of_players == 9:
            return ['good', 'good', 'good', 'good', 'good', 'evil', 'evil', 'evil', 'evil']
        if self.number_of_players == 9:
            return ['good', 'good', 'good', 'good', 'good', 'good', 'evil', 'evil', 'evil', 'evil']

    def _get_player_names(self):
        logger.info("Each player must enter their name. This game can take 5-10 players. Enter 'END' if all players have been entered")
        player_names = []
        def get_name():
            name = None
            if len(player_names) == 10:
                logger.info("You now have 10 players. The game will now start.")
                return player_names
            name = input("What's your name? ")
            if name.lower() in player_names:
                logger.info("ERROR: that name is taken!")
                name = ''
            if name.lower() == 'end':
                if len(player_names) < 5:
                    logger.info("ERROR:  you need more players to play.")
                    logger.info("")
                    get_name()
                else:
                    return player_names
            else:
                if name != '':
                    player_names.append(name.lower())
                get_name()
        get_name()
        return player_names

    def confirm_players(self):
        logger.info("The following players are in the game:")
        for p in self.players:
            logger.info(f"  {p}")
        logger.info("")

    @property
    def number_of_players(self):
        return len(self.players)

    def confirm_special_characters(self):
        self.assassin = (input("do you want to play with the Assassin?").lower() == 'y')
        if self.assassin == True:
            i = self.characters.index('evil')
            self.characters[i] = 'assassin'

        self.merlin = (input("do you want to play with Merlin?").lower() == 'y')
        if self.merlin == True:
            i = self.characters.index('good')
            self.characters[i] = 'merlin'


        self.percival = (input("do you want to play with Percival?").lower() == 'y')
        if self.percival == True:
            i = self.characters.index('good')
            self.characters[i] = 'percival'

        self.morgana = (input("do you want to play with Morgana?").lower() == 'y')
        if self.morgana == True:
            i = self.characters.index('evil')
            self.characters[i] = 'morgana'

        logger.info(f"you will play with the following characters: {self.characters}")
        logger.info("")

    def assign_characters(self):
        characters = self.characters
        random.shuffle(characters)
        logger.debug(f"characters = {characters}")
        roles = {}
        for player in self.players:
            roles[player] = characters.pop()
        return roles


    def communicate_characters(self):
        def print_evil_characters():
            for p, r in self.roles.items():
                if r in ('evil', 'assassin', 'morgana'):
                    logger.info(f"  {p}")

        for player, role in self.roles.items():
            input(f"Press enter when only {player} is looking at this screen")
            logger.info(f"{player}, your role is {role}.")
            if role == 'merlin':
                logger.info(f"Your special ability is that you know who is evil:")
                print_evil_characters()
                logger.info(f"But be careful, the Assassin will get one chance to kill you at the end of the game.")
            elif role == 'assassin':
                logger.info(f"You are evil and you will get one chance to kill Merlin at the end of the game.")
                logger.info(f"If you can correctly identify Merlin at this time, evil will win.")
                input("Press enter when you understand.")
                logger.info(f"You also get to know who else is evil:")
                print_evil_characters()
            elif role == 'percival':
                if self.morgana == True:
                    logger.info(f"One of the following characters is Merlin, the other is evil.")
                else:
                    logger.info(f"Your special ability is that you get to know who merlin is")
                for p, r in self.roles.items():
                    if r in ('merlin', 'morgana'):
                        logger.info(f"  {p}")
            elif role == 'morgana':
                if self.percival == True:
                    logger.info(f"You are evil and your special ability is that you pose as Merlin. Percival may think that you are Merlin.")
                else:
                    logger.info(f"ERROR: morgana is not much use as a special character if Percival is not playing. I will assume that you are just an ordinary evil character")
                input("Press enter when you understand.")
                logger.info(f"You also get to know who else is evil:")
                print_evil_characters()
            elif role == 'evil':
                logger.info(f"You get to know who else is evil:")
                print_evil_characters()
            elif role == 'good':
                # logger.info("Go forth in Merlin's name")
                pass
            else:
                raise AttriuteError(f"ERROR: There was an unexpected role. {player} was assigned {role}, but this was not one of the expected roles: merlin, percival, assassin, morgana, good, evil")
            input("Press enter when you understand.")
            clear_console()

    def determine_who_starts(self):
        def players_per_quest():
            if self.number_of_players == 5:
                return (2, 3, 2, 3, 3)
            elif self.number_of_players == 6:
                return (2, 3, 4, 3, 4)
            elif self.number_of_players == 7:
                return (2, 3, 3, 4, 4)
            else:
                return (3, 4, 4, 5, 5)

        logger.info("The number of players on each quest for each mission is as follows:")

        for q in range(5):
            logger.info(f"  {q+1}: {players_per_quest()[q]}")

        if self.number_of_players >=7:
            logger.info(r"Note: on quest number 4, two fails must be given to fail the mission")

        logger.info("")
        logger.info(f"{random.choice(self.players)} will start by choosing who goes on the first quest.")





if __name__ == "__main__":
    game = Session()
