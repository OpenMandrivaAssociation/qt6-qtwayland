#define beta rc
#define snapshot 20200627
%define major 6

%define _qtdir %{_libdir}/qt%{major}

Name:		qt6-qtwayland
Version:	6.10.1
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}1
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qtwayland.git
Source:		qtwayland-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		https://download.qt.io/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qtwayland-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Group:		System/Libraries
Summary:	Qt %{major} Wayland support library
BuildRequires:	qt6-cmake
BuildRequires:	ninja
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6Quick)
BuildRequires:	cmake(Qt6Qml)
BuildRequires:	cmake(Qt6QmlModels)
BuildRequires:	cmake(Qt6Svg)
BuildRequires:	cmake(Qt6SvgWidgets)
BuildRequires:	cmake(Qt6Xml)
BuildRequires:	cmake(Qt6OpenGL)
BuildRequires:	cmake(Qt6ShaderTools)
BuildRequires:	cmake(Qt6WaylandClientPrivate)
BuildRequires:	qt%{major}-cmake
BuildRequires:	pkgconfig(zlib)
BuildRequires:	cmake(OpenGL)
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(wayland-egl)
BuildRequires:	pkgconfig(wayland-scanner)
BuildRequires:	pkgconfig(wayland-kms)
License:	LGPLv3/GPLv3/GPLv2

%patchlist

%description
Qt %{major} Wayland library

%global extra_devel_files_WaylandEglCompositorHwIntegration \
%{_qtdir}/mkspecs/modules/qt_lib_wayland_egl_compositor_hw_integration_private.pri

%global extra_files_WaylandCompositor \
%dir %{_qtdir}/qml/QtWayland/Compositor \
%{_qtdir}/qml/QtWayland/Compositor/qmlfiles \
%{_qtdir}/qml/QtWayland/Compositor/IviApplication \
%{_qtdir}/qml/QtWayland/Compositor/PresentationTime \
%{_qtdir}/qml/QtWayland/Compositor/QtShell \
%{_qtdir}/qml/QtWayland/Compositor/TextureSharingExtension \
%{_qtdir}/qml/QtWayland/Compositor/WlShell \
%{_qtdir}/qml/QtWayland/Compositor/XdgShell \
%{_qtdir}/qml/QtWayland/Compositor/*.qmltypes \
%{_qtdir}/qml/QtWayland/Compositor/*.so \
%{_qtdir}/qml/QtWayland/Compositor/qmldir \
%dir %{_qtdir}/plugins/wayland-graphics-integration-server \
# FIXME is it worth splitting some of those plugins into their own package? \
# adwaita most definitely sucks... \
%{_qtdir}/plugins/wayland-graphics-integration-server/libqt-wayland-compositor-dmabuf-server-buffer.so \
%{_qtdir}/plugins/wayland-graphics-integration-server/libqt-wayland-compositor-drm-egl-server-buffer.so \
%{_qtdir}/plugins/wayland-graphics-integration-server/libqt-wayland-compositor-shm-emulation-server.so \
%{_qtdir}/plugins/wayland-graphics-integration-server/libqt-wayland-compositor-vulkan-server.so \
%{_qtdir}/plugins/wayland-graphics-integration-server/libqt-wayland-compositor-wayland-egl.so \
%{_qtdir}/plugins/wayland-graphics-integration-server/libqt-wayland-compositor-wayland-eglstream-controller.so \
%{_qtdir}/plugins/wayland-decoration-client/libadwaita.so \
%{_qtdir}/plugins/wayland-shell-integration/libivi-shell.so \
%{_qtdir}/plugins/wayland-shell-integration/libqt-shell.so \
%dir %{_qtdir}/qml/QtWayland \
%dir %{_qtdir}/qml/QtWayland/Client \
%dir %{_qtdir}/qml/QtWayland/Client/TextureSharing \
%{_qtdir}/qml/QtWayland/Client/TextureSharing/* \

%global extra_devel_files_WaylandCompositor \
%{_qtdir}/lib/cmake/Qt6Qml/QmlPlugins/Qt6WaylandCompositorIviapplication*.cmake \
%{_qtdir}/lib/cmake/Qt6Qml/QmlPlugins/Qt6WaylandCompositorPresentationTime*.cmake \
%{_qtdir}/lib/cmake/Qt6Qml/QmlPlugins/Qt6WaylandCompositorQtShell*.cmake \
%{_qtdir}/lib/cmake/Qt6Qml/QmlPlugins/Qt6WaylandCompositorWLShell*.cmake \
%{_qtdir}/lib/cmake/Qt6Qml/QmlPlugins/Qt6WaylandCompositorXdgShell*.cmake \
%{_qtdir}/lib/cmake/Qt6Qml/QmlPlugins/Qt6WaylandTextureSharing*.cmake \
%{_qtdir}/lib/cmake/Qt6Qml/QmlPlugins/Qt6qwaylandcompositorplugin*.cmake \
%{_qtdir}/lib/cmake/Qt6/FindWaylandkms.cmake \
%{_qtdir}/lib/cmake/Qt6BuildInternals/StandaloneTests/QtWaylandTestsConfig.cmake \
%{_qtdir}/lib/cmake/Qt6WaylandClient \
%{_qtdir}/lib/cmake/Qt6WaylandClientFeaturesPrivate \
%{_qtdir}/mkspecs/modules/qt_lib_waylandclientfeatures_private.pri \
%{_qtdir}/modules/WaylandClientFeaturesPrivate.json \
%{_qtdir}/sbom/qtwayland-%{version}.spdx

%qt6lib WaylandCompositor
%qt6lib WaylandEglCompositorHwIntegration
%qt6lib WaylandCompositorIviapplication
%qt6lib WaylandCompositorPresentationTime
%qt6lib WaylandCompositorWLShell
%qt6lib WaylandCompositorXdgShell

%prep
%autosetup -p1 -n qtwayland%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
# FIXME why are OpenGL lib paths autodetected incorrectly, preferring
# /usr/lib over /usr/lib64 even on 64-bit boxes?
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DBUILD_EXAMPLES:BOOL=ON \
	-DBUILD_SHARED_LIBS:BOOL=ON \
	-DFEATURE_cxx2a:BOOL=ON \
	-DFEATURE_dynamicgl:BOOL=ON \
	-DFEATURE_use_lld_linker:BOOL=ON \
	-DINPUT_sqlite=system \
	-DQT_WILL_INSTALL:BOOL=ON \
	-D_OPENGL_LIB_PATH=%{_libdir} \
	-DOPENGL_egl_LIBRARY=%{_libdir}/libEGL.so \
	-DOPENGL_glu_LIBRARY=%{_libdir}/libGLU.so \
	-DOPENGL_glx_LIBRARY=%{_libdir}/libGLX.so \
	-DOPENGL_opengl_LIBRARY=%{_libdir}/libOpenGL.so \
	-DQT_MKSPECS_DIR:FILEPATH=%{_qtdir}/mkspecs

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
%ninja_install -C build
%qt6_postinstall

%files
%{_qtdir}/examples/wayland
