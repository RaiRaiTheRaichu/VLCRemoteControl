import vlc

vlcInstance = vlc.Instance()
media_list = vlc.MediaList()
media_list_player = vlc.MediaListPlayer()
media_player = vlcInstance.media_player_new()
media_list_player.set_media_player(media_player)

def set_video_properties():
    media_player.set_fullscreen(True)

set_video_properties()
