Name:           ab-download-manager
Version:        1.10.1
Release:        1%{?dist}
Summary:        Fast and modern download manager

License:        Apache-2.0
URL:            https://github.com/amir1376/ab-download-manager

ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils
BuildRequires:  curl
BuildRequires:  tar

%description
AB Download Manager is a fast and modern download manager for Linux.

%prep
rm -rf ABDownloadManager

mkdir -p ABDownloadManager

curl -L --fail --retry 5 \
    "https://github.com/amir1376/ab-download-manager/releases/download/v%{version}/ABDownloadManager_%{version}_linux_x64.tar.gz" \
    -o ABDownloadManager.tar.gz

tar -xzf ABDownloadManager.tar.gz \
    -C ABDownloadManager \
    --strip-components=1

rm -f ABDownloadManager.tar.gz

%build
# Upstream provides a prebuilt binary.
# Nothing needs to be compiled.

%install
rm -rf %{buildroot}

# Application
install -d %{buildroot}%{_libdir}/%{name}

cp -a ABDownloadManager/. \
    %{buildroot}%{_libdir}/%{name}/

# Executable
install -d %{buildroot}%{_bindir}

ln -s \
    %{_libdir}/%{name}/bin/ABDownloadManager \
    %{buildroot}%{_bindir}/ab-download-manager

# Desktop entry
install -d %{buildroot}%{_datadir}/applications

cat > %{buildroot}%{_datadir}/applications/ab-download-manager.desktop <<EOF
[Desktop Entry]
Name=AB Download Manager
Comment=Fast and modern download manager
Exec=ab-download-manager
Icon=ab-download-manager
Terminal=false
Type=Application
Categories=Network;FileTransfer;
StartupNotify=true
EOF

# Icon
install -d \
    %{buildroot}%{_datadir}/icons/hicolor/256x256/apps

install -m 0644 \
    %{buildroot}%{_libdir}/%{name}/lib/ABDownloadManager.png \
    %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/ab-download-manager.png

%check
test -x \
    %{buildroot}%{_libdir}/%{name}/bin/ABDownloadManager

test -f \
    %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/ab-download-manager.png

desktop-file-validate \
    %{buildroot}%{_datadir}/applications/ab-download-manager.desktop

%files
%{_bindir}/ab-download-manager
%{_libdir}/%{name}/
%{_datadir}/applications/ab-download-manager.desktop
%{_datadir}/icons/hicolor/256x256/apps/ab-download-manager.png

%changelog
* Sat Aug 15 2026 Abhik Ghosh <abhik@example.com> - 1.10.1-1
- Initial package
