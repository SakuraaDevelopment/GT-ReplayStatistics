import sys
import os
import json
import tkinter as tk

print(
    f"-----   Starting   -----\n"
    f"Python executable: {sys.executable} \n"
    f"Python version: {sys.version} \n"
    f"------------------------"
)

root = tk.Tk()
root.title("Replay statistics")
root.geometry("300x200")
root.resizable(False, False)

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

label = tk.Label(frame, text="enter the path to your replay file (.txt) below")
label.pack(fill=tk.BOTH, expand=True)

entry = tk.Entry(frame, width=30)
entry.pack(fill=tk.BOTH, expand=True)


def start(replay_json):
    frame2 = tk.Frame(root)
    frame2.pack(fill=tk.BOTH, expand=True)
    button.destroy()
    entry.destroy()
    label.destroy()
    frame.pack_forget()
    print("creating new gui")
    player_tags = []
    for player_json in replay_json["players"]:
        actor_num = player_json["actornumber"]
        print(f"getting tags for player {actor_num}")
        user_tags = 0
        for playerdata in replay_json["playerDatas"]:
            if playerdata["actorNumber"] == actor_num:
                user_tags = int(playerdata["taggedLen"])
                break
        player_tags.append([user_tags, actor_num])
    player_tags.sort(reverse=True)
    leaderboard = tk.Label(frame2, text="Tagging Leaderboard")
    leaderboard.pack(fill=tk.BOTH, expand=True)
    player_count = 0
    for player in player_tags:
        player_count += 1
        player_actor_num = player[1]
        player_tags = round(player[0]/3)
        player_name = ""
        for player_json in replay_json["players"]:
            if player_json["actornumber"] == player_actor_num:
                player_name = player_json["Name"]
                break
        player_label = tk.Label(frame2, text=f"{player_name}: {player_tags} tags")
        player_label.pack(fill=tk.BOTH, expand=True)
    root.geometry("300x" + str(200 + (player_count * 20)))


def start_button():
    path = entry.get()
    if os.path.exists(path):
        with open(path, "r") as file:
            if not file.readable():
                print(f"the file {path} is not readable")
                return
            replay_json = json.load(file)
            try:
                str_1481984 = replay_json["FormatVersion"]
                if str_1481984 is None:
                    print("FormatVersion is not in the json")
                    raise Exception
            except Exception:
                print(f"the file {path} is not a valid replay file (json)")
                return
            start(replay_json)
    else:
        print(f"the path {path} does not exist")
    print("starting...")


button = tk.Button(frame, text="start", command=start_button, bg="blue", fg="white")
button.pack(fill=tk.BOTH, expand=True)

root.mainloop()
