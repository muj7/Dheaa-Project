Dheaa

Dheaa is an Arabic Quranic Tafsir (interpretation) tool that uses the first Arabic Large Language Model (LLM) developed by Sadaia called Allam. It leverages Allam’s comprehensive foundational knowledge and Retrieval-Augmented Generation (RAG) techniques, utilizing prominent and trusted sources of Quranic interpretation (tafsir).

Table of Contents

Overview
Features
Requirements
Installation
Usage
Configuration
Contributing
License
Overview
Dheaa provides detailed, accurate, and contextually relevant interpretations of Quranic verses in Arabic, with a focus on maintaining scholarly integrity and adherence to well-known tafsir sources. It is designed to help users understand the Quran by providing explanations that are easy to comprehend while remaining rooted in the classical tafsir texts.

Features
Dheaa’s functionality includes:

Contextual Interpretation: Provides explanations of Quranic verses based on their specific contexts, referencing statements of accredited tafsir scholars.
Historical Context: Links verses to their occasions of revelation (Asbab al-Nuzul) to clarify the context.
Linguistic and Rhetorical Analysis: Explains significant linguistic terms and rhetorical aspects within the verses to enhance understanding.
Jurisprudential Insights: Derives and presents Islamic legal rulings inferred from verses, when applicable.
Modern Language: Offers interpretations in a contemporary, accessible Arabic style.
Reliable Sources: Exclusively uses approved tafsir sources to ensure authenticity and reliability.
Avoidance of Controversy: Refrains from doctrinal disputes and avoids uncommon or unendorsed interpretations.
Source Attribution: Cites tafsir sources and scholarly opinions transparently.
Highlights Differences of Opinion: Alerts users to any areas of scholarly disagreement when relevant.
Each verse interpretation in Dheaa includes:

Full verse with its chapter and verse number.
General meaning.
Occasion of revelation (if any).
Key linguistic terms.
Rhetorical aspects.
Derived legal rulings.
Lessons and moral insights.
Requirements
To run Dheaa, ensure you have the following installed:

Python (3.8 or higher)
Flask for running the web app
HTML and CSS for the front-end
Python libraries:

Flask
Jinja2
Any additional libraries listed in requirements.txt
Installation
Clone the repository:
bash
Copy code
https://github.com/muj7/Dheaa-Project
Navigate to the project directory:
bash
Copy code
cd dheaa
Install required libraries:
bash
Copy code
pip install -r requirements.txt
Usage
Start the Flask Application:
bash
Copy code
python app.py
Open your web browser and navigate to http://127.0.0.1:5000 to access Dheaa on your local machine.
Enter the Quranic verse you want to interpret, and Dheaa will generate a comprehensive interpretation based on the structured tafsir method.
Configuration
If any configuration is required, update the config.py file with parameters such as:

Flask server settings
Local file paths for resources
Contributing
We welcome contributions from the community! If you’re interested in improving Dheaa, follow these steps:

Fork the repository.
Create a feature branch (git checkout -b feature/YourFeature).
Commit your changes (git commit -am 'Add YourFeature').
Push to the branch (git push origin feature/YourFeature).
Open a Pull Request.
