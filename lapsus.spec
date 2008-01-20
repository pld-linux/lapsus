# TODO:
# - fix install (kicker applets are installed into wrong dir)
%define snap	20070916
Summary:	Lapsus - Linux on laptops
Summary(pl.UTF-8):	Lapsus - Linux na laptopach
Name:		lapsus
Version:	0.0.5
Release:	0.1
License:	GPL v2
Group:		X11/Applications
Source0:	%{name}-%{snap}.tar.bz2
# Source0-md5:	e68eb1dc0d8ad1a7389600c85a9fbde6
Patch0:		%{name}-as_needed.patch
Patch1:		kde-ac260-lt.patch
URL:		http://lapsus.berlios.de/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-devel >= 0.90
BuildRequires:	kdelibs-devel >= 9:3.2.0
BuildRequires:	rpmbuild(macros) >= 1.129
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lapsus is a set of programs providing easy access to many features of
various laptops. It currently supports most features provided by
asus-laptop kernel module from ACPI4Asus project, such as additional
LEDs, hotkeys, backlight control etc. It also has support for some IBM
laptops features provided by IBM ThinkPad ACPI Extras Driver and NVRAM
device.

%description -l pl.UTF-8
Lapsus to zestaw narzędzi umożliwiających łatwy dostęp do
funkcjonalności udostępnianej przez laptopy. Aktualnie wspierana jest
wiekszość z funkcjonalności modułu jądra asus-laptop: dodatkowe
diody LED, przyciski, sterowanie podświetleniem matrycy itp. Lapsus
obsługuje też niektóre z funkcji laptopów IBM-a udostępnione przez
moduł IBM Thinkpad ACPI Extras oraz urządzenie NVRAM.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1

%build
# update config.sub for amd64
cp -f /usr/share/automake/config.sub admin
# or rebuild auto*
%{__make} -f admin/Makefile.common cvs
%configure \
%if "%{_lib}" == "lib64"
	--enable-libsuffix=64 \
%endif
	--%{?debug:en}%{!?debug:dis}able-debug%{?debug:=full} \
	--with-qt-libraries=%{_libdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}}
install -d $RPM_BUILD_ROOT%{_libdir}/kde3

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	kde_htmldir=%{_kdedocdir} \
	kde_libs_htmldir=%{_kdedocdir} \
	kdelnkdir=%{_desktopdir} \

%find_lang %{name} --with-kde

# XXX: fix Makefiles instead
mv -f $RPM_BUILD_ROOT%{_libdir}/lapsus_panelapplet.* $RPM_BUILD_ROOT%{_libdir}/kde3

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/lapsusd
%{_libdir}/kde3/lapsus_panelapplet.la
%attr(755,root,root) %{_libdir}/kde3/lapsus_panelapplet.so
%{_datadir}/apps/%{name}
%{_datadir}/apps/kicker/applets/*.desktop
