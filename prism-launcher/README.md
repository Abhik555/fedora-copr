# prismlauncher-rpm

Unofficial RPM specfile for [Prism Launcher](https://prismlauncher.org).

## Installation

### 1. Install Prism Launcher

If you use Enterprise Linux, make sure you have the [EPEL repositories enabled](https://docs.fedoraproject.org/en-US/epel/getting-started/).

```bash
sudo dnf copr enable abhik555/personal-repository
sudo dnf install prismlauncher
```

### 2. Java Runtime Installation (JDK 17 on Fedora 42+)

To run Minecraft instances that require Java 17 on Fedora 42+, add the official Adoptium repository and install `temurin-17-jdk`:

```bash
# 1. Add the official Adoptium repository
sudo dnf install adoptium-temurin-java-repository

# 2. Install JDK 17 package
sudo dnf install temurin-17-jdk

# 3. Verify the installation
java -version
```

## Supported Distributions

- Fedora 40+
- RHEL 9+
