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
        thuchien = query_to_dataframe(f"SELECT id, nhom_dv,doanhthu,line,thang,year_insert,loaidoanhthu,type_process FROM thuchien;", conn)
        kehoach = query_to_dataframe(f"SELECT * FROM kehoach_linelv;", conn)
        nhanvien = query_to_dataframe("SELECT * FROM nhanvien", conn)
        dichvu = query_to_dataframe("SELECT * FROM dichvu", conn)
        line = query_to_dataframe("SELECT * FROM line_manage WHERE ma_line != 'LDPVNPT';", conn)
        
        columns_to_multiply = [f"t{month}" for month in range(1, 13)]
        kehoach[columns_to_multiply] *= 1000000
        return thuchien, kehoach, nhanvien, dichvu, line
    finally:
        conn.close()
@st.cache_data
def load_line_manage():
    conn = module_config.connect_to_mysql()
    try:
        line = query_to_dataframe("SELECT * FROM line_manage;", conn)
        return line
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

    df['level'] = df['STT'].apply(lambda x: x.count('.') if len(x.split('.')) > 1 else 0)
    columns_to_sum = df.columns[2:]  

    def get_child_rows(df, parent_stt):
        return df[df['STT'].str.startswith(parent_stt + '.')]

    for level in sorted(df[(df['level'] >=2)]['level'].unique(), reverse=True):
        for index, row in df[df['level'] == level].iterrows():
            child_rows = get_child_rows(df, row['STT'])
            
            if not child_rows.empty:
                for col in columns_to_sum:
                    child_sum = child_rows[col].sum()
                    if child_sum > 0 and (pd.isna(row[col]) or row[col] == 0):
                        df.loc[index, col] = child_sum
    for index, row in df[df['level'] == 1].iterrows(): 
            child_rows = df[(df['STT'].str.startswith(row['STT'])) & (df['level'] == 2)]
            for col in columns_to_sum:
                if not child_rows.empty:
                    child_sum = child_rows[col].sum()
                    if child_sum > 0 and (pd.isna(row[col]) or row[col] == 0):
                        df.loc[index, col] = child_sum
    for index, row in df[df['level'] == 0].iterrows():
        if row['STT'] != '0':  
            child_rows = df[(df['STT'].str.startswith(row['STT'] + '.')) & (df['level'] == 1)]
            
            for col in columns_to_sum:
                if not child_rows.empty:
                    child_sum = child_rows[col].sum()
                    df.loc[index, col] = child_sum  

    for index, row in df[df['STT'] == '0'].iterrows():
        row_1 = df[df['STT'] == '1'].iloc[:, 2:].sum()  
        row_2 = df[df['STT'] == '2'].iloc[:, 2:].sum()  
        df.loc[index, columns_to_sum] = row_1 + row_2
    df= df.drop(columns=['level'])

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

# PART FOR YEAR VIEW
def create_dataframe_form_1_year_view(thang, ma_dv, ten_dv):
    ke_hoach_col = f"KẾ HOẠCH T{thang:02d}"
    thuc_hien_col = f"THỰC HIỆN T{thang:02d}"
    if thang == 1:
        thuc_hien_col = "THỰC HIỆN T1"
    columns = ["STT", "Dịch vụ", ke_hoach_col, thuc_hien_col, "% THỰC HIỆN", "KẾ HOẠCH NĂM","% VỚI KH NĂM", "KỲ TRƯỚC", "% VỚI KỲ TRƯỚC", "+/- VỚI KỲ TRƯỚC","CÙNG KỲ", "% VỚI CÙNG KỲ", "+/- VỚI CÙNG KỲ"]
    columns_luyke = ["STT", "Dịch vụ", ke_hoach_col, thuc_hien_col, "% THỰC HIỆN","KẾ HOẠCH NĂM","% VỚI KH NĂM" , "CÙNG KỲ", "% VỚI CÙNG KỲ", "+/- VỚI CÙNG KỲ"]
    # Dữ liệu
    data = {
        "STT": [*ma_dv],
        "Dịch vụ": [*ten_dv],
    }

    for col in columns[2:]:
        data[col] = [None] * len(data["STT"])
    kq_thuchien = pd.DataFrame(data, columns=columns)
    for col in columns_luyke[2:]:
        data[col] = [None] * len(data["STT"])
    kq_luyke = pd.DataFrame(data, columns=columns_luyke)

    # Tạo DataFrame
    
    return kq_thuchien,kq_luyke, ke_hoach_col, thuc_hien_col
def update_form_1_year_view(kq_dataframe, thuc_hien_col, ke_hoach_col):
    
    kq_dataframe = kq_dataframe.fillna(0).infer_objects(copy=False)
    kq_dataframe['% THỰC HIỆN'] = np.where(kq_dataframe[ke_hoach_col] != 0,
                                        kq_dataframe[thuc_hien_col] / kq_dataframe[ke_hoach_col] * 100,
                                        0)

    if 'KỲ TRƯỚC' in kq_dataframe.columns:
        kq_dataframe['% VỚI KỲ TRƯỚC'] = np.where(kq_dataframe['KỲ TRƯỚC'] != 0,
                                                kq_dataframe[thuc_hien_col] / kq_dataframe['KỲ TRƯỚC'] * 100,
                                                0)
        kq_dataframe['+/- VỚI KỲ TRƯỚC'] = kq_dataframe[thuc_hien_col] - kq_dataframe['KỲ TRƯỚC']

    kq_dataframe['% VỚI KH NĂM'] = np.where(kq_dataframe['KẾ HOẠCH NĂM'] != 0,
                                        kq_dataframe[thuc_hien_col] / kq_dataframe['KẾ HOẠCH NĂM'] * 100,
                                        0)
        
    if 'CÙNG KỲ' in kq_dataframe.columns:
        kq_dataframe['% VỚI CÙNG KỲ'] = np.where(kq_dataframe['CÙNG KỲ'] != 0,
                                            kq_dataframe[thuc_hien_col] / kq_dataframe['CÙNG KỲ'] * 100,
                                            0)
        kq_dataframe['+/- VỚI CÙNG KỲ'] = kq_dataframe[thuc_hien_col] - kq_dataframe['CÙNG KỲ']
    

    return kq_dataframe
def sum_hienhuu_moitrongnam(kq_thuchien_baocao_hienhuu, kq_thuchien_baocao_moitrongnam, kq_thuchien_thangtruoc_hienhuu, kq_thuchien_thangtruoc_moitrongnam, kq_kehoach_baocao_hienhuu, kq_kehoach_baocao_moitrongnam, kq_thuchien_baocao_cungki_hienhuu, kq_thuchien_baocao_cungki_moitrongnam):
        
        kq_thuchien_doanhthu = pd.merge(
            kq_thuchien_baocao_hienhuu[['nhom_dv', 'doanhthu']],
            kq_thuchien_baocao_moitrongnam[['nhom_dv', 'doanhthu']],
            on='nhom_dv',
            how='outer',
            suffixes=('_tongdoanhthu', '_baocao_moitrongnam')
        )

        kq_thuchien_doanhthu['doanhthu_tongdoanhthu'] = kq_thuchien_doanhthu['doanhthu_tongdoanhthu'].fillna(0)
        kq_thuchien_doanhthu['doanhthu_baocao_moitrongnam'] = kq_thuchien_doanhthu['doanhthu_baocao_moitrongnam'].fillna(0)

        kq_thuchien_doanhthu['doanhthu'] = (
            kq_thuchien_doanhthu['doanhthu_tongdoanhthu']
            + kq_thuchien_doanhthu['doanhthu_baocao_moitrongnam']
        )
        kq_thuchien_doanhthu = kq_thuchien_doanhthu.groupby('nhom_dv', as_index=False).agg({'doanhthu': 'sum'})

        kq_thangtruoc_doanhthu = pd.merge(
            kq_thuchien_thangtruoc_hienhuu[['nhom_dv', 'doanhthu']],
            kq_thuchien_thangtruoc_moitrongnam[['nhom_dv', 'doanhthu']],
            on='nhom_dv',
            how='outer',
            suffixes=('_tongdoanhthu', '_baocao_moitrongnam')
        )

        kq_thangtruoc_doanhthu['doanhthu_tongdoanhthu'] = kq_thangtruoc_doanhthu['doanhthu_tongdoanhthu'].fillna(0)
        kq_thangtruoc_doanhthu['doanhthu_baocao_moitrongnam'] = kq_thangtruoc_doanhthu['doanhthu_baocao_moitrongnam'].fillna(0)

        kq_thangtruoc_doanhthu['doanhthu'] = (
            kq_thangtruoc_doanhthu['doanhthu_tongdoanhthu']
            + kq_thangtruoc_doanhthu['doanhthu_baocao_moitrongnam']
        )
        kq_thangtruoc_doanhthu = kq_thangtruoc_doanhthu.groupby('nhom_dv', as_index=False).agg({'doanhthu': 'sum'})

        kq_kehoach_doanhthu = kq_kehoach_baocao_hienhuu.copy()
        kq_kehoach_doanhthu.iloc[:, 1:] += kq_kehoach_baocao_moitrongnam.iloc[:, 1:].values


        kq_cungki_doanhthu = kq_thuchien_baocao_cungki_hienhuu.copy()
        kq_cungki_doanhthu.iloc[:, 1:] += kq_thuchien_baocao_cungki_moitrongnam.iloc[:, 1:].values

        return kq_thuchien_doanhthu, kq_thangtruoc_doanhthu, kq_kehoach_doanhthu, kq_cungki_doanhthu