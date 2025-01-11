import time
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up WebDriver with necessary options
def setup_driver():
    options = Options()
    options.headless = True  # Running the browser in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Extract iframe src URLs from the given URL
def extract_iframe_src(driver, url):
    try:
        driver.get(url)
        time.sleep(2)  # Wait for the page to stabilize

        # Find all iframe elements on the page
        iframes = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'iframe'))
        )

        iframe_sources = []
        for iframe in iframes:
            src = iframe.get_attribute('src')
            if src:
                iframe_sources.append(src)

        return iframe_sources
    except Exception as e:
        print(f"Error extracting iframe sources: {e}")
        return []

# Filter iframe sources for video URLs (e.g., ok.ru, animeiat.xyz)
def filter_video_sources(iframe_sources):
    video_sources = []
    for src in iframe_sources:
        if 'ok.ru' in src or 'animeiat.xyz' in src:
            video_sources.append(src)
    return video_sources

# Create the GUI window
def create_gui():
    root = tk.Tk()
    root.title("BURGERANIME - Anime Video URL Extractor")
    root.geometry("600x450")
    root.config(bg="#f5f5f5")

    # Fonts
    font_title = ("Helvetica", 16, "bold")
    font_medium = ("Helvetica", 12)

    # Title label
    title_label = tk.Label(root, text="BURGERANIME - Anime Video URL Extractor", font=font_title, bg="#f5f5f5", fg="#4CAF50")
    title_label.pack(pady=20)

    # URL Input Section
    url_label = tk.Label(root, text="Enter Anime URL:", font=font_medium, bg="#f5f5f5")
    url_label.pack(pady=5)

    url_entry = tk.Entry(root, width=50, font=font_medium, borderwidth=2, relief="solid")
    url_entry.pack(padx=10, pady=10)

    # Output Section
    result_text = tk.Text(root, width=70, height=10, font=font_medium, wrap=tk.WORD, padx=10, pady=10)
    result_text.pack(pady=10)
    result_text.config(state=tk.DISABLED)

    # Fetch Button
    def fetch_data():
        url = url_entry.get()
        if not url:
            messagebox.showerror("Input Error", "Please enter a valid URL.")
            return

        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)  # Clear previous results
        result_text.insert(tk.END, "Fetching data...\n")

        # Set up the WebDriver
        driver = setup_driver()
        try:
            # Extract iframe sources
            iframe_sources = extract_iframe_src(driver, url)
            result_text.insert(tk.END, f"Found {len(iframe_sources)} iframe sources:\n")
            for src in iframe_sources:
                result_text.insert(tk.END, f"  - {src}\n")

            # Filter out the video URLs
            video_sources = filter_video_sources(iframe_sources)
            if video_sources:
                result_text.insert(tk.END, f"\nFound video URLs:\n")
                for video in video_sources:
                    result_text.insert(tk.END, f"  - {video}\n")
            else:
                result_text.insert(tk.END, "\nNo video URLs found.\n")

        except Exception as e:
            result_text.insert(tk.END, f"Error: {e}\n")
        finally:
            driver.quit()

        result_text.config(state=tk.DISABLED)

    # Fetch Button
    fetch_button = tk.Button(root, text="Fetch Data", font=font_medium, command=fetch_data, bg="#4CAF50", fg="white", relief="solid")
    fetch_button.pack(pady=10)

    # Copyright Label
    copyright_label = tk.Label(root, text="© 2025 BURGERANIME - By amadich", font=("Helvetica", 10), bg="#f5f5f5", fg="#777")
    copyright_label.pack(side=tk.BOTTOM, pady=10)

    # Run the main loop
    root.mainloop()

# Run the program
if __name__ == "__main__":
    create_gui()
