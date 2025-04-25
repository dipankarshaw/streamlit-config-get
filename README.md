# Streamlit & Netmiko Interaction

This project is a Python application that uses the `netmiko` library to connect to Cisco routers (both IOS-XR and IOS-XE) and execute commands. The application provides a Streamlit web interface for users to interact with the routers and also includes Azure chatbot functionalities.

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
    - `netmiko` is used to connect to Cisco routers and execute commands.
    - `azure.ai.inference` is used to interact with Azure chatbots.

2. **Functions**:
    - `connect_router(site_name, username, password, command, cisco_device_type)`: Connects to a router (IOS-XR or IOS-XE) and executes a command. Returns the output or an error message.
    - `configure_router(site_name, username, password, command, cisco_device_type)`: Connects to a router, enters enable mode, sends configuration commands, commits the changes, and returns the output or an error message.

3. **Streamlit App**:
    - The app has six main pages:
        - **Fetch Outputs ios-xr**:
            - Users can input the site name or IP address, username, password, and select or type a command to execute.
            - The app connects to the IOS-XR router and displays the output of the command.
        - **Configure Router ios-xr**:
            - Users can input the site name or IP address, username, password, and configuration commands.
            - The app connects to the IOS-XR router, sends the configuration commands, commits the changes, and displays the output.
        - **Fetch Outputs ios-xe**:
            - Similar to the IOS-XR fetch page but for IOS-XE routers.
        - **Configure Router ios-xe**:
            - Similar to the IOS-XR configure page but for IOS-XE routers.
        - **Talk-to-Deepseek**:
            - Users can interact with the Azure Deepseek chatbot by providing an endpoint, key, and their question.
            - The app sends the question to the chatbot and displays the response.
        - **Talk-to-Microsoft-phi4**:
            - Users can interact with the Azure Microsoft phi-4 chatbot by providing an endpoint, key, and their question.
            - The app sends the question to the chatbot and displays the response.

### Default Values

The application uses the following default values for user inputs:

- **IOS-XR**:
    - **Site Name or IP Address**: `sandbox-iosxr-1.cisco.com`
    - **Username**: `admin`
    - **Password**: `C1sco12345`
    - **Command Options**: 
        - `show ip interface brief`
        - `show version`
        - `show running-config`
- **IOS-XE**:
    - **Site Name or IP Address**: `devnetsandboxiosxe.cisco.com`
    - **Username**: `admin`
    - **Password**: `C1sco12345`
    - **Command Options**: 
        - `show ip interface brief`
        - `show version`
        - `show running-config`

These default values are set to provide a quick start for users to test the application with known Cisco sandbox environments.

### Snapshot
Here is the Main Page, which is for fetching Outputs:

![image](https://github.com/dipankarshaw/streamlit-config-get/assets/61518346/ab6f68d7-4ca5-4bdf-9089-c2d5d144ac3a)