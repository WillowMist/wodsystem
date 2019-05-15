ATTRIBUTE_LIST = {
    'Headers': ['Physical', 'Social', 'Mental'],
    'Default': {
        'Physical': ['Strength', 'Dexterity', 'Stamina'],
        'Social': ['Presence', 'Manipulation', 'Composure'],
        'Mental': ['Intelligence', 'Wits', 'Resolve']
    }
}

INFO_LIST = {
    'Default': {
        'Left': ['Age', 'Concept', 'Class'],
        'Right': ['Virtue', 'Vice']
    }
}

SKILL_LIST = {
    'Headers': ['Physical', 'Social', 'Mental'],
    'Default': {
        'Physical': ['Archery', 'Athletics', 'Brawl', 'Crafts', 'Dodge', 'Legerdemain',  'Melee', 'Ride', 'Survival', 'Stealth'],
        'Social': ['Empathy', 'Expression', 'Intimidation', 'Leadership', 'Subterfuge', 'Animal Ken', 'Commerce', 'Etiquette', 'Performance', 'Politics'],
        'Mental': ['Alertness', 'Academics', 'Hearth Wisdom', 'Investigation', 'Law', 'Linguistics', 'Medicine', 'Occult', 'Seneschal', 'Theology']
    }
}

RACE_LIST = ['Mortal', 'Mortal+', 'Vampire', 'Werewolf', 'Mage', 'Changeling']

VIRTUE_LIST = ['Charity', 'Faith', 'Fortitude', 'Hope', 'Justice', 'Prudence', 'Temperance']

VICE_LIST = ['Envy', 'Gluttony', 'Greed', 'Lust', 'Pride', 'Sloth', 'Wrath']

MERIT_LIST = {
    'Default': {
        'Physical': {'Ambidextrous': 3, 'Brawling Dodge': 1, 'Direction Sense': 1, 'Disarm': 2, 'Fast Reflexes': [1,2],
                     'Fighting Finesse': 2, 'Fighting Style: Boxing': [1,2,3,4,5], 'Fighting Style: Kung Fu': [1,2,3,4,5],
                     'Fighting Style: Two Weapons': [1,2,3,4,5], 'Fleet of Foot': [1,2,3], 'Fresh Start': 1, 'Giant': 4,
                     'Gunslinger': 3, 'Iron Stamina': [1,2,3], 'Iron Stomach': 2, 'Natural Immunity': 1, 'Quick Draw': 1,
                     'Quick Healer': 4, 'Strong Back': 1, 'Strong Lungs': 3, 'Stunt Driver': 3, 'Toxin Resistance': 2,
                     'Weaponry Dodge': 1},
        'Social': {'Allies': [1,2,3,4,5], 'Barfly': 1, 'Contacts': [1,2,3,4,5], 'Fame': [1,2,3], 'Inspiring': 4,
                   'Mentor': [1,2,3,4,5], 'Resources': [1,2,3,4,5], 'Retainer': [1,2,3,4,5], 'Status': [1,2,3,4,5],
                   'Striking Looks': [2,3,4]},
        'Mental': {'Common Sense': 4, 'Danger Sense': 2, 'Eidetic Memory': 2, 'Encyclopedic Knowledge': 4,
                   'Holistic Awareness': 3, 'Language': [1,2,3], 'Meditative Mine': 1, 'Unseen Sense': 3}
    }
}

FACTIONS_LIST = {
    'Default': ['None'],
}

SEARCHABLE_SECTIONS = ['cg_attributes', 'cg_skills', 'cg_advantages', 'cg_merits', 'cg_flaws']