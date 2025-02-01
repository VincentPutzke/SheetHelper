from typst_builder import TypstBuilder
import templates



builder = TypstBuilder(5, "Pokemon")
index = builder.generate_table("Regionen-Namen", 2, 3)
builder.add_to_doc(index)
index = builder.generate_table("Protagonisten", 3, 5)
builder.add_to_doc(index)

builder.export()