import wodsystem

wodsystem.RACE_LIST.append('Vampire')

wodsystem.FACTIONS_LIST['Vampire'] = list(wodsystem.FACTIONS_LIST['Default'])
wodsystem.FACTIONS_LIST['Vampire'].append('Ventrue')
