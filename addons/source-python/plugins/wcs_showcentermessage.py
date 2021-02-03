# Source.Python
from events.manager import game_event_manager
from players.entity import Player
from players.helpers import userid_from_index
from commands import CommandReturn
from commands.typed import TypedServerCommand 


@TypedServerCommand('wcs_showcentermessage')
def wcs_spawn_death_command(command_info, userid:int=0, message:str="",red:int=255,green:int=255,blue:int=255,duration:float=2.0):
    if userid == 0:
        return
    else:
        player = Player.from_userid(userid)
        index = player.index
    hex_color = '#{:02x}{:02x}{:02x}'.format(red, green, blue)
    send_win_message(
        message='<font color="%s">%s</font>' % (hex_color,message),
        recipients=(index,)
    )
    
    if duration > 0.0:
        player.delay(duration,send_win_message,("", (index,)))
    
    return CommandReturn.BLOCK

def send_win_message(message='', recipients=None):
    event = game_event_manager.create_event('cs_win_panel_round')
    event.set_string('funfact_token', message)

    if recipients is None:
        game_event_manager.fire_event(event)

    else:
        for index in recipients:
            try:
                # Try to get a Player instance.
                Player(index).base_client.fire_game_event(event)
            except ValueError:
                continue
        game_event_manager.free_event(event)
