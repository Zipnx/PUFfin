----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 08/15/2025 12:29:13 PM
-- Design Name: 
-- Module Name: tl_auth - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity tl_auth is
    port (
        clk:        in  std_logic;
        rst:        in  std_logic;
        trigger:    in  std_logic;
        challenge:  in  std_logic_vector(31 downto 0);
        response:   out std_logic_vector(31 downto 0);
        busy:       out std_logic;
        
        -- RO Direct Communication signals to retrieve puf bits for obfuscation
        -- They are optional, can be set to constant LOW
        -- This is done because the raw PUF bits must be kept as far from the PS as possible
        trigger_ro_xchg:    in  std_logic;
        ro_req:             out std_logic;
        ro_res:             in  std_logic;
        ro_inbound:         in  std_logic_vector(31 downto 0);
        ro_loaded:          out std_logic
    );
end tl_auth;

architecture Behavioral of tl_auth is
    attribute MARK_DEBUG: boolean;
    
    component raw_apuf_0 
        port (
            CLK:          in std_logic; 
            TRIGGER:      in  std_logic;
            CHALLENGE:    in  std_logic_vector(31 downto 0);
            RESPONSE:     out std_logic_vector(31 downto 0);
            BUSY:         out std_logic
        );
    end component;
    
    signal apuf_trigger: std_logic := '0';
    signal apuf_resp:    std_logic_vector(31 downto 0); 
    signal apuf_busy:    std_logic;
    
    signal ec_rst:       std_logic := '0';
    signal ec_trigger:   std_logic := '0';
    signal ec_readen:    std_logic := '0';
    
    signal ro_loaded_internal:   std_logic := '0';
    
    signal obf_bits:  std_logic_vector(31 downto 0) := x"AAAAAAAA";
    signal obf_chall: std_logic_vector(31 downto 0);
    
    attribute MARK_DEBUG of apuf_resp, response: signal is true;
    
begin
    ro_loaded <= ro_loaded_internal;
    
    CTRL: entity work.controller
    port map (
        clk => clk, rst => rst,
        trigger   => trigger,
        apuf_trig => apuf_trigger,
        apuf_busy => apuf_busy,
        ec_rst    => ec_rst,
        ec_readen => ec_readen,
        ec_trig   => ec_trigger,
        ro_trig   => trigger_ro_xchg,
        ro_req    => ro_req,
        ro_res    => ro_res,
        ro_loaded => ro_loaded_internal,
        busy      => busy
        
    );
    
    OBF_INST: entity work.chall_obf(barebone)
    port map (
        iObfuscate => obf_bits,
        iChallenge => challenge,
        oChallenge => obf_chall
    );
    
    -- For now, these instances have bogus connections
    PUF_INST: raw_apuf_0 port map (
        CLK => clk,
        TRIGGER => apuf_trigger,
        CHALLENGE => obf_chall,
        RESPONSE  => apuf_resp,
        BUSY => apuf_busy
    );
    
    EC_INST: entity work.majpoll(hardcode)
    port map (
        iClk => clk, iRead => ec_readen, 
        iTrigger => ec_trigger, iRst => ec_rst,
        iData => apuf_resp, oData => response
    );

end Behavioral;
