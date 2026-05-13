#!/bin/bash

set -e  # Exit on error

# Set the Python version
# PYTHON_VERSION="3.10.12" # Replace with the desired Python version
PYTHON_VERSION="3.12.3"

# Install minimal dependencies
sudo apt-get update && sudo apt-get install -y \
    build-essential curl git

# Install uv
echo "Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | bash


# Verify uv installation
if ! command -v uv &> /dev/null; then
    echo "uv installation failed" >&2
    exit 1
fi

# Install Python using uv
echo "Installing Python ${PYTHON_VERSION} with uv..."
uv python install "${PYTHON_VERSION}"


export UV_LINK_MODE=copy

# Set up shell environment for uv
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
echo 'export UV_LINK_MODE=copy' >> ~/.bashrc
echo "Setup complete!"

source ~/.bashrc


# install azure cli with extras:
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Install GitHub CLI
echo "Installing GitHub CLI..."
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh -y

# Verify GitHub CLI installation
if ! command -v gh &> /dev/null; then
    echo "GitHub CLI installation failed" >&2
    exit 1
fi
echo "GitHub CLI installed successfully: $(gh --version)"

# Install AzCopy for training data migration
echo "Installing AzCopy..."
cd /tmp
wget -q https://aka.ms/downloadazcopy-v10-linux -O azcopy.tar.gz
tar -xzf azcopy.tar.gz --strip-components=1
sudo mv azcopy /usr/local/bin/
sudo chmod +x /usr/local/bin/azcopy
rm -f azcopy.tar.gz
cd -

# Verify AzCopy installation
if ! command -v azcopy &> /dev/null; then
    echo "AzCopy installation failed" >&2
    exit 1
fi
echo "AzCopy installed successfully: $(azcopy --version)"

# Install Databricks CLI
DATABRICKS_CLI_VERSION="v0.214.0"
echo "Installing Databricks CLI..."
sudo rm -rf /usr/local/bin/databricks
if curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/$DATABRICKS_CLI_VERSION/install.sh | sudo bash; then
    echo "Databricks CLI installed successfully."
    echo "Running Databricks CLI version: $(databricks --version)"
else
    echo "Failed to install Databricks CLI." >&2
    exit 1
fi