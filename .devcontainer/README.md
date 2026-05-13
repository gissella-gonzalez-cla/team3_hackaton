# Python Dev Container

This repository includes a development container configuration for Python development. The dev container is based on an Ubuntu image and includes all necessary dependencies and tools to get started with Python development.

## Features

- Ubuntu-based development environment
- Python version management with pyenv
- Pre-installed Python 3.12.9
- Databricks CLI support
- UV tool installation
- Visual Studio Code extensions for Python, Databricks, YAML, Docker, Kubernetes, and more

## Getting Started

### Prerequisites

- Docker installed on your machine
- Visual Studio Code installed with extensions:
    - Visual Studio Code Remote - Containers
    - Remote Explorer
- LinuxVM Running and connected via SSH

### Setup

1. Clone this repository to your linuxVM.
2. Open the repository in Visual Studio Code.
3. When prompted, reopen the repository in the container.

### Configuration

The dev container is configured using the `.devcontainer/devcontainer.json` file. This file specifies the base image, environment variables, and post-create commands.

### Environment Variables

- `PYTHON_VERSION`: The version of Python to install (default: 3.12.9)
- `PYENV_ROOT`: The root directory for pyenv (default: `/home/vscode/.pyenv`)
- `UV_INSTALL_SCRIPT`: The URL for the UV installation script (default: `https://astral.sh/uv/install.sh`)
- `DATABRICKS_CLI_VERSION`: The version of the Databricks CLI to install (default: `main`)

### Mounts
- By default, this devcontainer is going to look at the source OS (e.g. your SSH tunnelled LinuxVM) and see if it can find:
    - ~/.ssh
    - ~/.databrickscfg
- It will try to bind these files so (1) git just works (ssh), and (2) if you've set a databricks profile via PAT or cli auth, it will pass that information through to the container from the host.
- For reference, see:
    - [Azure Linux setup for SSH](https://dev.azure.com/CLADevOps/Development/_git/onboarding?path=/user-guide/Environments/Development-VMs/2-Azure-Linux.md&version=GBmain&_a=preview&anchor=azure-devops-setup)
    - [Databricks configuration profiles](https://docs.databricks.com/aws/en/dev-tools/auth/config-profiles)

### Post-Create Command

The `postCreateCommand` in the `devcontainer.json` file runs the `.devcontainer/setup.sh` script, which installs Python, pyenv, UV, and the Databricks CLI.

## Usage

Once the dev container is set up, you can start developing your Python applications. The container includes the following tools and extensions:

- Python
- pyenv
- UV
- Databricks CLI
- Visual Studio Code extensions for Python, Databricks, YAML, Docker, Kubernetes, and more

### Running Python Code

You can run Python code directly in the container using the integrated terminal in Visual Studio Code. The terminal is configured to use the installed Python version and pyenv.

### Installing Additional Packages

To install additional Python packages, you can use `pip` in the integrated terminal. For example:

```sh
pip install <package-name>
```

## Connecting to the Dev Container

If you need to reconnect to the dev container after closing Visual Studio Code, follow these steps:

- Open Visual Studio Code.
- Open the Command Palette (Ctrl+Shift+P).
- Select Remote-Containers: Reopen in Container.

## Rebuilding the Dev Container

If you need to rebuild the dev container (e.g., after making changes to the devcontainer.json file), follow these steps:

- Open Visual Studio Code.
- Open the Command Palette (Ctrl+Shift+P).
- Select Remote-Containers: Rebuild and Reopen in Container.

## Contributing

If you have any suggestions or improvements for this dev container, feel free to open an issue or submit a pull request.