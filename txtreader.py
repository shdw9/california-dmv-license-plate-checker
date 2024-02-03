import requests
from bs4 import BeautifulSoup

def processPlate(plateText):
    data = {'kidsPlate': '', 'plateType': 'Z', 'plateLength': '7', 'plateNameLow': '1960 legacy'}
    plateText = plateText.replace(" ","")
    for x in range(7):
        if x > len(plateText) - 1:
            data["plateChar"+str(x)] = ""
        else:
            data["plateChar"+str(x)] = plateText[x]

    return data

def genPlateImage(plateText):
    url = "https://www.dmv.ca.gov/wasapp/ipp2/showPlateImage.do?backGroundCode=Z"
    for x in range(7):
        if x > len(plateText) - 1:
            url  += "&imageFile="
        else:
            url += "&imageFile=" + plateText[x]
    url += "&kidsPlate="
    return url

def isAvailable(plate):
    plate = plate.upper()

    if len(plate) < 2:
        print("License plate must be greater than 2 characters!")
        return False
    elif not plate.isalnum():
        print("Your license plate cannot have special characters!")
        return False
    elif len(plate) > 7:
        print("Your license plate cannot be greater than 7 characters!")
        return False
    elif "0" in plate:
        print("Your license plate cannot contain '0'")
        return False
    
    print(plate, end=" ")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.dmv.ca.gov',
        'Connection': 'keep-alive',
        'Referer': 'https://www.dmv.ca.gov/wasapp/ipp2/initPers.do',
        # 'Cookie': 'dtCookie=v_4_srv_4_sn_717F648FF69AA3C945500F0F28EEFEB3_perc_100000_ol_0_mul_1_app-3A9f1bd2f25652a221_1_rcs-3Acss_0; rxVisitor=168783836511576LADNO1F2N4QT4SNEH9SAGH4202KMTK; dtPC=4$146991188_92h1vUFCUCQQMFMCUMUHATKKNNEWOPPFKAUFN-0e0; rxvt=1702348791191^|1702346991191; PD_STATEFUL_0531fc7e-9a22-11ea-bf4d-fa163e384dc6=^%^2Fportal; TS013cb4be=01bcbb781c1b17e1de8199cb17f4fb01e82b488ca4f0ed3f725349e58eaa6d9333df3c2d1c093beeb6b2ec7c0a0b2e6ac203c3519e; TS013cb4be028=01e2aeb03a7252d16cd9ff918131ce1c1feafb3705e367b8d9777bdeb8d070f64e1222d661700eaa0d3652cc7aa5e58275fbec17a3; JSESSIONID=0000gJysm9Tmjilry9dFsb56B-C:18u4e7ncj; PD_STATEFUL_4a158fc4-b691-11ee-a06b-028c6cad0855=^%^2Fwasapp; AWSALB=UPesIG2hPB1HqfGi42A6GV9tsqs4hvPCOz01TivuRDXZtKD70Tc8RVbHAWbOuUWD4gyjRecLFN89dmEfgcERV+AH3p/D3GNKMv8FHIYh08gpEo10mvLbZNj06e5o; AWSALBCORS=UPesIG2hPB1HqfGi42A6GV9tsqs4hvPCOz01TivuRDXZtKD70Tc8RVbHAWbOuUWD4gyjRecLFN89dmEfgcERV+AH3p/D3GNKMv8FHIYh08gpEo10mvLbZNj06e5o; _gcl_au=1.1.1758457133.1706504907; iv_user=unauthorized; timeFormStarted=1706504917214; PD_STATEFUL_cf8518ca-b68f-11ee-8b0d-02f51ccdf669=^%^2Fwasapp',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Sec-GPC': '1',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    data = {
        'acknowledged': 'true',
        '_acknowledged': 'on',
    }

    sesh = requests.Session()

    # init pers
    sesh.get('https://www.dmv.ca.gov/wasapp/ipp2/initPers.do', headers=headers)

    # start pers
    sesh.post('https://www.dmv.ca.gov/wasapp/ipp2/startPers.do', headers=headers, data=data)

    # process pers, pulled a random licPlate and vin from autotrader
    data = {
        'imageSelected': 'none',
        'vehicleType': 'AUTO',
        'licPlateReplaced': '7JBY486',
        'last3Vin': '201',
        'isRegExpire60': 'no',
        'isVehLeased': 'no',
        'plateType': 'Z',
    }
    sesh.post('https://www.dmv.ca.gov/wasapp/ipp2/processPers.do', headers=headers, data=data)

    # get plate
    plate = sesh.post('https://www.dmv.ca.gov/wasapp/ipp2/processConfigPlate.do', headers=headers, data=processPlate(plate))

    soup = BeautifulSoup(plate.text,"html.parser")
    image = genPlateImage(plate)

    if "Order Verification & Owner Information" and "License Plate's Meaning" in soup.text:
        print("- AVAILABLE",image)
        return True
    elif "The license plate number you have selected is no longer available. Please try another plate number." in soup.text:
        print("- TAKEN")
        return False
    elif "The Special Interest License Plate Internet Ordering System is currently unavailable." in soup.text:
        print("- SYSTEM IS DOWN")
        return False
    elif "Your license plate request contains invalid characters" in soup.text:
        print("- INVALID CHARACTERS")
        return False

file2 = open('availableNames.txt', 'a')
file2.write("--------------------------\n")
file2.close()
file1 = open('checkThese.txt', 'r')

count = 0
 
print("Now checking license plates ...")

for line in file1:
    file2 = open('availableNames.txt', 'a')
    count += 1
    print(line.strip(), end = "\t")
    try:
        if (isAvailable(line.strip())):
            file2.write(line.strip() + "\n")
    except:
        pass

# Closing files 
file1.close()
print("Finished!")
