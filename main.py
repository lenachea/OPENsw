import sensor, image, time
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()
class Blob:
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
	def rect(self):
		return (self.x, self.y, self.w, self.h)
	def area(self):
		return self.w * self.h
threshold_orange =  (230, 260, 190, 210, 35, 55)
def find_blobs(img, threshold):
	width = img.width()
	height = img.height()
	blobs = []
	for y in range(0,height,5):
		for x in range(0,width,5):
			pixel = img.get_pixel(x, y)
			r, g, b = pixel
			if threshold_orange[0] <= r <= threshold_orange[1] and threshold_orange[2] <= g <= threshold_orange[3] and threshold_orange[4] <= b <= threshold_orange[5]:
				blobs.append(Blob(x,y,5,5))
	return blobs
def merge_blobs(blobs, distance_threshold=70):
	merged_blobs = []
	while blobs:
		current_blob = blobs.pop(0)
		merged = False
		for merged_blob in merged_blobs:
			dx = abs(current_blob.x - merged_blob.x)
			dy = abs(current_blob.y - merged_blob.y)
			if dx <= distance_threshold and dy <= distance_threshold:
				x1 = min(current_blob.x, merged_blob.x)
				y1 = min(current_blob.y, merged_blob.y)
				x2 = max(current_blob.x + current_blob.w, merged_blob.x + merged_blob.w)
				y2 = max(current_blob.y + current_blob.h, merged_blob.y + merged_blob.h)
				merged_blob.x = x1
				merged_blob.y = y1
				merged_blob.w = x2-x1
				merged_blob.h = y2-y1
				merged = True
				break
		if not merged:
			merged_blobs.append(current_blob)
	return merged_blobs
MIN_AREA_THRESHOLD = 200
while(True):
	clock.tick()
	img = sensor.snapshot()
	blobs = find_blobs(img, threshold_orange)
	merged_blobs = merge_blobs(blobs)
	for blob in merged_blobs:
		if blob.area() >= MIN_AREA_THRESHOLD :
			img.draw_rectangle(blob.rect())
			img.draw_cross(blob.x + blob.w // 2, blob.y + blob.h //2)
			print("Blob [면적: %d, 중심 좌표: (%d, %d), 가로: %d, 세로: %d]" %(blob.area(), blob.x + blob.w//2, blob.y + blob.h//2, blob.w, blob.h))