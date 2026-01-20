#!/usr/bin/env python3
"""
Simple GUI for AES-128-CBC File Encryption/Decryption
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
from aes_encrypt import encrypt_file, decrypt_file, display_encrypted_string


class AESEncryptionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AES-128-CBC File Encryption")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variables
        self.selected_file = tk.StringVar(value="No file selected")
        self.key_var = tk.StringVar()
        
        # Create UI
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="AES-128-CBC File Encryption", 
            font=("Arial", 16, "bold"),
            pady=10
        )
        title_label.pack()
        
        # File selection frame
        file_frame = tk.Frame(self.root, pady=10)
        file_frame.pack(fill=tk.X, padx=20, expand=False)
        
        tk.Label(file_frame, text="File:", font=("Arial", 10)).pack(side=tk.LEFT)
        file_label = tk.Label(
            file_frame, 
            textvariable=self.selected_file, 
            font=("Arial", 9),
            fg="gray",
            anchor="w"
        )
        file_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        select_btn = tk.Button(
            file_frame, 
            text="Select File", 
            command=self.select_file,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10),
            padx=15
        )
        select_btn.pack(side=tk.RIGHT)
        
        # Key frame
        key_frame = tk.Frame(self.root, pady=15)
        key_frame.pack(fill=tk.X, padx=20, expand=False)
        
        tk.Label(
            key_frame, 
            text="Key or passphrase (hex key = 32 chars, or any text):", 
            font=("Arial", 10)
        ).pack(anchor="w")
        
        key_entry = tk.Entry(
            key_frame, 
            textvariable=self.key_var, 
            font=("Courier", 10),
            width=50
        )
        key_entry.pack(fill=tk.X, pady=5)
        
        tk.Label(
            key_frame, 
            text="(Leave empty for encryption - random key/IV will be generated)", 
            font=("Arial", 8),
            fg="gray"
        ).pack(anchor="w")
        
        # Buttons frame
        button_frame = tk.Frame(self.root, pady=20)
        button_frame.pack(expand=False)
        
        encrypt_btn = tk.Button(
            button_frame,
            text="🔒 Encrypt File",
            command=self.encrypt,
            bg="#2196F3",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=30,
            pady=10,
            width=15
        )
        encrypt_btn.pack(side=tk.LEFT, padx=10)
        
        decrypt_btn = tk.Button(
            button_frame,
            text="🔓 Decrypt File",
            command=self.decrypt,
            bg="#FF9800",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=30,
            pady=10,
            width=15
        )
        decrypt_btn.pack(side=tk.LEFT, padx=10)
        
        # Output frame
        output_frame = tk.Frame(self.root)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        tk.Label(
            output_frame, 
            text="Output:", 
            font=("Arial", 10, "bold")
        ).pack(anchor="w")
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            height=12,
            font=("Courier", 8),
            wrap=tk.CHAR,
            state=tk.DISABLED,
            width=80
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=5)
    
    def select_file(self):
        filename = filedialog.askopenfilename(
            title="Select file to encrypt/decrypt",
            filetypes=[("All files", "*.*")]
        )
        if filename:
            self.selected_file.set(os.path.basename(filename))
            self.root.selected_file_path = filename
            self.log_output(f"Selected: {os.path.basename(filename)}")
    
    def log_output(self, message, clear=False, add_newline=True):
        self.output_text.config(state=tk.NORMAL)
        if clear:
            self.output_text.delete(1.0, tk.END)
        if add_newline:
            self.output_text.insert(tk.END, message + "\n")
        else:
            self.output_text.insert(tk.END, message)
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.root.update()
    
    def encrypt(self):
        if not hasattr(self.root, 'selected_file_path'):
            messagebox.showerror("Error", "Please select a file first!")
            return
        
        try:
            self.log_output("=" * 60, clear=True)
            self.log_output("ENCRYPTING FILE...")
            self.log_output("=" * 60)
            self.log_output(f"File: {os.path.basename(self.root.selected_file_path)}")
            
            # Encrypt file
            key_hex_out, iv_hex_out = encrypt_file(self.root.selected_file_path, self.key_var.get().strip() or None)
            
            # Read and display encrypted content in dense format (Latin-1)
            with open(self.root.selected_file_path, 'r', encoding='latin-1') as f:
                dense_display = f.read()
            
            self.log_output("\n" + "=" * 60)
            self.log_output("ENCRYPTION SUCCESSFUL!")
            self.log_output("=" * 60)
            self.log_output(f"\nGenerated Key (hex):")
            self.log_output(f"{key_hex_out}")
            self.log_output(f"IV (hex): {iv_hex_out}")
            self.log_output("\n⚠️ IMPORTANT: Save this key to decrypt the file!")
            self.log_output("=" * 60)
            self.log_output(f"\nEncrypted Content (Latin-1): {len(dense_display)} chars")
            self.log_output(dense_display, add_newline=False)
            self.log_output("\n" + "=" * 60)
            
            # Update key field
            self.key_var.set(key_hex_out)
            
            messagebox.showinfo(
                "Success", 
                f"File encrypted successfully!\n\nKey: {key_hex_out}\nIV: {iv_hex_out}\n\nSave the key!"
            )
            
        except Exception as e:
            error_msg = f"Encryption failed: {str(e)}"
            self.log_output("\n" + "=" * 60)
            self.log_output("ERROR!")
            self.log_output("=" * 60)
            self.log_output(error_msg)
            messagebox.showerror("Error", error_msg)
    
    def decrypt(self):
        if not hasattr(self.root, 'selected_file_path'):
            messagebox.showerror("Error", "Please select a file first!")
            return
        
        key_hex = self.key_var.get().strip()
        if not key_hex:
            messagebox.showerror("Error", "Please enter the 128-bit key!")
            return
        
        try:
            self.log_output("=" * 60, clear=True)
            self.log_output("DECRYPTING FILE...")
            self.log_output("=" * 60)
            self.log_output(f"File: {os.path.basename(self.root.selected_file_path)}")
            self.log_output(f"Key: {key_hex}")
            
            # Decrypt file
            decrypt_file(self.root.selected_file_path, key_hex)
            
            self.log_output("\n" + "=" * 60)
            self.log_output("DECRYPTION SUCCESSFUL!")
            self.log_output("=" * 60)
            
            # Read and display decrypted content
            try:
                with open(self.root.selected_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.log_output("\nDecrypted Content:")
                    self.log_output("-" * 60)
                    self.log_output(content)
                    self.log_output("-" * 60)
            except UnicodeDecodeError:
                self.log_output("\n(Binary file - content not displayed)")
            
            messagebox.showinfo("Success", "File decrypted successfully!")
            
        except ValueError as e:
            error_msg = str(e)
            self.log_output("\n" + "=" * 60)
            self.log_output("ERROR!")
            self.log_output("=" * 60)
            self.log_output(error_msg)
            messagebox.showerror("Error", error_msg)
        except Exception as e:
            error_msg = f"Decryption failed: {str(e)}"
            self.log_output("\n" + "=" * 60)
            self.log_output("ERROR!")
            self.log_output("=" * 60)
            self.log_output(error_msg)
            messagebox.showerror("Error", error_msg)


def main():
    root = tk.Tk()
    app = AESEncryptionGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()

