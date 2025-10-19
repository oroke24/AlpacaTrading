
def getLocalSymbols():
    fullList =[]
    for ticker in LOCAL_ARCHIVE:
        fullList.append(ticker)
    return fullList
# Add Watchlists here
MIDNIGHT6 = [ 
    "DXF", "BBGI", "VISL", "MBIO", "TOPS", "EFOI", "SHIP", "SLNO", "MIST", 
    "IFRX", "VAL", "XAIR", "OGI", "AMMJ", "NNDM", "M", "CAT", "DKNG", "NIO"
]
MASONS_LIST = [
    "CAKE", "SOFI", "NKE"
]
FALLBACK_SP500 = [
    "MMM", "AOS", "ABT", "ABBV", "ACN", "ADBE", "AMD", "AES", "AFL",
    "A", "APD", "AKAM", "ALB", "ARE", "ALGN", "ALLE", "LNT", "ALL", "GOOGL",
    "GOOG", "MO", "AMZN", "AMCR", "AEE", "AAL", "AEP", "AXP", "AIG", "AMT",
    "AWK", "AMP", "AME", "AMGN", "APH", "ADI", "AON",
    "APA", "AAPL", "AMAT", "APTV", "ACGL", "ADM", "ANET", "AJG", "AIZ", "T",
    "ATO", "ADSK", "AZO", "AVB", "AVY", "BKR", "BALL", "BAC", "BBWI", "BAX",
    "BDX", "BRK-B", "BBY", "BIO", "TECH", "BIIB", "BLK", "BK", "BA", "BKNG",
    "BWA", "BXP", "BSX", "BMY", "AVGO", "BR", "BRO", "BF-B", "BG", "CHRW",
    "CDNS", "CZR", "CPT", "CPB", "COF", "CAH", "KMX", "CCL", "CARR",
    "CAT", "CBOE", "CBRE", "CDW", "CE", "CF", "CRL", "SCHW", "CHTR", "CVX",
    "CMG", "CB", "CHD", "CI", "CINF", "CTAS", "CSCO", "C", "CFG",
    "CLX", "CME", "CMS", "KO", "CGNX", "CTSH", "CL", "CMCSA", "CMA", "CAG",
    "COP", "ED", "STZ", "CEG", "COO", "CPRT", "GLW", "CTVA", "COST", "CTRA",
    "CCI", "CSGP", "CAH", "CRL", "CSX", "CMI", "CVS", "DHI", "DHR", "DRI",
    "DVA", "DE", "DAL", "XRAY", "DVN", "DXCM", "FANG", "DLR", "DIS",
    "DG", "DLTR", "D", "DPZ", "DOV", "DOW", "DTE", "DUK", "DD", "DXC", "EMN",
    "ETN", "EBAY", "ECL", "EIX", "EW", "EA", "ELV", "LLY", "EMR", "ENPH",
    "ETR", "EOG", "EPAM", "EQT", "EFX", "EQIX", "EQR", "ESS", "EL", "ETSY",
    "EG", "EVRG", "ES", "EXC", "EXPE", "EXPD", "EXR", "XOM", "FFIV",
    "FDS", "FAST", "FRT", "FDX", "FITB", "FSLR", "FE", "FIS", "FI",
    "FMC", "F", "FTNT", "FTV", "FOXA", "FOX", "BEN", "FCX", "GRMN",
    "IT", "GEHC", "GEN", "GNRC", "GD", "GE", "GIS", "GM", "GPC", "GILD",
    "GL", "GPN", "GS", "HAL", "HIG", "HAS", "HCA", "HSIC", "HSY", "HPE",
    "HLT", "HOLX", "HD", "HON", "HRL", "HST", "HWM", "HPQ",
    "HUM", "HBAN", "HII", "IBM", "IEX", "IDXX", "ITW", "ILMN", "INCY", "IR",
    "INTC", "ICE", "IFF", "IP", "IPG", "INTU", "ISRG", "IVZ", "INVH", "IQV",
    "IRM", "JBHT", "JKHY", "J", "JNJ", "JCI", "JPM", "K", "KDP",
    "KEY", "KEYS", "KMB", "KIM", "KMI", "KLAC", "KHC", "KR", "LHX", "LH",
    "LRCX", "LW", "LVS", "LDOS", "LEN", "LIN", "LYV", "LKQ", "LMT", "L",
    "LOW", "LUMN", "LYB", "MTB", "MPC", "MKTX", "MAR", "MMC", "MLM",
    "MAS", "MA", "MKC", "MCD", "MCK", "MDT", "MRK", "META", "MET", "MTD",
    "MGM", "MCHP", "MU", "MSFT", "MAA", "MRNA", "MHK", "MOH", "TAP", "MDLZ",
    "MPWR", "MNST", "MCO", "MS", "MSI", "MSCI", "NDAQ", "NTAP", "NFLX",
    "NWL", "NEM", "NWSA", "NWS", "NEE", "NKE", "NI", "NDSN", "NSC", "NTRS",
    "NOC", "NCLH", "NOV", "NRG", "NUE", "NVDA", "NVR", "NXPI", "ORLY", "OXY",
    "ODFL", "OMC", "ON", "OKE", "ORCL", "OGN", "OTIS", "PCAR", "PKG",
    "PH", "PAYX", "PAYC", "PYPL", "PNR", "PEP", "PFE", "PM",
    "PSX", "PNW", "PNC", "POOL", "PPG", "PPL", "PFG", "PG", "PGR",
    "PLD", "PRU", "PEG", "PTC", "PSA", "PHM", "QRVO", "PWR", "QCOM", "DGX",
    "RL", "RJF", "RTX", "O", "REG", "REGN", "RF", "RSG", "RMD", "RHI", "ROK",
    "ROL", "ROP", "ROST", "RCL", "SPGI", "CRM", "SBAC", "SLB", "STX", "SEE",
    "SRE", "NOW", "SHW", "SBNY", "SPG", "SWKS", "SJM", "SNA", "SEDG", "SO",
    "LUV", "SWK", "SBUX", "STT", "STE", "SYK", "SYF", "SNPS", "SYY",
    "TMUS", "TROW", "TTWO", "TPR", "TRGP", "TGT", "TEL", "TDY", "TFX", "TER",
    "TSLA", "TXN", "TXT", "TMO", "TJX", "TSCO", "TT", "TDG", "TRV", "TRMB",
    "TFC", "TYL", "TSN", "USB", "UDR", "ULTA", "UNP", "UAL", "UPS",
    "URI", "UNH", "UHS", "VLO", "VTR", "VRSN", "VRSK", "VZ", "VFC", "VTRS",
    "VICI", "V", "VMC", "WAB", "WMT", "WBD", "WM", "WAT", "WEC",
    "WFC", "WELL", "WST", "WDC", "WY", "WHR", "WMB", "WTW", "WYNN",
    "XEL", "XYL", "YUM", "ZBRA", "ZBH", "ZION", "ZTS"
]
# NEXT_LIST_HERE = [
#   "ABC", "DEF"
# ]

LOCAL_ARCHIVE = MASONS_LIST + MIDNIGHT6 + FALLBACK_SP500