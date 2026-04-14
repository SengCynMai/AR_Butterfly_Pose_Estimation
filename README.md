# AR_Butterfly_Pose_Estimation

## Project Overview
This project implements **Absolute Camera Pose Estimation** to render an animated 3D butterfly in augmented reality. It utilizes a pre-calibrated camera and a chessboard pattern for real-time tracking.

## Result Demo
![AR Butterfly Demo](demo.gif)

## Technical Implementation

### 1. 3D Butterfly Generation
The butterfly is not an external file but is **procedurally generated** within the code. 
- **Geometry:** The wings are created using a polar coordinate system (Butterfly Curve logic) to generate curved, organic wing shapes.
- **Animation:** The flapping motion is achieved by applying a temporal sine-wave function, $f(t) = \sin(t)$, to the $Z$-coordinates of the wing vertices.
- **Dynamic Bending:** The wing displacement is scaled by the distance from the body ($|x|$), ensuring the wing tips move more than the base for a natural look.

### 2. Coordinate Transformation & Projection
The project follows the standard vision pipeline to project the 3D butterfly onto the 2D video frame:
1. **World Space:** The butterfly vertices are defined in a 3D coordinate system where the center of the chessboard is $(0,0,0)$.
2. **Pose Recovery:** The script uses `cv2.solvePnP` to find the Rotation ($R$) and Translation ($t$) vectors, moving the camera from World Space to Camera Space.
3. **Perspective Projection:** The final 2D pixel coordinates ($x$) are calculated using the intrinsic camera matrix ($K$) from the calibration file:
   $$x = K [R|t] X$$

## Repository Structure
- `pose_estimation_chessboard.py`: Main processing script.
- `chessboard.mp4`: Input video source.
- `calibration_data.npz`: Camera intrinsic parameters ($K$, $dist$).
- `demo.gif`: Animated demonstration of the AR effect.

## How to Run
1. Ensure `calibration_data.npz` and `chessboard.mp4` are in the folder.
2. Run the script:
   ```bash
   python pose_estimation_chessboard.py
