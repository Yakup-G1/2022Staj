"""
example of drawing a box-like spacecraft in python
    - Beard & McLain, PUP, 2012
    - Update history:  
        1/8/2019 - RWB
"""

import numpy as np

import pyqtgraph as pg
import pyqtgraph.opengl as gl
import pyqtgraph.Vector as Vector

from tools.tools import Euler2Quaternion, Quaternion2Rotation


class mav_viewer():
    def __init__(self):
        # initialize Qt gui application and window
        self.app = pg.QtGui.QApplication([])  # initialize QT
        self.window = gl.GLViewWidget()  # initialize the view object
        #self.window.setWindowTitle('Submarine Viewer')
        self.window.setGeometry(0, 0, 500, 500)  # args: upper_left_x, upper_right_y, width, height
        
        grid = gl.GLGridItem() # make a grid to represent the ground
        grid.scale(20, 20, 20) # set the size of the grid (distance between each line)
        self.window.addItem(grid) # add grid to viewer
        self.window.setCameraPosition(distance=1000) # distance from center of plot to camera
        self.window.setBackgroundColor('k')  # set background color to black
        self.window.show()  # display configured window
        self.window.raise_() # bring window to the front
        self.plot_initialized = False # has the spacecraft been plotted yet?
        # get points that define the non-rotated, non-translated spacecraft and the mesh colors
        self.points, self.meshColors = self._get_spacecraft_points()
        

    ###################################
    # public functions
    def update(self,path, state):
        """
        Update the drawing of the spacecraft.

        The input to this function is a (message) class with properties that define the state.
        The following properties are assumed to be:
            state.pn  # north position
            state.pe  # east position
            state.h   # altitude
            state.phi  # roll angle
            state.theta  # pitch angle
            state.psi  # yaw angle
        """
        spacecraft_position = np.array([[0], [0], [-0]])  
        
        ## quaternion uygulaması
        
        quat = Euler2Quaternion(state.phi, state.theta, state.psi)
        R    = Quaternion2Rotation(quat)
        #R = self._Euler2Rotation(state.phi, state.theta, state.psi)
        # rotate and translate points defining spacecraft
        rotated_points = self._rotate_points(self.points, R)
        
        translated_points = self._translate_points(rotated_points, spacecraft_position)
        
        # convert North-East Down to East-North-Up for rendering
        R = np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]])
        translated_points = R @ translated_points
        # convert points to triangular mesh defined as array of three 3D points (Nx3x3)
        mesh = self._points_to_mesh(translated_points)
        

        N = 100
        red = np.array([[1., 0., 0., 1]])
        green = np.array([[0., 1., 0., 1]])
        blue = np.array([[0., 0., 1., 1]])
        
        #############################XXXXX  
        theta = 0
        self.pointsX = np.array([[path.orbit_center.item(0) + path.orbit_radius,
                            path.orbit_center.item(1),
                            path.orbit_center.item(2)]])
        path_colorx = red
        i=0
        for i in range(0, N):
            theta += 2 * np.pi / N
            new_point = np.array([[path.orbit_center.item(0) + path.orbit_radius * np.cos(theta),
                                path.orbit_center.item(1) + path.orbit_radius * np.sin(theta),
                                path.orbit_center.item(2) ]])
            self.pointsX = np.concatenate((self.pointsX, new_point), axis=0)
            path_colorx = np.concatenate((path_colorx, red), axis=0)
        pointlistX = self.pointsX.T
        
        spacecraft_positionX = np.array([[0], [0], [0]]) 
        
        #### X ekseninde quaternion için Aktif et ####
        
        quat = Euler2Quaternion(state.phi, state.theta, state.psi)
        R    = Quaternion2Rotation(quat)
        

        rotated_pointsX = self._rotate_points(pointlistX, R)
        
        translated_pointsX = self._translate_points(rotated_pointsX, spacecraft_positionX)
        R = np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]])
        translated_pointsX = R @ translated_pointsX
        translated_pointsX = translated_pointsX.T
        
        #### X ekseninde Euler Açıları için Aktif et ####
        # R = self._Euler2Rotation(state.phi, state.theta, state.psi)
        
        # rotated_pointsX = self._rotate_points(pointlistX, R)
        # translated_pointsX = self._translate_points(rotated_pointsX, spacecraft_positionX)
        
        # R = np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]])
        # translated_pointsX = R @ translated_pointsX
        # translated_pointsX = translated_pointsX.T
        
         #############################YYYY
        theta = 0
        self.pointsY = np.array([[path.orbit_center.item(0) + path.orbit_radius,
                            path.orbit_center.item(1),
                            path.orbit_center.item(2)]])
        path_colory = blue
        i=0
        for i in range(0, N):
            theta += 2 * np.pi / N
            new_point = np.array([[path.orbit_center.item(0) + path.orbit_radius * np.cos(theta),
                                path.orbit_center.item(1) ,
                                path.orbit_center.item(2) + path.orbit_radius * np.sin(theta) ]])
            self.pointsY = np.concatenate((self.pointsY, new_point), axis=0)
            path_colory = np.concatenate((path_colory, blue), axis=0)
        pointlistY = self.pointsY.T
        
        spacecraft_positionY = np.array([[0], [0], [0]]) 
        
        #### Y ekseninde quaternion için Aktif et ####
        
        quat = Euler2Quaternion(state.phi, state.theta, state.psi)
        R    = Quaternion2Rotation(quat)

        rotated_pointsY = self._rotate_points(pointlistY, R)
        
        translated_pointsY = self._translate_points(rotated_pointsY, spacecraft_positionY)
        R = np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]])
        translated_pointsY = R @ translated_pointsY
        translated_pointsY = translated_pointsY.T
        
          #### Y ekseninde Euler için Aktif et ####
          
        # R = self._Euler2Rotation(state.phi, state.theta, state.psi)
        
        # rotated_pointsY = self._rotate_points(pointlistY, R)
        # translated_pointsY = self._translate_points(rotated_pointsY, spacecraft_positionY)
        
        # R = np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]])
        # translated_pointsY = R @ translated_pointsY
        # translated_pointsY = translated_pointsY.T
        
         #############################ZZZZZ
        theta = 0
        self.pointsZ = np.array([[path.orbit_center.item(0) ,
                            path.orbit_center.item(1),
                            path.orbit_center.item(2)+ path.orbit_radius]])
        path_colorz = blue
        i=0
        for i in range(0, N):
            theta += 2 * np.pi / N
            new_point = np.array([[path.orbit_center.item(0) ,
                                path.orbit_center.item(1) + path.orbit_radius * np.sin(theta),
                                path.orbit_center.item(2) + path.orbit_radius * np.cos(theta)]])
            self.pointsZ = np.concatenate((self.pointsZ, new_point), axis=0)
            path_colorz = np.concatenate((path_colorz, green), axis=0)
        pointlistZ = self.pointsZ.T
        
        spacecraft_positionZ = np.array([[0], [0], [0]]) 
        
        #### Z ekseninde quaternion için Aktif et ####
        
        quat = Euler2Quaternion(state.phi, state.theta, state.psi)
        R    = Quaternion2Rotation(quat)

        rotated_pointsZ = self._rotate_points(pointlistZ, R)
        
        translated_pointsZ = self._translate_points(rotated_pointsZ, spacecraft_positionZ)
        R = np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]])
        translated_pointsZ = R @ translated_pointsZ
        translated_pointsZ = translated_pointsZ.T
        
          #### Z ekseninde Euler için Aktif et ####
          
        # R = self._Euler2Rotation(state.phi, state.theta, state.psi)
        
        # rotated_pointsZ = self._rotate_points(pointlistZ, R)
        # translated_pointsZ = self._translate_points(rotated_pointsZ, spacecraft_positionZ)
        
        # R = np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]])
        # translated_pointsZ = R @ translated_pointsZ
        # translated_pointsZ = translated_pointsZ.T
        
        # initialize the drawing the first time update() is called
        if not self.plot_initialized:
            
            
            self.x_object = gl.GLLinePlotItem(pos=translated_pointsX,
                                color=path_colorx,
                                width=2,
                                antialias=True,
                                mode='line_strip')
            self.window.addItem(self.x_object)
            
            self.y_object = gl.GLLinePlotItem(pos=translated_pointsY,
                                color=path_colory,
                                width=2,
                                antialias=True,
                                mode='line_strip')
            self.window.addItem(self.y_object)
            
            self.z_object = gl.GLLinePlotItem(pos=translated_pointsZ,
                                color=path_colorz,
                                width=2,
                                antialias=True,
                                mode='line_strip')
            self.window.addItem(self.z_object)
            
            
            #self.window.addItem(z_object)

            # initialize drawing of triangular mesh.
            self.body = gl.GLMeshItem(vertexes=mesh,  # defines the triangular mesh (Nx3x3)
                                      vertexColors=self.meshColors, # defines mesh colors (Nx1)
                                      drawEdges=True,  # draw edges between mesh elements
                                      smooth=False,  # speeds up rendering
                                      computeNormals=False)  # speeds up rendering
            self.window.addItem(self.body)  # add body to plot
            self.plot_initialized = True

        # else update drawing on all other calls to update()
        else:
            # reset mesh using rotated and translated points
            self.body.setMeshData(vertexes=mesh, vertexColors=self.meshColors)
            self.x_object.setData(pos=translated_pointsX,color=path_colorx)
            self.y_object.setData(pos=translated_pointsY,color=path_colory)
            self.z_object.setData(pos=translated_pointsZ,color=path_colorz)

        # update the center of the camera view to the spacecraft location
        view_location = Vector(0, 0, 100)  # defined in ENU coordinates
        self.window.opts['center'] = view_location
        # redraw
        self.app.processEvents()

    ###################################
    # private functions
    def _rotate_points(self, points, R):
        "Rotate points by the rotation matrix R"
        rotated_points = R @ points
        return rotated_points

    def _translate_points(self, points, translation):
        "Translate points by the vector translation"
        translated_points = points + np.dot(translation, np.ones([1,points.shape[1]]))
        return translated_points

    def _get_spacecraft_points(self):
        """"
            Points that define the spacecraft, and the colors of the triangular mesh
            Define the points on the aircraft following diagram in Figure C.3
        """
        # points are in NED coordinates
        bu=1  # base unit for the plane
        # X coordinates
        fl1=2*bu
        fl2=1*bu
        fl3=4*bu
        wl=1*bu
        twl=1*bu
        # Y coordinates
        fw=1*bu
        ww=5*bu
        tww=3*bu
        # Z coordinates
        fh=1*bu
        th=1*bu

        points = np.array([[fl1, 0, 0],  # point 1
                           [fl2, fw/2, -fh/2],  # point 2
                           [fl2, -fw/2, -fh/2],  # point 3
                           [fl2, -fw/2, fh/2],  # point 4
                           [fl2, fw/2, fh/2],  # point 5
                           [-fl3, 0, 0],  # point 6
                           [0, ww/2, 0],  # point 7
                           [-wl, ww/2, 0],  # point 8
                           [-wl, -ww/2, 0],  # point 9
                           [0, -ww/2, 0],  # point 10
                           [-fl3+twl, tww/2, 0],  # point 11
                           [-fl3, tww/2, 0],  # point 12
                           [-fl3, -tww/2, 0],  # point 13
                           [-fl3+twl, -tww/2, 0],  # point 14
                           [-fl3+twl, 0, 0],  # point 15
                           [-fl3, 0, -th],  # point 16
                           ]).T
        # scale points for better rendering
        scale = 10
        points = scale * points

        #   define the colors for each face of triangular mesh
        red = np.array([1., 0., 0., 1])
        green = np.array([0., 1., 0., 1])
        blue = np.array([0., 0., 1., 1])
        yellow = np.array([1., 1., 0., 1])
        meshColors = np.empty((13, 3, 4), dtype=np.float32)
        meshColors[0] = yellow  # noset
        meshColors[1] = yellow  # noser
        meshColors[2] = yellow  # noseb
        meshColors[3] = yellow  # nosel
        meshColors[4] = blue  # flt
        meshColors[5] = blue  # flr
        meshColors[6] = blue  # flb
        meshColors[7] = blue  # fll
        meshColors[8] = green  # wing
        meshColors[9] = green  # wing
        meshColors[10] = red  # tail
        meshColors[11] = red  # tail
        meshColors[12] = green  # rudder
        return points, meshColors

    def _points_to_mesh(self, points):
        """"
        Converts points to triangular mesh
        Each mesh face is defined by three 3D points
          (a rectangle requires two triangular mesh faces)
        """
        points=points.T
        mesh = np.array([[points[0], points[1], points[2]],  # noset
                         [points[0], points[2], points[3]],  # noser
                         [points[0], points[3], points[4]],  # noseb
                         [points[0], points[4], points[1]],  # nosel
                         [points[5], points[1], points[2]],  # flt
                         [points[5], points[2], points[3]],  # flr
                         [points[5], points[3], points[4]],  # flb
                         [points[5], points[4], points[1]],  # fll
                         [points[6], points[7], points[8]],  # wing
                         [points[8], points[9], points[6]],  # wing
                         [points[10], points[11], points[12]],  # tail
                         [points[12], points[13], points[10]],  # tail
                         [points[5], points[14], points[15]],  # rudder
                         ])
        return mesh

    def _Euler2Rotation(self, phi, theta, psi):
        """
        Converts euler angles to rotation matrix (R_b^i, i.e., body to inertial)
        """
        # only call sin and cos once for each angle to speed up rendering
        c_phi = np.cos(phi)
        s_phi = np.sin(phi)
        c_theta = np.cos(theta)
        s_theta = np.sin(theta)
        c_psi = np.cos(psi)
        s_psi = np.sin(psi)

        R_roll = np.array([[1, 0, 0],
                           [0, c_phi, s_phi],
                           [0, -s_phi, c_phi]])
        R_pitch = np.array([[c_theta, 0, -s_theta],
                            [0, 1, 0],
                            [s_theta, 0, c_theta]])
        R_yaw = np.array([[c_psi, s_psi, 0],
                          [-s_psi, c_psi, 0],
                          [0, 0, 1]])
        R = R_roll @ R_pitch @ R_yaw  # inertial to body (Equation 2.4 in book)
        return R.T  # transpose to return body to inertial

    # def x_circleplot(self, path,state):
        
    #     N = 100
    #     red = np.array([[1., 0., 0., 1]])
    #     theta = 0
    #     self.pointsX = np.array([[path.orbit_center.item(0) + path.orbit_radius,
    #                         path.orbit_center.item(1),
    #                         path.orbit_center.item(2)]])
    #     path_color = red
    #     i=0
    #     for i in range(0, N):
    #         theta += 2 * np.pi / N
    #         new_point = np.array([[path.orbit_center.item(0) + path.orbit_radius * np.cos(theta),
    #                             path.orbit_center.item(1) + path.orbit_radius * np.sin(theta),
    #                             path.orbit_center.item(2) ]])
    #         self.pointsX = np.concatenate((self.pointsX, new_point), axis=0)
    #         path_color = np.concatenate((path_color, red), axis=0)
    #     pointlistX = self.pointsX.T
        
    #     spacecraft_positionX = np.array([[0], [0], [300]])  # NED coordinates
    #     # attitude of spacecraft as a rotation matrix R from body to inertial
    #     R = self._Euler2Rotation(state.phi, state.theta, state.psi)
    #     # rotate and translate points defining spacecraft
    #     rotated_pointsX = self._rotate_points(pointlistX, R)
        
    #     translated_pointsX = self._translate_points(rotated_pointsX, spacecraft_positionX)
    #     print("R:",R)
    #     print("pointlisxx:",pointlistX)
    #     print("Rotated:",rotated_pointsX)
        
        
    #     '''R = np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]])
    #     translated_pointsX = R @ translated_pointsX'''
    #     translated_pointsX = translated_pointsX.T
    #     print("Translated:",translated_pointsX)
        
        
    #     object = gl.GLLinePlotItem(pos=translated_pointsX,
    #                             color=path_color,
    #                             width=2,
    #                             antialias=True,
    #                             mode='line_strip')

    #     return object
    # def y_circleplot(self, path):
    #     N = 100
    #     red = np.array([[1., 0., 0., 1]])
    #     theta = 0
    #     self.pointsY = np.array([[path.orbit_center.item(0) + path.orbit_radius,
    #                         path.orbit_center.item(1),
    #                         path.orbit_center.item(2)]])
    #     path_color = red
    #     for i in range(0, N):
    #         theta += 2 * np.pi / N
    #         new_point = np.array([[path.orbit_center.item(0) + path.orbit_radius * np.cos(theta),
    #                             path.orbit_center.item(1) ,
    #                             path.orbit_center.item(2) + path.orbit_radius * np.sin(theta) ]])
    #         self.pointsY = np.concatenate((self.pointsY, new_point), axis=0)
    #         path_color = np.concatenate((path_color, red), axis=0)
    #     # convert North-East Down to East-North-Up for rendering
    #     R = np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]])
    #     self.pointsY = self.pointsY @ R.T
    #     object = gl.GLLinePlotItem(pos=self.pointsY,
    #                             color=path_color,
    #                             width=2,
    #                             antialias=True,
    #                             mode='line_strip')
    #     return object
    # def z_circleplot(self, path):
    #     N = 100
    #     red = np.array([[1., 0., 0., 1]])
    #     theta = 0
    #     self.pointsZ = np.array([[path.orbit_center.item(0) ,
    #                         path.orbit_center.item(1),
    #                         path.orbit_center.item(2)+ path.orbit_radius]])
    #     path_color = red
    #     for i in range(0, N):
    #         theta += 2 * np.pi / N
    #         new_point = np.array([[path.orbit_center.item(0) ,
    #                             path.orbit_center.item(1) + path.orbit_radius * np.sin(theta),
    #                             path.orbit_center.item(2) + path.orbit_radius * np.cos(theta)]])
    #         self.pointsZ = np.concatenate((self.pointsZ, new_point), axis=0)
    #         path_color = np.concatenate((path_color, red), axis=0)
    #     # convert North-East Down to East-North-Up for rendering
    #     R = np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]])
    #     self.pointsZ = self.pointsZ @ R.T
    #     object = gl.GLLinePlotItem(pos=self.pointsZ,
    #                             color=path_color,
    #                             width=2,
    #                             antialias=True,
    #                             mode='line_strip')
    #     return object


    def Euler2Quaternion(self,phi, theta, psi):
        cth = np.cos(theta/2)
        cph = np.cos(phi/2)
        cps = np.cos(psi/2)

        sth = np.sin(theta/2)
        sph = np.sin(phi/2)
        sps = np.sin(psi/2)

        e0 = cps*cth*cph+sps*sth*sph
        e1 = cps*cth*sph-sps*sth*cph
        e2 = cps*sth*cph+sps*cth*sph
        e3 = sps*cth*cph+cps*sth*sph
        norm_e = np.linalg.norm(np.array([e0,e1,e2,e3]))
        e = np.array([e0,e1,e2,e3]/norm_e)
        return e
    
    def Quaternion2Rotation(self,e):
        e0 = e.item(0)
        e1 = e.item(1)
        e2 = e.item(2)
        e3 = e.item(3)

        R = np.array([[e0**2 + e1**2 - e2**2 - e3**2, 2*(e1*e2 - e0*e3), 2*(e1*e3 + e0*e2)],
                    [2*(e1*e2 + e0*e3), e0**2 - e1**2 + e2**2 - e3**2, 2*(e2*e3 - e0*e1)],
                    [2*(e1*e3 - e0*e2), 2*(e2*e3 + e0*e1), e0**2 - e1**2 - e2**2 + e3**2]
                    ])
        return R