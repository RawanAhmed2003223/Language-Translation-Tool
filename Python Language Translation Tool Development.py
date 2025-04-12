import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from googletrans import Translator
import requests
import json

class TranslationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Translation Tool")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # Initialize translator
        self.google_translator = Translator()
        self.microsoft_endpoint = "https://api.cognitive.microsofttranslator.com"
        
        # Supported languages
        self.languages = {
            'Auto Detect': 'auto',
            'English': 'en',
            'Spanish': 'es',
            'French': 'fr',
            'German': 'de',
            'Italian': 'it',
            'Portuguese': 'pt',
            'Russian': 'ru',
            'Chinese': 'zh-cn',
            'Japanese': 'ja',
            'Korean': 'ko',
            'Arabic': 'ar',
            'Hindi': 'hi'
        }
        
        # Microsoft API key
        self.microsoft_key = ""
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        # Configure style
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text="Language Translation Tool", style='Header.TLabel').pack(side=tk.LEFT)
        
        # Settings button
        settings_btn = ttk.Button(header_frame, text="⚙️", width=3, command=self.show_settings)
        settings_btn.pack(side=tk.RIGHT)
        
        # Translation frame
        trans_frame = ttk.Frame(main_frame)
        trans_frame.pack(fill=tk.BOTH, expand=True)
        
        # Source frame
        source_frame = ttk.LabelFrame(trans_frame, text="Source Text")
        source_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.source_text = scrolledtext.ScrolledText(source_frame, wrap=tk.WORD, width=40, height=15, font=('Arial', 10))
        self.source_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Source language
        source_lang_frame = ttk.Frame(source_frame)
        source_lang_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(source_lang_frame, text="From:").pack(side=tk.LEFT)
        self.source_lang = ttk.Combobox(source_lang_frame, values=list(self.languages.keys()), state='readonly')
        self.source_lang.current(0)  # Auto-detect
        self.source_lang.pack(side=tk.LEFT, padx=5)
        
        # Controls frame
        controls_frame = ttk.Frame(trans_frame)
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Translate button
        self.translate_btn = ttk.Button(controls_frame, text="Translate →", command=self.translate_text)
        self.translate_btn.pack(pady=20)
        
        # Swap button
        swap_btn = ttk.Button(controls_frame, text="↔ Swap", command=self.swap_languages)
        swap_btn.pack(pady=5)
        
        # Service selection
        service_frame = ttk.LabelFrame(controls_frame, text="Translation Service")
        service_frame.pack(fill=tk.X, pady=10)
        
        self.service_var = tk.StringVar(value="google")
        ttk.Radiobutton(service_frame, text="Google", variable=self.service_var, value="google").pack(anchor=tk.W)
        ttk.Radiobutton(service_frame, text="Microsoft", variable=self.service_var, value="microsoft").pack(anchor=tk.W)
        
        # Target frame
        target_frame = ttk.LabelFrame(trans_frame, text="Translated Text")
        target_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.target_text = scrolledtext.ScrolledText(target_frame, wrap=tk.WORD, width=40, height=15, font=('Arial', 10))
        self.target_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Target language
        target_lang_frame = ttk.Frame(target_frame)
        target_lang_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(target_lang_frame, text="To:").pack(side=tk.LEFT)
        self.target_lang = ttk.Combobox(target_lang_frame, values=list(self.languages.keys())[1:], state='readonly')
        self.target_lang.current(0)  # English
        self.target_lang.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_bar = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN)
        self.status_bar.pack(fill=tk.X, pady=(5, 0))
        
    def show_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x200")
        
        ttk.Label(settings_window, text="Microsoft Translator Settings", style='Header.TLabel').pack(pady=10)
        
        key_frame = ttk.Frame(settings_window)
        key_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(key_frame, text="API Key:").pack(side=tk.LEFT)
        self.key_entry = ttk.Entry(key_frame, width=40)
        self.key_entry.pack(side=tk.LEFT, padx=5)
        self.key_entry.insert(0, self.microsoft_key)
        
        save_btn = ttk.Button(settings_window, text="Save", command=lambda: self.save_settings(settings_window))
        save_btn.pack(pady=10)
        
    def save_settings(self, window):
        self.microsoft_key = self.key_entry.get()
        window.destroy()
        messagebox.showinfo("Settings", "Microsoft API key saved successfully!")
        
    def translate_text(self):
        text = self.source_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter text to translate")
            return
            
        src_lang_name = self.source_lang.get()
        target_lang_name = self.target_lang.get()
        
        src_lang = self.languages[src_lang_name]
        target_lang = self.languages[target_lang_name]
        
        self.status_bar.config(text="Translating...")
        self.root.update()
        
        try:
            if self.service_var.get() == "google":
                translated = self.google_translate(text, target_lang, src_lang)
            else:
                if not self.microsoft_key:
                    messagebox.showerror("Error", "Microsoft API key is required")
                    self.status_bar.config(text="Ready")
                    return
                translated = self.microsoft_translate(text, target_lang, src_lang if src_lang != 'auto' else None)
            
            if translated:
                self.target_text.delete("1.0", tk.END)
                self.target_text.insert("1.0", translated)
                
                # Update status with detection info if auto-detected
                if src_lang == 'auto':
                    detected = self.detect_language(text)
                    if detected:
                        lang_name = self.get_language_name(detected[0])
                        self.status_bar.config(text=f"Detected source language: {lang_name} ({detected[0]}) with {detected[1]:.0%} confidence")
                    else:
                        self.status_bar.config(text="Translation complete (source language auto-detected)")
                else:
                    self.status_bar.config(text="Translation complete")
            else:
                self.status_bar.config(text="Translation failed")
                
        except Exception as e:
            messagebox.showerror("Error", f"Translation failed: {str(e)}")
            self.status_bar.config(text="Error occurred")
        
    def google_translate(self, text, dest_language, src_language='auto'):
        try:
            translation = self.google_translator.translate(text, dest=dest_language, src=src_language)
            return translation.text
        except Exception as e:
            raise Exception(f"Google Translate error: {e}")
    
    def microsoft_translate(self, text, dest_language, src_language=None):
        try:
            path = '/translate?api-version=3.0'
            params = f'&to={dest_language}'
            if src_language:
                params += f'&from={src_language}'
            
            url = self.microsoft_endpoint + path + params
            
            headers = {
                'Ocp-Apim-Subscription-Key': self.microsoft_key,
                'Content-type': 'application/json',
            }
            
            body = [{'text': text}]
            
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()
            
            result = response.json()
            return result[0]['translations'][0]['text']
        except Exception as e:
            raise Exception(f"Microsoft Translate error: {e}")
    
    def detect_language(self, text):
        try:
            detection = self.google_translator.detect(text)
            return (detection.lang, detection.confidence)
        except:
            return None
    
    def get_language_name(self, code):
        for name, lang_code in self.languages.items():
            if lang_code == code:
                return name
        return code
    
    def swap_languages(self):
        # Get current values
        src_lang = self.source_lang.get()
        target_lang = self.target_lang.get()
        
        # Don't swap if source is auto-detect
        if src_lang == "Auto Detect":
            return
            
        # Get current texts
        src_text = self.source_text.get("1.0", tk.END).strip()
        target_text = self.target_text.get("1.0", tk.END).strip()
        
        # Swap languages
        src_index = self.source_lang['values'].index(target_lang)
        self.source_lang.current(src_index)
        
        target_index = self.target_lang['values'].index(src_lang) if src_lang in self.target_lang['values'] else 0
        self.target_lang.current(target_index)
        
        # Swap texts if target text exists
        if target_text:
            self.source_text.delete("1.0", tk.END)
            self.source_text.insert("1.0", target_text)
            
            self.target_text.delete("1.0", tk.END)
            self.target_text.insert("1.0", src_text)
            
            self.status_bar.config(text="Languages and texts swapped")

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslationApp(root)
    root.mainloop()