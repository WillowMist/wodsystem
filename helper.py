import wodsystem
from evennia.utils import evtable, pad, fill, eveditor, evmenu
from evennia.utils.utils import justify
from evennia.utils.ansi import strip_ansi, ANSIString
from time import sleep
from evennia.contrib.dice import roll_dice

def wod_header(title=None, align="l"):
    '''
    Shows a 78 character wide magenta header.  Optional header imbedded in it.

    :param title: String that will be shown in white over the header, optional.
    :param align: "l", "c", or "r" alignment.  Only used if title is provided.
    '''
    if title:
        fulltitle = "|M===|w|||n %s |w|||M===" % title
        w = len(strip_ansi(fulltitle))
        # line = '|M%s|n' % pad(fulltitle, width=90, align=align, fillchar="=")
        if align == "r":
            line = '|M%s|n' % ANSIString(fulltitle).rjust(width=78, fillchar="=")
        elif align == "c":
            line = '|M%s|n' % ANSIString(fulltitle).center(width=78, fillchar="=")
        else:
            line = '|M%s|n' % ANSIString(fulltitle).ljust(width=78, fillchar="=")
    else:
        line = '|M%s|n' % pad('', width=78, fillchar='=')
    return line

def get_sheet(target):
    '''
    Returns the character sheet for target.

    :param target: object reference of a WoDCharacter or WoDEventCharacter
    '''
    if 'Race' in target.db.cg_info.keys():
        cg_race = target.db.cg_info['Race']
    else:
        cg_race = 'Default'
    return_table = wod_header("Character Sheet: %s" % target.name, align="r")
    return_table += '\n'
    return_table += str(get_cg_info(cg_race, wodsystem.INFO_LIST,target.db.cg_info, target))
    return_table += '\n'
    return_table += str(get_cg_data(cg_race, wodsystem.ATTRIBUTE_LIST, ['Physical', 'Social', 'Mental'], target.db.cg_attributes))
    return_table += '\n'
    return_table += str(get_cg_data(cg_race, wodsystem.SKILL_LIST, ['Physical', 'Social', 'Mental'], target.db.cg_skills, useheaders=False))
    return return_table

def get_race(target):
    '''

    :param target: object reference of a WoDCharacter or WoDEventCharacter
    :return:
    '''
    if 'Race' in target.db.cg_info.keys():
        cg_race = target.db.cg_info['Race']
    else:
        cg_race = 'Default'
    return cg_race

def get_template_options(target, template):
    cg_race = get_race(target)
    if cg_race in template.keys():
        datalist = template[cg_race]
    else:
        datalist = template['Default']
    return datalist


def get_cg_data(race, template, headers, data, useheaders=True, highlight_column=None, highlight_stat=None, show_zero=False):
    if race in template.keys():
        datalist = template[race]
    else:
        datalist = template['Default']
    columns = []
    for group in headers:
        tempcolumn = []
        for dataentry in datalist[group]:
            if dataentry in data.keys() and (data[dataentry] or show_zero):
                statline = '%-20.20s %s' % (dataentry, data[dataentry])
                if (highlight_column and highlight_column == group) or (highlight_stat and highlight_stat == dataentry):
                    statline = '|w%s|n' % statline
                tempcolumn.append(statline)
        columns.append(tempcolumn)
    if useheaders:
        table = evtable.EvTable(*headers, table=columns, border="tablecols")
    else:
        table = evtable.EvTable(table=columns, borders="tablecols")
    table.reformat(width=78)
    return table

def get_cg_info(race, template, data, target):
    if race in template.keys():
        infolist = template[race]
    else:
        infolist = template['Default']
    leftcolumn=['Name: %30.30s' % (target.name,)]
    rightcolumn=['Race: %29.29s' % (data['Race'],)]
    for infoentry in infolist['Left']:
        if infoentry in data.keys():
            w = 36 - len('%s: ' % infoentry)
            try:
                leftline = '%s: %s' % (infoentry, justify(data[infoentry], width=w, align='r'))
            except TypeError as e:
                leftline = e
            leftcolumn.append(leftline)
    for infoentry in infolist['Right']:
        if infoentry in data.keys():
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
    if 'Background' in caller.db.cg_info.keys():
        return caller.db.cg_info['Background']
    else:
        return ''

def save_bg(caller, buffer):
    "Set the background information"
    caller.db.cg_info['Background'] = buffer
    caller.msg("Background saved")

def quit_bg(caller):
    caller.msg("Exiting Background Editor")
    if caller.ndb.cg_stage:
        caller.ndb.cg_stage += 1
        sleep(1)
        caller.execute_cmd('+charactergen')

def search_stat(caller, statstring):
    results = []
    tempdict = {}
    for section in wodsystem.SEARCHABLE_SECTIONS:
        tempdict.update(caller.attributes.get(section))
    for stat in tempdict.keys():
        if statstring.lower() in stat.lower():
            results.append({'Stat': stat, 'Value': tempdict[stat]})
    return results

def get_stat(caller, stat):
    stats = search_stat(caller, stat)
    if len(results) == 0:
        return None
    elif len(results) > 1:
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

def wod_dice(dice, difficulty=5):
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