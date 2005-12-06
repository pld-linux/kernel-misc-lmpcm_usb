#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
Summary:	USB Logitech MediaPlay Cordless Mouse driver for Linux
Summary(pl):	Sterownik do myszy USB Logitech MediaPlay Cordless
Name:		kernel-misc-lmpcm_usb
Version:	0.5.2
%define		_rel	1
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://daemon.prozone.ws/~david/projects/lmpcm_usb/lmpcm_usb-%{version}.tar.gz
# Source0-md5:	551279d6bea3ee6252d9b4a62cc185a6
URL:		http://daemon.prozone.ws/~david/projects/lmpcm_usb/
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.217
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
Provides:	kernel(lmpcm_usb)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux driver for USB Logitech MediaPlay
Cordless Mouse.

%description -l pl
Ten pakiet zawiera sterownik dla Linuksa do myszy USB Logitech
MediaPlay Cordless.

%package -n kernel-smp-misc-lmpcm_usb
Summary:	USB Logitech MediaPlay Cordless Mouse driver for Linux SMP
Summary(pl):	Sterownik do myszy USB Logitech MediaPlay Cordless
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif
Provides:	kernel(lmpcm_usb)

%description -n kernel-smp-misc-lmpcm_usb
This package contains the Linux SMP driver for USB Logitech MediaPlay
Cordless Mouse.

%description -n kernel-smp-misc-lmpcm_usb -l pl
Ten pakiet zawiera sterownik dla Linuksa SMP do myszy USB Logitech
MediaPlay Cordless.


%prep
%setup -q -n lmpcm_usb-%{version}

%build
rm -rf built
mkdir -p built/{nondist,smp,up}
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf include
	install -d include/{linux,config}
	ln -sf %{_kernelsrcdir}/config-$cfg .config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg Module.symvers
	%if %{without dist_kernel}
                ln -sf %{_kernelsrcdir}/scripts
        %endif
	touch include/config/MARKER
	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}
	mv *.ko built/$cfg
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc

cd built
install %{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}/*.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
%if %{with smp} && %{with dist_kernel}
install smp/*.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc
%endif
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%post	-n kernel-smp-misc-lmpcm_usb
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-misc-lmpcm_usb
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc ChangeLog README
/lib/modules/%{_kernel_ver}/misc/*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-misc-lmpcm_usb
%defattr(644,root,root,755)
%doc ChangeLog README
/lib/modules/%{_kernel_ver}smp/misc/*
%endif
