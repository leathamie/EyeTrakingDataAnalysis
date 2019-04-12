import pandas as pd
import numpy as np
import os
import json
import re


encoding_dict = {"surprise": "SUS", "peur": "AFS", "degout": "DIS",
                 "joie": "HAS", "tristesse": "SAS", "colere": "ANS",
                 "neutre": "NES"}
zones = ['front', 'nez', 'bouche', 'menton', 'joueH_D', 'joueH_G', 'joueB_D', 'joueB_G', 'oeil_D', 'oeil_G']


# Creating files
def create_files():
    pd.options.mode.chained_assignment = None
    saved_answers = "C:/Users/Karim/Desktop/expe/expe/savedAnswers.csv"
    data = pd.read_csv(saved_answers, sep=';', header=0)
    i = 0
    for j in range(1, 16):
        new_data = data[i:j*4*11]
        # print(new_data)
        # Encoding ========================
        # for k in range(2, len(new_data)):
        #     new_data.at[k, 'Emotions'] = encoding_dict[new_data.iloc[k]['Emotions']]
        #     print(new_data.iloc[k]['Emotions'])
        # new_data.to_csv("./Answers_Encoded/Answers_Encoded_"+new_data.iloc[1]['Emotions']+".tsv", sep="\t", index=False)

        # =================================
        i=j*4*11
        new_data.to_csv("./Answers/Answers_"+new_data.iloc[1]['Emotions']+".tsv", sep="\t", index=False)
        # print(i*4*11)
    # print(data.iloc[0])
    # print(data.shape)


def user_answers_analysis():
    path = "C:/Users/Karim/Documents/GitHub/EyeTrakingDataAnalysis/Answers/"
    path_img = "C:/Users/Karim/Documents/GitHub/eyeTrackingWebPage/images"
    imgs = []
    users = ['S01', 'S02', 'S03', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 'S10', 'S12', 'S13', 'S14', 'Score %']

    for file in os.listdir(path_img):
        if file.endswith("S.JPG"):
            imgs.append(file)
    imgs.append("Score %")

    df_answers = pd.DataFrame(np.zeros(shape=(len(imgs), len(users)), dtype=int),
                              index=imgs, columns=users)

    for file in os.listdir(path):
        if file.endswith(".tsv"):
            # Reading files
            data = pd.read_csv(path + file, sep='\t', header=0)
            cpt = 0
            # print("=====")
            for i in range(2, len(data)):
                # print(data.iloc[i]["Imgs"])
                if encoding_dict[data.iloc[i]["Emotions"]] in data.iloc[i]["Imgs"]:
                    # print(data.iloc[i]["Emotions"], " - ", data.iloc[i]["Imgs"])
                    df_answers.at[data.iloc[i]["Imgs"], data.iloc[1]["Emotions"]] = 1
                    cpt += 1
            df_answers.at["Score %", data.iloc[1]["Emotions"]] = int(cpt/42*100)
    df_answers['Score %'] = (df_answers[:len(df_answers)-1].sum(axis=1)/13*100).astype(int)
    print(df_answers)
    df_answers.to_csv("./Answers_Scores.tsv", sep="\t")


def user_answers_by_emotion():
    path = "C:/Users/Karim/Documents/GitHub/EyeTrakingDataAnalysis/Answers/"
    emotions = ['AFS', 'ANS', 'DIS', 'HAS', 'NES', 'SAS', 'SUS']
    users = ['S01', 'S02', 'S03', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 'S10', 'S12', 'S13', 'S14', 'Score %']

    df_answers = pd.DataFrame(np.zeros(shape=(len(emotions), len(users)), dtype=int),
                              index=emotions, columns=users)

    for file in os.listdir(path):
        if file.endswith(".tsv"):
            # Reading files
            data = pd.read_csv(path + file, sep='\t', header=0)
            cpt = 0
            for i in range(2, len(data)):
                if encoding_dict[data.iloc[i]["Emotions"]] in data.iloc[i]["Imgs"]:
                    # print(data.iloc[i]["Emotions"], " - ", data.iloc[i]["Imgs"])
                    df_answers.at[encoding_dict[data.iloc[i]["Emotions"]], data.iloc[1]["Emotions"]] += 1
                    cpt += 1
            # df_answers.at["Score", data.iloc[1]["Emotions"]] = int(cpt/42*100)
    df_answers['Score %'] = (df_answers[:].sum(axis=1)/(13*6)*100).astype(int)
    print(df_answers)
    df_answers.to_csv("./Answers_Emotion_Scores.tsv", sep="\t")


def aoi():
    path = "C:/Users/Karim/Documents/GitHub/EyeTrakingDataAnalysis/AOI_Jumps_By_Users/"
    emotions = ['AFS', 'ANS', 'DIS', 'HAS', 'NES', 'SAS', 'SUS']
    users = ['S01', 'S02', 'S03', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 'S10', 'S12', 'S13', 'S14', 'Score %']

    df_answers = pd.DataFrame(np.zeros(shape=(len(emotions), len(users)), dtype=int),
                              index=emotions, columns=users)
    df_stats = pd.DataFrame(index=zones)
    cpt = 1
    b = pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], index=zones).astype(int)
    c = pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], index=zones).astype(int)
    d = pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], index=zones).astype(int)
    for file in os.listdir(path):
        if file.endswith(".tsv"):
            # Reading files
            data = pd.read_csv(path + file, sep='\t', header=0)
            b = pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], index=zones).astype(int)
            for col in list(data.columns[1:].values):
                # print(col)
                a = data[:][col].value_counts()
                # df_stats['position_'+col] = data[:][col].value_counts().astype(int)
                # b = b.add(a, fill_value=0)
                # c = c.add(a, fill_value=0)
                if 'position_' + col not in list(df_stats.columns.values):
                    df_stats['position_' + col] = pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], index=zones).astype(int)
                df_stats['position_' + col] = df_stats['position_' + col].add(a, fill_value=0).astype(int)
                # print(a)

            # print(b)
            # df_stats['position_' + col] = b.astype(int)
            # df_stats.to_csv("./AOI_All_Repetition_Sum/AOI_All_Repetition_Sum_"+re.search('(\d+\.tsv)', file).group(1), sep="\t")

    # print(c)
    # df_stats['position_' + col] = c.astype(int)
    # df_stats.to_csv("./AOI_All_Repetition_Sum_Total.tsv", sep="\t")
    df_stats.to_csv("./AOI_All_Repetition_Sum_By_Col.tsv", sep="\t")
            # print(data)
            # print(data['0'].value_counts().index[0], " - ",
            #       data['1'].value_counts(), " - ",
            #       data['2'].value_counts())
            # print(data[:]['0'].value_counts())
            # print(data[:]['1'].value_counts())
            # if cpt < 10:
            #     id_user = 'S0'+str(cpt)
            # elif cpt == 11:
            #     cpt=12
            #     id_user = 'S'+str(cpt)
            # else:
            #     id_user = 'S'+str(cpt)
            # df_stats[id_user+'_position_1'] = data[:]['0'].value_counts()
            # df_stats[id_user+'_position_2'] = data[:]['1'].value_counts()
            # df_stats[id_user+'_position_3'] = data[:]['2'].value_counts()
            # cpt+=1;

            # a = data[:]['0'].value_counts()
            # b = b.add(a, fill_value=0)
            # a = data[:]['1'].value_counts()
            # c = c.add(a, fill_value=0)
            # a = data[:]['2'].value_counts()
            # d = d.add(a, fill_value=0)
            # print(a)
            # b += a.astype(int)
            # print(b)
            # df_stats['position_1'] = data[:]['0'].value_counts()
            # df_stats['position_2'] = data[:]['1'].value_counts()
            # df_stats['position_3'] = data[:]['2'].value_counts()
            # df_stats.to_csv("./AOI_Repetition_OnlyFirst_All_Users.tsv", sep="\t")
            # df_stats.to_csv("./AOI_Repetition_All_Users.tsv", sep="\t")
            # df_stats.to_csv("./AOI_Repetition/AOI_Repetition_"+re.search('(\d+\.tsv)', file).group(1), sep="\t")
            # print("=============================")
    # df_stats['position_1'] = b
    # df_stats['position_2'] = c
    # df_stats['position_3'] = d
    # print(df_stats)
    # df_stats.to_csv("./AOI_Repetition_Sum_First_Only_All_Users.tsv", sep="\t")


def create_json_file():
    data = {}
    data['Info'] = []
    poids = 120
    freq_rest = 80
    freq_act = 180

    # init Constantes
    BORN_INIT = 10
    BORN_INF = 25
    BORN_SUP = 30
    BORN_MAX = 102
    POIDS_MOINS = -2.5
    POIDS_PLUS = 2
    CPT_REST = -6/100
    CPT_ACT = -24/100

    for i in range(2, 367):
        if(i == 102):
            BORN_INIT = 10
            BORN_INF = 75
            BORN_SUP = 80
            BORN_MAX = 202
            CPT_REST = -8/100
            CPT_ACT = -34/100
            print('==== les 200 ========================= ')
        if(i == 202):
            BORN_INIT = 10
            BORN_INF = 105
            BORN_SUP = 110
            BORN_MAX = 367
            CPT_REST = -9/100
            CPT_ACT = -42/100
            print('==== les 300 ========================= ')
        # Temps d'entrainement ==================================
        born_inf = BORN_INIT + (np.log(i) * BORN_INF / np.log(BORN_MAX))
        born_sup = BORN_INIT + (np.log(i) * BORN_SUP / np.log(BORN_MAX))
        time = np.random.randint(int(born_inf), int(born_sup))
        # =======================================================

        # Poids =================================================
        poids_moins = np.random.uniform(POIDS_MOINS,0)
        poids_plus = np.random.uniform(0,POIDS_PLUS)
        kilos = poids_plus + poids_moins
        poids += int(kilos)
        # =======================================================

        # Frequence =============================================
        cpt_rest = np.random.uniform(CPT_REST, 0)
        freq_rest += cpt_rest
        cpt_act = np.random.uniform(CPT_ACT, 0)
        freq_act += cpt_act
        # =======================================================

        print(i-1 , " = ", time, ' = ', poids, ' = ', int(freq_rest), ' = ', int(freq_act))
        data['Info'].append({
            'day' : i-1,
            'poids': poids,
            'duree': time,
            'freq_rest': int(freq_rest),
            'freq_act': int(freq_act)
        })
    print("================")

    with open('C:/Users/Karim/Desktop/data_new_5.json', 'w') as outfile:
        json.dump(data, outfile)


def corsH1():
    path = 'C:/Users/Karim/Documents/GitHub/EyeTrakingDataAnalysis/AOI_Jumps_By_Users/'
    df_corsH1 = pd.DataFrame(columns=['AOI', 'Position'])
    i = 0
    for file in os.listdir(path):
        if file.endswith(".tsv"):
            data = pd.read_csv(path+file, sep='\t', header=0)
            # print(data)
            for col in list(data.columns[1:].values):
                items = data[:][col]
                for it in items.dropna():
                    df_corsH1 = df_corsH1.append({'AOI' : it, 'Position' : int(col)+1}, ignore_index=True)
                # print(col)
            print(df_corsH1)
    df_corsH1.to_csv("./corsH1.tsv", sep="\t")

def ok():
    path_img = "C:/Users/Karim/Documents/GitHub/eyeTrackingWebPage/images"
    imgs = []
    # Retrieving image file names
    for file in os.listdir(path_img):
        if file.endswith("S.JPG"):
            imgs.append(file)
    print(imgs)

# ok()
# corsH1()
create_json_file()
# aoi()
# user_answers_by_emotion()
# user_answers_analysis()
# create_files()
