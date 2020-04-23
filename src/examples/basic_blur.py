import sys
sys.path.append('./')

from backend import blurring
x = blurring.blur("./files/test_images/lena.png")
x.set_mode("Explicit")
x.fit(3)
x.show()


#print(x)
#print(x.mode_boundary)
#print(x.mode_poisson)