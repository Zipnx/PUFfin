
connect
# TODO: Make more dynamic
#       Perhaps on the start of the script, run a target list to identify
#       the option to use here, could also leave it hardcoded for now,
#       and pray that all Zybo Z7-10s have the same
targets 2

source "{0}"
ps7_init
ps7_post_config

fpga -file "{1}"
dow "{2}"
con

