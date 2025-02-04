from typst_builder import TypstBuilder
import templates



builder = TypstBuilder(5, "Deutsche Städte")
index = builder.generate_table("Definition einer Stadt", 3, 5)
builder.add_to_doc(index)
index = builder.generate_combine("Hauptstädte der Bundesländer", 16)
builder.add_to_doc(index)

builder.export()