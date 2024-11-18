# LinkedIn Post Generator Using ChatGroq and Excel

This project automates the generation of LinkedIn posts based on ideas provided in an Excel file. Using a simple script, it fetches an idea from an Excel sheet, uses the `ChatGroq` model to generate a professional LinkedIn post, and then posts it on LinkedIn using the LinkedIn API. Once a post is successfully created, the script updates the Excel file to mark the idea as "posted."

## Project Workflow

1. **Input Idea in Excel:**
   - You provide short LinkedIn post ideas in an Excel file (`topic.xlsx`). Each row contains an idea in the "topic" column, and the "status" column is used to track if the idea has already been posted.
2. **Generate LinkedIn Post:**
   - The script reads the first idea from the Excel file that has not yet been posted (`NaN` status), sends the idea to the `ChatGroq` language model for enrichment, and generates a well-written LinkedIn post.
3. **Post to LinkedIn:**
   - Once the LinkedIn post is generated, the script automatically publishes the post on your LinkedIn profile using LinkedIn's API.
4. **Update Excel File:**
   - After a post is successfully published, the script updates the status of the corresponding row in the Excel file to "posted" to avoid duplicate posts in the future.

## Requirements

Before you begin, ensure you have the following:

- Python 3.7 or later
- An API key for accessing the [Groq API](https://groq.com/) for using the `ChatGroq` model.
- A LinkedIn account with access to LinkedIn's API and an API key (`linkedin_API_KEY`).
- The following Python libraries:
  - `langchain_groq`
  - `pandas`
  - `requests`
  - `python-dotenv`

## Setup

### 1. Clone the Repository

Start by cloning the repository to your local machine:

### 2. Install Dependencies

Install the required Python dependencies:

```bash
pip install langchain_groq pandas requests python-dotenv
```

### 3. Configure Environment Variables

To access the Groq API and LinkedIn API, you need to set up your environment variables. Create a `.env` file in the root directory of the project and add the following:

```bash
GROQ_API_KEY=your_groq_api_key_here
linkedin_API_KEY=your_linkedin_api_key_here
```

Replace `your_groq_api_key_here` and `your_linkedin_api_key_here` with the actual API keys.

### 4. Excel File Setup

Create an Excel file (`topic.xlsx`) in the same directory with the following columns:

- **topic**: Contains the idea for the LinkedIn post.
- **status**: Tracks the status of the post (e.g., `NaN` for ideas that haven't been posted yet).

Example:

| topic                                 | status |
| ------------------------------------- | ------ |
| "How to stay productive at work?"     | NaN    |
| "The importance of a morning routine" | NaN    |

### 5. Run the Script

Run the Python script to generate and post a LinkedIn update:

```bash
python llm_helper.py
```

This will read the first idea with a `NaN` status, generate a LinkedIn post using the `ChatGroq` model, and publish it to LinkedIn. After posting, the script will update the Excel file to reflect the status as "posted."

## Script Overview

The script is divided into the following key parts:

1. **Loading Environment Variables:**

   - The `.env` file is loaded using the `python-dotenv` library to securely access the API keys for both Groq and LinkedIn.

2. **Reading Excel File:**

   - The `pandas` library is used to read the Excel file (`topic.xlsx`), filter out rows that have already been posted, and fetch the first idea to be processed.

3. **Generate LinkedIn Post:**

   - The `ChatGroq` model (from the `langchain_groq` library) is invoked with the idea extracted from the Excel file. The model enriches the idea into a complete and well-written LinkedIn post.

4. **Post to LinkedIn:**

   - The LinkedIn API is used to create the post with the generated content. The post is made public and appears on your LinkedIn feed.

5. **Update Excel File:**
   - After successfully posting, the script updates the status of the respective idea in the Excel file to "posted."

### Example of Generated LinkedIn Post:

```bash
How to stay productive at work?

Staying productive at work is all about maintaining focus and using your time efficiently. Here are a few tips:
1. Break your work into smaller tasks.
2. Prioritize important tasks.
3. Take short breaks to refresh your mind.

By following these strategies, you’ll be able to stay on track and accomplish your goals more effectively!
```

### Example of Excel After Posting:

| topic                                 | status |
| ------------------------------------- | ------ |
| "How to stay productive at work?"     | posted |
| "The importance of a morning routine" | NaN    |

## Customization

- **Change Prompt Text:** You can modify the prompt or idea provided in the Excel file. Simply add or update the entries in the "topic" column.
- **LinkedIn Post Settings:** You can adjust the visibility, media types, or other LinkedIn post properties by modifying the API request parameters in the script.
