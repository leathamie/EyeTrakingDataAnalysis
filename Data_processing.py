import pandas as pd
import os

path = "C:/Users/Karim/Desktop/expe/expe/" #Changer le path selon l'emplacement du dossier dan votre machine

# Columns to be dropped
columns_list = ['ExportDate', 'StudioVersionRec', 'StudioProjectName', 'StudioTestName',
                'RecordingName', 'RecordingDate', 'RecordingDuration', 'RecordingResolution',
                'FixationFilter', 'MediaPosX (ADCSpx)', 'MediaPosY (ADCSpx)',
                'MediaWidth', 'MediaHeight', 'SegmentName', 'SegmentStart', 'SegmentEnd',
                'SegmentDuration', 'SceneName', 'SceneSegmentStart', 'SceneSegmentEnd',
                'SceneSegmentDuration', 'MouseEventIndex', 'MouseEvent', 'MouseEventX (ADCSpx)',
                'MouseEventY (ADCSpx)', 'MouseEventX (MCSpx)', 'MouseEventY (MCSpx)',
                'KeyPressEventIndex', 'KeyPressEvent', 'StudioEventIndex', 'StudioEvent',
                'StudioEventData', 'ExternalEventIndex', 'ExternalEvent', 'ExternalEventValue',
                'EventMarkerValue', 'CamLeftX', 'CamLeftY', 'CamRightX', 'CamRightY', 'IRMarkerCount',
                'IRMarkerID', 'PupilGlassesRight']

# Columns to be merged
columns_merge = ['AOI[bouche]Hit', 'AOI[nez]Hit', 'AOI[oeil_D]Hit', 'AOI[oeil_G]Hit',
                 'AOI[joueH_G]Hit', 'AOI[joueH_D]Hit', 'AOI[joueB_G]Hit', 'AOI[menton]Hit',
                 'AOI[joueB_D]Hit', 'AOI[front]Hit']

# Processing all files
for file in os.listdir(path):
    if file.endswith(".csv"):
        # Reading files
        data = pd.read_csv(path+file, sep=';', header=0)

        # Step1: Dropping columns======================================
        data = data.drop(columns_list, axis=1)
        print(file, " : dropping columns done!")
        # ============================================================

        # Step2: Merging and droping columns =========================
        print(file, " : merging!")
        for c in columns_merge:
            cols = [col for col in data.columns if c in col]
            temp = data[cols].apply(
                lambda x: ''.join(x.dropna().astype(int).astype(str)),
                axis=1
            )

            # converting to int and filling empty cells
            temp2 = pd.Series()
            for i in range(len(temp)):
                if temp.get(i) != "":
                    temp2.at[i] = int(temp.get(i))
                else:
                    temp2.at[i] = 0

            data = data.drop(cols, axis=1)
            data[c] = temp2
            print(file, " : done : ", c)

        # =============================================================

        # Dropping unnecessary rows ==================================
        data = data.dropna(subset=['MediaName'])
        data = data[data['MediaName'].str.contains("pages")]
        print(file, " : dropping rows done!")

        # Saving file
        data.to_csv(file, index=False)

        print(file, " : merging and dropping done!")
        print(file, " : Saved!")

        # =============================================================

# Dropping additional columns
file = "Grp_A_eyesTracking_emotions_Data_Export6.csv"
additional_columns = ['SaccadeIndex', 'AOI[menton ]Hit', 'AOI[joueB_G 2]Hit', 'AOI[joueB_G 2]Hit.1',
                      'AOI[joueB_G 2]Hit.2']
data = pd.read_csv("C:/Users/Karim/Documents/GitHub/EyeTrakingDataAnalysis/"+file, sep=',', header=0)

print(data.iloc[0])
# Step1: Dropping columns======================================
data = data.drop(additional_columns, axis=1)
print(file, " : dropping columns done!")
# Saving file
data.to_csv("Grp_A_eyesTracking_emotions_Data_Export6.tsv", index=False)

# Splitting by users =========================================================
path = "C:/Users/Karim/Documents/GitHub/EyeTrakingDataAnalysis/Grp_A_eyesTracking_emotions_Data_Export6.tsv" #Changer le path selon l'emplacement du dossier dan votre machine
for i in range(12, 15):
    data = pd.read_csv(path, sep=',', header=0)
    # Step1: Dropping columns======================================
    data = data.dropna(subset=['ParticipantName'])
    data = data[data['ParticipantName'].str.contains(str(i))]
    print(i, " : dropping rows done!")
    # =============================================================
    data.to_csv("User_Data_"+str(i)+".tsv", index=False)
# =========================================================================

# Appending everything in one file =======================================
path = "C:/Users/Karim/Documents/GitHub/EyeTrakingDataAnalysis/"
all_data = pd.DataFrame()
for file in os.listdir(path):
    if file.startswith("Grp"):
        # Reading files
        all_data = all_data.append(pd.read_csv(path+file, sep=',', header=0))

all_data.to_csv("All_User_Data.tsv", index=False)
# ==========================================================================

# Splitting by images =========================================================
path = "C:/Users/Karim/Documents/GitHub/EyeTrakingDataAnalysis/All_User_Data.tsv" #Changer le path selon l'emplacement du dossier dan votre machine

# getting images names
path_img = "C:/Users/Karim/Documents/GitHub/eyeTrackingWebPage/images"
for file in os.listdir(path_img):
    if file.endswith("S.JPG"):
        data = pd.read_csv(path, sep=',', header=0)
        # Step1: Dropping columns======================================
        data = data.dropna(subset=['MediaName'])
        data = data[data['MediaName'].str.contains(file)]
        print(file, " : dropping rows done!")
        # =============================================================
        data.to_csv("Image_Data_"+file+".tsv", index=False)
# =========================================================================
