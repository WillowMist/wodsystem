import re
import wodsystem
from evennia.utils import evtable, pad, fill, eveditor, evmenu
from evennia.utils.utils import justify
from evennia.utils.ansi import strip_ansi, ANSIString
from time import sleep
from evennia.contrib.dice import roll_dice

def init_object(obj):
    size = obj.ndb.size if obj.nattributes.has('size') else 5
    race = obj.ndb.race if obj.nattributes.has('race') else 'Mortal'
    reset = False
    if not obj.attributes.has('cg_info') or not len(obj.db.cg_info) or obj.db.cg_info['Race'] != race:
        obj.db.cg_info = {'Race': race, 'Size': size}
        reset = True
    if not obj.attributes.has('cg_attributes') or not len(obj.db.cg_attributes) or reset:
        obj.db.cg_attributes = get_base_stats(obj, wodsystem.ATTRIBUTE_LIST, base_stat=1)
    if not obj.attributes.has('cg_skills') or not len(obj.db.cg_skills) or reset:
        obj.db.cg_skills = get_base_stats(obj, wodsystem.SKILL_LIST)
    if not obj.attributes.has('cg_skill_specialties') or not len(obj.db.cg_skill_specialties) or reset: obj.db.cg_skill_specialties = []
    if not obj.attributes.has('cg_merits') or not len(obj.db.cg_merits) or reset:
        obj.db.cg_merits = get_base_stats(obj, wodsystem.MERIT_LIST)
    if not obj.attributes.has('cg_flaws') or not len(obj.db.cg_flaws) or reset: obj.db.cg_flaws = {}
    if not obj.attributes.has('cg_pools') or not len(obj.db.cg_pools) or reset: obj.db.cg_pools = {}
    if not obj.attributes.has('cg_advantages') or not len(obj.db.cg_advantages) or reset: obj.db.cg_advantages = {}
    if not obj.attributes.has('cg_creationpools') or not len(obj.db.cg_creationpools) or reset: obj.db.cg_creationpools = {'Attributes': (5, 4, 3), 'Skills': (11, 7, 4), 'Specialties': 3, 'Merits': 7}
    if not obj.attributes.has('cg_chargenfinished') or reset: obj.db.cg_chargenfinished = False


def wod_header(title=None, align="l", linecolor="W", textcolor="w", accentcolor="w"):
    '''
    Shows a 78 character wide header.  Optional header imbedded in it.

    :param title: String that will be shown in white over the header, optional.
    :param align: "l", "c", or "r" alignment.  Only used if title is provided.
    :param linecolor: Single character color code, default is 'W' (Light grey)
    :param textcolor: Single character color code, default is 'w' (White)
    '''
    if title:
        fulltitle = "|%s===|%s|||%s %s |%s|||%s===" % (linecolor, accentcolor, textcolor, title, accentcolor, linecolor)
        w = len(strip_ansi(fulltitle))
        if align == "r":
            line = '|%s%s|n' % (linecolor, ANSIString(fulltitle).rjust(width=78, fillchar="="))
        elif align == "c":
            line = '|%s%s|n' % (linecolor, ANSIString(fulltitle).center(width=78, fillchar="="))
        else:
            line = '|%s%s|n' % (linecolor, ANSIString(fulltitle).ljust(width=78, fillchar="="))
    else:
        line = '|%s%s|n' % (linecolor, pad('', width=78, fillchar='='))
    return line


def get_base_stats(obj, template, base_stat=0):
    racetemplate = get_template_options(obj, template)
    basestats = {}
    for header in template['Headers']:
        headerstat = {}
        for stat in racetemplate[header]:
            if base_stat:
                headerstat[stat] = base_stat
        basestats[header] = headerstat
    return basestats


def get_sheet(target):
    '''
    Returns the character sheet for target.

    :param target: object reference of a WoDCharacter or WoDEventCharacter
    '''
    if 'Race' in list(target.db.cg_info.keys()):
        cg_race = target.db.cg_info['Race']
    else:
        cg_race = 'Default'
    return_table = wod_header("Character Sheet: %s" % target.name, align="r", linecolor="M", accentcolor="w", textcolor="y")
    return_table += '\n'
    return_table += str(get_cg_info(cg_race, wodsystem.INFO_LIST,target.db.cg_info, target))
    return_table += '\n'
    return_table += str(get_cg_data(wodsystem.ATTRIBUTE_LIST, ['Physical', 'Social', 'Mental'], target.db.cg_attributes, caller=target))
    return_table += '\n'
    return_table += str(get_cg_data(wodsystem.SKILL_LIST, ['Physical', 'Social', 'Mental'], target.db.cg_skills, useheaders=False, caller=target))
    return_table += '\n'
    return_table += str(get_cg_data(wodsystem.MERIT_LIST, ['Physical', 'Social', 'Mental'], target.db.cg_merits, datatype='merits', useheaders=False, caller=target))
    return return_table


def get_race(target):
    '''

    :param target: object reference of a WoDCharacter or WoDEventCharacter
    :return:
    '''
    if 'Race' in list(target.db.cg_info.keys()):
        cg_race = target.db.cg_info['Race']
    else:
        cg_race = 'Default'
    return cg_race


def get_template_options(target, template):
    cg_race = get_race(target)
    if cg_race in list(template.keys()):
        datalist = template[cg_race]
    else:
        datalist = template['Default']
    return datalist


def get_cg_points_spent(group, base_stat=0):
    points = 0
    for item in list(group.keys()):
        if str(group[item]).isdigit():
            temppoints = group[item]
            if group[item] > 4: temppoints += (group[item] - 4)
            temppoints -= base_stat
            points += temppoints
        else:
            temppoints = get_cg_points_spent(group[item], base_stat=base_stat)
            points += temppoints
    return points


def get_cg_data(template, headers, data, useheaders=True, highlight_column=None, highlight_stat=None,
                datatype=None, caller=None, points_left = 0, for_purchase=False):
    datalist = get_template_options(caller, template)
    columns = []
    maxcontent=0
    if for_purchase:
        # Show all purchasble stats, marking ones that have been purchased in yellow.
        if datatype=='merits':
            for group in headers:
                tempcolumn = []
                for dataentry in sorted(datalist[group].keys()):
                    show_for_purchase = True
                    merit = parse_merit(datalist[group][dataentry])
                    ratings = merit['Cost']
                    if (dataentry in list(data[group].keys())):
                        if not merit['Multibuy']:
                            show_for_purchase = False
                        purchasedmerit = data[group][dataentry]
                        if str(purchasedmerit).isdigit():
                            statline = '%-20.20s %s' % (dataentry, purchasedmerit)
                            if (highlight_column and highlight_column == group):
                                statline = '|y%s|n' % statline
                            else: statline = '|Y%s|n' % statline
                            tempcolumn.append(statline)
                        else:
                            for entry in list(purchasedmerit.keys()):
                                meritname = '%s (%s)' % (dataentry, entry)
                                statline = '%-20.20s %s' % (meritname, purchasedmerit[entry])
                                if (highlight_column and highlight_column == group):
                                    statline = '|y%s|n' % statline
                                else:
                                    statline = '|Y%s|n' % statline
                                tempcolumn.append(statline)
                    if show_for_purchase:
                        if len(ratings) == 1:
                            statline = '%-20.20s %s' % (dataentry, ratings[0])
                        else:
                            statline = '%-18.18s %s-%s' % (dataentry, ratings[0], ratings[len(ratings)-1])
                        if (highlight_column and highlight_column == group) or (highlight_stat and highlight_stat == dataentry):
                            if merit_can_buy(caller, merit, points_left):
                                statline = '|w%s|n' % statline
                            else:
                                statline = '|r%s|n' % statline
                        else:
                            if merit_can_buy(caller, merit, points_left):
                                statline = '|W%s|n' % statline
                            else:
                                statline = '|R%s|n' % statline
                        tempcolumn.append(statline)
                maxcontent = max(len(tempcolumn), maxcontent)
                columns.append(tempcolumn)
        else:
            for group in headers:
                tempcolumn = []
                for dataentry in datalist[group]:
                    if dataentry in list(data[group].keys()) and (data[group][dataentry]):
                        statline = '%-20.20s %s' % (dataentry, data[group][dataentry])
                        if (highlight_column and highlight_column == group) or (highlight_stat and highlight_stat == dataentry):
                            statline = '|y%s|n' % statline
                        else:
                            statline = '|Y%s|n' % statline
                        tempcolumn.append(statline)
                    else:
                        statline = '%-20.20s %s' % (dataentry, 0)
                        if (highlight_column and highlight_column == group) or (highlight_stat and highlight_stat == dataentry):
                            statline = '|w%s|n' % statline
                        tempcolumn.append(statline)

                maxcontent = max(len(tempcolumn), maxcontent)
                columns.append(tempcolumn)
    else:
        if datatype=='merits':
            for group in headers:
                tempcolumn = []
                for dataentry in sorted(data[group].keys()):
                    purchasedmerit = data[group][dataentry]
                    if str(purchasedmerit).isdigit():
                        statline = '%-20.20s %s' % (dataentry, purchasedmerit)
                        tempcolumn.append(statline)
                    else:
                        for entry in list(purchasedmerit.keys()):
                            meritname = '%s (%s)' % (dataentry, entry)
                            statline = '%-20.20s %s' % (meritname, purchasedmerit[entry])
                            tempcolumn.append(statline)
                maxcontent = max(len(tempcolumn), maxcontent)
                columns.append(tempcolumn)
        else:
            for group in headers:
                tempcolumn = []
                for dataentry in sorted(data[group]):
                    if data[group][dataentry]:
                        statline = '%-20.20s %s' % (dataentry, data[group][dataentry])
                        tempcolumn.append(statline)
                maxcontent = max(len(tempcolumn), maxcontent)
                columns.append(tempcolumn)
    if maxcontent:
        if useheaders:
            table = evtable.EvTable(*headers, table=columns, border="tablecols")
        else:
            table = evtable.EvTable(table=columns, borders="tablecols")
        table.reformat(width=78)
    else:
        table = ''
    return table


def get_cg_info(race, template, data, target):
    if race in list(template.keys()):
        infolist = template[race]
    else:
        infolist = template['Default']
    leftcolumn=['Name: %30.30s' % (target.name,)]
    rightcolumn=['Race: %29.29s' % (data['Race'],)]
    for infoentry in infolist['Left']:
        if infoentry in list(data.keys()):
            w = 36 - len('%s: ' % infoentry)
            try:
                leftline = '%s: %s' % (infoentry, justify(data[infoentry], width=w, align='r'))
            except TypeError as e:
                leftline = e
            leftcolumn.append(leftline)
    for infoentry in infolist['Right']:
        if infoentry in list(data.keys()):
            w = 35 - len('%s: ' % infoentry)
            try:
                rightline = '%s: %s' % (infoentry, justify(data[infoentry], width=w, align='r'))
            except TypeError as e:
                rightline = e
            rightcolumn.append(rightline)
    table = evtable.EvTable(table=[leftcolumn, rightcolumn], border='incols')
    table.reformat(width=78)
    return table


def background_edit(caller):
    caller.msg("""

    Now editing your character background.  Please save and exit background to move on to Attributes.  
    Use |w:h|n for help.

    """)
    eveditor.EvEditor(caller, loadfunc=load_bg, savefunc=save_bg, quitfunc=quit_bg, key='Background Editor')


def load_bg(caller):
    "Get the current value"
    if 'Background' in list(caller.db.cg_info.keys()):
        return caller.db.cg_info['Background']
    else:
        return ''


def save_bg(caller, buffer):
    "Set the background information"
    caller.db.cg_info['Background'] = buffer
    caller.msg("Background saved")


def quit_bg(caller):
    caller.msg("Exiting Background Editor")
    if not caller.db.cg_chargenfinished:
        evmenu.EvMenu(caller, "wodsystem.menu", startnode="menu_chargen", cmd_on_exit=None)


def search_stat(caller, statstring, subsection='None', depth=0, matched=False):
    results = []
    tempdict = {}
    if subsection != 'None':
        tempdict = subsection
    else:
        for section in wodsystem.SEARCHABLE_SECTIONS:
            tempdict[section] = caller.attributes.get(section)
    for stat in list(tempdict.keys()):
        if str(tempdict[stat]).isdigit():
            if (statstring.lower() in stat.lower()) or matched:
                results.append({'Stat': stat, 'Value': tempdict[stat]})
        else:
            matched = True if (statstring.lower() in stat.lower() or matched) else False
            tempresults = search_stat(caller, statstring, subsection=tempdict[stat], depth=depth+1, matched=matched)
            for entry in tempresults:
                if stat in wodsystem.SEARCHABLE_SECTIONS:
                    results.append({'Stat': entry['Stat'], 'Value': entry['Value']})
                else:
                    if depth <= 1:
                        results.append({'Stat': entry['Stat'], 'Value': entry['Value']})
                    else:
                        results.append({'Stat': '%s (%s)' % (stat, entry['Stat']), 'Value': entry['Value']})
    return results


def get_stat(caller, stat):
    stats = search_stat(caller, stat)
    if len(stats) == 0:
        return None
    elif len(stats) > 1:
        return -1
    else:
        return stats[0]['Value']


def search_stat_disambiguation(statlist):
    commastring = ""
    sortedlist = sorted(statlist, key = lambda i: i['Stat'])
    for x in range(0, len(sortedlist)):
        if x > 0:
            commastring += ', '
        if x+1 == len(sortedlist):
            commastring += 'or '
        commastring += '|y%s|n' % sortedlist[x]['Stat']
    returnstring = "Did you mean %s?" % commastring
    return returnstring


def wod_dice(dice, difficulty=8):
    results = {'Dice': dice,
               'Difficulty': difficulty,
               'Successes': 0,
               'Results': []}
    while dice:
        result, outcome, diff, rolls = roll_dice(dice, 10, return_tuple=True)
        dielist = []
        for die in list(rolls):
            dielist.append(die)
            if die >= difficulty:
                results['Successes'] += 1
            if die < 10:
                dice -= 1
        results['Results'].append(dielist)
    return results


def parse_dicestring(caller, dicestring):
    RE_PARTS = re.compile(r"(\+|-)")
    MODS = ["+", "-"]
    parts = [part.strip() for part in RE_PARTS.split(dicestring) if part]
    dice = 0
    dicestring = ""
    cur_mod = '+'
    for part in parts:
        if part.isdigit():
            part = int(part)
            dicestring += " %d" % part
        elif part in MODS:
            cur_mod = part
            dicestring += " %s" % cur_mod
            part = 0
        else:
            tempstat = search_stat(caller, part)
            if len(tempstat) == 0:
                return False, "'%s' not found." % part, None
            if len(tempstat) > 1:
                return False, "'%s' has too many matches.  %s" % (part, search_stat_disambiguation(tempstat)), None
            else:
                part = int(tempstat[0]['Value'])
                dicestring += " |y%s|n" % tempstat[0]['Stat']
        if cur_mod == "-":
            dice -= part
        elif cur_mod == "+":
            dice += part
        else:
            return False, "Something went wrong.",
    return True, dice, dicestring.strip()


def parse_dicestring_rhs(caller, rhsstring):
    RE_PARTS = re.compile(r"(/)")
    parts = [part.strip() for part in RE_PARTS.split(rhsstring) if part]
    target = None
    difficulty = None
    for part in parts:
        if part.isdigit():
            difficulty = int(part)
        elif part == "/":
            pass
        else:
            temptarget = caller.search(part)
            if temptarget:
                target = temptarget
            else:
                msg = "Could not find '%s'" % part
                return False, target, difficulty, msg
    return True, target, difficulty, None


def merit_can_buy(character, merit, points):
    reqgroups = []
    for reqgroup in merit['Prereqs']:
        prereqpassed = True
        for stat in list(reqgroup.keys()):
            if not has_stat(character, stat, reqgroup[stat]):
                prereqpassed = False
        reqgroups.append(prereqpassed)
    if any(reqgroups) or len(reqgroups) == 0:
        if points >= merit['Cost'][0]:
            return True
    return False


def merit_check_prereqs(character, merit):
    reqstring = ''
    for reqgroup in merit['Prereqs']:
        if len(reqstring):
            reqstring += '\n|-|wOR|n\n'
        prereqpassed = True
        tempstring = ''
        for stat in list(reqgroup.keys()):
            if len(tempstring):
                tempstring += ', '
            if has_stat(character, stat, reqgroup[stat]):
                tempstring += '|y%s (%s)|n' % (stat, reqgroup[stat])
            else:
                tempstring += '|r%s (%s)|n' % (stat, reqgroup[stat])
        reqstring += tempstring
    return reqstring


def calculate_advantages(caller):
    attributes = caller.db.cg_attributes
    reflexes = caller.db.cg_merits['Physical']['Fast Reflexes'] if 'Fast Reflexes' in caller.db.cg_merits['Physical'].keys() else 0
    health = attributes['Physical']['Stamina'] + caller.db.cg_info['Size']
    willpower = attributes['Mental']['Resolve'] + attributes['Social']['Composure']
    defense = min([attributes['Physical']['Dexterity'], attributes['Mental']['Wits']])
    initiative = attributes['Physical']['Dexterity'] + attributes['Social']['Composure'] + reflexes
    speed = attributes['Physical']['Strength'] + attributes['Physical']['Dexterity'] + 5
    return_dict = {'Health': health, 'Willpower': willpower, 'Defense': defense, 'Initiative': initiative, 'Speed': speed}
    return return_dict


def parse_merit(merit):
    merit['Prereqs'] = [] if not 'Prereqs' in list(merit.keys()) else merit['Prereqs']
    merit['Effect'] = [] if not 'Effect' in list(merit.keys()) else merit['Effect']
    merit['Cost'] = [merit['Cost']] if str(merit['Cost']).isdigit() else merit['Cost']
    merit['Multibuy'] = False if not 'Multibuy' in list(merit.keys()) else merit['Multibuy']
    merit['Availability'] = None if not 'Availability' in list(merit.keys()) else merit['Availability']
    return merit


def has_stat(character, stat, level=0):
    statlevel = get_stat(character, stat)
    if statlevel and statlevel >= level:
        return True
    else:
        return False

