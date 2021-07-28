import numpy as np
import Levenshtein
class Card:

    def __init__(self, top, bottom):
        self.name = top
        self.anime = bottom

    def isCharacter(self, people):
        return self.isSomething("p",people)

    def isAnime(self, anime):
        return self.isSomething("a",anime)
    
    def isSomething(self, what, list_of_interested):
        
        if what == "a":
            string_to_ratio = self.anime
        else:
            string_to_ratio = self.name

        ratio = Levenshtein.seqratio(string_to_ratio, list_of_interested)  
        #print(f"{string_to_ratio} == {list_of_interested} ? Accuracy: {ratio}")

        if ratio > 0.6:
            return True
        else:
            return False

    def __str__(self):
        return f"Anime: [{self.anime}] - Character: [{self.name}]"