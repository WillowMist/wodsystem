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
        'Right': ['Virtue', 'Vice', 'Faction']
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
    'Headers': ['Physical', 'Social', 'Mental'],
    'Default': {
        'Physical': {},
        'Social': {'Retainer': {'Cost': [1,2,3,4,5],
                                'Effect': '',
                                'Multibuy': True}
        },
        'Mental': {'Common Sense': {'Cost': 4,
                                    'Effect': "Makes sound, straightforward decisions after a few moments' thought. Staff can make a reflexive Wits + Composure roll once per chapter for a PC with the merit if it is about to embark on a disastrous course of action, or if the PC finds itself at a point in the story where the PC is completely stumped for ideas. If the roll succeeds, Staff may point out the risks of a particular course, or suggest possible actions that the PC can take that might get events back on track. Note: A PC is free to ask Staff for a Common Sense roll when out of ideas, however, remember it's an aid, not a crutch and it should not be over used.",
                                    'Availability': 'chargen',
                                    },
                   'Danger Sense': {'Cost': 2,
                                    'Effect': "A sixth sense that staff may use to warn of danger. +2 modifier on reflexive Wits + Composure rolls to detect an impending ambush."
                                    },
                   'Eiditic Memory': {'Cost': 2,
                                      'Effect': "With a near-photographic memory, this merit able to recall vast amounts of observed detail with astonishing accuracy. Make no roll to remember an obscure fact or past experience, unless under stress then there is a +2 modifier on any Intelligence + Composure or other Skill-based roll (say, Academics, to remember a fact) for memory recall.",
                                      'Availability': 'chargen'
                                      },
                   'Emotional Detachment': {'Cost': 1,
                                            'Prereqs': [{'Resolve': 2}],
                                            'Effect': "Can distance oneself from the pain, grief and suffering of fellow human beings long enough to help them. Ignore penalties stemming from stress equal to Resolve rating. When one might normally suffer a -2 penalty from sheer emotional pressure, this Merit with a Resolve were 2 or higher, suffers no penalty."
                                            }
        }
    },
    'Old': {
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