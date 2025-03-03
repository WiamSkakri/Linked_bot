import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

class LinkedInBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LinkedIn Connection Bot")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Set app icon if needed
        # self.root.iconbitmap('path/to/icon.ico')
        
        # Variables
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.person_var = tk.StringVar()
        self.event_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready to connect...")
        
        # Initialize driver as None
        self.driver = None
        
        # Create UI components
        self.create_widgets()
        
        # Center the window
        self.center_window()
        
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="LinkedIn Connection Bot", font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # LinkedIn Credentials Frame
        cred_frame = ttk.LabelFrame(main_frame, text="LinkedIn Credentials", padding="10")
        cred_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        # Email
        ttk.Label(cred_frame, text="Email:").grid(row=0, column=0, sticky="w", pady=5)
        email_entry = ttk.Entry(cred_frame, textvariable=self.email_var, width=40)
        email_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        # Password
        ttk.Label(cred_frame, text="Password:").grid(row=1, column=0, sticky="w", pady=5)
        password_entry = ttk.Entry(cred_frame, textvariable=self.password_var, show="*", width=40)
        password_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # Connection Details Frame
        conn_frame = ttk.LabelFrame(main_frame, text="Connection Details", padding="10")
        conn_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        # Person Name
        ttk.Label(conn_frame, text="Person Name:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(conn_frame, textvariable=self.person_var, width=40).grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        # Event Name
        ttk.Label(conn_frame, text="Event Name:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(conn_frame, textvariable=self.event_var, width=40).grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # Connect Button
        connect_button = ttk.Button(main_frame, text="Connect", command=self.start_connection_thread, width=20)
        connect_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Status
        status_frame = ttk.Frame(main_frame, padding="5")
        status_frame.grid(row=4, column=0, columnspan=2, sticky="ew")
        
        self.progress = ttk.Progressbar(status_frame, orient="horizontal", length=300, mode="indeterminate")
        self.progress.pack(side=tk.TOP, fill=tk.X, expand=True, pady=(0, 5))
        
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Set column weight
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        cred_frame.columnconfigure(1, weight=1)
        conn_frame.columnconfigure(1, weight=1)
    
    def start_connection_thread(self):
        # Validate input
        if not self.validate_inputs():
            return
        
        # Start a new thread for LinkedIn operations
        thread = threading.Thread(target=self.connect_to_linkedin)
        thread.daemon = True
        thread.start()
        
        # Start progress bar
        self.progress.start()
    
    def validate_inputs(self):
        # Check if all fields are filled
        if not self.email_var.get() or not self.password_var.get() or not self.person_var.get() or not self.event_var.get():
            messagebox.showerror("Input Error", "All fields are required!")
            return False
        return True
    
    def connect_to_linkedin(self):
        try:
            # Update status
            self.status_var.set("Logging in to LinkedIn...")
            
            # Login to LinkedIn
            self.driver = self.login_to_linkedin(self.email_var.get(), self.password_var.get())
            
            # Search for the person
            self.status_var.set(f"Searching for {self.person_var.get()}...")
            self.search_for_person(self.driver, self.person_var.get())
            
            # Click connect button
            self.status_var.set("Clicking connect button...")
            self.click_connect_button(self.driver)
            
            # Click add note button
            self.status_var.set("Adding a note...")
            self.click_add_note_button(self.driver)
            
            # Type the note
            self.note_type(self.driver, self.person_var.get(), self.event_var.get())
            
            # Send the note
            self.status_var.set("Sending connection request...")
            self.send_note(self.driver)
            
            # Success
            self.status_var.set(f"Connection request sent successfully to {self.person_var.get()}!")
            
            # Show success message on main thread
            self.root.after(0, lambda: messagebox.showinfo("Success", f"Connection request sent successfully to {self.person_var.get()}!"))
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.status_var.set(error_msg)
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        
        finally:
            # Stop progress bar
            self.root.after(0, self.progress.stop)
    
    # Simulating human typing
    def human_like_typing(self, element, text):
        for char in text:
            # Add a random delay between keystrokes (between 0.05 and 0.25 seconds)
            time.sleep(random.uniform(0.05, 0.25))
            element.send_keys(char)
            
    # Simulating human mouse movement
    def human_like_cursor_movement(self, driver, element):
        action = ActionChains(driver)
        
        action.move_by_offset(
            random.randint(10, 50), 
            random.randint(10, 50)
        )
        
        # Add a slight jitter to the movement
        action.move_to_element_with_offset(
            element, 
            random.randint(-5, 5),  
            random.randint(-5, 5)   
        )
        action.pause(random.uniform(0.1, 0.3))  # Pause before clicking
        action.move_to_element(element)  # Finally move to the actual element
        action.perform()
    
    def login_to_linkedin(self, email, password):
        # Initialize driver
        driver = webdriver.Chrome()
        driver.get("https://www.linkedin.com/login")
        time.sleep(2)

        # Find username element
        username_field = driver.find_element(By.ID, "username")

        # Move to username field like a human
        self.human_like_cursor_movement(driver, username_field)
        username_field.click()

        # Type username with human-like behavior
        self.human_like_typing(username_field, email)

        # Pause before moving to password field (like a human would)
        time.sleep(random.uniform(0.5, 1.5))

        # Find password element
        password_field = driver.find_element(By.ID, "password")

        # Move to password field like a human
        self.human_like_cursor_movement(driver, password_field)
        password_field.click()

        # Type password with human-like behavior
        self.human_like_typing(password_field, password)

        # Pause before clicking submit (as if reviewing entries)
        time.sleep(random.uniform(0.8, 2))

        # Find and click submit button
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        self.human_like_cursor_movement(driver, submit_button)
        submit_button.click()

        # Wait for login to complete
        time.sleep(5)
        
        return driver

    # Method to search for a person
    def search_for_person(self, driver, person_name):
        try:
            # Wait for the page to load completely after login
            time.sleep(2)
            
            # Find and click on the search bar
            search_bar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[contains(@class, 'search-global-typeahead__input')]"))
            )
            search_bar.click()
            
            # Clear any existing text
            search_bar.clear()
            
            # Type the name with human-like behavior
            self.human_like_typing(search_bar, person_name)
            
            # Wait a moment before pressing Enter
            time.sleep(random.uniform(0.5, 1.5))
            
            # Press Enter to submit the search
            search_bar.send_keys(Keys.RETURN)
            
            # Wait for search results to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'search-results')]"))
            )
            
            print(f"Successfully searched for '{person_name}'")

            # Wait a moment before looking for the button
            time.sleep(2)
            
            # Find and click the specific button with multiple classes
            try:
                people_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[text()='People']"))
                )
                print("Found the filter button, clicking it now...")
                people_button.click()
                time.sleep(1.5)  # Wait for any dropdown or action to complete
                print("Successfully clicked the filter button")
            except Exception as e:
                print(f"Error clicking the filter button: {e}")
            
        except Exception as e:
            print(f"Error during search: {e}")
            raise

    # Clicking the Connect Button
    def click_connect_button(self, driver):
        try:
            # Wait for a moment to ensure the page is fully loaded
            time.sleep(random.uniform(2, 3))
            
            connect_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'artdeco-button') and .//span[text()='Connect']]"))
                    )
            print("Found the Connect button, clicking it now...")
            connect_button.click()
                
            # Add a small delay before clicking
            time.sleep(random.uniform(0.5, 1.5))
            
        except Exception as e:
            print(f"Error clicking the Connect button: {e}")
            raise

    # Clicking add a note button
    def click_add_note_button(self, driver):
        try:
            # Wait a moment for the dialog to fully render
            time.sleep(random.uniform(1, 2))

            # Clicking
            add_note_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Add a note']"))
                )
            
            # Add a small delay before clicking (human-like behavior)
            time.sleep(random.uniform(0.5, 1.2))
            
            # Click the button
            print("Found the 'Add a note' button, clicking it now...")
            add_note_button.click()
            
        except Exception as e:
            print(f"Error clicking 'Add a note' button: {e}")
            raise

    # Generate connection note
    def generate_connection_note(self, person_name, event_name):
        # Extract first name if full name is provided
        first_name = person_name.split()[0] if person_name else "there"
        
        # Create note
        note = f"Hi {first_name}, it was great meeting you at {event_name}! I enjoyed our conversation and would love to stay connected."
        
        return note

    # Typing the note
    def note_type(self, driver, person_name, event_name):
        try:
            # Wait for the textarea to appear - using the correct ID
            textarea = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "custom-message"))
            )
            
            # Alternative selectors if the above fails
            if not textarea:
                try:
                    textarea = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.NAME, "message"))
                    )
                except:
                    try:
                        textarea = WebDriverWait(driver, 3).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.connect-button-send-invite__custom-message"))
                        )
                    except:
                        print("Could not find the textarea for typing note")
                        raise Exception("Could not find the textarea for typing note")
                
            # Generate the connection note
            note_text = self.generate_connection_note(person_name, event_name)
            
            # Clear any default text in the textarea
            textarea.clear()
            
            # Add a short pause before typing (as a human would)
            time.sleep(random.uniform(0.8, 1.5))
            
            # Type the note with human-like behavior
            print(f"Typing personalized note: '{note_text}'")
            self.human_like_typing(textarea, note_text)
            
            # Pause after typing (as a human would before clicking Send)
            time.sleep(random.uniform(1, 2))
        
        except Exception as e:
            print(f"Error typing note: {e}")
            raise

    # Sending the invitation
    def send_note(self, driver):
        try:
            # Small pause before clicking (human-like behavior)
            time.sleep(random.uniform(0.8, 1.5))
            
            send_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Send invitation']"))
                    )
                
            # Click the button
            print("Found the 'Send invitation' button, clicking it now...")
            send_button.click()
            
            # Wait a moment to confirm the action completed
            time.sleep(2)
            
            return True
            
        except Exception as e:
            print(f"Error clicking 'Send invitation' button: {e}")
            raise

if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    app = LinkedInBotApp(root)
    
    # Run the application
    root.mainloop()