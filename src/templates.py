
def generate_table_data_template(columns, rows, hints=["ITEM", "ITEM"]):
    template = ""
    
    header_row = ""
    for c in range(columns-1):
        header_row += f"\"HEADER_{hints[c]} {c+1}\","
    header_row += f"\"HEADER_{hints[columns-1]} {columns-1}\""
    template += header_row + "\n"
    for r in range(rows):
        row = ""
        for c in range(columns-1):
            row += f"\"{hints[c]} {r+1} {c+1}\","
        row += f"\"{hints[columns-1]} {r+1} {columns-1}\""
        template += row +"\n"
    return template

def combine_table_with_data(nametag):
    template = f"#let {nametag} = csv(\"data/{nametag}.csv\")\n"
    
    template += "#align(center, block("
    template += f"  table(align: left,\n    columns: {nametag}.first().len(),\n"
    template += f"    ..for row in {nametag}"+" {\n"
    template += "      row\n  }\n)))"
    
    return template

def combine_connect_with_template(nametag):
    template = f"#let {nametag} = csv(\"data/{nametag}.csv\")\n"
    
    template += "#align(center, block(\n"
    template += "  table(align: (right, left),"
    template += "  stroke: none,"
    template += "  column-gutter: (-0.5em, 10%, -0.5em),"
    template += "  columns: 4,"
    template += f"  ..for (r1, r2) in {nametag} "+"{"
    template += "    (r1, sym.circle.stroked.big, sym.circle.stroked.big,r2)"
    template += "  }"
    template += ")\n))"
    
    return template