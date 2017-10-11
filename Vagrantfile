# -*- mode: ruby -*-
# vi: set ft=ruby sw=2:

Vagrant.configure(2) do |config|
    # The most common configuration options are documented and commented below.
    # For a complete reference, please see the online documentation at
    # https://docs.vagrantup.com.

    # Every Vagrant development environment requires a box. You can search for
    # boxes at https://atlas.hashicorp.com/search.
    config.vm.box = "ubuntu/xenial64"

    # Forward a port from the guest to the host, which allows for outside
    # computers to access the VM, whereas host only networking does not.
    config.vm.network :private_network, ip: "182.16.0.5"
    config.vm.network :forwarded_port, guest: 22, host: 2235, id: 'ssh'

    config.vm.provider "virtualbox" do |v|
        v.memory = 1024
        v.cpus = 1
        v.name = "webinvoices"
    end

    config.vm.synced_folder ".", "/opt/webinvoices"

    ANSIBLE_HOST_VARS = { "default" => {
      "ansible_python_interpreter" => "/usr/bin/python3" ,
      "webinvoices_domain" => "webinvoices-local.dev",
      "deploy_in_vagrant" => true,
      "nginx_user" => "demo-client",
      "nginx_pass" => "demo-pass",
      "db" => "fakturi",
      "dbuser" => "vagrant",
      "dbpassword" => "vagrant",
    }}
    provisioner = Vagrant::Util::Platform.windows? ? :guest_ansible : :ansible

    config.vm.provision provisioner do |ansible|
      # ansible.verbose = "v"
      ansible.playbook = "ansible/install_web_app.yml"
      ansible.host_vars = ANSIBLE_HOST_VARS
    end

    config.vm.provision provisioner do |ansible|
      # ansible.verbose = "v"
      ansible.playbook = "ansible/create_database.yml"
      ansible.host_vars = ANSIBLE_HOST_VARS
    end

    config.vm.provision provisioner do |ansible|
      # ansible.verbose = "v"
      ansible.playbook = "ansible/web_app.yml"
      ansible.host_vars = ANSIBLE_HOST_VARS
    end

    config.vm.provision provisioner do |ansible|
      # ansible.verbose = "v"
      ansible.playbook = "ansible/html2pdf.yml"
      ansible.host_vars = ANSIBLE_HOST_VARS
    end

end
