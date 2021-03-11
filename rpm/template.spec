%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/rolling/.*$
%global __requires_exclude_from ^/opt/ros/rolling/.*$

Name:           ros-rolling-rosidl-generator-py
Version:        0.9.4
Release:        2%{?dist}%{?release_suffix}
Summary:        ROS rosidl_generator_py package

License:        Apache License 2.0
Source0:        %{name}-%{version}.tar.gz

Requires:       python%{python3_pkgversion}-numpy
Requires:       ros-rolling-ament-cmake
Requires:       ros-rolling-ament-index-python
Requires:       ros-rolling-python-cmake-module
Requires:       ros-rolling-rmw
Requires:       ros-rolling-rosidl-cmake
Requires:       ros-rolling-rosidl-generator-c
Requires:       ros-rolling-rosidl-parser
Requires:       ros-rolling-rosidl-runtime-c
Requires:       ros-rolling-rosidl-typesupport-c
Requires:       ros-rolling-rosidl-typesupport-interface
Requires:       ros-rolling-rpyutils
Requires:       ros-rolling-ros-workspace
BuildRequires:  python%{python3_pkgversion}-numpy
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  ros-rolling-ament-cmake
BuildRequires:  ros-rolling-ament-cmake-pytest
BuildRequires:  ros-rolling-ament-index-python
BuildRequires:  ros-rolling-ament-lint-auto
BuildRequires:  ros-rolling-ament-lint-common
BuildRequires:  ros-rolling-python-cmake-module
BuildRequires:  ros-rolling-rmw
BuildRequires:  ros-rolling-rosidl-cmake
BuildRequires:  ros-rolling-rosidl-generator-c
BuildRequires:  ros-rolling-rosidl-generator-cpp
BuildRequires:  ros-rolling-rosidl-parser
BuildRequires:  ros-rolling-rosidl-runtime-c
BuildRequires:  ros-rolling-rosidl-typesupport-c
BuildRequires:  ros-rolling-rosidl-typesupport-introspection-c
BuildRequires:  ros-rolling-rpyutils
BuildRequires:  ros-rolling-test-interface-files
BuildRequires:  ros-rolling-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}
Provides:       ros-rolling-rosidl-generator-packages(member)

%if 0%{?with_weak_deps}
Supplements:    ros-rolling-rosidl-generator-packages(all)
%endif

%description
Generate the ROS interfaces in Python.

%prep
%autosetup

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/rolling" \
    -DAMENT_PREFIX_PATH="/opt/ros/rolling" \
    -DCMAKE_PREFIX_PATH="/opt/ros/rolling" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
%make_install -C obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
%make_build -C obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/rolling

%changelog
* Thu Mar 11 2021 Shane Loretz <sloretz@openrobotics.org> - 0.9.4-2
- Autogenerated by Bloom

* Mon Mar 08 2021 Shane Loretz <sloretz@openrobotics.org> - 0.9.4-1
- Autogenerated by Bloom

