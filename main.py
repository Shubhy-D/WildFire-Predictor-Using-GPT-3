# Import the OpenAI library
import openai

# Prompt the user to input the location for wildfire prediction
location_var = input("Enter the location of the wild fire prediction: ")

# Set the OpenAI API key
openai.api_key = "Your API_KEY(DO NOT SHARE)"

# Define a function to predict the likelihood of a wildfire based on input data
def predict_wildfire(flame_sensor_data, temperature, humidity, location):
    # Create a prompt string that includes the input data and the location
    prompt = f"Predict the percentage likelihood of a wildfire in the forested area near {location}, based on flame sensor data that shows a flame of {flame_sensor_data} a temperature of {temperature} degrees Celsius, and a humidity of {humidity} percent. Take into account recent wildfires in the area and the current weather conditions, including wind speed and direction. Provide an explanation for your prediction and give a one-word answer indicating whether the likelihood of a wildfire is high, medium, or low. Make sure to a percentage at the end of the likelihood of a wildfire."
    
    # Use the OpenAI Completion API to generate a text prediction based on the prompt
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=prompt,
      temperature=0.5,
      max_tokens=300,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    
    # Extract the text output from the API response
    text_output = response.choices[0].text.strip()
    percentage = None
    simple_text = "Unknown"
    
    # Iterate through the response choices to find the predicted likelihood of a wildfire
    for choice in response.choices:
        text = choice.text.strip()
        if "%" in text:
            percentage_str = ""
            
            # Extract the percentage value from the text
            for char in text:
                if char.isdigit() or char == ".":
                    percentage_str += char
                elif char == "%":
                    percentage = float(percentage_str)
                    
                    # Set the simple text prediction based on the percentage value
                    if percentage > 50:
                        simple_text = "High"
                    else:
                        simple_text = "Low"
                    break
            
            # Exit the loop once the percentage value has been found
            if percentage is not None:
                break
                
        # If the percentage value is not found in the text, try to extract it using another method
        elif "There is a" in text and "%" in text:
            percentage_str = text.split("There is a ")[-1].split("%")[0].strip()
            percentage = float(percentage_str)
            
            # Set the simple text prediction based on the percentage value
            if percentage > 50:
                simple_text = "High"
            else:
                simple_text = "Low"
            break
            
    # Return the percentage likelihood, simple text prediction, and full text prediction
    return percentage, simple_text, text_output

# Call the predict_wildfire function with sample input data and the user-input location
percentage, simple_text, text_output = predict_wildfire(0.75, 90, 50, location_var)

# If the percentage value is not None, print it out
if percentage is not None:
    print(f"Percentage likelihood: {percentage}%")

# Print out the simple text prediction and the full text prediction
print(f"Simple Text: {simple_text}")
print(f"AI Prediction: {text_output}")
