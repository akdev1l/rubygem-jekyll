%global gem_name jekyll

Name:           rubygem-%{gem_name}
Summary:        Simple, blog aware, static site generator
Version:        4.2.0
Release:        2%{?dist}
License:        MIT

URL:            https://github.com/jekyll/jekyll
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
Source1:        %{url}/archive/v%{version}/%{gem_name}-%{version}.tar.gz

# Patch the "new" command to skip the "bundle install" step
Patch0:         0000-jekyll-commands-remove-bundle-install-step-for-new.patch

# Patch test helper to disable code coverage and minitest plugins
Patch1:         0001-test-helper-disable-simplecov-and-minitest-plugins.patch

# Patch to remove (failing) internet connectivity check
Patch2:         0002-test-utils-remove-internet-connectivity-test.patch

# Patch to disable broken tests using the "test-theme" theme
Patch3:         0003-test-disable-tests-requiring-the-test-theme.patch

# Patches to remove tests for optional functionality with missing dependencies:
# classifier-reborn, jekyll-coffeescript, pygments.rb, tomlrb
Patch4:         0004-tests-related_posts-disable-tests-requiring-classifi.patch
Patch5:         0005-test-coffeescript-disable-tests-requiring-coffeescri.patch

# Patch to disable tests reliant on the Gemfile and .gemspec file,
# which are not shipped as part of the jekyll gem:
Patch6:         0006-test-plugin_manager-disable-tests-requiring-gemspec-.patch

# Patch to disable a race-y test that fails regularly
Patch7:         0007-test-kramdown-disable-race-y-test.patch

# Ruby 3.0 compatibility
# Upstream fix: https://github.com/jekyll/jekyll/commit/5c797ba136a4d162497e976a1a52946344e6c32f
Patch8:         0008-test-separate-keyword-arguments.patch

BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  ruby >= 2.4.0

BuildRequires:  help2man

# gems needed for running the test suite
BuildRequires:  rubygem(addressable) >= 2.4
BuildRequires:  rubygem(bundler)
BuildRequires:  rubygem(colorator)
BuildRequires:  rubygem(em-websocket)
BuildRequires:  rubygem(httpclient)
BuildRequires:  rubygem(i18n)
BuildRequires:  rubygem(jekyll-sass-converter) >= 2.0.0
BuildRequires:  rubygem(kramdown) >= 2.0.0
BuildRequires:  rubygem(kramdown-parser-gfm)
BuildRequires:  rubygem(kramdown-syntax-coderay)
BuildRequires:  rubygem(liquid) >= 4.0
BuildRequires:  rubygem(mercenary)
BuildRequires:  rubygem(minitest)
BuildRequires:  rubygem(nokogiri)
BuildRequires:  rubygem(pathutil)
BuildRequires:  rubygem(racc)
BuildRequires:  rubygem(rouge)
BuildRequires:  rubygem(rspec-mocks)
BuildRequires:  rubygem(safe_yaml)
BuildRequires:  rubygem(shoulda)
BuildRequires:  rubygem(terminal-table)
BuildRequires:  rubygem(tomlrb) >= 2.0.1
BuildRequires:  rubygem(webrick)

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

# extract test files not shipped with the gem
mkdir upstream && pushd upstream
tar -xzvf %{SOURCE1}
mv %{gem_name}-%{version}/test ../test
popd && rm -r upstream

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

# mercenary is too old in fedora (0.3.6 vs. 0.4.0)
# Upstream fix: https://github.com/jekyll/jekyll/pull/8586
%gemspec_remove_dep -g mercenary "~> 0.4.0"
%gemspec_add_dep -g mercenary ">= 0.3.6"

# works with terminal-table 1.8.0 and 3.0.0, too
# Upstream fix: https://github.com/jekyll/jekyll/pull/8586
%gemspec_remove_dep -g terminal-table "~> 2.0"
%gemspec_add_dep -g terminal-table ">= 1.8.0"

# webrick became a normal gem in Ruby 3.0, needs to be added as dependency
# Upstream fix: https://github.com/jekyll/jekyll/commit/5c797ba136a4d162497e976a1a52946344e6c32f
%gemspec_add_dep -g webrick "~> 1.7"

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
%{gem_instdir}/exe/

%{gem_libdir}
%{gem_spec}

%exclude %{gem_instdir}/.rubocop.yml
%exclude %{gem_instdir}/rubocop
%exclude %{gem_cache}


%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.markdown


%changelog
* Thu Feb 18 2021 Otto Urpelainen - 4.2.0-2
- Allow terminal-table 1.8.0

* Mon Feb 15 2021 Otto Urpelainen - 4.2.0-1
- Update to version 4.2.0.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 04 2020 Fabio Valentini <decathorpe@gmail.com> - 4.1.1-1
- Update to version 4.1.1.

* Thu May 28 2020 Fabio Valentini <decathorpe@gmail.com> - 4.1.0-2
- Relax mercenary runtime dependency.

* Wed May 27 2020 Fabio Valentini <decathorpe@gmail.com> - 4.1.0-1
- Update to version 4.1.0.

* Fri May 15 2020 Fabio Valentini <decathorpe@gmail.com> - 4.0.1-1
- Update to version 4.0.1.

* Fri Jan 31 2020 Fabio Valentini <decathorpe@gmail.com> - 4.0.0-3
- Add BR: rubygem(racc) to fix FTBFS issue.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Sep 13 2019 Fabio Valentini <decathorpe@gmail.com> - 4.0.0-1
- Update to version 4.0.0.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 08 2019 Fabio Valentini <decathorpe@gmail.com> - 3.8.6-1
- Update to version 3.8.6.
- Ignore broken tests for rouge 2, we have rouge 3 in fedora.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 05 2018 Fabio Valentini <decathorpe@gmail.com> - 3.8.5-1
- Update to version 3.8.5.

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

