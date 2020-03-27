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
  def __init__(self, title, url, year=None, resolution=None, language=None):
    self.title = title.strip()
    self.url = url
    self.year = year
    self.resolution = resolution
    self.language = language

  def getFilename(self):
    '''Getter to get the filename for the stream file
    
    :returns: the fully constructed filename with type directory ea. "movies/The Longest Yard - 720p.strm"
    :rtype: str
    '''
    filestring = [self.title.replace(':','-').replace('*','_').replace('/','_').replace('?','')]
    if self.year:
      if self.year[0] == "(":
        filestring.append(self.year)
      else:
        self.year = "(" + self.year + ")"
        filestring.append(self.year)
    else:
      self.year = "A"
    if self.resolution:
      filestring.append(self.resolution)
    return ('movies/' + self.title.replace(':','-').replace('*','_').replace('/','_').replace('?','') + ' - ' + self.year + "/" + ' - '.join(filestring) + ".strm")
  
  def makeStream(self):
    filename = self.getFilename()
    directories = filename.split('/')
    directories = directories[:-1]
    typedir = directories[0]
    moviedir = '/'.join([typedir, directories[1]])
    if not os.path.exists(typedir):
      os.mkdir(typedir)
    if not os.path.exists(moviedir):
      os.mkdir(moviedir)
    tools.makeStrm(filename, self.url)
  
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
  def __init__(self, showtitle, url, seasonnumber=None, episodenumber=None ,resolution=None, language=None, episodename=None, airdate=None):
    self.showtitle = showtitle
    self.episodenumber = episodenumber
    self.seasonnumber = seasonnumber
    self.episodenumber = episodenumber
    self.url = url
    self.resolution = resolution
    self.language = language
    self.episodename = episodename
    self.airdate = airdate
    self.sXXeXX = "S" + str(self.seasonnumber) + "E" + str(self.episodenumber)

  def getFilename(self):
    '''Getter to get the filename for the stream file
    
    :returns: the fully constructed filename with type directory ea. "tvshows/Star Trek the Next Generation - Season 02/Star Trek the Next Generation - S02E07 - The Borgs kill Picard - 1080p.strm"
    :rtype: str
    '''
    filestring = [self.showtitle.replace(':','-').replace('*','_').replace('/','_').replace('?','')]
    if self.airdate:
      filestring.append(self.airdate.strip())
    else:
      filestring.append(self.sXXeXX.strip())
    if self.episodename:
      filestring.append(self.episodename.strip())
    if self.language:
      filestring.append(self.language.strip())
    if self.resolution:
      filestring.append(self.resolution.strip())
    if self.seasonnumber:
      return ('tvshows/' + self.showtitle.strip().replace(':','-').replace('/','_').replace('*','_').replace('?','') + "/" + self.showtitle.strip().replace(':','-').replace('/','-').replace('*','_').replace('?','') + " - Season " + str(self.seasonnumber.strip()) + '/' + ' - '.join(filestring).replace(':','-').replace('*','_') + ".strm")
    else:
      return ('tvshows/' + self.showtitle.strip().replace(':','-').replace('/','_').replace('*','_').replace('?','') +"/" +' - '.join(filestring).replace(':','-').replace('*','_') + ".strm")
  
  def makeStream(self):
    filename = self.getFilename()
    directories = filename.split('/')
    directories = directories[:-1]
    typedir = directories[0]
    showdir = '/'.join([typedir, directories[1]])
    if not os.path.exists(typedir):
      os.mkdir(typedir)
    if not os.path.exists(showdir):
      os.mkdir(showdir)
    if len(directories) > 2:
      seasondir = '/'.join([showdir, directories[2]])
      if not os.path.exists(seasondir):
        os.mkdir(seasondir)
    tools.makeStrm(filename, self.url)

class rawStreamList(object):
  def __init__(self, filename):
    self.log = logger.Logger(__file__, log_level=logger.LogLevel.DEBUG)
    self.streams = {}
    self.filename = filename
    self.readLines()
    self.parseLine()

  def readLines(self):
    self.lines = [line.rstrip('\n') for line in open(self.filename, encoding="utf8")]
    return len(self.lines)
 
  def parseLine(self):
    linenumber=0
    for j in range(len(self.lines)):
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
        continue
      if thisline[0] == "#" and nextline[0] == "#":
        if tools.verifyURL(self.lines[linenumber+2]):
          self.log.write_to_log(msg=' '.join(["raw stream found:", str(linenumber),'\n', ' '.join([thisline, nextline]),self.lines[linenumber+2]]))
          self.parseStream(' '.join([thisline, nextline]),self.lines[linenumber+2])
          linenumber += 3
          #self.parseLine(linenumber)
        else:
          self.log.write_to_log(msg=' '.join(['Error finding raw stream in linenumber:', str(linenumber),'\n', ' '.join(self.lines[linenumber:linenumber+2])]))
          linenumber += 1
          #self.parseLine(linenumber)
      elif tools.verifyURL(nextline):
        self.log.write_to_log(msg=' '.join(["raw stream found: ", str(linenumber),'\n', '\n'.join([thisline,nextline])]))
        self.parseStream(thisline, nextline)
        linenumber += 2
        #self.parseLine(linenumber)

  def parseStreamType(self, streaminfo):
    typematch = tools.tvgTypeMatch(streaminfo)
    ufcwwematch = tools.ufcwweMatch(streaminfo)
    if ufcwwematch:
      return 'live'
    if typematch:
      streamtype = tools.getResult(typematch)
      if streamtype == 'tvshows':
        return 'vodTV'
      if streamtype == 'movies':
        return 'vodMovie'
      if streamtype == 'live':
        return 'live'
    
    tvshowmatch = tools.sxxExxMatch(streaminfo)
    if tvshowmatch:
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
    #print(streaminfo)
    title = tools.infoMatch(streaminfo)
    if title:
      title = tools.parseMovieInfo(title.group())
    resolution = tools.resolutionMatch(streaminfo)
    if resolution:
      resolution = tools.parseResolution(resolution)
      #print(resolution)
      title = tools.stripResolution(title)
    episodeinfo = tools.parseEpisode(title)
    if episodeinfo:
      if len(episodeinfo) == 3:
        showtitle = episodeinfo[0]
        airdate = episodeinfo[2]
        episodename = episodeinfo[1]
        episode = TVEpisode(showtitle, streamURL, resolution=resolution, episodename=episodename, airdate=airdate)
      else:
        showtitle = episodeinfo[0]
        episodename = episodeinfo[1]
        seasonnumber = episodeinfo[2]
        episodenumber = episodeinfo[3]
        language = episodeinfo[4]
        episode = TVEpisode(showtitle, streamURL, seasonnumber=seasonnumber, episodenumber=episodenumber, resolution=resolution, language=language, episodename=episodename)
    print(episode.__dict__, 'TVSHOW')
    print(episode.getFilename())
    episode.makeStream()
  
  def parseLiveStream(self, streaminfo, streamURL):
    #print(streaminfo, "LIVETV")
    pass

  def parseVodMovie(self, streaminfo, streamURL):
    #todo: add language parsing for |LA| and strip it
    title = tools.parseMovieInfo(streaminfo)
    resolution = tools.resolutionMatch(streaminfo)
    if resolution:
      resolution = tools.parseResolution(resolution)
    year = tools.yearMatch(streaminfo)
    if year:
      title = tools.stripYear(title)
      year = year.group().strip()
    language = tools.languageMatch(title)
    if language:
      title = tools.stripLanguage(title)
      language = language.group().strip()
    moviestream = Movie(title, streamURL, year=year, resolution=resolution, language=language)
    print(moviestream.__dict__, "MOVIE")
    print(moviestream.getFilename())
    moviestream.makeStream()






