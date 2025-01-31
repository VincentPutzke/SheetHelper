from typst_builder import TypstBuilder
import templates



builder = TypstBuilder(5, "Wetter")
index = builder.generate_table("Wasserkreislauf", 3, 5)

builder.add_to_doc(index)
builder.export()