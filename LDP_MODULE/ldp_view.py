import streamlit as st
import pandas as pd
import os
import numpy as np
import PROJECTS.config as module_config
import altair as alt
import plotly.express as px
from PROJECTS.module_view import query_to_dataframe

@st.cache_data
def load_data_ldp():
    conn = module_config.connect_to_mysql()
    try:
        thuchien = query_to_dataframe(f"SELECT * FROM thuchien;", conn)
        # thuchien_year = query_to_dataframe(f"SELECT * FROM thuchien WHERE type_process = 'LDPVNPT';", conn)
        kehoach = query_to_dataframe(f"SELECT * FROM kehoach_linelv;", conn)
        # kehoach_year = query_to_dataframe(f"SELECT * FROM kehoach_linelv WHERE type_process = 'LDPVNPT';", conn)
        nhanvien = query_to_dataframe("SELECT * FROM nhanvien", conn)
        dichvu = query_to_dataframe("SELECT * FROM dichvu", conn)
        line = query_to_dataframe("SELECT * FROM line_manage WHERE ma_line != 'LDPVNPT';", conn)
        for month in range(1, 13):
            kehoach[f"t{month}"] = kehoach[f"t{month}"] * 1000000
        # for month_y in range(1, 13):
        #     kehoach_year[f"t{month_y}"] = kehoach_year[f"t{month_y}"] * 1000000
        kehoach["LK_năm"] = kehoach["LK_năm"]*1000000
        # kehoach_year["LK_năm"] = kehoach_year["LK_năm"]*1000000
        return thuchien, kehoach, nhanvien, dichvu, line
    finally:
        conn.close()
def build_hierarchy(df):
    if not {'ma_dv_id66', 'ten_dv', 'danh_muc_tt'}.issubset(df.columns):
        raise ValueError("DataFrame phải có các cột 'ma_dv_id66', 'ten_dv', và 'danh_muc_tt'")
    
    df['full_path'] = df['ten_dv']

    def build_full_path(row, df):
        if pd.isna(row['danh_muc_tt']):
            return row['ten_dv']
        else:
            parent_row = df[df['ma_dv_id66'] == row['danh_muc_tt']]
            if not parent_row.empty:
                parent_full_path = parent_row['full_path'].values[0]
                return f"{parent_full_path}.{row['ten_dv']}"
            return row['ten_dv']

    df['full_path'] = df.apply(lambda row: build_full_path(row, df), axis=1)

    df_all = df.sort_values(by=['ma_dv_id66', 'full_path'])
    
    df_filtered = df[df['ma_dv_id66'].str.count('\.') <= 2]
    df_filtered = df_filtered.reset_index(drop=True)
    
    return df_all[['ma_dv_id66', 'ten_dv', 'full_path']], df_filtered[['ma_dv_id66', 'ten_dv', 'full_path']]

def sorted_service_from_db(df_all_2):
    ma_dv_1 = df_all_2['ma_dv_id66'].tolist()
    ten_dv_1 = df_all_2['ten_dv'].tolist()
    return ma_dv_1, ten_dv_1


def create_dataframe_thuchien_tt(thang, ma_dv, ten_dv):
    ke_hoach_col = f"KẾ HOẠCH T{thang:02d}"
    thuc_hien_col = f"THỰC HIỆN T{thang:02d}"
    if thang == 1:
        thuc_hien_col = "THỰC HIỆN T1"
    columns = ["STT", "Dịch vụ", ke_hoach_col, thuc_hien_col, "% THỰC HIỆN", "KỲ TRƯỚC", "% VỚI KỲ TRƯỚC", "+/- VỚI KỲ TRƯỚC", "THỰC HIỆN T01", "% THỰC HIỆN T01", "+ /- VỚI T01"]

    # Dữ liệu
    data = {
        "STT": [*ma_dv],
        "Dịch vụ": [*ten_dv],
    }

    for col in columns[2:]:
        data[col] = [None] * len(data["STT"])

    # Tạo DataFrame
    kq_thuchien = pd.DataFrame(data, columns=columns)
    return kq_thuchien, ke_hoach_col, thuc_hien_col
def map_kehoach_to_thuchien_tt(kehoach_after_filter,df_new_create_form_1,ke_hoach_col, thang):
        for index, row in kehoach_after_filter.iterrows():
            service = row["ten_dv"]

            # Tìm vị trí của dịch vụ trong df_new_create_form_1
            matching_rows = df_new_create_form_1[df_new_create_form_1["Dịch vụ"] == service]

            # Nếu có ít nhất một hàng khớp, ánh xạ dữ liệu
            if not matching_rows.empty:
                matching_index = matching_rows.index[0]
                df_new_create_form_1.loc[matching_index, ke_hoach_col] = row[f"t{thang}"] / 1000000
            else:
                print(f"Dịch vụ '{service}' không được tìm thấy trong DataFrame 'df_new_create_form_1'.")
        return df_new_create_form_1
def map_thuchien_tt_for_form(column_data, kq_thuchien_tt, kq_thuchien):
    for index, row in kq_thuchien_tt.iterrows():
        service = row['nhom_dv']

        # Tìm vị trí của dịch vụ trong kq_thuchien
        matching_rows = kq_thuchien[kq_thuchien["STT"] == service]

        # Nếu có ít nhất một hàng khớp, ánh xạ dữ liệu
        if not matching_rows.empty:
            matching_index = matching_rows.index[0]
            # Cập nhật giá trị tương ứng trong cột
            column_name = column_data.name
            kq_thuchien.at[matching_index, column_name] = row.iloc[1] / 1000000
        else:
            print(f"Dịch vụ '{service}' không được tìm thấy trong DataFrame 'kq_thuchien'.")
    
    return kq_thuchien
def update_summary_rows(df):
    df['STT'] = df['STT'].astype(str)

    columns_to_sum = df.columns[2:]

    def get_child_rows(df, parent_stt):
        return df[df['STT'].str.startswith(parent_stt + '.')]

    for index, row in df.iterrows():
        if pd.isna(row[columns_to_sum]).all() or (row[columns_to_sum] == 0).all():

            child_rows = get_child_rows(df, row['STT'])

            if not child_rows.empty:
                df.loc[index, columns_to_sum] = child_rows[columns_to_sum].sum()

    for index, row in df.iterrows():
        if row['STT'] == '0':
            row_1 = df[df['STT'] == '1'].iloc[:, 2:].sum()
            row_2 = df[df['STT'] == '2'].iloc[:, 2:].sum()

            df.loc[index, columns_to_sum] = row_1 + row_2

    return df
def update_form_1_table(kq_dataframe, thuc_hien_col, ke_hoach_col):
    
    kq_dataframe = kq_dataframe.fillna(0).infer_objects(copy=False)
    kq_dataframe['% THỰC HIỆN'] = np.where(kq_dataframe[ke_hoach_col] != 0,
                                        kq_dataframe[thuc_hien_col] / kq_dataframe[ke_hoach_col] * 100,
                                        0)


    kq_dataframe['% VỚI KỲ TRƯỚC'] = np.where(kq_dataframe['KỲ TRƯỚC'] != 0,
                                            kq_dataframe[thuc_hien_col] / kq_dataframe['KỲ TRƯỚC'] * 100,
                                            0)
    kq_dataframe['+/- VỚI KỲ TRƯỚC'] = kq_dataframe[thuc_hien_col] - kq_dataframe['KỲ TRƯỚC']

    kq_dataframe['% THỰC HIỆN T01'] = np.where(kq_dataframe['THỰC HIỆN T01'] != 0,
                                            kq_dataframe[thuc_hien_col] / kq_dataframe['THỰC HIỆN T01'] * 100,
                                            0)

    kq_dataframe['+ /- VỚI T01'] = kq_dataframe[thuc_hien_col] - kq_dataframe['THỰC HIỆN T01']


    return kq_dataframe
    # END FORM 1
    # FORM 2
def create_dataframe_form_2(ma_dv, ten_dv):
    columns = ["STT", "Dịch vụ"] + [f"Tháng {i:02d}" for i in range(1, 13)]

    data = {
        "STT": [*ma_dv],
        "Dịch vụ": [*ten_dv],
    }

    # Tạo DataFrame
    kq_dataframe = pd.DataFrame(data, columns=columns)

    return kq_dataframe
def map_thuchien_to_form_2(kq_thuchien, kq_dataframe):
    for index, row in kq_thuchien.iterrows():
        service = row['nhom_dv']
        month = row['thang']
        revenue = row['doanhthu']

        matching_rows = kq_dataframe[kq_dataframe["STT"] == service]

        if not matching_rows.empty:
            matching_index = matching_rows.index[0]
            kq_dataframe.at[matching_index, f"Tháng {int(month):02d}"] = revenue/1000000
        else:
            print(f"Dịch vụ '{service}' không được tìm thấy trong DataFrame 'kq_dataframe'.")
    
    return kq_dataframe
    # END FORM 2
    # FORM 3
def map_kehoach_to_form_3(kq_kehoach, kq_dataframe):
        for index, row in kq_kehoach.iterrows():
            service = row["ten_dv"]
            matching_rows = kq_dataframe[kq_dataframe["Dịch vụ"] == service]

            if not matching_rows.empty:
                matching_index = matching_rows.index[0]
                kq_dataframe.iloc[matching_index, 2:] = row[1:].values / 1000000
            else:
                print(f"Dịch vụ '{service}' không được tìm thấy trong DataFrame 'kq_dataframe'.")

        return kq_dataframe
    
def flag_row_form_bold(df):
    df = pd.DataFrame(df)
    bold_indices = []
    for index, row in df.iterrows():
        if row['ma_dv_id66'].count('.') <= 1:
            bold_indices.append(index+1)
    return bold_indices