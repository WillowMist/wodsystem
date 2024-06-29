CHARGEN_SYSTEMS = {
    'Default': ['Attributes', 'Skills', 'Merits', 'Virtue', 'Vice']
}

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

RACE_LIST = ['Mortal', 'Mortal+']

VIRTUE_LIST = ['Charity', 'Faith', 'Fortitude', 'Hope', 'Justice', 'Prudence', 'Temperance']

VICE_LIST = ['Envy', 'Gluttony', 'Greed', 'Lust', 'Pride', 'Sloth', 'Wrath']

MERIT_LIST = {
    'Headers': ['Physical', 'Social', 'Mental'],
    'Default': {
        'Physical': {'Ambidextrous': {'Cost': 3,
                                      'Effect': "Your character does not suffer the -2 penalty for using his off-hand in combat or to perform other actions."
                                      },
                     'Brawling Dodge': {'Cost': 1,
                                        'Effect': "Whenever your character performs a dodge, you can choose to add his Brawl Skill dots to his Defense instead of doubling his Defense.  He essentially draws on his training in blocking and evading attacks rather than relying on his raw ability alone.  While this might provide little benefit to a brawling novice, it can give the advanced fighter an edge.\nBrawling Dodge applies against incoming Brawl- and Weaponry-based attacks, against thrown-weapon attacks, and against Firearms attacks made within close-combat range. Your character can move up to his Speed and perform a Brawling Dodge maneuver in a turn.\nA character can possess both the Brawling Dodge and Weaponry Dodge Merits, but only one can be used per turn."
                                        },
                     'Direction Sense': {'Cost': 1,
                                         'Effect': "Your character has an innate sense of direction that instinctively allows him to remain oriented. He can enter unfamiliar territory and always retrace his steps back to his starting point, and can orient himself to any of the compass points (i.e., face north, face south) without references."
                                         },
                     'Disarm': {'Cost': 2,
                                'Effect': "Your character has refined his Weaponry Skill to the extent that he can use a weapon to disarm opponents in close combat. When making a normal attack, compare your successes to the opponent’s Dexterity. If you get a number of successes equal to or greater than the opponent’s Dexterity, you can choose to have your character disarm him instead of doing damage. A weapon lands a number of yards away from the opponent equal to your successes rolled."
                                },
                     'Fast Reflexes': {'Cost': [1,2],
                                       'Prereqs': [{'Dexterity': 3}],
                                       'Effect': "Your character’s mix of sharp reflexes and steady nerves helps him get the drop on adversaries."
                                       },
                     'Fighting Finesse': {'Cost': 2,
                                          'Prereqs': [{'Dexterity': 3, 'Weaponry': 2}],
                                          'Effect': "Your character prefers to fight with a chosen weapon in a manner that favors agility over power. With that one weapon (a rapier or katana, for example), you may substitute your character’s Dexterity for Strength when making attack rolls.\nThis Merit may be purchased multiple times to gain agility with more weapons, one for each purchase.",
                                          'Multibuy': True
                                          },
                     'FS: Boxing 1 (Body Blow)': {'Cost': 1,
                                                  'Prereqs': [{'Strength': 3, 'Stamina': 2, 'Brawl': 2}],
                                                  'Effect': "Your character can deliver powerful blows that leave opponents reeling and gasping for air. If successes inflicted in a single Brawl attack equal or exceed a target’s Size, the victim loses his next action."
                                                  },
                     'FS: Boxing 2 (Duck and Weave)': {'Cost': 2,
                                                       'Prereqs': [{'FS: Boxing 1 (Body Blow)': 1}],
                                                       'Effect': "Your character is trained to instinctively duck and evade an opponent’s blows. Use the higher of your character’s Dexterity or Wits to determine his Defense when dealing with Brawl-based attacks only (not against Weaponry attacks). If a combination of Brawl- and Weaponry-based attacks is focused on your character in the same turn, use his normal Defense against both."
                                                       },
                     'FS: Boxing 3 (Combination Blows)': {'Cost': 3,
                                                          'Prereqs': [{'FS: Boxing 2 (Duck and Weave)': 2}],
                                                          'Effect': "Your characters training and experience allow him to devastate opponents with a flurry of rapid blows. He can make two Brawl attacks against the same target in a single action. The second attack suffers a -1 penalty. Drawback: Your character cannot use his Defense against any attack in the same turn in which he intends to use this maneuver. If he uses Defense against attacks that occur earlier in the Initiative roster, before he can perform this maneuver, he cannot perform the maneuver in the turn. He is too busy bobbing and weaving out of the way of attacks."
                                                          },
                     'FS: Boxing 4 (Haymaker)': {'Cost': 4,
                                                 'Prereqs': [{'FS: Boxing 3 (Combination Blows)': 3}],
                                                 'Effect': "Your character can deliver powerful, accurate blows capable of knocking an opponent unconscious with a single punch. A single Brawl attack that equals or exceeds the target’s Size in damage might knock him unconscious. A Stamina roll is made for the victim.  If it succeeds, he is conscious but he still loses his next action due to the Body Blow. If it fails, he is unconscious for a number of turns equal to the damage done. Drawback: Your character cannot use his Defense against any attack in the same turn in which he intends to use this maneuver. If he uses Defense against attacks that occur earlier in the Initiative roster, before he can perform this maneuver, he cannot perform the maneuver in the turn. He is too busy bobbing and weaving out of the way of attacks."
                                                 },
                     'FS: Boxing 5 (Brutal Blow)': {'Cost': 5,
                                                    'Prereqs': [{'FS: Boxing 4 (Haymaker': 4}],
                                                    'Effect': "Your character's accuracy and power are such that his fists are lethal weapons, able to injure or kill opponents. A brutal blow inflicts lethal instead of bashing damage. Drawback: Spend one Willpower point per attack. Note that this Willpower expenditure does not add three dice to the attack. "
                                                    },
                     'FS: Kung Fu 1 (Focused Attack)': {'Cost': 1,
                                                        'Prereqs': [{'Strength': 2, 'Dexterity': 2, 'Stamina': 2, 'Brawl': 2}],
                                                        'Effect': "Physical conditioning and accuracy allow your character to deliver blows at vulnerable spots on targets. Penalties to hit specific targets are reduced by one. Even when a specific part of an opponent is not targeted, armor penalties to your character’s Brawl attacks are reduced by one."
                                                        },
                     'FS: Kung Fu 2 (Iron Skin)': {'Cost': 2,
                                                   'Prereqs': [{'FS: Kung Fu 1 (Focused Attack)': 1}],
                                                   'Effect': "Your character has hardened his body to physical blows, allowing him to withstand repeated hits with minimal effect. He has an effective armor trait of 1 against bashing attacks only."
                                                   },
                     'FS Kung Fu 3 (Defensive Attack)': {'Cost': 3,
                                    'Prereqs': [{'FS: Kung Fu 2 (Iron Skin)': 2}],
                                    'Effect': ""
                                    },
                     'FS Kung Fu 4 (Whirlwind Strike)': {'Cost': 4,
                                    'Prereqs': [{'FS Kung Fu 3 (Defensive Attack)': 3}],
                                    'Effect': ""
                                    },
                     'FS Kung Fu 5 (Lethal Strike)': {'Cost': 5,
                                    'Prereqs': [{'FS Kung Fu 4 (Whirlwind Strike)': 4}],
                                    'Effect': ""
                                    },
                     'FS Two Weapons 1 (Whirling Blades)': {'Cost': 1,
                                                            'Prereqs': [{'Dexterity': 3, 'Weaponry': 3}],
                                                            'Effect': ""},
                     'FS Two Weapons 2 (Deflect and Thrust)': {'Cost': 2,
                                        'Prereqs': [{'FS Two Weapons 1 (Whirling Blades)': 1}],
                                        'Effect': ""
                                        },
                     'FS Two Weapons 3 (Focused Attack)': {'Cost': 3,
                                        'Prereqs': [{'FS Two Weapons 2 (Deflect and Thrust)': 2}],
                                        'Effect': ""
                                        },
                     'FS Two Weapons 4 (Fluid Attack)': {'Cost': 5,
                                        'Prereqs': [{'FS Two Weapons 3 (Focused Attack)': 3}],
                                        'Effect': ""
                                        },
                     'Fleet of Foot': {'Cost': [1,2,3],
                                       'Prereqs': [{'Strength': 2}],
                                       'Effect': ""
                                       },
                     'Fresh Start': {'Cost': 1,
                                     'Prereqs': [{'Fast Reflexes': 2}],
                                     'Effect': ""
                                     },
                     'Giant': {'Cost': 4,
                               'Effect': ""
                               },
                     'Gunslinger': {'Cost': 3,
                                    'Prereqs': [{'Dexterity': 3, 'Firearms': 3}],
                                    'Effect': ""
                                    },
                     'Iron Stamina': {'Cost': [1,2,3],
                                      'Prereqs': [{'Stamina': 3}, {'Resolve': 3}],
                                      'Effect': ""},
                     'Iron Stomach': {'Cost': 3,
                                      'Prereqs': [{'Stamina': 2}],
                                      'Effect': ""
                                      },
                     'Natural Immunity': {'Cost': 1,
                                          'Prereqs': [{'Stamina': 2}],
                                          'Effect': ""
                                          },
                     'Quick Draw': {'Cost': 1,
                                    'Prereqs': [{'Dexterity': 3}],
                                    'Effect': "",
                                    },
                     'Quick Healer': {'Cost': 4,
                                      'Prereqs': [{'Stamina': 4}],
                                      'Effect': ""
                                      },
                     'Strong Back': {'Cost': 1,
                                     'Prereqs': [{'Strength': 2}],
                                     'Effect': ""
                                     },
                     'Strong Lungs': {'Cost': 3,
                                      'Prereqs': [{'Athletics': 3}],
                                      'Effect': ""
                                      },
                     'Stunt Driver': {'Cost': 3,
                                      'Prereqs': [{'Dexterity': 3}],
                                      'Effect': ""
                                      },
                     'Toxin Resistance': {'Cost': 2,
                                          'Prereqs': [{'Stamina': 3}],
                                          'Effect': ""
                                          },
                     'Weaponry Dodge': {'Cost': 1,
                                        'Prereqs': [{'Strength': 2, 'Weaponry': 1}],
                                        'Effect': ""
                                        }
                     },
        'Social': {'Allies': {'Cost': [1,2,3,4,5],
                              'Effect': "",
                              'Multibuy': True
                              },
                   'Barfly': {'Cost': 1,
                              'Effect': ""
                              },
                   'Contacts': {'Cost': [1,2,3,4,5],
                                'Effect': "",
                                'Multibuy': True
                                },
                   'Fame': {'Cost': [1,2,3],
                            'Effect': ""
                            },
                   'Inspiring': {'Cost': 4,
                                 'Prereqs': [{'Presence': 4}],
                                 'Effect': ""
                                 },
                   'Mentor': {'Cost': [1,2,3,4,5],
                              'Effect': ""
                              },
                   'Resources': {'Cost': [1,2,3,4,5],
                                 'Effect': ""
                                 },
                   'Retainer': {'Cost': [1,2,3,4,5],
                                'Effect': '',
                                'Multibuy': True
                                },
                   'Status': {'Cost': [1,2,3,4,5],
                              'Effect': "",
                              'Multibuy': True
                              },
                   'Striking Looks': {'Cost': [2,4],
                                      'Effect': ""
                                      }
        },
        'Mental': {'Common Sense': {'Cost': 4,
                                    'Effect': "Makes sound, straightforward decisions after a few moments' thought. Staff can make a reflexive Wits + Composure roll once per chapter for a PC with the merit if it is about to embark on a disastrous course of action, or if the PC finds itself at a point in the story where the PC is completely stumped for ideas. If the roll succeeds, Staff may point out the risks of a particular course, or suggest possible actions that the PC can take that might get events back on track. Note: A PC is free to ask Staff for a Common Sense roll when out of ideas, however, remember it's an aid, not a crutch and it should not be over used.",
                                    'Availability': 'chargen',
                                    },
                   'Danger Sense': {'Cost': 2,
                                    'Effect': "A sixth sense that staff may use to warn of danger. +2 modifier on reflexive Wits + Composure rolls to detect an impending ambush."
                                    },
                   'Eidetic Memory': {'Cost': 2,
                                      'Effect': "With a near-photographic memory, this merit able to recall vast amounts of observed detail with astonishing accuracy. Make no roll to remember an obscure fact or past experience, unless under stress then there is a +2 modifier on any Intelligence + Composure or other Skill-based roll (say, Academics, to remember a fact) for memory recall.",
                                      'Availability': 'chargen'
                                      },
                   'Emotional Detachment': {'Cost': 1,
                                            'Prereqs': [{'Resolve': 2}],
                                            'Effect': "Can distance oneself from the pain, grief and suffering of fellow human beings long enough to help them. Ignore penalties stemming from stress equal to Resolve rating. When one might normally suffer a -2 penalty from sheer emotional pressure, this Merit with a Resolve were 2 or higher, suffers no penalty."
                                            },
                   'Encyclopedic Knowledge': {'Cost': 4,
                                              'Effect': "Your character is a veritable font of useful (and sometimes useless) information on a wide variety of topics. Chances are he can come up with an anecdote pertaining to any situation based on something he’s read, witnessed or seen on TV."
                                              },
                   'Holistic Awareness': {'Cost': 3,
                                          'Effect': "Your character is skilled in the arts of whole-body healing, promoting health and recovery by keeping a person’s entire physiology balanced and strong. The result is that he is able to treat sickness and some injuries (those not requiring surgery, and ones suffered to bashing or lethal damage but not aggravated) with a collection of natural remedies rather than resorting to a doctor or hospital."
                                          },
                   'Language': {'Cost': [1,2,3,4],
                                'Effect': "Your character knows an additional language besides his own. One dot in this Merit means that he can read, write and speak an extra language with minimal fluency. Two dots indicate that he is literate and conversationally fluent. Three dots indicate that he can speak the language like a native and is well-read in it.",
                                'Multibuy': True
                                },
                   'Meditative Mind': {'Cost': 1,
                                       'Effect': "Your character can effortlessly enter a meditative state when she chooses, and can remain in it for as long as she wishes. All environmental penalties imposed to Wits + Composure rolls to meditate are ignored. Not even wound penalties apply to your character’s efforts to focus."
                                       },
                   'Unseen Sense': {'Cost': 3,
                                    'Prereqs': [{'Wits': 2}],
                                    'Effect': "Your character has a “sixth sense” when it comes to the supernatural. Perhaps his hair stands on end, goose bumps race along his arms, or a shiver runs up his spine. Regardless of the manner, his body reacts to the presence of unseen forces. He can’t see or hear anything, and in fact he might not know at first what causes this reaction. It might be a response to a specific type of supernatural phenomenon such as ghosts or vampires, or it might be a general sense that something isn’t right. Over time and with a little trial and error, he might be able to qualify what his body tries to tell him.\nThe specific type of supernatural phenomenon to which your character is sensitive must be determined when this Merit is purchased. It can be something as vague as a creepy feeling when in the presence of ghosts, or something as specific as a sudden chill when a vampire is nearby."
                   }
        }
    },
}

FACTIONS_LIST = {
    'Default': ['None'],
}

SEARCHABLE_SECTIONS = ['cg_attributes', 'cg_skills', 'cg_advantages', 'cg_merits', 'cg_flaws']

PACKAGES = {
    'Default': []
}