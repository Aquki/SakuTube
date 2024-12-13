from yt_dlp import YoutubeDL
from pyglet import media
from os import remove
from io import BytesIO
try:
    remove("tmp.m4a")
except:
    pass
def main():
    while True:
        search = input("Search: ")
        if search == "#q":
            exit()
        else:
            sakutube(search)

#song downloading function
def ytaudio(song_url):
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]',
        'outtmpl': 'tmp.%(ext)s',
        'quiet': True,
        'noplaylist': True,
        'http_chunk_size': 1024 * 1024,  # 1MB chunks
        'retries': 10,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(song_url)

#youtube search
def search_youtube(query, max_results=10):
    query = f"{query}, music"
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'extract_flat': True,
    }

    search_query = f"ytsearch{max_results}:{query}"
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_query, download=False)
        return [
            {
                'title': entry.get('title'),
                'id': entry.get('id')
            }
            for entry in info.get('entries', [])
        ]

def load_into_memory(file_path):
    with open(file_path, 'rb') as data:
        data = BytesIO(data.read())
    remove(file_path)
    return data

#the sound player
def user_player(player, sound):
    player.queue(sound)
    player.play()
    print("Quit=[0], Pause/Play=[1], Mute/Unmute=[2], Replay=[3]")
    try:
        while True:
            user_input = input("control: ")
            if user_input.lower() == '1':
                if player.playing == True:
                    player.pause()
                else:
                    player.play()
            elif user_input.lower() == '2':
                player.volume = 0.0 if player.volume > 0 else 1.0
            elif user_input.lower() == '3':
                player.seek(0)
            elif user_input.lower() == '0':
                player.pause()
                break
            else:
                print("invalid option")
    except Exception as e:
        print(f"Error: {e}")



def sakutube(keyword):
    old_search = False
    old_result = []
    links = []
    while True:
        #search for the keyword that user pass to the function
        try:
            if '#' in keyword:
                keyword, num = keyword.split('#')
                results = search_youtube(keyword, max_results=num)
            else:
                results = search_youtube(keyword)
            #sort the results
            if not old_search:
                for i, result in enumerate(results, 1):
                    links.append(result['id'])
                    old_result.append(f"{i}. {result['title']}")
                    print(f"{i}. {result['title']}")
                    old_search = True
            elif old_search:
                for title in old_result:
                    print(title)
            #choosing the song
            song_num = input("Choose a song: ")
            #if user type [q] return
            if song_num == 'q':
                return
            else:
                url = (f"https://www.youtube.com/watch?v={links[int(song_num)-1]}")
                ytaudio(url)

            #load the song from the tmp.m4a
            m4a_data = load_into_memory("tmp.m4a")
            sound = media.load(filename=None, file=m4a_data, streaming=False)
            player = media.Player()
            user_player(player, sound)

        except IndexError:
            print("This song number dosen't exsist")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()