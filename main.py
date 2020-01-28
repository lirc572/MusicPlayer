#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 12:55:40 2020

@author: rochor
"""

import json
import requests
import vlc
import sys
class MusicClient:
    _music_server = "https://music.163.com/song/media/outer/url?id="
    #music_server2 = "https://5akk68wdz8qnp.cfc-execute.bj.baidubce.com/music/"
    _playlists_file = "playlists.json"
    _playlists = {}
    def __init__(self, server="", playlists=""):
        self._music_server = server if server else self._music_server
        self._playlists_file = playlists if playlists else self._playlists_file
        with open(self._playlists_file) as pl:
            self._playlists = json.load(pl)
    def setServer(self, server):
        self._music_server = server
        return 0 #Successful
    def getServer(self):
        return self._music_server
    def getMusicURL(self, music_id):
        return self._music_server + music_id + ".mp3"
    def getPlaylists(self):
        return list(self._playlists.keys())
    def newPlaylist(self, playlist_name):
        self._playlists[playlist_name] = []
        return 0 #Successful
    def deleteFromPlaylist(self, music_id, playlist_name):
        if playlist_name not in self._playlists:
            return -1 #Playlist not found
        for m in range(len(self._playlists[playlist_name])):
            if self._playlists[playlist_name][m]["id"] == music_id:
                self._playlists[playlist_name].pop(m)
                return 0 #Successful
        return -1 #Music not found
    def addToPlaylist(self, music, playlist_name):
        if "id" not in music:
            return -1 #Wrong format of music
        if playlist_name not in self._playlists:
            return -2 #Playlist not found
        for m in range(len(self._playlists[playlist_name])):
            if self._playlists[playlist_name][m]["id"] == music["id"]:
                return -3 #Music already in playlist
        self._playlists[playlist_name].append(music)
        return 0
    def deletePlaylist(self, playlist_name):
        if playlist_name in self._playlists:
            del self._playlists[playlist_name]
            return 0
        else:
            return -1 #Playlist not found
    def searchMusic(self, keywords):
        url = "http://erosion572.com:3000/search?keywords=" + keywords
        res = json.loads(requests.get(url).text)
        if res["code"] == 200:
            return res["result"]["songs"]
        else:
            return -1 #GET error
    def musicPlayer(self, id):
        return vlc.MediaPlayer(self._music_server + id)
    def main(self):
        print("Welcome to Netease Cloud Music CLI!")
        print("Enter commands below (enter help to show helps)")
        current_player = 0
        while True:
            try:
                cmd = input()
                if cmd == "help":
                    print("Please read the source code (skip to main method of class MusicClient")
                elif cmd == "play":
                    current_player.play()
                elif cmd == "pause":
                    current_player.pause()
                elif cmd == "stop":
                    current_player.stop()
                elif cmd.split()[0] == "load":
                    current_player = self.musicPlayer(cmd.split()[1])
                    print("Done!")
                elif cmd.split()[0] == "search":
                    songs = self.searchMusic(cmd[7:])
                    for song in songs:
                        song_text = song["name"] + "    "
                        for artist in song["artists"]:
                            song_text += artist["name"] + " "
                        song_text += "   " + song["album"]["name"] + "\n"
                        song_text += "  " + str(song["id"])
                        print(song_text)
                elif cmd == "exit" or cmd == "quit":
                    return 0
                print()
            except KeyboardInterrupt:
                raise
            except:
                print("Something went wrong: " + str(sys.exc_info()[0]) + "\n")
    '''More functions to implement...
    def searchArtist(self, keywords):
        url = "https://music.163.com/#/search/m/?s=" + keywords + "&type=100"
    def searchAlbum(self, keywords):
        url = "https://music.163.com/#/search/m/?s=" + keywords + "&type=10"
    def searchVideo(self, keywords):
        url = "https://music.163.com/#/search/m/?s=" + keywords + "&type=1014"
    def searchLyrics(self, keywords):
        url = "https://music.163.com/#/search/m/?s=" + keywords + "&type=1006"
    def searchPlaylist(self, keywords):
        url = "https://music.163.com/#/search/m/?s=" + keywords + "&type=1000"
    '''
if __name__ == "__main__":
    MC = MusicClient("https://5akk68wdz8qnp.cfc-execute.bj.baidubce.com/music/")
    MC.main()