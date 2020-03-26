from backend import contrasting
from extra import local_adaptive_histogram
from PIL import Image
from rapport_snippets.figs import *
import numpy as np

contrast_obj = contrasting.Contrast("./files/test_images/contrast.jpg", False)

epoch_count = {
	0.25:[1, 3, 5],
	0.5:[1, 3, 5],
	0.75:[1, 3, 5]
}


#for alpha in [0.25, 0.5, 0.75]:
#	for epoch in [1, 3, 8]:
#output_folder = "rapport_snippets/output/"

results_doc = compile_doc(contrast_obj, epoch_count, "./rapport_snippets/output/contrast/", "kontrastforsterkning", setup=lambda x: x.destroy_information(2))

# this should proably be in the document elsewhere
'''
output = local_adaptive_histogram.contrast_enhancement(contrast_obj.data_copy)

# saves the local adaptive histogram iamge
Image.fromarray(np.uint8(255 * output)).save(output_folder + "contrast/adaptive.png")

results_doc.add_row_element(subfigure(path="kontrastforsterkning/" + "contrast/adaptive.png", text="local adaptive histogram"))
results_doc.add_row()
'''


results_doc.save("rapport_snippets/output/contrast/results.tex")


