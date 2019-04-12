import pandas as pd
import re
import os
import numpy as np


# cette fonction sert à asupprimer les 3 premières images
def remove_first_three():

    path = "./Old_Data/By_users/"
    for file in os.listdir(path):
        print(file)
        if file.endswith(".tsv"):
            data = pd.read_csv(path + file, sep=',', header=0)
            data = data[data.MediaName != 'http://localhost/eyetrackingwebpage/pages/AF01AFS.JPG.html (CRC)']
            data = data[data.MediaName != 'http://localhost/eyetrackingwebpage/pages/AF01ANS.JPG.html (CRC)']
            data = data[data.MediaName != 'http://localhost/eyetrackingwebpage/pages/AF01DIS.JPG.html (CRC)']
            data.to_csv('./Clean_by_users/'+file, sep='\t', index=False)


# cette fonction sert à générer les chemins pour chaque images pour chaque participant
def creat_aoi_paths():

    # Retrieving image file names =========================================
    imgs = []
    path_img = "C:/Users/Karim/Documents/GitHub/eyeTrackingWebPage/images_moins_3"
    for file in os.listdir(path_img):
        if file.endswith("S.JPG"):
            imgs.append(file)
    # ======================================================================

    # Creating Files =======================================================
    path = "./Clean_data/Clean_by_users/"
    for file in os.listdir(path):
        if file.endswith(".tsv"):
            print("user : ", file, " ==================")
            all_jumps = []
            data = pd.read_csv(path + file, sep='\t', header=0)
            # Dropping columns before AOI columns
            data = data.drop(data.ix[:, :'ParticipantName'].columns, axis=1)
            data = data.drop(data.ix[:, 'RecordingTimestamp':'ValidityRight'].columns, axis=1)
            for img in imgs:
                data_img = data[data['MediaName'].str.contains(img)]
                data_img = data_img.drop(data_img.ix[:, :'MediaName'].columns, axis=1)
                temp = ""
                jumps = []
                for row, column in data_img.iterrows():
                    for key, value in column.iteritems():
                        if value == 1 and key != temp:
                            jumps.append(re.search('\[(.+?)\]', key).group(1))
                            temp = key
                all_jumps += [jumps]
            df_emo = pd.DataFrame(all_jumps, index=imgs)
            # Saving file
            df_emo.to_csv("./Clean_data/Clean_aoi_paths/AOI_paths_" + file, sep='\t')
    # ================================================================================


# cette fonction sert à rassembler les fichiers AOI_paths_users
def create_aoi_paths_global():
    path = "./Clean_data/Clean_aoi_paths/"
    data_global = pd.DataFrame()
    for file in os.listdir(path):
        if file.endswith(".tsv"):
            print("user : ", file, " ==================")
            data = pd.read_csv(path + file, sep='\t', header=0)
            data_global = data_global.append(data, sort=False)
    # Saving file
    data_global.to_csv("./Clean_data/AOI_paths_global.tsv", sep='\t')


# Cette fonction sert à calculer le chemins le plus suivi par les participant
def create_aoi_transition_matrix():

    file = "./Clean_data/AOI_paths_global.tsv"
    zones = ['front', 'nez', 'bouche', 'menton', 'joueH_D', 'joueH_G', 'joueB_D', 'joueB_G', 'oeil_D', 'oeil_G']
    data = pd.read_csv(file, sep='\t', header=0)
    matrix = pd.DataFrame(np.zeros(shape=(len(zones), len(zones)), dtype=int),
                              index=zones, columns=zones)

    for index, row in data.iterrows():
        temp = "empty"
        for e, a in row.iteritems():
            if a in zones:
                if temp == 'empty':
                    temp = a
                else:
                    matrix.at[temp, a] += 1
    print(matrix)
    # Saving file
    matrix.to_csv("./Clean_data/AOI_transition_matrix.tsv", sep='\t')


def create_aoi_grouped_transition_matrix():

    file = "./Clean_data/AOI_paths_global.tsv"
    zones = ['front', 'nez', 'bouche', 'menton', 'joueH_D', 'joueH_G', 'joueB_D', 'joueB_G', 'oeil_D', 'oeil_G']
    grouped_zones = ['top_zones', 'middle_zones', 'bottom_zones']
    zone_dict = {'front': 'top_zones', 'oeil_D' : 'top_zones', 'oeil_G' : 'top_zones',
                 'nez' : 'middle_zones', 'joueH_D' : 'middle_zones', 'joueH_G' : 'middle_zones',
                 'bouche' : 'bottom_zones', 'menton' : 'bottom_zones', 'joueB_D' : 'bottom_zones',
                 'joueB_G' : 'bottom_zones'}
    data = pd.read_csv(file, sep='\t', header=0)
    matrix = pd.DataFrame(np.zeros(shape=(len(grouped_zones), len(grouped_zones)), dtype=int),
                              index=grouped_zones, columns=grouped_zones)

    for index, row in data.iterrows():
        temp = "empty"
        for e, a in row.iteritems():
            if a in zones:
                if temp == 'empty':
                    temp = a
                else:
                    matrix.at[zone_dict.get(temp), zone_dict.get(a)] += 1
    print(matrix)
    # Saving file
    matrix.to_csv("./Clean_data/Grouped_AOI_transition_matrix.tsv", sep='\t')


def tabs_for_hypo_1():
    path_tsv = "./Clean_data/Clean_by_users/"
    emotions = ['AFS', 'ANS', 'DIS', 'HAS', 'NES', 'SAS', 'SUS']
    images = ['AF01', 'AF22', 'AF28', 'AM04', 'AM09', 'AM14']

    # Retrieving image file names =========================================
    imgs = []
    path_img = "C:/Users/Karim/Documents/GitHub/eyeTrackingWebPage/images_moins_3"
    for file in os.listdir(path_img):
        if file.endswith("S.JPG"):
            imgs.append(file)
    # ======================================================================

    # Creating Emo_Img_By_Users
    for file in os.listdir(path_tsv):
        if file.endswith(".tsv"):
            print("user : ", file, " ==================")
            df_emo = pd.DataFrame(np.zeros(shape=(len(emotions), len(images))), index=emotions, columns=images)
            # print(df_emo)
            data = pd.read_csv(path_tsv + file, sep='\t', header=0)
            for img in imgs:
                data_img = data[data['MediaName'].str.contains(img)]
                column = re.search('(.*\d\d)', img).group(1)
                row = re.search('\d\d(.+?).JPG', img).group(1)
                # print(row, ' _ ', column, ' _ ', len(set(data_img['FixationIndex'])))
                df_emo.at[row, column] += len(set(data_img['FixationIndex']))
                # print(img, " - ", , " - ", data_emo['FixationIndex'].count())
            print("==============================================")
            print(df_emo)

            # Saving file
            df_emo.to_csv("./Clean_data/Clean_Emo_Img_By_Users/Emo_Img_" + file, sep='\t')


def tabs():

    path_tsv = "./Clean_data/Clean_by_users/"
    emotions = ['AFS', 'ANS', 'DIS', 'HAS', 'NES', 'SAS', 'SUS']
    images = ['AF01', 'AF22', 'AF28', 'AM04', 'AM09', 'AM14']
    users = ['2', '3', '4', '5', '6', '7', '8', '9',
             '10', '12', '13', '14']

    # Retrieving image file names =========================================
    imgs = []
    path_img = "C:/Users/Karim/Documents/GitHub/eyeTrackingWebPage/images_moins_3"
    for file in os.listdir(path_img):
        if file.endswith("S.JPG"):
            imgs.append(file)
    # ======================================================================

    # Creating Emo_Img_All_Users
    # Create column names
    all_images = []
    for i in range(2, 15):
        if i != 11:
            all_images += [c+"_"+str(i) for c in images]

    # print(all_images)
    df_emo = pd.DataFrame(np.zeros(shape=(len(emotions), len(users))),
                          index=emotions, columns=users)
    for file in os.listdir(path_tsv):
        if file.endswith(".tsv"):
            print("user : ", file, " ==================")
            # print(df_emo)
            data = pd.read_csv(path_tsv+file, sep='\t', header=0)
            for img in imgs:
                data_img = data[data['MediaName'].str.contains(img)]
                column = re.search('Data_(.*)\.tsv', file).group(1)
                row = re.search('\d\d(.+?).JPG', img).group(1)
                # print(row, ' _ ', column, ' _ ', len(set(data_img['FixationIndex'])))
                df_emo.at[row, column] += len(set(data_img['FixationIndex']))
                # print(img, " - ", , " - ", data_emo['FixationIndex'].count())
            print("==============================================")

    print(df_emo)
    # Saving file
    df_emo.to_csv("./Clean_Emo_Img_All_Users.tsv", sep='\t')


def corsH1():
    path = './Clean_data/Clean_aoi_paths/'
    df_corsH1 = pd.DataFrame(columns=['AOI', 'Position'])
    i = 0
    for file in os.listdir(path):
        if file.endswith(".tsv"):
            data = pd.read_csv(path+file, sep='\t', header=0)
            # print(data)
            for col in list(data.columns[1:].values):
                items = data[:][col]
                for it in items.dropna():
                    if 'oeil' in it:
                        df_corsH1 = df_corsH1.append({'AOI' : 'oeil', 'Position' : int(col)+1}, ignore_index=True)
                    elif 'joueH' in it:
                        df_corsH1 = df_corsH1.append({'AOI' : 'joueH', 'Position' : int(col)+1}, ignore_index=True)
                    elif 'joueB' in it:
                        df_corsH1 = df_corsH1.append({'AOI' : 'joueB', 'Position' : int(col)+1}, ignore_index=True)
                    else:
                        df_corsH1 = df_corsH1.append({'AOI' : it, 'Position' : int(col)+1}, ignore_index=True)
                # print(col)
            print(df_corsH1)
    df_corsH1.to_csv("./Clean_data/corsH1.tsv", sep="\t")


def create_aoi_symetric_transition_matrix():

    file = "./Clean_data/AOI_paths_global.tsv"
    zones = ['front', 'nez', 'bouche', 'menton', 'joueH_D', 'joueH_G', 'joueB_D', 'joueB_G', 'oeil_D', 'oeil_G']
    grouped_zones = ['front', 'nez', 'bouche', 'menton', 'joueH', 'joueB', 'oeil']
    zone_dict = {'front': 'front', 'oeil_D': 'oeil', 'oeil_G': 'oeil',
                 'nez': 'nez', 'joueH_D': 'joueH', 'joueH_G': 'joueH',
                 'bouche': 'bouche', 'menton': 'menton', 'joueB_D': 'joueB',
                 'joueB_G': 'joueB'}
    data = pd.read_csv(file, sep='\t', header=0)
    matrix = pd.DataFrame(np.zeros(shape=(len(grouped_zones), len(grouped_zones)), dtype=int),
                              index=grouped_zones, columns=grouped_zones)

    for index, row in data.iterrows():
        temp = "empty"
        for e, a in row.iteritems():
            if a in zones:
                if temp == 'empty':
                    temp = a
                else:
                    matrix.at[zone_dict.get(temp), zone_dict.get(a)] += 1
    print(matrix)
    # Saving file
    matrix.to_csv("./Clean_data/Symetric_AOI_transition_matrix.tsv", sep='\t')


def create_aoi_sym_transMat_users():

    path = "./Clean_data/Clean_aoi_paths/"
    zones = ['front', 'nez', 'bouche', 'menton', 'joueH_D', 'joueH_G', 'joueB_D', 'joueB_G', 'oeil_D', 'oeil_G']
    grouped_zones = ['front', 'nez', 'bouche', 'menton', 'joueH', 'joueB', 'oeil']
    zone_dict = {'front': 'front', 'oeil_D': 'oeil', 'oeil_G': 'oeil',
                 'nez': 'nez', 'joueH_D': 'joueH', 'joueH_G': 'joueH',
                 'bouche': 'bouche', 'menton': 'menton', 'joueB_D': 'joueB',
                 'joueB_G': 'joueB'}
    for file in os.listdir(path):
        if file.endswith(".tsv"):
            matrix = pd.DataFrame(np.zeros(shape=(len(grouped_zones), len(grouped_zones)), dtype=int),
                              index=grouped_zones, columns=grouped_zones)
            data = pd.read_csv(path+file, sep='\t', header=0)
            # print(data)
            for index, row in data.iterrows():
                temp = "empty"
                for e, a in row.iteritems():
                    if a in zones:
                        if temp == 'empty':
                            temp = a
                        else:
                            matrix.at[zone_dict.get(temp), zone_dict.get(a)] += 1
            print(matrix)
            # Saving file
            user = re.search('(\d+)', file).group(1)
            matrix.to_csv("./Clean_data/Sym_AOI_TransMat_By_Users/TransMat_User_"+user+".tsv", sep='\t')


def create_aoi_sym_transMat_emotions():

    path = "./Clean_data/Clean_aoi_paths/"
    zones = ['front', 'nez', 'bouche', 'menton', 'joueH_D', 'joueH_G', 'joueB_D', 'joueB_G', 'oeil_D', 'oeil_G']
    grouped_zones = ['front', 'nez', 'bouche', 'menton', 'joueH', 'joueB', 'oeil']
    zone_dict = {'front': 'front', 'oeil_D': 'oeil', 'oeil_G': 'oeil',
                 'nez': 'nez', 'joueH_D': 'joueH', 'joueH_G': 'joueH',
                 'bouche': 'bouche', 'menton': 'menton', 'joueB_D': 'joueB',
                 'joueB_G': 'joueB'}
    emotions = ['AFS', 'ANS', 'DIS', 'HAS', 'NES', 'SAS', 'SUS']
    for emo in emotions:
        matrix = pd.DataFrame(np.zeros(shape=(len(grouped_zones), len(grouped_zones)), dtype=int),
                          index=grouped_zones, columns=grouped_zones)
        for file in os.listdir(path):
            if file.endswith(".tsv"):
                data = pd.read_csv(path+file, sep='\t', header=0)
                # print(data)
                for index, row in data.iterrows():
                    # print(index, ' = ', row)
                    temp = "empty"
                    if emo in row[0]:
                        print(emo, ' = ', row[0])
                        for e, a in row.iteritems():
                            # print(e, ' === ', a)
                            # if emo in a:
                            if a in zones:
                                if temp == 'empty':
                                    temp = a
                                else:
                                    matrix.at[zone_dict.get(temp), zone_dict.get(a)] += 1
        print(matrix)
        # Saving file
        matrix.to_csv("./Clean_data/Sym_AOI_TransMat_By_Emotions/TransMat_Emotion_"+emo+".tsv", sep='\t')

# remove_first_three()
# creat_aoi_paths()
# create_aoi_paths_global()
# create_aoi_transition_matrix()
# create_aoi_grouped_transition_matrix()
# tabs()
# corsH1()
# create_aoi_symetric_transition_matrix()
create_aoi_sym_transMat_emotions()
