import streamlit as st
import pandas as pd
import os
import numpy as np
import PROJECTS.config as module_config
import altair as alt
import plotly.express as px
import PROJECTS.module_view as module_view


def filter_data_show(df,month,year,loaidoanhthu,type_process):
        df = df[(df["type_process"] == type_process) &
            (df["year_insert"] == year)]
        if loaidoanhthu is not None and month is None:
            df = df[df["loaidoanhthu"] == loaidoanhthu]
        elif loaidoanhthu is None and month is not None:
            df = df[df["thang"] == month]
        else:
            df = df[(df["loaidoanhthu"] == loaidoanhthu) & (df["thang"] == month)]
        return df
def metric_show_result_for_board(thuchien_after_load,selected_month,selected_year,selection_line=None):
    metric_01_ldp_yearsum_hh = filter_data_show(thuchien_after_load,None,selected_year,"Hiện hữu","LINE")
    delta_metric_01_ldp_yearsum_hh = filter_data_show(thuchien_after_load,None,selected_year - 1,"Hiện hữu","LINE")
    metric_02_ldp_yearsum_ptm = filter_data_show(thuchien_after_load,None,selected_year,"Phát triển mới","LINE")
    delta_metric_02_ldp_yearsum_ptm = filter_data_show(thuchien_after_load,None,selected_year - 1,"Phát triển mới","LINE")
    metric_03_ldp_monthsum_hh = filter_data_show(thuchien_after_load,selected_month,selected_year,"Hiện hữu","LINE")
    delta_metric_03_ldp_monthsum_hh = filter_data_show(thuchien_after_load,selected_month - 1,selected_year,"Hiện hữu","LINE")
    metric_04_ldp_monthsum_ptm = filter_data_show(thuchien_after_load,selected_month,selected_year,"Phát triển mới","LINE")
    delta_metric_04_ldp_monthsum_ptm = filter_data_show(thuchien_after_load,selected_month - 1,selected_year,"Phát triển mới","LINE")
    if selection_line is not None:
        metric_01_ldp_yearsum_hh = metric_01_ldp_yearsum_hh[metric_01_ldp_yearsum_hh["line"] == selection_line]
        delta_metric_01_ldp_yearsum_hh = delta_metric_01_ldp_yearsum_hh[delta_metric_01_ldp_yearsum_hh["line"] == selection_line]
        metric_02_ldp_yearsum_ptm = metric_02_ldp_yearsum_ptm[metric_02_ldp_yearsum_ptm["line"] == selection_line]
        delta_metric_02_ldp_yearsum_ptm = delta_metric_02_ldp_yearsum_ptm[delta_metric_02_ldp_yearsum_ptm["line"] == selection_line]
        metric_03_ldp_monthsum_hh = metric_03_ldp_monthsum_hh[metric_03_ldp_monthsum_hh["line"] == selection_line]
        delta_metric_03_ldp_monthsum_hh = delta_metric_03_ldp_monthsum_hh[delta_metric_03_ldp_monthsum_hh["line"] == selection_line]
        metric_04_ldp_monthsum_ptm = metric_04_ldp_monthsum_ptm[metric_04_ldp_monthsum_ptm["line"] == selection_line]
        delta_metric_04_ldp_monthsum_ptm = delta_metric_04_ldp_monthsum_ptm[delta_metric_04_ldp_monthsum_ptm["line"] == selection_line]
    metric_01_ldp_yearsum_hh_value = metric_01_ldp_yearsum_hh["doanhthu"].sum()
    metric_02_ldp_yearsum_ptm_value = metric_02_ldp_yearsum_ptm["doanhthu"].sum()
    metric_03_ldp_monthsum_hh_value = metric_03_ldp_monthsum_hh["doanhthu"].sum()
    metric_04_ldp_monthsum_ptm_value = metric_04_ldp_monthsum_ptm["doanhthu"].sum()
    
    delta_metric_01_ldp_yearsum_hh_value = metric_01_ldp_yearsum_hh_value - delta_metric_01_ldp_yearsum_hh["doanhthu"].sum() if delta_metric_01_ldp_yearsum_hh is not None else metric_01_ldp_yearsum_hh_value
    delta_metric_02_ldp_yearsum_ptm_value = metric_02_ldp_yearsum_ptm_value - delta_metric_02_ldp_yearsum_ptm["doanhthu"].sum() if delta_metric_02_ldp_yearsum_ptm is not None else metric_02_ldp_yearsum_ptm_value
    delta_metric_03_ldp_monthsum_hh_value = metric_03_ldp_monthsum_hh_value - delta_metric_03_ldp_monthsum_hh["doanhthu"].sum() if delta_metric_03_ldp_monthsum_hh is not None else metric_03_ldp_monthsum_hh_value
    delta_metric_04_ldp_monthsum_ptm_value = metric_04_ldp_monthsum_ptm_value - delta_metric_04_ldp_monthsum_ptm["doanhthu"].sum() if delta_metric_04_ldp_monthsum_ptm is not None else metric_04_ldp_monthsum_ptm_value
    
    metric_01_ldp_yearsum_hh = module_view.format_number(metric_01_ldp_yearsum_hh_value)
    metric_02_ldp_yearsum_ptm = module_view.format_number(metric_02_ldp_yearsum_ptm_value)
    metric_03_ldp_monthsum_hh = module_view.format_number(metric_03_ldp_monthsum_hh_value)
    metric_04_ldp_monthsum_ptm = module_view.format_number(metric_04_ldp_monthsum_ptm_value)
    
    delta_metric_01_ldp_yearsum_hh = module_view.format_number(delta_metric_01_ldp_yearsum_hh_value)
    delta_metric_02_ldp_yearsum_ptm = module_view.format_number(delta_metric_02_ldp_yearsum_ptm_value)
    delta_metric_03_ldp_monthsum_hh = module_view.format_number(delta_metric_03_ldp_monthsum_hh_value)
    delta_metric_04_ldp_monthsum_ptm = module_view.format_number(delta_metric_04_ldp_monthsum_ptm_value)
    return metric_01_ldp_yearsum_hh,delta_metric_01_ldp_yearsum_hh,metric_02_ldp_yearsum_ptm,delta_metric_02_ldp_yearsum_ptm,metric_03_ldp_monthsum_hh,delta_metric_03_ldp_monthsum_hh,metric_04_ldp_monthsum_ptm,delta_metric_04_ldp_monthsum_ptm
def line_chart_view_board_ldp(thuchien_after_load,selected_year,loaidoanhthu,selection_line=None):
    data = filter_data_show(thuchien_after_load,None,selected_year,loaidoanhthu,"LINE")
    if not data.empty:
        if selection_line is not None:
            data = data[data["line"] == selection_line]
        data = pd.DataFrame(data)
        data_groupby = data.groupby(["thang","loaidoanhthu"])["doanhthu"].sum().reset_index()
        selection = alt.selection_point(fields=['thang'], empty="none")
        line_chart = alt.Chart(data_groupby).mark_line(point=True).encode(
            x=alt.X('thang:O', title='Tháng',
                    axis=alt.Axis(
                    titleFontSize=14, 
                    titleColor='rgb(0, 50, 73)', 
                    labelFontSize=12, 
                    labelColor='rgb(0, 50, 73)' 
                )),
            y=alt.Y('doanhthu:Q', title='Doanh thu', axis=alt.Axis(
            titleFontSize=14,  
            titleColor='rgb(0, 50, 73)',
            labelFontSize=12,  
            labelColor='rgb(0, 50, 73)'
        )),
            tooltip=['thang', 'doanhthu', 'loaidoanhthu']
        ).properties(
            height=300,
            title=['Doanh thu theo tháng']
        ).add_params(selection)
        return line_chart
    else:
        return None
def Pie_chart_ldp_view_board(thuchien_after_load,line_manage,selected_year,loaidoanhthu,selected_month = None):
    if selected_month is not None:
        data = filter_data_show(thuchien_after_load,selected_month,selected_year,loaidoanhthu,"LINE")
    else:
        data = filter_data_show(thuchien_after_load,None,selected_year,loaidoanhthu,"LINE")
    data["ten_line"] = data["line"].map(line_manage.set_index("ma_line")["ten_line"])
    if not data.empty:
        data = pd.DataFrame(data)
        data_groupby = data.groupby(["line","ten_line","loaidoanhthu"])["doanhthu"].sum().reset_index()
        selection = alt.selection_point(fields=['line'], empty="none")
        data_groupby['percentage'] = data_groupby['doanhthu'] / data_groupby['doanhthu'].sum() * 100
        pie_chart = alt.Chart(data_groupby).mark_arc().encode(
            theta=alt.Theta(field="percentage", type="quantitative"),
            color=alt.Color(field="ten_line", type="nominal"),
            tooltip=['ten_line', 'doanhthu',"percentage"]
        ).properties(
            height=300,
            title=['Tỷ lệ doanh thu theo line']
        ).add_params(selection)
        return pie_chart
    else:
        return None
def table_show_right_ldp(thuchien_after_load,kehoach_after_load,dichvu_after_load,selected_year,loaidoanhthu,selected_line=None,selected_month = None):
    data_kehoach =  kehoach_after_load[(kehoach_after_load["type_process"] == "LINE") &
            (kehoach_after_load["year_insert"] == selected_year)]
    if selected_month is not None:
        data = filter_data_show(thuchien_after_load,selected_month,selected_year,loaidoanhthu,"LINE")
        data_kehoach = data_kehoach[["line",f"t{selected_month}","loaidoanhthu","id_dv_606"]]
        
    if selected_line is not None:
        data = data[data["line"] == selected_line]
        data_kehoach = data_kehoach[data_kehoach["line"] == selected_line]
        
    data = data.groupby(["nhom_dv"])["doanhthu"].sum().reset_index()
    data_kehoach = (data_kehoach.groupby("id_dv_606")[f"t{selected_month}"].sum().reset_index(name="doanhthu"))
    data_kehoach = data_kehoach.rename(columns={"id_dv_606": "nhom_dv"})
    merged_data = pd.merge(data, data_kehoach, on="nhom_dv", how="left")
    
    merged_data["percentage"] = (merged_data["doanhthu_x"] / merged_data["doanhthu_y"]) * 100
    merged_data["nhom_dv"] = merged_data["nhom_dv"].map(dichvu_after_load.set_index("ma_dv_id66")["ten_dv"])
    merged_data = merged_data[["nhom_dv","percentage"]]
    return merged_data
