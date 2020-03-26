import asyncio
import logger
import os
import re
import tools
class Movie(object):
  '''A class used to construct the Movie filename.

  :param title: The Title of the Movie (required)
  :type title: str.
  :param url: The url to the location of the stream (required)
  :type url: str.
  :param year: The Year the movie was made (optional)
  :type year: str.
  :param resolution: The resolution of the stream (optional)
  :type resolution: str.
  '''
  def __init__(self, title, url, year="", resolution=""):
    self.title = title
    self.url = url
    self.year = year
    self.resolution = resolution

  def getFilename(self):
    '''Getter to get the filename for the stream file
    
    :returns: the fully constructed filename with type directory ea. "movies/The Longest Yard - 720p.strm"
    :rtype: str
    '''
    filestring = [self.title]
    if self.year != "":
      filestring.append(("(" + self.year + ")"))
    if self.resolution != "":
      filestring.append(self.resolution)
    return ('movies/' + ' - '.join(filestring) + ".strm")

  
class TVEpisode(object):
  '''A class used to construct the TV filename.

  :param showtitle: The Title of the TVshow (required)
  :type showtitle: str.
  :param url: The url to the location of the stream (required)
  :type url: str.
  :param seasonnumber: The season number of this episode. (optional)
  :type seasonnumber: str
  :param episodenumber: The episode number of this episode. (optional)
  :type episodenumber: str
  :param resolution: The resolution of the stream (optional)
  :type resolution: str.
  :param year: The Year the show was made (optional)
  :type year: str.
  :param episodename: The name of the episode. (optional)
  :type episodename: str
  :param airdate: The date the show aired, for daily or nightly shows like news (optional)
  :type airdate: str
  '''
  def __init__(self, showtitle, url, seasonnumber="", episodenumber="" ,resolution="", year="", episodename="", airdate=""):
    self.showtitle = showtitle
    self.episodenumber = episodenumber
    self.seasonnumber = seasonnumber
    self.episodenumber = episodenumber
    self.url = url
    self.resolution = resolution
    self.year = year
    self.episodename = episodename
    self.airdate = airdate
    self.sXXeXX = "S" + self.seasonnumber + "E" + self.episodenumber

  def getFilename(self):
    '''Getter to get the filename for the stream file
    
    :returns: the fully constructed filename with type directory ea. "tvshows/Star Trek the Next Generation - Season 02/Star Trek the Next Generation - S02E07 - The Borgs kill Picard - 1080p.strm"
    :rtype: str
    '''
    filestring = [self.showtitle]
    if self.year != "":
      filestring.append(("(" + self.year + ")"))
    if self.airdate != "":
      filestring.append(self.airdate)
    else:
      filestring.append(self.sXXeXX)
    if self.episodename != "":
      filestring.append(self.episodename)
    if self.resolution != "":
      filestring.append(self.resolution)
    if self.seasonnumber != "":
      return ('tvshows/'+ self.showtitle + " - Season " + self.seasonnumber + '/' + ' - '.join(filestring) + ".strm")
    else:
      return ('tvshows/' + ' - '.join(filestring) + ".strm")
'''
#TestCases:

testMovie = Movie('The Longest Yard', 'https://url.com/stream', resolution='720p')
print(testMovie.getFilename())
testTvepisode = TVEpisode('Late Night with David Letterman', 'https://url.com/tvstream', airdate='5-5-2020', resolution='480p', episodename='interviews with celebrities')
print(testTvepisode.getFilename())
testTvepisode = TVEpisode('Late Night with David Letterman', 'https://url.com/tvstream', airdate='5-5-2020', resolution='480p')
print(testTvepisode.getFilename())
testTvepisode = TVEpisode('Late Night with David Letterman', 'https://url.com/tvstream', airdate='5-5-2020')
print(testTvepisode.getFilename())
testTvepisode = TVEpisode('Star Trek', 'https://url.com/tvstream', seasonnumber='02', episodenumber='05', resolution='360p')
print(testTvepisode.getFilename())
testTvepisode = TVEpisode('Star Trek the Next Generation', 'https://url.com/tvstream', seasonnumber='06', episodenumber='15', episodename='Picard Kills the Borgs')
print(testTvepisode.getFilename())
testTvepisode = TVEpisode('Star Trek the Next Generation', 'https://url.com/tvstream', seasonnumber='02', episodenumber='07', resolution='1080p', episodename='The Borgs kill Picard')
print(testTvepisode.getFilename())
'''
class rawStreamList(object):
  def __init__(self, filename):
    self.log = logger.Logger(__file__, log_level=logger.LogLevel.DEBUG)
    self.streams = {}
    self.filename = filename
    self.readLines()
    self.parseLine(0)

  def readLines(self):
    self.lines = [line.rstrip('\n') for line in open(self.filename)]
    return len(self.lines)
 
  def parseLine(self, linenumber):
    numlines = len(self.lines)
    if linenumber >= numlines:
      return 0
    if not linenumber:
      linenumber = 0
    thisline = self.lines[linenumber]
    nextline = self.lines[linenumber + 1]
    firstline = re.compile('EXTM3U', re.IGNORECASE).search(thisline)
    if firstline:
      linenumber += 1
      self.parseLine(linenumber)
    if thisline[0] == "#" and nextline[0] == "#":
      if tools.verifyURL(self.lines[linenumber+2]):
        self.log.write_to_log(msg=' '.join(["raw stream found:", str(linenumber),'\n', ' '.join([thisline, nextline]),self.lines[linenumber+2]]))
        self.parseStream(' '.join([thisline, nextline]),self.lines[linenumber+2])
        linenumber += 3
        self.parseLine(linenumber)
      else:
        self.log.write_to_log(msg=' '.join(['Error finding raw stream in linenumber:', str(linenumber),'\n', ' '.join(self.lines[linenumber:linenumber+2])]))
        linenumber += 1
        self.parseLine(linenumber)
    elif tools.verifyURL(nextline):
      self.log.write_to_log(msg=' '.join(["raw stream found: ", str(linenumber),'\n', '\n'.join([thisline,nextline])]))
      self.parseStream(thisline, nextline)
      linenumber += 2
      self.parseLine(linenumber)

  def parseStreamType(self, streaminfo):
    typematch = tools.tvgTypeMatch(streaminfo)
    if typematch:
      streamtype = tools.getResult(typematch)
      if streamtype == 'tvshows':
        return 'vodTV'
      if streamtype == 'movies':
        return 'vodMovie'
      if streamtype == 'live':
        return 'live'
    
    tvshowmatch = tools.sxxExxMatch(streaminfo)
    if tvshowmatch != False:
      return 'vodTV'
    
    airdatematch = tools.airDateMatch(streaminfo)
    if airdatematch:
      return 'vodTV'

    channelmatch = tools.tvgChannelMatch(streaminfo)
    if channelmatch:
      return 'live'
    
    logomatch = tools.tvgLogoMatch(streaminfo)
    if logomatch:
      return 'live'
    
    tvgnamematch = tools.tvgNameMatch(streaminfo)
    if tvgnamematch:
      if not tools.imdbCheck(tools.getResult(tvgnamematch)):
        return 'live'
    return 'vodMovie'


  def parseStream(self, streaminfo, streamURL):
    streamtype = self.parseStreamType(streaminfo)
    if streamtype == 'vodTV':
      self.parseVodTv(streaminfo, streamURL)
    elif streamtype == 'vodMovie':
      self.parseVodMovie(streaminfo, streamURL)
    else:
      self.parseLiveStream(streaminfo, streamURL)
  
  def parseVodTv(self, streaminfo, streamURL):
    print(streaminfo, "TVSHOW")
  
  def parseLiveStream(self, streaminfo, streamURL):
    print(streaminfo, "LIVETV")

  def parseVodMovie(self, streaminfo, streamURL):
    #todo: strip year from title, add language parsing for |LA| and strip it
    title = tools.parseMovieInfo(streaminfo)
    resolution = tools.resolutionMatch(streaminfo)
    if resolution:
      resolution = tools.parseResolution(resolution)
    else:
      resolution = ""
    year = tools.yearMatch(streaminfo)
    if year:
      year = year.group().strip()
    else:
      year = ""
    moviestream = Movie(title, streamURL, year=year, resolution=resolution)
    print(moviestream.__dict__, "MOVIE")

examplelist = rawStreamList('test.m3u')
#examplelist.readM3u()



     

