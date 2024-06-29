
from evennia.commands.default.building import CmdObjects
from evennia import default_cmds, Command
from evennia.commands.default.muxcommand import MuxCommand
from evennia.utils import evmenu
from wodsystem import menu
from wodsystem import helper
import wodsystem

class MyCmdObjects(CmdObjects):
    """
    This removes the alias @stats from @objects command so we can use it for the chargen system.
    """
    aliases = ["@listobjects", "@listobjs", "@db"]

"""
----------------------------------------------------------------------------
CHARGEN COMMANDS START HERE
----------------------------------------------------------------------------
"""

class CmdStats(Command):
    """
    View your character sheet.

    Usage:
      +stats [character]

    Show the character sheet for your character.  [character] may be
    specified by judges and staff members.
    """

    key = "+stats"
    help_category = "World of Darkness"
    locks = "cmd:all();others:perm(Helper) or perm(cg_view_others)"


    def func(self):
        """
        This performs the actual command.
        """
        if self.args:
            target = self.caller.search(self.args)
        else:
            target = self.caller
        if not target:
            return
        if not self.access(self.caller, 'others') and not target == self.caller:
            self.caller.msg("You can't view other player's sheets.")
            return
        sheet = helper.get_sheet(target)
        self.caller.msg(sheet)


class CmdRaces(Command):
    key = "+races"
    def func(self):
        self.caller.msg(wodsystem.RACE_LIST)

class CmdBackground(Command):
    """
    View your background.

    Usage:
      +background [character]

    Show the background for your character.  [character] may be
    specified by judges and staff members.
    """

    key = "+background"
    help_category = "World of Darkness"
    locks = "cmd:all();others:perm(Helper) or perm(cg_view_others)"


    def func(self):
        """
        This performs the actual command.
        """
        if self.args:
            target = self.caller.search(self.args)
        else:
            target = self.caller
        if not target:
            return
        if not self.access(self.caller, 'others') and not target == self.caller:
            self.caller.msg("You can't view other player's backgrounds.")
            return
        bg = helper.load_bg(target)
        self.caller.msg(bg)


class CmdChargen(Command):
    """
    Start (or continue) character generation.

    Usage:
    +chargen

    Takes you through character generation, step by step.  There are ten steps.
        1. Background
        2. Faction
        3. Attributes
        4. Skills
        5. Template (for games that have supernatural races)
        6. Advantages (Calculated from Attributes and Skills, mostly)
        7. Virtue
        8. Vice
        9. Merits
        10. Flaw
    """

    key = "+chargen"
    aliases = ["+cg", "+charactergen"]
    help_category = "World of Darkness"
    locks = 'cmd:NOT attr(cg_chargenfinished)'

    def func(self):
        """
        Start the process
        """
        evmenu.EvMenu(self.caller, "wodsystem.menu", startnode="menu_chargen", cmd_on_exit=None)
        # if self.caller.ndb.cg_stage:
        #     pass
        # else:
        #     self.caller.ndb.cg_stage = 1
        # if self.caller.ndb.cg_stage == 1:
        #     helper.background_edit(self.caller)
        # if self.caller.ndb.cg_stage == 2:
        #     evmenu.EvMenu(self.caller, "wodsystem.menu", startnode="menu_faction_choose")
        # if self.caller.ndb.cg_stage == 3:
        #     evmenu.EvMenu(self.caller,
        #                   "wodsystem.menu",
        #                   startnode="menu_set_pools",
        #                   startnode_input=("",
        #                                    {"template": wodsystem.ATTRIBUTE_LIST,
        #                                     "pools": self.caller.db.cg_creationpools['Attributes'],
        #                                     "current_data": 'cg_attributes',
        #                                     "base_stat": 1}))
        # if self.caller.ndb.cg_stage == 4:
        #     evmenu.EvMenu(self.caller,
        #                   "wodsystem.menu",
        #                   startnode="menu_set_pools",
        #                   startnode_input=("",
        #                                    {"template": wodsystem.SKILL_LIST,
        #                                     "pools": self.caller.db.cg_creationpools['Skills'],
        #                                     "current_data": 'cg_skills',
        #                                     "base_stat": 0}))


class CmdStatReveal(MuxCommand):
    '''
    Reveal a stat value to the room (or, optionally, an individual).

    Usage: +statreveal <stat>[=<target>]
    '''
    key = "+statreveal"
    help_category = "World of Darkness"
    locks = 'cmd:attr(cg_chargenfinished)'

    def func(self):
        target = None
        if self.rhs:
            target = self.caller.search(self.rhs)
            if not target:
                self.caller.msg("Could not find '%s', please try again" % self.rhs)
                return
        if not self.lhs:
            self.caller.msg("What stat are you trying to show?")
            return
        else:
            stat = helper.search_stat(self.caller, self.lhs)
            if len(stat) == 0:
                self.caller.msg("You don't seem to have that stat.")
            elif len(stat) > 1:
                self.caller.msg(helper.search_stat_disambiguation(stat))
            else:
                returnstring="|ySTATS|n: %s reveals their %s value: |y%d|n" % (self.caller.name, stat[0]['Stat'], stat[0]['Value'])
                if target:
                    returnstring += " (Privately sent to %s)" % target.name
                    target.msg(returnstring)
                    self.caller.msg(returnstring)
                else:
                    self.caller.location.msg_contents(returnstring)


class CmdRoll(MuxCommand):
    '''
    Roll a dice pool against a target difficulty, either privately or to the room.

    Usage:  +roll <dice string> [=[<difficulty>][/<target>]]

    Dice string can be a single number, a stat (like Strength or Intelligence) or
    a simple addition/subtraction math equation (Strength + Dexterity + 2) or
    (Intelligence + Wits - 1)

    Difficulty is a target number (integer) that you must roll for a die to count
    as a "Success".
    Target is used if you want to privately send the results to  a player.  'me'
    works here too.

    While you may roll X dice, the system may add to those dice.  Every time you
    roll one or more 10, the system will reroll that many dice, adding successes,
    and rerolling 10s again.

    Results will be sent to the whole room, or <target>, if specified.
    '''

    key = '+roll'
    help_category = "World of Darkness"
    locks = 'cmd:attr(cg_chargenfinished)'

    def func(self):
        # results = helper.wod_dice(10, 7)
        success, dice, dicestring = helper.parse_dicestring(self.caller, self.lhs)
        if success:
            # self.caller.msg('Dice: %s' % dice)
            # self.caller.msg('String: %s' % dicestring)
            difficulty = None
            target = None
            if self.rhs:
                success, target, difficulty, msg = helper.parse_dicestring_rhs(self.caller, self.rhs)
                # if success:
                #    self.caller.msg('Target: %s' % target)
                #    self.caller.msg('Difficulty: %s' % difficulty)
                # else:
                #    self.caller.msg('Target Error: %s' % msg)
                #    self.caller.msg('Difficulty: %s' % difficulty)
            if dice:
                if difficulty:
                    dice_result = helper.wod_dice(dice, difficulty)
                else:
                    dice_result = helper.wod_dice(dice)
                dice_result_string = '|yDICE|n: %s rolled %s (%d), difficulty %d. \n|yDICE|n: Successes: |y%d|n' % (self.caller.name, dicestring, dice, dice_result['Difficulty'], dice_result['Successes'])
                for resultset in dice_result['Results']:
                    resultlist = []
                    for die in sorted(resultset):
                        diestring = str(die)
                        if die < dice_result['Difficulty']:
                            diestring = '|R%s|n' % diestring
                        elif die == 10:
                            diestring = '|y%s|n' % diestring
                        else:
                            diestring = '|Y%s|n' % diestring
                        resultlist.append(diestring)
                    dice_result_string += '\n|yDICE|n: Roll Result: %s' % resultlist
                if target:
                    msg = '%s \n|yDICE|n: Sent privately to %s' % (dice_result_string, target.name)
                    messagelist = list(dict.fromkeys([self.caller, target]))
                    for temptarg in messagelist:
                        temptarg.msg(msg)
                else:
                    self.caller.location.msg_contents(dice_result_string)
        else:
            self.caller.msg(dice)


"""
----------------------------------------------------------------------------
IN-GAME COMMANDS START HERE
----------------------------------------------------------------------------
"""



"""
----------------------------------------------------------------------------
COMMANDSETS START HERE
----------------------------------------------------------------------------
"""

class WodSystemCmdSet(default_cmds.CharacterCmdSet):
    """
    This command set includes all the commands used by the WoD System
    """

    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        """
        Populate the cmdset
        """
        self.add(MyCmdObjects)
        self.add(CmdStats)
        self.add(CmdChargen)
        self.add(CmdBackground)
        self.add(CmdStatReveal)
        self.add(CmdRoll)
        self.add(CmdRaces)
