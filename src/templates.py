
def generate_table_template(columns, rows):
    template = "#table(\n  columns: ("
    
    for i in range(columns-1):
        template += f" auto, "
    template += f" auto),\n"
    
    template += "  "
    for j in range(columns-1):
        template += f"[*HEADER {j}*], "
    template += f"[*HEADER {columns-1}*],\n"
    for i in range(rows):
        template += "  "
        for j in range(columns-1):
            template += f"[CELL {i} {j}], "
        template += f"[CELL {i} {columns-1}],\n"
    template += "\n)"
    return template