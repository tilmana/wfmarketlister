import requests
import urllib3
import time
import bisect

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    "http": "127.0.0.1:8080",
    "https": "127.0.0.1:8080"
}

runType = input("Modes: 'warframe', 'prime', 'sentinel', 'melee', 'weapon', 'secondary', 'archwing', 'primary', 'rivens': ").lower()
if runType.lower().strip(" ").strip("\n") in ['warframe', 'prime', 'sentinel', 'melee', 'weapon', 'secondary', 'archwing', 'primary', 'rivens']:
    runType = runType.strip("\n")

def sendRequest(url, timeDuration=15):
    r1 = requests.get(verify=False, url=url)
    if r1.status_code == 429:
        time.sleep(timeDuration)
        return None
    else:
        return r1

def sortAlgorithm(csvString):
    return int(csvString.split(",")[2])

def sortAlgorithmRivens(csvString):
    return int(csvString.split(",")[1])

def runNormal():
    outputArray = []
    writeFile = open("outputWFAPI.csv", "w")
    allTags = []

    timeDurationStart = 0
    r1 = sendRequest("https://api.warframe.market/v1/items", timeDurationStart)
    if not r1:
        timeDurationStart += 15
        r1 = sendRequest("https://api.warframe.market/v1/items", timeDurationStart)
    r1response = r1.json()
    for item in r1response["payload"]["items"]:
        if " Prime Set" in item["item_name"]:
            timeDuration = 15
            name = item["url_name"]
            r2 = sendRequest("https://api.warframe.market/v1/items/{0}".format(name), timeDuration)
            if not r2:
                timeDuration += 15
                r2 = sendRequest("https://api.warframe.market/v1/items/{0}".format(name), timeDuration)
            r2response = r2.json()
            setPrice = 0
            itemPrices = []
            proceed = False
            for tag in r2response["payload"]["item"]["items_in_set"][0]["tags"]:
                if tag not in allTags:
                    allTags.append(tag)
            if runType in (r2response["payload"]["item"]["items_in_set"][0]["tags"]):
                proceed = True
            elif runType == "all":
                proceed = True
            if proceed == True:
                print("========={0}=========".format(name))
                for item in r2response["payload"]["item"]["items_in_set"]:
                    r3 = None
                    while r3 is None:
                        r3 = sendRequest("https://api.warframe.market/v1/items/{0}/orders?include=item".format(item["url_name"]), timeDuration)
                        timeDuration += 15
                    r3response = r3.json()
                    responseValue = r3response["payload"]["orders"]
                    validOrders = []
                    prices = []
                    combine = False
                    valid = False
                    for order in responseValue:
                        if order["order_type"] == "sell" and order["user"]["status"] == "ingame":
                            validOrders.append(order)
                    for i in range(len(validOrders)):
                        if validOrders[i]["order_type"] == "sell":
                            if validOrders[i]["user"]["status"] == "ingame":
                                valid = True
                                bisect.insort(prices, validOrders[i]["platinum"])
                        if i == (len(validOrders) - 1) and validOrders[i]["quantity"] == 1 and validOrders[i]["platinum"] == prices[0]:
                            combine == True
                    if valid == False:
                        print("{0} has no in-game sellers!".format(item["en"]["item_name"]))
                        break
                    if combine == False:
                        try:
                            if item["set_root"] == False:
                                itemPrices.append(prices[0] * item["quantity_for_set"])
                            elif item["set_root"] == True:
                                setPrice = prices[0]
                        except:
                            itemPrices.append(prices[0])
                    else:
                        itemPrices.append(prices[0:1])
                currentSetPrice = setPrice
                for price in itemPrices:
                    currentSetPrice = currentSetPrice - price
                print("Purchase: {0}. Individual Difference: {1}".format(setPrice, currentSetPrice))
                itemTags = r2response["payload"]["item"]["items_in_set"][0]["tags"]
                for i in range(len(itemTags)):
                    if itemTags[i] in ["warframe", "sentinel", "weapon", "archwing"]:
                        addTag = itemTags[i]
                        break
                    elif i == (len(itemTags) - 1):
                        addTag = "other"
                        break
                outputArray.append("{0},{1},{2},{3}\n".format(addTag, name, setPrice, currentSetPrice))

    totalCost = 0
    totalDifference = 0
    outputArray.sort(key=sortAlgorithm)
    for output in outputArray:
        writeFile.write(output)
        output = output.split(",")
        totalCost += int(output[2])
        totalDifference += int(output[3])

    print("Total: {0}".format(totalCost))
    print("Difference: {0}".format(totalDifference))

    writeFile.close()

def runRivens():
    outputArray = []
    writeFile = open("outputWFAPI.csv", "w")
    timeDurationStart = 0

    r1 = sendRequest("https://api.warframe.market/v1/riven/items", timeDurationStart)
    if not r1:
        timeDurationStart += 15
        r1 = sendRequest("https://api.warframe.market/v1/riven/items", timeDurationStart)
    r1response = r1.json()
    for item in r1response["payload"]["items"]:
        r2 = sendRequest("https://api.warframe.market/v1/auctions/search?type=riven&weapon_url_name={0}&sort_by=price_asc".format(item["url_name"]), timeDurationStart)
        if not r2:
            timeDurationStart += 15
            r2 = sendRequest("https://api.warframe.market/v1/auctions/search?type=riven&weapon_url_name={0}&sort_by=price_asc".format(item["url_name"]), timeDurationStart)
        r2response = r2.json()
        for listing in r2response["payload"]["auctions"]:
            if listing["owner"]["status"] == "ingame" and listing["buyout_price"] != None:
                print(listing["item"]["weapon_url_name"], listing["buyout_price"])
                outputArray.append("{},{}\n".format(listing["item"]["weapon_url_name"], listing["buyout_price"]))
                break
    totalCost = 0
    outputArray.sort(key=sortAlgorithmRivens)
    for output in outputArray:
        writeFile.write(output)
        output = output.split(",")
        totalCost += int(output[1])

    print("\nTotal: {0}".format(totalCost))
    writeFile.close()

if runType != "rivens":
    runNormal()
else:
    runRivens()
