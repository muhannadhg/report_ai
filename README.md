# report_ai

This Python code utilizes OpenAI's GPT-3 to generate security vulnerability reports. It takes user-provided information about a security vulnerability (such as the vulnerability's name, description, and target URL) and creates a structured security report that includes a title, rating, URL, description, proof of concept, impact, and recommendations.

The code also captures a screenshot of the target website and adds it to the PDF report. Several libraries are used to enhance the functionality and appearance of the report, including pyfiglet for generating a stylish title and reportlab for creating the PDF document.

Step-by-step installation and usage guide:

Install Python if it's not already installed on your computer. You can download it from the official website: https://www.python.org/downloads/

Install the pyfiglet library using the following command:

    pip install pyfiglet
Install the rich library using the following command:

    pip install rich
Install the reportlab library using the following command:

    pip install reportlab
Install the openai library using the following command:

    pip install openai
you have to get the API KEY from: https://platform.openai.com/account/api-keys

    
Download the Bulk-Bing-Image-downloader project from GitHub: https://github.com/ostrolucky/Bulk-Bing-Image-downloader/

Run the provided code and follow the on-screen instructions.

The program will create a security report and save it as a PDF file. It will also capture a screenshot of the target website and add it to the report. Make sure to execute the steps in order and install the necessary libraries to run the program successfully.
