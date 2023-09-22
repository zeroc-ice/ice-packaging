#
# Copyright (c) ZeroC, Inc. All rights reserved.
#

Gem::Specification.new do |s|
  s.name        = 'zeroc-ice'
  s.version     = '3.7.10'
  s.summary     = "ZeroC Ice for Ruby"
  s.description = <<-eos
The Internet Communications Engine (Ice) provides a robust, proven
platform for developing mission-critical networked applications
with minimal effort. Let Ice handle all of the low-level details
such as network connections, serialization, and concurrency so that
you can focus on your application logic.

This package includes the Ice extension for Ruby, the standard Slice
definition files, and the Slice-to-Ruby compiler. You will need to
install a full Ice distribution if you want to use other Ice language
mappings, or Ice services such as IceGrid, IceStorm and Glacier2.

We provide extensive online documentation for Ice, the Ruby extension,
and the other Ice language mappings and services.

Join us on our user forums if you have questions about Ice.
eos
  s.authors     = ["ZeroC, Inc."]
  s.email       = 'info@zeroc.com'
  s.files       = %w[ICE_LICENSE LICENSE MCPP_LICENSE ice.gemspec] + Dir.glob('lib/**/*.rb') + Dir.glob("ext/*") + Dir.glob("ext/**/*") + Dir.glob("slice/**/*.ice")
  s.homepage    = 'https://zeroc.com'
  s.license     = 'GPL-2.0'
  s.extensions = %w[ext/extconf.rb]
  s.rdoc_options = %w[--exclude=ext/IceRuby/.*\.o$ --exclude=IceRuby\.(bundle|so)$ --exclude=lib/slice2rb$]
  s.executables << 'slice2rb'
end
