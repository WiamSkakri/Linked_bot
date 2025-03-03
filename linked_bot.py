from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import argparse

# Simulating human typing
def human_like_typing(element, text):
    for char in text:
        # Add a random delay between keystrokes (between 0.05 and 0.25 seconds)
        time.sleep(random.uniform(0.05, 0.25))
        element.send_keys(char)
        
# Simulating human mouse movement
def human_like_cursor_movement(driver, element):
   
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
   


def login_to_linkedin(email, password):
    # Initialize driver
    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)


    # Find username element
    username_field = driver.find_element(By.ID, "username")

    # Move to username field like a human
    human_like_cursor_movement(driver, username_field)
    username_field.click()

    # Type username with human-like behavior
    human_like_typing(username_field, email)

    # Pause before moving to password field (like a human would)
    time.sleep(random.uniform(0.5, 1.5))

    # Find password element
    password_field = driver.find_element(By.ID, "password")

    # Move to password field like a human
    human_like_cursor_movement(driver, password_field)
    password_field.click()

    # Type password with human-like behavior
    human_like_typing(password_field, password)

    # Pause before clicking submit (as if reviewing entries)
    time.sleep(random.uniform(0.8, 2))

    # Find and click submit button
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    human_like_cursor_movement(driver, submit_button)
    submit_button.click()

    # Wait for login to complete
    time.sleep(5)
    
    return driver

# Method to search for a person
def search_for_person(driver, person_name):
    try:
        # Wait for the page to load completely after login
        time.sleep(2)
        
        # Find and click on the search bar
        # search_bar = driver.find_element(By.XPATH, "//input[contains(@class, 'search-global-typeahead__input')]")
        search_bar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[contains(@class, 'search-global-typeahead__input')]"))
        )
        search_bar.click()
        
        # Clear any existing text
        search_bar.clear()
        
        # Type the name with human-like behavior
        human_like_typing(search_bar, person_name)
        
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


# Clicking the Connect Button
def click_connect_button(driver):
    
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
        return False
    
# Clicking add a note button
def click_add_note_button(driver):
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
        return False
    
# Writing a note 
def generate_connection_note(person_name, event_name):
    
    # Extract first name if full name is provided
    first_name = person_name.split()[0] if person_name else "there"
    
    # List of template messages with variations for natural sounding notes
    note =  f"Hi {first_name}, it was great meeting you at {event_name}! I enjoyed our conversation and would love to stay connected."

    return note


# Typing the note
def note_type(driver, person_name, event_name):
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
                return
        
    # Generate the connection note
    note_text = generate_connection_note(person_name, event_name)
    
    # Clear any default text in the textarea
    textarea.clear()
    
    # Add a short pause before typing (as a human would)
    time.sleep(random.uniform(0.8, 1.5))
    
    # Type the note with human-like behavior
    print(f"Typing personalized note: '{note_text}'")
    human_like_typing(textarea, note_text)
    
    # Pause after typing (as a human would before clicking Send)
    time.sleep(random.uniform(1, 2))


# Sending the invitation
def send_note(driver):
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
        
    except Exception as e:
        print(f"Error clicking 'Send invitation' button: {e}")
        return False



def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='LinkedIn Search Bot')
    parser.add_argument('--email', required=True, help='Your LinkedIn email')
    parser.add_argument('--password', required=True, help='Your LinkedIn password')
    parser.add_argument('--name', required=True, help='Name of person to search for')
    parser.add_argument ('--event', required=True, help="Name of the event")
    
    args = parser.parse_args()
    
    # Login to LinkedIn
    driver = login_to_linkedin(args.email, args.password)
    
    # Search for the person
    search_for_person(driver, args.name)

    # click on the connect button
    click_connect_button(driver)

    # Clicking the add a note button
    click_add_note_button(driver)

    # Typing the note
    note_type(driver, args.name, args.event )

    # Sending the note
    send_note(driver)
    
    # Keep the browser open for a while to see results
    time.sleep(10)
    
    # Uncomment the line below to close the browser automatically
    # driver.quit()

if __name__ == "__main__":
    main()
