import json
import requests
import string

def split_string(s) :
    sout = []
    si   = ''
    punc = list(set(['"']+["'"]+list(string.punctuation)))
    # print(punc)
    for i in s :
        if i in string.ascii_letters or i in '1234567890' :
            si += i
        elif i in punc :
            sout.append(si)
            sout.append(i)
            si = ''
        else :
            sout.append(si)
            si = ''
    sout.append(si)
    return list(filter(lambda x : x != '', sout))

with open("text_long.txt","r") as fin :
    input_text = split_string(fin.read().strip())
    # print(input_text)

input_data = [{'id':i,'token':t} for i,t in enumerate(input_text)]

print(json.dumps(input_data[-10:],indent=2))

result = requests.get("http://127.0.0.1:8000/sentiment", data=json.dumps(input_data)).text
print(json.dumps(json.loads(result),indent=2))

# print("Result: {}".format(result))
