#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)
#
%define		_rel	1
%define		pname	lmpcm_usb
Summary:	USB Logitech MediaPlay Cordless Mouse driver for Linux
Summary(pl.UTF-8):	Sterownik do myszy USB Logitech MediaPlay Cordless
Name:		kernel%{_alt_kernel}-misc-%{pname}
Version:	0.5.6
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://daemon.prozone.org/~david/projects/lmpcm_usb/%{pname}-%{version}.tar.gz
# Source0-md5:	33cbe52adae24bdf628fe04b254f5d48
Patch0:		%{pname}-print_info.patch
Patch1:		%{pname}-kernel_compatibility.patch
URL:		http://daemon.prozone.org/~david/projects/lmpcm_usb/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
%{?with_dist_kernel:%requires_releq_kernel}
Requires(post,postun):	/sbin/depmod
Provides:	kernel(lmpcm_usb)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux driver for USB Logitech MediaPlay
Cordless Mouse.

%description -l pl.UTF-8
Ten pakiet zawiera sterownik dla Linuksa do myszy USB Logitech
MediaPlay Cordless.

%prep
%setup -q -n %{pname}-%{version}
%patch0 -p1
%patch1 -p1

%build
%build_kernel_modules -m lmpcm_usb

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m lmpcm_usb -d misc


%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-misc-%{pname}
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-misc-%{pname}
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
%doc ChangeLog README
/lib/modules/%{_kernel_ver}/misc/lmpcm_usb.ko*
