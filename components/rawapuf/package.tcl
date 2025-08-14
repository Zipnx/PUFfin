#ipx::package_project -root_dir D:/Programs/Vivado/puffin/iprepo/rawapuf -vendor xilinx.com -library user -taxonomy /UserIP -import_files -set_current false
#ipx::unload_core d:/Programs/Vivado/puffin/iprepo/rawapuf/component.xml
#ipx::edit_ip_in_project -upgrade true -name tmp_edit_project -directory D:/Programs/Vivado/puffin/iprepo/rawapuf d:/Programs/Vivado/puffin/iprepo/rawapuf/component.xml
#current_project rawapuf
#set_property previous_version_for_upgrade xilinx.com:user:apuf_wrapper:1.0 [ipx::current_core]
#set_property core_revision 1 [ipx::current_core]
#ipx::create_xgui_files [ipx::current_core]
#ipx::update_checksums [ipx::current_core]
#ipx::save_core [ipx::current_core]
#current_project tmp_edit_project
#ipx::move_temp_component_back -component [ipx::current_core]
#close_project -delete
#update_ip_catalog -rebuild -repo_path d:/Programs/Vivado/puffin/iprepo/rawapuf

# Variables (adjust these as needed)
set ip_name "raw_apuf"
set ip_vendor "puffin"
set ip_library "user"
set ip_version "1.0"
set scriptdir [file dirname [info script]]
set ip_repo_path $scriptdir/../../iprepo

# Make sure we're in a project context
if { [current_project -quiet] eq "" } {
    puts "ERROR: No project is currently open. Open the component project first."
    exit 1
}

# Create the IP package into iprepo/<ip_name>
ipx::package_project -root_dir "$ip_repo_path/$ip_name" \
    -vendor $ip_vendor \
    -library $ip_library \
    -taxonomy /UserIP

# Set metadata for the IP
set core [ipx::current_core]
set_property display_name $ip_name $core
set_property name $ip_name $core
set_property version $ip_version $core
set_property description "Custom IP: $ip_name" $core

# Save the IP definition
ipx::save_core $core

puts "INFO: Packaged $ip_name to $ip_repo_path/$ip_name"