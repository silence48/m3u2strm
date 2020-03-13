# This Python file uses the following encoding: utf-8
'''
This is a python script to parse an m3u file that has a list of VOD media, and create a folder structure like follows:

/workspace folder
  /groupname
    /title(year)
      /resolution
        title.strm

title.strm is a text file which has the URL to the stream inside of it

the strm files can then be used in your emby media server as defined here:
https://support.emby.media/support/solutions/articles/44001159147-strm-files
additional reference material here:
https://emby.media/community/index.php?/topic/674-media-files-folders-structure/
https://support.emby.media/support/solutions/articles/44001159102-movie-naming
https://support.emby.media/support/solutions/articles/44001159319-library-setup

I plan to do some more work to this at some point, but i just needed something quick n dirty.  

Change the m3u file name to the m3u file you want to use, and root directory is relative to
the working directory which the python script is executed in ...

'''

import os
#this should be the name of your m3u and in the same directory as this python file.
m3ufile = "liveTV.2020.03.12 (1).m3u"
#root directory should be created already, it is where the group folders will be located. relative to the working directory.
rootdirectory = "strms"
#create the strms directory if it does not exist:
if not os.path.exists(rootdirectory):
  os.mkdir(rootdirectory)
    print('Created Streams Directory:', rootdirectory)
  else:
    print('Streams Directory Found', rootdirectory)
m3ulist = open(m3ufile,"r")
streamlist = m3ulist.read()
#parse the file into an array of streams
streams = streamlist.split("#EXTINF:0 ")
#delete the first element of the streams array since it is identifying the m3u file
del streams[0]
mediadictionary = {}
print("streams length", len(streams))
#iterate over all the streams and parse the information for each content into a list, then put that list into the dictionary
for i in range(len(streams)):
#for i in range(50):
  stream = []
  lines = streams[i].split("\n")
  if i+1 != len(streams):
    del lines[3]
  #parse the first line to get the resolution, title, and year
  resolutionandtitle = lines[0].split(",")[1].split(" : ")
  title = ' '.join(resolutionandtitle[1].split(" ")[:-1])
  stream.append(title)
  
  resolution = resolutionandtitle[0]
  stream.append(resolution)

  year = resolutionandtitle[1].split(" ")[-1]
  stream.append(year)

  #get the group name from line 2
  group = lines[1].split("#EXTGRP:")[1]
  stream.append(group)

  #get the URL to the stream from line 3
  link = lines[2]
  stream.append(link)
  #add the stream to the dictionary
  mediadictionary[i] = stream

'''
for media in mediadictionary:
  print(media, mediadictionary[media])
'''
for i in range(len(mediadictionary)):
  md = mediadictionary[i]
  print(md)
  groupdirectory = '/'.join((rootdirectory,md[3]))
  resolution = ""
  if md[1] == "HD":
    resolution = "720p"
  elif md[1] == "SD":
    resolution = "480p"
  else:
    resolution = md[1]
  if md[2] == "":
    md[2] = "null"
  if not os.path.exists(groupdirectory):
    os.mkdir(groupdirectory)
    print('Created Group Directory:', groupdirectory)
  else:
    print('Group Directory Found', groupdirectory)
  if md[3] == "Movie VOD":
    moviewithyear = (md[0] + " (" + md[2] + ")")
    moviedirectory = '/'.join((groupdirectory,moviewithyear))
    filename = moviedirectory + "/" + (" - ".join((moviewithyear, resolution))) + ".strm"
    if not os.path.exists(moviedirectory):
      os.mkdir(moviedirectory)
      print('Created Movie Directory:', moviedirectory)
    else:
      print('Movie Directory Found', moviedirectory)
    if not os.path.exists(filename):
      streamfile = open(filename, "w+")
      streamfile.write(md[4])
      streamfile.close
      print("strm file created:", filename)
      streamfile.close()
    else:
      print("stream file already found")
  else:
    showdirectory = ""
    title = ""
    date = ""
    if list(md[2])[0] == "S" and list(md[2])[3] == "E":
      showdirectory = '/'.join((groupdirectory,md[0]))
      showwithepisode = (md[0] + " (" + md[2] + ")")
      filename = showdirectory + "/" + (" - ".join((showwithepisode, resolution))) + ".strm"
    elif list(md[2])[0] == "S":
      showdirectory = '/'.join((groupdirectory,md[0]))
      showwithepisode = (md[0] + " (" + md[2] + ")")
      filename = showdirectory + "/" + (" - ".join((showwithepisode, resolution))) + ".strm"
    else:
      titlestring = md[0].split(" ")
      title = ""
      date = ""
      vset = False
      for i in range(len(titlestring)):
        if vset == True:
          break
        try:
          int(titlestring[i])
        except:
          if i+1 == len(titlestring):
            showdirectory = '/'.join((groupdirectory,md[0]))
            filename = showdirectory + "/" + (" - -".join((md[0], resolution))) + ".strm"
          continue
        else:
          try:
            int(titlestring[i+1])
          except:
            showdirectory = '/'.join((groupdirectory,md[0]))
            filename = showdirectory + "/" + (" - -".join((md[0], resolution))) + ".strm"
          else:
            if 1900 < int(titlestring[i]) < 2025 and 0 < int(titlestring[i+1]) <= 12 and 0 < int(titlestring[i+2]) <= 31:
              date = "-".join((titlestring[i], titlestring[i+1], titlestring[i+2]))
              title = " ".join(titlestring[:i])
              showdirectory = '/'.join((groupdirectory,title))
              filename = showdirectory + "/" + ("-".join((title,date))) + " - " + resolution + ".strm"
              vset = True
            elif 0 < int(titlestring[i]):
              title = " ".join(titlestring[:i])
              showdirectory = '/'.join((groupdirectory,title))
              filename = showdirectory + "/" + (" - ".join((md[0], resolution))) + ".strm"
              vset = True
            else:
              showdirectory = '/'.join((groupdirectory,md[0]))
              filename = showdirectory + "/" + (" - -".join((md[0], resolution))) + ".strm"
              vset = True
    if not os.path.exists(showdirectory):
      os.mkdir(showdirectory)
      print('Created show Directory:', showdirectory)
    else:
      print('Show Directory Found', showdirectory)
    if not os.path.exists(filename):
      streamfile = open(filename, "w+")
      streamfile.write(md[4])
      streamfile.close
      print("strm file created:", filename)
      streamfile.close()
    else:
      print("stream file already found")
