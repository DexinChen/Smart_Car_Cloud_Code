# import the necessary packages
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2 
import csv
import json, time, sys
from datetime import datetime
from collections import OrderedDict
from threading import Thread
import boto3
from boto3.dynamodb.conditions import Key,Attr
from PIL import Image


# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-p", "--prototxt", required=True,
#	help="path to Caffe 'deploy' prototxt file")
#ap.add_argument("-m", "--model", required=True,
#	help="path to Caffe pre-trained model")
#ap.add_argument("-c", "--confidence", type=float, default=0.5,
#	help="minimum probability to filter weak detections")
#args = vars(ap.parse_args())
def everything():
    args = {"prototxt": "deploy.prototxt.txt", "model": "res10_300x300_ssd_iter_140000.caffemodel", "confidence": 0.5}
   
    ACCOUNT_ID = '880652607631'
    IDENTITY_POOL_ID = 'us-east-1:db12e203-9a39-43fa-8dab-2309d4309d39'
    ROLE_ARN = 'arn:aws:iam::880652607631:role/Cognito_Android_Identity_PoolUnauth_Role'
    
    
    cognito = boto3.client('cognito-identity')
    cognito_id = cognito.get_id(AccountId = ACCOUNT_ID, IdentityPoolId = IDENTITY_POOL_ID)
    oidc = cognito.get_open_id_token(IdentityId = cognito_id['IdentityId'])
    
    sts = boto3.client('sts')
    assumedRoleObject = sts.assume_role_with_web_identity(RoleArn = ROLE_ARN, RoleSessionName = "XX",
                                                          WebIdentityToken = oidc['Token'])
    
    client_dynamo = boto3.client('dynamodb',
                                 aws_access_key_id=assumedRoleObject['Credentials']['AccessKeyId'],
                                 aws_secret_access_key=assumedRoleObject['Credentials']['SecretAccessKey'],
                                 aws_session_token=assumedRoleObject['Credentials']['SessionToken']
                                 )
    
    s3 = boto3.client('s3',
                       aws_access_key_id = assumedRoleObject['Credentials']['AccessKeyId'],
                       aws_secret_access_key = assumedRoleObject['Credentials']['SecretAccessKey'],
                       aws_session_token = assumedRoleObject['Credentials']['SessionToken']
                       )
    data = []
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
     
    # initialize the video stream and allow the camera sensor to warm up
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    try:
    	while True:
    		# grab the frame from the threaded video stream and resize it
    		# to have a maximum width of 400 pixels
    		frame = vs.read()
    		frame = imutils.resize(frame, width=400)
    	 
    		# grab the frame dimensions and convert it to a blob
    		(h, w) = frame.shape[:2]
    		blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
    			(300, 300), (104.0, 177.0, 123.0))
    	 
    		# pass the blob through the network and obtain the detections and
    		# predictions
    		net.setInput(blob)
    		detections = net.forward()
    		for i in range(0, detections.shape[2]):
    			# extract the confidence (i.e., probability) associated with the
    			# prediction
    			confidence = detections[0, 0, i, 2]
    	 
    			# filter out weak detections by ensuring the `confidence` is
    			# greater than the minimum confidence
    			if confidence < args["confidence"]:
    				continue
    	 		
    			tmp_frame = np.asarray(frame)
    			# compute the (x, y)-coordinates of the bounding box for the
    			# object
    			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
    			(startX, startY, endX, endY) = box.astype("int")
    	 
    			# draw the bounding box of the face along with the associated
    			# probability
#    			text = "{:.2f}%".format(confidence * 100)
#    			y = startY - 10 if startY - 10 > 10 else startY + 10
#    			cv2.rectangle(frame, (startX, startY), (endX, endY),
#    				(0, 0, 255), 2)
#    			cv2.putText(frame, text, (startX, y),
#    				cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
    			print(frame.shape)
    			filename = "face_image.jpg"
    			im = Image.fromarray(tmp_frame)
    			im.save(filename)
    			with open(filename, 'rb') as data:
    				s3.upload_fileobj(data, 'iot-image-19951124', str(int(time.time())) + ".jpg")
    			time.sleep(5)
    
    		# show the output frame  
#    		cv2.imshow("Frame", frame)
#    		key = cv2.waitKey(1) & 0xFF
     	
    	# if the `q` key was pressed, break from the loop
    	#if key == ord("q"):
    except (KeyboardInterrupt):
    	print("end")	
    	#break
     
    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()
everything()