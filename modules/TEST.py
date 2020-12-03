dictionary = [
    {"featureId": 6, "providers": [{"id": 6, "name": "Sport Radar"}, {"id": 1, "name": "Enet Pulse"}], "sportId": 1, "tournamentStageId": 576, "updatedAt": 1605720267685},
    {"featureId": 6, "providers": [{"id": 6, "name": "Sport Radar"}, {"id": 1, "name": "Enet Pulse"}], "sportId": 1, "tournamentStageId": 588, "updatedAt": 1605720267679}
]
for mt in dictionary:
    for sportId, tournamentStageId in mt.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
        print(mt)
        if sportId == 1 and tournamentStageId == 588:
            pass # print(mt)
