import numpy as np


class TrackableObject:
    def __init__(self, objectID, centroid) -> None:
        self.centroids = [centroid]
        self.objectID = objectID
        self.isCounted = False
    
    def update_centroid(self, new_cX, new_cY):
        self.curr_cX = new_cX
        self.curr_cY = new_cY
    
    def get_centroid(self):
        return (self.curr_cX, self.curr_cY)
    
    def check_intersection(self, line_startX):
        if self.isCounted:
            return
        
        else:
            init_direction = np.sign(line_startX - self.initial_cX)
            curr_direction =  np.sign(line_startX - self.curr_cX)

            dist = np.abs(line_startX - self.curr_cX)

            if dist == 0:
                print("intersected")
                self.isCounted = True
                return

            if dist > 0 and init_direction != curr_direction:
                print("counted and removing")
                self.isCounted = True
                return