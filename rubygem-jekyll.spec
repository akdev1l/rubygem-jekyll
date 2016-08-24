%{!?_pkgdocdir:%global _pkgdocdir %{_docdir}/%{name}-%{version}}
%global gem_name jekyll

Name:		rubygem-%{gem_name}
Version:	3.2.1
Release:	1%{?dist}
Summary:	Transform your plain text into static websites and blogs

License:	MIT
URL:		https://%{gem_name}rb.com
Source0:	https://rubygems.org/downloads/%{gem_name}-%{version}.gem

BuildArch:	noarch
BuildRequires:	help2man
BuildRequires:	rubygem(bigdecimal)
BuildRequires:	rubygem(colorator)
BuildRequires:	rubygem(jekyll-sass-converter)
BuildRequires:	rubygem(jekyll-watch)
BuildRequires:	rubygem(kramdown)
BuildRequires:	rubygem(liquid)
BuildRequires:	rubygem(mercenary)
BuildRequires:	rubygem(pathutil)
BuildRequires:	rubygem(rouge)
BuildRequires:	rubygem(safe_yaml)
BuildRequires:	rubygems-devel

Provides:	%{gem_name}		== %{version}-%{release}
%if (0%{?rhel} && 0%{?rhel} <=7)
Provides:	rubygem(%{gem_name})	== %{version}-%{release}
%endif # (0%%{?rhel} && 0%%{?rhel} <=7)

%description
Jekyll is a simple, blog-aware, static site generator perfect
for personal, project, or organization sites.  Think of it like
a file-based CMS, without all the complexity.  Jekyll takes your
content, renders Markdown and Liquid templates, and spits out a
complete, static website ready to be served by Apache, Nginx or
another web server.  Jekyll is the engine behind GitHub Pages,
which you can use to host sites right from your GitHub repositories.
Jekyll does what you tell it to do — no more, no less.  It doesn't
try to outsmart users by making bold assumptions, nor does it
burden them with needless complexity and configuration.  Put simply,
Jekyll gets out of your way and allows you to concentrate on what
truly matters: your content.


%package doc
Summary:	Documentation files for %{name}

%description doc
This package contains the documentation files for %{name}.


%prep
%{__rm} -rf %{gem_name}-%{version}
%{_bindir}/gem unpack %{SOURCE0}
%setup -DTqn %{gem_name}-%{version}
%{_bindir}/gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
f="exe/%{gem_name}"
%{__sed} -e '1s:^#![ \t]*%{_bindir}/env ruby:#!%{_bindir}/ruby:'	\
	< ${f} > ${f}.new &&						\
/bin/touch -r ${f} ${f}.new && %{__mv} -f ${f}.new ${f}


%build
%{_bindir}/gem build %{gem_name}.gemspec
%gem_install


%install
%{__mkdir} -p %{buildroot}%{_bindir} %{buildroot}%{gem_dir}		\
	%{buildroot}%{_mandir}/man1
%{__cp} -a ./%{_bindir}/* %{buildroot}%{_bindir}
%{__cp} -a ./%{gem_dir}/* %{buildroot}%{gem_dir}
%{__rm} -f %{buildroot}%{gem_instdir}/{*.markdown,LICENSE,.rubocop.yml}
export GEM_PATH="%{buildroot}%{gem_dir}:%{gem_dir}"
%{_bindir}/help2man -N -s1 -o %{buildroot}%{_mandir}/man1/%{gem_name}.1	\
	%{buildroot}%{_bindir}/%{gem_name}


%files
%exclude %{gem_cache}
%license LICENSE
%doc README.markdown
%{_bindir}/%{gem_name}
%{_mandir}/man1/%{gem_name}.1*
%{gem_instdir}
%{gem_spec}

%files doc
%doc %{_pkgdocdir}
%doc %{gem_docdir}


%changelog
* Wed Aug 24 2016 Björn Esser <fedora@besser82.io> - 3.2.1-1
- initial import (#1368851)

* Sun Aug 21 2016 Björn Esser <fedora@besser82.io> - 3.2.1-0.1
- initial rpm-release (#1368851)
