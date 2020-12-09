import face_recognition
import cv2
import numpy as np
from transitions import Machine
import random
import pygame
from pygame.locals import *

import face_recognition
import cv2
import numpy as np

def rec():
    global name
    video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
    obama_image = face_recognition.load_image_file("obama.jpg")
    obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

    # Load a second sample picture and learn how to recognize it.
    biden_image = face_recognition.load_image_file("biden.jpg")
    biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        obama_face_encoding,
        biden_face_encoding
    ]
    known_face_names = [
        "Barack Obama",
        "Joe Biden"
    ]

    # Initialize some variables
    
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        face_locations = [0,0,0,0]
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                

                # # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)
        if len(face_locations) > 0 :
            App.running = False
            face.active()
        else:

            face.inactive()
            



        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

class Text:
    """Create a text object."""

    def __init__(self, text, pos, **options):
        self.text = text
        self.pos = pos

        self.fontname = 'freesansbold.ttf'
        self.fontsize = 32
        self.green = (0, 255, 0)
        self.blue = (0, 0, 128)
        self.set_font()
        self.render()

    def set_font(self):
        """Set the Font object from name and size."""
        self.font = pygame.font.Font(self.fontname, self.fontsize)

    def render(self):
        """Render the text into an image."""
        self.img = self.font.render(self.text, True,self.green,self.blue)
        self.rect = self.img.get_rect()
        self.rect.center = (200 , 200)

    def draw(self):
        """Draw the text image to the screen."""
        App.screen.blit(self.img, self.rect)

class App:
    """Create a single-window app with multiple scenes."""

    def __init__(self):
        """Initialize pygame and the application."""
        pygame.init()
        flags = RESIZABLE
        App.screen = pygame.display.set_mode((400, 400), flags)

        App.running = True

    def run(self):
        global name
        """Run the main event loop."""
        while App.running:
            if face.state == 'MachineInactive' :
                App.t = Text("Application Inactive", pos=(20, 20))
            elif face.state == 'MachineActive':
                App.t = Text(name, pos=(20, 20))

            
            for event in pygame.event.get():
                if event.type == QUIT:
                    App.running = False

            App.screen.fill(Color('gray'))
            App.t.draw()
            pygame.display.update()
            r = rec()
            

        pygame.quit()




class FaceRecognitionMachine():
    global name
    # Define some states. Most of the time, narcoleptic superheroes are just like
    # everyone else. Except for...
    states = ['MachineActive', 'MachineInactive']
    # A more compact version of the quickstart transitions
    transitions = [
                   {'trigger': 'active', 'source': '*', 'dest':  'MachineActive', 'after': 'display_name'},
                   {'trigger': 'inactive', 'source': '*', 'dest':  'MachineInactive', 'after': 'display_none'},
                  ]


    def __init__(self):

        # Initialize the state machine
        self.machine = Machine(model=self, states=FaceRecognitionMachine.states,
                               transitions=FaceRecognitionMachine.transitions, initial='MachineInactive')

    def display_name(self):
        App().run()
    
    def display_none(self):
        App().run()
        

        
face =  FaceRecognitionMachine()
assert face.state == 'MachineInactive'
name = "Unknown"
face.display_none()