# -*- coding: utf-8 -*-
import cv2
import numpy as np

# Charger la vidéo
video_capture = cv2.VideoCapture("project_video.mp4")

def region_of_interest(img, vertices):
    #defining a blank mask to start with
    mask = np.zeros_like(img)   
    
    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def extend_lines(img, lines, center_left=0, center_right=0):
    center = img.shape[1] / 2  # Center of the image width
    exclusion_left = center - (center * center_left)
    exclusion_right = center + (center * center_right)

    left_lines = [] 
    right_lines = []  

    for line in lines:
        for x1, y1, x2, y2 in line:
            if x2 == x1:
                continue  # Avoid division by zero
            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - (slope * x1)

            if (x1 > exclusion_left and x1 < exclusion_right) or (x2 > exclusion_left and x2 < exclusion_right):
                continue

            # Filter out nearly horizontal lines
            if abs(slope) < 0.5:
                continue

            if slope < 0:  # Negative slope: line belongs to the left side
                left_lines.append((slope, intercept))
            else:  # Positive slope: line belongs to the right side
                right_lines.append((slope, intercept))

    def average_slope_intercept(lines):
        if lines:
            slope, intercept = np.mean(lines, axis=0)
            y1 = img.shape[0]  # Bottom of the image
            y2 = int(y1 * 0.6)  # Up to 60% of the height from the bottom
            x1 = int((y1 - intercept) / slope)
            x2 = int((y2 - intercept) / slope)
            return (x1, y1, x2, y2)
        else:
            return None

    left_line = average_slope_intercept(left_lines)
    right_line = average_slope_intercept(right_lines)

    return left_line, right_line

# Fonction pour détecter les lignes
def detect_lines(frame, hist_right, hist_left, direction, mean_point):
    x_milieu = frame.shape[1]/2
    base_y = frame.shape[0]
    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Détection des contours avec la méthode de Canny
    edges = cv2.Canny(gray, 200, 200)
    # Appliquer une transformation de Hough pour détecter les lignes
    img_shape = frame.shape
    vertices = np.array([[(img_shape[1]*0.20,img_shape[0]),(img_shape[1]*0.40, img_shape[0]*0.60), 
                          (img_shape[1]*0.55, img_shape[0]*0.60), (img_shape[1],img_shape[0])]], dtype=np.int32)
        
    #Application d'un masque pour avoir les régions d'intérêt
    img_masked_edges = region_of_interest(edges, vertices)
    lines = cv2.HoughLinesP(img_masked_edges, 1, np.pi/180, 100, minLineLength=50, maxLineGap=50)
    
    if lines is not None:
        left_lines = [] # pour le tri des lignes
        right_lines = [] #pour le tri des lignes
        for line in lines:
            x1, y1, x2, y2 = line[0]
            slope = (y2 - y1) / (x2 - x1)
            # Filtrer les lignes en fonction de leur pente et position
            if (frame.shape[1]/4 < x1 < frame.shape[1] - frame.shape[1]/8 and 
                frame.shape[1]/4 < x2 < frame.shape[1]- frame.shape[1]/8 and 
                (0.5 < slope or slope < -0.5) and 
                y1 > frame.shape[0] /4 and y2 > frame.shape[0] /4) :
    
                # Ajouter la ligne à gauche ou à droite
                if x1 < frame.shape[1] / 2 and x2 < frame.shape[1] / 2:
                    left_lines.append(line)
                elif x1 > frame.shape[1] / 2 and x2 > frame.shape[1] / 2:
                    right_lines.append(line)
            
            #Etendre la ligne jusqu'au bas de l'image pour avoir le point d'intersection de la ligne avec la base de l'image
            left_line, right_line = extend_lines(frame, lines, 0, 0.3)
            
            #Enregistement de l'historique des lignes
            if left_line is not None :
                hist_left.append(left_line)
            if right_line is not None :
                hist_right.append(right_line)
                
           
            #Calcul de la moyenne entre les 2 points d'intersection entre les deux lignes et la base de l'image
            if left_line is not None:
                if right_line is not None : 
                    mean_point = (left_line[2] + right_line[2])/2
                elif len(hist_right)>0 :
                    mean_point = (left_line[2] + hist_right[-1][2])/2
            elif right_line is not None :
                if len(hist_left)>0:
                    mean_point = (hist_left[-1][2] + right_line[2])/2
            elif len(hist_left)>0 and len(hist_right)>0:
                    mean_point = (hist_left[-1][2] + hist_right[-1][2])/2
            
            # Détermination de la direction en fonction de la moyenne calculée
            if mean_point < x_milieu:
                direction = "gauche"
            elif mean_point > x_milieu:
                direction = "droite"
            else:
                direction = "milieu"
                
            #Calcul de la distance réelle entre la voiture et le centre de l'image
            distance_centre = np.abs(x_milieu - mean_point) * 3.5 / frame.shape[1]
            cv2.putText(frame, "Direction : {}".format(direction), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, f"Centre de l'image: {x_milieu}", (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, f"Distance du centre de l'image: {distance_centre:.2f}m a {direction}", (50, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


        
        #Dessin des lignes détectées actuellement, ou si il n'y a pas de ligne détectée à l'instant t, dessiner la dernière ligne de l'historique
        if left_line is not None:
            x1, y1, x2, y2 = left_line
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
        elif len(hist_left)>0:
            x1, y1, x2, y2 = hist_left[-1]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
        if right_line is not None:
            x1, y1, x2, y2 = right_line
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
        elif len(hist_right)>0:
            x1, y1, x2, y2 = hist_right[-1]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
            
        if left_line is None and len(hist_left) > 0:
            left_line = hist_left[-1]
        
        if right_line is None and len(hist_right) > 0:
            right_line = hist_right[-1]
            
        if left_line is not None and right_line is not None:
            left_x1, left_y1, left_x2, left_y2 = left_line
            right_x1, right_y1, right_x2, right_y2 = right_line
            # Calculer les points d'intersection
            intersection_point1 = np.array([left_x1, left_y1])
            intersection_point2 = np.array([right_x1, right_y1])
            intersection_point3 = np.array([left_x2, left_y2])
            intersection_point4 = np.array([right_x2, right_y2])
            # Définir les points de la région d'intérêt
            pts = np.array([intersection_point1, intersection_point2, intersection_point4, intersection_point3], np.int32)
            pts = pts.reshape((-1, 1, 2))
            mask = np.zeros_like(frame, dtype=np.uint8)
            color = (0, 100, 0)  # Couleur verte
            cv2.fillPoly(mask, [pts], color)

            # Définir l'opacité (transparence)
            alpha = 0.4  # Valeur entre 0 (transparent) et 1 (opaque)

            # Mélanger la couleur de remplissage avec la région d'origine
            cv2.addWeighted(mask, alpha, frame, 1 - alpha, 0, frame)
    return frame

hist_left= []
hist_right = []
direction = ""
mean_point = 0

# Lecture de la vidéo
while video_capture.isOpened():
    ret, frame = video_capture.read()
    if not ret:
        break
    frame_with_lines = detect_lines(frame, hist_right, hist_left, direction, mean_point)
    cv2.imshow('Video avec lignes détectées', frame_with_lines)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Libérer la capture vidéo et fermer les fenêtres OpenCV
video_capture.release()
cv2.destroyAllWindows()
