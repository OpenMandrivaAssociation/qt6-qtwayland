#define beta rc2
#define snapshot 20200627
%define major 6

%define _qtdir %{_libdir}/qt%{major}

Name:		qt6-qtwayland
Version:	6.0.1
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
BuildRequires:	%{_lib}Qt6DBus-devel
BuildRequires:	%{_lib}Qt6Gui-devel
BuildRequires:	%{_lib}Qt6Widgets-devel
BuildRequires:	%{_lib}Qt6Xml-devel
BuildRequires:	%{_lib}Qt6Qml-devel >= %{version}-0
BuildRequires:	%{_lib}Qt6OpenGL-devel
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
for i in %{buildroot}%{_qtdir}/lib/cmake/*; do
	d="$(basename ${i})"
	# BuildInternals, Gui and Qml are owned by qtbase
	[ "$d" = "Qt6BuildInternals" -o "$d" = "Qt6Gui" -o "$d" = "Qt6Qml" ] && continue
	ln -s ../qt%{major}/lib/cmake/$d %{buildroot}%{_libdir}/cmake/
done

%files
%{_libdir}/cmake/Qt6WaylandClient
%{_libdir}/cmake/Qt6WaylandCompositor
%{_libdir}/cmake/Qt6WaylandScannerTools
%{_libdir}/libQt6WaylandClient.so
%{_libdir}/libQt6WaylandClient.so.*
%{_libdir}/libQt6WaylandCompositor.so
%{_libdir}/libQt6WaylandCompositor.so.*
%{_qtdir}/bin/qtwaylandscanner
%{_qtdir}/examples/wayland
%{_qtdir}/include/QtWaylandClient
%{_qtdir}/include/QtWaylandCompositor
%{_qtdir}/lib/cmake/Qt6BuildInternals/StandaloneTests/QtWaylandTestsConfig.cmake
%{_qtdir}/lib/cmake/Qt6Gui/*.cmake
%{_qtdir}/lib/cmake/Qt6Qml/QmlPlugins/*.cmake
%{_qtdir}/lib/cmake/Qt6WaylandClient
%{_qtdir}/lib/cmake/Qt6WaylandCompositor
%{_qtdir}/lib/cmake/Qt6WaylandScannerTools
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
%{_qtdir}/plugins/wayland-shell-integration/libwl-shell.so
%{_qtdir}/plugins/wayland-shell-integration/libxdg-shell.so
%{_qtdir}/qml/QtWayland/Client
%{_qtdir}/qml/QtWayland/Compositor
