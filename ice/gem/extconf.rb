#
# Copyright (c) ZeroC, Inc. All rights reserved.
#

require "mkmf"
require "rbconfig"

if RUBY_PLATFORM =~ /mswin|mingw/
    puts "MinGW is not supported with Ice for Ruby."
    exit 1
end

#
# On OSX & Linux bzlib.h is required.
#
if not have_header("bzlib.h") then
    exit 1
end

if RUBY_PLATFORM =~ /linux/
    #
    # On Linux openssl is required for IceSSL.
    #
    if not have_header("openssl/ssl.h") then
        exit 1
    end
end

if RUBY_PLATFORM =~ /darwin/
    # Make sure to use the SDK from Xcode (required for Sierra where old system headers can be used otherwise)
    RbConfig::MAKEFILE_CONFIG['CC'] = 'xcrun -sdk macosx clang'
    RbConfig::MAKEFILE_CONFIG['CXX'] = 'xcrun -sdk macosx clang++'
end

$INCFLAGS << ' -Iice/cpp/include'
$INCFLAGS << ' -Iice/cpp/include/generated'
$INCFLAGS << ' -Iice/cpp/src'

$CPPFLAGS << ' -DICE_STATIC_LIBS'
$CPPFLAGS << ' -DICE_GEM'

if RUBY_PLATFORM =~ /darwin/
    $LOCAL_LIBS << ' -framework Security -framework CoreFoundation'
elsif RUBY_PLATFORM =~ /linux/
    $LOCAL_LIBS << ' -lssl -lcrypto -lbz2 -lrt'
        if RUBY_VERSION =~ /1.8/
            # With 1.8 we need to link with C++ runtime, as gcc is used to link the extension
            $LOCAL_LIBS << ' -lstdc++'
            # With 1.8 we need to fix the objects output directory
            $CPPFLAGS << ' -o$@'
            # With 1.8 /usr/lib/ruby/1.8/regex.h conflicts with /usr/include/regex.h
            # we add a symbolic link to workaround the problem
            if File.exist?('/usr/include/regex.h') && !File.exist?('regex.h')
                FileUtils.ln_s '/usr/include/regex.h', 'regex.h'
            end
        end
end
$CPPFLAGS << ' -w'

# Setup the object and source files.
$objs = []
$srcs = []

# Add the plugin source.
Dir["*.cpp"].each do |f|
    $objs << File.basename(f, ".*") + ".o"
    $srcs << f
end

def filter(f)
    #
    # Filter IceSSL sources that doesn't match current OS default
    # implementation
    #
    if f.start_with?("SChannel") or f.start_with?("UWP")
        return false
    end
    if RUBY_PLATFORM =~ /darwin/ and f.start_with?("OpenSSL")
        return false
    end
    if !(RUBY_PLATFORM =~ /darwin/) and f.start_with?("SecureTransport")
         return false
    end
    return true
end

Dir["ice/**/*.cpp"].each do |f|
    if filter File.basename(f)
        $objs << File.dirname(f) + "/" + File.basename(f, ".*") + ".o"
        $srcs << f
    end
end

# The mcpp source.
Dir["ice/mcpp/*.c"].each do |f|
    dir = "ice/mcpp"
    $objs << File.join(dir, File.basename(f, ".*") + ".o")
    $srcs << File.join(dir, f)
end

create_makefile "IceRuby"
