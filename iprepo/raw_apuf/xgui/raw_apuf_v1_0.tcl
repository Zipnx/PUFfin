# Definitional proc to organize widgets for parameters.
proc init_gui { IPINST } {
  ipgui::add_param $IPINST -name "Component_Name"
  #Adding Page
  set Page_0 [ipgui::add_page $IPINST -name "Page 0"]
  ipgui::add_param $IPINST -name "BIT_WIDTH" -parent ${Page_0}
  ipgui::add_param $IPINST -name "CHALL_BITS" -parent ${Page_0}
  ipgui::add_param $IPINST -name "INTCONFIG" -parent ${Page_0}


}

proc update_PARAM_VALUE.BIT_WIDTH { PARAM_VALUE.BIT_WIDTH } {
	# Procedure called to update BIT_WIDTH when any of the dependent parameters in the arguments change
}

proc validate_PARAM_VALUE.BIT_WIDTH { PARAM_VALUE.BIT_WIDTH } {
	# Procedure called to validate BIT_WIDTH
	return true
}

proc update_PARAM_VALUE.CHALL_BITS { PARAM_VALUE.CHALL_BITS } {
	# Procedure called to update CHALL_BITS when any of the dependent parameters in the arguments change
}

proc validate_PARAM_VALUE.CHALL_BITS { PARAM_VALUE.CHALL_BITS } {
	# Procedure called to validate CHALL_BITS
	return true
}

proc update_PARAM_VALUE.INTCONFIG { PARAM_VALUE.INTCONFIG } {
	# Procedure called to update INTCONFIG when any of the dependent parameters in the arguments change
}

proc validate_PARAM_VALUE.INTCONFIG { PARAM_VALUE.INTCONFIG } {
	# Procedure called to validate INTCONFIG
	return true
}


proc update_MODELPARAM_VALUE.BIT_WIDTH { MODELPARAM_VALUE.BIT_WIDTH PARAM_VALUE.BIT_WIDTH } {
	# Procedure called to set VHDL generic/Verilog parameter value(s) based on TCL parameter value
	set_property value [get_property value ${PARAM_VALUE.BIT_WIDTH}] ${MODELPARAM_VALUE.BIT_WIDTH}
}

proc update_MODELPARAM_VALUE.CHALL_BITS { MODELPARAM_VALUE.CHALL_BITS PARAM_VALUE.CHALL_BITS } {
	# Procedure called to set VHDL generic/Verilog parameter value(s) based on TCL parameter value
	set_property value [get_property value ${PARAM_VALUE.CHALL_BITS}] ${MODELPARAM_VALUE.CHALL_BITS}
}

proc update_MODELPARAM_VALUE.INTCONFIG { MODELPARAM_VALUE.INTCONFIG PARAM_VALUE.INTCONFIG } {
	# Procedure called to set VHDL generic/Verilog parameter value(s) based on TCL parameter value
	set_property value [get_property value ${PARAM_VALUE.INTCONFIG}] ${MODELPARAM_VALUE.INTCONFIG}
}

