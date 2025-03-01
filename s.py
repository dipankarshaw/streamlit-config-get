import streamlit as st
from netmiko import ConnectHandler

def connect_router(site_name, username, password, command):
    # Create a dictionary with the device details
    device = {
        'device_type': 'cisco_xr',
        'ip': site_name,
        'username': username,
        'password': password,
    }

    try:
        # Connect to the router
        net_connect = ConnectHandler(**device)

        # Send the command
        output = net_connect.send_command(command)

        # Close the connection
        net_connect.disconnect()

        return output
    except Exception as e:
        return str(e)
def configure_router(site_name, username, password, command):
    # Create a dictionary with the device details
    device = {
        'device_type': 'cisco_xr',
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
        output += net_connect.commit()
        # Close the connection
        net_connect.disconnect()
        return output
    except Exception as e:
        return str(e)

# Streamlit app
def main():
    # Page title
    page = st.sidebar.selectbox("Page", ["Fetch Outputs", "Configure Router"])
    if page == "Fetch Outputs":
        st.title("Fetch Outputs")
        # User input fields
        site_name = st.text_input("Site Name or IP Address", value="sandbox-iosxr-1.cisco.com")
        username = st.text_input("Username", value="admin")
        password = st.text_input("Password", type="password", value="C1sco12345")
        command_options = ["show ip interface brief", "show version", "show running-config"]
        command = st.selectbox("Show Command", command_options, index=0)
        custom_command = st.text_input("Or type your own command")
        if custom_command:
            command = custom_command
        # Connect button
        if st.button("Get Output"):
            # Split the site names if comma-separated
            sites = [s.strip() for s in site_name.split(',')]
            # Iterate over the sites and connect to each router
            for site in sites:
                # Call the connect_router function
                output = connect_router(site, username, password, command)
                # Display the output in a sub-page
                with st.expander(f"Output for {site}"):
                    st.code(output)
    elif page == "Configure Router":
        st.title("Configure Router")
        # User input fields for configuration
        site_name = st.text_input("Site Name or IP Address")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        config_commands = st.text_area("Configuration Commands")
        # Configure button
        if st.button("Configure"):
            # Split the site names if comma-separated
            sites = [s.strip() for s in site_name.split(',')]
            # Iterate over the sites and connect to each router
            for site in sites:
                # Call the connect_router function
                output = configure_router(site, username, password, config_commands)
                # Display the output in a sub-page
                with st.expander(f"Output for {site}"):
                    st.code(output)

if __name__ == "__main__":
    main()