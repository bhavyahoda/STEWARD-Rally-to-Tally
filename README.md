# STEWARD-Rally-to-Tally

Smart TErrestrial WArehouse Robot Deployment

# Problems 
Companies manufacturing, processing, and selling steel pipes have to store these huge pipes in large outside yards. As a result, they face many difficulties in inventory management. These difficulties majorly include:
 * Counting the number of pipes in a particular stack in the inventory
 * Inability to automate the counting process and dependency on manual labor leads increase in cost
 * Keeping a live record of pipe data like count, material, diameter location in inventory, etc. 

# Solution
A generic ROS based rover stack which is capable of going to periodic pipe counting missions. Rover will be equipped with sensors like a camera, GPS, etc. that will be used for all the labor-intensive tasks like going in the field and counting. 
Rover has a computer vision algorithm deployed that will be used to calculate the number of pipes in a stack using the camera’s video stream. Rover is also responsible to publish useful
information on Grafana dashboards like:

 * Count
 * Pipe manufacturing type, outside diameter and material
 * Rover health stats like current drawn, charge estimate, power monitoring, etc.

# Technologies used
1. ROS
2. [Husky Rover by Clearpath Robotics](https://clearpathrobotics.com/husky-unmanned-ground-vehicle-robot/)
3. OpenCV
4. Python
5. Influx DB
6. Grafana

# Highlighting features

 * The solution is highly customised as it uses ROS stack due to which it easy to port to any autonomous solution. This makes our rover stack a plugin like entity that can be
deployed to any autonomous solution including Rovers, drones etc.
 * An intuitive dashboard which increases observability about:
    * Count of pipes for each rover mission
    * Pipe material, manufacturing type & diameter
    * Rover Stats like current drawn, battery 
 * Separation of concerns between rover stack, computer vision and dashboards which makes our solution modular and customizable.
 * Makes use of Terrestrial Rover (Husky) instead of drones which provides following benefits:
    * Drones are more susceptible to weather changes like rain whereas rover provide more robust and reliable solution.
    * Due to their high payload capacity, rovers will be more flexible and customizable. They may also come in handy for other use cases.


# Data flow diagram

<img width="696" alt="Screenshot 2021-09-26 at 2 05 24 AM" src="https://user-images.githubusercontent.com/12881364/134800936-b27cc35b-7324-42ed-b6d0-bc3c617a00e4.png">

# Developers

Bhavya hoda, Prabhsimar singh Taneja, Jasmeet Singh, Amanjeet Singh

