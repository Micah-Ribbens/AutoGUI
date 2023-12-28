Finished development: 04/05/2023

Full documentation: https://micah-ribbens.github.io/Auto-GUI


# Summary
An application for the 2122 Robotics Team that allowed the user to make autonomous paths for the robot. I worked on the GUI (this application).
Ibrahim (https://github.com/IbrahimAhmad65) wrote the path generating code and path following code. One important note is that there is error checking, 
but we decided as a team to have it be somewhat minimal, so if the user
inputs invalid data, either the GUI could get into a bad state or the path could be invalid. We did this because we assumed
that the user knew how to create valid paths. We also wanted the majority of the development time to be spent on making the
application robust and user-friendly, instead of constantly checking what the user does.
The paths could include actions to be done at certain points (locking the wheels, placing a cone, placing a cube, etc.) The output
of this program is a json file, which the java autonomous code on the robot used to execute the path the user made.
The idea of the application was to have it be modular. That way specific parts of the robot path could be focused on
individually. There are three types of points for the robotics path:
- A path modifying point, which modifies the path of the robot (robot is not guaranteed to go through these).
- A required point, which is a point the robot is guaranteed to go through.
- A path action point, which specifies what the robot will do at a certain points on the path.

For the path action and required points, the x and y coordinates cannot be modified directly, but instead the t-value
can be modified. The autonomous following code uses the t-value to decide where those points should be executed (see vocab 
for a detailed explanation of t-values). Also, when moving and placing those points, the points are placed directly on what
part of the path they will be executed on.

One important note is that the path of the robot is not constantly updated because updating the path is costly in execution time. Updating the path 
involves an expensive call to SwerveLib.jar, which uses the path modifying points to determine the robot's path. Instead, once the 
user hits the draw button, the path is updated. This means that if the user did not hit the draw button and has modified 
path modifying points, then the application will be using the 'old path' for calculations. This was never an issue because the 
user would always hit the draw button before finalizing the path.

# Example Path
![Example Path](documentation/Example%20Path.png)

# Vocab
- Path Modifying Point &rarr; modifies the path of the robot (robot is not guaranteed to go through these)
- Required Point &rarr; a point the robot will go through
- Path Action Point &rarr; specifies what the robot will do at a certain point in the path 
- t-value &rarr; where a path action or a required point is located on the path. The whole number represents what number
the point is after (0 indexed or path modifying point number - 1). The decimal represents the proportion of the way it is to next path modifying point. For instance,
2.5 would be halfway between path modifying point 3 and 4. While 2.98 would be between path modifying point 3 and 4, 
but would be 98% of the way to 4.
- Vx &rarr; velocity in the x direction of the robot at the path modifying point
- Vy &rarr; velocity in the y direction of the robot at the path modifying point
- x power &rarr; power of the spline at the current path modifying point (1 and 5 are the only valid options)
- Command &rarr; the action that the robot will do at the path action point
- Angle &rarr; the angle of the robot at the current required point
- Placement Angle &rarr; the angle the robot is placed at before the path has started
- Initial Angle &rarr; the angle the robot should start at
- End Angle &rarr; the angle the robot should end at

# How To Use and UI/UX Explained
## UI/UX Specifics
See the summary for an overview of the application and explanation of vocab. Everytime the path is drawn, there are multiple colored lines drawn
onto the screen. The blue lines are the path of the robot. The purple lines show the direction of the robot at the current path modifying point. 
There are path point frames, which correlate to the points above. The location of the path action points and required 
points shows roughly where they will be executed. The t-value of those points is a more accurate measure, however. The points that are being currently modified will be
the name that appears for the frame. The frames can be switched by clicking the frame button, which has the name of the
type of point currently being modified. The type of point that is currently being modified will have all actions "done
to it." These actions include: adding a point and modifying point data.

## A Note On Shortcuts
The application many shortcuts, but it can also be used without any shortcuts. A list of all the shortcuts will
be provided below

# Shortcuts

## File shortcuts
1. f &rarr; Saves the current path as a new file and a file dialogue will appear
2. s &rarr; Quickly saves the currently loaded file (a file is loaded if a file path was specified from saving the file or loading the file)
3. g &rarr; Loads a file onto the GUI and a file dialogue will appear
4. Ctrl + l &rarr; Loads a file onto the GUI and a file dialogue will appear (same as 'g')

## Navigating Input Fields ('Vim' Shortcuts)
Note: All these shortcuts are for the point editing frame (The top right frame of the application)
1. h &rarr; Go left one input field
2. l &rarr; Go right one input field
3. k &rarr; Go up one input field
4. j &rarr; Go down one input field
5. i &rarr; Go to the very first input field
6. o &rarr; Go to the very last input field
7. Tab &rarr; Go right one input field

## Point Frames
1. Ctrl + a &rarr; Change the points frame to 'Path Modifying Point'
2. Ctrl + d &rarr; Change the points frame to 'Required Point'
3. Ctrl + s &rarr; Change the point editing state to 'Path Action Point'
4. Ctrl + Space &rarr; Toggle the points frame (Cycle is Path Modifying Point -> Path Action Point -> Required Point)

## Point Editing States
1. e &rarr; Change the point editing state to 'Moving Points'
2. q &rarr; Change the point editing state to 'Adding Points'
3. w &rarr; Change the point editing state to 'Deleting Points'

## Modifying Application Data
1. d &rarr; Draw the path
2. Return &rarr; Update the points location, so they reflect what is in the input fields
3. r &rarr; Reset all the point location input fields, so they reflect the location of points on the field
4. u &rarr; Clear the field of all points

## Point Editing
1. Ctrl + c  &rarr; Copy the currently selected point
2. Ctrl + v &rarr; Paste the currently selected point
3. z &rarr; Swap the two the points with the numbers provided in the input field
4. Ctrl + Backspace &rarr; Delete the currently selected point
5. Up Arrow &rarr; Move the currently selected point up one, thereby decrementing the point number by one
6. Down Arrow &rarr; Move the currently selected point down one, thereby incrementing the point number by one

# Detailed Documentation
![Documentation Image](documentation/Auto%20GUI%20Documentation.drawio.png)