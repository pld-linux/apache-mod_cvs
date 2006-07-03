%define		mod_name	cvs
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: Automatically updates files in a CVS-based webtree
Summary(pl):	Modu³ do apache: Automatyczne uaktualnianie plików z drzewa CVS
Name:		apache-mod_%{mod_name}
Version:	0.5.91
Release:	2
License:	GPL
Group:		Networking/Daemons
Source0:	http://resare.com/noa/mod_cvs/dist/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	ef100c30ff734464c6194a2e707136b5
URL:		http://www.resare.com/noa/mod_cvs/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	zlib-devel
Requires(triggerpostun):	%{apxs}
Requires:	apache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
Apache module: Automatically updates files in a CVS-based webtree.

%description -l pl
Modu³ do apache: Automatyczne uaktualnianie plików z drzewa CVS.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{apxs} -c mod_%{mod_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}/mod_%{mod_name}.so

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc README doc/*.html
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
