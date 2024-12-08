import sys
import os
import pygame
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import font
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from PIL import Image, ImageTk

class RSAGUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RSA Encryption/Decryption")
        self.root.geometry("800x600")  # Taille initiale de la fenêtre
        self.root.minsize(600, 400)  # Taille minimale
        self.root.config(bg="#000000")  # Fond noir

        # Vérification si le programme est exécuté dans un fichier .exe (PyInstaller)
        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS  # Dossier temporaire où PyInstaller extrait les fichiers
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))  # Si en développement

        # Définir les chemins complets des fichiers vidéo et audio
        self.video_source = os.path.join(application_path, "video.mp4")
        self.music_file = os.path.join(application_path, "coden.mp3")

        # Initialiser pygame pour la musique
        pygame.mixer.init()

        # Lire la vidéo
        self.cap = cv2.VideoCapture(self.video_source)

        # Jouer la musique en arrière-plan
        pygame.mixer.music.load(self.music_file)
        pygame.mixer.music.play(-1, 0.0)  # Loop la musique

        # Ajouter une police personnalisée
        self.title_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=10)
        
        # Création d'un Canvas pour afficher la vidéo
        self.canvas = tk.Canvas(self.root, bg="black", width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Label de titre
        self.title_label = tk.Label(self.root, text="RSA Encryption/Decryption - Logiciel Kairyct7 branche de Klexou", font=self.title_font, fg="white", bg="#000000")
        self.title_label.place(x=50, y=30)

        # Ajouter un cadre pour les boutons, pour ne pas être masqué par la vidéo
        self.button_frame = tk.Frame(self.root, bg="#000000")
        self.button_frame.place(relx=0.5, rely=0.5, anchor="center")  # Centrer les boutons

        # Section Génération de Clés
        self.generate_button = tk.Button(self.button_frame, text="Générer des Clés", command=self.generate_keys, font=self.button_font, bg="#4CAF50", fg="white", relief="raised", width=20)
        self.generate_button.grid(row=0, column=0, pady=10)

        # Section Chiffrement
        self.encrypt_button = tk.Button(self.button_frame, text="Chiffrer un Message", command=self.encrypt_message, font=self.button_font, bg="#4CAF50", fg="white", relief="raised", width=20)
        self.encrypt_button.grid(row=1, column=0, pady=10)

        # Section Déchiffrement
        self.decrypt_button = tk.Button(self.button_frame, text="Déchiffrer un Message", command=self.decrypt_message, font=self.button_font, bg="#4CAF50", fg="white", relief="raised", width=20)
        self.decrypt_button.grid(row=2, column=0, pady=10)

        # Copyright
        self.copyright_label = tk.Label(self.root, text="© Klexou Kairyct7", font=("Helvetica", 8), fg="gray", bg="#000000")
        self.copyright_label.place(x=350, y=550)  # Positionner le copyright au bas de la fenêtre

        # Mettre à jour la vidéo
        self.update_video()

    def generate_keys(self):
        """Générer des clés et les sauvegarder dans des fichiers."""
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()

        # Sauvegarder les clés
        with open("client_private_key.pem", "wb") as priv_file:
            priv_file.write(private_key)
        with open("client_public_key.pem", "wb") as pub_file:
            pub_file.write(public_key)

        messagebox.showinfo("Succès", "Clés générées avec succès !\n"
                                      "Clé privée : client_private_key.pem\n"
                                      "Clé publique : client_public_key.pem")

    def encrypt_message(self):
        """Chiffrer un message."""
        # Sélectionner la clé publique
        public_key_file = filedialog.askopenfilename(title="Sélectionnez la clé publique", filetypes=[("PEM Files", "*.pem")])
        if not public_key_file:
            return

        # Charger la clé publique
        try:
            with open(public_key_file, "rb") as file:
                public_key = RSA.import_key(file.read())
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lire la clé publique : {e}")
            return

        # Entrer le message à chiffrer
        message = simpledialog.askstring("Message", "Entrez le message à chiffrer :")
        if not message:
            return

        # Chiffrement
        cipher = PKCS1_OAEP.new(public_key)
        encrypted_message = cipher.encrypt(message.encode())

        # Sauvegarder le message chiffré
        with open("message_chiffre.txt", "wb") as file:
            file.write(encrypted_message)

        messagebox.showinfo("Succès", "Message chiffré et sauvegardé dans 'message_chiffre.txt'.")

    def decrypt_message(self):
        """Déchiffrer un message."""
        # Sélectionner la clé privée
        private_key_file = filedialog.askopenfilename(title="Sélectionnez votre clé privée", filetypes=[("PEM Files", "*.pem")])
        if not private_key_file:
            return

        # Charger la clé privée
        try:
            with open(private_key_file, "rb") as file:
                private_key = RSA.import_key(file.read())
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lire la clé privée : {e}")
            return

        # Sélectionner le fichier du message chiffré
        encrypted_file = filedialog.askopenfilename(title="Sélectionnez le fichier du message chiffré", filetypes=[("Text Files", "*.txt")])
        if not encrypted_file:
            return

        # Charger le message chiffré
        try:
            with open(encrypted_file, "rb") as file:
                encrypted_message = file.read()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lire le fichier : {e}")
            return

        # Déchiffrement
        cipher = PKCS1_OAEP.new(private_key)
        try:
            decrypted_message = cipher.decrypt(encrypted_message)
            messagebox.showinfo("Message Déchiffré", decrypted_message.decode())
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec du déchiffrement : {e}")

    def update_video(self):
        """Mettre à jour l'image de la vidéo dans la fenêtre."""
        ret, frame = self.cap.read()
        if ret:
            # Convertir l'image OpenCV (BGR) en format RGB pour Tkinter
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(img)

            # Afficher la vidéo dans le canvas
            if not hasattr(self, 'video_label'):
                self.video_label = self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
                self.canvas.image = img
            else:
                self.canvas.itemconfig(self.video_label, image=img)
                self.canvas.image = img

            # Mettre à jour la vidéo toutes les 30 ms
            self.root.after(30, self.update_video)
        else:
            # Revenir au début de la vidéo une fois qu'elle est terminée
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)


# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = RSAGUIApp(root)
    root.mainloop()
