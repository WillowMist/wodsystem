
from evennia.commands.default.system import CmdObjects
from evennia import default_cmds, Command
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
    help_category = "wod"
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

class CmdBackground(Command):
    """
    View your background.

    Usage:
      +background [character]

    Show the background for your character.  [character] may be
    specified by judges and staff members.
    """

    key = "+background"
    help_category = "wod"
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
    help_category = "wod"
    locks = 'cmd:NOT attr(cg_chargenfinished)'

    def func(self):
        """
        Start the process
        """
        if self.caller.ndb.cg_stage:
            pass
        else:
            self.caller.ndb.cg_stage = 1
        if self.caller.ndb.cg_stage == 1:
            helper.background_edit(self.caller)
        if self.caller.ndb.cg_stage == 2:
            evmenu.EvMenu(self.caller, "wodsystem.menu", startnode="menu_faction_choose")
        if self.caller.ndb.cg_stage == 3:
            evmenu.EvMenu(self.caller,
                          "wodsystem.menu",
                          startnode="menu_set_pools",
                          startnode_input=("",
                                           {"template": wodsystem.ATTRIBUTE_LIST,
                                            "pools": self.caller.db.cg_creationpools['Attributes'],
                                            "current_data": 'cg_attributes',
                                            "base_stat": 1}))
        if self.caller.ndb.cg_stage == 4:
            evmenu.EvMenu(self.caller,
                          "wodsystem.menu",
                          startnode="menu_set_pools",
                          startnode_input=("",
                                           {"template": wodsystem.SKILL_LIST,
                                            "pools": self.caller.db.cg_creationpools['Skills'],
                                            "current_data": 'cg_skills',
                                            "base_stat": 0}))


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
