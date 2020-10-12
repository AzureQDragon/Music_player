#Music Player
#3/6/20
#Music Player that can load in files from a text file and play them

import pygame
from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk

# Initialize global linked List
class LinkedListNode:
    
    def __init__(self, myPrev, myData, myNext):
        #Construct a new Linked List Node
        self.data = myData
        self.next = myNext
        self.prev = myPrev
        return

# Initialize Music class
class Music:
    def __init__(self, song, artist, album, album_cover, file):
        self.song = song # Song name
        self.artist = artist # Name of artist
        self.album = album # Name of album
        self.album_cover = album_cover # Album cover path
        self.file = file # File path
        return

    # Getters for each parameter
    def getSong(self):
        return self.song

    def getArtist(self):
        return self.artist

    def getAlbum(self):
        return self.album

    def getAlbumCover(self):
        return self.album_cover

    def getFile(self):
        return self.file

# Linked List class
class LinkedList:

    def __init__(self):
        #Construct a new LinkedList. The first node and last node are the same. Size is 0        self.firstNode = LinkedListNode(None, None)
        self.firstNode = None #LinkedListNode(None, None)
        self.lastNode = self.firstNode
        self.size = 0
        self.currentNode = self.firstNode
        return

    def addToRear(self, data):
        #Add a node to the list
        node = LinkedListNode(None, data, self.firstNode)
        self.currentNode = self.firstNode
        if self.firstNode == None: #.data == None:
            self.firstNode = node
            self.lastNode = node
        else:
            self.lastNode.next = node
            node.prev = self.lastNode
            self.lastNode = node
            self.lastNode.next = self.firstNode
            self.firstNode.prev = self.lastNode

        self.size += 1
        return
    
    # Moves current node to the next node
    def next (self):
        self.currentNode = self.currentNode.next
        return self.currentNode.data

    # Moves current node to previous node
    def prev (self):
        self.currentNode = self.currentNode.prev
        return self.currentNode.data    

# Master linked list for music
MusicPlayList = LinkedList()

# Loads music player with music provided in text file
def loadLinkedList():
    file = open("data.txt", "r")
    line = file.readline()
    while(line != ""):
        newMusic = line.split(",")
        nsplit = line.split("\n")
        for i in range(len(newMusic)):
            newMusic[i] = newMusic[i].strip("\n")
        tempMusic = Music(newMusic[0], newMusic[1], newMusic[2], newMusic[3], newMusic[4])
        MusicPlayList.addToRear(tempMusic)
        line = file.readline()
    return
    
# Load the linked list
loadLinkedList()

# Plays or pauses the song depending on the current status
def playsong():
    global pausing, playbutton, playing

    # If player is currently playing when button is pressed, then pause
    if(isPlaying.get() == "Playing"):
        pygame.mixer.music.pause()
        isPlaying.set("Paused")
        playbutton["image"] = playing
    
    # If player is currently paused when button is pressed, then unpause
    elif(isPlaying.get() == "Paused"):
        pygame.mixer.music.unpause()
        isPlaying.set("Playing")
        playbutton["image"] = pausing
    
    # Else if stopped, then play
    else:
        pygame.mixer.music.play()
        isPlaying.set("Playing")
        playbutton["image"] = pausing
    return

# Start to play song without toggling for when skipping
def startplaysong():
    isPlaying.set("Playing")
    pygame.mixer.music.play()
    return

# Stops the song entirely and resets position
def stopsong():
    global isPlaying, playbutton, playing
    pygame.mixer.music.stop()
    isPlaying.set("Stopped")
    playbutton["image"] = playing
    return

# Find song by name and play
def playsongby(song):
    songNotFound = True

    while songNotFound: # While the song is not found
        if(song == MusicPlayList.next().getSong()): # If the song is found then play next song
            nextsong()
            prevsong()
            songNotFound = False
            startplaysong()
        else: # Else skip to next song
            nextsong()
    return

# Moves player to next song
def nextsong():
    global img, Song, Album, Artist
    nextdata = MusicPlayList.next()

    # Retrieves file path and loads album cover
    songfile = "Music\\" + nextdata.getFile()
    pygame.mixer.music.load(songfile)
    img = ImageTk.PhotoImage(Image.open("Music\\" + nextdata.getAlbumCover()))   
    canvas.itemconfig(imgcanvas, image = img) 

    # Change Labels
    Song["text"] = "Song: " + nextdata.getSong()
    Album["text"] = "Album: " + nextdata.getAlbum()
    Artist["text"] = "Artist: " + nextdata.getArtist()

    # Start to play song
    startplaysong()
    return


def prevsong():
    global img, Song, Album, Artist

    # Retrieves file path and loads album cover
    prevdata = MusicPlayList.prev()
    songfile = "Music\\" + prevdata.getFile()
    pygame.mixer.music.load(songfile)
    img = ImageTk.PhotoImage(Image.open("Music\\" + prevdata.getAlbumCover()))  
    canvas.itemconfig(imgcanvas, image = img)

    # Updates Labels
    Song["text"] = "Song: " + prevdata.getSong()
    Album["text"] = "Album: " + prevdata.getAlbum()
    Artist["text"] = "Artist: " + prevdata.getArtist()
    startplaysong()
    return

# Finds the searched items in the entrybox
def search():
    global returnlist, searchFrame

    # Destroys any previous items searched
    for widget in searchFrame.winfo_children():
        widget.destroy()

    # Stores returned items in a list
    returnlist = []
    tempList = MusicPlayList

    # Search by Song name
    if searchOption.get() == "Song":
        for i in range(tempList.size):
            data = tempList.next()
            if(searchVar.get().lower() in data.getSong().lower()):
                returnlist.append(data)

    # Search by Artist name
    elif searchOption.get() == "Artist":
        for i in range(tempList.size):
            data = tempList.next()
            if(searchVar.get().lower() in data.getArtist().lower()):
                returnlist.append(data)

    # Search by Album name
    else:
        for i in range(tempList.size):
            data = tempList.next()
            if(searchVar.get().lower() in data.getAlbum().lower()):
                returnlist.append(data)
                print(data.getArtist)
    
    # For each item added to the return list
    for i in range(len(returnlist)):
        action = lambda x = returnlist[i].getSong() : playsongby(x)
        Button(searchFrame, image=playing, borderwidth=0,command=action).grid(column = 0, row=2+i) # Create a button that will play the selected song
        Label(searchFrame, text="Song: " + returnlist[i].getSong() + " Artist: " + returnlist[i].getArtist()).grid(column=1, row=2+i) # Create a corresponding label
    return

pygame.mixer.init() # Initialize pygame music player

# Initialize playing of the first song
tempMusic = MusicPlayList.next() 
songfile = "Music\\" + tempMusic.getFile()
pygame.mixer.music.load(songfile)

# Intialize tkinter window
root =Tk()
root.geometry("900x450")
root.title('Media Player')
searchFrame = Frame(root)

# Initialize global variables
returnlist = []
isPlaying = StringVar()
isPlaying.set("Stopped")
searchVar = StringVar()
searchOption = StringVar()

# Create canvas for album cover
canvas = Canvas(root, width=300, height=300)
canvas.grid(columnspan = 5, rowspan = 5)
img = ImageTk.PhotoImage(Image.open("Music\\" + tempMusic.getAlbumCover()))      
imgcanvas = canvas.create_image(20,20, anchor=NW, image=img) 

# Create labels for the corresponding song
Song = Label(root, text= "Song: " + tempMusic.getSong())
Album = Label(root, text="Album: " + tempMusic.getAlbum()) 
Artist = Label(root, text = "Artist: " + tempMusic.getArtist())

# Load in icons for each button
playing = ImageTk.PhotoImage(Image.open("Music\\iconplay.png").resize((32,32), Image.ANTIALIAS))
pausing = ImageTk.PhotoImage(Image.open("Music\\iconpause.png").resize((32,32), Image.ANTIALIAS))
stop = ImageTk.PhotoImage(Image.open("Music\\iconstop.png").resize((32,32), Image.ANTIALIAS))
skipnext = ImageTk.PhotoImage(Image.open("Music\\next.png").resize((32,32), Image.ANTIALIAS))
previous = ImageTk.PhotoImage(Image.open("Music\\prev.png").resize((32,32), Image.ANTIALIAS))

# Create buttons for playing stopping and skipping along with searching
playbutton = Button(root, text='Play', borderwidth=0, image= playing, command = playsong)
Button(root, text='Stop', borderwidth=0, image = stop, command = stopsong).grid(row=9, column =3, padx=20)
Button(root, text = "Next",borderwidth=0, image=skipnext, command = nextsong).grid(row =9, column = 2, padx=20)
Button(root, text = "Prev",borderwidth=0, image=previous, command = prevsong).grid(row=9, column = 0, padx = 20)
SearchButton = Button(root, text="Search", command=search)
combo = ttk.Combobox(root, textvariable=searchOption, values=["Artist", "Song", "Album"], state="readonly")
Entry = ttk.Entry(root, textvariable=searchVar)
Label(root, text ="Search By: ").grid(column=6, row = 0, sticky=N, pady=10) #Label for search

# Gridding all items
Song.grid(columnspan=5, row = 6)
Album.grid(columnspan = 5, row = 7)
Artist.grid(columnspan=5, row = 8)
playbutton.grid(row = 9, column = 1)
Entry.grid(column=8, row=0, sticky=N, pady=10, padx=10)
SearchButton.grid(column=9,row=0,sticky=N, pady=10)
combo.grid(column=7, row=0, sticky=N, pady=10)
searchFrame.grid(column=7, columnspan = 7, row=1)

# Play starting song on start
playsong()

root.mainloop() # tkinter mainloop
