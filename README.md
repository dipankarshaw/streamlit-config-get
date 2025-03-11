# Streamlit & netmiko interaction

This project is a Python application that uses the `netmiko` library to connect to a Cisco XR router and execute commands. The application provides a Streamlit web interface for users to interact with the router and also includes Azure chatbot functionalities.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.x
- Streamlit
- Netmiko
- Azure AI Inference

You can install the Python dependencies with pip:

```sh
pip install streamlit netmiko azure-ai-inference
```
or 
```sh
pip install -r requirements.txt
```

### Usage
To run the application, use the following command:

```sh
streamlit run s.py
```
or 
```sh
python3 -m streamlit run s.py
```

### Code Explanation

The `s.py` file contains the main code for the Streamlit application. Here is a brief overview of its functionality:

1. **Imports**:
    - `streamlit` is used to create the web interface.
    - `netmiko` is used to connect to the Cisco XR router and execute commands.
    - `azure.ai.inference` is used to interact with Azure chatbots.

2. **Functions**:
    - `connect_router(site_name, username, password, command)`: Connects to the router and executes a command. Returns the output or an error message.
    - `configure_router(site_name, username, password, command)`: Connects to the router, enters enable mode, sends configuration commands, commits the changes, and returns the output or an error message.

3. **Streamlit App**:
    - The app has four main pages: "Fetch Outputs", "Configure Router", "Talk-to-Deepseek", and "Talk-to-Microsoft-phi4".
    - **Fetch Outputs**:
        - Users can input the site name or IP address, username, password, and select or type a command to execute.
        - The app connects to the router and displays the output of the command.
    - **Configure Router**:
        - Users can input the site name or IP address, username, password, and configuration commands.
        - The app connects to the router, sends the configuration commands, commits the changes, and displays the output.
    - **Talk-to-Deepseek**:
        - Users can interact with the Azure Deepseek chatbot by providing an endpoint, key, and their question.
        - The app sends the question to the chatbot and displays the response.
    - **Talk-to-Microsoft-phi4**:
        - Users can interact with the Azure Microsoft phi-4 chatbot by providing an endpoint, key, and their question.
        - The app sends the question to the chatbot and displays the response.

### Default Values

The application uses the following default values for user inputs:

- **Site Name or IP Address**: `sandbox-iosxr-1.cisco.com`
- **Username**: `admin`
- **Password**: `C1sco12345`
- **Command Options**: 
  - `show ip interface brief`
  - `show version`
  - `show running-config`

These default values are set to provide a quick start for users to test the application with a known Cisco XR sandbox environment.

### Snapshot
Here is the Main Page, which is for fetching Outputs

![image](https://github.com/dipankarshaw/streamlit-config-get/assets/61518346/ab6f68d7-4ca5-4bdf-9089-c2d5d144ac3a)