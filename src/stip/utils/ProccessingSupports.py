class ProcessingSupports:
    def __init__(self):
        pass

    # 現状のは作ってるだけだけど，複数箇所でDataBaseコンテンツの加工が必要になったらこれに切り替える
    def convertFromStrToList(self, str_list_contents):
        # remove_quoute = str_list_contents.replace('"')
        remove_double_quote = str_list_contents.replace("'", "")
        remove_space = remove_double_quote.replace(" ", "")
        convert_to_list = remove_space.split(',')
        return convert_to_list

    def nextLatitudeLargerThanCurrentLatitude(self, base_latitude, latitude):
        if (latitude < base_latitude):
            return latitude
        return base_latitude

    def nextLatitudeSmallerThanCurrentLatitude(self, base_latitude, latitude):
        if (base_latitude < latitude):
            return latitude
        return base_latitude

    def nextLongitudeLagerThanCurrentLongitude(self, base_longitude, longitude):
        if (longitude < base_longitude):
            return longitude
        return base_longitude

    def nextLongitudeSmallerThanCurrentLongitude(self, base_longitude, longitude):
        if (base_longitude < longitude):
            return longitude
        return base_longitude
    
