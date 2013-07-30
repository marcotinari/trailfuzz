trailfuzz
=========

Fuzz a parameter in a HTTP Request after multiple pages browsing

trailfuzz is a simple script, it may help you fuzzing webpages/uris aren't giving you significative response in the same REQUEST/RESPONSE you are actually fuzzing. I found scripting those actions in presense of anti-CSRF (Cross Site Request Forgery) tokens.

dependences
----------
pycurl

usage
----------
- multipagefuzz.py -d|--dictionary <FUZZ_dictionary.txt> -w <outputfile> -
g|--get_session_uri_list <get_session_uri_list.txt> [-c|--cookie <cookie>] [-v|-
-verbose]

get_session_uri_list.txt
----------
short request list needed to establish a valid session "state"
```
|http://mysite.example/muri?param=param|,,GET

|http://mysite.example/muurilist|,|postdata=data|,POST
```

FUZZ_dictionary.txt example
----------
```
payload1
payload2
'
' OR 1=1
```

ATTENTION PLEASE:
----------
you must edit the global vars:
prima: 'this is the URI you need to fuzz'
FUZZME is the placeholder and it will be replaced by your payloads
example: 
```
prima = 'http://mycrazysite.countrycode/path/dynbuyer.do?codBuyer=FUZZME&codProd=112345'
```

seconda: 'this is the URI you want to retrive to check if your fuzz was successful and you got something different from wath you usually get'
example: 
```
seconda = 'http://mycrazysite.countrycode/path/checkSuccessfulbid.jsp'
```
