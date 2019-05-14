from evennia.utils import evmenu
import wodsystem
from evennia.utils.ansi import ANSIString
from wodsystem import helper
import itertools

def menu_faction_choose(caller):
    text = helper.wod_header("Choose a Faction")
    current_faction = caller.db.cg_info['Faction'] if 'Faction' in caller.db.cg_info.keys() else 'None'
    text += "\n" + ANSIString("|nYour current Faction is: |w%s" % current_faction).center(width=78, fillchar=" ")
    text += "\n" + helper.wod_header() + "\n\n Choose a faction:"
    factions = helper.get_template_options(caller, wodsystem.FACTIONS_LIST)
    options = []
    if current_faction != 'None':
        options.append({"key": "None", "desc": "Do not change.", "goto": (_set_info, {"name": "Faction", "info": current_faction})})
    for faction in factions:
        options.append({"key": faction, "desc": "Set to '%s'." % faction, "goto": (_set_info, {"name": "Faction", "info": faction})})
    if current_faction != 'None':
        options.append({"key": "Exit", "desc": "Exit the faction menu.", "goto": "exit_menu"})
    return text, options


def exit_menu(caller):
    if caller.ndb.cg_stage:
        caller.ndb.cg_stage += 1
        caller.execute_cmd('+charactergen')

def _set_info(caller, raw_string, **kwargs):
    attribute = kwargs.get("name", "Error")
    value = kwargs.get("info", "Error")
    caller.db.cg_info[attribute] = value
    return ''

def menu_set_pools(caller, raw_string, **kwargs):
    template = kwargs['template'] if 'template' in kwargs.keys() else None
    race_template = helper.get_template_options(caller, template)
    headers = kwargs['template']['Headers'] if 'template' in kwargs.keys() else None
    caller.ndb._menutree.template = template
    caller.ndb._menutree.race_template = race_template
    caller.ndb._menutree.headers = headers
    caller.ndb._menutree.base_stat = kwargs['base_stat'] if 'base_stat' in kwargs.keys() else 0
    caller.ndb._menutree.current_data = kwargs['current_data']
    options = []
    # options.append({"key": "Test", "goto": "test_node"})
    if race_template:
        temp_data = {}
        for key in race_template.keys():
            for subkey in race_template[key]:
                temp_data[subkey] = caller.ndb._menutree.base_stat
        caller.ndb._menutree.temp_data = temp_data
        text = helper.get_cg_data(helper.get_race(caller), template, headers, temp_data)
        keys = race_template.keys()
        for p in itertools.permutations(keys):
            option_list = {}
            desc = ''
            for x in range(0, 3):
                perm_dict = {"Points": kwargs['pools'][x], "MaxPoints": kwargs['pools'][x]}
                option_list[p[x]] = perm_dict
                desc += "%s (|y%s|n)" % (p[x], kwargs['pools'][x])
                desc += ", " if x < 2 else ""
            options.append({"desc": desc, "goto": ("menu_select_group", {"option_list": option_list})})
            # text += str(p)
    return text, options

def get_remaining_points(option_list):
    pointsleft = 0
    for group in option_list.keys():
        pointsleft += option_list[group]['Points']
    return pointsleft

def menu_select_group(caller, raw_string, **kwargs):
    if 'option_list' in kwargs.keys():
        caller.ndb._menutree.option_list = kwargs['option_list']
    option_list = caller.ndb._menutree.option_list
    pointsleft = get_remaining_points(option_list)
    text = helper.get_cg_data(helper.get_race(caller), caller.ndb._menutree.template, caller.ndb._menutree.headers, caller.ndb._menutree.temp_data)
    options = []
    for key_dict in option_list.keys():
        options.append({"desc": '%s (|y%s points to spend.|n)' % (key_dict, option_list[key_dict]['Points']), "goto": ("menu_select_stat", {'Group': key_dict})})
    if pointsleft:
        options.append({"key": (">", "accept", "continue"), "desc": "Accept these stats. |rWARNING|n: You still have |y%d|n unspent points" % pointsleft, "goto": "menu_confirm_accept"})
    else:
        options.append({"key": (">", "accept", "continue"), "desc": "Accept these stats.", "goto": "menu_accept_stats"})
    return text, options

def menu_select_stat(caller, raw_string, **kwargs):
    option_list = caller.ndb._menutree.option_list
    text = str(helper.get_cg_data(helper.get_race(caller), caller.ndb._menutree.template, caller.ndb._menutree.headers, caller.ndb._menutree.temp_data, highlight_column=kwargs['Group']))
    points = option_list[kwargs['Group']]['Points']
    pointsleft = get_remaining_points(option_list)
    text += '\n|y%d|n points left to spend in this group.' % points
    options = []
    for stat in caller.ndb._menutree.race_template[kwargs['Group']]:
        options.append({"desc": stat, "goto": ("menu_adjust_stat", {'Stat': stat, 'Group': kwargs['Group']})})
    options.append({"key": ("<", "back"), "desc": "Go back to Group Selection", "goto": "menu_select_group"})
    if not pointsleft:
        options.append({"key": (">", "accept", "continue"), "desc": "Accept these stats.", "goto": "menu_accept_stats"})
    return text, options

def menu_adjust_stat(caller, raw_string, **kwargs):
    option_list = caller.ndb._menutree.option_list
    text = str(helper.get_cg_data(helper.get_race(caller), caller.ndb._menutree.template, caller.ndb._menutree.headers, caller.ndb._menutree.temp_data, highlight_stat=kwargs['Stat']))
    options = []
    pointsleft = get_remaining_points(option_list)
    stat = kwargs['Stat']
    points = option_list[kwargs['Group']]['Points']
    text += '\n|y%d|n points left to spend in this group.' % points
    maxpoints = option_list[kwargs['Group']]['MaxPoints']
    if (points > 0 and caller.ndb._menutree.temp_data[stat] < 4) or (points > 1 and caller.ndb._menutree.temp_data[stat] < 5):
        cost = 1
        if caller.ndb._menutree.temp_data[stat] >= 4:
            cost = 2
        desc = 'Increment %s by |yone|n point (Cost: |y%d|n)' % (kwargs['Stat'], cost)
        options.append({"key": ("+", "add", "increment"), "desc": desc, "goto": (_adjust_stat, {'Stat': stat, 'Amount': 1, 'Cost': cost, 'Group': kwargs['Group']})})
    if (points <= maxpoints and caller.ndb._menutree.temp_data[stat] > caller.ndb._menutree.base_stat):
        cost = -1
        if caller.ndb._menutree.temp_data[stat] >= 5:
            cost = -2
        desc = 'Decrement %s by |yone|n point (Refund |y%d|n)' % (kwargs['Stat'], cost)
        options.append({"key": ("-", "subtract", "sub", "dec", "decrement"), "desc": desc, "goto": (_adjust_stat, {'Stat': stat, 'Amount': -1, 'Cost': cost, 'Group': kwargs['Group']})})
    options.append({"key": ("<", "back"), "desc": "Go back to Stat Selection", "goto": ("menu_select_stat", {'Stat': stat, 'Group': kwargs['Group']})})
    if not pointsleft:
        options.append({"key": (">", "accept", "continue"), "desc": "Accept these stats.", "goto": "menu_accept_stats"})
    return text, options

def _adjust_stat(caller, raw_string, **kwargs):
    caller.ndb._menutree.temp_data[kwargs['Stat']] += kwargs['Amount']
    caller.ndb._menutree.option_list[kwargs['Group']]['Points'] -= kwargs['Cost']
    return None, {'Stat': kwargs['Stat'], 'Group': kwargs['Group']}

def menu_confirm_accept(caller, raw_string, **kwargs):
    option_list = caller.ndb._menutree.option_list
    pointsleft = get_remaining_points(option_list)
    text = str(helper.get_cg_data(helper.get_race(caller), caller.ndb._menutree.template, caller.ndb._menutree.headers, caller.ndb._menutree.temp_data))
    text += "\n\nAre you sure?  You still have |y%d|n points remaining to spend." % pointsleft
    options = []
    options.append({"key": ("yes", "y"), "goto": "menu_accept_stats"})
    options.append({"key": ("no", "n", "back", "quit", "exit"), "goto": "menu_select_group"})
    return text, options

def menu_accept_stats(caller, raw_string, **kwargs):
    caller.attributes.add(caller.ndb._menutree.current_data, caller.ndb._menutree.temp_data)
