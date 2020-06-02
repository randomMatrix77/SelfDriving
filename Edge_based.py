def draw_lines(img, lines):
    for line in lines:
        for coords in line:
            cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), (0, 255, 0), 5)

def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, [vertices], 255)
    masked = cv2.bitwise_and(img, mask)
    return masked

def edge_detection(original_image):
    processed_image = cv2.Canny(processed_image, threshold1=100, threshold2=200)
    clipped_image = roi(processed_image, vertices)
    lines = cv2.HoughLinesP(clipped_image, 1, np.pi/180, 200, 500, 30)
    try:
        draw_lines(original_image, lines)
    except:
        pass
