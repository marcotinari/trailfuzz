#!/usr/bin/python

##### fuzz a page after a preset requests and check response codes/details with a custom request, after each fuzzing request
##### Hope you'll enjoy!
##### TYPE ./trailfuzz.py -h please


import pycurl
import cStringIO
import getopt, sys
import urllib
import csv
def fuzz(dictionary,outputfile,verbose,listafile,personalcookie):
  # prima   : INSER HERE URI TO FUZZ - FUZZME IS THE PLACEHOLDER
  prima = 'http://mysite.ontheweb/checkBuyer.do?progPubblic=761&cod=FUZZME&data&code=15002'
  # seconda : INSERT HERE URI TO CHECK IF SOMETHING WENT DIFFERENT FROM DEFAULT
  seconda = 'http://mysite.ontheweb/path/jsp/checkMyStatus.jsp'
  buf = cStringIO.StringIO()
  buf2 = cStringIO.StringIO()
  output_file = open(outputfile, "w")
  Dictionary=dictionary
  
  urilist = csv.reader(open(listafile,'r'),delimiter=',',quotechar='|')

  c = pycurl.Curl()
  cookie = personalcookie
  c.setopt(c.WRITEFUNCTION, buf.write)
  if personalcookie == '':
    c.setopt(c.COOKIEFILE,'')
  else:
    c.setopt(c.COOKIE, personalcookie)
    if verbose: print 'USING USER SUPPLIED COOKIE:', personalcookie
  c.setopt(c.VERBOSE, verbose)
  for row in urilist:
    if row[2] == 'POST':
      c.setopt(c.POSTFIELDS, row[1])
    elif row[2] == 'GET':
      c.setopt(c.HTTPGET, 1)
    c.setopt(c.URL, row[0])
    c.perform()
  if verbose:
    print buf.getvalue()
  buf.close()
  c.setopt(c.WRITEFUNCTION, buf2.write)
  dictionary_file = open(Dictionary, "r")
  fuzzlines = dictionary_file.readlines()
  responselength=0
  responselength2=0
  for fuzzline in fuzzlines:
    FUZZ=fuzzline.rstrip('\r\n')
    if verbose: print '****************** Fuzzing: ' + FUZZ + '  *************************'
    fuzzstring = prima.replace('FUZZME',urllib.quote_plus(FUZZ,'/'))
    c.setopt(c.URL, fuzzstring)
    if verbose: print 'PRIMA URI=' + fuzzstring
    try: 
      c.perform()
      responselength = c.getinfo(pycurl.CONTENT_LENGTH_DOWNLOAD)
    except pycurl.error,error:
      errno, errstr = error
      print 'An Error occurred ', errstr
      responselength = 0
    httpcode = c.getinfo(pycurl.RESPONSE_CODE)
    c.setopt(c.URL, seconda)
    c.perform()
    # retrive the information you want to compare ... for example content lenght
    responselength2 = c.getinfo(pycurl.CONTENT_LENGTH_DOWNLOAD)
    print 'FUZZ= ' + str(FUZZ) + ' HTTP-CODE= ' + str(httpcode) + '  RESPONSE-LENGTH= ' + str(responselength) + '  RESPONSE-LENGTH2= ' + str(responselength2)
    output_file.write(urllib.quote_plus(FUZZ,'/') + ',' + str(httpcode) + ',' + str(responselength) + ',' + str(responselength2) + '\n')
    
    if verbose: print buf2.getvalue()
    
  output_file.close()
  buf2.close()
  dictionary_file.close()
  
def main(argv):
   outputfilename = ''
   FUZZ_dictionary = ''
   get_session_uri_list = ''
   verbose = False
   personalcookie = ''
   try:
      opts, args = getopt.getopt(argv,"hd:w:g:vc:",["FUZZ_dictionary=","get_session_uri_list=","verbose","cookie"])
   except getopt.GetoptError:
      print 'trailfuzz.py -d|--dictionary <FUZZ_dictionary.txt> -w <outputfile> -g|--get_session_uri_list <get_session_uri_list.txt> -c|--cookie <cookie> [-v|--verbose]'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'trailfuzz.py -d|--dictionary <FUZZ_dictionary.txt> -w <outputfile> -g|--get_session_uri_list <get_session_uri_list.txt> -c|--cookie <cookie> [-v|--verbose]'
         sys.exit()
      elif opt in ("-d", "--dictionary"):
         FUZZ_dictionary = arg
      elif opt in ("-w"):
	 outputfilename = arg
      elif opt in ("-c","--cookie"):
	 personalcookie = arg
      elif opt in ("-v", "--verbose"):
         verbose = True
         print 'VERBOSE OUTPUT'
      elif opt in ("-g", "--get-session-uri_list"):
	 get_session_uri_list = arg
   print 'using dictionary :', FUZZ_dictionary
   print 'output file:', outputfilename
   print 'using_sessions :', get_session_uri_list
   fuzz(FUZZ_dictionary,outputfilename,verbose,get_session_uri_list,personalcookie)

if __name__ == "__main__":
   main(sys.argv[1:])
