import os
import requests
import json
import sys

url = "https://dashboard.ribbitnetwork.org/"
download_url = "https://dashboard.ribbitnetwork.org/_dash-update-component"

sensor_id = "643e2fc3f272169b4557ee8e_golioth_esp32s3"
get_data_payload = {"output":"sensor-data.data","outputs":{"id":"sensor-data","property":"data"},"inputs":[{"id":"selected-sensor","property":"data","value":sensor_id},{"id":"timezone","property":"children","value":"America/New_York"},{"id":"duration","property":"value","value":"30d"},{"id":"frequency","property":"value","value":"1h"}],"changedPropIds":["selected-sensor.data"]}

# Set up a session to maintain the cookies across requests
session = requests.Session()

# Visit the main website to set up the session cookies
session.get(url)


# GET FROG DATA RIBBIT
print("Getting frog data...")
get_data = session.post(download_url, json=get_data_payload)
if get_data.status_code == 200:
    resp = json.loads(get_data.text)
    frogs = resp["response"]["sensor-data"]["data"]


else:
    print("Could not fetch data from frogs. Bad status code: " + str(get_data.status_code))
    sys.exit()

print(f"Successfully found {str(len(frogs))} frogs")
payload = {"output":"download.data","outputs":{"id":"download","property":"data"},"inputs":[{"id":"export","property":"n_clicks","value":2}],"changedPropIds":["export.n_clicks"],"state":[{"id":"sensor-data","property":"data","value":frogs}]}

    # Make a POST request to download the CSV file
response = session.post(download_url, json=payload)
print("RESPONSE CODE FOR FIRST FROG: " + str(response.status_code))
    #print(response.status_code, response.text)
    # Check if the request was successful
if response.status_code == 200:
    resp = json.loads(response.text)
        # Get the content disposition header to extract the filename
    filename = f"data2.csv"
        # Specify the directory to save the file
    save_directory = "/Users/paraggupta/Desktop/IDEA R project/upload"
        
        # Create the directory if it doesn't exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
        
        # Check if a file with the same name already exists
    existing_file_path = os.path.join(save_directory, filename)
    if os.path.exists(existing_file_path):
        os.remove(existing_file_path)
        print(f"Existing file '{filename}' removed.")
        
        # Save the CSV file in the specified directory
    save_path = os.path.join(save_directory, filename)
    with open(save_path, "w+") as file:
        file.write(resp["response"]["download"]["data"]["content"])
            
    print(f"CSV file '{filename}' downloaded successfully and saved at '{save_path}'.")
else:
    print("Failed to download the CSV file.")
    print(response.text)
