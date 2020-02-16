import xml.etree.ElementTree as ET


class PKN_DEX_Load:
    def __init__(self, pkmn_id, DataFile):
        self.XML = DataFile + ".xml"
        self.tree = ET.parse(self.XML)
        self.root = self.tree.getroot()

        self.base_info = []
        self.move_info = []
        self.stat_info = []

        tree = self.tree
        root = self.root
        for i in root:
            if i.tag == "GenderedEntity":
                for e in i:
                    if e.tag == "BaseStats":
                        for s in e:
                            if (s.tag, s.text) not in self.base_info:
                                self.base_info.append((s.tag, s.text))

            if i.tag == "Moveset":
                for e in i:
                    if e.tag == "LevelUpMoves":
                        for s in e:
                            if s.tag == "Learn":
                                gloss = []
                                for v in s:
                                    gloss.append((v.tag, v.text))
                                #print(gloss)
                                self.move_info.append(gloss)

            if i.tag == "StatsGrowth":
                for e in i:
                    if e.tag == "Level":
                        additions = []
                        for s in e:
                            additions.append((s.tag, s.text))
                        self.stat_info.append(additions)


read = PKN_DEX_Load(0, '0025_pikachu')

print(read.base_info)
print(read.move_info)
print(read.stat_info)

