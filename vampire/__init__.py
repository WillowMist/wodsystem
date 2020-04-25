import wodsystem

wodsystem.RACE_LIST.append('Vampire')
wodsystem.CHARGEN_SYSTEMS['Vampire'] = list(wodsystem.CHARGEN_SYSTEMS['Default']) + ['Disciplines', 'Covenant']
wodsystem.FACTIONS_LIST['Vampire'] = list(wodsystem.FACTIONS_LIST['Default'])
wodsystem.FACTIONS_LIST['Vampire'].append('Ventrue')

