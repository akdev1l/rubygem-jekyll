%global gem_name jekyll

Name:           rubygem-%{gem_name}
Summary:        Simple, blog aware, static site generator
Version:        3.8.4
Release:        1%{?dist}
License:        MIT

URL:            https://github.com/jekyll/jekyll
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem

# Generated tarball of tests (not present in the gem file)
# git clone https://github.com/jekyll/jekyll jekyll-repo && pushd jekyll-repo
# git checkout v3.8.4
# git archive -o ../jekyll-3.8.4-test.tar.gz v3.8.4 test
# popd
# rm -rf jekyll-repo
Source1:        %{gem_name}-%{version}-test.tar.gz

# Patches generated with "git format-patch --start-number 0"
# Repository:   https://pagure.io/jekyll-fedora/branch/fedora-3.8.4
# Patches:      v3.8.4 → fedora-3.8.4

# Patch test helper to disable code coverage and minitest plugins
Patch0:         0000-test-helper-disable-simplecov-and-minitest-plugins.patch

# Patch tests for the "jekyll new" command to use "--skip-bundle" - to not
# require internet access and fail due to timeouts in "bundle install"
Patch1:         0001-test-new_command-add-skip-bundle-to-fix-tests-withou.patch

# Patch to adapt to different rdiscount TOC generation
Patch2:         0002-test-rdiscount-adapt-to-different-TOC-generation-wit.patch

# Patch to remove (failing) internet connectivity check
Patch3:         0003-test-utils-remove-internet-connectivity-test.patch

# Patch to disable broken tests using the "test-theme" theme
Patch4:         0004-test-disable-tests-requiring-the-test-theme.patch

# Patches to remove tests for optional functionality with missing dependencies:
# classifier-reborn, jekyll-coffeescript, pygments.rb, tomlrb
Patch5:         0005-tests-configuration-disable-tests-requiring-the-toml.patch
Patch6:         0006-tests-disable-tests-requiring-the-pygments.rb-gem.patch
Patch7:         0007-tests-related_posts-disable-tests-requiring-the-clas.patch
Patch8:         0008-test-coffeescript-disable-tests-requiring-the-coffee.patch

# Patch to disable tests reliant on the Gemfile and .gemspec file,
# which are not shipped as part of the jekyll gem:
Patch9:         0009-test-plugin_manager-disable-tests-requiring-upstream.patch

BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  ruby >= 2.1.0

BuildRequires:  help2man

# gems needed for running the test suite
BuildRequires:  rubygem(addressable) >= 2.4
BuildRequires:  rubygem(bundler)
BuildRequires:  rubygem(coderay)
BuildRequires:  rubygem(colorator)
BuildRequires:  rubygem(em-websocket)
BuildRequires:  rubygem(httpclient)
BuildRequires:  rubygem(i18n)
BuildRequires:  rubygem(jekyll-sass-converter)
BuildRequires:  rubygem(kramdown)
BuildRequires:  rubygem(liquid) >= 4.0
BuildRequires:  rubygem(mercenary)
BuildRequires:  rubygem(minitest)
BuildRequires:  rubygem(nokogiri)
BuildRequires:  rubygem(pathutil)
BuildRequires:  rubygem(rdiscount)
BuildRequires:  rubygem(rouge)
BuildRequires:  rubygem(redcarpet)
BuildRequires:  rubygem(rspec-mocks)
BuildRequires:  rubygem(safe_yaml)
BuildRequires:  rubygem(shoulda)

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
%setup -q -n %{gem_name}-%{version} -a1

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

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
ruby -I"lib:test" -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'


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
* Wed Sep 19 2018 Fabio Valentini <decathorpe@gmail.com> - 3.8.4-1
- Update to version 3.8.4.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 11 2018 Fabio Valentini <decathorpe@gmail.com> - 3.8.3-1
- Update to version 3.8.3.

* Tue Jun 05 2018 Fabio Valentini <decathorpe@gmail.com> - 3.8.2-3
- Fix kramdown test issues (patch: Vít Ondruch).
- Patch test suite to remove tests reliant on upstream Gemfile and .gemspec.
- Don't ignore test results anymore.

* Tue Jun 05 2018 Fabio Valentini <decathorpe@gmail.com> - 3.8.2-2
- Drop code coverage and minitest plugins (patches: Vít Ondruch).
- Patch test suite to remove broken tests and tests for optional functionality.

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

