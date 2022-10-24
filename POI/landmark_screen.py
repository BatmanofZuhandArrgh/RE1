import numpy as np
import cv2
from location_of_interest import LOI

class LandmarkScreen():
    def __init__(self, color_frame, depth_frame) -> None:
        self.height, self.width, _ = color_frame.shape
        print(depth_frame.shape)
        self.depth_frame = cv2.medianBlur(depth_frame,5)
        self.color_frame = color_frame

        #Assuming the height and width is dividable by 10
        self.grid_unit_h, self.grid_unit_w = int(self.height //10), int(self.width //10)
        self.grid_repr = np.array([
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,1,0,0,1,0,0,1,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,1,0,0,1,0,0,1,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,1,0,0,1,0,0,1,0],
            [0,0,0,0,0,0,0,0,0,0]
        ])

        self.grid = {}
        for w in range(self.grid_repr.shape[0]):
            self.grid[w] = {}
            for h in range(self.grid_repr.shape[1]):
                img_coord = (int((w+.5)* self.grid_unit_w),int((h+.5)* self.grid_unit_h))
                bbox = ((int(w* self.grid_unit_w),int(h* self.grid_unit_h)),(int((w+1)* self.grid_unit_w),int((h+1)* self.grid_unit_h)))

                # print(w, h, self.grid_repr[w][h], img_coord, self.depth_frame.shape)
                # print(self.depth_frame[img_coord[1]][img_coord[0]])
                depth_grid_unit = self.depth_frame[bbox[0][0]: bbox[1][0], bbox[0][1]: bbox[1][1]]
                depth = np.median(depth_grid_unit)
                
                self.grid[w][h] = LOI(
                    img_coord=img_coord,
                    depth=depth,
                    bbox = bbox,
                    active=self.grid_repr[w][h],
                )

    def show(self):
        for w in range(self.grid_repr.shape[0]):
            for h in range(self.grid_repr.shape[1]):
                cv2.rectangle(self.color_frame, self.grid[w][h].bbox[0], self.grid[w][h].bbox[1], self.grid[w][h].landmark_color, 2)
                if self.grid[w][h].active_landmark:
                    # cv2.circle(self.color_frame, self.grid[w][h].img_coord[:-1], radius= 2, color = (255,0,0), thickness = 2)
                    self.color_frame = cv2.putText(self.color_frame, str(self.grid[w][h].depth), self.grid[w][h].img_coord[:-1], cv2.FONT_HERSHEY_SIMPLEX, 
                                    0.5, (255,0,0), 1, cv2.LINE_AA)

        self.color_frame = cv2.cvtColor(self.color_frame, cv2.COLOR_RGB2BGR)
        print('save')
        cv2.imwrite('./sample/selection_output.png', self.color_frame)

        cv2.imshow('',self.color_frame)
        
        if cv2.waitKey(0) & 0xFF == ord('q'):
            #closing all open windows 
            cv2.destroyAllWindows() 


if __name__ == '__main__':
    sample_img = cv2.imread('./sample/color_output.png')
    sample_img = cv2.cvtColor(sample_img, cv2.COLOR_BGR2RGB)
    sample_img = cv2.resize(sample_img, (480, 640))
    landmark_screen = LandmarkScreen(color_frame=sample_img, depth_frame=sample_img[:,:, 0])
    landmark_screen.show()