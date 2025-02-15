#!/usr/bin/env python

import rospy #importar ros para python
from std_msgs.msg import String, Int32 # importar mensajes de ROS tipo String y tipo Int32
from geometry_msgs.msg import Twist # importar mensajes de ROS tipo geometry / Twist
from sensor_msgs.msg import Image # importar mensajes de ROS tipo Image
import cv2 # importar libreria opencv
from cv_bridge import CvBridge # importar convertidor de formato de imagenes
import numpy as np # importar libreria numpy


class Template(object):
	def __init__(self, args):
		super(Template, self).__init__()
		self.args = args
		self.sub  = rospy.Subscriber('duckiebot/camera_node/image/raw', Image, self.procesar_img)
		self.pub = rospy.Publisher('duckiebot/camera_node/pov', Image )



	#def publicar(self):

	#def callback(self,msg):

	def procesar_img(self, img):
		bridge = CvBridge()
		image = bridge.imgmsg_to_cv2(img, "bgr8")
		
		# Cambiar espacio de color
		
		image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

		# Filtrar rango util
		limL = np.array([10, 150,  100])
		limU = np.array([120, 255, 255])
	
		mask = cv2.inRange(image_hsv, limL, limU)

		# Aplicar mascara

		image_out = cv2.bitwise_and(image, image, mask= mask)

		# Aplicar transformaciones morfologicas

		# Definir blobs
		
		kernel = np.ones((5,5), np.uint8)
		img_out= cv2.erode(image_hsv, kernel, iterations= 1)
		img_out= cv2.dilate(image_hsv, kernel, iterations= 1)
		
		# Dibujar rectangulos de cada blob

		# Publicar imagen final
		#image_out3 = cv2.cvtColor(image_out, cv2.COLOR_HSV2BGR)
		msg = bridge.cv2_to_imgmsg(image_out, "bgr8")
		self.pub.publish(msg)

def main():
	rospy.init_node('test') #creacion y registro del nodo!

	obj = Template('args') # Crea un objeto del tipo Template, cuya definicion se encuentra arriba

	#objeto.publicar() #llama al metodo publicar del objeto obj de tipo Template

	rospy.spin() #funcion de ROS que evita que el programa termine -  se debe usar en  Subscribers


if __name__ =='__main__':
	main()
