----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 07/07/2025 03:15:42 PM
-- Design Name: 
-- Module Name: apuf - Behavioral
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
use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity apuf is
    generic (
        CHALL_BITS: integer := 4;
        CONFIG:     std_logic_vector(1 downto 0) := x"1"
    );
    port (
        clk: in std_logic;
        ipulse: in std_logic;
        challenge: in  std_logic_vector(CHALL_BITS - 1 downto 0);
        response:  out std_logic
    );
end apuf;

architecture Behavioral of apuf is
    attribute DONT_TOUCH: boolean;
    attribute MARK_DEBUG: boolean;
    
    signal start_sig: std_logic_vector(1 downto 0);
    signal chain_out_sig: std_logic_vector(1 downto 0);
    
    attribute DONT_TOUCH of CHAIN_INST: label is true;
    
    attribute MARK_DEBUG of chain_out_sig: signal is true;
begin
    
    STARTER_INST: entity work.puf_starter 
    port map (
        CLK => clk,
        PULSE => ipulse,
        DATA_OUT => start_sig
    );
    
    CHAIN_INST: entity work.chain
    generic map (CHALL_BITS => CHALL_BITS)
    port map (
        CHALLENGE => challenge,
        UP_IN => start_sig(0),
        DOWN_IN => start_sig(1),
        
        UP_OUT => chain_out_sig(0),
        DOWN_OUT => chain_out_sig(1)
    );
    
    ARBITER_INST: entity work.arbiter(carrytap)
    generic map (
        TAP_IDX => to_integer(unsigned(CONFIG))
        --TAP_IDX => 2
    )
    port map (
        --CLK => clk, RST => ipulse,
        DATA => chain_out_sig,
        RESP => response
    );

end Behavioral;