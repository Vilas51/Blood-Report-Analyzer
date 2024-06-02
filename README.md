# Project Setup and Execution Guide

## Getting Started

### 1. Create a Virtual Environment

To begin, we will create a Conda environment. Open your terminal and run:
```sh
conda create -n wingify_assignment python=3.10 -y
```

### 2. Install Required Libraries
After creating the environment, activate it and install the necessary libraries by running:

```sh
pip install -r requirements.txt

```

### 3. Set Up Environment Variables
While the libraries are installing, we need to set up our environment variables.

Create a ```.env``` File
In the project directory, create a new file named ``.env`` Add your environment variables to this file in the following format:

```env
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
SERPER_API_KEY="YOUR_SERPER_API_KEY"
```

* Obtain API Keys
    - Google API Key: Obtain your API key from [Google API Key](https://aistudio.google.com/app/apikey).
    - Serper API Key: Obtain your API key from [Serper API Key](https://serper.dev/api-key).

### 4. Start the Project
Now that we have everything set up, let's start the project.

### Open the Folder
Open the folder named: ``blood test analyser``

### Running the Project
To run the project, follow these steps:

1. Open your terminal.
2. Navigate to the project directory.
3. Execute the following command:
```sh
streamlit run main.py
```

# You're All Set!
Congratulations! The project should now be up and running.
