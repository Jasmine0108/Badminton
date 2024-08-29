import os
import json
import pandas as pd
import numpy as np
class SumData:
    acc_x: np.ndarray
    acc_y: np.ndarray
    acc_z: np.ndarray
    ang_acc_x: np.ndarray
    ang_acc_y: np.ndarray
    ang_acc_z: np.ndarray

    def __init__(self):
        self.acc_x = np.zeros(125)
        self.acc_y = np.zeros(125)
        self.acc_z = np.zeros(125)
        self.ang_acc_x = np.zeros(125)
        self.ang_acc_y = np.zeros(125)
        self.ang_acc_z = np.zeros(125)

json_list = []
sum_data = SumData()

grade_comment_path= "public/grade_and_comment.csv"
df_grade_comment = pd.read_csv(grade_comment_path)
folder_path = "public/cut"

def create_json_file(file_name, file_number, swing_total):
    print('start create json file.', file_number)
    json_list.append({
        "檔名":file_name,
        "評語":str(df_grade_comment.at[file_number,'評語']),
        "揮拍軌跡正確度":str(df_grade_comment.at[file_number,'揮拍軌跡正確度']),
        "揮拍速度流暢度":str(df_grade_comment.at[file_number,'揮拍速度流暢度']),
        "手腕轉動時機正確度":str(df_grade_comment.at[file_number,'手腕轉動時機正確度']),
        "擊球時機正確度":str(df_grade_comment.at[file_number,'擊球時機正確度']),
        "擊球位置正確度":str(df_grade_comment.at[file_number,'擊球位置正確度']),
        "x軸平均加速度":list(np.around(sum_data.acc_x / swing_total, 3)),
        "y軸平均加速度":list(np.around(sum_data.acc_y / swing_total, 3)),
        "z軸平均加速度":list(np.around(sum_data.acc_z / swing_total, 3)),
        "x軸平均角加速度":list(np.around(sum_data.ang_acc_x / swing_total, 3)),
        "y軸平均角加速度":list(np.around(sum_data.ang_acc_y / swing_total, 3)),
        "z軸平均角加速度":list(np.around(sum_data.ang_acc_z / swing_total, 3))
    })
    
file_number = -1
swing_total = 0
pre_name='h001'
flag = False
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    split_name = file_name.split('.')[0].split('_')
    if split_name[2] == '1':
        if flag:
            file_number += 1
            create_json_file(pre_name, file_number, swing_total)
            pre_name = split_name[0]
            sum_data.acc_x = np.zeros(125); sum_data.acc_y = np.zeros(125); sum_data.acc_z = np.zeros(125)
            sum_data.ang_acc_x = np.zeros(125); sum_data.ang_acc_y = np.zeros(125); sum_data.ang_acc_z = np.zeros(125)
            swing_total = 0
        else:
            flag = True
    df = pd.read_csv(file_path, header=None)
    df.columns = ['時間','x軸平均加速度', 'y軸平均加速度', 'z軸平均加速度','x軸平均角加速度','y軸平均角加速度','z軸平均角加速度']
    acc_x = np.array(df['x軸平均加速度'].tolist())
    acc_y = np.array(df['y軸平均加速度'].tolist())
    acc_z = np.array(df['z軸平均加速度'].tolist())
    ang_acc_x = np.array(df['x軸平均角加速度'].tolist())
    ang_acc_y = np.array(df['y軸平均角加速度'].tolist())
    ang_acc_z = np.array(df['z軸平均角加速度'].tolist())

    sum_data.acc_x += acc_x; sum_data.acc_y += acc_y; sum_data.acc_z += acc_z
    sum_data.ang_acc_x += ang_acc_x; sum_data.ang_acc_y += ang_acc_y; sum_data.ang_acc_z += ang_acc_z
    
    if file_name == 'h203_55555_30':
        create_json_file(split_name, file_number, swing_total)
    swing_total += 1

# create new json file
output_file = f'public/grade_and_comment.json'
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(json_list, file, ensure_ascii=False, indent=4)
print('create json file successfully!')




