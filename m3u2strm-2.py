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
m3ufile = "test3.m3u"
#root directory should be created already, it is where the group folders will be located. relative to the working directory.
rootdirectory = "strms"

m3ulist = open(m3ufile,"r")
streamlist = m3ulist.read()
mediadictionary = {}
#parse the file into an array of streams
streams = streamlist.split("#EXTINF:")
del streams[0]
#delete the first element of the streams array since it is identifying the m3u file
for i in range(len(streams)):
#for i in range(50):
  stream = []
  case = ""
  lines = streams[i].split("\n")
  if i+1 != len(streams):
    del lines[2]
  '''for line in lines:
    print(line, "lon", i)'''
  line1 = lines[0].split(",")
  del line1[0]
  info = line1[0].split("|")
  stream.append(info[1]) #language
  if len(info) > 3:
    case = "tv"
  else:
    case = "movie"
  #for movie the stream structure is [language, title, streamlink]
  if case == "movie":
    title = info[2].split(" ")
    del title[0]
    del title[-1]
    stream.append("Movie")
    stream.append(' '.join(title))
    stream.append(lines[1])
  
  #for tv the stream structure is [language, seriesname, seriesnumber, episodenumber, episodetitle]
  if case == "tv":
    stream.append("TV")
    seriesinfo = info[2].split(" ")
    withepisodename = False
    del seriesinfo[0]
    del seriesinfo[-1]
    if seriesinfo[-1][0] == "S":
      stream.append(" ".join(seriesinfo[0:-1]))
      stream.append("".join([seriesinfo[-1][1], seriesinfo[-1][2]]))
    else:
      stream.append("".join([seriesinfo[0:-1]]))
      stream.append("")
    episodeinfo = info[-1].split(" ")
    del episodeinfo[0]
    for j in range(len(episodeinfo)):
      try:
        int(episodeinfo[j][0])
        int(episodeinfo[j][1])
        int(episodeinfo[j][3])
        int(episodeinfo[j][4])
      except:
        if episodeinfo[j] == "-":
          withepisodename = True
        else:
          if withepisodename == True:
            continue
          else:
            withepisodename = False
      else:
        stream.append("".join([episodeinfo[j][3], episodeinfo[j][4]]))
    if withepisodename == True:
      episode = list(info[-1].split("-")[-1])
      del episode[0]
      stream.append("".join(episode))
    else:
      stream.append("")
  stream.append(lines[1])
  mediadictionary[i] = stream
for i in range(len(mediadictionary)):
  md = mediadictionary[i]
  #print(md)
  typedirectory = md[1]
  language = md[0]
  url = md[-1]
  if not os.path.exists(typedirectory):
    os.mkdir(typedirectory)
    print('Created Type Directory:', typedirectory)
  else:
    print('Type Directory Found', typedirectory)
  if typedirectory == "Movie":
    title = md[2]
    moviedirectory = '/'.join((typedirectory,title))
    filename = moviedirectory + "/" + title + " - [" + language + "]" + ".strm"
    print(filename)
    if not os.path.exists(moviedirectory):
      os.mkdir(moviedirectory)
      print('Created Movie Directory:', moviedirectory)
    else:
      print('Movie Directory Found', moviedirectory)
    if not os.path.exists(filename):
      streamfile = open(filename, "w+")
      streamfile.write(url)
      streamfile.close
      print("strm file created:", filename)
      streamfile.close()
    else:
      print("stream file already found")
  else:
    seriesname = md[2]
    seriesandepisode = "S" + md[3] + "E" + md[4]
    showdirectory = typedirectory + "/" + seriesname
    if md[5] != "":
      episodename = md[5]
      filename = showdirectory + "/" + " - ".join((seriesname, seriesandepisode, episodename)) + "[" + language + "]" + ".strm"
    else:
      filename = showdirectory + "/" + " - ".join((seriesname, seriesandepisode)) + "[" + language + "]" + ".strm"
    if not os.path.exists(showdirectory):
      os.mkdir(showdirectory)
      print('Show Movie Directory:', showdirectory)
    else:
      print('Show Directory Found', showdirectory)
    if not os.path.exists(filename):
      streamfile = open(filename, "w+")
      streamfile.write(url)
      streamfile.close
      print("strm file created:", filename)
      streamfile.close()
    else:
      print("stream file already found")
