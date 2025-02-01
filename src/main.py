from typst_builder import TypstBuilder
import templates



builder = TypstBuilder(5, "Jahreszeiten")
index = builder.generate_table("Wetter", 2, 3)
builder.add_to_doc(index)
index = builder.generate_combine("Temperatur", 5)
builder.add_to_doc(index)

builder.export()