# -*- mode: ruby -*-
# vi: set ft=ruby sw=2:

Vagrant.configure(2) do |config|
    # The most common configuration options are documented and commented below.
    # For a complete reference, please see the online documentation at
    # https://docs.vagrantup.com.

    # Every Vagrant development environment requires a box. You can search for
    # boxes at https://atlas.hashicorp.com/search.
    config.vm.box = "bento/ubuntu-16.04"

    # Forward a port from the guest to the host, which allows for outside
	# computers to access the VM, whereas host only networking does not.
	config.vm.network :private_network, ip: "182.16.0.5"
    config.vm.network :forwarded_port, guest: 22, host: 2235, id: 'ssh'

    config.vm.provider "virtualbox" do |v|
        v.memory = 1024
        v.cpus = 1
        v.name = "webinvoices"
    end

    config.vm.synced_folder ".", "/home/vagrant/webinvoices"
    config.vm.provision :shell, path: "scripts/install.sh"
    config.vm.provision :shell, run: "always", :path => "scripts/update.sh", privileged: false
    config.vm.provision :shell, run: "always", :path => "scripts/startup.sh"
end
