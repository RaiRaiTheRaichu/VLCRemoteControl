import os

import vlc

import utils
from discord.ext import commands
import vlc_handler

config = utils.FetchConfig('config.jsonc')
ALLOWED_ROLES = config['ALLOWED_ROLES']

command_list = []

@commands.command(name='ping', help='Checks latency with the bot.')
async def ping(ctx):
    await ctx.reply(f'Pong! {round(ctx.bot.latency * 1000)}ms')
command_list.append(ping)

@commands.command(name='add', help='Adds the supplied file to the queue of videos to play.\nArguments: Path to video file on bot host machine, relative to the Videos folder with the bot.')
@utils.CheckPrivilege(ALLOWED_ROLES)
async def add(ctx, file_path: str):
    if not isinstance(file_path, str):
        await ctx.reply(f'Error: The argument provided is not a valid string (surround it with quotation marks if it has a space in it.)')
        return

    file_path = os.path.join('videos', file_path)
    file_path_lower = file_path.casefold()

    if not os.path.exists(file_path_lower):
        await ctx.reply(f'Error: The file "{file_path}" does not exist.\nSearched path: {file_path_lower}.')
        return

    media = vlc_handler.vlcInstance.media_new(file_path)
    vlc_handler.media_list.add_media(media)
    await ctx.reply(f'Added "{file_path}" to the queue.')
command_list.append(add)

@commands.command(
    name='list',
    help='Lists all video files in the Videos folder.'
)
@utils.CheckPrivilege(ALLOWED_ROLES)
async def list(ctx):
    videos_folder = os.path.join(os.path.dirname(__file__), 'videos')

    if os.path.basename(videos_folder).lower() != 'videos':
        await ctx.reply('The Videos folder does not exist.')
        return

    if not os.path.exists(videos_folder):
        await ctx.reply('The Videos folder does not exist.')
        return

    files = os.listdir(videos_folder)
    video_files = [f for f in files if os.path.isfile(os.path.join(videos_folder, f))]

    if not video_files:
        await ctx.reply('There are no video files in the Videos folder.')
        return

    response = "Video files in the Videos folder:\n" + "\n".join(video_files)
    await ctx.reply(response)
command_list.append(list)

@commands.command(name='play', help='Plays assigned media in a new VLC instance.')
@utils.CheckPrivilege(ALLOWED_ROLES)
async def play(ctx):
    if vlc_handler.media_list.count() > 0:
        vlc_handler.media_list_player.set_media_list(vlc_handler.media_list)
        vlc_handler.media_list_player.play()
        await ctx.send('Playing media queue')
    else:
        await ctx.send('No media in queue to play')
command_list.append(play)

@commands.command(name='stop', help='Forcibly closes the VLC instance.')
@utils.CheckPrivilege(ALLOWED_ROLES)
async def stop(ctx):
    if not vlc_handler.media_list_player.is_playing():
        await ctx.reply('Error: VLC player is already not playing.')
        return
    vlc_handler.media_list_player.stop()
    await ctx.reply(f'VLC player closed.')
command_list.append(stop)

@commands.command(name='pause', help='Pauses video playback. Repeat the command to unpause (it\'s a toggle).')
@utils.CheckPrivilege(ALLOWED_ROLES)
async def pause(ctx):
    vlc_handler.media_list_player.pause()
    if vlc_handler.media_list_player.is_paused():
        await ctx.reply(f'VLC player paused!.')
    if not vlc_handler.media_list_player.is_paused():
        await ctx.reply(f'VLC player unpaused!.')
command_list.append(pause)

@commands.command(name='skip', help='Skips the currently playing video.')
@utils.CheckPrivilege(ALLOWED_ROLES)
async def skip(ctx):
    vlc_handler.media_list_player.next()
    vlc_handler.set_video_properties()
    await ctx.send('Skipped to next media in queue')
command_list.append(skip)

@commands.command(name='seek',
                  help='Seek the current video by the specified number of milliseconds (negative values rewind and positive values fast forward).\nExample: \'vlc!seek -5000\' will rewind the video by 5 seconds.')
@utils.CheckPrivilege(ALLOWED_ROLES)
async def seek(ctx, milliseconds: int):
    player = vlc_handler.media_list_player.get_media_player()

    state = player.get_state()
    if state not in [vlc.State.Playing, vlc.State.Paused]:
        await ctx.reply('No video is currently playing.')
        return

    current_time = player.get_time()
    new_time = current_time + milliseconds
    duration = player.get_length()
    new_time = max(0, min(duration, new_time))
    player.set_time(new_time)

    await ctx.reply(f'Set the video time by {milliseconds} milliseconds. Current time: {new_time} ms.')
command_list.append(seek)

@commands.command(name='volume', help='Sets the volume of the current media. Range: 0 to 150.')
@utils.CheckPrivilege(ALLOWED_ROLES)
async def volume(ctx, volume_level: int):
    if volume_level < 0 or volume_level > 150:
        await ctx.reply('Volume level must be between 0 and 150.')
        return

    vlc_handler.media_player.audio_set_volume(volume_level)
    await ctx.reply(f'Set the volume to {volume_level}.')
command_list.append(volume)

@commands.command(name='clear', help='Clears all queued media.')
@utils.CheckPrivilege(ALLOWED_ROLES)
async def clear(ctx):
    vlc_handler.media_list.lock()
    try:
        while vlc_handler.media_list.count() > 0:
            vlc_handler.media_list.remove_index(0)
        await ctx.reply('Media queue cleared.')
    finally:
        vlc_handler.media_list.unlock()
command_list.append(clear)

@commands.command(name='queue', help='Lists all videos in the player queue.')
@utils.CheckPrivilege(ALLOWED_ROLES)
async def list_media(ctx):
    media_items = []
    for i in range(vlc_handler.media_list.count()):
        media = vlc_handler.media_list.item_at_index(i)
        full_path = media.get_mrl()
        filename = os.path.basename(full_path)
        media_items.append(filename)

    if media_items:
        message = '\n'.join(media_items)
        await ctx.reply(f'Current media list:\n{message}')
    else:
        await ctx.reply('The media list is empty.')


command_list.append(list_media)