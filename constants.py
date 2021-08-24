"""This module contains constants that is shared across modules
"""

import win32api
from config import __DEBUG__

screen_width, screen_height = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
v_split = 0.7  # Vertical split of user profile image vs playball area
act_pos = (0.0, v_split - 1)  # Center of playball animation
act_size = [2.0, 1.4]  # Normalized scale of playball animation

uprof_pos_y = 1 - 0.43 * v_split  # Center of user profile section
face_vid_size_px = (1280, 720)  # Native size of face videos
face_vid_aspect_ratio = (
    face_vid_size_px[0] / face_vid_size_px[1]
)  # Aspect ratio of face videos

lface_pos = (-0.5, uprof_pos_y)  # Normalized position for left face
rface_pos = (0.5, uprof_pos_y)  # Normalized position for right face

if __DEBUG__:
    playball_frame_duration = 0.05  # Frame duration of playball
else:
    playball_frame_duration = 0.2  # Frame duration of playball

FPS = 30  # Global frames per second
