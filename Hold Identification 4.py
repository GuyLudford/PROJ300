import cv2
import numpy as np

def detect_climbing_holds(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Preprocessing: Apply median filter to remove noise
    denoised_image = cv2.GaussianBlur(image, (5,5), 0)

    cv2.imshow("Climbing Holds Detection", denoised_image)
    cv2.waitKey(0)

    # Thresholding using Otsu's method
    grayscale_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    otsu, _ = cv2.threshold(grayscale_image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # Edge detection using Canny
    edges = cv2.Canny(image,otsu, otsu * 2, L2gradient = True)

    cv2.imshow("Climbing Holds Detection", edges)
    cv2.waitKey(0)

    # Find contours
    contours, _ = cv2.findContours(edges,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    hull = map(cv2.convexHull, contours)

    mask = np.zeros(image.shape, np.uint8)
    cv2.drawContours(mask, hull, -1, [255,255,255],-1)

    showImage(mask)

    BlobDetector = cv2.SimpleBlobDetector_BlobDetector()

    # Change thresholds
    BlobDetector.minThreshold = 0
    BlobDetector.maxThreshold = 255


    # Filter by Area.
    BlobDetector.filterByArea = True
    BlobDetector.minArea = 25

    # Filter by Circularity
    BlobDetector.filterByCircularity = False
    BlobDetector.minCircularity = 0.1

    # Filter by Convexity
    BlobDetector.filterByConvexity = False
    BlobDetector.minConvexity = 0.1
        
    # Filter by Inertia
    BlobDetector.filterByInertia = True
    BlobDetector.minInertiaRatio = 0.05

    # Create a detector with the parameters
    ver = (cv2.__version__).split('.')
    if int(ver[0]) < 3 :
        detector = cv2.SimpleBlobDetector(BlobDetector)
    else : 
        detector = cv2.SimpleBlobDetector_create(BlobDetector)

    keypoints = detector.detect(mask)


    for i, key in enumerate(keypoints):
        x = int(key.pt[0])
        y = int(key.pt[1])

        size = int(math.ceil(key.size)) 

        #Finds a rectangular window in which the keypoint fits
        br = (x + size, y + size)   
        tl = (x - size, y - size)
        cv2.rectangle(image,tl,br,(0,0,255),2)

    #OpenCV uses BGR format, so that'll need to be reversed for display
    image = image[...,::-1]

    # Display the resulting frame
    fig = plt.imshow(image)
    plt.title("Image with Keypoints")

##    # Initialize a list to store keypoints (holds)
##    keypoints = []
##
##    for contour in contours:
##        # Approximate the contour with a convex hull
##        hull = cv2.convexHull(contour)
##
##        # Calculate area and inertia for blob filtering
##        area = cv2.contourArea(hull)
##        inertia = cv2.matchShapes(hull, contour, cv2.CONTOURS_MATCH_I1, 0)
##
##        # Filter out small or low inertia blobs
##        if area > 100 and inertia > 0.1:
##            # Get bounding rectangle for each hold
##            x, y, w, h = cv2.boundingRect(hull)
##            keypoints.append(cv2.KeyPoint(x + w / 2, y + h / 2, w))

    # Draw bounding boxes on the original image
##    result_image = cv2.drawKeypoints(image, keypoints, None, color=(0, 255, 0), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
##
##    # Display the result
##    cv2.imshow("Climbing Holds Detection", result_image)
##    cv2.waitKey(0)
##    cv2.destroyAllWindows()


image_path = "Blank Wall 2.png"
detect_climbing_holds(image_path)
