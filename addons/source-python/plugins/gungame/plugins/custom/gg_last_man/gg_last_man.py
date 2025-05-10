# ../gungame/plugins/custom/gg_last_man/gg_last_man.py

"""Plugin that stops the round from ending until only 1 player remains."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from cvars import ConVar
from entities.entity import Entity
from events import Event
from filters.players import PlayerIter
from listeners.tick import Delay

# GunGame
from gungame.core.status import GunGameRoundStatus, GunGameStatus

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
ignore_round_win = ConVar("mp_ignore_round_win_conditions")
_alive_players = PlayerIter("alive")
_win_conditions = {
    2: 8,
    3: 7,
}


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event("player_death")
def _player_death(game_event):
    """End the round if only 1 player remaining alive."""
    players = list(_alive_players)
    if len(players) > 1:
        return

    ignore_round_win.set_bool(False)
    try:
        team = players[0].team_index
    except IndexError:
        team = None

    Delay(0, _reset_convar, (_win_conditions.get(team, 9),))


def _reset_convar(reason):
    """Verify that the round has not already ended, and end the round."""
    if GunGameStatus.ROUND is GunGameRoundStatus.ACTIVE:
        Entity.find_or_create("info_map_parameters").fire_win_condition(reason)

    Delay(0, ignore_round_win.set_bool, (True,))
