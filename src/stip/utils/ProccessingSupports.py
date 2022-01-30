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