#define beta rc
#define snapshot 20200627
%define major 6

%define _qtdir %{_libdir}/qt%{major}

Name:		qt6-qtwayland
Version:	6.2.1
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}1
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qtwayland.git
Source:		qtwayland-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		http://download.qt-project.org/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qtwayland-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Group:		System/Libraries
Summary:	Qt %{major} Wayland support library
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	%{_lib}Qt6Core-devel >= %{version}-0
BuildRequires:	%{_lib}Qt6DBus-devel >= %{version}-0
BuildRequires:	%{_lib}Qt6Gui-devel >= %{version}-0
BuildRequires:	%{_lib}Qt6Network-devel >= %{version}-0
BuildRequires:	%{_lib}Qt6Widgets-devel >= %{version}-0
BuildRequires:	%{_lib}Qt6Xml-devel >= %{version}-0
BuildRequires:	%{_lib}Qt6OpenGL-devel >= %{version}-0
BuildRequires:	qt6-qtdeclarative-devel >= %{version}-0
BuildRequires:	qt6-qtdeclarative >= %{version}-0
BuildRequires:	qt6-qtshadertools >= %{version}-0
BuildRequires:	qt%{major}-cmake
BuildRequires:	pkgconfig(zlib)
BuildRequires:	cmake(OpenGL)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(wayland-egl)
BuildRequires:	pkgconfig(wayland-scanner)
#BuildRequires:	pkgconfig(wayland-kms)
License:	LGPLv3/GPLv3/GPLv2

%description
Qt %{major} Wayland library

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
	-DOPENGL_opengl_LIBRARY=%{_libdir}/libOpenGL.so

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
%ninja_install -C build
# Put stuff where tools will find it
# We can't do the same for %{_includedir} right now because that would
# clash with qt5 (both would want to have /usr/include/QtCore and friends)
mkdir -p %{buildroot}%{_bindir} %{buildroot}%{_libdir}/cmake
for i in %{buildroot}%{_qtdir}/lib/*.so*; do
	ln -s qt%{major}/lib/$(basename ${i}) %{buildroot}%{_libdir}/
done
mv %{buildroot}%{_qtdir}/lib/cmake %{buildroot}%{_libdir}/

%files
%{_libdir}/cmake/Qt6WaylandClient
%{_libdir}/cmake/Qt6WaylandCompositor
%{_libdir}/cmake/Qt6WaylandScannerTools
%{_libdir}/cmake/Qt6BuildInternals/StandaloneTests/*.cmake
%{_libdir}/cmake/Qt6Gui/*.cmake
%{_libdir}/cmake/Qt6Qml/QmlPlugins/*.cmake
%{_libdir}/libQt6WaylandClient.so
%{_libdir}/libQt6WaylandClient.so.*
%{_libdir}/libQt6WaylandCompositor.so
%{_libdir}/libQt6WaylandCompositor.so.*
%{_qtdir}/examples/wayland
%{_qtdir}/include/QtWaylandClient
%{_qtdir}/include/QtWaylandCompositor
%{_qtdir}/lib/libQt6WaylandClient.prl
%{_qtdir}/lib/libQt6WaylandClient.so
%{_qtdir}/lib/libQt6WaylandClient.so.*
%{_qtdir}/lib/libQt6WaylandCompositor.prl
%{_qtdir}/lib/libQt6WaylandCompositor.so
%{_qtdir}/lib/libQt6WaylandCompositor.so.*
%{_qtdir}/lib/metatypes/qt6waylandcompositor_relwithdebinfo_metatypes.json
%{_qtdir}/mkspecs/modules/qt_lib_waylandclient.pri
%{_qtdir}/mkspecs/modules/qt_lib_waylandclient_private.pri
%{_qtdir}/mkspecs/modules/qt_lib_waylandcompositor.pri
%{_qtdir}/mkspecs/modules/qt_lib_waylandcompositor_private.pri
%{_qtdir}/modules/WaylandClient.json
%{_qtdir}/modules/WaylandCompositor.json
%dir %{_qtdir}/plugins/platforms
%{_qtdir}/plugins/platforms/libqwayland-egl.so
%{_qtdir}/plugins/platforms/libqwayland-generic.so
%{_qtdir}/plugins/platforms/libqwayland-xcomposite-egl.so
%{_qtdir}/plugins/platforms/libqwayland-xcomposite-glx.so
%dir %{_qtdir}/plugins/wayland-decoration-client
%{_qtdir}/plugins/wayland-decoration-client/libbradient.so
%dir %{_qtdir}/plugins/wayland-graphics-integration-client
%{_qtdir}/plugins/wayland-graphics-integration-client/libqt-plugin-wayland-egl.so
%{_qtdir}/plugins/wayland-graphics-integration-client/libshm-emulation-server.so
%{_qtdir}/plugins/wayland-graphics-integration-client/libvulkan-server.so
%{_qtdir}/plugins/wayland-graphics-integration-client/libxcomposite-egl.so
%{_qtdir}/plugins/wayland-graphics-integration-client/libxcomposite-glx.so
%dir %{_qtdir}/plugins/wayland-graphics-integration-server
%{_qtdir}/plugins/wayland-graphics-integration-server/libqt-wayland-compositor-shm-emulation-server.so
%{_qtdir}/plugins/wayland-graphics-integration-server/libqt-wayland-compositor-vulkan-server.so
%{_qtdir}/plugins/wayland-graphics-integration-server/libqt-wayland-compositor-wayland-egl.so
%{_qtdir}/plugins/wayland-graphics-integration-server/libqt-wayland-compositor-wayland-eglstream-controller.so
%{_qtdir}/plugins/wayland-graphics-integration-server/libqt-wayland-compositor-xcomposite-egl.so
%{_qtdir}/plugins/wayland-graphics-integration-server/libqt-wayland-compositor-xcomposite-glx.so
%dir %{_qtdir}/plugins/wayland-shell-integration
%{_qtdir}/plugins/wayland-shell-integration/libfullscreen-shell-v1.so
%{_qtdir}/plugins/wayland-shell-integration/libivi-shell.so
%{_qtdir}/plugins/wayland-shell-integration/libxdg-shell.so
%{_qtdir}/plugins/wayland-shell-integration/libwl-shell-plugin.so
%{_qtdir}/qml/QtWayland/Client
%{_qtdir}/qml/QtWayland/Compositor
%{_libdir}/cmake/Qt6/FindWaylandkms.cmake
%{_libdir}/cmake/Qt6/FindXComposite.cmake
%{_libdir}/cmake/Qt6WaylandEglClientHwIntegrationPrivate
%{_libdir}/cmake/Qt6WaylandEglCompositorHwIntegrationPrivate
%{_libdir}/cmake/Qt6WlShellIntegrationPrivate
%{_libdir}/libQt6WaylandEglClientHwIntegration.so
%{_libdir}/libQt6WaylandEglClientHwIntegration.so.%{major}*
%{_libdir}/libQt6WaylandEglCompositorHwIntegration.so
%{_libdir}/libQt6WaylandEglCompositorHwIntegration.so.%{major}*
%{_libdir}/libQt6WlShellIntegration.so
%{_libdir}/libQt6WlShellIntegration.so.%{major}*
%{_qtdir}/include/QtWaylandEglClientHwIntegration
%{_qtdir}/include/QtWaylandEglCompositorHwIntegration
%{_qtdir}/include/QtWlShellIntegration
%{_qtdir}/lib/libQt6WaylandEglClientHwIntegration.prl
%{_qtdir}/lib/libQt6WaylandEglClientHwIntegration.so
%{_qtdir}/lib/libQt6WaylandEglClientHwIntegration.so.%{major}*
%{_qtdir}/lib/libQt6WaylandEglCompositorHwIntegration.prl
%{_qtdir}/lib/libQt6WaylandEglCompositorHwIntegration.so
%{_qtdir}/lib/libQt6WaylandEglCompositorHwIntegration.so.%{major}*
%{_qtdir}/lib/libQt6WlShellIntegration.prl
%{_qtdir}/lib/libQt6WlShellIntegration.so
%{_qtdir}/lib/libQt6WlShellIntegration.so.%{major}*
%{_qtdir}/lib/metatypes/qt6waylandclient_relwithdebinfo_metatypes.json
%{_qtdir}/lib/metatypes/qt6waylandeglclienthwintegrationprivate_relwithdebinfo_metatypes.json
%{_qtdir}/lib/metatypes/qt6waylandeglcompositorhwintegrationprivate_relwithdebinfo_metatypes.json
%{_qtdir}/lib/metatypes/qt6wlshellintegrationprivate_relwithdebinfo_metatypes.json
%{_qtdir}/libexec/qtwaylandscanner
%{_qtdir}/mkspecs/modules/qt_lib_wayland_egl_client_hw_integration_private.pri
%{_qtdir}/mkspecs/modules/qt_lib_wayland_egl_compositor_hw_integration_private.pri
%{_qtdir}/mkspecs/modules/qt_lib_wl_shell_integration_private.pri
%{_qtdir}/modules/WaylandEglClientHwIntegrationPrivate.json
%{_qtdir}/modules/WaylandEglCompositorHwIntegrationPrivate.json
%{_qtdir}/modules/WlShellIntegrationPrivate.json
