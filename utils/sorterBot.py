class SorterBot:
    def __init__(self):
        pass

    def sort_by_volumeChange(self, list):
        return sorted(list, key=lambda s: s['volumeChange'], reverse=True)

    def sort_by_priceChange(self, list):
        return sorted(list, key=lambda s: s['priceChangePercentage'], reverse=True)

    def sort_price_low_to_high(self, list):
        return sorted(list, key=lambda s: s['latestClose'], reverse=False)

    def sort_by_market_cap(self, list):
        # Sort descending by 'marketCap' if present, else 0
        return sorted(list, key=lambda s: s.get('marketCap', 0), reverse=True)

    def sort_by_volume(self, list):
        # Sort descending by 'volume' if present, else 0
        return sorted(list, key=lambda s: s.get('volume', 0), reverse=True)


    def double_placers(self, list1, list2):
        newList = []
        for index, i in enumerate(list1):
            if index > 5: break 
            for index, j in enumerate(list2):
                if index > 5: break
                if i['ticker'] == j['ticker']: newList.append(i)

        if newList.count == 0: newList.append("No double placers")

        return newList
        

        
