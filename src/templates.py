
def generate_table_data_template(columns, rows):
    template = ""
    
    header_row = ""
    for c in range(columns-1):
        header_row += f"\"HEADER {c+1}\","
    header_row += f"\"HEADER {columns-1}\""
    template += header_row + "\n"
    for r in range(rows):
        row = ""
        for c in range(columns-1):
            row += f"\"ITEM {r+1} {c+1}\","
        row += f"\"ITEM {r+1} {columns-1}\""
        template += row +"\n"
    return template

def combine_table_with_data(nametag):
    template = f"#let {nametag} = csv(\"data/{nametag}.csv\")\n"
    
    template += "#align(center, block("
    template += f"  table(align: left,\n    columns: {nametag}.first().len(),\n"
    template += f"    ..for row in {nametag}"+" {\n"
    template += "      row\n  }\n)))"
    
    return template