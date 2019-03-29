import pandas as pd
import numpy as np
import re
import os

# Path_file
path_tsv = "./By_users/"
path_img = "C:/Users/Karim/Documents/GitHub/eyeTrackingWebPage/images"

# Tableau d'emotion (affraid, angry, disgusted, happy, neutral, sad, suprised)
emotions = ['AFS', 'ANS', 'DIS', 'HAS', 'NES', 'SAS', 'SUS']
images = ['AF01', 'AF22', 'AF28', 'AM04', 'AM09', 'AM14']
imgs = []

# Retrieving image file names
for file in os.listdir(path_img):
    if file.endswith("S.JPG"):
        imgs.append(file)

# Creating Emo_Img_By_Users
# for file in os.listdir(path_tsv):
#     if file.endswith(".tsv"):
#         print("user : ", file, " ==================")
#         df_emo = pd.DataFrame(np.zeros(shape=(len(emotions), len(images))), index=emotions, columns=images)
#         # print(df_emo)
#         data = pd.read_csv(path_tsv+file, sep=',', header=0)
#         for img in imgs:
#             data_img = data[data['MediaName'].str.contains(img)]
#             column = re.search('(.*\d\d)', img).group(1)
#             row = re.search('\d\d(.+?).JPG', img).group(1)
#             # print(row, ' _ ', column, ' _ ', len(set(data_img['FixationIndex'])))
#             df_emo.at[row, column] += len(set(data_img['FixationIndex']))
#             # print(img, " - ", , " - ", data_emo['FixationIndex'].count())
#         print("==============================================")
#         print(df_emo)
#
#         # Saving file
#         df_emo.to_csv("./Emo_Img_By_Users/Emo_Img_"+file, sep='\t')

# Creating Emo_Img_All_Users
# Create column names
# all_images = []
# for i in range(1, 15):
#     if i != 11:
#         all_images += [c+"_"+str(i) for c in images]
#
# # print(all_images)
# df_emo = pd.DataFrame(np.zeros(shape=(len(emotions), len(all_images))),
#                       index=emotions, columns=all_images)
# for file in os.listdir(path_tsv):
#     if file.endswith(".tsv"):
#         print("user : ", file, " ==================")
#         # print(df_emo)
#         data = pd.read_csv(path_tsv+file, sep=',', header=0)
#         for img in imgs:
#             data_img = data[data['MediaName'].str.contains(img)]
#             column = re.search('(.*\d\d)', img).group(1) + "_" + re.search('Data_(.*)\.tsv', file).group(1)
#             row = re.search('\d\d(.+?).JPG', img).group(1)
#             # print(row, ' _ ', column, ' _ ', len(set(data_img['FixationIndex'])))
#             df_emo.at[row, column] += len(set(data_img['FixationIndex']))
#             # print(img, " - ", , " - ", data_emo['FixationIndex'].count())
#         print("==============================================")
#
# print(df_emo)
# # Saving file
# df_emo.to_csv("./Emo_Img_All_Users/Emo_Img_All_Users.tsv", sep='\t')


# Creating AOI_Jumps_By_Users
# columns_merge = {'AOI[bouche]Hit', 'AOI[nez]Hit', 'AOI[oeil_D]Hit', 'AOI[oeil_G]Hit',
#                  'AOI[joueH_G]Hit', 'AOI[joueH_D]Hit', 'AOI[joueB_G]Hit', 'AOI[menton]Hit',
#                  'AOI[joueB_D]Hit', 'AOI[front]Hit'}

for file in os.listdir(path_tsv):
    if file.endswith(".tsv"):
        print("user : ", file, " ==================")
        # df_emo = pd.DataFrame(index=imgs)
        all_jumps = []
        # print(df_emo)
        data = pd.read_csv(path_tsv+file, sep=',', header=0)
        # Dropping columns before AOI columns
        data = data.drop(data.ix[:, :'ParticipantName'].columns, axis=1)
        data = data.drop(data.ix[:, 'RecordingTimestamp':'ValidityRight'].columns, axis=1)
        for img in imgs:
            # print("============", img)
            data_img = data[data['MediaName'].str.contains(img)]
            # row = data[data['MediaName']]
            data_img = data_img.drop(data_img.ix[:, :'MediaName'].columns, axis=1)
            temp = ""
            jumps = []
            for row, column in data_img.iterrows():
                # print(type(column))
                for key, value in column.iteritems():
                    # print(key, " _ ", value)
                    if value == 1 and key != temp:
                        # print(value == 1)
                        # print(key == temp)
                        jumps.append(re.search('\[(.+?)\]', key).group(1))
                        temp = key
            # print(jumps)
            all_jumps += [jumps]
        print(all_jumps)
        df_emo = pd.DataFrame(all_jumps, index=imgs)
        print(df_emo)
        # Saving file
        df_emo.to_csv("./AOI_Jumps_By_Users/AOI_Jumps_"+file, sep='\t')
