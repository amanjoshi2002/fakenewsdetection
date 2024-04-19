
# import google.generativeai as genai

#  os.environ['YOUR_API_KEY'] = "AIzaSyCCgV_4zM-zQQfui-vs8QNZ8LKyVVD5k4Y"

# # Configure Germi AI
# genai.configure(api_key=os.environ['YOUR_API_KEY'])
# model = genai.GenerativeModel('gemini-pro')
# @app.route('/generate')
# def generate_summary():

#     # Retrieve user input from query parameters
#     userinput = request.args.get('userinput', '')

#     # Static prompt to ask for user's view
#     prompt = "Please state your view (1 for yes, 0 for no):"

#     # Combine user input with the prompt
#     input_with_prompt = f"{userinput} {prompt}"

#     # Generate content using Germi AI
#     response = model.generate_content(input_with_prompt)

#     # Process the response to determine if it's a "yes" or "no" answer
#     generated_text = response.text.lower().strip()
#     if "1" in generated_text or "yes" in generated_text:
#         output = "1"  # Yes
#     elif "0" in generated_text or "no" in generated_text:
#         output = "0"  # No
#     else:
#         output = "Unknown"  # Unable to determine

#     # Return the generated content
#     return jsonify({'user_input': userinput, 'output': output})