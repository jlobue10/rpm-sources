%global libliftoff_minver 0.4.1

# latest git
%define commit 033872dcb694e8be6c01826dc37764dd6b95a26c

# release
#%%define commit d0d23c4c3010c81add1bd90cbe478ce4a386e28d

# refactor
#%%define commit aad7eed33bd2186f10ffc39213d6091a9764e65a

# working color
#%%define commit 8f3f5c5b445a42409ed387442ad80fec8c5153d9

%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global _default_patch_fuzz 2
%global build_timestamp %(date +"%Y%m%d")

%global rel_build 15.git.%{build_timestamp}.%{shortcommit}%{?dist}

Name:           gamescope
Version:        3.14.2
Release:        %{rel_build}
Summary:        Micro-compositor for video games on Wayland

License:        BSD
URL:            https://github.com/ValveSoftware/gamescope

# Create stb.pc to satisfy dependency('stb')
Source0:        stb.pc

BuildRequires:  meson >= 0.54.0
BuildRequires:  ninja-build
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  glm-devel
BuildRequires:  google-benchmark-devel
BuildRequires:  libXmu-devel
BuildRequires:  libXcursor-devel
BuildRequires:  pkgconfig(libdisplay-info)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(xres)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.17
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libavif)
BuildRequires:  (pkgconfig(wlroots) >= 0.18.0 with pkgconfig(wlroots) < 0.19.0)
BuildRequires:  (pkgconfig(libliftoff) >= 0.4.1 with pkgconfig(libliftoff) < 0.5)
BuildRequires:  pkgconfig(libcap)
BuildRequires:  pkgconfig(hwdata)
BuildRequires:  spirv-headers-devel
# Enforce the the minimum EVR to contain fixes for all of:
# CVE-2021-28021 CVE-2021-42715 CVE-2021-42716 CVE-2022-28041 CVE-2023-43898
# CVE-2023-45661 CVE-2023-45662 CVE-2023-45663 CVE-2023-45664 CVE-2023-45666
# CVE-2023-45667
BuildRequires:  stb_image-devel >= 2.28^20231011gitbeebb24-12
# Header-only library: -static is for tracking per guidelines
BuildRequires:  stb_image-static
BuildRequires:  stb_image_resize-devel
BuildRequires:  stb_image_resize-static
BuildRequires:  stb_image_write-devel
BuildRequires:  stb_image_write-static
BuildRequires:  /usr/bin/glslangValidator
BuildRequires:  libdecor-devel
BuildRequires:  libXdamage-devel
BuildRequires:  xorg-x11-server-Xwayland-devel
BuildRequires:  git

# libliftoff hasn't bumped soname, but API/ABI has changed for 0.2.0 release
Requires:       libliftoff%{?_isa} >= %{libliftoff_minver}
Requires:       xorg-x11-server-Xwayland
Recommends:     mesa-dri-drivers
Recommends:     mesa-vulkan-drivers

%description
%{name} is the micro-compositor optimized for running video games on Wayland.

%prep
git clone --single-branch --branch master https://github.com/ValveSoftware/gamescope
cd gamescope
git checkout %{commit}
git submodule update --init --recursive
mkdir -p pkgconfig
cp %{SOURCE0} pkgconfig/stb.pc

# Replace spirv-headers include with the system directory
sed -i 's^../thirdparty/SPIRV-Headers/include/spirv/^/usr/include/spirv/^' src/meson.build

%autopatch -p1

%build
cd gamescope
export PKG_CONFIG_PATH=pkgconfig
%meson -Dpipewire=enabled -Ddrm_backend=enabled -Drt_cap=enabled -Davif_screenshots=enabled -Dsdl2_backend=enabled -Dforce_fallback_for=vkroots
%meson_build

%install
cd gamescope
%meson_install --skip-subprojects

%files
%license gamescope/LICENSE
%doc gamescope/README.md
%{_bindir}/gamescope
%{_libdir}/libVkLayer_FROG_gamescope_wsi_*.so
%{_datadir}/vulkan/implicit_layer.d/VkLayer_FROG_gamescope_wsi.*.json


%changelog
