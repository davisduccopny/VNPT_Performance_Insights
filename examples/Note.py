from streamlit_elements import elements, dashboard, mui

# Ví dụ dữ liệu
columns = [
    {"field": "id", "headerName": "ID", "width": 70},
    {"field": "name", "headerName": "Name", "width": 130},
    {"field": "age", "headerName": "Age", "width": 90},
]
rows = [
    {"id": 1, "name": "Alice", "age": 25},
    {"id": 2, "name": "Bob", "age": 30},
    {"id": 3, "name": "Charlie", "age": 35},
]

# Streamlit Elements
with elements("demo_grid"):
    mui.DataGrid(
        rows=rows,
        columns=columns,
        pageSize=5,
        checkboxSelection=True,
        style={"height": 400, "width": "100%","borderRadius": 3, "overflow": "hidden"}
    )
