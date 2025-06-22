import pandas as pd

def getSP500():
    try:
        url = "https://en.wikipedia.org/wiki/List_of_s%26P_500_companies"
        df = pd.read_html(url,attrs={"id" : "constituents"})[0]
        return df["Symbol"].str.replace("\.", "-", regex=False).tolist()
    except Exception as e:
        print(f"Could not fetch live SP500 data, using fallback")
        return fallback_sp500

fallback_sp500 = [
    "MMM", "AOS", "ABT", "ABBV", "ACN", "ATVI", "ADBE", "AMD", "AES", "AFL",
    "A", "APD", "AKAM", "ALB", "ARE", "ALGN", "ALLE", "LNT", "ALL", "GOOGL",
    "GOOG", "MO", "AMZN", "AMCR", "AEE", "AAL", "AEP", "AXP", "AIG", "AMT",
    "AWK", "AMP", "ABC", "AME", "AMGN", "APH", "ADI", "ANSS", "ANTM", "AON",
    "APA", "AAPL", "AMAT", "APTV", "ACGL", "ADM", "ANET", "AJG", "AIZ", "T",
    "ATO", "ADSK", "AZO", "AVB", "AVY", "BKR", "BALL", "BAC", "BBWI", "BAX",
    "BDX", "BRK-B", "BBY", "BIO", "TECH", "BIIB", "BLK", "BK", "BA", "BKNG",
    "BWA", "BXP", "BSX", "BMY", "AVGO", "BR", "BRO", "BF-B", "BG", "CHRW",
    "CDNS", "CZR", "CPT", "CPB", "COF", "CAH", "KMX", "CCL", "CARR", "CTLT",
    "CAT", "CBOE", "CBRE", "CDW", "CE", "CF", "CRL", "SCHW", "CHTR", "CVX",
    "CMG", "CB", "CHD", "CI", "CINF", "CTAS", "CSCO", "C", "CFG", "CTXS",
    "CLX", "CME", "CMS", "KO", "CGNX", "CTSH", "CL", "CMCSA", "CMA", "CAG",
    "COP", "ED", "STZ", "CEG", "COO", "CPRT", "GLW", "CTVA", "COST", "CTRA",
    "CCI", "CSGP", "CAH", "CRL", "CSX", "CMI", "CVS", "DHI", "DHR", "DRI",
    "DVA", "DE", "DAL", "XRAY", "DVN", "DXCM", "FANG", "DLR", "DFS", "DIS",
    "DG", "DLTR", "D", "DPZ", "DOV", "DOW", "DTE", "DUK", "DD", "DXC", "EMN",
    "ETN", "EBAY", "ECL", "EIX", "EW", "EA", "ELV", "LLY", "EMR", "ENPH",
    "ETR", "EOG", "EPAM", "EQT", "EFX", "EQIX", "EQR", "ESS", "EL", "ETSY",
    "EG", "EVRG", "ES", "RE", "EXC", "EXPE", "EXPD", "EXR", "XOM", "FFIV",
    "FDS", "FAST", "FRT", "FDX", "FITB", "FSLR", "FE", "FIS", "FI", "FLT",
    "FMC", "F", "FTNT", "FTV", "FBHS", "FOXA", "FOX", "BEN", "FCX", "GRMN",
    "IT", "GEHC", "GEN", "GNRC", "GD", "GE", "GIS", "GM", "GPC", "GILD",
    "GL", "GPN", "GS", "HAL", "HIG", "HAS", "HCA", "PEAK", "HSIC", "HSY",
    "HES", "HPE", "HLT", "HOLX", "HD", "HON", "HRL", "HST", "HWM", "HPQ",
    "HUM", "HBAN", "HII", "IBM", "IEX", "IDXX", "ITW", "ILMN", "INCY", "IR",
    "INTC", "ICE", "IFF", "IP", "IPG", "INTU", "ISRG", "IVZ", "INVH", "IQV",
    "IRM", "JBHT", "JKHY", "J", "JNJ", "JCI", "JPM", "JNPR", "K", "KDP",
    "KEY", "KEYS", "KMB", "KIM", "KMI", "KLAC", "KHC", "KR", "LHX", "LH",
    "LRCX", "LW", "LVS", "LDOS", "LEN", "LIN", "LYV", "LKQ", "LMT", "L",
    "LOW", "LUMN", "LYB", "MTB", "MRO", "MPC", "MKTX", "MAR", "MMC", "MLM",
    "MAS", "MA", "MKC", "MCD", "MCK", "MDT", "MRK", "META", "MET", "MTD",
    "MGM", "MCHP", "MU", "MSFT", "MAA", "MRNA", "MHK", "MOH", "TAP", "MDLZ",
    "MPWR", "MNST", "MCO", "MS", "MSI", "MSCI", "NDAQ", "NTAP", "NFLX",
    "NWL", "NEM", "NWSA", "NWS", "NEE", "NKE", "NI", "NDSN", "NSC", "NTRS",
    "NOC", "NCLH", "NOV", "NRG", "NUE", "NVDA", "NVR", "NXPI", "ORLY", "OXY",
    "ODFL", "OMC", "ON", "OKE", "ORCL", "OGN", "OTIS", "PCAR", "PKG", "PARA",
    "PH", "PAYX", "PAYC", "PYPL", "PNR", "PBCT", "PEP", "PKI", "PFE", "PM",
    "PSX", "PNW", "PXD", "PNC", "POOL", "PPG", "PPL", "PFG", "PG", "PGR",
    "PLD", "PRU", "PEG", "PTC", "PSA", "PHM", "QRVO", "PWR", "QCOM", "DGX",
    "RL", "RJF", "RTX", "O", "REG", "REGN", "RF", "RSG", "RMD", "RHI", "ROK",
    "ROL", "ROP", "ROST", "RCL", "SPGI", "CRM", "SBAC", "SLB", "STX", "SEE",
    "SRE", "NOW", "SHW", "SBNY", "SPG", "SWKS", "SJM", "SNA", "SEDG", "SO",
    "LUV", "SWK", "SBUX", "STT", "STE", "SYK", "SIVB", "SYF", "SNPS", "SYY",
    "TMUS", "TROW", "TTWO", "TPR", "TRGP", "TGT", "TEL", "TDY", "TFX", "TER",
    "TSLA", "TXN", "TXT", "TMO", "TJX", "TSCO", "TT", "TDG", "TRV", "TRMB",
    "TFC", "TWTR", "TYL", "TSN", "USB", "UDR", "ULTA", "UNP", "UAL", "UPS",
    "URI", "UNH", "UHS", "VLO", "VTR", "VRSN", "VRSK", "VZ", "VFC", "VTRS",
    "VICI", "V", "VMC", "WAB", "WBA", "WMT", "WBD", "WM", "WAT", "WEC",
    "WFC", "WELL", "WST", "WDC", "WRK", "WY", "WHR", "WMB", "WTW", "WYNN",
    "XEL", "XYL", "YUM", "ZBRA", "ZBH", "ZION", "ZTS"
]
