import pandas as pd
from LLM_helper import llm
from langchain_core.prompts import PromptTemplate
import json
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Function to return the LinkedIn post based on the first topic
def return_post():
    # Read the Excel file
    df = pd.read_excel("./topic.xlsx")
    
    # Filter out rows with NaN 'status'
    df = df[df["status"].isna()]
    
    # Get the first topic from the dataframe (assuming the first row is what we need)
    if not df.empty:
        text = df.iloc[0]["topic"]
        enriched_post = write_post(text)
        return enriched_post, df.index[0]  # Return the post and its index
    else:
        return None, None

# Function to generate the LinkedIn post and tags
def write_post(post):
    # Define the prompt template for LinkedIn post generation
    template = '''
    You are given a short LinkedIn post idea. Your task is to:
    1. Return a valid text. No preamble.
    2. Generate a well-written, complete LinkedIn post based on the idea.
    3. Just return a text without anything extra.
    
    Here is the idea for the LinkedIn post:  
    {post}
    '''

    # Create the prompt template and invoke the LLM
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"post": post}).content
    return response

# Function to update the status in the Excel file
def update_status(index):
    # Load the Excel file
    df = pd.read_excel("./topic.xlsx")
    
    # Update the status of the corresponding row
    df.loc[index, "status"] = "posted"
    
    # Save the updated DataFrame back to the file
    df.to_excel("./topic.xlsx", index=False)

# Main execution
if __name__ == "__main__":
    # Get the generated LinkedIn post and its index
    result, row_index = return_post()
    
    if result:
        final_result = "Melika + AI Assistant:\n" + result

        # Your LinkedIn access token
        access_token = os.getenv("linkedin_API_KEY")
        
        # LinkedIn API URL for creating a post
        url = "https://api.linkedin.com/v2/ugcPosts"

        # Set the headers, including the access token
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        # Create the post content
        post_content = {
            "author": "urn:li:person:3LU-AXhw2I",  # Replace with your LinkedIn URN
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": final_result 
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        # Send the request to create the post
        response = requests.post(url, headers=headers, data=json.dumps(post_content))

        # Check the response
        if response.status_code == 201:
            print("Post created successfully!")
            print("Response:", response.json())

            # Update the Excel file to mark the post as "posted"
            update_status(row_index)
        else:
            print(f"Failed to create post. Status code: {response.status_code}")
            print("Error:", response.text)
