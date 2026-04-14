import cv2 as cv
import numpy as np
import time

# 1. Load Calibration Data
try:
    data = np.load('calibration_data.npz')
    K = data['mtx'] if 'mtx' in data else data[data.files[0]]
    dist = data['dist'] if 'dist' in data else data[data.files[1]]
except:
    print("Error: Could not find calibration_data.npz")
    exit()

# 2. Setup Video Input & Output (MP4)
cap = cv.VideoCapture('chessboard.mp4')
width, height = int(cap.get(3)), int(cap.get(4))
fps = cap.get(cv.CAP_PROP_FPS)
fourcc = cv.VideoWriter_fourcc(*'mp4v')
out = cv.VideoWriter('result.mp4', fourcc, fps, (width, height))

# 3. SET PATTERN SIZE (Inner corners for 9x7 squares = 8x6)
pattern_size = (8, 6) 
objp = np.zeros((8 * 6, 3), np.float32)
objp[:, :2] = np.mgrid[0:8, 0:6].T.reshape(-1, 2)

# --- Butterfly Geometry Generator ---
def get_butterfly_pts(flap_val):
    pts = []
    # Using a polar-style equation to draw realistic wing shapes
    for theta in np.linspace(0, 2 * np.pi, 100):
        # Butterfly Curve logic (simplified for 3D)
        r = (np.exp(np.cos(theta)) - 2*np.cos(4*theta) + np.sin(theta/12)**5)
        x = r * np.sin(theta)
        y = r * np.cos(theta)
        # Z-axis flap: Points further from center (larger x) move more
        z = -1.0 + (abs(x) * flap_val * 0.5) 
        pts.append([x, y, z])
    return np.array(pts, dtype=np.float32)

print("Processing Beautiful Butterfly... Saving to result.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    ret_corners, corners = cv.findChessboardCorners(gray, pattern_size, None)

    if ret_corners:
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        _, rvec, tvec = cv.solvePnP(objp, corners2, K, dist)

        # Animation logic
        t = time.time() * 7
        flap = np.sin(t) 
        
        # Center of the board (8x6 corners)
        cx, cy = 3.5, 2.5
        
        # Generate Butterfly and shift to center
        butterfly_3d = get_butterfly_pts(flap)
        butterfly_3d[:, 0] += cx
        butterfly_3d[:, 1] += cy

        # Project 3D to 2D
        img_pts, _ = cv.projectPoints(butterfly_3d, rvec, tvec, K, dist)
        img_pts = np.int32(img_pts).reshape(-1, 2)

        # Draw the wings with a "Glow" effect (multiple thin lines)
        cv.polylines(frame, [img_pts], True, (255, 255, 100), 2) # Cyan main line
        for pt in img_pts[::5]: # Add glowing dots at intervals
            cv.circle(frame, tuple(pt), 3, (255, 150, 255), -1) # Pink glow
            
        # Draw board corners to confirm tracking
        cv.drawChessboardCorners(frame, pattern_size, corners2, ret_corners)

    out.write(frame)
    cv.imshow('AR Mission: Beautiful 3D Butterfly', frame)
    if cv.waitKey(1) == ord('q'): break

cap.release()
out.release()
cv.destroyAllWindows()