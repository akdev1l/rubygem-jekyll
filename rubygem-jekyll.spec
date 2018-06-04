%global gem_name jekyll

Name:           rubygem-%{gem_name}
Summary:        Simple, blog aware, static site generator
Version:        3.8.2
Release:        1%{?dist}
License:        MIT

URL:            https://github.com/jekyll/jekyll
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem

# Generated tarballs of tests and Rakefile (not present in the gem file)
# git clone https://github.com/jekyll/jekyll jekyll-repo && pushd jekyll-repo
# git checkout v3.8.2
# git archive -o ../jekyll-3.8.2-test.tar.gz v3.8.2 test
# cp -pv Rakefile ../Rakefile-3.8.2
# popd
# rm -rf jekyll-repo
Source1:        %{gem_name}-%{version}-test.tar.gz
Source2:        Rakefile-%{version}

BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  ruby >= 2.1.0

BuildRequires:  help2man

# gems needed for running the test suite
BuildRequires:  rubygem(addressable) >= 2.4
BuildRequires:  rubygem(bundler)
BuildRequires:  rubygem(colorator)
BuildRequires:  rubygem(em-websocket)
BuildRequires:  rubygem(httpclient)
BuildRequires:  rubygem(i18n)
BuildRequires:  rubygem(jekyll-sass-converter)
BuildRequires:  rubygem(kramdown)
BuildRequires:  rubygem(liquid) >= 4.0
BuildRequires:  rubygem(mercenary)
BuildRequires:  rubygem(minitest)
BuildRequires:  rubygem(minitest-profile)
BuildRequires:  rubygem(minitest-reporters)
BuildRequires:  rubygem(nokogiri)
BuildRequires:  rubygem(pathutil)
BuildRequires:  rubygem(rake)
BuildRequires:  rubygem(rdiscount)
BuildRequires:  rubygem(rouge)
BuildRequires:  rubygem(redcarpet)
BuildRequires:  rubygem(rspec-mocks)
BuildRequires:  rubygem(safe_yaml)
BuildRequires:  rubygem(shoulda)
BuildRequires:  rubygem(simplecov)

# Additional gems required by the test suite, which cover optional features of
# jekyll (gems are not yet packaged for fedora):
# BuildRequires:  rubygem(classifier-reborn)
# BuildRequires:  rubygem(jekyll-coffeescript)
# BuildRequires:  rubygem(pygments.rb)
# BuildRequires:  rubygem(tomlrb)

# Additional gems required to run jekyll:
Requires:       rubygem(bigdecimal)
Requires:       rubygem(bundler)
Requires:       rubygem(json)

# Additional gems needed to actually deploy jekyll with default settings:
Recommends:     rubygem(jekyll-feed)
Recommends:     rubygem(jekyll-seo-tag)
Recommends:     rubygem(minima)

# Provide "jekyll", since this package ships a binary
Provides:       %{gem_name} = %{version}-%{release}

BuildArch:      noarch

%description
Jekyll is a simple, blog-aware, static site generator.

You create your content as text files (Markdown), and organize them into
folders. Then, you build the shell of your site using Liquid-enhanced
HTML templates. Jekyll automatically stitches the content and templates
together, generating a website made entirely of static assets, suitable
for uploading to any server.


%package        doc
Summary:        Documentation for %{name}
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description    doc
Documentation for %{name}.


%prep
%setup -q -n %{gem_name}-%{version}

# Relax dependency constraints on i18n
%gemspec_remove_dep -g i18n "~> 0.7"
%gemspec_add_dep -g i18n ">= 0.7"


%build
gem build ../%{gem_name}-%{version}.gemspec

%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/exe -type f | xargs chmod a+x


# Build man page from "jekyll --help" output
export GEM_PATH="%{buildroot}/%{gem_dir}:%{gem_dir}"

mkdir -p %{buildroot}%{_mandir}/man1

help2man -N -s1 -o %{buildroot}%{_mandir}/man1/%{gem_name}.1 \
    %{buildroot}/usr/share/gems/gems/%{gem_name}-%{version}/exe/%{gem_name}


%check
pushd .%{gem_instdir}

# There are some failures among the results of the unit tests, most of them are
# caused by missing dependencies:
#
# - classifier-reborn:
#     Gem isn't packaged for fedora, it has *really* outdated dependencies.
# - jekyll-coffeescript:
#     Gem isn't yet packaged for fedora, and coffeescript functionality is
#     optional.
# - pygments.rb:
#     Gem isn't packaged for fedora, it's test suite fails, and it vendors
#     its own copy of pygments. Additionally, support for pygments is optional
#     and will be dropped with jekyll 4.0 anyway.
# - tomlrb:
#     Gem isn't yet packaged for fedora, and the functionality looks optional.

# extract "test" directory
tar -xzvf %{SOURCE1}

# add "Rakefile"
cp %{SOURCE2} ./Rakefile

# run tests and ignore failure (for now)
rake test TESTOPTS='-v' --trace || :

popd


%files
%license %{gem_instdir}/LICENSE

%{_bindir}/jekyll

%{_mandir}/man1/jekyll.1*

%dir %{gem_instdir}
%{gem_instdir}/exe
%{gem_instdir}/rubocop

%{gem_libdir}
%{gem_spec}

%exclude %{gem_instdir}/.rubocop.yml
%exclude %{gem_cache}


%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.markdown


%changelog
* Mon Jun 04 2018 Fabio Valentini <decathorpe@gmail.com> - 3.8.2-1
- Update to version 3.8.2.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Apr 09 2017 Björn Esser <besser82@fedoraproject.org> - 3.2.1-3
- Add explicit Requires: rubygem(json)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Aug 24 2016 Björn Esser <fedora@besser82.io> - 3.2.1-1
- initial import (#1368851)

* Sun Aug 21 2016 Björn Esser <fedora@besser82.io> - 3.2.1-0.1
- initial rpm-release (#1368851)

