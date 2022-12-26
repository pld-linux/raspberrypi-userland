%define		gitref	54fd97ae4066a10b6b02089bc769ceed328737e0
%define		snap	20220616
Summary:	Libraries for interfacing to Raspberry Pi GPU
Name:		raspberrypi-userland
Version:	1.0.0
Release:	0.%{snap}.1
License:	BSD
Group:		Base/Kernel
Source0:	https://github.com/raspberrypi/userland/archive/%{gitref}/%{name}-%{gitref}.tar.gz
# Source0-md5:	9ce7f475fd3f38800d361cad7f3852c2
Patch0:		install-dirs.patch
Patch1:		system-libfdt.patch
URL:		https://github.com/raspberrypi/userland
BuildRequires:	cmake >= 2.8
BuildRequires:	libfdt-devel >= 1.6.0
BuildRequires:	libstdc++-devel
BuildRequires:	rpmbuild(macros) >= 1.605
ExclusiveArch:	%{arm}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		rpiincludedir	%{_includedir}/raspberrypi
%define		rpilibdir	%{_libdir}/raspberrypi

%description
Libraries used on Raspberry Pi to interface to: EGL, mmal, GLESv2,
vcos, openmaxil, vchiq_arm, bcm_host, WFC, OpenVG.

%package -n raspberrypi-libs
Summary:	Libraries for interfacing to Raspberry Pi GPU
Group:		Libraries
Requires:	libfdt >= 1.6.0

%description -n raspberrypi-libs
Libraries used on Raspberry Pi to interface to: EGL, mmal, GLESv2,
vcos, openmaxil, vchiq_arm, bcm_host, WFC, OpenVG.

%package -n raspberrypi-utils
Summary:	Utilities for Raspberry Pi
Group:		Applications
Requires:	raspberrypi-libs = %{version}-%{release}

%description -n raspberrypi-utils
Utilities for Raspberry Pi.

%package -n raspberrypi-devel
Summary:	Header files for Raspberry Pi libraries
Group:		Development/Libraries
Requires:	raspberrypi-libs = %{version}-%{release}
Provides:	EGL-devel
Provides:	OpenGLESv2-devel

%description -n raspberrypi-devel
Header files for Raspberry Pi libraries.

%package -n raspberrypi-static
Summary:	Static libraries for Raspberry Pi
Group:		Development/Libraries
Requires:	raspberrypi-devel = %{version}-%{release}

%description -n raspberrypi-static
Static libraries for Raspberry Pi.

%prep
%setup -q -n userland-%{gitref}
%patch0 -p1
%patch1 -p1

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH="%{rpiincludedir}" \
	-DCMAKE_INSTALL_LIBDIR:PATH="%{rpilibdir}" \
	-DVMCS_PLUGIN_DIR:PATH="%{rpilibdir}/plugins"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/ld.so.conf.d
echo %{rpilibdir} >$RPM_BUILD_ROOT/etc/ld.so.conf.d/raspberrypi.conf

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{rpilibdir}/pkgconfig $RPM_BUILD_ROOT%{_libdir}

%{__rm} -r $RPM_BUILD_ROOT/opt/vc/src/hello_pi

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n raspberrypi-libs -p /sbin/ldconfig
%postun	-n raspberrypi-libs -p /sbin/ldconfig

%files -n raspberrypi-libs
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/ld.so.conf.d/raspberrypi.conf
%attr(755,root,root) %{rpilibdir}/libEGL.so
%attr(755,root,root) %{rpilibdir}/libGLESv2.so
%attr(755,root,root) %{rpilibdir}/libOpenVG.so
%attr(755,root,root) %{rpilibdir}/libWFC.so
%attr(755,root,root) %{rpilibdir}/libbcm_host.so
%attr(755,root,root) %{rpilibdir}/libbrcm*.so
%attr(755,root,root) %{rpilibdir}/libcontainers.so
%attr(755,root,root) %{rpilibdir}/libdebug_sym.so
%attr(755,root,root) %{rpilibdir}/libdtovl.so
%attr(755,root,root) %{rpilibdir}/libkhrn_client.so
%attr(755,root,root) %{rpilibdir}/libmmal*.so
%attr(755,root,root) %{rpilibdir}/libopenmaxil.so
%attr(755,root,root) %{rpilibdir}/libvc*.so

%files -n raspberrypi-utils
%defattr(644,root,root,755)
%attr(755,root,root) %{rpilibdir}/libEGL.so
%attr(755,root,root) %{_bindir}/containers_*
%attr(755,root,root) %{_bindir}/dtmerge
%attr(755,root,root) %{_bindir}/dtoverlay
%attr(755,root,root) %{_bindir}/dtoverlay-post
%attr(755,root,root) %{_bindir}/dtoverlay-pre
%attr(755,root,root) %{_bindir}/dtparam
%attr(755,root,root) %{_bindir}/mmal_vc_diag
%attr(755,root,root) %{_bindir}/raspistill
%attr(755,root,root) %{_bindir}/raspivid
%attr(755,root,root) %{_bindir}/raspividyuv
%attr(755,root,root) %{_bindir}/raspiyuv
%attr(755,root,root) %{_bindir}/tvservice
%attr(755,root,root) %{_bindir}/vcgencmd
%attr(755,root,root) %{_bindir}/vchiq_test
%attr(755,root,root) %{_bindir}/vcmailbox
%attr(755,root,root) %{_bindir}/vcsmem
%dir %{rpilibdir}/plugins
%attr(755,root,root) %{rpilibdir}/plugins/reader_*.so
%attr(755,root,root) %{rpilibdir}/plugins/writer_*.so
%{_mandir}/man1/dtmerge.1*
%{_mandir}/man1/dtoverlay.1*
%{_mandir}/man1/dtparam.1*
%{_mandir}/man1/raspistill.1*
%{_mandir}/man1/raspivid.1*
%{_mandir}/man1/raspividyuv.1*
%{_mandir}/man1/raspiyuv.1*
%{_mandir}/man1/tvservice.1*
%{_mandir}/man1/vcgencmd.1*
%{_mandir}/man1/vcmailbox.1*
%{_mandir}/man7/raspicam.7*
%{_mandir}/man7/raspiotp.7*
%{_mandir}/man7/raspirev.7*
%{_mandir}/man7/vcmailbox.7*

%files -n raspberrypi-devel
%defattr(644,root,root,755)
%{rpiincludedir}/EGL
%{rpiincludedir}/GLES
%{rpiincludedir}/GLES2
%{rpiincludedir}/IL
%{rpiincludedir}/KHR
%{rpiincludedir}/VG
%{rpiincludedir}/WF
%{rpiincludedir}/interface
%{rpiincludedir}/vcinclude
%{rpiincludedir}/bcm_host.h
%{_pkgconfigdir}/bcm_host.pc
%{_pkgconfigdir}/brcmegl.pc
%{_pkgconfigdir}/brcmglesv2.pc
%{_pkgconfigdir}/brcmvg.pc
%{_pkgconfigdir}/mmal.pc
%{_pkgconfigdir}/vcsm.pc

%files -n raspberrypi-static
%defattr(644,root,root,755)
%{rpilibdir}/libEGL_static.a
%{rpilibdir}/libGLESv2_static.a
%{rpilibdir}/libdebug_sym_static.a
%{rpilibdir}/libkhrn_static.a
