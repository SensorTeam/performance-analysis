import cv2 as cv
import colorsys as cs

import errno
from glob import glob

def intensity(image):
	width = image.shape[1]
	height = image.shape[0]
	intensity = 0
	for row in range(0, height):
		row_intensity = 0
		for pixel in range(0, width):
			rgb = image[row][pixel]
			hsv = cs.rgb_to_hsv(
						rgb[0] / 255,
						rgb[1] / 255,
						rgb[2] / 255
					)
			row_intensity += hsv[1] * hsv[2]
		intensity += row_intensity
	return intensity

def read(file):
	return cv.imread(file)

def batch(path):
	images = []
	files = glob(path)
	for file in files:
		try:
			images.append({
				'title': file,
				'number': int(file[-6:-4]),
				'data': read(file),
				'intensity': None
			})
		except IOError as e:
			if e.errno != errno.EISDIR:
				raise
	return images

if __name__ == '__main__':
	cow_images = batch('data/IvT/Original/Cow/*.jpg')
	cow_images = sorted(cow_images, key=lambda image: image['number'])

	for image in cow_images:
		image['intensity'] = intensity(image['data'])
		print('{}: {:.2f}'.format(image['number'], image['intensity']))
		
