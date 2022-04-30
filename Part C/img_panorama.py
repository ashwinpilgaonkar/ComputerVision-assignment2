import cv2 
import depthai as dai

pipeline = dai.Pipeline()

camRgb = pipeline.create(dai.node.ColorCamera)
xoutVideo = pipeline.create(dai.node.XLinkOut)

xoutVideo.setStreamName("video")

camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
camRgb.setVideoSize(1920, 1080)
camRgb.setVideoSize(1280, 720)

xoutVideo.input.setBlocking(False)
xoutVideo.input.setQueueSize(1)

camRgb.video.link(xoutVideo.input)

with dai.Device(pipeline, True) as device:

    video = device.getOutputQueue(name="video", maxSize=1, blocking=False)
    count = 0
    frames_arr = []
    while True:
        videoIn = video.get()
        output = videoIn.getCvFrame()

        cv2.imshow("video", output)
        
        if cv2.waitKey(1) == ord('c'):
            frames_arr.append(output)
            count +=1
        if cv2.waitKey(1) == ord('p'):
            print('Creating Panorama...')
            if count < 2:
                print('More images are required for a panorama')
            else:
                stitcher=cv2.Stitcher.create()
                code,panorama =stitcher.stitch(frames_arr)
                if code != cv2.STITCHER_OK:
                    print("Stitching failed")
                else:
                    print('Panorama stitched successfully')
                    cv2.imshow('Panorama',panorama)
                    cv2.imwrite('Panorama.jpg', panorama)
        
        if cv2.waitKey(1) == ord('q'):
            break