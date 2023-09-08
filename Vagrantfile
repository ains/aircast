unless Vagrant.has_plugin?('vagrant-vbguest')
  puts 'Installing vagrant-vbguest...'
  system 'vagrant plugin install vagrant-vbguest'
end


Vagrant.configure(2) do |config|
  config.vm.box = 'ubuntu/trusty64'
  config.vm.network 'public_network', bridge: 'en0: Wi-Fi (AirPort)'
  config.vm.hostname = 'aircast'

  config.vm.provider 'virtualbox' do |v|
    v.memory = 1024
    v.cpus = 2
  end

  # enable the sound card on the vm
  config.vm.provider :virtualbox do |vb|
    vb.customize [
      "modifyvm", :id,
      "--audio",           "alsa",
      "--audiocontroller", "hda"
    ]
  end
  config.vm.provision "shell", path: "provision.sh", privileged: false
end
