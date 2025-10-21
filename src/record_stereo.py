import cv2
import numpy as np
from stereo_image_source import ImageSource
import time
import threading

trigger_timestamp = []

#def trigger(image_source):
#    global trigger_timestamp
#    for i in range(10000):
#        image_source.trigger_cameras()
#        trigger_timestamp.append(time.time())
#        time.sleep(1/30.0)

def main():
    image_source = ImageSource()
    image_source.trigger_cameras()
    images = image_source.get_images()
    videoWriters = [cv2.VideoWriter(f'{cam_id}.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 30, (image.shape[1], image.shape[0]))
                    for cam_id, timestamp, image in images]

    #threading.Thread(target=trigger, args=(image_source,)).start()
    image_source.trigger_cameras()
    timestamp = time.time()
    trigger_timestamp.append(timestamp)

    for frame in range(1000000000):
        for videoWriter, image_record in zip(videoWriters, images):
            images = image_source.get_images()
            image_source.trigger_cameras()
            timestamp = time.time()
            trigger_timestamp.append(timestamp)

            cam_id, _, image = image_record
            image = np.stack([image, image, image], axis=2)
            videoWriter.write(image)

            #cv2.imshow(cam_id, image)
            print(cam_id, frame + 1, len(trigger_timestamp), trigger_timestamp[frame])

        #key = cv2.waitKey(1)
        #if key == ord(' '):
        #    break

    for videoWriter in videoWriters:
        videoWriter.release()


if __name__ == '__main__':
    main()





