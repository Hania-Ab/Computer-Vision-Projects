# Projet de Détection de Lignes de Voie avec OpenCV

Bienvenue sur le dépôt de mon projet de détection de lignes de voie en temps réel utilisant OpenCV en Python. Ce projet vise à identifier et suivre les lignes de voie sur une vidéo, offrant ainsi des informations précieuses telles que la direction du véhicule et la distance par rapport au centre de la voie.

## Table des Matières

- [Description](#description)
- [Fonctionnalités](#fonctionnalités)
- [Méthodologie](#méthodologie)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Explications du Code](#explications-du-code)
- [Affichage des résultats](#affichage-des-résultats)

## Description

Ce projet implémente un système de détection de lignes de voie qui analyse une vidéo pour identifier les lignes de gauche et de droite sur la route. En utilisant des techniques de traitement d'images telles que la conversion en niveaux de gris, la détection de contours avec l'algorithme de Canny, et la transformation de Hough, le système est capable de tracer les lignes de voie, de déterminer la direction du véhicule (gauche, droite, milieu) et de calculer la distance par rapport au centre de la voie. De plus, un historique des lignes détectées est maintenu pour assurer une détection continue même en cas de perte momentanée des lignes.

## Fonctionnalités

- **Conversion en Niveaux de Gris :** Simplifie l'image pour faciliter la détection des contours.

- **Détection de Contours (Canny) :** Identifie les bords dans l'image.

- **Masquage de la Région d'Intérêt :** Se concentre sur la partie pertinente de l'image (zone de la route).

- **Transformation de Hough :** Détecte les lignes droites dans l'image.

- **Filtrage des Lignes :** Élimine les lignes horizontales et celles situées aux extrémités de l'image.

- **Agrégation des Lignes :** Moyenne des lignes détectées pour obtenir une ligne unique de chaque côté.
  
- **Historique des Lignes :** Maintien des lignes détectées pour une détection stable.

- **Affichage des Informations :** Direction du véhicule et distance par rapport au centre de la voie.

## Méthodologie

### 1- Prétraitement de l'Image

- **Conversion en Niveaux de Gris :** Réduit la complexité de l'image en supprimant les informations de couleur.

- **Détection des Contours avec Canny :** Identifie les bords de l'image en appliquant l'algorithme de Canny avec un seuil de 200.

### 2. Définition de la Région d'Intérêt

- **Application d'un Masque :** Se concentre sur la partie de l'image où les lignes de voie sont attendues, généralement en bas au centre de l'image.

### 3. Détection des Lignes avec la Transformation de Hough

- **Transformation de Hough Probabiliste :** Identifie les segments de ligne dans l'image masquée.

### 4. Filtrage et Classification des Lignes

- **Filtrage des Lignes Inutiles :** Élimine les lignes horizontales et celles situées aux extrémités de l'image.

- **Classification des Lignes :** Sépare les lignes en listes de gauche et de droite en fonction de leur pente.

### 5. Agrégation des Lignes

- **Calcul de la Moyenne :** Obtient une ligne unique pour la gauche et une pour la droite en calculant la moyenne des pentes et des intercepts.

### 6. Historique des Lignes

- **Maintien des Lignes Détectées :** Garde en mémoire les dernières lignes détectées pour assurer une détection continue même si une ligne temporairement absente.

### 7. Affichage des Informations

- **Direction du Véhicule :** Détermine si la direction est à gauche, droite ou au milieu en fonction de la position des lignes par rapport au centre de l'image.

- **Distance par Rapport au Centre :** Calcule la distance entre le centre de l'image et le point médian des lignes détectées.

## Installation

### Prérequis
- Python 3.11.5
- OpenCV
- NumPy

## Utilisation

## Explications du Code

## Affichage des résultats
