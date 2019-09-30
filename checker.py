import pandas as pd

def StringParser(string):
    out_array = []
    string = string.split(',')
   
    for i in string:
        try:
            out_array.append(int(i))
        except:
            print("Omitting unknown value")
    return set(out_array)

def RetrieveRes(df, participants):
    ans_dict = {}
    for p in participants:
        a = list()
        for i in range(10):
            a.append(df[df['Адрес электронной почты']==p]["Q"+str(i+1)].values)
        ans_dict[p] = a
    return ans_dict


def Score(ans,correct_ans):
    if(len(ans - correct_ans)) !=0:
        score = 0
    else:
        score = len(ans)
    return score

def ApplyScore(participants_dict, correct_answers):
    final_res = {}
    for participant in participants_dict.keys():
        res_current = participants_dict[participant]
        sum = 0
        for i in range(len(res_current)):
            if len(res_current[i]) == 0:
                continue
            q = res_current[i][0]
            sum +=Score(StringParser(q), correct_answers)
        final_res[participant] = sum
    return final_res

#grades = ApplyScore(RetrieveRes(df, participants), correct_answers)

