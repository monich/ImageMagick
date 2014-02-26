%global MAJOR_VERSION  6
%global FULL_VERSION  6.8.7

Name:           ImageMagick
Version:        6.8.7
Release:        10
Summary:        Convert, edit, or compose bitmap images in a variety of formats
Group:          Applications/Multimedia
License:        http://www.imagemagick.org/script/license.php
Url:            http://www.imagemagick.org/
Source0:        %{name}-%{version}.tar.bz2

BuildRequires: python
BuildRequires:  bzip2-devel, freetype-devel, libjpeg-devel, libpng-devel
BuildRequires:  libtool-ltdl-devel
BuildRequires:  libtiff-devel, giflib-devel, zlib-devel
BuildRequires:  libgomp

%description
ImageMagick is a software suite to create, edit, and compose bitmap images. It
can read, convert and write images in a variety of formats (about 100)
including DPX, GIF, JPEG, JPEG-2000, PDF, PhotoCD, PNG, Postscript, SVG,
and TIFF. Use ImageMagick to translate, flip, mirror, rotate, scale, shear
and transform images, adjust image colors, apply various special effects,
or draw text, lines, polygons, ellipses and Bezier curves.

The functionality of ImageMagick is typically utilized from the command line
or you can use the features from programs written in your favorite programming
language. Choose from these interfaces: G2F (Ada), MagickCore (C), MagickWand
(C), ChMagick (Ch), Magick++ (C++), JMagick (Java), L-Magick (Lisp), nMagick
(Neko/haXe), PascalMagick (Pascal), PerlMagick (Perl), MagickWand for PHP
(PHP), PythonMagick (Python), RMagick (Ruby), or TclMagick (Tcl/TK). With a
language interface, use ImageMagick to modify or create images automagically
and dynamically.

ImageMagick is free software delivered as a ready-to-run binary distribution
or as source code that you may freely use, copy, modify, and distribute in
both open and proprietary applications. It is distributed under an Apache
2.0-style license, approved by the OSI.

The ImageMagick development process ensures a stable API and ABI. Before
each ImageMagick release, we perform a comprehensive security assessment that
includes memory and thread error detection to help prevent exploits.ImageMagick
is free software delivered as a ready-to-run binary distribution or as source
code that you may freely use, copy, modify, and distribute in both open and
proprietary applications. It is distributed under an Apache 2.0-style license,
approved by the OSI.

%package tools
Summary: ImageMagick tools
Group: Applications/Multimedia
Requires: %{name} = %{version}-%{release}

%description tools
ImageMagick command line tools.

%package devel
Summary: Library links and header files for ImageMagick application development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: bzip2-devel
Requires: freetype-devel
Requires: libtiff-devel
Requires: libjpeg-devel
Requires: pkgconfig

%description devel
ImageMagick-devel contains the library links and header files you will
need to develop ImageMagick applications. ImageMagick is an image
manipulation program.

If you want to create applications that will use ImageMagick code or
APIs, you need to install ImageMagick-devel as well as ImageMagick.
You do not need to install it if you just want to use ImageMagick,
however.

%prep
%setup -q -n %{name}-%{version}
sed -i 's/libltdl.la/libltdl.so/g' configure
iconv -f ISO-8859-1 -t UTF-8 README.txt > README.txt.tmp
touch -r README.txt README.txt.tmp
mv README.txt.tmp README.txt
# for %%doc
mkdir Magick++/examples
cp -p Magick++/demo/*.cpp Magick++/demo/*.miff Magick++/examples

%build
%configure --enable-shared \
           --disable-static \
           --with-modules \
           --without-perl \
           --without-x \
           --with-threads \
           --without-magick_plus_plus \
           --without-gslib \
           --without-wmf \
           --without-lcms \
           --without-rsvg \
           --without-xml \
           --without-dps

# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# Do *NOT* use %%{?_smp_mflags}, this causes PerlMagick to be silently misbuild
make

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot} INSTALL="install -p"

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libMagickCore*so*
%{_libdir}/libMagickWand*so*
%{_libdir}/%{name}-%{FULL_VERSION}
%{_datadir}/%{name}-%{MAJOR_VERSION}
%config %{_sysconfdir}/%{name}-%{MAJOR_VERSION}/*

%files tools
%{_bindir}/[a-z]*

%files devel
%defattr(-,root,root,-)
%{_bindir}/MagickCore-config
%{_bindir}/Magick-config
%{_bindir}/MagickWand-config
%{_bindir}/Wand-config
%{_libdir}/pkgconfig/MagickCore.pc
%{_libdir}/pkgconfig/ImageMagick.pc
%{_libdir}/pkgconfig/MagickWand.pc
%{_libdir}/pkgconfig/Wand.pc
%dir %{_includedir}/%{name}-%{MAJOR_VERSION}
%{_includedir}/%{name}-%{MAJOR_VERSION}/magick
%{_includedir}/%{name}-%{MAJOR_VERSION}/wand

%exclude %{_libdir}/*.la
%exclude %{_libdir}/pkgconfig/*-*.pc
%exclude %{_datadir}/doc/*
%exclude %{_mandir}/man*

%changelog
* Wed Feb 26 2014 Slava Monich <slava.monich@jolla.com> 1.0-0
- RPM spec for Jolla OBS build
