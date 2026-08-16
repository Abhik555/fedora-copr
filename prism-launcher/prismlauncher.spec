%bcond_with toolchain_clang

%if %{with toolchain_clang}
%global toolchain clang
%else
%global toolchain gcc
%endif

# Set the Qt version
%global qt_version 6
%global min_qt_version 6.4

# Build platform identifier
%global build_platform Fedora
%if 0%{?rhel}
%global build_platform RedHat
%endif

Name:           prismlauncher
Version:        11.0.3
Release:        %autorelease
Summary:        Custom Minecraft Launcher to easily manage multiple installations at once

# SPDX identifiers from upstream source tree
License:        GPL-3.0-only AND Apache-2.0 AND LGPL-3.0-only AND LGPL-2.1-only AND OFL-1.1 AND MIT
URL:            https://prismlauncher.org/
Source0:        https://github.com/PrismLauncher/PrismLauncher/releases/download/%{version}/PrismLauncher-%{version}.tar.gz

ExclusiveArch:  x86_64 aarch64

# Compiler & Toolchain
%if "%{toolchain}" == "gcc"
BuildRequires:  gcc-c++
%endif
%if "%{toolchain}" == "clang"
BuildRequires:  clang
BuildRequires:  lld
%endif

# Java Build Requirements
BuildRequires:  java-devel >= 17
BuildRequires:  javapackages-tools

# Build System & Utilities
BuildRequires:  cmake >= 3.22
BuildRequires:  ninja-build
BuildRequires:  extra-cmake-modules
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  scdoc

# System Libraries & Dependencies
BuildRequires:  pkgconfig(gamemode)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libcmark)
BuildRequires:  pkgconfig(libqrencode)
BuildRequires:  pkgconfig(tomlplusplus)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  ghc-filesystem-devel
BuildRequires:  quazip-qt6-devel

# Qt6 Modules
BuildRequires:  cmake(Qt6Concurrent) >= %{min_qt_version}
BuildRequires:  cmake(Qt6Core) >= %{min_qt_version}
BuildRequires:  cmake(Qt6CoreTools) >= %{min_qt_version}
BuildRequires:  cmake(Qt6Network) >= %{min_qt_version}
BuildRequires:  cmake(Qt6NetworkAuth) >= %{min_qt_version}
BuildRequires:  cmake(Qt6OpenGL) >= %{min_qt_version}
BuildRequires:  cmake(Qt6Test) >= %{min_qt_version}
BuildRequires:  cmake(Qt6Widgets) >= %{min_qt_version}
BuildRequires:  cmake(Qt6Xml) >= %{min_qt_version}
BuildRequires:  cmake(Qt6Svg) >= %{min_qt_version}
BuildRequires:  cmake(Qt65Compat) >= %{min_qt_version}

# Core Runtime Dependencies
Requires:       qt6-qtimageformats%{?_isa}
Requires:       qt6-qtsvg%{?_isa}
Requires:       javapackages-filesystem
Requires:       pciutils
Requires:       libglvnd-glx%{?_isa}

# Runtime Java Support for Minecraft Versions
Recommends:     java-21-openjdk
Recommends:     java-17-openjdk
Suggests:       java-latest-openjdk
Suggests:       java-1.8.0-openjdk

# Game Enhancements & Extras
Recommends:     gamemode%{?_isa}
Recommends:     mesa-dri-drivers%{?_isa}
Recommends:     xrandr
Recommends:     flite

%description
Prism Launcher is a custom launcher for Minecraft that allows you to easily
manage multiple installations of Minecraft at once (a fork of MultiMC).
It provides mod, modpack, and instance management alongside runtime Java
isolation.

%prep
%autosetup -n PrismLauncher-%{version} -p1

# Fix: OpenJDK 21+ compiler drops support for bytecode target < 8.
# Upstream Java launcher stubs targeting 6 or 7 must be updated to 8.
find . -name "CMakeLists.txt" -exec sed -i 's/-target [67] -source [67]/-target 8 -source 8/g' {} +

%build
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    %if "%{toolchain}" == "clang"
    -DCMAKE_LINKER_TYPE=LLD \
    %endif
    -DLauncher_QT_VERSION_MAJOR=%{qt_version} \
    -DLauncher_BUILD_PLATFORM="%{build_platform}" \
    -DLauncher_ENABLE_JAVA_DOWNLOADER=ON \
    -DENABLE_LTO=ON \
    -DBUILD_TESTING=OFF

%cmake_build

%install
%cmake_install

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/org.prismlauncher.PrismLauncher.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/org.prismlauncher.PrismLauncher.metainfo.xml

%files
%license LICENSE COPYING.md
%doc README.md
%{_bindir}/prismlauncher
%{_datadir}/applications/org.prismlauncher.PrismLauncher.desktop
%{_datadir}/icons/hicolor/*/apps/org.prismlauncher.PrismLauncher.*
%{_datadir}/mime/packages/org.prismlauncher.PrismLauncher.xml
%{_datadir}/qlogging-categories6/prismlauncher.categories
%{_metainfodir}/org.prismlauncher.PrismLauncher.metainfo.xml
%{_mandir}/man1/prismlauncher.1*

%changelog
%autochangelog
