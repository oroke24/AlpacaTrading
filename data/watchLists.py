
def getLocalSymbols():
    fullList =[]
    for ticker in LOCAL_ARCHIVE:
        fullList.append(ticker)
    return fullList
# Add Watchlists here
MIDNIGHT6 = [ 
    "DXF", "BBGI", "VISL", "MBIO", "TOPS", "EFOI", "AYRO", "SHIP", "CYCC",
    "SLNO", "MIST", "IFRX", "RGLS", "VAL", "XAIR", "OGI", "AMMJ", "NNDM", "M", "CAT", 
    "DKNG", "NIO"
]
MASONS_LIST = [
    "AMD", "CAKE", "SOFI", "NIKE", "META"
]
# NEXT_LIST_HERE = [
#   "ABC", "DEF"
# ]

LOCAL_ARCHIVE = MASONS_LIST + MIDNIGHT6