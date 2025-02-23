import streamlit as st
import time
import LDP_MODULE.ldp_board as ldp_board
import EM_MODULE.config as module_config
import LDP_MODULE.ldp_view as ldp_view

# PART LOGIN 
if not st.session_state.get("is_logged_in", False):
    with st.spinner("🔐 Đang chuyển hướng đến trang đăng nhập..."):
        time.sleep(2)
    st.session_state.is_logged_in = False
    st.session_state.role_access_admin = False
    st.session_state.line_access = None
    st.switch_page("main.py")
    st.stop() 
# PART SET CONFIG
with open('src/style.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
with open('src/style_general.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
with open('src/style_board.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    
class BOARD_LDP():
    def __init__(self):
        self.month_select = {"Tháng 1" : 1,"Tháng 2" : 2,"Tháng 3" : 3,"Tháng 4" : 4,"Tháng 5" : 5,"Tháng 6" : 6,"Tháng 7" : 7,"Tháng 8" : 8,"Tháng 9" : 9,"Tháng 10" : 10,"Tháng 11" : 11,"Tháng 12" : 12}
        self.month_key_show = self.month_select.keys()
        
        self.unique_months = thuchien_after_load[(thuchien_after_load["year_insert"] == thuchien_after_load["year_insert"].unique().max()) &
                                                 (thuchien_after_load["type_process"] == "LINE")]["thang"].unique()
        self.unique_months = [int(month) for month in self.unique_months]
        self.max_month = max(self.unique_months)
        self.month_now_index = list(self.month_select.values()).index(self.max_month)
        self.year_select = thuchien_after_load["year_insert"].unique()
    
    def show_board_ldp(self):
        ctn_board_ldp_header = st.container(key="ctn_board_ldp_header")
        with ctn_board_ldp_header:
            cols_header_ldp = st.columns([1,1,0.5,0.5])
            display_name_home = st.session_state.display_name_vnpt if ('display_name_vnpt' in st.session_state and st.session_state.display_name_vnpt != None) else st.session_state.usernamevnpt
            cols_header_ldp[0].info(f"{display_name_home}!",icon=":material/emoji_people:")
            cols_header_ldp[1].info("VNPT PERFORMANCE INSIGHTS",icon=":material/grid_view:")
            selected_month = cols_header_ldp[2].selectbox(" ",options=self.month_key_show,
                                                            index=self.month_now_index,
                                                          key="selected_month_board_ldp")
            selected_month = self.month_select[selected_month]
            selected_year = cols_header_ldp[3].selectbox(" ",options=self.year_select,
                                                         index=list(self.year_select).index(self.year_select.max()),
                                                         key="selected_year_board_ldp")
        ctn_main_board_ldp = st.container(key="ctn_main_board_ldp")
        if "line_selection_board" not in st.session_state:
            st.session_state.line_selection_board = None
        with ctn_main_board_ldp:
            cols_main_board_ldp = st.columns([1,0.75])
            pills_loaidoanhthu_ldp_board = cols_main_board_ldp[1].pills(" ",["Hiện hữu","Phát triển mới"],default="Hiện hữu",key="pills_loaidoanhthu_ldp_board")
            with cols_main_board_ldp[0]:
                ctn_line_chart_ldp = st.container(key="ctn_line_chart_ldp")
                with ctn_line_chart_ldp:
                    line_chart_ldp_board = ldp_board.line_chart_view_board_ldp(thuchien_after_load,selected_year,pills_loaidoanhthu_ldp_board,st.session_state.line_selection_board)
                    if line_chart_ldp_board is not None:
                        selection_month_line_chart = st.altair_chart(line_chart_ldp_board,key="line_chart_ldp_board_altair",on_select="rerun",use_container_width=True)
                        if selection_month_line_chart["selection"]["param_1"] != {}:
                            selected_month = selection_month_line_chart["selection"]["param_1"][0]["thang"]
                ctn_pie_chart_ldp = st.container(key="ctn_pie_chart_ldp")
                with ctn_pie_chart_ldp:
                    pie_chart_ldp_board = ldp_board.Pie_chart_ldp_view_board(thuchien_after_load,line_after_load,selected_year,pills_loaidoanhthu_ldp_board,selected_month)
                    if pie_chart_ldp_board is not None:
                        selection_line_from_pie_chart = st.altair_chart(pie_chart_ldp_board,key="Pie_chart_ldp_board",on_select="rerun",use_container_width=True)
                        if selection_line_from_pie_chart["selection"]["param_1"] != {}:
                            st.session_state.line_selection_board = selection_line_from_pie_chart["selection"]["param_1"][0]["line"]
                        else:
                            st.session_state.line_selection_board = None
            with cols_main_board_ldp[1]:
                metric_01_ldp_yearsum_hh,delta_metric_01_ldp_yearsum_hh,metric_02_ldp_yearsum_ptm,\
                delta_metric_02_ldp_yearsum_ptm,metric_03_ldp_monthsum_hh,delta_metric_03_ldp_monthsum_hh,\
                metric_04_ldp_monthsum_ptm,delta_metric_04_ldp_monthsum_ptm  = ldp_board.metric_show_result_for_board(thuchien_after_load,selected_month,selected_year,st.session_state.line_selection_board)
                cols_metric_ldp_board = st.columns([1,1])
                with cols_metric_ldp_board[0]:
                    ctn_metric_ldp_board_01 = st.container(key="ctn_metric_ldp_board_01")
                    ctn_metric_ldp_board_01.metric("Doanh thu năm hiện hữu",
                                                   value=metric_01_ldp_yearsum_hh,
                                                   delta=delta_metric_01_ldp_yearsum_hh)
                    ctn_metric_ldp_board_02 = st.container(key="ctn_metric_ldp_board_02")
                    ctn_metric_ldp_board_02.metric("Doanh thu năm phát triển mới",
                                                   value=metric_02_ldp_yearsum_ptm,
                                                   delta=delta_metric_02_ldp_yearsum_ptm)
                with cols_metric_ldp_board[1]:
                    ctn_metric_ldp_board_03 = st.container(key="ctn_metric_ldp_board_03")
                    ctn_metric_ldp_board_03.metric("Doanh thu tháng hiện hữu",
                                                   value=metric_03_ldp_monthsum_hh,
                                                   delta=delta_metric_03_ldp_monthsum_hh)
                    ctn_metric_ldp_board_04 = st.container(key="ctn_metric_ldp_board_04")
                    ctn_metric_ldp_board_04.metric("Doanh thu tháng phát triển mới",
                                                   value=metric_04_ldp_monthsum_ptm,
                                                   delta=delta_metric_04_ldp_monthsum_ptm)
                    
                ctn_key_table_show_ldp = st.container(key="ctn_key_table_show_ldp")
                with ctn_key_table_show_ldp:
                    table_show_ldp_service = ldp_board.table_show_right_ldp(thuchien_after_load,kehoach_after_load,dichvu_after_load,selected_year,pills_loaidoanhthu_ldp_board,st.session_state.line_selection_board,selected_month)
                    st.dataframe(
                        table_show_ldp_service, 
                        column_config={
                            "nhom_dv": "Nhóm dịch vụ",
                            "percentage": st.column_config.ProgressColumn(
                                "% Hoàn thành",
                                min_value=0,
                                max_value=100,
                                format="%d%%",
                                width="medium"
                            )
                        },
                        hide_index=True, 
                        height=300,use_container_width=True
                    )

class MAIN_BOARD():
    def __init__(self):
        self.board_ldp = BOARD_LDP()
    def main_run(self):
        with st.sidebar:
            module_config.show_expander_sidebar()
        self.board_ldp.show_board_ldp()
thuchien_after_load, kehoach_after_load, nhanvien_after_load, dichvu_after_load,line_after_load = ldp_view.load_data_ldp()
main_board = MAIN_BOARD()
main_board.main_run()
module_config.add_sidebar_footer()

        