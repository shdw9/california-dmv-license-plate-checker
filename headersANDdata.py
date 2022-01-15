import requests
from requests.structures import CaseInsensitiveDict

def processInput(plate):
    data = "kidsPlate=&plateType=Z&plateLength=7&plateNameLow=1960+legacy"
    for letter in range(len(plate)):
        data += "&plateChar" + str(letter) + "=" + plate[letter]
    if (len(plate) != 7):
        for letter in range(7-len(plate)):
            data += "&plateChar" + str(letter + len(plate)) + "="
    return data

def getImage(plate):
    url = "https://www.dmv.ca.gov/wasapp/ipp2/showPlateImage.do?backGroundCode=Z"
    for letter in range(len(plate)):
        url += "&imageFile=" + plate[letter]
    if (len(plate) != 7):
        for letter in range(7-len(plate)):
            url+= "&imageFile="
    url += "&kidsPlate="
    print(url)
    return url

toCheck = "YASUO58"

url = "https://www.dmv.ca.gov/wasapp/ipp2/processConfigPlate.do"

headers = CaseInsensitiveDict()
headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"
headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
headers["Accept-Language"] = "en-US,en;q=0.5"
headers["Accept-Encoding"] = "gzip, deflate, br"
headers["Content-Type"] = "application/x-www-form-urlencoded"
headers["Origin"] = "https://www.dmv.ca.gov"
headers["Connection"] = "keep-alive"
headers["Referer"] = "https://www.dmv.ca.gov/wasapp/ipp2/processConfigPlate.do"
headers["Cookie"] = "_ga=GA1.2.2128232942.1623958651; _abck=F2B02BB5ECB745DB068626215DAFDC4C~-1~YAAQxdscuLML+LN9AQAAGaSBWgeqzixbVME5Wez78EOy5+fzX3mPFrVoQBE4U0iIYvjVTVm8NrSQmneCPXrYH5BUXBRv7pYclBvymkHNkv53/gJO9911rn7I+SOPE6h0K4SteMGnVDqWPfP1tm/GUePjF2iiqozQNpVyOL8mInrwaqeeZ1OFtLoI8FLLsrKlk02gEAEo/onQlZVRKg8+iq3dj2P3BBgEq62/iZk4bvdjxidZMSLWRLRbhdZ7N8CsmQ8g03u8Z7SngObCcnCyh/ysQQSc8AQqHnK4BrEN2w7kJkJl+/49eKg2LVuqU8YzGXQme70fARvmMhPGY35ZVb46eo5ETkXEDhQnl51XyQjUjBy24nu+/wt92GptFNMNndZeGQ2aYhnKngSWm/k6CW1feP8AjA==~-1~-1~-1; PD_STATEFUL_0531fc7e-9a22-11ea-bf4d-fa163e384dc6=%2Fportal; TS013cb4be=01da805aaf35d0afe934ae12a1bad3a46c4abab245d2c420f256d37626c0bfca07ec19860fd3440010c76d54f46228414a93457390c30688af0bb345e8b1942e46d7e857272ecaf61e291145682c2366a3dd038307393f338672b136cb3afb5053417ec945; TS013cb4be028=018c127eb8e227e9051126977579d3aa31ae030e142943e18a3bf3b632a2e04e263b6048c0f89018ae39434467ead35737066dcc47; JSESSIONID=0000fiqPGm1OdNcLqudpB_ypKYm:18u4e7n8r; PD_STATEFUL_00bcef52-0c5a-11e4-98a1-a224e2a50102=%2Fwasapp; AWSALB=wm8Fe6jVjT0JsGPLxQAtG/uF89FwH0bvuDHI481W0f1+jqmLg2HsvtSoGBMdDMwXWQKv7zRIDDcJE4GCBu0EG0jHeb1bIHsuYQ4MBMwoyeQk9elrUR9S1oW8p3m5; AWSALBCORS=wm8Fe6jVjT0JsGPLxQAtG/uF89FwH0bvuDHI481W0f1+jqmLg2HsvtSoGBMdDMwXWQKv7zRIDDcJE4GCBu0EG0jHeb1bIHsuYQ4MBMwoyeQk9elrUR9S1oW8p3m5; iv_user=unauthorized; mdLogger=false; kampyleUserSession=1642230165555; kampyleSessionPageCounter=3; kampyleUserSessionsCount=3; kampyleUserPercentile=78.26129452287994"
headers["Upgrade-Insecure-Requests"] = "1"
headers["Sec-Fetch-Dest"] = "document"
headers["Sec-Fetch-Mode"] = "navigate"
headers["Sec-Fetch-Site"] = "same-origin"
headers["Sec-Fetch-User"] = "?1"
headers["Sec-GPC"] = "1"
headers["TE"] = "trailers"

data = "kidsPlate=&plateType=Z&plateLength=7&plateNameLow=1960+legacy&plateChar0=&plateChar1=C&plateChar2=K&plateChar3=V&plateChar4=2&plateChar5=&plateChar6="

resp = requests.post(url, headers=headers, data=processInput(toCheck))

print(resp.status_code)
if "The license plate number you have selected is no longer available. Please try another plate number" in resp.text:
    print("License plate " + toCheck + " is taken!")
    getImage(toCheck)
else:
    print("License plate " + toCheck + " is NOT taken!")
    getImage(toCheck)
