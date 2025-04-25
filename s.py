# pylint: disable=line-too-long
# pylint: disable=broad-exception-caught
# pylint: disable=import-error
"""
This module provides a Streamlit application for interacting with Cisco routers and Azure chatbots.
"""

import streamlit as st
from netmiko import ConnectHandler
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential



def connect_router(site_name, username, password, command,cisco_device_type):
    """
    Connect to a Cisco router and execute a series of commands.

    Args:
        site_name (str): The IP address or hostname of the router.
        username (str): The username for authentication.
        password (str): The password for authentication.
        command (str): A string containing one or more commands separated by newlines.

    Returns:
        str: The output from the executed commands or an error message if the connection fails.

    Raises:
        Exception: If there is an issue with the connection or command execution.
    """
    # Create a dictionary with the device details
    device = {
        'device_type': cisco_device_type,
        'ip': site_name,
        'username': username,
        'password': password,
    }

    try:
        # Connect to the router
        net_connect = ConnectHandler(**device)

        # Send the command
        commands = [cmd.strip() for cmd in command.replace('\n', ',').split(',')]
        output = ""
        for cmd in commands:
            output += f"*****{cmd} ********\n"
            output += net_connect.send_command(cmd) + "\n"

        # Close the connection
        net_connect.disconnect()

        return output
    except Exception as e:
        return str(e)
def configure_router(site_name, username, password, command,cisco_device_type):
    """
    Configure a Cisco router using provided credentials and commands.

    Args:
        site_name (str): The IP address or hostname of the router.
        username (str): The username for authentication.
        password (str): The password for authentication.
        command (str): The configuration command(s) to be sent to the router, separated by newlines.

    Returns:
        str: The output from the router after sending the configuration commands 
             and committing the changes.
             If an exception occurs, returns the exception message as a string.

    Raises:
        Exception: If there is an error during the connection or configuration process.
    """
    # Create a dictionary with the device details
    device = {
        'device_type': cisco_device_type,
        'ip': site_name,
        'username': username,
        'password': password,
    }
    try:
        # Connect to the router
        net_connect = ConnectHandler(**device)
        # Go into enable mode
        net_connect.enable()
        # Send the command(s)
        output = net_connect.send_config_set(command.split('\n'))
        # Commit the configuration changes
        if cisco_device_type == "cisco_xe":
            output += net_connect.save_config()
        elif cisco_device_type == "cisco_xr":
            output += net_connect.commit()
        # Close the connection
        net_connect.disconnect()
        return output
    except Exception as e:
        return str(e)

# Streamlit app
def main():
    """
    Main function to render the Streamlit app with multiple pages.

    Pages:
    - Fetch Outputs: Allows users to fetch outputs from a router by providing site name, username, password, and command.
    - Configure Router: Allows users to configure a router by providing site name, username, password, and configuration commands.
    - Talk-to-Deepseek: Allows users to interact with the Azure Deepseek Chatbot by providing an endpoint, key, and user input.
    - Talk-to-Microsoft-phi4: Allows users to interact with the Azure Microsoft phi-4 Chatbot by providing an endpoint, key, and user input.

    Each page has its own set of input fields and buttons to perform the respective actions.

    Note:
    - The 'Fetch Outputs' and 'Configure Router' pages require a function `connect_router` and `configure_router` respectively to handle the router connections.
    - The 'Talk-to-Deepseek' and 'Talk-to-Microsoft-phi4' pages require the `ChatCompletionsClient` and `AzureKeyCredential` classes from the Azure SDK to interact with the chatbots.
    """
    # Page title
    page = st.sidebar.selectbox("Page", [
        "Fetch Outputs ios-xr", 
        "Configure Router ios-xr",
        "Fetch Outputs ios-xe", 
        "Configure Router ios-xe",
        "Talk-to-Deepseek",
        "Talk-to-Microsoft-phi4"])
    if page == "Fetch Outputs ios-xr":
        st.title("Fetch Outputs ios-xr")
        # User input fields
        site_name = st.text_input("Site Name or IP Address", value="sandbox-iosxr-1.cisco.com")
        username = st.text_input("Username", value="admin")
        password = st.text_input("Password", type="password", value="C1sco12345")
        command_options = ["show ip interface brief", "show version", "show running-config"]
        command = st.selectbox("Show Command", command_options, index=0)
        custom_command = st.text_area("Or type your own command in Comma separated or line separated way")
        if custom_command:
            command = custom_command
        # Connect button
        if st.button("Get Output"):
            # Split the site names if comma-separated
            sites = [s.strip() for s in site_name.split(',')]
            # Iterate over the sites and connect to each router
            for site in sites:
                # Call the connect_router function
                output = connect_router(site, username, password, command,cisco_device_type="cisco_xr")
                # Display the output in a sub-page
                with st.expander(f"Output for {site}"):
                    st.code(output)
    elif page == "Configure Router ios-xr":
        st.title("Configure Router ios-xr")
        # User input fields for configuration
        site_name = st.text_input("Site Name or IP Address", value="sandbox-iosxr-1.cisco.com")
        username = st.text_input("Username", value="admin")
        password = st.text_input("Password", type="password", value="C1sco12345")
        config_commands = st.text_area("Configuration Commands")
        # Configure button
        if st.button("Configure"):
            # Split the site names if comma-separated
            sites = [s.strip() for s in site_name.split(',')]
            # Iterate over the sites and connect to each router
            for site in sites:
                # Call the connect_router function
                output = configure_router(site, username, password, config_commands,cisco_device_type="cisco_xr")
                # Display the output in a sub-page
                with st.expander(f"Output for {site}"):
                    st.code(output)
    elif page == "Fetch Outputs ios-xe":
        st.title("Fetch Outputs ios-xe")
        # User input fields
        site_name = st.text_input("Site Name or IP Address", value="devnetsandboxiosxe.cisco.com")
        username = st.text_input("Username", value="admin")
        password = st.text_input("Password", type="password", value="C1sco12345")
        command_options = ["show ip interface brief", "show version", "show running-config"]
        command = st.selectbox("Show Command", command_options, index=0)
        custom_command = st.text_area("Or type your own command in Comma separated or line separated way")
        if custom_command:
            command = custom_command
        # Connect button
        if st.button("Get Output"):
            # Split the site names if comma-separated
            sites = [s.strip() for s in site_name.split(',')]
            # Iterate over the sites and connect to each router
            for site in sites:
                # Call the connect_router function
                output = connect_router(site, username, password, command,cisco_device_type='cisco_xe')
                # Display the output in a sub-page
                with st.expander(f"Output for {site}"):
                    st.code(output)
    elif page == "Configure Router ios-xe":
        st.title("Configure Router ios-xe")
        # User input fields for configuration
        site_name = st.text_input("Site Name or IP Address", value="devnetsandboxiosxe.cisco.com")
        username = st.text_input("Username", value="admin")
        password = st.text_input("Password", type="password", value="C1sco12345")
        config_commands = st.text_area("Configuration Commands")
        # Configure button
        if st.button("Configure"):
            # Split the site names if comma-separated
            sites = [s.strip() for s in site_name.split(',')]
            # Iterate over the sites and connect to each router
            for site in sites:
                # Call the connect_router function
                output = configure_router(site, username, password, config_commands,cisco_device_type='cisco_xe')
                # Display the output in a sub-page
                with st.expander(f"Output for {site}"):
                    st.code(output)
    elif page == "Talk-to-Deepseek":
        st.title("Azure Deepseek Chatbot")
        model_name = "DeepSeek-R1"

        if "messages" not in st.session_state:
            st.session_state.messages = [SystemMessage(content="You are a helpful assistant.")]
        endpoint = st.text_input("endpoint", value="https://DeepSeek-R1-cbngc.eastus.models.ai.azure.com",)
        key = st.text_input("key",type="password",value="N5FfB3fNbJTnLWnS9audXJWuUe7hVF5w")
        user_input = st.text_area("Ask your question:")

        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key),
        )
        if st.button("Submit"):
            st.session_state.messages.append(UserMessage(content=user_input))
            response = client.complete(
                messages=st.session_state.messages,
                max_tokens=2048,
                model=model_name
            )
            answer = response.choices[0].message.content
            st.session_state.messages.append(SystemMessage(content=answer))
            st.write(answer)
    elif page == "Talk-to-Microsoft-phi4":
        st.title("Azure Microsoft phi-4 Chatbot")
        model_name = "Phi-4"
        if "messages" not in st.session_state:
            st.session_state.messages = [SystemMessage(content="You are a helpful assistant.")]
        endpoint = "https://Phi-4-jhzdm.eastus.models.ai.azure.com"

        endpoint = st.text_input("endpoint", value="https://Phi-4-jhzdm.eastus.models.ai.azure.com",)
        key = st.text_input("key",type="password",value="wYfWdT0xb640vPWS1kaxw8YSnaB2a2wS")
        user_input = st.text_area("Ask your question:")

        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential("wYfWdT0xb640vPWS1kaxw8YSnaB2a2wS"),
        )
        if st.button("Submit"):
            st.session_state.messages.append(UserMessage(content=user_input))
            response = client.complete(
                messages=st.session_state.messages,
                max_tokens=2048,
                temperature=0.8,
                top_p=0.1,
                presence_penalty=0.0,
                frequency_penalty=0.0,
                model=model_name
            )
            answer = response.choices[0].message.content
            st.session_state.messages.append(SystemMessage(content=answer))
            st.write(answer)

if __name__ == "__main__":
    main()
