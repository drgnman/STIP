import re
from stip.utils.MathOperator import MathOperator 

class ProcedureProcessing:
    def __init__(self):
        self.math_operator = MathOperator()

    def procedureSplit(self, procedure):
        # Operatorの後ろには必ず(があるため，(の位置を取得する
        operator_position_indicators = list(re.finditer("\(", procedure))

        # 文字列の後ろから抽出されたOperatorを順に格納するリスト
        operators = []
        # 抽出された(のindexを後ろから探索
        for position_num in range(len(operator_position_indicators)-1, -1, -1):
            if  position_num == 0:
                # 一番前の要素については，最初から(の前まで
                operators.append(procedure[:operator_position_indicators[position_num].span()[0]])
            else:
                # 二番目以降は，連続する(の間を切り取ることで抽出
                operator = procedure[
                    operator_position_indicators[position_num-1].span()[1]: operator_position_indicators[position_num].span()[0]
                    ]
                # 注意: Add(5, Hot(T))のように数式の第二引数にOperatorが来る場合，","を頼りに該当部分を切り出す
                if "," in operator:
                    operator = operator[operator.rfind(",")+1:]
                if operator != "":
                    operators.append(operator)
        
        return operators
    
    def extractTargetFormulaPart(self, operator, procedure):
        extract_part_to_target_operator = procedure.rfind(operator) # find開始する位置
        target_formula = procedure[
            procedure.find("(", extract_part_to_target_operator) + 1: procedure.find(")", extract_part_to_target_operator)
            ]
        return target_formula # Add(10,T) -> "10,T" <- target_formula_part
    # Hot Onlyな処理はこいつに食わせないこととする = 途中式にHotがあった場合だけDBに接続する

    def splitEachElementFromTargetFormula(self, target_formula, value_list):
        elements = target_formula.split(",")
        for i in range(0, len(elements)):
            if (self.math_operator.isInt(elements[i])):
                elements[i] = int(elements[i])
            elif (self.math_operator.isFloat(elements[i])):
                elements[i] = float(elements[i])
            elif (elements[i] in value_list.keys()):
                elements[i] = value_list[elements[i]][:-1] # Tの場合，value_list["T"]の値を取ってくる，末尾はタイムスタンプのため，除外
            else:
                elements[i] = 0.0 #どれにも値しない(まだ値がない変数)の場合は，0.0とする
        return elements

    def calcurateFromProcedure(self, operator, values):
        # オペレータに応じて引数が変わるため，分岐させる
        pattern_aggregation = re.compile(r'\b(SUM|AVE|MAX|MIN|MID|MOD|NEW)\b')
        pattern_query = re.compile(r'\b(Hot)\b')
        if bool(pattern_aggregation.search(operator)):
            return self.math_operator.callAggregation(operator, values)
        elif bool(pattern_query.search(operator)):
            resultSet = self.math_operator.callQuery(operator, values)
            if (resultSet == []): return resultSet
            resultSet = list(resultSet[0])
            resultSet[1] = str(resultSet[1])
            return resultSet
        else:
            return self.math_operator.callCalculate(operator, values[0], values[1])

    def calculateAggrigation(self, target_formula, operator):
        return self.calcCall(target_formula, operator)